# SimHub Plugin Skeleton — MCP4H Traction LEDs

This is a minimal C# plugin skeleton to **read `bridges/simhub/out/SimHubVars.json`**
and expose dashboard properties:

- `MCP4H_Traction_LF_Color`, `...RF_Color`, `...LR_Color`, `...RR_Color`
- `MCP4H_Traction_LF_Blink`, `...RF_Blink`, `...LR_Blink`, `...RR_Blink`

## Build
1. Install Visual Studio (Windows) with **.NET Framework 4.7.2** dev tools.
2. Open `src/Mcp4hSimHubPlugin.csproj`.
3. Add references to SimHub SDK DLLs (from your SimHub install folder):
   - `SimHub.Plugins.dll`
   - `SimHub.Plugins.DataPlugins.dll` (names may differ slightly per version)
4. Build in **Release**; copy the resulting `.dll` to `%ProgramFiles(x86)%\SimHub\Plugins\`.
5. Start SimHub; enable the plugin in **Settings → Plugins**.

## Notes
- The skeleton uses a **FileSystemWatcher** to reload `SimHubVars.json` when the Python bridge updates it.
- Property publishing is shown as `AddProperty(...)` — adjust to your SDK version if method names differ.
- If you prefer to consume UDP envelopes, adapt the code to parse UDP JSON instead.
