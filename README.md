# MCP4H

**Multimodal Communications Protocol for Humans (MCP4H)**  
*A translation layer for signals — not another app, not another silo.*

MCP4H defines a **grammar of attention**: a common way to express cues so they land clearly, at the right time, through the right channel.

- **Type**: Coach, Risk, Plan, State, Confirm  
- **Priority**: now, soon, later  
- **Channel**: light, haptic, text, audio, or all  
- **Rules**: expiry + acknowledgement

Think of MCP4H as the **referee, not another player**. It doesn’t add more noise — it decides *what matters, when to deliver it, and how to make sure it lands*.

---

## Proving grounds

- **Conversations**: via a custom GPT (*MCP4H: Harmonizer*). Keeps tone aligned, distills tangents into cues, nudges constructive habits.  
- **(Sim)Racing**: tested as an extra race engineer. Turns raw telemetry into cues like:  
  - `tyre hot` → more grip, but risk of overheating  
  - `tyre cold` → less grip, unstable  
  - `brake fade risk` → adjust before failure  

If MCP4H works here — high-stakes, high-speed, or universally familiar — it can work anywhere.

---

## Why not just use existing tools?

- **Otter / Rewind**: capture everything → you dig through haystack later.  
- **CrewChief / AI racing coaches**: analysis for experts.  
- **MCP4H**: translation into *human-friendly cues* in real time.  
  Clearer, not more.

---

## Repo structure

- `spec/schema/` → baseline schemas  
- `examples/`, `examples_v0.1.1/`, `examples_harmonizer/` → worked examples  
- `docs/` → FAQ, Vision, Harmonizer guide, Handbook v1.7  
- `bridges/` → adapters (SimHub PoC coming)  
- `tests/` → validation scripts  
- `.github/workflows/` → CI (validates examples against schemas)

---

## Status

- Schemas + examples live  
- Harmonizer Handbook at **v1.7** (current)  
- SimHub PoC bridge next milestone  
- First tagged release pending

---

📂 [Zenodo DOI](#)  
📂 [HAL preprint](#)  
📂 [OSF preprint](#)  
🤖 [MCP4H: Harmonizer](#)
