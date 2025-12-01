# 🔥 CODEX DASHBOARD BULLETPROOF LAUNCHER 👑
# Automatic port management and dashboard startup
# The Merritt Method™ - Guaranteed Access

Write-Host "🔥 CODEX DOMINION DASHBOARD LAUNCHER 👑" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow

# Kill any existing Python processes
Write-Host "`n🧹 Cleaning up existing processes..." -ForegroundColor Cyan
try {
    taskkill /f /im python.exe /t 2>$null
    Start-Sleep -Seconds 2
    Write-Host "✅ Process cleanup completed" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ No processes to clean up" -ForegroundColor Yellow
}

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $listener = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties()
        $tcpConnections = $listener.GetActiveTcpConnections()
        $usedPorts = $tcpConnections | Where-Object { $_.LocalEndPoint.Port -eq $Port }
        return $usedPorts.Count -eq 0
    }
    catch {
        return $true
    }
}

# Find available port
$ports = @(18080, 18081, 18082, 18083, 18084)
$selectedPort = $null

Write-Host "`n🔍 Finding available port..." -ForegroundColor Cyan
foreach ($port in $ports) {
    if (Test-Port -Port $port) {
        $selectedPort = $port
        Write-Host "✅ Port $port is available" -ForegroundColor Green
        break
    } else {
        Write-Host "❌ Port $port is in use" -ForegroundColor Red
    }
}

if (-not $selectedPort) {
    Write-Host "❌ No available ports found. Please close other applications and try again." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
$venvPath = ".\.venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    $pythonExe = $venvPath
} else {
    Write-Host "⚠️ Virtual environment not found, using system Python" -ForegroundColor Yellow
    $pythonExe = "python"
}

# Check if dashboard file exists
if (Test-Path "codex_simple_dashboard.py") {
    Write-Host "✅ Dashboard file found" -ForegroundColor Green
} else {
    Write-Host "❌ Dashboard file not found!" -ForegroundColor Red
    exit 1
}

# Launch dashboard
Write-Host "`n🚀 Launching Codex Dashboard on port $selectedPort..." -ForegroundColor Cyan
Write-Host "Dashboard URL: http://127.0.0.1:$selectedPort" -ForegroundColor Yellow

try {
    # Start dashboard in background
    $process = Start-Process -FilePath $pythonExe -ArgumentList "-m", "streamlit", "run", "codex_simple_dashboard.py", "--server.port", $selectedPort, "--server.address", "127.0.0.1" -PassThru -WindowStyle Hidden
    
    # Wait a moment for startup
    Start-Sleep -Seconds 3
    
    # Check if process is still running
    if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
        Write-Host "✅ Dashboard started successfully!" -ForegroundColor Green
        Write-Host "`n🎯 ACCESS YOUR DASHBOARD:" -ForegroundColor Yellow
        Write-Host "URL: http://127.0.0.1:$selectedPort" -ForegroundColor White
        Write-Host "`n📺 Features Available:" -ForegroundColor Cyan
        Write-Host "• 🏛️ Dominion Central Command" -ForegroundColor White
        Write-Host "• 🌅 Dawn Dispatch System" -ForegroundColor White
        Write-Host "• 📺 YouTube Charts (NEW!)" -ForegroundColor White
        Write-Host "• 📊 System Status Monitor" -ForegroundColor White
        
        Write-Host "`n🔥 Dashboard Process ID: $($process.Id)" -ForegroundColor Gray
        Write-Host "Use 'taskkill /f /pid $($process.Id)' to stop the dashboard" -ForegroundColor Gray
        
        # Try to open browser
        Write-Host "`n🌐 Opening browser..." -ForegroundColor Cyan
        try {
            Start-Process "http://127.0.0.1:$selectedPort"
            Write-Host "✅ Browser opened successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️ Could not auto-open browser. Please navigate manually to:" -ForegroundColor Yellow
            Write-Host "http://127.0.0.1:$selectedPort" -ForegroundColor White
        }
        
    } else {
        Write-Host "❌ Dashboard failed to start" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error launching dashboard: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔥 Codex Dashboard is now running! 👑" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop this launcher (dashboard will continue running)" -ForegroundColor Gray

# Keep launcher alive to show status
try {
    while ($true) {
        Start-Sleep -Seconds 30
        if (-not (Get-Process -Id $process.Id -ErrorAction SilentlyContinue)) {
            Write-Host "`n⚠️ Dashboard process has stopped" -ForegroundColor Yellow
            break
        }
    }
}
catch {
    Write-Host "`n🛑 Launcher stopped" -ForegroundColor Yellow
}