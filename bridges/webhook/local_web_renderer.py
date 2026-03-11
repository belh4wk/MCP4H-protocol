#!/usr/bin/env python3
"""
bridges/webhook/local_web_renderer.py

A dead-simple local web renderer for MCP4H projected payloads.
- Serves a small HTML page at http://127.0.0.1:8090/
- Accepts POST of JSON (projected cue payload) at /ingest
- Shows:
  - text.short / text.long
  - LED dot (color + blink_hz)
  - audio mode/beep/tts/sample
  - haptic pattern/intensity/duration

No dependencies. Intended as a "make it visible in 30 seconds" demo renderer.

Run:
  python bridges/webhook/local_web_renderer.py

Then publish to it (example):
  python bridges/webhook/send_projected.py --url "http://127.0.0.1:8090/ingest" --input examples/messages/mcp/mcp_event_projected_payload.json --cue-only

Or via MCP tool:
  ... mcp4h.webhook.publish url=http://127.0.0.1:8090/ingest cue_only=true ...
"""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional

HOST = "127.0.0.1"
PORT = 8090

_state_lock = threading.Lock()
_last_payload: Dict[str, Any] = {}
_last_seen_ts: float = 0.0


HTML = r"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>MCP4H Local Renderer</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }
    .row { display:flex; gap: 18px; align-items: center; }
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; max-width: 900px; }
    .muted { color:#666; }
    .led { width:18px; height:18px; border-radius:50%; border:1px solid #222; display:inline-block; margin-right:10px; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; white-space: pre-wrap; }
    .badge { font-size:12px; padding: 2px 8px; border-radius: 999px; background:#eee; display:inline-block; }
  </style>
</head>
<body>
  <h2>MCP4H Local Renderer <span class="badge">projected payload</span></h2>
  <p class="muted">POST JSON to <code>/ingest</code>. Page polls <code>/state</code> every 500ms.</p>

  <div class="card">
    <div class="row">
      <span id="led" class="led"></span>
      <div>
        <div><b id="short">Waiting…</b></div>
        <div class="muted" id="long"></div>
      </div>
    </div>

    <hr/>

    <div class="row">
      <div style="min-width:140px;"><b>Audio</b></div>
      <div id="audio" class="muted">—</div>
    </div>
    <div class="row">
      <div style="min-width:140px;"><b>Haptic</b></div>
      <div id="haptic" class="muted">—</div>
    </div>

    <hr/>

    <details>
      <summary>Raw payload</summary>
      <pre class="mono" id="raw">{}</pre>
    </details>
  </div>

<script>
let blinkTimer = null;
let ledOn = true;

function setLed(color, blinkHz) {
  const led = document.getElementById('led');
  if (blinkTimer) { clearInterval(blinkTimer); blinkTimer = null; }
  led.style.background = color || '#999';

  if (blinkHz && blinkHz > 0) {
    const ms = Math.max(100, Math.round(1000 / (blinkHz * 2)));
    blinkTimer = setInterval(() => {
      ledOn = !ledOn;
      led.style.opacity = ledOn ? '1.0' : '0.2';
    }, ms);
  } else {
    led.style.opacity = '1.0';
  }
}

async function poll() {
  try {
    const r = await fetch('/state');
    const data = await r.json();

    const txt = (data.text || {});
    document.getElementById('short').textContent = txt.short || '—';
    document.getElementById('long').textContent  = txt.long  || '';

    const vis = (data.visual || {});
    const led = (vis.led || {});
    setLed(led.color || '#999', led.blink_hz || 0);

    const aud = (data.audio || {});
    const audParts = [];
    if (aud.mode) audParts.push('mode=' + aud.mode);
    if (aud.beep) audParts.push('beep=' + aud.beep);
    if (aud.tts)  audParts.push('tts="' + aud.tts + '"');
    if (aud.sample) audParts.push('sample=' + aud.sample);
    document.getElementById('audio').textContent = audParts.length ? audParts.join(' | ') : '—';

    const hap = (data.haptic || {});
    const hapParts = [];
    if (hap.pattern) hapParts.push('pattern=' + hap.pattern);
    if (hap.intensity !== undefined) hapParts.push('intensity=' + hap.intensity);
    if (hap.duration_ms !== undefined) hapParts.push('duration_ms=' + hap.duration_ms);
    document.getElementById('haptic').textContent = hapParts.length ? hapParts.join(' | ') : '—';

    document.getElementById('raw').textContent = JSON.stringify(data, null, 2);

  } catch (e) {
    // ignore
  }
}

setInterval(poll, 500);
poll();
</script>
</body>
</html>
"""

def _set_payload(p: Dict[str, Any]) -> None:
    global _last_payload, _last_seen_ts
    with _state_lock:
        _last_payload = p
        _last_seen_ts = time.time()

def _get_payload() -> Dict[str, Any]:
    with _state_lock:
        return dict(_last_payload)

class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if self.path == "/state":
            payload = _get_payload()
            self._send(200, json.dumps(payload).encode("utf-8"), "application/json; charset=utf-8")
            return
        self._send(404, b"Not found", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/ingest":
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        n = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(n)
        try:
            payload = json.loads(raw.decode("utf-8-sig"))
            if not isinstance(payload, dict):
                payload = {"raw": payload}
            _set_payload(payload)
            self._send(204, b"", "text/plain")
        except Exception as e:
            self._send(400, (f"bad json: {e}").encode("utf-8"), "text/plain; charset=utf-8")

def main() -> None:
    print(f"Listening on http://{HOST}:{PORT}/  (POST projected payload to /ingest)")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
