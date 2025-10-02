# MCP4H — The 4‑Point Harness Protocol

MCP4H is a common language for communication, built to help people and machines share *situational awareness* across **text · visual · audio · haptic**.

## Quickstart

```bash
docker compose up --build

# Smoke test
curl -X POST http://localhost:8080/cue   -H "Content-Type: application/mcp4h+json"   -d @examples_cues/smoketest.json
```

Open `bridges/wearables-pwa/index.html` and click **Connect** to feel/see the pattern (mock).

## Contents

- **Spec:** schema + lexicon
- **Lingua:** deterministic audio/haptic/visual maps
- **Profiles:** assistive, safety, media
- **Microservices:** cue-gateway, voice-coach, osc-bridge, udp-proxy, simhub-adapter
- **Tools:** CLI sender/validator (via curl), Postman collection (TBD)
- **Docs:** spine, deployment, governance (TBD)
- **CI & Tests:** schema + MQTT loopback (TBD)

## Archival

Badges/links (fill in your DOIs/IDs when ready):

- Zenodo: _add DOI badge/link here_
- ORCID / HAL: _add links here_

---

## License

Apache-2.0 for code in this repo. Protocol and marks per `/docs/governance` (TBD).
