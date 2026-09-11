# Shared Envelope Grammar and Semantic Records

**Status:** candidate design, non-normative

The v0.2 core is a shared envelope grammar with separately addressable records rather than one monolithic semantic packet.

Observation and Interpretation are the primary semantic records.

Policy, Projection and Response are linked records that operate on or respond to semantic records.

## Shared header

Candidate shape:

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

### `mcp4h`

Contract/version identifier.

The exact final version string format remains a schema-stage decision.

### `kind`

Identifies the record contract.

Initial core kinds:

- `observation`
- `interpretation`
- `policy`
- `projection`
- `response`
- `capability_profile`

Whether extension record kinds use a namespaced convention is still open.

### `id`

Unique record identifier.

Records should be independently addressable so one observation can support multiple interpretations and one interpretation can support multiple projections.

### `created_at`

Time the MCP4H record was created.

This is not necessarily the source observation time.

### `profile`

Optional/required according to record kind.

A profile identifies domain semantics without leaking domain-specific vocabulary into the universal envelope.

Example:

```json
"profile": {
  "id": "machine.dynamics.airframe",
  "version": "0.1-draft"
}
```

### `relations`

Generic links between independently addressable records.

Candidate shape:

```json
"relations": [
  {
    "type": "interprets",
    "ref": "obs-123"
  }
]
```

Likely common relationships include:

- `derived_from`
- `interprets`
- `governed_by`
- `projects`
- `responds_to`
- `updates`

The exact normative relation vocabulary remains open.

### `provenance`

Enough lineage to answer where a record came from and what transformed it.

Candidate fields:

```json
"provenance": {
  "trace_id": "...",
  "transformations": [
    {
      "component": "mcp4sh.semantic.land_chassis",
      "version": "1.2-dev",
      "operation": "interpret"
    }
  ]
}
```

The goal is useful audit/debug lineage, not a general workflow language.

## Observation record

Observation records what was measured, reported or emitted before interpretation.

```json
{
  "mcp4h": "0.2-draft",
  "kind": "observation",
  "id": "obs-123",
  "created_at": "...",
  "profile": {
    "id": "machine.dynamics.land_chassis",
    "version": "0.1-draft"
  },
  "source": {
    "system": "simulator.example",
    "component": "vehicle.telemetry"
  },
  "subject": {
    "type": "vehicle.tyre",
    "id": "front_left"
  },
  "observation": {
    "observed_at": "...",
    "confidence": 0.99,
    "measurements": []
  }
}
```

### Observation confidence

`observation.confidence` describes confidence/quality in the observed record as represented.

This is distinct from confidence in a later interpretation.

Individual measurements may carry uncertainty:

```json
{
  "name": "aircraft.normal_acceleration",
  "value": 4.7,
  "unit": "g",
  "uncertainty": 0.03
}
```

The final uncertainty representation still needs a schema decision about units/meaning.

### Measurements

A measurement should preserve:

- namespaced identity;
- source value;
- unit where meaningful.

Optional fields may include uncertainty, range, sample rate, coordinate frame, source-field reference or quality flag.

The base protocol should not require every measurement to become a normalized 0.0-1.0 value.

### Structure

Some observations only make sense with structure over time or space.

Candidate optional container:

```json
"structure": {
  "temporal": {},
  "spatial": {},
  "spectral": {},
  "relations": []
}
```

#### Temporal

Potential concepts:

- duration;
- rate;
- trend;
- recurrence;
- sequence;
- time window;
- sample rate.

#### Spatial

Potential concepts:

- coordinate frame;
- region;
- direction;
- orientation;
- topology/location.

#### Spectral

Potential concepts:

- dominant frequency;
- band;
- modulation;
- phase relationship.

Spectral data is present only when semantically relevant.

## Interpretation record

An Interpretation describes what one or more observations are believed to mean.

```json
{
  "mcp4h": "0.2-draft",
  "kind": "interpretation",
  "id": "int-456",
  "created_at": "...",
  "profile": {
    "id": "machine.dynamics.land_chassis",
    "version": "0.1-draft"
  },
  "relations": [
    {
      "type": "interprets",
      "ref": "obs-123"
    }
  ],
  "interpretation": {
    "type": "vehicle.tyre.breakaway_margin",
    "state": "approaching",
    "confidence": 0.93,
    "attributes": {}
  }
}
```

### Interpretation confidence

`interpretation.confidence` describes confidence in the inferred meaning.

It is intentionally separate from Observation confidence.

Excellent source data does not guarantee an excellent interpretation, and noisy source data can sometimes still support a high-confidence categorical interpretation.

### Semantic identity

`interpretation.type` is a namespaced, profile-defined semantic identity.

Examples:

- `vehicle.tyre.breakaway_margin`
- `aircraft.airframe.load`
- `navigation.hazard.proximity`

### State

`state` is optional and profile-defined.

Examples:

- `approaching`
- `active`
- `recovering`
- `sustained`

The base protocol should avoid a universal domain-state enum.

### Domain severity / criticality

There is no universal MCP4H `severity` field in the core Interpretation contract.

A domain profile may define `severity`, `criticality`, `intensity`, `risk_class` or another concept where useful.

For example:

```json
"attributes": {
  "criticality": "high"
}
```

The profile defines what that value means.

Attention priority remains a separate Policy concern.

### Profile-defined magnitude

Some domains benefit from a normalized semantic magnitude.

A normalized number should identify its scale/profile:

```json
"magnitude": {
  "value": 0.72,
  "scale": "machine.dynamics.tyre.breakaway_margin/0.1"
}
```

An anonymous `0.72` is not portable semantics.

### Optional projection preservation requirements

An Interpretation may optionally state what downstream projections must preserve without selecting a renderer.

Example:

```json
"projection_requirements": {
  "preserve": [
    "event_identity",
    "spatial.side",
    "state"
  ]
}
```

This is intentionally different from saying:

```text
render 46 Hz on channel 2
```

That belongs in Projection.

## One observation, many interpretations

Separately addressable records make alternative or parallel interpretations explicit:

```text
obs-123
  -> int-a (deterministic model, confidence 0.91)
  -> int-b (learned model, confidence 0.84)
  -> int-c (different domain profile, confidence 0.77)
```

Policy or a consuming application can decide what to do with competing interpretations without rewriting the source observation.

## Low-latency bundling

MCP4H should permit a transport bundle containing several records so a low-latency implementation does not need a network hop between conceptual stages.

Example idea:

```json
{
  "mcp4h_bundle": "0.2-draft",
  "records": [
    { "kind": "observation" },
    { "kind": "interpretation" }
  ]
}
```

The bundle is a transport convenience, not a return to one monolithic semantic object.
