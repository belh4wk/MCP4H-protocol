# Tyre Slip Cue Example (udp-realtime)

This folder contains a **normative example** of MCP4H messages for tyre slip cues.
- Transport: UDP (NDJSON), profile `udp-realtime`
- Message types: `cue` (stateful), occasionally `telemetry` for reference
- Monotonic timestamps: `ts_monotonic_us`
- Sequence: `seq`

## States
- `ok` → no slip
- `warn` → approaching slip threshold
- `crit` → slip detected (blink LED)

**Hysteresis:** enter/exit have different thresholds to avoid flicker.
- Enter warn: slip_ratio >= 0.07
- Exit warn: slip_ratio < 0.05
- Enter crit: slip_ratio >= 0.12
- Exit crit: slip_ratio < 0.09

Units:
- `slip_ratio` is fraction (0.0–1.0)
