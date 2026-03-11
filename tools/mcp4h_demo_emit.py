#!/usr/bin/env python3
"""
mcp4h_demo_emit.py

Small demo to prove the "projection" idea:
- Load an MCP4H envelope (v0.1.1).
- Validate it by calling the local MCP server (stdio JSON-RPC).
- For each cue, print what could be rendered across modalities
  based on the structured projected payload.

Usage:
  python tools/mcp4h_demo_emit.py --input examples/messages/mcp/mcp_event_projected_payload.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

REPO = Path(__file__).resolve().parents[1]
MCP_SERVER = REPO / "bridges" / "mcp" / "server" / "mcp_server.py"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def jsonrpc_call_validate(packet: Dict[str, Any]) -> Dict[str, Any]:
    req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "mcp4h.validate", "arguments": {"packet": packet}}}
    p = subprocess.run(
        [sys.executable, str(MCP_SERVER)],
        input=(json.dumps(req) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    # stderr may contain warnings; ignore unless stdout is empty
    out = p.stdout.decode("utf-8", errors="replace").strip()
    if not out:
        raise RuntimeError(f"No response from MCP server. stderr:\n{p.stderr.decode('utf-8', errors='replace')}")
    resp = json.loads(out)
    text = resp["result"]["content"][0]["text"]
    return json.loads(text)


def print_projection(cue: Dict[str, Any]) -> None:
    payload = cue.get("payload", {})
    print(f"\n--- cue {cue.get('id')} ({cue.get('channel')}/{cue.get('intent')}) ---")

    txt = payload.get("text")
    if isinstance(txt, dict):
        short = txt.get("short") or ""
        long = txt.get("long") or ""
        if short or long:
            print(f"[text] short='{short}'")
            if long and long != short:
                print(f"[text] long ='{long}'")

    vis = payload.get("visual")
    if isinstance(vis, dict):
        led = vis.get("led")
        if isinstance(led, dict):
            print(f"[visual:led] color={led.get('color')} blink_hz={led.get('blink_hz')} ttl_ms={led.get('ttl_ms')}")
        icon = vis.get("icon")
        if icon:
            print(f"[visual] icon={icon}")

    aud = payload.get("audio")
    if isinstance(aud, dict):
        mode = aud.get("mode")
        if mode:
            print(f"[audio] mode={mode}")
        if aud.get("beep"):
            print(f"[audio:beep] pattern={aud.get('beep')}")
        if aud.get("tts"):
            print(f"[audio:tts] '{aud.get('tts')}'")
        if aud.get("sample"):
            print(f"[audio:sample] {aud.get('sample')}")

    hap = payload.get("haptic")
    if isinstance(hap, dict):
        print(f"[haptic] pattern={hap.get('pattern')} intensity={hap.get('intensity')} duration_ms={hap.get('duration_ms')} channel={hap.get('channel')}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to an MCP4H envelope JSON")
    args = ap.parse_args()

    inp = (REPO / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    pkt = load_json(inp)

    v = jsonrpc_call_validate(pkt)
    if not v.get("ok"):
        print("VALIDATION FAILED:")
        for e in v.get("errors", []):
            print(" -", e)
        return 2

    print("VALIDATION OK ✅")
    cues = pkt.get("cues", [])
    if not isinstance(cues, list) or not cues:
        print("No cues to emit.")
        return 0

    for cue in cues:
        if isinstance(cue, dict):
            print_projection(cue)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
