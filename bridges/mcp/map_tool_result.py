#!/usr/bin/env python3
"""
bridges/mcp/map_tool_result.py

Map a simple MCP tool event/result into a schema-valid MCP4H v0.1.1 envelope
containing a single **projected payload** cue (canonical path).

Input (recommended shape):
{
  "server": "mcp-server-local",
  "tool": "filesystem.read",
  "trace_id": "trace_abc",
  "method": "tools/call",
  "status": "ok" | "error",
  "summary": "Tool completed",
  "details": "filesystem.read returned text."
}

Outputs:
- --output <file.json> writes a normal JSON file
- --output-jsonl <file.jsonl> writes one JSON object per line (append by default)
  Use --truncate to overwrite the JSONL file.

Examples:

# Write JSON
python bridges/mcp/map_tool_result.py --input examples/messages/mcp/mcp_tool_event_example.json --output out_mcp4h.json

# Append JSONL (continuous bridge input)
python bridges/mcp/map_tool_result.py --input examples/messages/mcp/mcp_tool_event_example.json --output-jsonl packets.jsonl

# Overwrite JSONL then run bridge once
python bridges/mcp/map_tool_result.py --input examples/messages/mcp/mcp_tool_event_example.json --output-jsonl packets.jsonl --truncate
Get-Content .\\packets.jsonl | python .\\bridges\\webhook\\bridge.py --url "http://127.0.0.1:8080/" --cue-only --validate --once
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPO = Path(__file__).resolve().parents[2]


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj: Any, truncate: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if truncate else "a"
    with path.open(mode, encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def severity_to_led(status: str) -> Dict[str, Any]:
    s = status.lower().strip()
    if s == "error":
        return {"color": "#FF3344", "blink_hz": 4, "ttl_ms": 600}
    return {"color": "#00FF66", "blink_hz": 2, "ttl_ms": 300}


def build_packet(ev: Dict[str, Any], *, platform: str, relation: str, heat: int, valence: str) -> Dict[str, Any]:
    status = str(ev.get("status", "ok"))
    summary = str(ev.get("summary", "Tool result received."))
    details = str(ev.get("details", ""))

    cue_ts = iso_now()
    pkt = {
        "version": "mcp4h/0.1.1",
        "id": str(uuid.uuid4()),
        "timestamp": cue_ts,
        "origin": {"platform": platform, "relation": relation},
        "actor": {"role": "system", "handle": "agent:local"},
        "text": summary if not details else f"{summary} {details}".strip(),
        "metadata": {
            "heat": int(heat),
            "valence": valence,
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
                "intent": "inform" if status.lower() != "error" else "warning",
                "payload": {
                    "text": {
                        "short": summary[:180],
                        "long": (details if details else summary)[:1200],
                        "style": "neutral" if status.lower() != "error" else "urgent",
                    },
                    "visual": {"led": severity_to_led(status)},
                    "audio": {"mode": "beep", "beep": "single" if status.lower() != "error" else "double"},
                    "haptic": {
                        "pattern": "double_tap" if status.lower() != "error" else "triple_tap",
                        "intensity": 0.4 if status.lower() != "error" else 0.7,
                        "duration_ms": 180,
                    },
                },
            }
        ],
    }
    return pkt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", help="Write MCP4H packet as JSON to this path")
    ap.add_argument("--output-jsonl", help="Append MCP4H packet as one-line JSON to this JSONL file (continuous mode input)")
    ap.add_argument("--truncate", action="store_true", help="If set with --output-jsonl, overwrite the JSONL file instead of appending")
    ap.add_argument("--platform", default="mcp")
    ap.add_argument("--relation", default="telemetry")
    ap.add_argument("--heat", type=int, default=0)
    ap.add_argument("--valence", default="neutral")
    args = ap.parse_args()

    if not args.output and not args.output_jsonl:
        ap.error("Provide --output or --output-jsonl (or both).")

    inp = (REPO / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    ev = load_json(inp)

    pkt = build_packet(ev, platform=args.platform, relation=args.relation, heat=args.heat, valence=args.valence)

    if args.output:
        outp = (REPO / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
        write_json(outp, pkt)
        print(f"Wrote JSON: {outp}")

    if args.output_jsonl:
        outjl = (REPO / args.output_jsonl).resolve() if not Path(args.output_jsonl).is_absolute() else Path(args.output_jsonl)
        append_jsonl(outjl, pkt, truncate=args.truncate)
        print(f"Wrote JSONL: {outjl} (truncate={args.truncate})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
