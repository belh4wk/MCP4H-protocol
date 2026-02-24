# identity profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `identity.credential.issued`
- `identity.credential.presented`
- `identity.verification.performed`
- `identity.claim.asserted`
- `identity.proof.attached`
- `identity.revocation.checked`
- `identity.risk.hypothesis`
- `identity.cue.allow`
- `identity.cue.deny`
- `identity.session.started`
- `identity.session.ended`
- `identity.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
