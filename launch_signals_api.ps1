# 🔥 Codex Signals API Launcher
# =============================
# FastAPI REST API Service for Advanced Market Intelligence

param(
    [string]$HostAddress = "0.0.0.0",
    [int]$Port = 8000,
    [switch]$Reload,
    [string]$LogLevel = "info"
)

Write-Host "🔥 LAUNCHING CODEX SIGNALS API 📊" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow
Write-Host "The Merritt Method™ - Scalable Financial Intelligence" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "codex_signals\api.py")) {
    Write-Host "❌ Error: codex_signals\api.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the codex-dominion directory." -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Green
pip install fastapi uvicorn pydantic

Write-Host ""
Write-Host "🚀 Starting FastAPI Signals Service..." -ForegroundColor Green
Write-Host "API will be available at: http://$HostAddress`:$Port" -ForegroundColor White
Write-Host "Interactive docs at: http://$HostAddress`:$Port/docs" -ForegroundColor White
Write-Host "ReDoc documentation: http://$HostAddress`:$Port/redoc" -ForegroundColor White
Write-Host ""

Write-Host "📊 AVAILABLE ENDPOINTS:" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow
Write-Host "POST /signals/daily     - Generate daily portfolio signals" -ForegroundColor Cyan
Write-Host "GET  /signals/mock      - Generate signals with mock data" -ForegroundColor Cyan
Write-Host "GET  /signals/live      - Generate signals with live data" -ForegroundColor Cyan
Write-Host "GET  /signals/dawn      - Dawn dispatch integration" -ForegroundColor Cyan
Write-Host "POST /classify/tier     - Classify single asset tier" -ForegroundColor Cyan
Write-Host "POST /portfolio/analysis - Complete portfolio analysis" -ForegroundColor Cyan
Write-Host "GET  /engine/config     - Get engine configuration" -ForegroundColor Cyan
Write-Host "POST /engine/config     - Update engine configuration" -ForegroundColor Cyan
Write-Host "GET  /health            - Service health check" -ForegroundColor Cyan
Write-Host "GET  /metrics           - Performance metrics" -ForegroundColor Cyan
Write-Host "GET  /docs              - Interactive API documentation" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔥 FASTAPI SIGNALS ENGINE ACTIVATED 👑" -ForegroundColor Yellow
Write-Host ""

# Build uvicorn command
$ReloadFlag = if ($Reload) { "--reload" } else { "" }

# Run the FastAPI server
uvicorn codex_signals.api:app --host $HostAddress --port $Port --log-level $LogLevel $ReloadFlag