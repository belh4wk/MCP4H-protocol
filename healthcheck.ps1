# MCP4H healthcheck
Set-Location -Path $PSScriptRoot
try {
  $r = Invoke-WebRequest -Uri "http://localhost:8080/docs" -UseBasicParsing -TimeoutSec 3
  Write-Host "Gateway: OK" -ForegroundColor Green
} catch {
  Write-Host "Gateway not reachable ❌  (Is 'docker compose up' running?)" -ForegroundColor Red
  exit 1
}
Write-Host "Posting trail_brake_deep..." -ForegroundColor Yellow
$res = Invoke-WebRequest -Uri "http://localhost:8080/cue" -Method Post `
  -ContentType "application/mcp4h+json" `
  -InFile ".\examples_cues\trail_brake_deep.json" -UseBasicParsing
Write-Host $res.Content
Write-Host "All green ✅" -ForegroundColor Green
