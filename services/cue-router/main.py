from __future__ import annotations

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any

import requests
import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from paho.mqtt import client as mqtt
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

try:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
except Exception:  # pragma: no cover
    OTLPSpanExporter = None


SERVICE_NAME = 'mcp4h-cue-router'
LOGGER = logging.getLogger(SERVICE_NAME)
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper(), format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')

PACKETS_TOTAL = Counter('mcp4h_router_packets_total', 'Packets seen by cue-router', ['source'])
ROUTE_TOTAL = Counter('mcp4h_router_route_total', 'Route target attempts', ['route', 'target_kind', 'status'])
POLICY_RELOAD_TOTAL = Counter('mcp4h_router_policy_reload_total', 'Policy reload attempts', ['status'])
ROUTE_LATENCY = Histogram('mcp4h_router_route_latency_seconds', 'Time spent routing packets')


class PolicyStore:
    def __init__(self, path: Path):
        self.path = path
        self.data: dict[str, Any] = {'defaults': {}, 'routes': []}
        self.mtime: float | None = None
        self.lock = threading.RLock()
        self.reload(force=True)

    def reload(self, force: bool = False) -> bool:
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            if force:
                LOGGER.warning('policy file missing at %s; using empty policy', self.path)
                with self.lock:
                    self.data = {'defaults': {}, 'routes': []}
                    self.mtime = None
                POLICY_RELOAD_TOTAL.labels(status='missing').inc()
            return False
        if not force and self.mtime is not None and stat.st_mtime <= self.mtime:
            return False
        try:
            loaded = yaml.safe_load(self.path.read_text(encoding='utf-8')) or {}
            if not isinstance(loaded, dict):
                raise ValueError('policy root must be a mapping')
            loaded.setdefault('defaults', {})
            loaded.setdefault('routes', [])
            with self.lock:
                self.data = loaded
                self.mtime = stat.st_mtime
            POLICY_RELOAD_TOTAL.labels(status='ok').inc()
            LOGGER.info('policy loaded from %s (%s routes)', self.path, len(loaded.get('routes', [])))
            return True
        except Exception:
            POLICY_RELOAD_TOTAL.labels(status='error').inc()
            LOGGER.exception('failed to reload policy from %s', self.path)
            return False

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return json.loads(json.dumps(self.data))


class RouterState:
    def __init__(self) -> None:
        self.policy_path = Path(os.getenv('CUE_ROUTER_POLICY', 'bridges/cue-router/policy.yaml'))
        self.policy = PolicyStore(self.policy_path)
        self.mqtt_host = os.getenv('MQTT_HOST', 'mqtt')
        self.mqtt_port = int(os.getenv('MQTT_PORT', '1883'))
        self.mqtt_client = mqtt.Client(client_id=os.getenv('CUE_ROUTER_CLIENT_ID', SERVICE_NAME))
        self.mqtt_connected = False
        self.reload_interval = float(os.getenv('POLICY_RELOAD_INTERVAL_SEC', '2'))
        self.shutdown = threading.Event()
        self.reloader_thread: threading.Thread | None = None
        self._configure_mqtt()

    def _configure_mqtt(self) -> None:
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.on_message = self._on_message

    def start(self) -> None:
        try:
            self.mqtt_client.connect_async(self.mqtt_host, self.mqtt_port, keepalive=30)
            self.mqtt_client.loop_start()
            LOGGER.info('connecting to mqtt at %s:%s', self.mqtt_host, self.mqtt_port)
        except Exception:
            LOGGER.exception('failed to start mqtt client')
        self.reloader_thread = threading.Thread(target=self._policy_reloader_loop, name='policy-reloader', daemon=True)
        self.reloader_thread.start()

    def stop(self) -> None:
        self.shutdown.set()
        try:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        except Exception:
            LOGGER.exception('failed to stop mqtt cleanly')

    def _policy_reloader_loop(self) -> None:
        while not self.shutdown.wait(self.reload_interval):
            self.policy.reload(force=False)

    def _source_topics(self) -> list[str]:
        snapshot = self.policy.snapshot()
        topics = snapshot.get('defaults', {}).get('source_topics') or os.getenv('MQTT_SOURCE_TOPICS', 'mcp4h/cues').split(',')
        return [topic.strip() for topic in topics if str(topic).strip()]

    def _on_connect(self, client: mqtt.Client, userdata: Any, flags: dict[str, Any], rc: int) -> None:
        self.mqtt_connected = (rc == 0)
        if rc != 0:
            LOGGER.error('mqtt connect failed rc=%s', rc)
            return
        topics = self._source_topics()
        for topic in topics:
            client.subscribe(topic)
            LOGGER.info('subscribed to mqtt topic: %s', topic)

    def _on_disconnect(self, client: mqtt.Client, userdata: Any, rc: int) -> None:
        self.mqtt_connected = False
        LOGGER.warning('mqtt disconnected rc=%s', rc)

    def _on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
        except Exception:
            LOGGER.exception('discarding non-json mqtt payload on %s', msg.topic)
            return
        route_packet(payload, source='mqtt', inbound_topic=msg.topic)


state = RouterState()
app = FastAPI(title='MCP4H Cue Router', version='0.1.0')


def configure_tracing() -> None:
    resource = Resource.create({'service.name': SERVICE_NAME})
    provider = TracerProvider(resource=resource)
    otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')
    if otlp_endpoint and OTLPSpanExporter is not None:
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint)))
    elif os.getenv('OTEL_TRACES_EXPORTER', '').lower() == 'console':
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()


configure_tracing()
TRACER = trace.get_tracer(SERVICE_NAME)


def extract_urgency(packet: dict[str, Any]) -> str | None:
    return packet.get('metadata', {}).get('urgency') or packet.get('urgency')


def extract_platform(packet: dict[str, Any]) -> str | None:
    if isinstance(packet.get('origin'), dict):
        return packet['origin'].get('platform')
    if isinstance(packet.get('header'), dict):
        return packet['header'].get('source')
    return None


def render_text(packet: dict[str, Any], route_name: str) -> str:
    text = packet.get('text')
    if not text:
        text = packet.get('payload', {}).get('text')
    if not text and packet.get('action_hint'):
        text = f"{packet.get('signal', 'cue')}: {packet.get('action_hint')}"
    if not text:
        text = json.dumps(packet, ensure_ascii=False)
    packet_id = packet.get('id') or packet.get('message_id') or 'unknown'
    platform = extract_platform(packet) or 'unknown'
    urgency = extract_urgency(packet) or 'unspecified'
    return f"[{route_name}] {platform} · urgency={urgency} · id={packet_id}\n{text}"


def matches(packet: dict[str, Any], matcher: dict[str, Any]) -> bool:
    if not matcher:
        return True
    urgency = extract_urgency(packet)
    platform = extract_platform(packet)
    relation = packet.get('origin', {}).get('relation') if isinstance(packet.get('origin'), dict) else None
    if matcher.get('urgency_in') and urgency not in set(matcher['urgency_in']):
        return False
    if matcher.get('origin_platforms') and platform not in set(matcher['origin_platforms']):
        return False
    if matcher.get('relations') and relation not in set(matcher['relations']):
        return False
    if matcher.get('version_in') and packet.get('version') not in set(matcher['version_in']):
        return False
    if matcher.get('requires_text') and not (packet.get('text') or packet.get('payload', {}).get('text')):
        return False
    return True


def publish_mqtt(target: dict[str, Any], packet: dict[str, Any]) -> tuple[bool, str]:
    if not state.mqtt_connected:
        return False, 'mqtt not connected'
    topic = target.get('topic') or state.policy.snapshot().get('defaults', {}).get('mqtt_fallback_topic', 'mcp4h/routed/default')
    result = state.mqtt_client.publish(topic, json.dumps(packet, ensure_ascii=False), qos=int(target.get('qos', 0)), retain=bool(target.get('retain', False)))
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        return False, f'mqtt publish rc={result.rc}'
    return True, topic


def resolve_url(target: dict[str, Any]) -> str | None:
    if target.get('url'):
        return str(target['url'])
    if target.get('url_env'):
        return os.getenv(str(target['url_env']))
    return None


def post_slack(target: dict[str, Any], packet: dict[str, Any], route_name: str) -> tuple[bool, str]:
    url = resolve_url(target)
    if not url:
        return False, 'missing slack webhook url'
    response = requests.post(url, json={'text': render_text(packet, route_name)}, timeout=float(os.getenv('ROUTER_HTTP_TIMEOUT_SEC', '5')))
    return response.ok, f'http {response.status_code}'


def post_teams(target: dict[str, Any], packet: dict[str, Any], route_name: str) -> tuple[bool, str]:
    url = resolve_url(target)
    if not url:
        return False, 'missing teams webhook url'
    body = {
        '@type': 'MessageCard',
        '@context': 'https://schema.org/extensions',
        'summary': 'MCP4H cue',
        'themeColor': '0076D7',
        'text': render_text(packet, route_name),
    }
    response = requests.post(url, json=body, timeout=float(os.getenv('ROUTER_HTTP_TIMEOUT_SEC', '5')))
    return response.ok, f'http {response.status_code}'


def dispatch_target(route_name: str, target: dict[str, Any], packet: dict[str, Any]) -> tuple[bool, str]:
    kind = str(target.get('kind', '')).strip()
    if kind == 'mqtt':
        return publish_mqtt(target, packet)
    if kind == 'slack_webhook':
        return post_slack(target, packet, route_name)
    if kind == 'teams_webhook':
        return post_teams(target, packet, route_name)
    return False, f'unsupported target kind: {kind}'


def route_packet(packet: dict[str, Any], source: str, inbound_topic: str | None = None) -> dict[str, Any]:
    PACKETS_TOTAL.labels(source=source).inc()
    with TRACER.start_as_current_span('route_packet'):
        start = time.perf_counter()
        policy = state.policy.snapshot()
        decisions: list[dict[str, Any]] = []
        for route in policy.get('routes', []):
            if not route.get('enabled', True):
                continue
            route_name = route.get('name', 'unnamed-route')
            if not matches(packet, route.get('matcher', {})):
                continue
            for target in route.get('targets', []):
                kind = str(target.get('kind', 'unknown'))
                ok, detail = dispatch_target(route_name, target, packet)
                ROUTE_TOTAL.labels(route=route_name, target_kind=kind, status='ok' if ok else 'error').inc()
                decisions.append({'route': route_name, 'target_kind': kind, 'ok': ok, 'detail': detail})
        ROUTE_LATENCY.observe(time.perf_counter() - start)
        LOGGER.info('routed packet source=%s topic=%s decisions=%s', source, inbound_topic or '-', len(decisions))
        return {'accepted': True, 'source': source, 'inbound_topic': inbound_topic, 'decisions': decisions}


@app.on_event('startup')
def on_startup() -> None:
    state.start()
    LOGGER.info('cue-router ready on :8090')


@app.on_event('shutdown')
def on_shutdown() -> None:
    state.stop()


@app.get('/healthz')
def healthz() -> dict[str, Any]:
    policy = state.policy.snapshot()
    return {
        'status': 'ok',
        'service': SERVICE_NAME,
        'mqtt_connected': state.mqtt_connected,
        'policy_path': str(state.policy_path),
        'policy_routes': len(policy.get('routes', [])),
        'policy_mtime': state.policy.mtime,
    }


@app.get('/readyz')
def readyz() -> JSONResponse:
    ready = state.policy_path.exists()
    status = 200 if ready else 503
    return JSONResponse({'ready': ready, 'mqtt_connected': state.mqtt_connected}, status_code=status)


@app.get('/metrics')
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest().decode('utf-8'), media_type=CONTENT_TYPE_LATEST)


@app.post('/admin/reload')
def reload_policy() -> dict[str, Any]:
    changed = state.policy.reload(force=True)
    return {'reloaded': changed, 'policy_path': str(state.policy_path)}


@app.post('/route')
def route_endpoint(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise HTTPException(status_code=400, detail='packet must be a JSON object')
    return route_packet(packet, source='http')
