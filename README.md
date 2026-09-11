# MCP4H: Multimodal Communications Protocol For Humanity 🦉

> **Preserve meaning. Adapt the carrier.**

MCP4H is an open, receiver-aware communication framework for translating meaningful information across machines, software, people and sensory interfaces.

The problem is simple:

**Useful information often exists in a form the receiver cannot use directly.**

A source may expose telemetry, events, sensor data, logs or model output. One receiver may need touch. Another may need sound, force, light, text, spatial cues or machine-readable state.

MCP4H aims to keep the useful meaning separate enough from the original carrier that it can be expressed appropriately at the other end.

The point is not more data.

The point is clearer translation.

## Start here

- **Foundations:** [`FOUNDATIONS.md`](FOUNDATIONS.md)
- **Quickstart:** [`docs/quickstart.md`](docs/quickstart.md)
- **Assumptions and design rationale:** [`ASSUMPTIONS.md`](ASSUMPTIONS.md)
- **Roadmap:** [`ROADMAP.md`](ROADMAP.md)
- **Current project status:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md)
- **Citation information:** [`CITATIONS.md`](CITATIONS.md)

## In plain English

A source should not dictate how its meaning must be received.

For example, a simulator may expose tyre, suspension and chassis state as numbers. MCP4SH can interpret those values as useful driving events and render them through tactile hardware.

The useful event is the important part.

A different renderer could express the same event through another supported carrier without requiring the source semantics to be reinvented.

## Architectural direction

v0.2 uses a shared envelope grammar with separately addressable records:

```text
Observation record(s)
  -> Interpretation record(s)
  -> optional Policy record(s)
  -> Projection record(s)
  -> Transport / Renderer
  -> optional Response record(s)
```

Records are linked by IDs/relations. One Observation can support multiple Interpretations, and one Interpretation can support multiple Projections. Low-latency implementations may bundle multiple records into one transport message, so logical separation does not require extra network hops.

The current v0.1.x implementation remains the compatibility/runtime line while these v0.2 contracts are designed under `spec/v0.2/`.

Current v0.2 design choices keep confidence scoped to Observation vs Interpretation, leave severity/criticality to domain profiles, keep carrier identifiers open-ended, and keep Projection separate from semantics unless linked through record relations/capability references.

## Text is one carrier

Earlier MCP4H work treated text as the canonical intermediate representation.

That was useful for the initial conversational and dashboard-oriented experiments, but it is too narrow for the wider problem.

Some information is naturally temporal, spatial, relational, spectral, force-related or probabilistic.

MCP4H therefore no longer treats text as a mandatory intermediate for all meaning.

The historical assumption remains recorded in [`ASSUMPTIONS.md`](ASSUMPTIONS.md), where it is marked as superseded rather than deleted.

## Receiver capability

v0.1.5 introduced renderer capabilities, behavior policy and portable cue behavior.

That work is an important bridge toward the next architecture.

A receiver or renderer may need to describe supported carriers, topology, timing/frequency range, latency, dynamic range, accessibility constraints, calibration/fingerprint information, context and preferences.

The same semantic event can then be projected differently while preserving the information that matters.

## AI and the Arbiter

An Arbiter remains a useful optional judgment-assist layer for prioritization, suppression, deduplication, escalation, interruption budgets and context-aware channel substitution.

It is not required for the base protocol.

AI may participate in interpretation or policy, but deterministic systems remain first-class.

See [`arbiter/README.md`](arbiter/README.md).

## Current implementation line: v0.1.x

The latest tagged protocol release is **v0.1.5**.

v0.1.5 includes:

- portable cue behavior;
- priority, confidence and severity;
- cooldown, merge, dedupe and escalation concepts;
- modality intent;
- Behavior Policy;
- Renderer Capabilities;
- schema-driven validation;
- compatible envelope extensions.

The repository also includes practical bridge work added after the tagged release, including:

- Model Context Protocol interoperability;
- projected cue examples;
- webhook delivery;
- local web rendering;
- mapping and validation tools.

The v0.1.x line remains the compatibility baseline while v0.2 foundations are designed.

## MCP interoperability

MCP4H includes a reference bridge for mapping Model Context Protocol tool events/results into MCP4H packets.

- Implementation: [`bridges/mcp/`](bridges/mcp/)
- Examples: [`examples/messages/mcp/`](examples/messages/mcp/)
- Quickstart: [`docs/quickstart.md`](docs/quickstart.md)

MCP and MCP4H solve different layers of the problem.

MCP can help software and agents expose tools, resources and results.

MCP4H focuses on how meaningful interpreted information can be structured and projected toward a receiver.

## Current practical reference: MCP4SH

[MCP4SH](https://github.com/belh4wk/MCP4SH) is Tyto Sensory Labs' first commercial reference implementation and the clearest current proving ground for the wider MCP4H direction.

MCP4SH turns heterogeneous simulation telemetry into coherent tactile cues through normalization, event/state interpretation and effect orchestration.

Its strategic role is larger than one output device or one simulation title:

```text
source-specific data
  -> canonical interpretation
  -> receiver-specific projection
```

The next MCP4SH cycle extends that proof from land vehicles into aircraft dynamics, while preserving domain-specific meaning rather than forcing one domain to imitate the other.

MCP4SH remains a separate product and repository under its own licensing terms.

## Reference domains

MCP4H is being tested against deliberately different classes of problem:

- **Simulation:** vehicle and aircraft state translated into useful sensory cues.
- **Remote operation:** future work around restoring useful machine/environment awareness when the operator is physically separated from the equipment.
- **Accessibility:** future work around translating information away from an unavailable or overloaded sensory channel.
- **People + AI:** making machine interpretation perceivable and inspectable without turning every conclusion into more text.
- **Living-system research:** longer-horizon work where our language or senses should not be assumed to be the only useful representation.

These are trajectories and test domains, not claims that each problem is already solved.

## What this repo is

This repository contains the open MCP4H protocol/framework:

- schemas;
- cues and behavior contracts;
- domain/profile experiments;
- bridge references;
- examples;
- validation tooling;
- documentation;
- governance and prior-art material.

It does not contain the commercial MCP4SH SimHub plugin.

## Repository areas

- `spec/` - protocol/specification work and domain/profile structures
- `schemas/` - current schema assets used by tooling and examples
- `bridges/` - source, transport and delivery bridge references
- `arbiter/` - optional policy/judgment-assist layer
- `examples/` - packets, examples and runnable demonstrations
- `tools/` - validation and demo utilities
- `docs/` - quickstart, explanatory material and historical publications

The v0.2 design cycle will review overlapping historical directories and naming so the specification surface becomes easier for outside implementers to navigate.

## Prior-art disclosure

The architectural concepts and design principles underlying MCP4H are intentionally published as prior art.

- Concept DOI: [10.5281/zenodo.17164550](https://doi.org/10.5281/zenodo.17164550)
- Prior-art disclosure DOI: [10.5281/zenodo.18223144](https://doi.org/10.5281/zenodo.18223144)
- Release-specific citation information: [`CITATIONS.md`](CITATIONS.md)

## Quickstart

Follow [`docs/quickstart.md`](docs/quickstart.md).

The current quickstart exercises the working v0.1.x packet/projection model and the MCP/webhook reference path.

## Design rationale

Important assumptions are superseded when the work provides a better model; they are not silently erased.

See [`ASSUMPTIONS.md`](ASSUMPTIONS.md).

## Status

MCP4H is an active v0.x protocol/framework.

It is not yet a universal standard.

The current foundations pass aligns the project's public architecture before the v0.2 schema cycle begins.

See [`ROADMAP.md`](ROADMAP.md) and [`PROJECT_STATUS.md`](PROJECT_STATUS.md).

## Related projects

- **MCP4SH™** - simulation haptics and machine-state interpretation reference implementation
- **MCP4H Harmonizer** - earlier conversational work built from MCP4H principles; retained as an important domain-specific branch of the project's history

---

© 2025-2026 Dirk Van Echelpoel / Tyto Sensory Labs

MCP4H™ means **Multimodal Communications Protocol For Humanity**. The `4` means **For**; it does not limit the framework to four carriers or modalities.
