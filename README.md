# MCP4H — The 4-Point Harness Protocol

MCP4H™ (*Multimodal Communications Protocol For Humanity*) is a **common language for communication** built to help people and machines share situational awareness.

It is the packet grammar and translation backbone.
It is **not** the commercial implementation, game-specific haptics layer, or product-specific UI.

Works across **text • visual • audio • haptic**.
Small cue grammar — big reach.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17164550.svg)](https://doi.org/10.5281/zenodo.17164550)

---

## Citation / DOI

- **Concept DOI (all versions):** `10.5281/zenodo.17164550`
- **Latest tagged release DOI:** see `CITATIONS.md` for the current release-specific identifier
- **Citation files in this repo:** `CITATION.cff`, `CITATIONS.md`, `CITATIONS.bib`, `zenodo.json`

## Prior-art disclosure

MCP4H’s core architecture is intentionally published as prior art to keep the protocol backbone open and to make the public record easy to cite and verify.

Use the concept DOI above as the stable reference point. Use `CITATIONS.md` as the source of truth for the latest tagged release DOI.

---

## What lives here

- schemas, bindings, and protocol docs
- canonical examples and validation tooling
- reference bridges and demo services
- developer guidance for building adapters cleanly

## What does not live here

- SimHub plugin product code
- proprietary arbiter logic
- commercial dashboards or shipping apps

Those belong in implementation repos such as MCP4SH™.

---

## Repo map (where to start)

### 1) Protocol
The protocol is the language itself.

Start here:

- `spec/`
- `schemas/`
- `examples/messages/`
- `tests/`
- `sdk-js/`
- `protocol/README.md`

### 2) Bridges
Bridges are connectors. They move packets between systems without inventing new meaning.

Start here:

- `bridges/README.md`
- `bridges/cue-router/`
- `bridges/simhub/`
- `bridges/notify-led/`

### 3) Arbiter
The arbiter is the judgment-assist layer.

It decides priority, suppression, escalation, and interruption budgets.
That should stay separable from the neutral protocol.

Start here:

- `arbiter/README.md`

---

## Quickstart

### 1. Build and start the services

```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

### 2. Run the smoke test

From a second terminal in the repo root:

```powershell
curl.exe -X POST http://localhost:8080/cue `
  -H "Content-Type: application/mcp4h+json" `
  --data-binary "@examples/messages/cues/smoketest.json"
```

Expected output:

```json
{"accepted": true, "topic": "mcp4h/cues"}
```

Legacy path compatibility remains in place, so `examples_cues/smoketest.json` still works. The canonical source now lives under `examples/messages/cues/`.

---

## Cue-router bridge

The repo now includes a cue-router bridge for Slack / Teams / MQTT fanout with:

- health and readiness endpoints
- Prometheus metrics
- policy hot-reload
- replay CLI
- OpenTelemetry hooks

Useful local URLs:

- `http://localhost:8090/healthz`
- `http://localhost:8090/metrics`

Policy file:

- `bridges/cue-router/policy.yaml`

Replay example:

```bash
python tools/replay_cues.py bridges/cue-router/examples/replay.ndjson --url http://localhost:8090/route
```

---

## Design rule: Bridge / Protocol / Arbiter

Keep these three separate.

- **Bridge**: connector / transport glue
- **Protocol**: packet grammar and validation rules
- **Arbiter**: judgment-assist and prioritization logic

That distinction keeps MCP4H portable, auditable, and reusable across games, wearables, messaging, assistive tech, and future adapters.

---

## Canonical examples and sync guardrails

`examples/messages/` is the maintained source of truth.

Legacy paths are still preserved so older scripts and links do not break:

- `examples/*.json`
- `examples_cues/*.json`

To resync legacy mirrors after editing canonical sources:

```bash
python tools/sync_examples.py
```

To verify mirrors in CI or before commit:

```bash
python tools/sync_examples.py --check
```

---

## Related projects

- **MCP4SH™** – SimHub implementation of MCP4H for sim racing haptics
- **MCP4H: Harmonizer** – conversational stack built on MCP4H principles
