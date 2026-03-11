#!/usr/bin/env python3
"""
MCP4H MCP server (stdio JSON-RPC 2.0) — Windows-hardened + local-ref-safe validator.

This single file intentionally bundles ALL fixes so you stop bouncing between partial drop-ins:

1) Windows PowerShell piping:
   - Reads sys.stdin.buffer (bytes)
   - Decodes UTF-8 (with BOM) and UTF-16LE/BE (PowerShell 5.1 default) safely

2) Local JSON loading:
   - Uses utf-8-sig so schema/example files with a UTF-8 BOM still parse

3) Schema $ref resolution (no HTTP 404, no broken file URIs):
   - Overrides schema["$id"] to local file:///... URI for validation
   - RefResolver handlers:
       * http/https: map https://example.com/<path> -> <repo>/<path> if exists
       * file: decode file:/// URIs and normalize Windows backslashes
   - Collapses accidental duplicate path segments (e.g., spec/spec -> spec)

Exposes:
- tools: mcp4h.validate, mcp4h.normalize, mcp4h.map_tool_result, mcp4h.webhook.publish, mcp4h.publish (stub)
- resources: schema v0.1, schema v0.1.1, examples index + examples read
"""

from __future__ import annotations

import json
import sys
import uuid
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse, unquote
import urllib.request

# Process-local policy state (only persists while this server process is running)
_policy_last_sent = {}
_policy_last_hash = {}


try:
    from jsonschema import Draft202012Validator
    from jsonschema import RefResolver
except Exception:
    Draft202012Validator = None
    RefResolver = None

REPO = Path(__file__).resolve().parents[3]
SCHEMA_V01 = REPO / "spec" / "schema" / "mcp4h-v0.1.json"
SCHEMA_V011 = REPO / "schemas" / "mcp4h-0.1.1.schema.json"
EXAMPLES_CANON = REPO / "examples" / "messages"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    # Tolerate UTF-8 BOM in JSON files (common on Windows).
    return json.loads(path.read_bytes().decode("utf-8-sig"))

def post_json(url: str, obj: Any, timeout_s: float = 10.0) -> int:
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return int(resp.getcode())



def ensure_jsonschema() -> None:
    if Draft202012Validator is None:
        raise RuntimeError("jsonschema is not available. Install requirements.txt for this repo.")


def schema_for(version: str) -> Path:
    v = (version or "").strip()
    if v in ("0.1", "v0.1", "mcp4h/0.1"):
        return SCHEMA_V01
    return SCHEMA_V011


def http_uri_to_local(uri: str) -> Path:
    # https://example.com/<path> -> <repo>/<path>
    u = urlparse(uri)
    rel = unquote(u.path).lstrip("/")
    return (REPO / rel).resolve()


def file_uri_to_path(uri: str) -> Path:
    """Convert file:/// URIs into local Paths on Windows/Linux; normalize backslashes."""
    u = urlparse(uri)
    p = unquote(u.path)
    p = p.replace("\\", "/")
    # Windows drive letter: "/D:/foo" -> "D:/foo"
    if sys.platform.startswith("win") and len(p) >= 3 and p[0] == "/" and p[2] == ":":
        p = p[1:]
    return Path(p)


def collapse_duplicate_segments(p: Path) -> Path:
    parts = list(p.parts)
    if not parts:
        return p
    new_parts = [parts[0]]
    for part in parts[1:]:
        if part == new_parts[-1]:
            continue
        new_parts.append(part)
    try:
        return Path(*new_parts)
    except Exception:
        return p


def validate_packet(packet: Dict[str, Any], version_hint: str | None = None) -> Dict[str, Any]:
    ensure_jsonschema()

    version = version_hint or packet.get("version") or "mcp4h/0.1.1"
    schema_path = schema_for(str(version))
    if not schema_path.exists():
        return {"ok": False, "errors": [f"Schema not found: {schema_path}"], "warnings": []}

    schema = load_json(schema_path)

    # Force $id to local file URI so jsonschema doesn't try HTTP for relative $refs.
    schema["$id"] = schema_path.resolve().as_uri()

    Draft202012Validator.check_schema(schema)

    def http_handler(uri: str):
        p = http_uri_to_local(uri)
        if p.exists():
            return load_json(p)
        raise FileNotFoundError(uri)

    def file_handler(uri: str):
        p = file_uri_to_path(uri)
        if p.exists():
            return load_json(p)

        pc = collapse_duplicate_segments(p)
        if pc != p and pc.exists():
            return load_json(pc)

        # If a repo-relative path got wrapped as file://, try resolving from repo root
        try_rel = (REPO / str(p).lstrip("/")).resolve()
        if try_rel.exists():
            return load_json(try_rel)

        try_rel_c = collapse_duplicate_segments(try_rel)
        if try_rel_c != try_rel and try_rel_c.exists():
            return load_json(try_rel_c)

        raise FileNotFoundError(str(pc))

    resolver = None
    if RefResolver is not None:
        resolver = RefResolver(
            base_uri=schema_path.resolve().as_uri(),
            referrer=schema,
            handlers={"http": http_handler, "https": http_handler, "file": file_handler},
        )

    errors: List[str] = []
    try:
        Draft202012Validator(schema, resolver=resolver).validate(packet)
    except Exception as e:
        errors.append(str(e))

    return {"ok": len(errors) == 0, "errors": errors, "warnings": [], "schema": str(schema.get("$id", schema_path.name))}



def map_mcp_tool_event_to_packet(ev: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonical MCP -> MCP4H mapping.
    Input is a simple event dict:
      {server, tool, trace_id, method, status, summary, details}
    Output is an MCP4H v0.1.1 envelope containing one projected payload cue.
    """
    status = str(ev.get("status", "ok")).strip().lower()
    summary = str(ev.get("summary", "Tool result received.")).strip()
    details = str(ev.get("details", "")).strip()

    cue_ts = iso_now()

    def led_for(status_s: str) -> Dict[str, Any]:
        if status_s == "error":
            return {"color": "#FF3344", "blink_hz": 4, "ttl_ms": 600}
        return {"color": "#00FF66", "blink_hz": 2, "ttl_ms": 300}

    pkt = {
        "version": "mcp4h/0.1.1",
        "id": str(uuid.uuid4()),
        "timestamp": cue_ts,
        "origin": {"platform": "mcp", "relation": "telemetry"},
        "actor": {"role": "system", "handle": "agent:local"},
        "text": summary if not details else f"{summary} {details}".strip(),
        "metadata": {
            "heat": 0,
            "valence": "neutral",
            "domain_profile": "comms.toolcall",
            "mcp": {
                "server": ev.get("server", "unknown"),
                "tool": ev.get("tool", "unknown"),
                "trace_id": ev.get("trace_id", ""),
                "method": ev.get("method", "tools/call"),
            },
        },
        "cues": [
            {
                "id": "cue-proj-001",
                "ts": cue_ts,
                "channel": "multi",
                "intent": "inform" if status != "error" else "warning",
                "payload": {
                    "text": {
                        "short": summary[:180],
                        "long": (details if details else summary)[:1200],
                        "style": "neutral" if status != "error" else "urgent",
                    },
                    "visual": {"led": led_for(status)},
                    "audio": {"mode": "beep", "beep": "single" if status != "error" else "double"},
                    "haptic": {
                        "pattern": "double_tap" if status != "error" else "triple_tap",
                        "intensity": 0.4 if status != "error" else 0.7,
                        "duration_ms": 180,
                    },
                },
            }
        ],
    }
    return pkt

def normalize_input(inp: Any) -> Dict[str, Any]:
    # Minimal on-ramp that matches your stricter v0.1.1 envelope patterns.
    if isinstance(inp, dict) and "version" in inp:
        return {"ok": True, "packet": inp}

    pkt = {
        "version": "mcp4h/0.1.1",
        "id": str(uuid.uuid4()),
        "timestamp": iso_now(),
        "origin": {"platform": "mcp", "relation": "telemetry"},
        "actor": {"role": "system", "handle": "agent:local"},
        "text": "Normalized input",
        "metadata": {"heat": 0, "valence": "neutral"},
        "cues": [],
    }
    return {"ok": True, "packet": pkt}


def publish_stub(packet: Dict[str, Any], target: str) -> Dict[str, Any]:
    return {"ok": True, "published": True, "target": target, "id": packet.get("id"), "timestamp": iso_now()}


TOOLS = [
    {"name": "mcp4h.validate", "description": "Validate an MCP4H packet.", "inputSchema": {"type": "object", "properties": {"packet": {"type": "object"}, "version": {"type": "string"}}, "required": ["packet"]}},
    {"name": "mcp4h.normalize", "description": "Wrap input into an MCP4H packet (on-ramp).", "inputSchema": {"type": "object", "properties": {"input": {}}, "required": ["input"]}},
        {"name": "mcp4h.map_tool_result", "description": "Map a simple MCP tool event/result into an MCP4H v0.1.1 packet with a projected payload cue (canonical).", "inputSchema": {"type": "object", "properties": {"event": {"type": "object"}}, "required": ["event"]}},
    {"name": "mcp4h.webhook.publish", "description": "POST an MCP4H packet (or projected cue payload) to a webhook URL. Optionally validate first.", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}, "packet": {"type": "object"}, "cue_only": {"type": "boolean", "default": True}, "validate": {"type": "boolean", "default": False}, "timeout_s": {"type": "number", "default": 10}, "cooldown_ms": {"type": "integer", "default": 0}, "dedupe_window_ms": {"type": "integer", "default": 0}, "dedupe_key": {"type": "string", "default": "mcp.trace_id"}}, "required": ["url", "packet"]}},
{"name": "mcp4h.publish", "description": "Publish an MCP4H packet (stub).", "inputSchema": {"type": "object", "properties": {"packet": {"type": "object"}, "target": {"type": "string"}}, "required": ["packet"]}},
]


def resources_list() -> List[Dict[str, Any]]:
    return [
        {"uri": "mcp4h://schema/v0.1", "name": "MCP4H schema v0.1", "mimeType": "application/json"},
        {"uri": "mcp4h://schema/v0.1.1", "name": "MCP4H schema v0.1.1", "mimeType": "application/json"},
        {"uri": "mcp4h://examples/messages/index", "name": "Examples index (canonical)", "mimeType": "application/json"},
    ]


def resources_read(uri: str) -> Dict[str, Any]:
    if uri == "mcp4h://examples/messages/index":
        files = sorted([p.relative_to(EXAMPLES_CANON).as_posix() for p in EXAMPLES_CANON.rglob("*.json")]) if EXAMPLES_CANON.exists() else []
        return {"contents": [{"type": "text", "text": json.dumps(files, indent=2)}]}

    if uri.startswith("mcp4h://examples/messages/"):
        rel = uri[len("mcp4h://examples/messages/"):]
        p = (EXAMPLES_CANON / rel).resolve()
        return {"contents": [{"type": "text", "text": p.read_bytes().decode("utf-8-sig")}]}

    if uri == "mcp4h://schema/v0.1":
        return {"contents": [{"type": "text", "text": SCHEMA_V01.read_bytes().decode("utf-8-sig")}]}
    if uri == "mcp4h://schema/v0.1.1":
        return {"contents": [{"type": "text", "text": SCHEMA_V011.read_bytes().decode("utf-8-sig")}]}

    raise KeyError(uri)


def ok_response(req_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def err_response(req_id: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
    e: Dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        e["data"] = data
    return {"jsonrpc": "2.0", "id": req_id, "error": e}


def handle(method: str, params: Dict[str, Any]) -> Any:
    if method == "initialize":
        return {"serverInfo": {"name": "mcp4h-mcp-server", "version": "0.0.1"}, "capabilities": {"tools": True, "resources": True}}
    if method == "ping":
        return {"ok": True, "timestamp": iso_now()}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        if name == "mcp4h.validate":
            pkt = args.get("packet")
            if not isinstance(pkt, dict):
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": ["'packet' must be an object"], "warnings": []}, indent=2)}]}
            res = validate_packet(pkt, args.get("version"))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        if name == "mcp4h.normalize":
            res = normalize_input(args.get("input"))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        if name == "mcp4h.map_tool_result":
            ev = args.get("event")
            if not isinstance(ev, dict):
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": ["'event' must be an object"], "warnings": []}, indent=2)}]}
            pkt = map_mcp_tool_event_to_packet(ev)
            return {"content": [{"type": "text", "text": json.dumps({"ok": True, "packet": pkt}, indent=2)}]}
        if name == "mcp4h.webhook.publish":
            url = args.get("url")
            pkt = args.get("packet")
            cue_only = bool(args.get("cue_only", True))
            do_validate = bool(args.get("validate", False))
            timeout_s = float(args.get("timeout_s", 10.0))
            if not isinstance(url, str) or not url.strip():
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": ["'url' must be a non-empty string"], "warnings": []}, indent=2)}]}
            if not isinstance(pkt, dict):
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": ["'packet' must be an object"], "warnings": []}, indent=2)}]}
            if do_validate:
                res = validate_packet(pkt, args.get("version"))
                if not res.get("ok"):
                    return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": res.get("errors", []), "warnings": res.get("warnings", [])}, indent=2)}]}
            body = pkt
            if cue_only:
                cues = pkt.get("cues") or []
                if isinstance(cues, list) and cues and isinstance(cues[0], dict):
                    body = cues[0].get("payload", {})
                else:
                    body = {}

            # Optional policy (process-local; for real streams use bridges/webhook/bridge.py policy flags)
            cooldown_ms = int(args.get("cooldown_ms", 0) or 0)
            dedupe_window_ms = int(args.get("dedupe_window_ms", 0) or 0)
            dedupe_key = str(args.get("dedupe_key", "mcp.trace_id") or "mcp.trace_id")

            def _get_key(pkt_obj: dict) -> str:
                if dedupe_key.startswith("mcp."):
                    md = pkt_obj.get("metadata", {})
                    mcp = md.get("mcp", {}) if isinstance(md, dict) else {}
                    return str(mcp.get(dedupe_key.split(".",1)[1], "global"))
                return "global"

            k = _get_key(pkt)
            now = time.time()
            if cooldown_ms > 0:
                last = _policy_last_sent.get(k, 0.0)
                if (now - last) * 1000.0 < cooldown_ms:
                    return {"content": [{"type": "text", "text": json.dumps({"ok": True, "http_status": 0, "dropped": "cooldown"}, indent=2)}]}

            if dedupe_window_ms > 0:
                h = json.dumps(body, sort_keys=True, separators=(",", ":"))
                prev = _policy_last_hash.get(k)
                if prev:
                    prev_h, prev_t = prev
                    if h == prev_h and (now - prev_t) * 1000.0 < dedupe_window_ms:
                        return {"content": [{"type": "text", "text": json.dumps({"ok": True, "http_status": 0, "dropped": "dedupe"}, indent=2)}]}
                _policy_last_hash[k] = (h, now)
            try:
                code = post_json(url, body, timeout_s=timeout_s)
                _policy_last_sent[k] = time.time()
                return {"content": [{"type": "text", "text": json.dumps({"ok": True, "http_status": code}, indent=2)}]}
            except Exception as e:
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "errors": [str(e)]}, indent=2)}]}
        if name == "mcp4h.publish":
            pkt = args.get("packet")
            tgt = args.get("target") or "stdout"
            if not isinstance(pkt, dict):
                return {"content": [{"type": "text", "text": json.dumps({"ok": False, "error": "'packet' must be an object"}, indent=2)}]}
            res = publish_stub(pkt, tgt)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        raise KeyError(f"Unknown tool: {name}")
    if method == "resources/list":
        return {"resources": resources_list()}
    if method == "resources/read":
        uri = params.get("uri")
        if not uri:
            raise RuntimeError("Missing uri")
        return resources_read(uri)
    raise KeyError(f"Unknown method: {method}")


def decode_stdin_line(raw: bytes) -> str:
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    return raw.decode("utf-8")


def main() -> None:
    for raw in sys.stdin.buffer:
        try:
            line = decode_stdin_line(raw).strip()
            if not line:
                continue
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params") or {}
            result = handle(method, params)
            sys.stdout.write(json.dumps(ok_response(req_id, result), ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            req_id = None
            try:
                if isinstance(req, dict):
                    req_id = req.get("id")
            except Exception:
                pass
            sys.stdout.write(json.dumps(err_response(req_id, -32000, "Server error", {"detail": str(e)}), ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
