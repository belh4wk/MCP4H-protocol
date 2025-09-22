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
