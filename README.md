# MCP4H — The 4-Point Harness Protocol

MCP4H is a common language for communication, built to help people and machines share situational awareness.

Works across text • visual • audio • haptic. Small cue grammar, big reach.

---

## Quickstart

### 1. Build and start the services
```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

### 2. Run the smoke test
Run this from a separate PowerShell terminal in the repo root:

```powershell
curl.exe -X POST http://localhost:8080/cue `
  -H "Content-Type: application/mcp4h+json" `
  --data-binary "@examples_cues/smoketest.json"
```

✅ **Expected output** (in the curl terminal):
```json
{"accepted": true, "topic": "mcp4h/cues"}
```

📋 **Docker logs** will show:
```
POST /cue HTTP/1.1" 200 OK
```

> Note: The response body only appears in the terminal where you ran `curl.exe`. Docker logs confirm requests were received and processed, but do not echo response JSON.

---

## Contents

- **Spec**: schema + lexicon + media type  
- **Lingua**: deterministic audio/haptic/visual maps  
- **Profiles**: assistive, safety, media  
- **Microservices**: cue-gateway, voice-coach (+TTS script), osc-bridge, udp-proxy, simhub-adapter, fanatec-adapter  
- **Tools**: CLI sender/validator, Postman collection  
- **Docs**: Spine, Roadmap, RFCs, Deployment, Compliance, Governance, Patent covenant  
- **CI + Tests**: schema + MQTT loopback  
- **Diagram**: /diagrams/stack.svg  

---

## Tagline

“MCP4H is a common language for communication, built to help people and machines share situational awareness.”

---

## References

- 📄 [Zenodo DOI](https://doi.org/10.5281/zenodo.YOUR_DOI)  
- 📄 [HAL Preprint](https://hal.science/)  
- 📄 [OSF Preprint](https://osf.io/)  
- 📄 [ORCID Profile](https://orcid.org/)  

---
