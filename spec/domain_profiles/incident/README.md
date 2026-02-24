# incident profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `incident.alert.received`
- `incident.signal.enriched`
- `incident.hypothesis.raised`
- `incident.impact.estimated`
- `incident.mitigation.applied`
- `incident.status.updated`
- `incident.customer.communication`
- `incident.metric.observed`
- `incident.postmortem.finding`
- `incident.followup.task`
- `incident.resolution.declared`
- `incident.timeline.annotated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
