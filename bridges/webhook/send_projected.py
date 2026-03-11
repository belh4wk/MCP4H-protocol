#!/usr/bin/env python3
"""
send_projected.py

One-command webhook test for MCP4H projected payload cues.

Posts the entire MCP4H packet (or optionally the first cue payload) to the given URL.

Usage:
  python bridges/webhook/send_projected.py --url https://example --input examples/messages/mcp/mcp_event_projected_payload.json
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path
from typing import Any, Dict

REPO = Path(__file__).resolve().parents[2]

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_bytes().decode("utf-8-sig"))

def post_json(url: str, obj: Any) -> int:
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.getcode()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--cue-only", action="store_true", help="Send only the first cue payload instead of the full packet")
    args = ap.parse_args()

    inp = (REPO / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    pkt = load_json(inp)

    obj: Any = pkt
    if args.cue_only:
        cues = pkt.get("cues") or []
        if cues and isinstance(cues, list) and isinstance(cues[0], dict):
            obj = cues[0].get("payload", {})
        else:
            obj = {}

    code = post_json(args.url, obj)
    print(f"POST {args.url} -> HTTP {code}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
