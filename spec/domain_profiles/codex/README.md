# codex profile (dev)

Event naming: `<profile>.<noun>.<verb>`.

## Canonical event types (starter set)
- `codex.document.registered`
- `codex.page.image.observed`
- `codex.region.detected`
- `codex.line.segmented`
- `codex.glyph.segmented`
- `codex.token.extracted`
- `codex.pattern.clustered`
- `codex.translation.hypothesis`
- `codex.reading.alternate`
- `codex.annotation.added`
- `codex.cue.review_requested`
- `codex.export.generated`

## Namespace
All domain-specific fields live under `extensions.{name}.*` (or `extensions.{name}._x.*` for experimental).
