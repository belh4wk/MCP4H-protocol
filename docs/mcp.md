# MCP interoperability

MCP4H includes a reference bridge for the Model Context Protocol ecosystem.

The protocols are complementary rather than interchangeable.

- **MCP** exposes tools, resources and results between software/agents.
- **MCP4H** structures meaningful interpreted information for projection toward a receiver.

## Current reference path

```text
MCP tool event/result
  -> MCP4H mapping
  -> validation
  -> projected cue payload
  -> webhook / renderer
```

Implementation:

`bridges/mcp/`

Examples:

`examples/messages/mcp/`

Runnable path:

`docs/quickstart.md`

## Boundary rule

The bridge performs structural/source mapping.

Domain interpretation should be explicit.

Prioritization, suppression, dedupe, escalation or attention decisions belong to an optional policy/Arbiter layer rather than being hidden inside the bridge.

## v0.2 direction

The bridge will eventually map into the receiver-aware semantic model being designed for v0.2.

Existing v0.1.x examples remain the compatibility baseline until a migration contract is published.
