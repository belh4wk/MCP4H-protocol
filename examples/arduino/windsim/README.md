# Arduino WindSim Example (MCP4H-L1)

This example shows a minimal **SimHub → MCP4H-L1 → Arduino** pipeline:
SimHub emits a simple line protocol; the Arduino parses it and drives a fan (windsim)
and an LED based on vehicle speed and gear.

> ⚠️ **Safety**: Power the fan/motor from a suitable external supply through a motor shield or driver.
> The Arduino pin only provides a PWM signal, not power.

## Hardware
- Arduino **Uno**
- Motor shield/driver for fan (e.g., L298N or Arduino Motor Shield)
- DC fan for wind simulation
- Optional: LED + resistor for gear indicator

**Pins (default)**
- Fan PWM: D9
- LED: D6

Adjust pins in the sketch if needed.

## SimHub Setup
1. In SimHub: **Settings → Arduino → Custom serial devices**
2. Select your Arduino COM port
3. Set the **baud** to `115200`
4. Use this one-line **send format**:
```
MCP4H v=1 ts=$now() spd_mps=[DataCorePlugin.GameData.NewData.SpeedMps] gear=[DataCorePlugin.GameData.NewData.Gear]
```
(You can substitute game-specific variables if needed.)

## Upload
1. Open `mcp4h_windsim.ino` in the Arduino IDE (or VS Code + PlatformIO).
2. Select the right board/port.
3. Upload.

## Run
- Launch a supported sim with SimHub running.
- Start driving: you should feel the fan scale with speed; LED intensity reflects gear.

## How this is MCP4H-aligned
- Uses a **neutral message** with timestamp (`ts`) and **units** (`spd_mps`).
- Parses into a structured state on-device.
- Ready to evolve into full JSON if needed, while staying friendly to 8-bit MCUs.

## Files
- `mcp4h_windsim.ino` — Arduino sketch
- `simhub_format.txt` — Copy/paste line protocol for SimHub
