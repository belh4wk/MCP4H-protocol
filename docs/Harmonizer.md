
# MCP4H: Harmonizer

Harmonizer is a universal tone coach and copy generator. It preserves your authentic voice while applying guardrails that prevent clarity breakdowns, credibility risks, and unnecessary hostility.

---

## Core Principles
- Attack ideas, not people
- Preserve voice (cadence, idioms, edge)
- Trim only when sharpness undermines clarity or credibility
- Offer structured reasoning (steelman, claim, trade-offs, receipts, curious close)
- Platform-agnostic invocation with flexible profiles
- Optional machine-readable MCP4H packets for automation

---

## Visual Guardrails

Harmonizer outputs can include **emoji shorthand**, **heat bars**, and a **normalized risk score** to make feedback instantly visible.

### Levels
- ⛔ **Block** → ▮▮▮▮ (Critical stop – must fix before sending)
- ⚠️ **Warn** → ▮▮▮▯ (Warning – consider rewording)
- 💡 **Suggest** → ▮▮▯▯ (Suggestion – optional improvement)
- ✅ **Clear** → ▮▯▯▯ (No major risks)

### Risk Score
- Method: sum weighted risks, normalized to 0–100
- Display: `Risk score: {score}/100`
- Example: `⚠️ 2 warnings, 💡 1 suggestion — Risk score: 42/100`

This system turns Harmonizer into a **pre-flight check for communication**: sharp style, clear guardrails, no splinters.

---

## Whisper Mode
Whisper mode provides **5s/15s/30s speakable variants** with delivery cues like `[pause]`, `[soften]`, `[anchor with example]`.  
This makes Harmonizer useful not only for written posts but also for **live meetings, panels, and speeches**.

---

## License & Scope
- Not medical, legal, or financial advice
- Avoid sensitive PII (IDs, account numbers, full DOB, health records)
- Open spec; contributions welcome via PR with examples + doc blurbs
