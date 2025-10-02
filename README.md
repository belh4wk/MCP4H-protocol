# MCP4H — The 4‑Point Harness Protocol

**MCP4H is a common language for communication, built to help people and machines share situational awareness.**

Works across text • visual • audio • haptic. Small cue grammar, big reach.

## Quickstart
```bash
docker compose up --build
# Smoke test
curl -X POST http://localhost:8080/cue   -H "Content-Type: application/mcp4h+json"   -d @examples_cues/trail_brake_deep.json
```
Open `bridges/wearables-pwa/index.html` and click **Connect** to feel patterns.

## Contents
- **Spec**: schema + lexicon + media type
- **Lingua**: deterministic audio/haptic/visual maps
- **Profiles**: assistive, safety, media
- **Microservices**: cue-gateway, voice-coach (+TTS script), osc-bridge, udp-proxy, simhub-adapter, fanatec-adapter
- **Tools**: CLI sender/validator, Postman collection
- **Docs**: Spine, Roadmap, RFCs, Deployment, Compliance, Governance, Patent covenant
- **CI + Tests**: schema + MQTT loopback
- **Diagram**: ./diagrams/stack.svg

## Tagline
“MCP4H is a common language for communication, built to help people and machines share situational awareness.”
