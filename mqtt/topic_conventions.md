# MQTT Topic Conventions

Topic shape:
`mcp4h/{version}/{profile}/{source_id}/{signal}`

Examples:
- `mcp4h/0.1/mqtt-dist/rig01/tyre_fl.slip_ratio`
- `mcp4h/0.1/mqtt-dist/rig01/traction.cue`

QoS guidance: 0 for hot telemetry; 1 for state/config. Retain only slow-changing state.
