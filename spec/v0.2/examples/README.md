# v0.2 Design Examples

These files are **non-normative design examples**. They are not yet validated against a v0.2 JSON Schema.

The examples exercise the shared envelope grammar and linked-record model.

## Land-chassis example

- `tyre-breakaway.observation.json` - source Observation record
- `tyre-breakaway.semantic.json` - Interpretation record linked to the Observation
- `tyre-breakaway.policy.json` - optional Policy record
- `receiver-capability.simrig.json` - Capability Profile
- `tyre-breakaway.projection.json` - receiver-specific Projection record
- `tyre-breakaway.bundle.json` - example low-latency transport bundle containing Observation + Interpretation records

The `.semantic.json` filename is retained from the earlier design pass, but its content is now explicitly an `interpretation` record rather than a combined observation/interpretation envelope.

## Airframe example

- `airframe-load.observation.json`
- `airframe-load.semantic.json`

These demonstrate that aircraft load semantics do not need to pretend to be land-chassis semantics.

## Accessibility/navigation example

- `accessibility-proximity.observation.json`
- `accessibility-proximity.semantic.json`

This is the first non-simulation pressure test of the base record model.

## Important boundary

A semantic Interpretation such as:

```text
tyre approaching breakaway
```

is separate from a Projection choice such as:

```text
46 Hz breakaway-ramp pattern on pedal.front
```

The latter is valid only for a receiving path that declares compatible capability.
