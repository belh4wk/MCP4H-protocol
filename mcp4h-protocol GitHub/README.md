# Multimodal Communication Protocol (MCP)

**Draft-00 — Experimental**

MCP is an open protocol for coordinating **text, audio, visual, and haptic** signals into one coherent conversation stream.  
It’s designed to reduce miscommunication across languages, cultures, and accessibility contexts.

## 📌 Repo Structure
- `spec/` → Living draft specifications (Markdown, RFC-style)
- `examples/` → Example JSON fixtures and test vectors
- `sdk-js/` → Reference JavaScript SDK (planned)

## 🚀 Roadmap
- **Phase 0:** Publish draft, build text+emoji+haptic demo  
- **Phase 1:** Pilots with translation & tone tagging  
- **Phase 2:** Game SDKs + SaaS relay  
- **Phase 3:** AR/wearable integration  
- **Phase 4:** Ecosystem scale, foundation governance

## 📖 License
Apache-2.0 — open protocol, royalty-free patent pledge for essential claims.


---

## 🐳 Run the Echo Server with Docker
```bash
# From repo root
docker compose up --build
# Server will be available at ws://localhost:8080
```
