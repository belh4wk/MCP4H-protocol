
# MCP4H™: Harmonizer — Universal Invocation

Use this template for *any* situation (online post, email, DM, live speaking, etc.).
All fields are optional—leave them blank if not relevant.

## Text Template
```
Context:
- Platform (optional): [LinkedIn, Live, Forum, Email, Generic, ...]
- Audience (optional): [recruiters, peers, execs, public, ...]
- Goal (optional): [callout_post, hiring, thought_leadership, debate, update, DM, ...]
- Voice profile (optional): [default, <profile_id>]
- Mode (optional): [default, whisper, civility_lint, outline]
- Length (optional): [short, medium, long]
- Heat (optional): [0 cool, 1 warm, 2 spiky, 3 very spiky (still civil)]

Draft:
<PASTE YOUR TEXT HERE>
```

## JSON Template
If you prefer structured input, send JSON in this shape:

```json
{
  "context": {
    "platform": "Generic",
    "audience": "general",
    "goal": "thought_leadership",
    "voice_profile": "default",
    "mode": "default",
    "length": "medium",
    "heat": 1
  },
  "draft": "Prototypes are windows, not monuments..."
}
```

## Tips
- If you omit `platform` and `audience`, Harmonizer defaults to **Generic** and applies Voice Map + Guardrails automatically.
- Use `mode=whisper` for 5s/15s/30s speakable variants (live).
- Use `mode=civility_lint` to only get flags + neutral rewrites (no full rewrite).
- Set `emit_metadata=true` to receive a JSON header with risk/notes/CTA suggestions.
- Screenshots: redact names, emails, logos that imply endorsement.
