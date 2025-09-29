# Project Status – MCP4H™ Protocol

**Last updated:** 2025-09-21

## Current State
- ✅ Repository structure in place with governance files (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, DISCLAIMER, ROADMAP, CHANGELOG).
- ✅ Documentation drafts added (Manifesto v0.1.0, Whitepaper v0.1.0, overview).
- ✅ Reference implementations started:
  - Python reference (`/Code/src/mcp4h_reference_impl.py`)
  - TypeScript/JS SDK (`/sdk-js/`)
- ✅ Example demos included (`/examples/echo-server.ts`, `/examples/message-demo.json`).
- ✅ Draft specification added (`/spec/draft-mcp-00.md`).
- ✅ DOI minted (Zenodo) and linked across platforms (ORCID, HAL, OSF, GitHub).

## In Progress
- Refining terminology (e.g., “4-point harness” language alignment).
- Preparing initial Arduino + SimHub MVP for `/examples/arduino/`.
- Clarifying schema in draft spec.

## Next Steps (Short-Term)
1. Add a machine-readable schema definition (JSON Schema) to `/spec/`.
2. Expand `/examples/` with Arduino windsim + SimHub integration.
3. Create a minimal test harness for schema validation (Python/Node).
4. Add `SECURITY.md` and GitHub issue/PR templates for community contributions.
5. Update README with a **Getting Started** guide + protocol diagram.

## Medium-Term Goals
- MVP demonstration (Arduino windsim + LEDs) with SimHub.
- Gather early feedback from DIY/simracing community.
- Publish v0.2.0 of spec once MVP tested.
- Draft outreach plan for coalition (SimHub dev, peripheral OEM, simracing community, accessibility researcher).

## Long-Term Vision
- Position MCP4H™ as a neutral interoperability protocol for multimodal human↔machine signals.
- Expand beyond simracing into accessibility and mobility domains.
- Explore consortium/standardization pathways (SAE, IEEE, Khronos).

**2025-09-21:** Repo housekeeping completed (docs path normalized, schema path consolidated, examples reorganized, duplicate validator removed).
