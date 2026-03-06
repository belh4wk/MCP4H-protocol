# Canonical MCP4H Message Examples

This folder is the source of truth for maintained JSON examples.

## Structure

- Top-level `*.json` files are MCP4H envelope examples validated in CI.
- `cues/` contains cue-router and cue-gateway demo payloads kept for backward compatibility with older tooling.

## Sync rules

Do not hand-edit mirrored legacy files in:

- `examples/*.json`
- `examples_cues/*.json`

Edit the canonical file here, then run:

```bash
python tools/sync_examples.py
```
