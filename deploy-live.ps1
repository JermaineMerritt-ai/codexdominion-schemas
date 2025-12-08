#!/usr/bin/env pwsh
# =============================================================================
# Codex Dominion - Production Deployment Script
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "🔥 Codex Dominion - Production Deployment 🔥" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$ComposeFile = "docker-compose.live.yml"
$EnvFile = ".env"

# Check if .env file exists
if (-not (Test-Path $EnvFile)) {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    Write-Host "⚠ Please copy .env.production.template to .env and update values" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ .env file found" -ForegroundColor Green

# Check Docker installation
try {
    docker --version | Out-Null
    Write-Host "✓ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed!" -ForegroundColor Red
    exit 1
}

# Check Docker Compose
try {
    docker compose version | Out-Null
    Write-Host "✓ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Compose is not installed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 Building images..." -ForegroundColor Yellow
docker compose -f $ComposeFile build --no-cache

Write-Host "✓ Images built successfully" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Yellow
docker compose -f $ComposeFile up -d

Write-Host "✓ Services started" -ForegroundColor Green

Write-Host ""
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service health
Write-Host ""
Write-Host "🏥 Checking service health..." -ForegroundColor Yellow

Write-Host ""
Write-Host "📊 Service status:" -ForegroundColor Yellow
docker compose -f $ComposeFile ps

Write-Host ""
Write-Host "📝 Viewing logs (last 20 lines):" -ForegroundColor Yellow
docker compose -f $ComposeFile logs --tail=20

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✓ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Frontend: http://localhost:3001"
Write-Host "🔌 Backend API: http://localhost:8001"
Write-Host "📖 API Docs: http://localhost:8001/docs"
Write-Host ""
Write-Host "Commands:"
Write-Host "  View logs: docker compose -f $ComposeFile logs -f"
Write-Host "  Stop: docker compose -f $ComposeFile down"
Write-Host "  Restart: docker compose -f $ComposeFile restart"
Write-Host ""
Write-Host "🔥 The flame burns eternal! 🔥" -ForegroundColor Cyan
