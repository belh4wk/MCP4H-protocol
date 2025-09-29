# SimHub Dash Studio — MCP4H™ Traction LEDs (4-block) setup

This shows how to drive 4 LED blocks (LF, RF, LR, RR) from wheel slip using MCP4H.

## 1) Run the bridge
Demo (fake slip):
```bash
python bridges/simhub/mcp4h_to_simhub.py --mode demo
```
Switch to UDP later:
```bash
python bridges/simhub/mcp4h_to_simhub.py --mode udp --udp-port 9999
```

## 2) In SimHub, add the data source
- Add a **Custom UDP/JSON** input on port `9999` (or your chosen port).
- Map JSON fields to custom properties:
  - `MCP4H_Traction_LF_Color`, `...RF_Color`, `...LR_Color`, `...RR_Color`
  - `MCP4H_Traction_LF_Blink`, `...RF_Blink`, `...LR_Blink`, `...RR_Blink`

If your build can’t map JSON → properties, build the **SimHub plugin skeleton** in `bridges/simhub-plugin/`.
It watches `bridges/simhub/out/SimHubVars.json` and publishes the same properties natively.

## 3) Bind in Dash Studio
- Create four rectangles/images.
- Fill color ← bind to `MCP4H_Traction_<wheel>_Color`.
- Blink/visibility ← bind to `MCP4H_Traction_<wheel>_Blink`.

## 4) Tune thresholds
Edit `bridges/simhub/mcp4h_to_simhub.py`:
```python
lo, hi = 0.05, 0.12  # slip thresholds
alpha = 0.3          # smoothing
```
Hysteresis is built-in to avoid flicker.

## 5) Optional: share MCP4H™ envelopes
With `--mode udp` the bridge emits a full envelope including:
```json
"extensions": { "traction_leds": { "values": {...}, "colors": {...}, "blink": {...} } }
```
Other apps/devices can mirror the same cues.
