# finance profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `finance.message.received`
- `finance.transaction.recorded`
- `finance.risk.signal`
- `finance.fraud.hypothesis`
- `finance.compliance.check`
- `finance.cue.hold`
- `finance.cue.release`
- `finance.settlement.updated`
- `finance.ledger.posted`
- `finance.audit.artifact`
- `finance.exception.detected`
- `finance.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
