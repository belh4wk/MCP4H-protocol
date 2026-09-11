# Migration Notes: v0.1.x to v0.2

**Status:** design mapping, not a compatibility specification

The goal is to evolve MCP4H without pretending v0.1.x was a mistake.

v0.1.x contains useful concepts that move into clearer contracts in v0.2.

## Candidate mapping

| v0.1.x concept | v0.2 destination |
| --- | --- |
| `origin` | Observation source and/or Provenance |
| `actor` | profile-specific participant/subject data where relevant |
| root `text` | source Observation or text Projection depending on role |
| `metadata.heat` | social/conversation profile |
| `metadata.valence` | social/conversation profile |
| `metadata.tone` | social/conversation profile |
| `civility_flags` | social/conversation profile |
| `reasoning_moves` | social/conversation profile |
| `constraints_detected` | domain profile or Interpretation attributes |
| `metadata.confidence` | Observation confidence or Interpretation confidence, based on actual meaning |
| `extensions` | profile-specific data/extensions |
| `cues[].type` | Interpretation semantic type |
| `cues[].severity` | domain-profile severity/criticality where meaningful |
| `cues[].priority` | Policy Decision |
| `cues[].attention` | Policy Decision |
| `cues[].modalities` | Projection constraints/intent and Projection record |
| `cues[].data` | profile-specific Interpretation attributes |
| `cues[].provenance` | expanded record Provenance |
| `behavior_policy` | Policy profile / Policy engine input |
| `renderer_capabilities` | Capability Profile |

## Severity

v0.1 Cue v1 uses `severity` as receiver-facing seriousness.

v0.2 should not promote this to a universal core scale.

Where severity/criticality is meaningful, the domain profile defines it.

Attention priority and interruption behavior belong in Policy.

## Confidence

v0.2 intentionally permits confidence at more than one layer:

- `observation.confidence` - confidence/quality in the observed record;
- `interpretation.confidence` - confidence in the inferred meaning;
- measurement-level uncertainty where required.

A v0.1 `metadata.confidence` field cannot be migrated correctly without knowing what it was intended to describe.

Ambiguous conversion should be reported rather than guessed.

## Text

Root `text`, cue labels and text modality fields must be classified by role:

- source text that was observed;
- semantic/developer label;
- receiver-facing text Projection.

Those roles should not be conflated.

## Modality intent

v0.1 Cue v1 embeds preferred/allowed modalities.

v0.2 separates:

- semantic preservation requirements;
- Policy preferences/constraints;
- Capability Profile support;
- actual Projection outputs.

The semantic record can exist before a renderer is selected.

## Renderer Capabilities

v0.1.5 Renderer Capabilities is an important predecessor of the v0.2 Capability Profile.

The main expansion is from a renderer-only view toward the usable receiver path, including topology, calibration, accessibility constraints and open-ended carriers.

## Compatibility approach

Preferred direction:

- keep v0.1.x validators and examples intact;
- add v0.2 as a new contract;
- provide deterministic converters where mapping is unambiguous;
- report information loss or ambiguity where mapping is not safe;
- never relabel a v0.1.x packet as v0.2 without transformation;
- move historical v0.1.x directories only during a dedicated reference/path migration.
