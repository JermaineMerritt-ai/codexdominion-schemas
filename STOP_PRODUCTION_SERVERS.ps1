#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Stop all production servers
#>

Write-Host "🛑 Stopping Codex Dominion Production Servers..." -ForegroundColor Yellow
Write-Host ""

# Stop PM2 processes
Write-Host "Stopping PM2 processes..." -ForegroundColor Cyan
pm2 stop all
pm2 delete all

# Stop Gunicorn
Write-Host "Stopping Gunicorn..." -ForegroundColor Cyan
if (Test-Path "gunicorn.pid") {
    $pid = Get-Content "gunicorn.pid"
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Remove-Item "gunicorn.pid"
}

# Kill any processes on ports 5000 and 3003
Write-Host "Cleaning up ports..." -ForegroundColor Cyan
$processes = Get-NetTCPConnection -LocalPort 5000, 3003 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($pid in $processes) {
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Write-Host "   → Stopped process $pid"
}

Write-Host ""
Write-Host "✅ All servers stopped" -ForegroundColor Green
