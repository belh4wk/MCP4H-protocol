# MCP4H v0.1 — Minimum Viable Spec (One‑Pager)

**Purpose**  
A tiny, open envelope + metadata sidecar so any client can route a message into human‑friendly signals (text, audio, visual, haptic). Keep UX unchanged; add machine‑readable hints.

---

## 1) Message Envelope (transport‑agnostic JSON)
```json
{
  "version": "mcp4h/0.1",
  "id": "uuid",
  "timestamp": "ISO-8601",
  "origin": { "platform": "instagram|facebook|sms|email|…", "relation": "dm|mention|tag|comment" },
  "actor": { "role": "sender", "handle": "opaque_or_hashed" },
  "text": "visible text (optional if voice-only)",
  "metadata": { /* sidecar, see §2 */ }
}
```

## 2) Metadata Sidecar (minimal fields)
- `heat` **0–3** — overall sharpness (0 cool, 1 warm, 2 spiky, 3 very spiky).  
- `valence` **positive|neutral|negative|mixed** — quick polarity.  
- `tone` *(free text)* — e.g., “formal, sarcastic, playful”.  
- `civility_flags` **[ ]** — e.g., `["labeling","motive_attribution"]`.  
- `reasoning_moves` **[ ]** — any of: `steelman, claim, tradeoffs, receipts, curious_close`.  
- `constraints_detected` **[ ]** — e.g., `["cost","time","battery","complexity"]`.  
- `urgency` **low|normal|high** — optional.  
- `confidence` **0–1** — optional model confidence.  
- `visual_cues` — `{ "emoji": ["👍"], "meme_labels": ["Distracted Boyfriend"], "alt_text": "…" }` *(labels only; no images)*.  
- `platform_hints` — `{ "schedule": ["09:00–10:00","16:00–17:00"], "link_handling": "…" }` *(optional)*.

> **Producer**: Harmonizer (or any tool) fills this sidecar. **Consumers**: LED/haptics/tts/clients read it; humans only see normal text.

## 3) Handshake (capability + consent)
1. **HELLO** → client advertises channels:  
   ```json
   {"channels":{"led":true,"haptics":true,"audio":true},
    "caps":{"led_colors":["#FF3B30","#34C759","#FFFFFF","#FFCC00"],
            "haptics_max":0.85}}
   ```
2. **OK** → agree caps + user consent (e.g., “recipient alignment uses public info only”).  
3. **SEND** → envelope with sidecar.  
4. **ACK** → optional delivery/actuation receipt.

## 4) Profile Mappings (reference)

### 4a) Notif‑LED Profile v0.1 (smartglasses/earbuds)
- **RED `#FF3B30`** → `valence=negative` OR `heat≥2` OR `civility_flags.length>0` (pattern: *double‑pulse* 1.2s).  
- **GREEN `#34C759`** → `valence=positive` AND `heat≤1` (pattern: *steady* 1.0s).  
- **WHITE `#FFFFFF`** → `valence=neutral|mixed` AND `heat≤1` (pattern: *single* 0.8s).  
- **AMBER `#FFCC00`** → `urgency=high` regardless of valence (pattern: *triple quick* 1.0s).  
- Quiet hours / repeat suppression = client policy.

### 4b) Haptics (SimHub wind/fans) v0.1
Map `heat` → duty/intensity (cap by `haptics_max`):
- `0` → 0% (off)  
- `1` → 25% (soft, 300ms ramp)  
- `2` → 55% (medium, 300ms ramp)  
- `3` → 85% (firm, 500ms ramp; clamp to `haptics_max`)  
If `civility_flags` present, **reduce by 10%** (de‑escalation bias).

## 5) Example Envelope (IG mention → LED + Haptics)
```json
{
  "version": "mcp4h/0.1",
  "id": "9d3c…",
  "timestamp": "2025-09-22T10:12:55Z",
  "origin": { "platform": "instagram", "relation": "mention" },
  "actor": { "role": "sender", "handle": "hash_abc123" },
  "text": "This take is wild — you ignore battery reality.",
  "metadata": {
    "heat": 2,
    "valence": "negative",
    "tone": "blunt",
    "civility_flags": ["labeling"],
    "reasoning_moves": ["claim"],
    "constraints_detected": ["battery"],
    "urgency": "normal",
    "visual_cues": { "emoji": ["👀"], "meme_labels": [], "alt_text": "eyes emoji meaning 'looking closely'" }
  }
}
```
**Client action:** LED = **RED** double‑pulse; SimHub fan = **55%** (reduced to 45% due to flag).

## 6) Privacy & Safety (baked‑in)
- No medical/legal/financial advice; no PII ingestion (IDs, full DOB, account numbers).  
- Recipient alignment uses **public** material only; browsing requires explicit “browsing_ok=yes”.  
- Sidecar contains **hints**, not determinations; clients **may ignore** or override.

## 7) Tiny reference mapper (pseudo)
```python
def map_led(meta):
    if meta.get("urgency") == "high": return ("#FFCC00","triple_quick")
    if meta.get("valence") == "positive" and meta.get("heat",0) <= 1: return ("#34C759","steady")
    if meta.get("valence") in ["neutral","mixed"] and meta.get("heat",0) <= 1: return ("#FFFFFF","single")
    return ("#FF3B30","double_pulse")

def map_haptics(meta, cap=0.85):
    base = {0:0.0,1:0.25,2:0.55,3:0.85}.get(meta.get("heat",0),0.0)
    if meta.get("civility_flags"): base *= 0.9
    return min(base, cap)
```
