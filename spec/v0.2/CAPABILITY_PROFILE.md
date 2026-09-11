# Capability Profile

**Status:** candidate design, non-normative

v0.1.5 introduced Renderer Capabilities. v0.2 broadens that work into a receiver/render capability contract without losing deterministic fallback behavior.

## Why broaden the model

A renderer is only one part of the receiving path.

Projection may depend on:

- the person/operator;
- output device(s);
- actuator/speaker/display topology;
- calibration;
- available carriers;
- timing constraints;
- accessibility constraints;
- current context.

The Capability Profile describes what can be delivered without making the semantic event itself device-specific.

## Candidate shape

```json
{
  "mcp4h": "0.2-draft",
  "kind": "capability_profile",
  "id": "cap-rig-reference",
  "created_at": "2026-09-11T16:00:00Z",
  "capability_profile": {
    "receiver": {
      "kind": "composite"
    },
    "carriers": [],
    "constraints": {},
    "calibration": {}
  }
}
```

## Receiver kind

Useful common values include:

- `person`
- `device`
- `system`
- `composite`

The final contract should allow extensibility rather than assume this list is eternal.

A composite receiver is useful for a path such as:

```text
person + seat shaker + pedal transducer + wheelbase
```

## Open-ended carrier identifiers

Carrier identifiers are intentionally **not** a permanently closed global enum.

Recommended common identifiers can provide interoperability, for example:

- `haptic.vibration`
- `haptic.force`
- `audio`
- `visual.display`
- `visual.led`
- `text`
- `motion`
- `machine.event`

Vendor, research or future carrier identifiers may use additional namespaced identifiers.

A carrier unknown to one implementation is still syntactically valid; it is only usable when the receiving path declares compatible capability or extension handling.

## Per-carrier capabilities

Example:

```json
{
  "id": "haptic.vibration",
  "targets": [
    {
      "id": "seat.rear",
      "location": "rig.rear"
    }
  ],
  "temporal": {
    "max_update_hz": 200
  },
  "spectral": {
    "frequency_hz": {
      "min": 20,
      "max": 80
    }
  }
}
```

## Topology

A receiver path may have multiple independently addressable targets.

Examples:

- front/rear tactile zones;
- left/right pedal motors;
- steering-wheel motor;
- speaker positions;
- display regions;
- wearable locations.

Topology should use declared identifiers rather than assume automotive corners or body locations in the universal schema.

## Temporal capability

Potential fields:

- maximum update rate;
- minimum useful pulse duration;
- maximum practical latency;
- queue depth;
- scheduling precision.

## Spectral capability

Where relevant:

- frequency range;
- frequency resolution;
- known unusable bands;
- preferred operating region.

Not every carrier needs a spectral section.

## Dynamic capability

Potential fields:

- minimum/maximum output;
- resolution;
- safe continuous range;
- peak range.

Values should retain explicit units/scales.

## Calibration

Calibration should be referencable rather than necessarily embedded.

```json
"calibration": {
  "profile_id": "rig-fingerprint-2026-09-11",
  "version": "1"
}
```

For MCP4SH this is where the long-term Rig Fingerprint concept naturally connects to MCP4H receiver capability.

## Accessibility constraints

A Capability Profile may declare that carriers are unavailable, unsuitable or preferred.

It should describe communication constraints/capabilities relevant to projection rather than encode a medical diagnosis.

Example:

```json
"constraints": {
  "unavailable_carriers": ["audio"],
  "preferred_carriers": ["haptic.vibration", "visual.display"]
}
```

## Static capability vs runtime context

Static or semi-static capability includes:

- hardware;
- topology;
- supported bands;
- calibration;
- declared accessibility constraints.

Runtime context includes:

- current noise level;
- driving state;
- focus mode;
- temporary mute;
- current device occupancy.

Runtime context should probably be a separate referenced record rather than being overloaded into the Capability Profile. This remains a schema-stage question.
