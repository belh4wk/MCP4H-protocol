# MCP4H FAQ

Frequently asked questions about the **Multimodal Communication Protocol for Humans (MCP4H)**.

---

### ❓ What is MCP4H?
MCP4H is an **open, neutral protocol** for normalizing, timestamping, and routing different human↔machine signals.  
It grew out of simracing, but the vision is bigger: unify telemetry, haptics, biometrics, voice, and controls so devices and apps can speak the same “language.”

---

### ❓ How is this different from SimHub, USB HID, or vendor SDKs?
- **SimHub** → Great middleware, but it passes game-specific values with no universal schema. MCP4H could sit *under* SimHub as a common backbone.  
- **USB HID** → Standardized, but very narrow (mostly input devices). MCP4H covers more modalities (telemetry, haptics, biometrics, etc.).  
- **Vendor SDKs** (Logitech, Fanatec, Corsair iCue, etc.) → Proprietary and siloed. MCP4H provides a bridge so they can coexist in the same system.

---

### ❓ Why JSON? Isn’t that too heavy for real-time use?
JSON was chosen because it’s:
- **Human-readable** → easy for developers to debug.  
- **Schema-validatable** → ensures messages conform to a contract.  
- **Translatable** → can be layered into lighter binary protocols (e.g., MCP4H-L1 line protocol for Arduinos).  

Think of JSON as the **spec layer**, not necessarily the on-the-wire encoding for every device.

---

### ❓ What does “confidence” and “provenance” mean in messages?
- **Confidence** → how reliable the signal is (0.0–1.0).  
  Example: an eye-tracking sample may have `confidence: 0.72`.  
- **Provenance** → chain of where the data came from.  
  Example: `[ "simhub:ac", "mcp4h-adapter:v1" ]`.  
This helps apps reason about trust, noise, or conflicting signals.

---

### ❓ Is this meant only for simracing?
No. Simracing is the **testbed** because it already mixes signals (telemetry, haptics, inputs). But MCP4H could apply to:
- **Accessibility** (assistive devices, alternative controls)  
- **Esports** (analytics, overlays, coaching)  
- **Mobility/Automotive** (driver biometrics + telemetry + assistance systems)  
- **Defense/Aviation** (AR/VR training, cockpit integration)

---

### ❓ How stable is the spec today?
- **v0.1.x** → draft schema, meant for experiments and feedback.  
- Breaking changes may happen.  
- Goal: converge toward **v1.0** once the schema and core fields stabilize.  

---

### ❓ How can I contribute?
- Try the [Arduino + SimHub example](../examples/arduino/windsim/)  
- Add more schema-valid JSONs under [`examples/messages`](../examples/messages)  
- Propose refinements to [`spec/schema/mcp4h-v0.1.json`](../spec/schema/mcp4h-v0.1.json)  
- Pick an item from [STARTER_ISSUES.md](../STARTER_ISSUES.md)  
- File issues with questions or suggestions  

---

### ❓ Where can I learn more?
- 📖 [Whitepaper](MCP4H_Whitepaper_v0.1.0.pdf)  
- 📜 [Manifesto](MCP4H_Manifesto_v0.1.0.pdf)  
- 📊 [Flow diagram](diagrams/mcp4h_flow.svg)  
- 🐙 [GitHub Wiki → Getting Started](https://github.com/YOUR_USER/MCP4H-protocol/wiki/Getting-Started)

