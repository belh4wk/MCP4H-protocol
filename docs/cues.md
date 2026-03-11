# Cues and Projection

MCP4H cues are designed to be **portable**: the same high-level intent should render consistently across different devices and modalities.

## Modality vs content

Think in two layers:

- **Modality (how it is perceived):** `visual`, `audio`, `haptic`
- **Content (what it contains):** text, icon/image/video, LED signal (color/blink), tone/beep, speech (TTS), vibration pattern, etc.

Examples:

- A phone notification with words is **visual** modality with **text** content.
- An LED flash is **visual** modality with **signal** content.
- TTS is **audio** modality with **speech** content.
- A rumble pattern is **haptic** modality with **pattern** content.

## Projection (what you wanted)

Instead of duplicating the same message into multiple separate cues, MCP4H supports **projection**:

1. You describe the intent once (and optionally provide channel-specific variants).
2. Renderers choose what they can output based on their capabilities and context.

### Backward compatible cue shapes

The cue schema (`spec/cues/cue.schema.json`) accepts multiple shapes via `oneOf`:

- **Legacy** cue formats (kept for compatibility).
- **Projected payload** cue (v0.1.1): keeps the legacy shell (`id/ts/channel/intent`) but makes `payload` structured.

## Projected payload (v0.1.1)

When using the projected payload branch, `payload` is structured (no junk drawer):

- `payload.text`: `{ short, long, lang, style }`
- `payload.visual`: `{ led, icon, image, ttl_ms }`
- `payload.audio`: `{ mode, beep, tts, sample, rate_limit_ms }`
- `payload.haptic`: `{ pattern, intensity, duration_ms, channel }`
- optional: `payload.data`, `payload.provenance`

Renderers can:

- pick `payload.text.short` for overlays/notifications,
- map `payload.visual.led` to LED devices,
- use `payload.audio` for beep/TTS/sample,
- use `payload.haptic` for vibration/tensioner patterns.

### Minimal example

```json
{
  "id": "cue-003",
  "ts": "2026-03-07T12:00:01Z",
  "channel": "multi",
  "intent": "inform",
  "payload": {
    "text": { "short": "Tool completed", "long": "filesystem.read returned text.", "style": "neutral" },
    "visual": { "led": { "color": "#00FF66", "blink_hz": 2, "ttl_ms": 300 } },
    "audio": { "mode": "beep", "beep": "single" },
    "haptic": { "pattern": "double_tap", "intensity": 0.4, "duration_ms": 180 }
  }
}
```

## Where to look

- Cue schema: `spec/cues/cue.schema.json`
- MCP example using projected payload: `examples/messages/mcp/mcp_event_mapped_to_mcp4h_packet.json`
- Bridges/renderers: `bridges/` (e.g., `bridges/mcp/`, cue-router, SimHub bridge)


## Canonical cue path

For v0.1.x, the canonical cue representation is the **Projected payload cue (v0.1.1)**. Legacy cue shapes remain accepted only for backward compatibility and are deprecated.
