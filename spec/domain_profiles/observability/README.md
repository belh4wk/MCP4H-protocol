# observability profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `observability.log.observed`
- `observability.metric.observed`
- `observability.trace.observed`
- `observability.span.derived`
- `observability.error.hypothesis`
- `observability.anomaly.detected`
- `observability.slo.breach`
- `observability.cue.page`
- `observability.cue.rollback`
- `observability.deployment.observed`
- `observability.rootcause.claim`
- `observability.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
