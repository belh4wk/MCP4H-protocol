**Dev note:** The validator only checks JSON files that look like MCP4H envelopes
(`version` starts with `mcp4h/` and a `metadata` object exists). Non-envelope JSON (e.g., `package.json`)
is skipped to avoid false failures.
