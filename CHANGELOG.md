# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v0.1.1] – 2025-10-05
### Added
- **Dockerized microservice stack** including `cue-gateway`, `voice-coach`, `osc-bridge`, `udp-proxy`, and `simhub-adapter`.
- **Unified Docker Compose orchestration** for quick local setup and isolated testing.
- **Schema validation CI** extended to include message loopback and MQTT transport tests.
- **Expanded example set** under `/examples_cues` and `/examples_harmonizer`.
- **Documentation updates** across `/docs/` with references to CI, governance, and developer contribution rules.
- **Initial rationale framework** introduced; `ASSUMPTIONS.md` planned for next release.

### Changed
- Updated `README.md` for Quickstart commands and smoke test example.
- Revised folder structure to clarify `/spec/`, `/examples/`, `/bridges/`, and `/docs/` boundaries.
- Refined naming and metadata alignment across Zenodo/HAL/OSF/ORCID links.

### Fixed
- Minor schema consistency issues in `mcp4h-v0.1.json`.
- CI paths now correctly skip non-envelope JSONs.

---

## [v0.1] – 2025-09-01
### Added
- **Initial MCP4H schema** and lexicon definitions.
- **Baseline examples** validating schema conformance.
- **Continuous Integration pipeline** for JSON validation.
- **Core documentation** including README, Overview, and CONTRIBUTING guidelines.
- **Placeholder Zenodo release** linked for DOI and archival.

---

## [Unreleased] – Upcoming
### Planned
- **v0.1.2 – Trail-Braking Alpha (SimHub Chain)**
  - First end-to-end demonstration of MCP4H signal translation:  
    *Game telemetry → MCP4H core → SimHub text cue (“LIFT” / “PUSH”)*  
  - Adds `ASSUMPTIONS.md` (design rationale), live output validation logs, and recorded demo artifact.
  - Prepares repo for Zenodo/ORCID update with new release metadata.

---
