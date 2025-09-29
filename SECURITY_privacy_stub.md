# Security & Privacy (stub)

- MCP4H messages SHOULD NOT include PII by default. Use hashed or pseudonymous IDs if needed.
- Prefer TLS for MQTT/WebSocket transports.
- For UDP, limit to LAN or VPN where possible.
- Consider sequence numbers and replay windows when state transitions are security-relevant.
