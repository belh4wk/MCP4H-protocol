# Quickstart (2–3 minutes)

This quickstart gives you a **single happy path**:
1) validate a canonical packet,
2) run a tiny demo that **projects** one intent to multiple modality outputs,
3) optionally send the projected cue to a **webhook**.

## Prereqs

- Python 3.10+ (Windows/macOS/Linux)
- (Recommended) a virtualenv

From repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 1) Smoke-test the MCP server

```powershell
Get-Content .\bridges\mcp\server\sample_requests.jsonl | python .\bridges\mcp\server\mcp_server.py
```

You should see three JSON-RPC responses (`initialize`, `tools/list`, `resources/list`).

## 2) Validate the canonical projected MCP example

```powershell
$path = ".\examples\messages\mcp\mcp_event_projected_payload.json"
$pkt  = Get-Content $path -Raw | ConvertFrom-Json

@{jsonrpc="2.0"; id=12; method="tools/call"; params=@{name="mcp4h.validate"; arguments=@{packet=$pkt}}} |
  ConvertTo-Json -Compress -Depth 80 |
  python .\bridges\mcp\server\mcp_server.py
```

Expected: `"ok": true`.

## 3) Run the projection demo (prints the outputs)

```powershell
python .\tools\mcp4h_demo_emit.py --input .\examples\messages\mcp\mcp_event_projected_payload.json
```

It prints what a renderer *could* output for:
- text (notifications/overlays),
- visual (LED),
- audio (beep/TTS),
- haptic (pattern).

## 4) (Optional) One-command webhook test

This posts the **projected cue payload** to your webhook endpoint:

```powershell
python .\bridges\webhook\send_projected.py --url "https://your-webhook-endpoint" --input .\examples\messages\mcp\mcp_event_projected_payload.json
```

## Where to go next

- Cues + projection model: `docs/cues.md`
- MCP interoperability: `bridges/mcp/` and `bridges/mcp/server/`
- Example messages (canonical): `examples/messages/`
- Schema: `schemas/` and `spec/`


### Continuous mode (generate JSONL directly)

```powershell
python .\bridges\mcp\map_tool_result.py --input .\examples\messages\mcp\mcp_tool_event_example.json --output-jsonl .\packets.jsonl --truncate
Get-Content .\packets.jsonl | python .\bridges\webhook\bridge.py --url "http://127.0.0.1:8080/" --cue-only --validate --once
```


## 6) Call the mapper as an MCP tool (no external script)

The MCP server now exposes a tool that maps a tool event/result into a canonical MCP4H packet:

```powershell
$ev = Get-Content .\examples\messages\mcp\mcp_tool_event_example.json -Raw | ConvertFrom-Json
@{jsonrpc="2.0"; id=22; method="tools/call"; params=@{name="mcp4h.map_tool_result"; arguments=@{event=$ev}}} |
  ConvertTo-Json -Compress -Depth 80 |
  python .\bridges\mcp\server\mcp_server.py
```

The response includes `{ ok: true, packet: {...} }`. You can then validate or send the packet to the webhook bridge.


## Publish via MCP tool

```powershell
$ev = Get-Content .\examples\messages\mcp\mcp_tool_event_example.json -Raw | ConvertFrom-Json
$mappedResp = @{jsonrpc="2.0"; id=30; method="tools/call"; params=@{name="mcp4h.map_tool_result"; arguments=@{event=$ev}}} |
  ConvertTo-Json -Compress -Depth 80 |
  python .\bridges\mcp\server\mcp_server.py | ConvertFrom-Json
$mapped = ($mappedResp.result.content[0].text | ConvertFrom-Json).packet

@{jsonrpc="2.0"; id=31; method="tools/call"; params=@{name="mcp4h.webhook.publish"; arguments=@{url="http://127.0.0.1:8080/"; packet=$mapped; cue_only=$true; validate=$true}}} |
  ConvertTo-Json -Compress -Depth 80 |
  python .\bridges\mcp\server\mcp_server.py
```


## Local web renderer (visible demo)

Start the renderer:

```powershell
python .\bridges\webhook\local_web_renderer.py
```

Then publish projected payload to it:

```powershell
python .\bridges\webhook\send_projected.py --url "http://127.0.0.1:8090/ingest" --input .\examples\messages\mcp\mcp_event_projected_payload.json --cue-only
```

Or publish via MCP tool (mapped packet):

```powershell
@{jsonrpc="2.0"; id=40; method="tools/call"; params=@{name="mcp4h.webhook.publish"; arguments=@{url="http://127.0.0.1:8090/ingest"; packet=$mapped; cue_only=$true; validate=$true}}} |
  ConvertTo-Json -Compress -Depth 80 |
  python .\bridges\mcp\server\mcp_server.py
```


## Slack / Teams (reference examples)

Slack Incoming Webhook:

```powershell
python .\bridges\webhook\send_slack.py --url "<SLACK_WEBHOOK_URL>" --input .\out_mcp4h.json
```

Teams Incoming Webhook:

```powershell
python .\bridges\webhook\send_teams.py --url "<TEAMS_WEBHOOK_URL>" --input .\out_mcp4h.json
```


## Policy (dedupe + cooldown) for streams

Use these flags on the continuous webhook bridge to avoid spam:

```powershell
Get-Content .\packets.jsonl | python .\bridges\webhook\bridge.py --url "http://127.0.0.1:8080/" --cue-only --validate --rate 10 --cooldown-ms 500 --dedupe-window-ms 1500 --dedupe-key mcp.trace_id --policy-debug
```

Notes:
- Policy is most effective in `bridges/webhook/bridge.py` because it persists while the process is running.
- The MCP tool `mcp4h.webhook.publish` also supports `cooldown_ms` and `dedupe_window_ms`, but only persists within a single server process.
