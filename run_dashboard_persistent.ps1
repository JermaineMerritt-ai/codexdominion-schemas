# ============================================================================
# CODEX DOMINION PERSISTENT DASHBOARD
# ============================================================================
# This script keeps the dashboard running and auto-restarts if it crashes
# ============================================================================

param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "SilentlyContinue"

# Colors
$HeaderColor = "Cyan"
$SuccessColor = "Green"
$ErrorColor = "Red"
$WarningColor = "Yellow"
$InfoColor = "White"

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host ("=" * 80) -ForegroundColor $HeaderColor
    Write-Host $Text -ForegroundColor $HeaderColor
    Write-Host ("=" * 80) -ForegroundColor $HeaderColor
    Write-Host ""
}

function Write-Status {
    param(
        [string]$Symbol,
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host "$Symbol $Text" -ForegroundColor $Color
}

# Change to project directory
$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectPath

Write-Header "👑 CODEX DOMINION MASTER DASHBOARD - PERSISTENT MODE"

# Check Python
$PythonExe = Join-Path $ProjectPath ".venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Status "❌" "Virtual environment not found!" $ErrorColor
    Write-Host "   Expected at: $PythonExe" -ForegroundColor $ErrorColor
    Write-Host ""
    Pause
    exit 1
}

Write-Status "✅" "Python virtual environment found" $SuccessColor

# Dashboard script
$DashboardScript = Join-Path $ProjectPath "flask_dashboard.py"
if (-not (Test-Path $DashboardScript)) {
    Write-Status "❌" "Dashboard script not found!" $ErrorColor
    Write-Host "   Expected at: $DashboardScript" -ForegroundColor $ErrorColor
    Write-Host ""
    Pause
    exit 1
}

Write-Status "✅" "Dashboard script found" $SuccessColor
Write-Host ""

# Clean up old processes
Write-Status "🧹" "Cleaning up old processes..." $InfoColor
Get-Process python* -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -like "*\.venv*"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Write-Status "✅" "Ready to start" $SuccessColor
Write-Host ""

Write-Header "🚀 STARTING PERSISTENT DASHBOARD"

Write-Status "📊" "48 Intelligence Engines: Loading..." "Cyan"
Write-Status "🔧" "6 Tools Suite: Loading..." "Cyan"
Write-Status "💰" "$316/month Savings: Activating..." "Cyan"
Write-Host ""

$Attempt = 0
$MaxAttempts = 999999  # Run forever
$RestartDelay = 5

while ($Attempt -lt $MaxAttempts) {
    $Attempt++

    if ($Attempt -gt 1) {
        Write-Host ""
        Write-Status "🔄" "Restarting dashboard (Attempt $Attempt)..." $WarningColor
        Write-Host ""
        Start-Sleep -Seconds $RestartDelay
    }

    Write-Status "🌐" "Dashboard URL: http://localhost:5000" "Green"
    Write-Status "⚡" "Status: STARTING..." "Yellow"
    Write-Host ""

    # Open browser on first attempt
    if ($Attempt -eq 1 -and -not $NoBrowser) {
        Start-Sleep -Seconds 2
        Write-Status "🌐" "Opening browser..." "Cyan"
        Start-Process "http://localhost:5000"
    }

    try {
        # Run dashboard
        & $PythonExe $DashboardScript

        # If we get here, the server stopped normally
        Write-Host ""
        Write-Status "⚠️" "Dashboard stopped normally" $WarningColor

        # Ask if user wants to restart
        Write-Host ""
        $Response = Read-Host "Restart dashboard? (Y/N)"
        if ($Response -notlike "Y*") {
            break
        }

    } catch {
        Write-Host ""
        Write-Status "❌" "Dashboard crashed with error:" $ErrorColor
        Write-Host "   $($_.Exception.Message)" -ForegroundColor $ErrorColor
        Write-Status "🔄" "Will restart in $RestartDelay seconds..." $WarningColor
    }
}

Write-Host ""
Write-Header "👋 DASHBOARD SESSION ENDED"
Write-Status "📊" "Total run attempts: $Attempt" "Gray"
Write-Host ""
Write-Status "🔥" "The Flame Burns Sovereign and Eternal! 👑" "Yellow"
Write-Host ""
