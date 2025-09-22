# DEVELOPERS.md — MCP4H repo notes

## Schemas & Examples
- Baseline schema (v0.1): `spec/schema/mcp4h-v0.1.json`
- Examples in `examples/` MUST be **v0.1-only** (no `extensions`). CI validates these.
- Optional extensions (v0.1.1): `schemas/mcp4h-0.1.1.schema.json`
- Examples that use `extensions` live in `examples_v0.1.1/` (validated against v0.1.1).

### Local validation
```bash
pip install jsonschema
python tests/validate_messages.py
```
CI workflow: `.github/workflows/validate.yml`

## Versioning
- v0.1: stable minimal envelope + sidecar.
- v0.1.1: adds optional `extensions` container. Keep extensions backwards-compatible.

## Contributing
- Open an issue for new fields or extensions. Provide use-cases and example envelopes.
- No PII; `actor.handle` should be opaque/hashed.

## Bridges
- `bridges/simhub/` — per-wheel **Traction LEDs** mapping (colors + blink) for Dash Studio.
- `bridges/simhub-plugin/` — C# plugin skeleton reading `SimHubVars.json` and publishing properties.
- `bridges/notify-led/` — Notif-LED mapping for wearables (heat/valence → color/pattern).

## Harmonizer Integration

Harmonizer is an optional, app-agnostic translator that can emit **MCP4H** packets on request during conversations.
This enables natural-language inputs to produce interoperable JSON artifacts consumable by any adapter (apps/devices/humans).

**Packet types Harmonizer may emit:** `ux_signal`, `semantic_event`, `telemetry_annotation`, `action_intent`, `delivery_receipt`, `capability_advertisement`.

**Repo rules for all Harmonizer-emitted packets:**
- `$schema: spec/schema/mcp4h-v0.1.json`
- `schema_version: v0.1.1`
- ISO-8601 UTC timestamps (ending in `Z`)
- Include `assumptions` (array), `confidence` (0..1), and `tags` (array)
- No comments, no trailing commas

See [MCP4H_Harmonizer_Handbook_v1.5.md](./MCP4H_Harmonizer_Handbook_v1.5.md) for canonical templates and triggers.
