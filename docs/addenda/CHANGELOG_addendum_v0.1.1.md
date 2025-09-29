# MCP4H v0.1.1 Addendum (Patch)

Date: 2025-09-29

**Additive (non-breaking) changes:**

- Envelope schema `mcp4h-v0.1.1.json` with optional fields: `profile`, `msg_type`, `seq`, `ts_monotonic_us`, `content_type`.
- Wire profiles documented: `udp-realtime`, `mqtt-dist`, `ws-dashboard`.
- Content types registered: `application/vnd.mcp4h.v0.1+json` and `+cbor`.
- Transport guidance (UDP/MQTT/WebSocket) and framing (NDJSON / length-prefix).
- Tyre-slip cue normative example (examples_v0.1.1/tyre_slip).
- Test vectors (JSON) and CBOR round-trip helper (optional if `cbor2` installed).
- Small UDP tools for local testing.
