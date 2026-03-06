# Cue Router Bridge

The cue-router is a transport-oriented bridge that fans MCP4H packets out to:

- Slack webhooks
- Microsoft Teams webhooks
- MQTT topics

It also adds the operational pieces needed to run it like a real bridge:

- `/healthz` and `/readyz`
- `/metrics` for Prometheus scraping
- policy hot-reload from disk
- replay CLI support
- OpenTelemetry instrumentation hooks

## What it is for

Use it when one MCP4H packet should be delivered to several targets without baking transport-specific logic into the producer.

## What it is not for

It is **not** the arbiter. Keep deep ranking, interruption logic, and user-state judgment elsewhere. The cue-router should route based on explicit policy, not invent meaning.

## Run with Docker Compose

The service is defined in `services/cue-router/` and wired in `docker-compose.yml`.

Default local URL:

- `http://localhost:8090/healthz`
- `http://localhost:8090/metrics`

## Policy file

Canonical policy path:

- `bridges/cue-router/policy.yaml`

Policy changes are hot-reloaded automatically when the file timestamp changes.

## Replay CLI

```bash
python tools/replay_cues.py bridges/cue-router/examples/replay.ndjson --url http://localhost:8090/route
```

Or publish directly to MQTT:

```bash
python tools/replay_cues.py bridges/cue-router/examples/replay.ndjson --transport mqtt --topic mcp4h/cues
```
