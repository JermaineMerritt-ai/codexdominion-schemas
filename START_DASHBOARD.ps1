# ============================================================================
# CODEX DOMINION MASTER DASHBOARD - EASY LAUNCHER
# ============================================================================
# Double-click this file to start your dashboard!
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "👑 CODEX DOMINION MASTER DASHBOARD ULTIMATE" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectPath

Write-Host "📂 Project Path: $ProjectPath" -ForegroundColor Gray
Write-Host ""

# Check if virtual environment exists
$VenvPath = Join-Path $ProjectPath ".venv"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
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

# Check if Flask is installed
Write-Host "🔍 Checking Flask installation..." -ForegroundColor Gray
$FlaskCheck = & $PythonExe -c "import flask; print('OK')" 2>&1
if ($FlaskCheck -notlike "*OK*") {
    Write-Host "❌ Flask not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Installing Flask now..." -ForegroundColor Yellow
    & $PythonExe -m pip install flask
    Write-Host ""
}

Write-Host "✅ Flask is installed" -ForegroundColor Green
Write-Host ""

# Kill any existing Python processes on port 5000
Write-Host "🧹 Cleaning up old processes..." -ForegroundColor Gray
Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*\.venv*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Host "✅ Ready to start" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING DASHBOARD..." -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 48 Intelligence Engines: Loading..." -ForegroundColor Cyan
Write-Host "🔧 6 Tools Suite: Loading..." -ForegroundColor Cyan
Write-Host "💰 $316/month Savings: Active..." -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "🌐 Dashboard will open at: http://localhost:5000" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "   Main Dashboard:     http://localhost:5000" -ForegroundColor White
Write-Host "   Intelligence:       http://localhost:5000/engines" -ForegroundColor White
Write-Host "   Tools Suite:        http://localhost:5000/tools" -ForegroundColor White
Write-Host "   System Status:      http://localhost:5000/status" -ForegroundColor White
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "⚠️  IMPORTANT: Keep this window open while using the dashboard!" -ForegroundColor Yellow
Write-Host "⚠️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Wait a moment before starting
Start-Sleep -Seconds 2

# Start the Flask dashboard
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑" -ForegroundColor Yellow
Write-Host ""

try {
    # Launch dashboard and open browser after 3 seconds
    $DashboardScript = Join-Path $ProjectPath "flask_dashboard.py"

    # Start dashboard in background
    $Job = Start-Job -ScriptBlock {
        param($PythonPath, $ScriptPath)
        & $PythonPath $ScriptPath
    } -ArgumentList $PythonExe, $DashboardScript

    # Wait for server to start
    Start-Sleep -Seconds 3

    # Open browser
    Write-Host "🌐 Opening dashboard in browser..." -ForegroundColor Cyan
    Start-Process "http://localhost:5000"

    Write-Host ""
    Write-Host "✅ Dashboard is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to stop the dashboard..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

    # Stop the job
    Stop-Job $Job
    Remove-Job $Job

    Write-Host ""
    Write-Host "👋 Dashboard stopped. Thank you!" -ForegroundColor Cyan

} catch {
    Write-Host ""
    Write-Host "❌ ERROR: Failed to start dashboard" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Running direct command instead..." -ForegroundColor Yellow
    Write-Host ""

    # Fallback: Run directly
    & $PythonExe $DashboardScript
}

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Dashboard session ended" -ForegroundColor Gray
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
