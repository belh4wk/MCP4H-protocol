# MCP4H Roadmap

**Updated:** 2026-09-11

> **Preserve meaning. Adapt the carrier.**

MCP4H is moving from a capable v0.1.x cue/projection protocol into a clearer receiver-aware semantic architecture.

The next milestone is not "more modalities".

It is a cleaner separation between what was observed, what it means, optional policy, how it should be projected, what the receiver can support, and how it is transported and rendered.

## Current baseline: v0.1.x

The current compatibility line is **v0.1.5 plus subsequent additive bridge/tool work on `main`**.

Existing strengths include portable cue behavior, Behavior Policy, Renderer Capabilities, schema-driven validation, projected payload examples, Model Context Protocol interoperability, webhook delivery, local web rendering and runnable validation/demo tooling.

## Stage 1 - Foundations alignment

**Status:** CURRENT

Deliver:

- `FOUNDATIONS.md`;
- updated README;
- superseded text-first assumption recorded explicitly;
- receiver-aware terminology;
- updated project status;
- roadmap aligned with current Tyto direction;
- historical citation titles preserved.

Success: someone arriving cold can understand the problem; the `4` is clearly **For**; AI/Arbiter is optional; v0.1.x compatibility and v0.2 direction are not confused.

## Stage 2 - v0.2 neutral semantic core

Design and implement a small base model for:

- a shared envelope grammar;
- independently addressable Observation and Interpretation records;
- linked optional Policy, Projection and Response records;
- layer-scoped confidence/uncertainty;
- provenance;
- transformation lineage;
- temporal structure;
- spatial/relational structure;
- extension/profile references.

Text must not be required as the canonical semantic intermediate.

## Stage 3 - Receiver capability model

Evolve Renderer Capabilities into a broader receiver/render capability contract.

Potential capability areas:

- carrier/modalities;
- topology and location;
- temporal resolution;
- frequency range;
- dynamic range;
- latency;
- calibration/fingerprint reference;
- accessibility constraints;
- preferences;
- current context.

## Stage 4 - Domain profiles

Initial profiles:

- machine dynamics - land chassis;
- machine dynamics - airframe;
- conversation/social.

Domain vocabularies are extensions, not the universal MCP4H vocabulary.

## Stage 5 - MCP4SH dual-domain proof

Use MCP4SH as the first serious conformance pressure test.

Deliver land-chassis and airframe reference packets, a shared base envelope, tactile renderer example and receiver capability example.

Explore, where supported by vendor/platform interfaces:

```text
game/platform data
  -> MCP4SH semantic interpretation
  -> FullForce/OEM projection
  -> wheelbase
```

This is an integration target, not a currently shipped MCP4H capability.

## Stage 6 - Non-simulation proof

Choose one focused reference problem:

- accessibility navigation/environment event; or
- remote-machine state/operator cue.

Render one semantic event through at least two valid receiver configurations.

## Stage 7 - SDK, validation and conformance

Deliver canonical schema(s), migration guide, C# and Python reference libraries, validator/CLI, sample producer, sample renderer, provenance tests, capability examples and conformance fixtures.

## Stage 8 - External interoperability

Have another developer/system implement one side of the contract independently.

Success means interoperability works because of the specification, not because Tyto controls both endpoints.

## Stage 9 - Governance and standards path

Only after independent implementation:

- tighten versioning and extension governance;
- publish conformance requirements;
- document compatibility policy;
- expand external review;
- evaluate standards-body pathways where useful.

The goal is not a standards logo. The goal is an architecture people can actually implement.

## Longer-horizon research

Keep explicit but evidence-led research tracks for AI interpretation and policy, advanced tactile/neurohaptic interfaces, environmental/ecological state projection, bioacoustic and multimodal animal-communication data, and cross-species receiver models.

These are research directions, not present-tense product claims.

## Decision filter

New work should strengthen at least one of:

- preservation of meaning across a boundary;
- independence from one source/carrier/renderer/vendor;
- receiver-awareness;
- provenance/inspectability;
- outside implementability;
- genuine cross-domain proof.
