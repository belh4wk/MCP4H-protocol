# MCP4H Content Types (MIME)

Use these content types to distinguish encodings:

- JSON: `application/vnd.mcp4h.v0.1+json`
- CBOR: `application/vnd.mcp4h.v0.1+cbor`

When the transport cannot carry MIME, include `content_type` in the envelope.
