# MCP4H Content Types (MIME)

- JSON: `application/vnd.mcp4h.v0.1+json`
- CBOR: `application/vnd.mcp4h.v0.1+cbor`

If transport can't carry MIME (e.g., raw UDP), include `content_type` in the envelope.
