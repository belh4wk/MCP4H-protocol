# MCP4H MCP Server (minimal, runnable)

This is a **minimal** MCP (Model Context Protocol) server that exposes MCP4H as:

- **Tools**
  - `mcp4h.validate`
  - `mcp4h.normalize`
  - `mcp4h.publish` (stub)
- **Resources**
  - `mcp4h://schema/v0.1`
  - `mcp4h://schema/v0.1.1`
  - `mcp4h://examples/messages/index`
  - `mcp4h://examples/messages/<path>`

## Transport

Stdio JSON-RPC (one request per line, one response per line). This matches common MCP host patterns.

## Run

From repo root:

```bash
python bridges/mcp/server/mcp_server.py
```

## Quick manual test

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python bridges/mcp/server/mcp_server.py
```

Then:

```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python bridges/mcp/server/mcp_server.py
```

## Wiring publish()

`mcp4h.publish` currently returns an ACK only. Next step is to connect it to `bridges/cue-router/` or MQTT.


## Windows PowerShell note (UTF-8 BOM)

Windows PowerShell may emit a UTF-8 BOM at the start of piped output or when using `Set-Content -Encoding utf8`. The server strips BOMs automatically, but if you edit JSON files, prefer `-Encoding utf8NoBOM` when available.


## Windows PowerShell 5.1 note (UTF-16 pipes)

Windows PowerShell may pipe text to external programs as **UTF-16LE**.
This server reads from `sys.stdin.buffer` and decodes BOM/UTF-16 safely, so JSON-RPC requests won't fail.

If you still want to force UTF-8 in your session:

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $OutputEncoding
```
