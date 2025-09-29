# Choosing a Transport for MCP4H™

## UDP (profile: udp-realtime)
Pros: very low latency, simple. Cons: loss/out-of-order. Use `seq` and tolerate gaps. Framing: NDJSON or length-prefix.

## MQTT v5 (profile: mqtt-dist)
Pros: pub/sub, TLS, QoS. Cons: broker dependency. Topics: `mcp4h/{version}/{profile}/{source_id}/{signal}`. QoS 0 hot; QoS 1 state/config.

## WebSocket (profile: ws-dashboard)
Pros: native to browsers; one MCP4H™ message per frame. Cons: server required.
