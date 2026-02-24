# health profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `health.observation.recorded`
- `health.vital.observed`
- `health.symptom.reported`
- `health.score.derived`
- `health.risk.hypothesis`
- `health.cue.escalate`
- `health.cue.monitor`
- `health.medication.recorded`
- `health.lab.result`
- `health.device.telemetry`
- `health.provenance.import`
- `health.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
