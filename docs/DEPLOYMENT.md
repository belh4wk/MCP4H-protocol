# Deployment Guide

## Dev (Docker)
- `docker compose up --build`

## Simracing (local)
- Game UDP → `udp-proxy` (20777) → normalized JSON → `simhub-adapter` (9999) → MQTT cues.
- Tweak thresholds in `services/simhub-adapter/mapping.json`.

## Assistive demo
- Open `bridges/wearables-pwa/index.html` and connect to ws://localhost:8080/cues.
- Post `examples_cues/friend_withdrawing.json` to see vibration patterns.

## Production notes
- MQTT v5 content-type if supported (`application/mcp4h+json`).
- Separate networks for safety/assistive; log cues but strip PII.
