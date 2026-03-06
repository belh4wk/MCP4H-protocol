# MCP4H – Developer Guide (README-DEV)

This guide helps you build, run, test, and troubleshoot the MCP4H stack locally.

## Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine (Linux)
- (Windows) WSL2 enabled
- Ports free: 8080 (API), 1883 (MQTT)

## Project Layout (quick)
- `docker-compose.yml` – services
- `services/*` – microservices (Python)
- `spec/` – schemas & lexicon
- `examples/messages/` – canonical maintained examples
- `examples_cues/` – legacy mirrored cue examples kept for compatibility

## Start the Stack

### Attached (see live logs)
> Close the terminal or hit CTRL+C to stop all containers.
```powershell
docker compose up
```

### Detached (background)
> Safe to close the terminal; containers keep running.
```powershell
docker compose up -d
```

### Check status
```powershell
docker ps --format "table {{.Names}}	{{.Status}}	{{.Ports}}"
```

## Stop the Stack
```powershell
docker compose down
```
*(This is the clean way. Closing the attached window will also stop them.)*

## Rebuild (clean)
If you changed code or requirements:
```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

## Smoke Test

### Windows (PowerShell)
```powershell
curl.exe -X POST http://localhost:8080/cue `
  -H "Content-Type: application/mcp4h+json" `
  --data-binary "@examples/messages/cues/smoketest.json"
```

### macOS/Linux
```bash
curl -X POST http://localhost:8080/cue   -H "Content-Type: application/mcp4h+json"   --data-binary @examples/messages/cues/smoketest.json
```

**Expected response (in the curl terminal):**
```json
{"accepted": true, "topic": "mcp4h/cues"}
```

**Docker logs (in the compose window) will show:**
```
POST /cue HTTP/1.1" 200 OK
[mcp4h] ✅ cue-gateway validated cue → topic=mcp4h/cues
```

## Logs

Follow all logs:
```powershell
docker compose logs -f
```

Follow one service:
```powershell
docker compose logs -f cue-gateway
```

## Health Checks

- API up?
```powershell
curl.exe http://localhost:8080/docs
```
(should return the FastAPI docs HTML)

- Broker reachable?
```powershell
docker compose logs -f mqtt
```
(you should see “New client connected” when services start)

## Troubleshooting

**Q: curl on Windows errors on `-H`**
- Use `curl.exe` instead of `curl` (PowerShell aliases `curl` to `Invoke-WebRequest`).

**Q: 422 Unprocessable Entity**
- Your JSON didn’t validate against `spec/cues/cue.schema.json`. Try `examples_cues/smoketest.json` first.

**Q: Port 8080/1883 already in use**
- Something else is running. Stop it or change ports in `docker-compose.yml`.

**Q: Containers exit immediately**
- Check per-service logs:
```powershell
docker compose logs <service-name>
```
- Common cause: missing Python dependency (fix by adding to the service’s `requirements.txt`, then rebuild).

## Developer Notes

- Each service prints a startup banner like:
```
[mcp4h] 🚀 cue-gateway ready on :8080
```
- Friendly logs describe actions in plain English across services.
- Prefer small, composable adapters over large monoliths.

## Next Steps

- Build a source adapter (e.g., SimHub/F1 UDP) to publish telemetry to MQTT.
- Map telemetry → MCP4H cues via the cue-gateway.
- Consume cues in a target adapter (voice-coach, wearables, dashboards).
