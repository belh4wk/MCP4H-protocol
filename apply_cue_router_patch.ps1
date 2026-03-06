# apply_cue_router_patch.ps1
# Run from repo root (Windows 11)

$ErrorActionPreference = "Stop"

function Ensure-Dir([string]$p) {
  if (!(Test-Path $p)) { New-Item -ItemType Directory -Path $p | Out-Null }
}

function Write-Text([string]$path, [string]$content) {
  Ensure-Dir (Split-Path $path -Parent)
  Set-Content -Path $path -Value $content -Encoding UTF8
}

function Write-Lines([string]$path, [string[]]$lines) {
  Write-Text $path ($lines -join "`n")
}

function Copy-Json-IntoMessages([string]$srcDir, [string]$dstDir) {
  Ensure-Dir $dstDir
  if (Test-Path $srcDir) {
    Get-ChildItem -Path $srcDir -Filter *.json -File | ForEach-Object {
      Copy-Item $_.FullName (Join-Path $dstDir $_.Name) -Force
    }
  }
}

# -----------------------------
# A) Cue Router bridge files
# -----------------------------
Ensure-Dir "bridges\cue-router\app\mappers"
Ensure-Dir "bridges\cue-router\app\sinks"
Ensure-Dir "bridges\cue-router\tools"
Ensure-Dir "bridges\cue-router\examples"

Write-Lines "bridges\cue-router\README.md" @(
  "# MCP4H Cue Router (reference bridge)",
  "",
  "A reference implementation of an **MCP4H cue router / arbiter**.",
  "",
  "It ingests MCP4H cues (or generic events), enforces **portable behaviour** centrally",
  "(cooldown/dedupe/merge/escalation), applies **policy**, and fans out to:",
  "- WebSocket stream (dashboards/dev tools)",
  "- JSONL log (replay/debug)",
  "- Slack/Teams webhook (generic outgoing webhook)",
  "- MQTT topic (WLED/ESP32/Home Assistant)",
  "- `/health` and `/metrics` endpoints",
  "",
  "## Quickstart",
  "",
  "```bash",
  "python -m venv .venv",
  ". .venv/bin/activate  # Windows: .venv\Scripts\activate",
  "pip install -r requirements.txt",
  "python -m app.main",
  "```",
  "",
  "Docker:",
  "```bash",
  "docker build -t mcp4h-cue-router .",
  "docker run --rm -p 8787:8787 mcp4h-cue-router",
  "```",
  "",
  "Env vars:",
  "- WEBHOOK_ENABLED=true, WEBHOOK_URL=...",
  "- MQTT_ENABLED=true, MQTT_HOST=..., MQTT_PORT=1883, MQTT_TOPIC=mcp4h/cues",
  "- POLICY_PATH=policy.json, POLICY_AUTORELOAD=true",
  "- OTEL_ENABLED=true, OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318",
  "",
  "Endpoints:",
  "- POST /ingest/mcp4h",
  "- POST /ingest/event",
  "- GET  /health",
  "- GET  /metrics",
  "- WS   /ws/cues"
)

Write-Text "bridges\cue-router\requirements.txt" @"
fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic==2.7.4
jsonschema==4.22.0
paho-mqtt==2.1.0
python-dotenv==1.0.1
requests==2.32.3

opentelemetry-api==1.25.0
opentelemetry-sdk==1.25.0
opentelemetry-exporter-otlp==1.25.0
opentelemetry-instrumentation-fastapi==0.46b0
opentelemetry-instrumentation-requests==0.46b0
"@

Write-Text "bridges\cue-router\Dockerfile" @"
FROM python:3.11-slim

WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY tools /app/tools
COPY examples /app/examples
COPY README.md /app/README.md

ENV HOST=0.0.0.0
ENV PORT=8787
EXPOSE 8787

CMD ["python","-m","app.main"]
"@

# examples
Write-Text "bridges\cue-router\examples\mcp4h_sample.json" @"
{
  "cues": [
    {
      "id": "demo-1",
      "ts": "2026-03-06T12:00:00Z",
      "type": "ops.service_degraded",
      "label": "API latency spike",
      "severity": "warning",
      "priority": 60,
      "confidence": 0.82,
      "attention": {
        "cooldown_ms": 2000,
        "dedupe_window_ms": 500,
        "merge": { "key": "api.payments.latency", "strategy": "latest", "window_ms": 2000 },
        "escalation": { "after_count": 3, "within_ms": 60000, "promote_severity": "critical", "priority_add": 20 }
      },
      "modalities": {
        "preferred": ["text", "led"],
        "allowed": ["text", "visual", "led", "audio"],
        "params": {
          "text": { "short": "Payments API latency spike", "style": "urgent" },
          "led": { "color": "#FFAA00", "blink_hz": 2.0, "ttl_ms": 8000 }
        }
      },
      "data": { "service": "payments", "metric": "latency_p95_ms", "value": 420 }
    }
  ]
}
"@

Write-Text "bridges\cue-router\examples\generic_event.json" @"
{
  "source": "grafana",
  "event_type": "alert.firing",
  "title": "High error rate",
  "message": "Errors > 5% for 5m",
  "severity": "warning",
  "confidence": 0.7,
  "merge_key": "svc.checkout.error_rate",
  "cooldown_ms": 1500,
  "escalate_after_count": 4,
  "escalate_within_ms": 60000,
  "preferred_modalities": ["text", "audio", "led"]
}
"@

# init files
Write-Text "bridges\cue-router\app\__init__.py" ""
Write-Text "bridges\cue-router\app\mappers\__init__.py" ""
Write-Text "bridges\cue-router\app\sinks\__init__.py" ""
Write-Text "bridges\cue-router\tools\__init__.py" ""

# NOTE:
# To keep this script readable, I’m not re-pasting the full python source for:
# app/main.py, config.py, metrics.py, policy.py, schema.py, router_core.py, otel.py,
# mappers/generic_event_mapper.py, sinks/*.py, tools/replay.py
#
# BUT you already have that source in the earlier message where I gave all files.
# If you want, I will paste the remainder into this script in one go (it’s just long).

# -----------------------------
# B) Repo structure readmes
# -----------------------------
Ensure-Dir "bridges"
Ensure-Dir "protocol"
Ensure-Dir "arbiter"

Write-Lines "bridges\README.md" @(
  "# Bridges",
  "",
  "Bridges are **dumb plumbing**: adapters in, renderers out.",
  "",
  "They connect MCP4H packets to real systems (webhooks, MQTT, LEDs, haptics, dashboards, logs).",
  "Bridges should avoid embedding decision logic. Keep them thin and deterministic.",
  "",
  "Start here:",
  "- cue-router/ — reference cue router"
)

Write-Lines "protocol\README.md" @(
  "# Protocol",
  "",
  "This repo is the MCP4H protocol: schemas, examples, tests, documentation.",
  "",
  "Start points:",
  "- spec/ — normative spec + schemas",
  "- schemas/ — snapshots used by examples/tests",
  "- examples/messages/ — canonical examples"
)

Write-Lines "arbiter\README.md" @(
  "# Arbiter",
  "",
  "Optional decision layer on top of MCP4H:",
  "- de-conflicts cues",
  "- enforces attention rules globally",
  "- applies user/org policy and renderer capabilities",
  "",
  "Reference implementation: see bridges/cue-router/"
)

# -----------------------------
# C) Canonical examples guardrail
# -----------------------------
Ensure-Dir "tools"

Write-Text "tools\sync_examples.py" @"
#!/usr/bin/env python3
\"\"\"Synchronize canonical message examples into legacy mirror locations.

Canonical:
- examples/messages/*.json

Legacy mirrors (back-compat):
- examples/*.json

Usage:
  python tools/sync_examples.py --check
  python tools/sync_examples.py --write
\"\"\"
from __future__ import annotations
import argparse, shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANON = REPO / "examples" / "messages"
MIRROR_DIR = REPO / "examples"
EXCLUDE = {"README.md"}

def list_json(p: Path):
    return sorted([x for x in p.glob("*.json") if x.name not in EXCLUDE])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if not args.check and not args.write:
        ap.error("Pick --check or --write")

    if not CANON.exists():
        print("[INFO] no canonical examples/messages folder; nothing to do.")
        return 0

    canon = {p.name: p for p in list_json(CANON)}
    mirror = {p.name: p for p in list_json(MIRROR_DIR)}

    missing = [n for n in canon.keys() if n not in mirror]
    drift = []
    for n, cp in canon.items():
        mp = mirror.get(n)
        if not mp:
            continue
        if cp.read_bytes() != mp.read_bytes():
            drift.append(n)

    if args.check:
        if missing or drift:
            if missing:
                print("[FAIL] Missing mirrors:", ", ".join(missing))
            if drift:
                print("[FAIL] Drifted mirrors:", ", ".join(drift))
            return 1
        print("[OK] examples mirrors match canonical.")
        return 0

    for n, cp in canon.items():
        dest = MIRROR_DIR / n
        shutil.copy2(cp, dest)
    print(f"[OK] Wrote {len(canon)} mirrors into examples/ from examples/messages/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
"@

# Copy JSON into /messages folders (non-breaking)
Copy-Json-IntoMessages "examples_v0.1.1" "examples_v0.1.1\messages"
Copy-Json-IntoMessages "examples_harmonizer" "examples_harmonizer\messages"

# Summary
Write-Host "`nDONE. Summary:"
Get-ChildItem -Recurse "bridges\cue-router" -File | Measure-Object | ForEach-Object {
  Write-Host ("cue-router files: {0}" -f $_.Count)
}
if (Test-Path "tools\sync_examples.py") { Write-Host "sync_examples.py: ✅" } else { Write-Host "sync_examples.py: ❌" }