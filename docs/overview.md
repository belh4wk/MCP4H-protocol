# MCP4H Overview

MCP4H is an open, receiver-aware communication framework.

Its core idea is simple:

> **Preserve meaning. Adapt the carrier.**

A source may expose telemetry, events, sensor data, logs or model output.

A receiver may need touch, force, audio, light, text, spatial cues or another supported form.

MCP4H aims to keep those ends from becoming unnecessarily coupled.

## Conceptual flow

```text
Observation record(s)
  -> Interpretation record(s)
  -> optional Policy record(s)
  -> Projection record(s)
  -> Transport / Renderer
  -> optional Response record(s)
```

The records share a small envelope grammar and link by IDs/relations. A low-latency transport may bundle several records in one message.

## Current v0.1.x implementation

The v0.1.x line already contains useful building blocks:

- cue identity and metadata;
- confidence, severity and priority;
- cooldown, merge, dedupe and escalation behavior;
- Behavior Policy;
- Renderer Capabilities;
- schema validation;
- projected payloads;
- transport/bridge examples.

These remain the compatibility baseline while v0.2 is designed.

## v0.2 direction

The next architecture separates source observations from interpreted meaning more explicitly and broadens renderer capability into receiver capability.

The intended base will support:

- provenance;
- uncertainty;
- temporal structure;
- spatial/relational structure;
- spectral structure where relevant;
- domain-specific profiles;
- replaceable transports and renderers.

## Reference example

In MCP4SH:

```text
title-specific simulation telemetry
  -> normalization / conditioning
  -> meaningful vehicle state
  -> tactile projection
  -> physical rig
```

The same semantic event may later support another valid renderer without changing the source-domain meaning.

## Protocol boundaries

- **Bridge** - adapts a source, transport or external endpoint.
- **Semantic layer** - describes observations and interpreted meaning.
- **Policy / Arbiter** - optional prioritization, suppression, merge or escalation logic.
- **Projection** - maps meaning toward receiver capabilities.
- **Renderer** - produces the final output.

Small implementations may combine these responsibilities in one process.

The contract should still keep them conceptually distinguishable.

## Status

MCP4H is an active v0.x framework.

For the current foundation, see:

- `FOUNDATIONS.md`
- `ASSUMPTIONS.md`
- `ROADMAP.md`
- `PROJECT_STATUS.md`
