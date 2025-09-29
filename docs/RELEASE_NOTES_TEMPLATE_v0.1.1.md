# MCP4H™ v0.1.1

**Type:** Additive (non-breaking) update to v0.1.x line.

## Highlights
- Envelope: optional `profile`, `msg_type`, `seq`, `ts_monotonic_us`, `content_type`
- Wire profiles: `udp-realtime`, `mqtt-dist`, `ws-dashboard`
- Content types: `application/vnd.mcp4h.v0.1+json|+cbor`
- Example: tyre slip LED cues (`examples_v0.1.1/tyre_slip/`)
- Tools: UDP emitter/reader demo
- Tests: JSON golden vectors, CBOR generator, CI workflow

## Upgrade Notes
- Emit `version: "0.1.1"` (bare semver); accept legacy `mcp4h/0.1` during v0.1.x
- No breaking schema changes; existing messages remain valid

## Thanks
Thanks to MCP4H™ contributors and early testers for feedback and reviews.
