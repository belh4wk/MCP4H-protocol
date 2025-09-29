# MCP4H™ Wire Profiles (v0.1.1 addendum)

| Profile        | Typical transport | Framing                 | Rate guidance       | Reliability/QoS                       | Intended use                           |
|----------------|-------------------|-------------------------|---------------------|---------------------------------------|-----------------------------------------|
| udp-realtime   | UDP (LAN)         | NDJSON or length-prefix | 50–250 Hz (bursty) | seq + tolerant to gaps                | Haptics, LEDs, wheels, realtime cues    |
| mqtt-dist      | MQTT v5 over TLS  | MQTT payload = message  | 5–50 Hz             | QoS 0 hot, QoS 1 state/config         | Cross-device routing / remote relays    |
| ws-dashboard   | WebSocket (TLS)   | One message per frame   | 5–60 Hz (UI-driven) | Browser/WebSocket reliability         | Browser dashboards / visualizations     |

Additive envelope fields: `profile`, `msg_type`, `seq`, `ts_monotonic_us`, `timestamp`, `content_type`.
