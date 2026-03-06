#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests
from paho.mqtt import client as mqtt


def load_packets(path: Path):
    text = path.read_text(encoding='utf-8').strip()
    if not text:
        return []
    if path.suffix.lower() in {'.jsonl', '.ndjson'}:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    return [data]


def send_http(packets, url: str, interval_sec: float) -> None:
    for idx, packet in enumerate(packets, start=1):
        response = requests.post(url, json=packet, timeout=10)
        print(f'[{idx}] HTTP {response.status_code} {response.text}')
        if interval_sec:
            time.sleep(interval_sec)


def send_mqtt(packets, host: str, port: int, topic: str, interval_sec: float) -> None:
    client = mqtt.Client(client_id='mcp4h-replay-cli')
    client.connect(host, port, keepalive=30)
    client.loop_start()
    try:
        for idx, packet in enumerate(packets, start=1):
            payload = json.dumps(packet, ensure_ascii=False)
            result = client.publish(topic, payload)
            print(f'[{idx}] MQTT rc={result.rc} topic={topic}')
            if interval_sec:
                time.sleep(interval_sec)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replay MCP4H packets to cue-router over HTTP or MQTT.')
    parser.add_argument('file', type=Path, help='Input .json, .jsonl, or .ndjson file')
    parser.add_argument('--transport', choices=['http', 'mqtt'], default='http')
    parser.add_argument('--url', default='http://localhost:8090/route')
    parser.add_argument('--mqtt-host', default='localhost')
    parser.add_argument('--mqtt-port', type=int, default=1883)
    parser.add_argument('--topic', default='mcp4h/cues')
    parser.add_argument('--interval-ms', type=int, default=250)
    args = parser.parse_args()

    packets = load_packets(args.file)
    interval_sec = max(args.interval_ms, 0) / 1000.0
    if args.transport == 'http':
        send_http(packets, args.url, interval_sec)
    else:
        send_mqtt(packets, args.mqtt_host, args.mqtt_port, args.topic, interval_sec)
