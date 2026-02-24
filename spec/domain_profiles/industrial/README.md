# industrial profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `industrial.sensor.observed`
- `industrial.state.derived`
- `industrial.fault.hypothesis`
- `industrial.maintenance.cue`
- `industrial.command.issued`
- `industrial.alarm.raised`
- `industrial.asset.registered`
- `industrial.process.step`
- `industrial.energy.observed`
- `industrial.vibration.observed`
- `industrial.quality.check`
- `industrial.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
