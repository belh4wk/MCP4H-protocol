# MCP4H — The 4-Point Harness Protocol

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17727584.svg)](https://doi.org/10.5281/zenodo.17727584)

## What this repo is (and is not)

This repository contains the **MCP4H™ protocol**:

- Schemas, examples, docs, and tooling for the **Multimodal Communications Protocol For Humanity**.
- A neutral backbone for machine-to-machine and machine-to-human cue exchange.
- Reference material for anyone building adapters, bridges, or UIs on top of MCP4H.

This repo **does not** contain:

- SimHub plugins
- Game-specific haptics code
- Commercial implementations

Those live in **separate implementation repos** (for example MCP4SH™ for SimHub).

MCP4H™ (Multimodal Communications Protocol for Humanity) is a **common language for communication**, built to help people and machines share situational awareness.

Works across **text • visual • audio • haptic.**  
Small cue grammar — big reach.

---

## Prior-Art Disclosure

The architectural concepts and design principles underlying MCP4H are intentionally published as prior art.
A public prior-art disclosure describing the system architecture, telemetry normalization approach, and multimodal design principles is available via Zenodo:

**DOI:** https://doi.org/10.5281/zenodo.18223144

This disclosure is intended to prevent exclusive patent claims on the core MCP4H architecture while enabling open and interoperable implementations.

## Quickstart

### 1. Build and start the services
```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

### 2. Run the smoke test
Run this from a separate PowerShell terminal in the repo root:

```powershell
curl.exe -X POST http://localhost:8080/cue `
  -H "Content-Type: application/mcp4h+json" `
  --data-binary "@examples_cues/smoketest.json"
```

✅ **Expected output** (in the curl terminal):
```json
{"accepted": true, "topic": "mcp4h/cues"}
```

📋 **Docker logs** will show:
```
POST /cue HTTP/1.1" 200 OK
```

> Note: The response body only appears in the terminal where you ran `curl.exe`. Docker logs confirm requests were received and processed, but do not echo response JSON.

---

## Contents

- **Spec**: schema + lexicon + media type  
- **Lingua**: deterministic audio/haptic/visual maps  
- **Profiles**: assistive, safety, media  
- **Microservices**: cue-gateway, voice-coach (+TTS script), osc-bridge, udp-proxy, simhub-adapter, fanatec-adapter  
- **Tools**: CLI sender/validator, Postman collection  
- **Docs**: Spine, Roadmap, RFCs, Deployment, Compliance, Governance, Patent covenant  
- **CI + Tests**: schema + MQTT loopback  
- **Diagram**: `/diagrams/stack.svg`  
- **Assumptions**: design rationale and conceptual foundations (`/docs/ASSUMPTIONS.md`)

---

## Design Rationale

📘 **Assumptions & Rationale**  
See [`/docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md) for the conceptual and ethical backbone of MCP4H —  
why each design decision exists, the principles guiding signal translation, and how future versions validate or deprecate those assumptions.

Each assumption is treated as a **commit of understanding** — dated, versioned, and never deleted.  
Together, they form the *Principles of Human-Readable Signal Translation* — the living documentation of the protocol’s evolution.

Example categories of assumptions include:

- **Conceptual:** how humans interpret multimodal cues under cognitive load.  
- **Design:** why every signal resolves to a text semantic layer before voice or haptics.  
- **Ethical:** ensuring MCP4H augments awareness rather than automating judgment.  
- **Validation:** measurable tests for clarity, latency, and adoption.

---

## Architectural Flow

```
[Game Telemetry] → [MCP4H Core Translator] → [Output Adapter]
```

For the trail-braking alpha demo:  
- **Input:** Game telemetry (speed, brake pressure, slip ratio)  
- **Core:** MCP4H translator applies rule logic → "LIFT" / "PUSH" cue  
- **Output:** SimHub dashboard text label  

Future adapters (voice, haptic, AI coach) will follow this same interface pattern.  
This minimal chain is the first real-world test of MCP4H’s founding claim:  
> “Clarity is a deliverable.”

---

## Tagline

> “MCP4H is a common language for communication, built to help people and machines share situational awareness.”

---

## References

- 📄 [Zenodo DOI](https://doi.org/10.5281/zenodo.17727584)  
- 📄 [HAL Preprint](https://hal.science/)  
- 📄 [OSF Preprint](https://osf.io/)  
- 📄 [ORCID Profile](https://orcid.org/)  

---

© 2025 Dirk Van Echelpoel — MCP4H™ (Multimodal Communications Protocol for Humanity)

## Related projects

- **MCP4SH™** – SimHub implementation of MCP4H for sim racing haptics  
  *(separate repository, distributed under a more restrictive license)*

- **MCP4H: Harmonizer** – conversational stack built on MCP4H principles (guardrails, voice profiles, and cue mappings).
