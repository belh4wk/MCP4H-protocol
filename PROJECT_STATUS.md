# Project Status - MCP4H Protocol

**Last updated:** 2026-09-11
**Latest tagged protocol release:** v0.1.5
**Current direction:** v0.2 semantic model design

## Current state

MCP4H is an active v0.x protocol/framework with working schemas, validation, bridge examples and transport/rendering demonstrations.

The project has moved beyond its original 2025 trail-braking/conversation-oriented framing.

## What exists today

### v0.1.5
- portable cue behavior;
- priority, confidence and severity;
- cooldown/rate-limit concepts;
- merge/dedupe behavior;
- optional escalation;
- modality intent;
- Behavior Policy;
- Renderer Capabilities;
- schema-driven validation.

### MCP interoperability on `main`
The repo includes a reference Model Context Protocol path:

```text
MCP tool event/result
  -> MCP4H mapping
  -> projected cue payload
  -> webhook/render target
```

This includes `bridges/mcp/`, a minimal MCP server, mapping/validation tools, example messages and projected cue examples.

### Delivery/rendering examples
The repo includes webhook utilities, local web rendering, Slack/Teams reference examples, stream dedupe/cooldown options and demo tooling.

See [`docs/quickstart.md`](docs/quickstart.md).

### Optional policy layer
The Arbiter is already documented in its own area as a separable judgment-assist layer.

Preferred interpretation: useful and optional; not the brain of the protocol.

### Practical reference implementation
MCP4SH has matured outside this repo as Tyto Sensory Labs' first commercial reference implementation.

It demonstrates heterogeneous telemetry normalization, semantic event/state interpretation, cross-title consistency, tactile projection and real hardware mapping/calibration workflows.

MCP4SH remains a separate repository/product.

## What is changing now

The 2026 foundations alignment updates the project around:

> **Preserve meaning. Adapt the carrier.**

Key corrections:

- text is no longer the mandatory universal intermediate;
- the framework is not limited to four modalities;
- the `4` in MCP4H means **For**;
- receiver capability becomes first-class;
- temporal, spatial, relational and spectral structure may carry meaning;
- provenance and confidence become first-class design goals;
- AI/Arbiter logic remains optional;
- domain semantics move toward explicit profiles over a neutral base.

Current v0.2 design decisions:

- one shared envelope grammar with separate Observation, Interpretation, Policy, Projection and Response records;
- confidence is scoped separately to Observation and Interpretation;
- severity/criticality is profile-specific rather than universal;
- carriers are open-ended identifiers;
- Projection is separate from semantics by default but linkable through relations and Capability Profiles;
- low-latency record bundling is allowed as a transport convenience.

## Compatibility position

v0.1.x remains the compatibility baseline.

The foundations update does not silently redefine existing v0.1.x packets.

v0.2 requires an explicit migration/compatibility story before becoming canonical.

## Immediate next work

1. Finalize mandatory shared-header fields, relation vocabulary, unit handling and bundle shape.
2. Author the first non-final v0.2 JSON Schemas.
3. Build deterministic v0.1.x -> v0.2 conversion fixtures where mapping is unambiguous.
4. Evolve Renderer Capabilities into the normative receiver Capability Profile.
5. Formalize land-chassis and airframe domain profiles.
6. Add one focused non-simulation reference prototype.
7. Consolidate overlapping specification directories only after schema references/migrations are ready.
8. Seek an independent external implementation before standards work.

## Repository cleanup deferred until after foundations

The repository currently carries historical structure from multiple development cycles, including overlapping areas such as `schema` / `schemas` and `profiles` / `domain_profiles`.

These should be reviewed during the v0.2 schema pass, not reorganized blindly before the canonical model is agreed.

## Historical documents

The original 2025 manifesto/whitepaper and citation titles remain part of the published historical record.

Terminology such as "4-Point Harness" should remain verbatim inside bibliographic citations and archived publications.

Current working architecture should point readers to `FOUNDATIONS.md`, `README.md`, `ASSUMPTIONS.md` and `ROADMAP.md`.

## Current definition of success

MCP4H has "legs" when:

- a semantic message can survive different transports;
- a receiver can declare capabilities instead of receiving device assumptions;
- transformations preserve provenance;
- MCP4SH can use the architecture without conceptual contortions;
- a non-haptic/non-simulation example feels natural;
- an outside developer can implement one endpoint from the public specification.
