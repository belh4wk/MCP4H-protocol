# README Additions (drop into your README.md)

## Quick Start
```bash
# Install tools
python -m pip install -r requirements.txt

# Validate examples
python tests/validate_roundtrip.py

# Generate CBOR vectors (optional)
python tests/generate_cbor_vectors.py

# UDP demo (LED cue)
python tools/udp_reader_led_demo.py  # terminal A
python tools/udp_emitter.py          # terminal B
```

## Wire Profiles & Content Types
See `docs/profiles.md`, `docs/transports.md`, and `docs/content-types.md`.

## Versioning
See `docs/versioning.md`. During v0.1.x, emit `version: "0.1.1"` (bare semver) and accept legacy `mcp4h/0.1`.
