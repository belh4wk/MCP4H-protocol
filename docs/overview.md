# Overview

MCP4H is a **multimodal communications protocol**.  
It defines a grammar for expressing cues consistently:

- **Type** (Coach, Risk, Plan, State, Confirm)  
- **Priority** (now, soon, later)  
- **Channel** (light, haptic, text, audio, all)  
- **Rules** (expiry + acknowledgement)

CI now validates lint/type checks in addition to schema/tests.

---

## Example outputs

- `tyre hot` → more grip, but risk of overheating  
- `tyre cold` → less grip, unstable  
- `brake fade risk` → adjust before failure  

---

## Architecture (from Whitepaper)

- **Envelope**: each cue conforms to schema in `spec/`.  
- **Transport**: protocol-agnostic; publish/subscribe ready.  
- **Adapters (bridges/)**: translate MCP4H envelopes into domain-specific outputs (SimHub, LEDs, chatbots).  
- **Validation**: CI ensures conformance to schema.

---

## Metaphor

MCP4H is the **referee, not another player**.  
It reduces clutter, delivers clarity, and ensures important signals aren’t missed.
