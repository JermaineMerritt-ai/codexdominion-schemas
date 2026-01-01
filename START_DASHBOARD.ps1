# ============================================================================
# CODEX DOMINION MASTER DASHBOARD - FIXED LAUNCHER
# ============================================================================
# This version opens Flask in a separate persistent window
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "👑 CODEX DOMINION MASTER DASHBOARD" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectPath

Write-Host "📂 Project Path: $ProjectPath" -ForegroundColor Gray
Write-Host ""

# Check if virtual environment exists
$VenvPath = Join-Path $ProjectPath ".venv"
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (-not (Test-Path $ActivateScript)) {
    Write-Host "❌ ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Expected at: $VenvPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Please create virtual environment first:" -ForegroundColor Yellow
    Write-Host "   python -m venv .venv" -ForegroundColor White
    Write-Host ""
    Pause
    exit 1
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host ""

# Kill any existing Flask processes on port 5000
Write-Host "🧹 Cleaning up old processes..." -ForegroundColor Gray
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port5000) {
    $processId = $port5000[0].OwningProcess
    Write-Host "   Stopping process $processId on port 5000..." -ForegroundColor Gray
    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host "✅ Ready to start" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING DASHBOARD IN NEW WINDOW..." -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 52+ Integrated Dashboards" -ForegroundColor Cyan
Write-Host "🤖 AI Agents & Automation" -ForegroundColor Cyan
Write-Host "💰 Revenue & Treasury Tracking" -ForegroundColor Cyan
Write-Host ""

# Launch Flask in a new persistent PowerShell window
$launchCommand = "cd '$ProjectPath'; Write-Host ''; Write-Host '🔥 CODEX DOMINION DASHBOARD 👑' -ForegroundColor Yellow; Write-Host '============================================================================' -ForegroundColor Cyan; Write-Host ''; & '$ActivateScript'; Write-Host '✅ Virtual environment activated' -ForegroundColor Green; Write-Host '✅ Starting Flask on http://localhost:5000' -ForegroundColor Cyan; Write-Host ''; Write-Host '⚠️  KEEP THIS WINDOW OPEN while using the dashboard!' -ForegroundColor Red; Write-Host '   Press Ctrl+C here to stop Flask' -ForegroundColor Gray; Write-Host ''; Write-Host '============================================================================' -ForegroundColor Cyan; Write-Host ''; python flask_dashboard.py"

Start-Process powershell -ArgumentList "-NoExit", "-Command", $launchCommand -WindowStyle Normal

# Wait for Flask to start
Write-Host "⏳ Waiting for Flask to start (7 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 7

# Test if Flask is responding
Write-Host "🔍 Testing Flask connection..." -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host "✅ FLASK IS RUNNING SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Available Dashboards:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   🏠 Home:            http://localhost:5000" -ForegroundColor White
    Write-Host "   💰 Revenue:         http://localhost:5000/revenue" -ForegroundColor White
    Write-Host "   📱 Social Media:    http://localhost:5000/social" -ForegroundColor White
    Write-Host "   🛒 Stores:          http://localhost:5000/stores" -ForegroundColor White
    Write-Host "   🤖 AI Agents:       http://localhost:5000/agents" -ForegroundColor White
    Write-Host "   🎯 AI Advisor:      http://localhost:5000/ai-advisor" -ForegroundColor White
    Write-Host "   💸 Affiliate:       http://localhost:5000/affiliate" -ForegroundColor White
    Write-Host "   🌐 Websites:        http://localhost:5000/websites" -ForegroundColor White
    Write-Host "   🚀 Auto-Publish:    http://localhost:5000/autopublish" -ForegroundColor White
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Opening dashboard in your browser..." -ForegroundColor Cyan
    Start-Process "http://localhost:5000"
    Write-Host ""
    Write-Host "✅ Dashboard is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑" -ForegroundColor Yellow
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Yellow
    Write-Host "⚠️  Flask is starting but not yet responding" -ForegroundColor Yellow
    Write-Host "============================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Give it a few more seconds, then visit:" -ForegroundColor Gray
    Write-Host "   http://localhost:5000" -ForegroundColor White
    Write-Host ""
    Write-Host "   If it still doesn't work, check the Flask window for errors" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "📌 IMPORTANT NOTES:" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   • Flask is running in a separate window" -ForegroundColor White
Write-Host "   • DO NOT close the Flask window" -ForegroundColor Red
Write-Host "   • This launcher can be closed safely" -ForegroundColor Green
Write-Host "   • To stop Flask: Press Ctrl+C in the Flask window" -ForegroundColor White
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to close this launcher..." -ForegroundColor Gray
Read-Host
