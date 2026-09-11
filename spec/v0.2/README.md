# MCP4H v0.2 Semantic Model - Design Draft

**Status:** design draft, non-normative  
**Date:** 2026-09-11  
**Compatibility:** does not replace or modify v0.1.x

> **Preserve meaning. Adapt the carrier.**

This directory is the design checkpoint between the MCP4H foundation alignment and the first normative v0.2 JSON Schemas.

The goal is to agree the contracts before encoding them as schema.

## Core decision: one grammar, multiple records

v0.2 should not force observation, interpretation, policy and projection into one monolithic semantic object.

Instead, MCP4H uses a **shared envelope grammar** with separately addressable records.

Initial record family:

1. **Observation** - what was measured, reported or emitted.
2. **Interpretation** - what an observation or set of observations is believed to mean.
3. **Policy Decision** - optional decision about priority, suppression, merging, escalation or attention.
4. **Projection** - how meaning is mapped toward a declared receiver capability.
5. **Response** - optional acknowledgement, action, correction or feedback.

A **Capability Profile** is a referenced receiver/render resource using the same identity/versioning principles.

This makes patterns such as the following natural:

```text
Observation A
  -> Interpretation 1
  -> Interpretation 2
  -> Interpretation 3
```

or:

```text
Interpretation X
  -> Policy A
  -> Projection A
  -> Projection B
```

Logical separation does not require separate network hops. A low-latency implementation may bundle several records into one transport message.

## Shared envelope grammar

Each record should share a small header such as:

```json
{
  "mcp4h": "0.2-draft",
  "kind": "observation",
  "id": "obs-...",
  "created_at": "2026-09-11T16:00:00Z",
  "profile": {
    "id": "machine.dynamics.land_chassis",
    "version": "0.1-draft"
  },
  "relations": [],
  "provenance": {}
}
```

The record-specific body then appears under the matching key, for example `observation`, `interpretation`, `policy`, `projection` or `response`.

## Decisions already made

### Confidence is layer-specific

Support confidence at both:

- Observation level - source/observation confidence or quality;
- Interpretation level - confidence in the inferred meaning.

Individual measurements may additionally express uncertainty.

There should be no ambiguous universal top-level confidence field.

### Severity is not universal

The MCP4H core should not define one universal `severity` field or scale.

Domain profiles may define severity, criticality, intensity or equivalent concepts where they are meaningful.

Policy separately decides attention priority, interruption and escalation.

### Carrier identifiers are open-ended

MCP4H should publish recommended common carrier identifiers but must not impose a permanently closed global enum.

Examples:

- `haptic.vibration`
- `haptic.force`
- `audio`
- `visual.display`
- `visual.led`
- `text`
- `motion`
- `machine.event`

Future/vendor/research carriers can use additional namespaced identifiers.

### Projection is separate by default

A semantic record should remain valid before a final renderer/carrier is selected.

Projection records reference semantic records and Capability Profiles.

All records may use relations when an application needs explicit links in either direction.

An Interpretation may optionally declare **projection preservation requirements**, such as preserving direction or state, but it should not contain device-specific renderer choices.

## Design constraints

The v0.2 model should:

- not require text as an intermediate;
- not require AI;
- not require one transport;
- not require one renderer;
- not impose one domain vocabulary;
- preserve source units and provenance where they matter;
- allow profile-defined normalization without assuming all useful values are 0.0-1.0;
- support temporal, spatial, relational and spectral structure;
- distinguish observed state from interpreted state;
- distinguish semantic seriousness from attention policy;
- support simple implementations without flattening richer domains.

## Reference pressure tests

The design is pressure-tested against:

- tyre approaching breakaway;
- aircraft entering a high positive-G load state;
- proximity hazard for an accessibility/navigation receiver.

If these examples require domain leakage into the base contract, the base should change before schemas are written.

## Files

- `SEMANTIC_ENVELOPE.md` - shared envelope grammar and semantic record model
- `CAPABILITY_PROFILE.md` - receiver/render capability design
- `POLICY_AND_PROJECTION.md` - optional policy and separate projection contracts
- `MIGRATION_FROM_V0.1.md` - mapping from useful v0.1.x concepts
- `OPEN_QUESTIONS.md` - resolved decisions plus remaining schema questions
- `examples/*.json` - non-normative design examples

The JSON files are illustrative shapes only. They are not conformance fixtures yet.
