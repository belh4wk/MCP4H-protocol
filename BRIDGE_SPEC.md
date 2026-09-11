# MCP4H Bridge Technical Specification

**Status:** v0.1.x bridge guidance aligned for the v0.2 foundation cycle
**Updated:** 2026-09-11

A bridge connects an external source or destination to MCP4H.

A bridge is not the universal semantic model.

Its job is to map between a source-specific representation and the MCP4H contract while preserving useful source truth.

## Bridge responsibilities

A source bridge may:

- identify the source and source event/state;
- preserve useful raw/source fields where appropriate;
- map source fields into a domain profile;
- normalize values when the profile defines a meaningful normalization;
- attach timestamps and provenance;
- attach confidence when interpretation occurs at the bridge;
- emit a valid MCP4H packet.

A delivery/output bridge may adapt a projected payload to a transport or external service while preserving identifiers and provenance.

## What a bridge should not do by default

A bridge should not:

- collapse all values to 0.0-1.0 merely for convenience;
- invent universal meaning from a source-specific field;
- discard source units or context when they remain relevant;
- silently convert an interpretation into source truth;
- require an Arbiter or AI service;
- hard-code one renderer as the meaning of the event.

Normalization is useful when it makes comparable semantics possible.

Normalization is harmful when it destroys distinctions required by the domain.

## Policy and Arbiter

Prioritization, suppression, deduplication, escalation and interruption policy may be handled by an optional policy/Arbiter layer.

A bridge can provide metadata needed by policy. It should not require the Arbiter to exist.

## v0.1.x compatibility

Existing bridge examples and candidate/projected payload flows remain valid for the v0.1.x line.

This document does not redefine the current schema.

The v0.2 design cycle will define a clearer relationship between:

```text
Source
  -> Observation
  -> Interpretation
  -> optional Policy
  -> Projection
```

Bridges may implement more than one conceptual step in small systems, but those responsibilities should remain distinguishable.

## Design rule

> **Bridges adapt boundaries; they should not become the place where every domain, renderer and policy rule accumulates.**
