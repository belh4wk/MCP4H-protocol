# Harmonizer

The **Harmonizer** is an optional GPT configuration that works alongside MCP4H.

## Purpose
- Preserve civility and clarity in human-to-human communication.
- Optionally emit MCP4H™ packets (JSON) when triggered by specific words (e.g., "packet", "MCP4H™", "JSON for apps/devices").

## Why it matters
Harmonizer bridges natural language and the MCP4H™ protocol.  
It allows conversations to generate interoperable, schema-valid packets that can be consumed by software, hardware, or other humans.

## Packet Types Supported
- `ux_signal` (alerts/notifications)
- `semantic_event` (incidents or state changes)
- `telemetry_annotation` (metrics and state)
- `action_intent` (requests to act)
- `delivery_receipt` (confirmations)
- `capability_advertisement` (adapter declarations)

## Documentation
See [MCP4H_Harmonizer_Handbook_v1.5.md](../MCP4H_Harmonizer_Handbook_v1.5.md) for canonical templates and rules.
