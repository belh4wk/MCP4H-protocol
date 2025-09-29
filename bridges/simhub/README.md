# MCP4H™ ↔ SimHub Bridge (Traction LEDs)

This bridge turns per-wheel slip into MCP4H™ `extensions.traction_leds` and also exports simple variables:

- `MCP4H_Traction_LF_Color`, `...RF_Color`, `...LR_Color`, `...RR_Color`
- `MCP4H_Traction_LF_Blink`, `...RF_Blink`, `...LR_Blink`, `...RR_Blink`

## Usage
Demo (fake slip):
```bash
python mcp4h_to_simhub.py --mode demo
```
UDP output for SimHub custom receiver:
```bash
python mcp4h_to_simhub.py --mode udp --udp-port 9999
```
