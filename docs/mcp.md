# MCP interoperability

This repo integrates with **Model Context Protocol (MCP)** by providing a bridge that maps MCP tool events/results into MCP4H packets.

- Implementation: `bridges/mcp/`
- Examples: `examples/messages/mcp/`

Design rule: the bridge performs structural mapping only; prioritization belongs in `arbiter/`.
