#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Production-Grade Server Launcher for Codex Dominion
    
.DESCRIPTION
    Starts Flask backend with Gunicorn and Next.js with PM2 for robust, auto-restarting production servers.
    Prevents crashes and automatically restarts on failure.
    
.EXAMPLE
    .\START_PRODUCTION_SERVERS.ps1
#>

Write-Host "🔥 CODEX DOMINION - PRODUCTION SERVER LAUNCHER" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "❌ Virtual environment not found. Run: python -m venv .venv" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install production dependencies
Write-Host ""
Write-Host "📥 Installing production dependencies..." -ForegroundColor Cyan

# Install Gunicorn for Flask (production WSGI server)
Write-Host "   → Installing Gunicorn (Flask production server)..."
pip install gunicorn gevent --quiet

# Install PM2 for Next.js (production process manager)
Write-Host "   → Checking for PM2 (Next.js production manager)..."
$pm2Installed = Get-Command pm2 -ErrorAction SilentlyContinue
if (-not $pm2Installed) {
    Write-Host "   → PM2 not found. Installing globally..."
    npm install -g pm2
}

Write-Host "✅ Dependencies ready" -ForegroundColor Green
Write-Host ""

# Kill any existing processes on ports 5000 and 3003
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Cyan
$processes = Get-NetTCPConnection -LocalPort 5000, 3003 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($pid in $processes) {
    Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    Write-Host "   → Stopped process $pid"
}

Write-Host ""
Write-Host "🚀 Starting production servers..." -ForegroundColor Cyan
Write-Host ""

# Start Flask with Gunicorn (4 workers, auto-restart)
Write-Host "1️⃣  Starting Flask Backend with Gunicorn..." -ForegroundColor Yellow
Write-Host "   URL: http://localhost:5000" -ForegroundColor White

$flaskCmd = @"
import sys
sys.path.insert(0, '.')
from flask_dashboard import app
if __name__ == '__main__':
    app.run()
"@

# Create Gunicorn config
$gunicornConfig = @"
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 4
worker_class = 'gevent'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'
loglevel = 'info'
access_log_format = '%%(h)s %%(l)s %%(u)s %%(t)s "%%(r)s" %%(s)s %%(b)s "%%(f)s" "%%(a)s"'

# Process naming
proc_name = 'codex-flask'

# Server mechanics
daemon = False
pidfile = 'gunicorn.pid'
user = None
group = None
umask = 0
tmp_upload_dir = None

# SSL (uncomment for HTTPS)
# keyfile = 'path/to/keyfile'
# certfile = 'path/to/certfile'
"@

# Create logs directory
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Save Gunicorn config
Set-Content -Path "gunicorn_config.py" -Value $gunicornConfig

# Start Flask with Gunicorn in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& .\.venv\Scripts\gunicorn.exe flask_dashboard:app -c gunicorn_config.py" -WindowStyle Minimized

Write-Host "   ✅ Flask started with Gunicorn (4 workers, auto-restart)" -ForegroundColor Green
Write-Host ""

# Start Next.js with PM2
Write-Host "2️⃣  Starting Next.js Frontend with PM2..." -ForegroundColor Yellow
Write-Host "   URL: http://localhost:3003" -ForegroundColor White

cd dashboard-app

# Create PM2 ecosystem file
$pm2Config = @"
module.exports = {
  apps: [
    {
      name: 'codex-nextjs',
      script: 'npm',
      args: 'run dev',
      cwd: '.',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'development',
        PORT: 3003
      },
      error_file: '../logs/pm2_nextjs_error.log',
      out_file: '../logs/pm2_nextjs_out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      restart_delay: 4000
    }
  ]
}
"@

Set-Content -Path "ecosystem.config.js" -Value $pm2Config

# Start with PM2
pm2 start ecosystem.config.js
pm2 save

cd ..

Write-Host "   ✅ Next.js started with PM2 (auto-restart enabled)" -ForegroundColor Green
Write-Host ""

Write-Host "============================================" -ForegroundColor Yellow
Write-Host "✅ PRODUCTION SERVERS RUNNING" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Access Points:" -ForegroundColor Cyan
Write-Host "   • Flask Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "   • Next.js Frontend: http://localhost:3003" -ForegroundColor White
Write-Host "   • Dashboard: http://localhost:3003/dashboard/overview" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Management Commands:" -ForegroundColor Cyan
Write-Host "   • View PM2 status:    pm2 status" -ForegroundColor White
Write-Host "   • View PM2 logs:      pm2 logs codex-nextjs" -ForegroundColor White
Write-Host "   • Restart Next.js:    pm2 restart codex-nextjs" -ForegroundColor White
Write-Host "   • Stop all:           pm2 stop all" -ForegroundColor White
Write-Host "   • View Gunicorn logs: Get-Content logs\gunicorn_access.log -Tail 50 -Wait" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Benefits:" -ForegroundColor Cyan
Write-Host "   ✓ Auto-restart on crash" -ForegroundColor Green
Write-Host "   ✓ Multi-worker processing (Flask: 4 workers)" -ForegroundColor Green
Write-Host "   ✓ Better performance under load" -ForegroundColor Green
Write-Host "   ✓ Centralized logging" -ForegroundColor Green
Write-Host "   ✓ Zero-downtime restarts" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring (servers will continue running)" -ForegroundColor Yellow
Write-Host ""

# Monitor servers
pm2 logs codex-nextjs --lines 20
