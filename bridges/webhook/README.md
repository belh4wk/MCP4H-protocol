# Webhook bridge (reference)

This is the **reference output bridge**: it posts MCP4H packets (or projected cue payloads) to an HTTP webhook.

## One-command local test (no external services)

### 1) Start a local receiver (2nd PowerShell window)

```powershell
python -c "from http.server import BaseHTTPRequestHandler,HTTPServer; 
class H(BaseHTTPRequestHandler):
  def do_POST(self):
    n=int(self.headers.get('Content-Length',0)); b=self.rfile.read(n)
    print('\n--- POST', self.path, '---'); print(b.decode('utf-8','replace'))
    self.send_response(204); self.end_headers()
HTTPServer(('127.0.0.1',8080),H).serve_forever()"
```

### 2) Send the projected payload (1st PowerShell window)

```powershell
python .\bridges\webhook\send_projected.py --url "http://127.0.0.1:8080/" --input .\examples\messages\mcp\mcp_event_projected_payload.json --cue-only
```

## Continuous bridge mode (JSONL)

Read MCP4H packets (JSONL) from stdin and POST them:

```powershell
Get-Content .\packets.jsonl | python .\bridges\webhook\bridge.py --url "http://127.0.0.1:8080/"
```

Send only the first cue payload:

```powershell
Get-Content .\packets.jsonl | python .\bridges\webhook\bridge.py --url "http://127.0.0.1:8080/" --cue-only
```

Validate before posting:

```powershell
Get-Content .\packets.jsonl | python .\bridges\webhook\bridge.py --url "http://127.0.0.1:8080/" --validate
```


## Local web renderer (demo)

Run:

```powershell
python .\\bridges\\webhook\\local_web_renderer.py
```

Then publish projected payload to it:

```powershell
python .\\bridges\\webhook\\send_projected.py --url "http://127.0.0.1:8090/ingest" --input .\\examples\\messages\\mcp\\mcp_event_projected_payload.json --cue-only
```


## Slack / Teams examples

Slack incoming webhook:

```powershell
python .\\bridges\\webhook\\send_slack.py --url "<SLACK_WEBHOOK_URL>" --input .\\out_mcp4h.json
```

Teams incoming webhook:

```powershell
python .\\bridges\\webhook\\send_teams.py --url "<TEAMS_WEBHOOK_URL>" --input .\\out_mcp4h.json
```
