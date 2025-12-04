# Simple Codex Service Manager - Windows systemctl equivalent
param([string]$Action = "status", [string]$Service = "all")

$WorkingDirectory = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
Set-Location $WorkingDirectory

Write-Host "🚀 CODEX SERVICE MANAGER" -ForegroundColor Cyan

function Show-Status {
    Write-Host "`n📊 Service Status:" -ForegroundColor Cyan

    # Check FastAPI (Port 8000)
    $api = netstat -ano | Select-String ":8000.*LISTENING"
    if ($api) {
        Write-Host "✅ API (8000): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ API (8000): STOPPED" -ForegroundColor Red
    }

    # Check Main Dashboard (Port 8501)
    $dash = netstat -ano | Select-String ":8501.*LISTENING"
    if ($dash) {
        Write-Host "✅ Dashboard (8501): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ Dashboard (8501): STOPPED" -ForegroundColor Red
    }

    # Check Portfolio (Port 8503)
    $port = netstat -ano | Select-String ":8503.*LISTENING"
    if ($port) {
        Write-Host "✅ Portfolio (8503): RUNNING" -ForegroundColor Green
    } else {
        Write-Host "❌ Portfolio (8503): STOPPED" -ForegroundColor Red
    }

    Write-Host "`n🌐 Access URLs:" -ForegroundColor Cyan
    Write-Host "   http://127.0.0.1:8000/docs  (API)" -ForegroundColor White
    Write-Host "   http://127.0.0.1:8501      (Dashboard)" -ForegroundColor White
    Write-Host "   http://127.0.0.1:8503      (Portfolio)" -ForegroundColor White
}

function Start-Services {
    Write-Host "`n🚀 Starting services..." -ForegroundColor Green

    # Kill existing Python processes
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

    Write-Host "Starting API on port 8000..."
    Start-Process -FilePath "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe" -ArgumentList "-c", "print('API placeholder - implement uvicorn command')" -WindowStyle Hidden

    Write-Host "Starting Dashboard on port 8501..."
    Start-Process -FilePath "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "codex_simple_dashboard.py", "--server.port", "8501", "--server.address", "127.0.0.1" -WindowStyle Hidden -ErrorAction SilentlyContinue

    Write-Host "Starting Portfolio on port 8503..."
    Start-Process -FilePath "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe" -ArgumentList "-m", "streamlit", "run", "codex_portfolio_dashboard.py", "--server.port", "8503", "--server.address", "127.0.0.1" -WindowStyle Hidden -ErrorAction SilentlyContinue

    Start-Sleep 3
    Write-Host "✅ Services starting..." -ForegroundColor Green
}

function Stop-Services {
    Write-Host "`n🛑 Stopping services..." -ForegroundColor Yellow

    # Find and stop Python processes on our ports
    $processes = Get-Process python -ErrorAction SilentlyContinue
    if ($processes) {
        $processes | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "✅ All services stopped" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ No services were running" -ForegroundColor Gray
    }
}

# Execute based on action
switch ($Action.ToLower()) {
    "start" { Start-Services; Show-Status }
    "stop" { Stop-Services }
    "restart" { Stop-Services; Start-Sleep 2; Start-Services; Show-Status }
    "reload" { Stop-Services; Start-Sleep 2; Start-Services; Show-Status }
    "status" { Show-Status }
    default {
        Write-Host "Usage: .\simple-service-manager.ps1 [start|stop|restart|reload|status]" -ForegroundColor Yellow
        Show-Status
    }
}
