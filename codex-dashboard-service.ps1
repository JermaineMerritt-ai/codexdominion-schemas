# Codex Dashboard Windows Service Script
# This replaces systemd on Windows

param(
    [string]$Action = "start"
)

# Service Configuration
$ServiceName = "CodexDashboard"
$ServiceDisplayName = "Codex Dashboard - Digital Sovereignty Control Interface"
$WorkingDirectory = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
$PythonPath = "$WorkingDirectory\.venv\Scripts\python.exe"
$DashboardScript = "codex_dashboard.py"
$Port = 8501
$Address = "127.0.0.1"

Write-Host "🚀 CODEX DASHBOARD WINDOWS SERVICE" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

# Change to working directory
Set-Location $WorkingDirectory

switch ($Action.ToLower()) {
    "start" {
        Write-Host "🟢 Starting Codex Dashboard Service..." -ForegroundColor Green
        
        # Kill any existing instances
        Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*streamlit*"} | Stop-Process -Force -ErrorAction SilentlyContinue
        
        # Start the dashboard
        Write-Host "📊 Launching Dashboard on port $Port..." -ForegroundColor Yellow
        Start-Process -FilePath $PythonPath -ArgumentList @(
            "-m", "streamlit", "run", 
            $DashboardScript,
            "--server.port", $Port,
            "--server.address", $Address,
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ) -WorkingDirectory $WorkingDirectory -WindowStyle Hidden
        
        Start-Sleep 3
        
        # Verify service is running
        $streamlitProcess = Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*streamlit*"}
        if ($streamlitProcess) {
            Write-Host "✅ Dashboard service started successfully!" -ForegroundColor Green
            Write-Host "🌐 Access at: http://$Address`:$Port" -ForegroundColor White
            Write-Host "📊 Process ID: $($streamlitProcess.Id)" -ForegroundColor Gray
        } else {
            Write-Host "❌ Failed to start dashboard service" -ForegroundColor Red
        }
    }
    
    "stop" {
        Write-Host "🛑 Stopping Codex Dashboard Service..." -ForegroundColor Yellow
        
        # Find and stop streamlit processes
        $processes = Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*streamlit*"}
        
        if ($processes) {
            $processes | ForEach-Object {
                Write-Host "🔥 Stopping process $($_.Id)..." -ForegroundColor Red
                Stop-Process -Id $_.Id -Force
            }
            Write-Host "✅ Dashboard service stopped" -ForegroundColor Green
        } else {
            Write-Host "ℹ️ No dashboard service running" -ForegroundColor Gray
        }
    }
    
    "restart" {
        Write-Host "🔄 Restarting Codex Dashboard Service..." -ForegroundColor Yellow
        & $MyInvocation.MyCommand.Path -Action "stop"
        Start-Sleep 2
        & $MyInvocation.MyCommand.Path -Action "start"
    }
    
    "status" {
        Write-Host "📋 Codex Dashboard Service Status:" -ForegroundColor Cyan
        
        # Check for running processes
        $processes = Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*streamlit*"}
        
        if ($processes) {
            Write-Host "✅ Service Status: RUNNING" -ForegroundColor Green
            $processes | ForEach-Object {
                Write-Host "📊 Process ID: $($_.Id)" -ForegroundColor White
                Write-Host "💾 Memory Usage: $([math]::Round($_.WorkingSet64/1MB, 2)) MB" -ForegroundColor White
                Write-Host "⏱️ Start Time: $($_.StartTime)" -ForegroundColor White
            }
            
            # Test connectivity
            try {
                $response = Invoke-WebRequest -Uri "http://$Address`:$Port" -TimeoutSec 5 -UseBasicParsing
                if ($response.StatusCode -eq 200) {
                    Write-Host "🌐 Web Interface: ACCESSIBLE" -ForegroundColor Green
                } else {
                    Write-Host "🌐 Web Interface: RESPONSE CODE $($response.StatusCode)" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "🌐 Web Interface: NOT ACCESSIBLE" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ Service Status: STOPPED" -ForegroundColor Red
        }
        
        # Show port status
        $portCheck = netstat -ano | Select-String ":$Port"
        if ($portCheck) {
            Write-Host "🔌 Port $Port`: IN USE" -ForegroundColor Green
        } else {
            Write-Host "🔌 Port $Port`: AVAILABLE" -ForegroundColor Yellow
        }
    }
    
    "install" {
        Write-Host "🔧 Installing Codex Dashboard as Windows Service..." -ForegroundColor Cyan
        
        # Create Windows Service
        $servicePath = "`"powershell.exe`" -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`" -Action start"
        
        try {
            sc.exe create $ServiceName binPath= $servicePath displayName= $ServiceDisplayName start= auto
            Write-Host "✅ Windows Service installed successfully!" -ForegroundColor Green
            Write-Host "ℹ️ Use 'sc start $ServiceName' to start the service" -ForegroundColor Gray
        } catch {
            Write-Host "❌ Failed to install Windows Service" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
    
    "uninstall" {
        Write-Host "🗑️ Removing Codex Dashboard Windows Service..." -ForegroundColor Yellow
        
        try {
            sc.exe stop $ServiceName
            sc.exe delete $ServiceName
            Write-Host "✅ Windows Service removed successfully!" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to remove Windows Service" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "❓ USAGE:" -ForegroundColor Yellow
        Write-Host "  .\codex-dashboard-service.ps1 -Action start" -ForegroundColor White
        Write-Host "  .\codex-dashboard-service.ps1 -Action stop" -ForegroundColor White
        Write-Host "  .\codex-dashboard-service.ps1 -Action restart" -ForegroundColor White
        Write-Host "  .\codex-dashboard-service.ps1 -Action status" -ForegroundColor White
        Write-Host "  .\codex-dashboard-service.ps1 -Action install" -ForegroundColor White
        Write-Host "  .\codex-dashboard-service.ps1 -Action uninstall" -ForegroundColor White
        Write-Host ""
        Write-Host "🔧 Windows Service Commands:" -ForegroundColor Cyan
        Write-Host "  sc start $ServiceName" -ForegroundColor Gray
        Write-Host "  sc stop $ServiceName" -ForegroundColor Gray
        Write-Host "  sc query $ServiceName" -ForegroundColor Gray
    }
}