# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses semantic versioning for tagged protocol releases.

## [Unreleased]

### v0.2 semantic model design - 2026-09-11

#### Added
- `spec/README.md` to document the current v0.1.x compatibility layout and planned versioned migration.
- `spec/v0.2/` design documents and cross-domain examples.
- `.gitignore` for local environments, caches, build output and editor/OS noise.

#### Decided
- v0.2 uses one shared envelope grammar with multiple independently addressable record kinds rather than one monolithic Semantic Envelope.
- Observation confidence/quality and Interpretation confidence are separate; measurements may also carry uncertainty.
- Severity/criticality is domain-profile specific; Policy owns attention priority, interruption and escalation.
- Carrier identifiers are open-ended, with recommended common identifiers rather than a closed universal enum.
- Projection remains separate from semantics by default and links through record relations/capability references.
- Low-latency implementations may bundle records without collapsing their logical roles.

#### Preserved
- Existing v0.1.x specification paths remain in place so current `$ref` links, tests and validators keep working.
- Historical published titles and citation records remain unchanged.

#### Fixed
- v0.1.1 example envelope version strings now match the v0.1.1 schema expected by the blocking validator.
- Legacy Harmonizer pytest discovery now resolves its local mapper reliably from repo-root test runs.
- Harmonizer timestamps now use timezone-aware UTC generation while preserving the existing `Z` output format.

### Foundations alignment - 2026-09-11

#### Added
- `FOUNDATIONS.md` as the current architectural/philosophical anchor.
- Explicit receiver-aware design principles.
- Explicit provenance, temporal/spectral structure and domain-profile direction.
- Clear v0.1.x compatibility vs v0.2 design distinction.

#### Changed
- README reframed around **Preserve meaning. Adapt the carrier.**
- Text is no longer described as the mandatory universal semantic intermediate.
- Arbiter/AI is described as an optional policy/judgment-assist layer.
- Roadmap updated around v0.2 semantic core, receiver capability, cross-domain references and external interoperability.
- Project status updated to reflect v0.1.5 plus subsequent MCP/webhook bridge work.
- Bridge guidance updated to preserve source truth and avoid destructive universal normalization.

#### Preserved
- v0.1.x schemas and compatibility behavior are not changed by this documentation pass.
- Historical published titles and citations remain verbatim for archival/citation integrity.

#### Next
- Finalize the v0.2 shared envelope grammar and record contracts.
- Consolidate overlapping schema/profile directory structure only after the canonical model is agreed.
- Build land-chassis and airframe references.
- Add one focused non-simulation reference.

## Documentation update - MCP4SH v1.1 implementation note

- Updated README language to describe MCP4SH v1.1 as a practical proving ground for MCP4H-style haptic translation.
- Added Setup Assistant context as an example of MCP4H thinking applied to user onboarding and hardware mapping.

## [v0.1.5] - 2026-02-26

### Added
- Portable behavior contract for cues.
- Behavior Policy schema.
- Renderer Capabilities schema.

### Changed
- Cue schema supports the v0.1 compatibility shapes plus portable Cue v1 behavior.

### Fixed
- CI cue validation validates examples against the canonical cue schema rather than hardcoded required keys.

## [v0.1.2-protocol] - 2025-11-26

Protocol and documentation alignment release.

See the GitHub release and `CITATIONS.md` for archival/version citation information.

## [v0.1.1] - 2025-10-05

### Added
- Dockerized microservice stack.
- Unified Docker Compose orchestration.
- Expanded examples.
- Extended validation.

### Changed
- Quickstart and repository structure documentation.

### Fixed
- Schema consistency and CI path handling.

## [v0.1] - 2025-09-01

### Added
- Initial MCP4H schema and lexicon definitions.
- Baseline examples and JSON validation.
- Initial public documentation and governance structure.
- Archival/DOI groundwork.
