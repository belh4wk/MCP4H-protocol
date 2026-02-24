# supplychain profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `supplychain.event.observed`
- `supplychain.asset.registered`
- `supplychain.location.observed`
- `supplychain.transfer.recorded`
- `supplychain.temperature.observed`
- `supplychain.condition.derived`
- `supplychain.compliance.claim`
- `supplychain.cue.hold`
- `supplychain.cue.release`
- `supplychain.audit.artifact`
- `supplychain.exception.detected`
- `supplychain.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
