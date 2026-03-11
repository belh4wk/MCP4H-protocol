#!/usr/bin/env python3
"""
bridges/webhook/send_teams.py

Send an MCP4H projected payload cue to a Microsoft Teams Incoming Webhook URL.

Input can be:
- MCP4H packet JSON (uses first cue payload), or
- projected payload JSON (text/visual/audio/haptic)

Usage:
  python bridges/webhook/send_teams.py --url "https://.../webhookb2/..." --input out_mcp4h.json
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

def get_payload(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict) and "cues" in obj:
        cues=obj.get("cues") or []
        if cues and isinstance(cues[0], dict):
            return cues[0].get("payload", {}) or {}
    return obj if isinstance(obj, dict) else {"raw": obj}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--input", required=True)
    args=ap.parse_args()

    obj=load_json(Path(args.input))
    p=get_payload(obj)

    txt=p.get("text", {}) if isinstance(p, dict) else {}
    title=str(txt.get("short","")).strip() or "MCP4H cue"
    body=str(txt.get("long","")).strip() or "(no details)"

    vis=(p.get("visual", {}) if isinstance(p, dict) else {})
    led=(vis.get("led", {}) if isinstance(vis, dict) else {})
    color=str(led.get("color","#999999"))

    card={
        "@type":"MessageCard",
        "@context":"https://schema.org/extensions",
        "summary": title,
        "themeColor": color.lstrip("#"),
        "title": title[:200],
        "text": body[:7000],
        "sections":[{"facts":[{"name":"LED","value":color},{"name":"Source","value":"MCP4H"}]}],
    }

    code=post(args.url, card)
    print(f"POST Teams -> HTTP {code}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
