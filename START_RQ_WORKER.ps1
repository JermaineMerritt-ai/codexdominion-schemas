# ============================================================================
# START RQ WORKER - PowerShell Script
# ============================================================================
# This script activates the virtual environment and starts the RQ worker
# for background job processing.
#
# Usage:
#   .\START_RQ_WORKER.ps1
#
# Prerequisites:
#   - Redis server running (redis-server)
#   - Virtual environment created (.venv)
#   - Requirements installed (pip install -r requirements.txt)
# ============================================================================

Write-Host "🔥 CODEX DOMINION - RQ WORKER STARTUP" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Redis is running
Write-Host "🔍 Checking Redis connection..." -ForegroundColor Yellow
try {
    $redisUrl = $env:REDIS_URL
    if (-not $redisUrl) {
        $redisUrl = "redis://localhost:6379/0"
        Write-Host "ℹ️  Using default Redis URL: $redisUrl" -ForegroundColor Gray
    }
    
    # Test Redis connection (basic check - assumes redis-cli is available)
    $redisTest = redis-cli -u $redisUrl ping 2>$null
    if ($redisTest -eq "PONG") {
        Write-Host "✅ Redis is running and responding" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Could not verify Redis connection" -ForegroundColor Yellow
        Write-Host "   Make sure Redis server is running: redis-server" -ForegroundColor Yellow
        Write-Host "   Or run via Docker: docker run -d -p 6379:6379 redis:7-alpine" -ForegroundColor Yellow
        Write-Host ""
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y") {
            exit 1
        }
    }
}
catch {
    Write-Host "⚠️  Redis check failed (redis-cli not found)" -ForegroundColor Yellow
    Write-Host "   Assuming Redis is running..." -ForegroundColor Gray
}

Write-Host ""

# Activate virtual environment
Write-Host "🐍 Activating virtual environment..." -ForegroundColor Yellow
$venvPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    & $venvPath
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
}
else {
    Write-Host "❌ Virtual environment not found at $venvPath" -ForegroundColor Red
    Write-Host "   Create it with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Display environment info
Write-Host "📊 Environment Configuration:" -ForegroundColor Cyan
Write-Host "   Python: $(python --version)" -ForegroundColor Gray
Write-Host "   Working Directory: $(Get-Location)" -ForegroundColor Gray
Write-Host "   Redis URL: $($env:REDIS_URL ?? 'redis://localhost:6379/0')" -ForegroundColor Gray
Write-Host ""

# Start RQ worker
Write-Host "🚀 Starting RQ Worker..." -ForegroundColor Cyan
Write-Host "   Queue: workflows" -ForegroundColor Gray
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Run RQ worker
rq worker workflows --url $($env:REDIS_URL ?? 'redis://localhost:6379/0')

# If worker exits
Write-Host ""
Write-Host "🛑 RQ Worker stopped" -ForegroundColor Yellow
