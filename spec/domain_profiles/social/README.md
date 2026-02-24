# social profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `social.post.created`
- `social.reply.created`
- `social.reaction.added`
- `social.report.filed`
- `social.moderation.action`
- `social.claim.contested`
- `social.context.added`
- `social.cue.request_sources`
- `social.cue.downrank`
- `social.activity.import`
- `social.network.signal`
- `social.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
