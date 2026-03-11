# MCP Bridge (Model Context Protocol)

This bridge makes **MCP4H™** interoperable with the **Model Context Protocol (MCP)** ecosystem.

**Goal:** convert MCP tool-call events/results into MCP4H packets (and optionally publish MCP4H cues back out to human channels).

## Responsibilities (hard boundaries)

- **Bridge = connector / plumbing**
  - Connects to MCP servers/hosts (JSON-RPC) or consumes MCP logs/events.
  - Maps MCP tool results / resources into **MCP4H packets** (no “meaning logic” beyond mapping).
- **Protocol = meaning + validation**
  - The MCP4H schema and canonical examples define packet meaning.
- **Arbiter = judgement assist**
  - Prioritization, suppression, rate limiting, escalation, and multi-channel emission decisions.

If you find yourself adding “priority rules” or “should we notify?” logic here, it belongs in `arbiter/`.

## Reference implementation (skeleton)

This folder intentionally starts as a **minimal reference**. A full MCP server/client implementation is planned.

Suggested next steps:
1) Add an MCP **server** exposing MCP4H tools/resources (validate, normalize, publish).
2) Add an MCP **client** adapter that consumes tool-call outputs and emits MCP4H packets.
3) Wire into `bridges/cue-router/` for multi-channel delivery.

See: `examples/messages/mcp/` for MCP-related message examples.
