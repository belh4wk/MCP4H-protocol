# Tyre Slip Cue Example (udp-realtime)

- Transport: UDP (NDJSON), profile `udp-realtime`
- Message type: `cue`
- Fields used: `seq`, `ts_monotonic_us`, `content_type`

Hysteresis thresholds:
- warn: enter >= 0.07, exit < 0.05
- crit: enter >= 0.12, exit < 0.09
