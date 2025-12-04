# Simple Codex Service Manager - Windows systemctl equivalent
param([string]$Action = "status")

$WorkingDirectory = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
Set-Location $WorkingDirectory

Write-Host "CODEX SERVICE MANAGER (Windows)" -ForegroundColor Cyan

function Show-Status {
    Write-Host ""
    Write-Host "Service Status:" -ForegroundColor Cyan

    # Check FastAPI (Port 8000)
    $api = netstat -ano | Select-String ":8000.*LISTENING"
    if ($api) {
        Write-Host "API (8000): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "API (8000): STOPPED" -ForegroundColor Red
    }

    # Check Main Dashboard (Port 8501)
    $dash = netstat -ano | Select-String ":8501.*LISTENING"
    if ($dash) {
        Write-Host "Dashboard (8501): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "Dashboard (8501): STOPPED" -ForegroundColor Red
    }

    # Check Portfolio (Port 8503)
    $port = netstat -ano | Select-String ":8503.*LISTENING"
    if ($port) {
        Write-Host "Portfolio (8503): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "Portfolio (8503): STOPPED" -ForegroundColor Red
    }

    Write-Host ""
    Write-Host "Access URLs:" -ForegroundColor Cyan
    Write-Host "  http://127.0.0.1:8000/docs  (API)" -ForegroundColor White
    Write-Host "  http://127.0.0.1:8501      (Dashboard)" -ForegroundColor White
    Write-Host "  http://127.0.0.1:8503      (Portfolio)" -ForegroundColor White
}

function Start-Services {
    Write-Host ""
    Write-Host "Starting services..." -ForegroundColor Green

    # Kill existing Python processes that might conflict
    Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -eq "python"
    } | Stop-Process -Force -ErrorAction SilentlyContinue

    Write-Host "Starting Dashboard on port 8501..."
    try {
        Start-Process -FilePath "$WorkingDirectory\.venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "codex_simple_dashboard.py", "--server.port", "8501", "--server.address", "127.0.0.1", "--server.headless", "true" -WindowStyle Hidden -ErrorAction Stop
    } catch {
        Write-Host "Failed to start dashboard: $($_.Exception.Message)" -ForegroundColor Red
    }

    Write-Host "Starting Portfolio on port 8503..."
    try {
        Start-Process -FilePath "$WorkingDirectory\.venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "codex_portfolio_dashboard.py", "--server.port", "8503", "--server.address", "127.0.0.1", "--server.headless", "true" -WindowStyle Hidden -ErrorAction Stop
    } catch {
        Write-Host "Failed to start portfolio: $($_.Exception.Message)" -ForegroundColor Red
    }

    Start-Sleep 5
    Write-Host "Services starting complete" -ForegroundColor Green
}

function Stop-Services {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow

    # Find and stop processes using our ports
    $ports = @(8000, 8501, 8503)
    foreach ($port in $ports) {
        $connections = netstat -ano | Select-String ":$port.*LISTENING"
        foreach ($conn in $connections) {
            if ($conn -match ":$port\s+.*LISTENING\s+(\d+)") {
                $processId = $matches[1]
                try {
                    Stop-Process -Id $processId -Force -ErrorAction Stop
                    Write-Host "Stopped process $processId on port $port" -ForegroundColor Green
                } catch {
                    Write-Host "Failed to stop process $processId" -ForegroundColor Red
                }
            }
        }
    }

    Write-Host "All services stopped" -ForegroundColor Green
}

# Execute based on action
switch ($Action.ToLower()) {
    "start" {
        Start-Services
        Show-Status
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Stop-Services
        Start-Sleep 2
        Start-Services
        Show-Status
    }
    "reload" {
        Stop-Services
        Start-Sleep 2
        Start-Services
        Show-Status
    }
    "status" {
        Show-Status
    }
    default {
        Write-Host "Usage: .\codex-systemctl.ps1 [start|stop|restart|reload|status]" -ForegroundColor Yellow
        Show-Status
    }
}
