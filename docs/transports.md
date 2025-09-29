# Choosing a Transport for MCP4H

MCP4H is transport-agnostic. Pick the transport that matches your use-case:

## UDP (profile: udp-realtime)
- **Pros:** very low latency, simple, widely supported for telemetry
- **Cons:** packet loss/out-of-order; add `seq` and tolerate gaps
- **Framing:** NDJSON (one JSON per line) **or** length-prefix (`<len>\n<json bytes>`)
- **When:** wheel force feedback, LEDs, haptics, local rig integrations

## MQTT v5 (profile: mqtt-dist)
- **Pros:** pub/sub routing, fan-out to many consumers, TLS, QoS
- **Cons:** broker dependency
- **Topics:** `mcp4h/{version}/{profile}/{source_id}/{signal}`
- **QoS:** 0 for hot telemetry, 1 for state/config; use `retain=true` only for slow-changing state

## WebSocket (profile: ws-dashboard)
- **Pros:** native to browsers, easy to build UIs
- **Cons:** server required
- **Rule:** send a single MCP4H message per frame
