# Starts MCP4H stack in background and tails health briefly
Write-Host "🚀 Starting MCP4H (detached)..." -ForegroundColor Green
docker compose up -d
Write-Host "📡 Services:" -ForegroundColor Cyan
docker compose ps
Write-Host "ℹ️  Tail logs with: docker compose logs -f" -ForegroundColor Yellow
