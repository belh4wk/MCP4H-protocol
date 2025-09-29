# MCP4H — Multimodal Communication Protocol for Humanity

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17164550.svg)](https://doi.org/10.5281/zenodo.17164550)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17225488.svg)](https://doi.org/10.5281/zenodo.17225488)

> MCP4H is a transport-agnostic protocol spec and set of examples for human-first, low-latency multimodal comms.

## Quick Start

```bash
python -m pip install -r requirements.txt
python tests/validate_roundtrip.py
# Optional (needs cbor2)
python tests/generate_cbor_vectors.py
# UDP demo
python tools/udp_reader_led_demo.py   # terminal A
python tools/udp_emitter.py           # terminal B
```

## Docs

- **Profiles:** `docs/profiles.md`
- **Transports:** `docs/transports.md`
- **Content types:** `docs/content-types.md`
- **Versioning:** `docs/versioning.md`
- **Style guide:** `docs/style_guide.md`

## Schemas

- Envelope schema: `spec/schema/mcp4h-v0.1.1.json`
- Examples: `examples_v0.1.1/` (tyre slip cues with UDP packets)

## CI

- `.github/workflows/ci.yml` validates JSON vectors and runs optional CBOR, pytest, lint/type checks.

## Versioning

Emit `version: "0.1.1"` (bare semver). During v0.1.x, receivers MAY accept legacy `mcp4h/0.1` for compatibility.

---

## Citation & DOI

- **Concept DOI (always latest):** https://doi.org/10.5281/zenodo.17164550  
- **Version DOI (this release):** https://doi.org/10.5281/zenodo.17225488

**APA**  
Van Echelpoel, D. (2025). *MCP4H v0.1.1 — Additive update (envelope + profiles + examples + CI)*. Zenodo. https://doi.org/10.5281/zenodo.17225488

**BibTeX**
```bibtex
@software{van_echelpoel_mcp4h_v0_1_1_2025,
  author    = {Dirk Van Echelpoel},
  title     = {MCP4H v0.1.1 — Additive update (envelope + profiles + examples + CI)},
  year      = {2025},
  publisher = {Zenodo},
  version   = {v0.1.1},
  doi       = {10.5281/zenodo.17225488},
  url       = {https://doi.org/10.5281/zenodo.17225488}
}
```

## License

MIT © Dirk Van Echelpoel
