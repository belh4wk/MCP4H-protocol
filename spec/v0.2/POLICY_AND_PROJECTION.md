# Policy and Projection

**Status:** candidate design, non-normative

v0.1.x Cue v1 combines semantic identity, attention behavior and modality intent in one portable cue structure.

v0.2 preserves the useful behavior while separating the concepts.

## Policy Decision

Policy decides whether, when and how strongly an Interpretation should compete for attention.

Candidate shape:

```json
{
  "mcp4h": "0.2-draft",
  "kind": "policy",
  "id": "policy-...",
  "created_at": "...",
  "relations": [
    {
      "type": "governs",
      "ref": "int-..."
    }
  ],
  "policy": {
    "action": "surface",
    "priority": 70,
    "attention": {
      "cooldown_ms": 500,
      "merge_key": "vehicle.tyre.front_left",
      "merge_strategy": "latest"
    },
    "reason": "profile-default"
  }
}
```

Potential actions include:

- `surface`
- `suppress`
- `defer`
- `merge`
- `escalate`

The final vocabulary can be extended if needed.

### What belongs in policy

Good candidates:

- priority;
- cooldown;
- dedupe;
- merge;
- escalation;
- quiet periods;
- interruption budgets;
- urgency handling;
- context-dependent suppression.

### Severity is not priority

A domain profile may describe a condition as severe or critical.

Policy separately determines attention behavior.

Examples:

- a severe mechanical condition may be logged but not interrupt a current safety-critical task;
- a minor navigation hazard may need immediate attention;
- a high-G aircraft state may be intense but entirely expected.

The core should therefore not use one `severity` field as a proxy for policy priority.

## Arbiter

The existing Arbiter maps naturally to an optional policy engine.

An implementation may use deterministic rules, state machines, learned models, AI or a mixture.

The protocol defines the contract, not the required policy engine.

## Projection record

Projection maps semantic meaning toward a declared receiver Capability Profile.

Candidate shape:

```json
{
  "mcp4h": "0.2-draft",
  "kind": "projection",
  "id": "proj-...",
  "created_at": "...",
  "relations": [
    {
      "type": "projects",
      "ref": "int-..."
    },
    {
      "type": "uses_capability",
      "ref": "cap-..."
    }
  ],
  "projection": {
    "outputs": []
  }
}
```

The Projection is separate by default.

An Interpretation does not need to know which renderer eventually expresses it.

## Output

A projection output describes one carrier and target.

Example:

```json
{
  "carrier": "haptic.vibration",
  "target": "pedal.front",
  "parameters": {
    "pattern": "breakaway-ramp",
    "frequency_hz": 46,
    "amplitude": {
      "value": 0.58,
      "scale": "renderer.normalized-output/1"
    }
  }
}
```

If 46 Hz is chosen because that is how a shaker communicates the semantic event, it belongs in Projection/Rendering.

If 46 Hz were actually an observed physical property of the source phenomenon, that source frequency could appear in Observation.

This distinction is central to MCP4H.

## Optional linking from semantics

Projection records should normally reference the semantic records they express.

The semantic record does not need a back-link to remain valid.

When an application needs bidirectional graph navigation, the shared `relations` mechanism can link records in either direction.

An Interpretation may also declare preservation requirements without selecting an output device:

```json
"projection_requirements": {
  "preserve": [
    "event_identity",
    "spatial.side",
    "state"
  ]
}
```

## Projection preservation declaration

A Projection may report what it preserved or degraded:

```json
"preservation": {
  "preserved": [
    "event_identity",
    "spatial.side",
    "state"
  ],
  "degraded": [
    "magnitude_resolution"
  ]
}
```

This may later support semantic-invariance conformance tests.

## Response

A Response is independently addressable and may reference either a semantic record or Projection.

It may represent:

- acknowledgement;
- operator action;
- machine action;
- correction;
- dismissal;
- feedback.

Response remains optional for the first v0.2 schema cycle.
