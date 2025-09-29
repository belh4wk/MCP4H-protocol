# MCP4H Wire Profiles (v0.1.1 addendum)

This addendum defines three **wire profiles** to guide implementations while keeping MCP4H transport-agnostic.

| Profile        | Typical transport | Framing                 | Rate guidance        | Reliability                           | Intended use                            |
|----------------|-------------------|-------------------------|----------------------|----------------------------------------|------------------------------------------|
| udp-realtime   | UDP (LAN)         | NDJSON or length-prefix | 50–250 Hz (bursty)  | seq + optional resend/FEC by app       | Haptics, LEDs, wheels, near-real-time    |
| mqtt-dist      | MQTT v5 over TLS  | MQTT payload = message  | 5–50 Hz (rate-limit)| QoS 0 for hot, QoS 1 for state/config  | Cross-device routing / remote relays     |
| ws-dashboard   | WebSocket (TLS)   | 1 MCP4H msg per frame   | 5–60 Hz (UI-driven) | Browser-level reliability              | Browser dashboards / visualizations      |

**Envelope additions (optional, recommended):**

- `profile` – one of: `udp-realtime`, `mqtt-dist`, `ws-dashboard`  
- `msg_type` – one of: `telemetry`, `cue`, `state`, `config`, `ack`  
- `seq` (uint32), `ts_monotonic_us` (int), `timestamp` (ISO 8601)  
- `content_type` – `application/vnd.mcp4h.v0.1+json` or `+cbor`

**Versioning:** All changes here are **additive** to v0.1.x. Breaking changes move MCP4H to v0.2.
