# Harmonizer (Optional) — App‑Agnostic MCP4H Companion

**Last updated:** 2025-09-22T09:42:03Z

Harmonizer is a **human‑first helper** that can also emit **MCP4H packets** on request, letting conversations drive interoperable software/hardware outcomes. It is optional; MCP4H works fine without it.

## Why it exists
- Bridge human language ↔ machine‑readable MCP4H JSON
- Keep tone/civility while preserving the sender’s voice
- Speed up prototyping of rules and adapters

## Packet types it can emit
- `ux_signal`, `semantic_event`, `telemetry_annotation`, `action_intent`, `delivery_receipt`, `capability_advertisement`

## Formatting contract
- `$schema: spec/schema/mcp4h-v0.1.json`, `schema_version: v0.1.1`
- UTC timestamps (`YYYY-MM-DDThh:mm:ssZ`), strict JSON (no comments/trailing commas)
- Include `assumptions`, `confidence`, `tags`
- Mark `inferred_from_text: true` when not sourced from live telemetry

## Examples
See [`examples_harmonizer/`](../examples_harmonizer) for ready‑to‑validate JSON packets.

## Learn more
- [MCP4H_Harmonizer_Handbook_v1.6.md](../MCP4H_Harmonizer_Handbook_v1.6.md)
- [DEVELOPERS.md](../DEVELOPERS.md)
- [docs/FAQ.md](./FAQ.md)
