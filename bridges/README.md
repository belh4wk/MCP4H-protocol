# Bridges

Bridges are the **plumbing layer**.

They connect MCP4H packets to real transports or endpoints, but they do **not** define the protocol and they do **not** make higher-order judgment calls.

## In plain terms

- **Bridge** = connector / adapter / transport glue
- **Protocol** = shared packet grammar, schemas, examples, bindings, and validation rules
- **Arbiter** = prioritization or decision logic that decides what should be surfaced, suppressed, delayed, merged, or escalated

## Bridge rule

A bridge should stay as dumb as practical:

- read MCP4H packets
- map them to an output transport
- preserve metadata and provenance
- fail loudly and observably

If a component is deciding *which* cue matters most, *when* it should interrupt, or *whether* competing cues should be merged, that belongs in an **arbiter**, not a bridge.
