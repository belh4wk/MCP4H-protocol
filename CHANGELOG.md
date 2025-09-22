# Changelog

All notable changes to **MCP4H – Multimodal Communication Protocol for Humanity** will be documented in this file.  
This project follows [Semantic Versioning](https://semver.org/).

---

# Version History

| Version   | Date       | Type        | Description                                   | DOI / Link                                                                 |
|-----------|------------|-------------|-----------------------------------------------|-----------------------------------------------------------------------------|
| v0.1.0-alpha | 2025-09-20 | Preprint / Draft | First public draft (Manifesto + Whitepaper). Repo structure + governance files. | [Zenodo DOI](https://doi.org/10.5281/zenodo.17164550) · [OSF Preprint (MetaArXiv, pending)](https://osf.io/preprints/metaarxiv) |
| Unreleased | –          | Planned     | Expanded spec, early MVP prototype (text/audio/visual integration), first haptic signal experiments. | –                                                                           |

---

## [v0.1.0-alpha] – 2025-09-20
### Added
- ✍️ First public draft of the **MCP4H Manifesto**  
- 📄 First public draft of the **MCP4H Whitepaper**  
- 📂 Initial repository structure:
  - `/examples` – placeholder for practical implementations
  - `/scripts` – utilities and automation stubs
  - `/sdk-js` – placeholder for JavaScript SDK
  - `/spec` – early technical specification
- 📜 Governance files:
  - `LICENSE`
  - `CODE_OF_CONDUCT.md`
  - `CONTRIBUTING.md`
- 🐳 Containerization scaffolding:
  - `Dockerfile`
  - `docker-compose.yml`

### Notes
- This is an **exploratory release** intended for community feedback and discussion.  
- Not yet suitable for production use.  
- Feedback and contributions are welcome via Issues and Pull Requests.

---

## [Unreleased]
- Expanded technical specification of the MCP4H protocol
- Early MVP prototype (text, audio, visual integration)
- First haptic signal experiments

- chore(structure): normalize `Docs/` → `docs/`, consolidate `spec/schemas` → `spec/schema`, and organize examples.

# Changelog

## 2025-09-22 — Harmonizer Handbook v1.6 Migration

### Added
- **MCP4H_Harmonizer_Handbook_v1.6.md**:  
  - New configuration section for GPT setup (conversation starters, knowledge file, capabilities).  
  - Expanded **Appendix F — MCP4H Packet Emission (v1.6)**.  
  - New **Appendix G — GPT Configuration Mapping** to align repo docs with GPT Configure UI.  

### Changed
- Updated references in `DEVELOPERS.md`, `docs/FAQ.md`, `docs/Harmonizer.md`, and `README.md` to point to v1.6.  
- CI continues validating `examples_harmonizer/` using schema v0.1.1.

### Removed
- **MCP4H_Harmonizer_Handbook_v1.5.md** deprecated and removed to avoid confusion.  

---
