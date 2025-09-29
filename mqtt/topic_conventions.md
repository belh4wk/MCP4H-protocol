# MQTT Topic Conventions for MCP4H

**Topic shape:**

```
mcp4h/{version}/{profile}/{source_id}/{signal}
```

- `version` → e.g., `0.1` or `0.1.1`
- `profile` → usually `mqtt-dist`
- `source_id` → stable emitter ID (rig/device/process)
- `signal` → dotted path like `tyre_fl.slip_ratio` or `traction.cue`

**QoS guidance**
- QoS 0 → hot telemetry (low-latency, occasional loss OK)
- QoS 1 → state/config (must arrive)
- Retain only for slow-changing state (e.g., `config.*`)
