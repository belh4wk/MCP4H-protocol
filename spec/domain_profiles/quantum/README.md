# quantum profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `quantum.job.submitted`
- `quantum.circuit.compiled`
- `quantum.mapping.selected`
- `quantum.run.executed`
- `quantum.result.observed`
- `quantum.telemetry.observed`
- `quantum.anomaly.detected`
- `quantum.hypothesis.raised`
- `quantum.cue.recommendation`
- `quantum.calibration.snapshot`
- `quantum.error_rate.estimated`
- `quantum.postrun.summary`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
