# Harmonizer Reference Bridge (MCP4H ↔ GPT)

Minimal reference adapter showing how to map MCP4H packets to GPT-style prompts and back.
Designed to live at `bridges/harmonizer/`.

Related docs in this repo:
- `docs/Harmonizer.md` (design/wiki)
- `examples_harmonizer/` (validated examples)

## Files
- `adapter.py` — CLI entrypoint.
- `mapper.py` — MCP4H ↔ prompt mapping.
- `bridge_config.yaml` — tiny config (prefix/suffix, roles).
- `examples/request_packet.json` — demo input.
- `tests/test_mapper.py` — smoke tests (no external deps).

## Usage
```bash
python bridges/harmonizer/adapter.py   --in bridges/harmonizer/examples/request_packet.json   --out bridges/harmonizer/examples/response_packet.json
```

Swap `simulate_gpt_completion()` with a real client when ready.
