# Bridges

Bridges are boundary adapters.

They connect MCP4H-compatible information to real sources, transports or endpoints without becoming the universal semantic model themselves.

## In plain terms

- **Source bridge** - adapts an external source into MCP4H-compatible observations/semantics.
- **Delivery bridge** - adapts MCP4H output to a transport or external endpoint.
- **Protocol** - shared contracts, schemas, profiles and validation rules.
- **Policy / Arbiter** - optional prioritization, suppression, merging, escalation or attention logic.
- **Renderer** - produces the final carrier/output.

## Bridge rule

A bridge should stay as simple as the boundary allows.

It should usually:

- preserve useful source identity and timing;
- preserve provenance;
- map known fields explicitly;
- normalize only where a domain/profile defines a meaningful normalization;
- fail observably when it cannot preserve the required contract.

A bridge should not casually:

- flatten every value to one universal scale;
- invent meaning outside its domain contract;
- hide policy decisions;
- make one output renderer the definition of the semantic event.

If a component is deciding which cue matters most, whether something should interrupt, or whether competing events should merge, that is policy.

If it is deciding how a semantic event should be expressed for a device/receiver, that is projection/rendering.

See the root `BRIDGE_SPEC.md` for the current guidance.
