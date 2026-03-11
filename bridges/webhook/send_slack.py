#!/usr/bin/env python3
"""
bridges/webhook/send_slack.py

Send an MCP4H projected payload cue to a Slack Incoming Webhook URL.

Input can be:
- an MCP4H packet JSON (we'll pick first cue payload), or
- a projected payload JSON (text/visual/audio/haptic)

Usage:
  python bridges/webhook/send_slack.py --url "https://hooks.slack.com/services/..." --input out_mcp4h.json
  python bridges/webhook/send_slack.py --url "..." --input projected_payload.json --payload-only
"""
from __future__ import annotations
import argparse, json, urllib.request
from pathlib import Path
from typing import Any, Dict

def load_json(path: Path) -> Any:
    return json.loads(path.read_bytes().decode("utf-8-sig"))

def post(url: str, obj: Any) -> int:
    data=json.dumps(obj).encode("utf-8")
    req=urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return int(resp.getcode())

def get_payload(obj: Any, payload_only: bool) -> Dict[str, Any]:
    if payload_only:
        return obj if isinstance(obj, dict) else {"raw": obj}
    if isinstance(obj, dict) and "cues" in obj:
        cues=obj.get("cues") or []
        if cues and isinstance(cues[0], dict):
            return cues[0].get("payload", {}) or {}
    return obj if isinstance(obj, dict) else {"raw": obj}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--payload-only", action="store_true")
    args=ap.parse_args()

    obj=load_json(Path(args.input))
    p=get_payload(obj, args.payload_only)

    txt=p.get("text", {}) if isinstance(p, dict) else {}
    short=str(txt.get("short","")).strip() or "MCP4H cue"
    long=str(txt.get("long","")).strip()

    vis=(p.get("visual", {}) if isinstance(p, dict) else {})
    led=(vis.get("led", {}) if isinstance(vis, dict) else {})
    color=str(led.get("color","#999999"))

    blocks=[
        {"type":"header","text":{"type":"plain_text","text":short[:150]}},
        {"type":"section","text":{"type":"mrkdwn","text":long[:2900] if long else "_(no details)_"}},
        {"type":"context","elements":[{"type":"mrkdwn","text":f"*LED:* `{color}`  *Source:* MCP4H"}]},
    ]
    payload={"blocks":blocks}

    code=post(args.url, payload)
    print(f"POST Slack -> HTTP {code}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
