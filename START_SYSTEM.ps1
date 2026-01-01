#!/usr/bin/env pwsh
# Codex Dominion - Complete System Startup Script

Write-Host "`n👑 CODEX DOMINION - SYSTEM STARTUP`n" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray

# Kill any existing processes
Write-Host "🧹 Cleaning up old processes..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Stop-Process -Name node -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start Flask Backend
Write-Host "🔥 Starting Flask Backend (Port 5000)..." -ForegroundColor Green
Start-Process python -ArgumentList "flask_dashboard.py" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
Start-Sleep -Seconds 5

# Verify Flask is running
try {
    $health = Invoke-RestMethod "http://localhost:5000/api/agents" -TimeoutSec 3
    Write-Host "   ✅ Flask running ($($health.agents.Count) agents loaded)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Flask failed to start: $_" -ForegroundColor Red
    exit 1
}

# Check if Next.js is desired
Write-Host "`n🚀 Start Next.js Dashboard? (Port 3002)" -ForegroundColor Yellow
Write-Host "   [Y] Yes  [N] No  (Default: N)" -ForegroundColor Gray
$choice = Read-Host

if ($choice -eq "Y" -or $choice -eq "y") {
    Write-Host "`n📦 Starting Next.js Dashboard..." -ForegroundColor Green
    Set-Location "$PSScriptRoot\dashboard-app"
    Start-Process npm -ArgumentList "run dev" -WorkingDirectory "$PSScriptRoot\dashboard-app" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "   ✅ Next.js starting at http://localhost:3002" -ForegroundColor Green
    Set-Location $PSScriptRoot
}

# Display Status
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "✨ SYSTEM OPERATIONAL`n" -ForegroundColor Green
Write-Host "🌐 Flask API:      http://localhost:5000" -ForegroundColor Cyan
if ($choice -eq "Y" -or $choice -eq "y") {
    Write-Host "🎨 Next.js UI:     http://localhost:3002" -ForegroundColor Cyan
}
Write-Host "📚 API Docs:       http://localhost:5000/api/agents" -ForegroundColor Cyan
Write-Host "`n💬 Test chat:      Run .\TEST_CHAT_API.ps1" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray
