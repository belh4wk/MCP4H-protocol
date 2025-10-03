param(
  [string]$FilePath = "examples_cues\smoketest.json"
)
if (-not (Test-Path $FilePath)) {
  Write-Error "File not found: $FilePath"
  exit 1
}
Write-Host "🔥 Smoke testing with $FilePath" -ForegroundColor Green
curl.exe -X POST http://localhost:8080/cue -H "Content-Type: application/mcp4h+json" --data-binary "@$FilePath"
