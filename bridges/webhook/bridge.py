#!/usr/bin/env python3
"""
bridges/webhook/bridge.py

Reference webhook bridge for MCP4H.
- Reads MCP4H packets from stdin (JSONL) or from a file.
- Optionally validates using the local MCP server (stdio JSON-RPC).
- Posts either the full packet or cue payloads to an HTTP webhook.
- Includes basic rate limiting + retry with exponential backoff.

Examples:

# stdin JSONL -> webhook (send full packet)
type packets.jsonl | python bridges/webhook/bridge.py --url http://127.0.0.1:8080/

# send only first cue payload
type packets.jsonl | python bridges/webhook/bridge.py --url http://127.0.0.1:8080/ --cue-only

# validate before posting
type packets.jsonl | python bridges/webhook/bridge.py --url http://127.0.0.1:8080/ --validate

# read from file (JSONL)
python bridges/webhook/bridge.py --url http://127.0.0.1:8080/ --from packets.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional
import subprocess

REPO = Path(__file__).resolve().parents[2]
MCP_SERVER = REPO / "bridges" / "mcp" / "server" / "mcp_server.py"


def _loads_any(s: str) -> Any:
    return json.loads(s)


def iter_jsonl_text(lines: Iterable[str]) -> Iterator[Dict[str, Any]]:
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        obj = _loads_any(ln)
        if isinstance(obj, dict):
            yield obj


def read_jsonl_file(path: Path) -> Iterator[Dict[str, Any]]:
    # tolerate BOM
    txt = path.read_bytes().decode("utf-8-sig").splitlines()
    yield from iter_jsonl_text(txt)


def read_one_json_file(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def jsonrpc_validate(packet: Dict[str, Any]) -> Dict[str, Any]:
    req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "mcp4h.validate", "arguments": {"packet": packet}}}
    p = subprocess.run(
        [sys.executable, str(MCP_SERVER)],
        input=(json.dumps(req) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    out = p.stdout.decode("utf-8", errors="replace").strip()
    if not out:
        raise RuntimeError(f"No response from MCP server. stderr:\n{p.stderr.decode('utf-8', errors='replace')}")
    resp = json.loads(out)
    text = resp["result"]["content"][0]["text"]
    return json.loads(text)


def post_json(url: str, obj: Any, timeout: float = 10.0) -> int:
    data = json.dumps(obj).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.getcode()


@dataclass
class Retry:
    attempts: int = 5
    base_delay_s: float = 0.5
    max_delay_s: float = 8.0

    def sleep(self, i: int) -> None:
        delay = min(self.max_delay_s, self.base_delay_s * (2 ** i))
        time.sleep(delay)


def extract_payload(packet: Dict[str, Any], cue_only: bool) -> Any:
    if not cue_only:
        return packet
    cues = packet.get("cues") or []
    if isinstance(cues, list) and cues and isinstance(cues[0], dict):
        return cues[0].get("payload", {})
    return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Webhook URL to POST JSON to")
    ap.add_argument("--from", dest="from_path", help="Read packets from this file (JSONL or JSON)")
    ap.add_argument("--stdin", action="store_true", help="Read packets from stdin (JSONL). Default if --from not set.")
    ap.add_argument("--cue-only", action="store_true", help="Send only first cue payload (projected payload) instead of full packet")
    ap.add_argument("--validate", action="store_true", help="Validate packets before posting (calls local MCP server)")
    ap.add_argument("--rate", type=float, default=0.0, help="Max posts per second (0 = no limit). Example: 2 means 2/sec.")
    ap.add_argument("--once", action="store_true", help="Stop after first packet")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--cooldown-ms", type=int, default=0, help="Per-key cooldown window; drop packets arriving within this window. 0 disables.")
    ap.add_argument("--dedupe-window-ms", type=int, default=0, help="Drop identical payloads within this window (per-key). 0 disables.")
    ap.add_argument("--dedupe-key", default="mcp.trace_id", help="Key path to identify streams. Examples: mcp.trace_id, mcp.tool, text.short. Default mcp.trace_id")
    ap.add_argument("--policy-debug", action="store_true", help="Print when packets are dropped/merged by policy.")
    args = ap.parse_args()

    rate_interval = (1.0 / args.rate) if args.rate and args.rate > 0 else 0.0
    last_post = 0.0
    
    # Policy state (lives for the duration of this process)
    last_sent_ts = {}   # key -> epoch seconds
    last_hash_ts = {}   # key -> (hash, epoch seconds)

    def get_path(d: dict, path: str):
        cur = d
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return None
            cur = cur[part]
        return cur

    def policy_key(pkt: dict) -> str:
        path = args.dedupe_key.strip()
        if path.startswith("mcp."):
            md = pkt.get("metadata", {}) if isinstance(pkt, dict) else {}
            mcp = md.get("mcp", {}) if isinstance(md, dict) else {}
            return str(get_path({"mcp": mcp}, path) or "global")
        if path.startswith("text."):
            txt = pkt.get("text", "") if isinstance(pkt, dict) else ""
            # packet.text is string in v0.1.1; for projected payload it's payload.text.{short,long}
            return str(get_path({"text": txt if isinstance(txt, dict) else {"short": txt}}, path) or "global")
        # fallback: try packet root
        return str(get_path(pkt, path) or "global")

    def stable_hash(obj) -> str:
        try:
            return json.dumps(obj, sort_keys=True, separators=(",", ":"))
        except Exception:
            return str(obj)
retry = Retry()

    def maybe_rate_limit() -> None:
        nonlocal last_post
        if rate_interval <= 0:
            return
        now = time.time()
        wait = (last_post + rate_interval) - now
        if wait > 0:
            time.sleep(wait)
        last_post = time.time()

    # source iterator
    packets: Iterator[Dict[str, Any]]
    if args.from_path:
        p = (REPO / args.from_path).resolve() if not Path(args.from_path).is_absolute() else Path(args.from_path)
        if p.suffix.lower() == ".json":
            packets = iter([read_one_json_file(p)])
        else:
            packets = read_jsonl_file(p)
    else:
        # default to stdin JSONL
        packets = iter_jsonl_text(sys.stdin)

    sent = 0
    for pkt in packets:
        if args.validate:
            res = jsonrpc_validate(pkt)
            if not res.get("ok"):
                print("SKIP (validation failed):", res.get("errors", []), file=sys.stderr)
                continue

        body = extract_payload(pkt, args.cue_only)

        # Policy: cooldown + dedupe (per key)
        k = policy_key(pkt)
        now = time.time()
        if args.cooldown_ms and args.cooldown_ms > 0:
            last = last_sent_ts.get(k, 0.0)
            if (now - last) * 1000.0 < args.cooldown_ms:
                if args.policy_debug:
                    print(f"DROP cooldown key={k}", file=sys.stderr)
                continue
        if args.dedupe_window_ms and args.dedupe_window_ms > 0:
            h = stable_hash(body)
            prev = last_hash_ts.get(k)
            if prev:
                prev_h, prev_t = prev
                if h == prev_h and (now - prev_t) * 1000.0 < args.dedupe_window_ms:
                    if args.policy_debug:
                        print(f"DROP dedupe key={k}", file=sys.stderr)
                    continue
            last_hash_ts[k] = (h, now)

        maybe_rate_limit()

        ok = False
        for i in range(retry.attempts):
            try:
                code = post_json(args.url, body, timeout=args.timeout)
                print(f"POST {args.url} -> HTTP {code}")
                last_sent_ts[k] = time.time()
                ok = True
                break
            except Exception as e:
                print(f"POST failed (attempt {i+1}/{retry.attempts}): {e}", file=sys.stderr)
                retry.sleep(i)

        if not ok:
            return 2

        sent += 1
        if args.once and sent >= 1:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
