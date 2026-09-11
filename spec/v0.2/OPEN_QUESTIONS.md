# v0.2 Decisions and Remaining Open Questions

These items should be settled before the first normative v0.2 JSON Schema is committed.

## Resolved design decisions

### 1. One monolithic Semantic Envelope or multiple records?

**Decision:** shared envelope grammar, multiple independently addressable record kinds.

Observation and Interpretation remain logically separate. Policy, Projection and Response are separate linked records.

Low-latency implementations may bundle several records into one transport message.

### 2. Is `severity` universal?

**Decision:** no.

Domain profiles may define severity, criticality, intensity, risk class or equivalent concepts where meaningful.

Policy uses separate priority/interruption/escalation concepts.

### 3. Does confidence exist at multiple layers?

**Decision:** yes.

At minimum:

- Observation confidence/quality;
- Interpretation confidence.

Measurement-level uncertainty is also allowed where relevant.

No ambiguous universal top-level confidence field.

### 4. Are carriers a closed enum?

**Decision:** no.

Use open-ended identifiers with a recommended common registry/naming convention.

### 5. Is Projection embedded in semantic records?

**Decision:** no by default.

Projection is a separate record that references semantic records and receiver Capability Profiles.

Semantic records may optionally express preservation requirements and all records may use generic relations when linking is needed.

## Remaining open questions

### A. Exact mandatory shared-header fields

Likely:

- `mcp4h`
- `kind`
- `id`
- `created_at`

Need to decide whether `relations`, `profile` and `provenance` are optional in every record kind or required selectively.

### B. Relation vocabulary

Should core relation types be:

- a small closed set with extension namespacing;
- fully open strings;
- a recommended registry with syntactic validation only?

Current leaning: small recommended core vocabulary plus namespaced extensions.

### C. Bundle transport shape

Need a minimal bundle format for low-latency multi-record delivery without turning the bundle into semantic meaning itself.

### D. Units

Keep units explicit and simple initially.

Need to decide whether v0.2 defines a small unit convention, references an existing notation, or leaves unit restrictions entirely to domain profiles.

### E. Normalized semantic magnitudes

A normalized number should reference a declared scale/profile.

Need to finalize the scale identifier and whether range metadata is included inline or referenced.

### F. Capability Profile vs runtime context

Capability Profile should remain mostly static/semi-static.

Need a separate record/resource design for temporary context such as mute state, environmental noise, occupancy or focus mode.

### G. Response scope

Response remains optional for the first schema cycle.

Need to decide whether the first normative v0.2 release includes a minimal Response schema or defers it one minor revision.

### H. Profile identity and versioning

Need to define namespacing/version rules for domain profiles without requiring a central authority for private/vendor extensions.

### I. Extension record kinds

Need to decide how future record kinds extend `kind` without breaking validators.

### J. Repository migration

Current v0.1.x paths stay in place until converters and v0.2 schemas exist.

The eventual move into `spec/v0.1/` must update `$ref` paths, tests, CI, examples and documentation in one controlled pass.
