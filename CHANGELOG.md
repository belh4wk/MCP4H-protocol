# Changelog

All notable changes will be documented in this file.

## [0.1.1] - 2025-09-29

### Added
- Envelope optional fields: `profile`, `msg_type`, `seq`, `ts_monotonic_us`, `content_type`
- New schema: `spec/schema/mcp4h-v0.1.1.json`
- Normative example: `examples_v0.1.1/tyre_slip/`
- Tools: `tools/udp_emitter.py`, `tools/udp_reader_led_demo.py`
- Tests: JSON golden vectors, CBOR generator, roundtrip validator
- Docs: profiles, transports, content-types, versioning, style guide, security stub
- `mqtt/topic_conventions.md` with topic/QoS guidance
- Citation metadata: `CITATION.cff`, `CITATIONS.bib`, `zenodo.json`
- README.md now includes DOI badges, APA + BibTeX citation

### Changed
- CI merged into single `.github/workflows/ci.yml` (schema checks, pytest, lint, type checks)
- `requirements.txt` expanded to include `cbor2`, `pytest`, `flake8`, `mypy`

### Removed
- Old duplicate workflow `.github/workflows/validate.yml`
- Extra licenses (`LICENSE-CC-BY-NC-4.0.txt`, `LICENSE-GPL-3.0-or-later.txt`) — MIT is now sole license

---

## [0.1.0-alpha] - Initial
- Initial draft of MCP4H spec, schema, and docs
