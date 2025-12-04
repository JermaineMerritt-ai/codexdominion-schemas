# Simple Codex Dashboard Manager
param([string]$Action = "status")

$Port = 8095
$Script = "app.py"

Write-Host "Codex Dashboard Service Manager" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

function Get-Status {
    Write-Host "Checking dashboard status..." -ForegroundColor Cyan

    # Check if port is in use
    $portInUse = netstat -an | Select-String ":$Port "

    if ($portInUse) {
        Write-Host "Status: RUNNING" -ForegroundColor Green
        Write-Host "Port ${Port}: IN USE" -ForegroundColor Green
        Write-Host "URL: http://localhost:$Port" -ForegroundColor Cyan

        # Test if responding
        try {
            Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop | Out-Null
            Write-Host "Health: RESPONDING" -ForegroundColor Green
        }
        catch {
            Write-Host "Health: NOT RESPONDING" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Status: STOPPED" -ForegroundColor Red
        Write-Host "Port ${Port}: AVAILABLE" -ForegroundColor Yellow
    }
}

function Start-Dashboard {
    Write-Host "Starting Codex Dashboard..." -ForegroundColor Green

    $args = @("-m", "streamlit", "run", $Script, "--server.port", $Port, "--server.headless", "true")
    Start-Process -FilePath "python" -ArgumentList $args -NoNewWindow

    Write-Host "Dashboard starting..." -ForegroundColor Yellow
    Start-Sleep 3
    Get-Status
}

function Stop-Dashboard {
    Write-Host "Stopping dashboard processes..." -ForegroundColor Yellow

    Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
        $_.MainWindowTitle -like "*streamlit*" -or $_.CommandLine -like "*streamlit*"
    } | Stop-Process -Force -ErrorAction SilentlyContinue

    Write-Host "Processes stopped" -ForegroundColor Green
    Get-Status
}

# Execute action
switch ($Action.ToLower()) {
    "start" { Start-Dashboard }
    "stop" { Stop-Dashboard }
    "restart" {
        Stop-Dashboard
        Start-Sleep 2
        Start-Dashboard
    }
    "status" { Get-Status }
    default {
        Write-Host "Usage: service-simple.ps1 [start|stop|restart|status]"
        Get-Status
    }
}

Write-Host "`nService management complete!" -ForegroundColor Yellow
