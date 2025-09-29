# Spec Style Guide

Use RFC 2119 keywords: **MUST**, **SHOULD**, **MAY** for normative requirements.

## Naming
- Use `snake_case` for field names.
- Units must be explicit in docs (e.g., `*_us` for microseconds).
- Prefer consistent, short keys: `seq`, `ts_monotonic_us`, `msg_type`.

## Envelope fields (v0.1.1)
- `version` (string, semver)
- `profile` (`udp-realtime|mqtt-dist|ws-dashboard`)
- `msg_type` (`telemetry|cue|state|config|ack`)
- `source_id` (string)
- `seq` (uint32)
- `ts_monotonic_us` (int)
- `timestamp` (ISO-8601 UTC)
- `payload` (object)
