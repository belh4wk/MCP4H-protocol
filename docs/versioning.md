# MCP4H Versioning Rules

- **Envelope `version` field:** Use semantic versions `0.1`, `0.1.1`, etc. (no `mcp4h/` prefix).  
  - For compatibility, implementations MAY accept legacy `mcp4h/0.1` during v0.1.x but SHOULD emit bare semver.
- **Content types:** `application/vnd.mcp4h.v0.1+json` or `+cbor`.
- **Additive changes (v0.1.x):** Only add optional fields or enum values. Do not change existing meanings.
- **Breaking changes (v0.2):** Allowed when necessary; MUST provide migration guidance.
