# MCP Bridge - Model Context Protocol

This bridge makes MCP4H interoperable with the Model Context Protocol ecosystem.

The two protocols address different layers:

- **MCP** helps software and agents expose tools, resources and results.
- **MCP4H** focuses on how useful interpreted information can be structured and projected toward a receiver.

## Current goal

Map MCP tool events/results into valid MCP4H v0.1.x packets, validate them, and optionally deliver projected payloads to supported endpoints.

## Current implementation

This folder now includes working reference pieces rather than only a skeleton.

The wider repo also includes:

- a minimal MCP server;
- validation/mapping tools;
- example MCP messages;
- projected payload examples;
- webhook publication paths;
- local rendering examples.

See `docs/quickstart.md` and `examples/messages/mcp/`.

## Responsibilities

### Bridge = connector / mapping boundary

The MCP bridge:

- receives MCP-compatible events/results;
- preserves useful origin/trace information;
- maps them into MCP4H-compatible structures;
- avoids inventing unrelated domain meaning;
- can hand packets to validation, policy or delivery components.

### Protocol = shared contract

The MCP4H schema, profiles and canonical examples define the packet contract.

### Policy / Arbiter = optional judgment assist

Prioritization, suppression, rate limiting, escalation, interruption decisions and channel substitution may belong in an optional policy/Arbiter layer.

The MCP bridge must not require that layer to exist.

## Design rule

If mapping a tool result requires domain interpretation, make that boundary explicit.

If a component is deciding whether something deserves attention, that is policy rather than transport mapping.

## v0.2 direction

The current bridge remains a v0.1.x compatibility/reference path.

As v0.2 develops, MCP mapping should target the clearer sequence:

```text
MCP result
  -> Observation
  -> optional Interpretation
  -> optional Policy
  -> Projection
```

This should remain additive until a migration path is explicitly defined.
