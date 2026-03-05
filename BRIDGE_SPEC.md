# MCP4H Bridge Technical Specification v1.0

A Bridge is a translator. It must convert external signals into "Candidate Packets."

## Requirements
- **Normalization:** Raw values (e.g., 0-100% G-force or P0-P4 tickets) must be mapped to a 0.0 - 1.0 intensity scale.
- **Contextual Metadata:** Every packet must include a `category` (alert, telemetry, message) so the Arbiter knows how to treat it.

## Standard Packet Schema (JSON)
```json
{
  "bridge_id": "string",
  "payload": {
    "raw_text": "Brief summary for TTS or HUD",
    "metadata": {
      "intensity_suggestion": 0.8,
      "category": "emergency",
      "source_ref": "jira-1042"
    }
  }
}