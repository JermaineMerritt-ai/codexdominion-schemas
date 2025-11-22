# Codex Dominion Complete Service Manager
# Windows equivalent of systemctl commands

param(
    [string]$Action = "status",
    [string]$Service = "all"
)

# Service Configuration
$Services = @{
    "api" = @{
        Name = "CodexAPI"
        DisplayName = "Codex Trading API"
        Command = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe"
        Args = @("-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload")
        Port = 8000
        HealthCheck = "http://127.0.0.1:8000/health"
    }
    "dashboard" = @{
        Name = "CodexDashboard"
        DisplayName = "Codex Main Dashboard"
        Command = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe"
        Args = @("-m", "streamlit", "run", "codex_dashboard.py", "--server.port", "8501", "--server.address", "127.0.0.1", "--server.headless", "true")
        Port = 8501
        HealthCheck = "http://127.0.0.1:8501"
    }
    "portfolio" = @{
        Name = "CodexPortfolio"
        DisplayName = "Codex Portfolio Dashboard"
        Command = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe"
        Args = @("-m", "streamlit", "run", "codex_portfolio_dashboard.py", "--server.port", "8503", "--server.address", "127.0.0.1", "--server.headless", "true")
        Port = 8503
        HealthCheck = "http://127.0.0.1:8503"
    }
    "proxy" = @{
        Name = "CodexProxy"
        DisplayName = "Codex Reverse Proxy"
        Command = "node"
        Args = @("proxy.js")
        Port = 3000
        HealthCheck = "http://127.0.0.1:3000/health"
    }
}

$WorkingDirectory = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"

Write-Host "🚀 CODEX DOMINION SERVICE MANAGER" -ForegroundColor Cyan
Write-Host "=" * 45 -ForegroundColor Cyan

Set-Location $WorkingDirectory

function Start-CodexService {
    param($ServiceConfig, $ServiceKey)
    
    Write-Host "🟢 Starting $($ServiceConfig.DisplayName)..." -ForegroundColor Green
    
    # Kill existing processes on this port
    $existingProcesses = Get-Process | Where-Object {
        $_.ProcessName -eq "python" -or $_.ProcessName -eq "node"
    } | Where-Object {
        $connections = netstat -ano | Select-String ":$($ServiceConfig.Port)"
        $connections | ForEach-Object {
            if ($_ -match ":$($ServiceConfig.Port)\s+.*\s+(\d+)$") {
                return $matches[1] -eq $_.Id
            }
        }
    }
    
    $existingProcesses | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
    
    # Start the service
    $process = Start-Process -FilePath $ServiceConfig.Command -ArgumentList $ServiceConfig.Args -WorkingDirectory $WorkingDirectory -WindowStyle Hidden -PassThru
    Write-Host "🚀 Started process ID: $($process.Id)" -ForegroundColor Green
    
    Start-Sleep 3
    
    # Verify startup
    try {
        if ($ServiceConfig.HealthCheck) {
            $response = Invoke-WebRequest -Uri $ServiceConfig.HealthCheck -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ $($ServiceConfig.DisplayName) started successfully (Port $($ServiceConfig.Port))" -ForegroundColor Green
            } else {
                Write-Host "⚠️ $($ServiceConfig.DisplayName) started but returned status $($response.StatusCode)" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "⚠️ $($ServiceConfig.DisplayName) started but health check failed" -ForegroundColor Yellow
    }
}

function Stop-CodexService {
    param($ServiceConfig, $ServiceKey)
    
    Write-Host "🛑 Stopping $($ServiceConfig.DisplayName)..." -ForegroundColor Yellow
    
    # Find processes using the port
    $portProcesses = netstat -ano | Select-String ":$($ServiceConfig.Port)" | ForEach-Object {
        if ($_ -match ":$($ServiceConfig.Port)\s+.*\s+(\d+)$") {
            Get-Process -Id $matches[1] -ErrorAction SilentlyContinue
        }
    }
    
    $portProcesses | ForEach-Object {
        if ($null -ne $_) {
            Write-Host "🔥 Stopping process $($_.Id)..." -ForegroundColor Red
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "✅ $($ServiceConfig.DisplayName) stopped" -ForegroundColor Green
}

function Get-CodexServiceStatus {
    param($ServiceConfig, $ServiceKey)
    
    Write-Host ""
    Write-Host "📊 $($ServiceConfig.DisplayName):" -ForegroundColor Cyan
    
    # Check port status
    $portCheck = netstat -ano | Select-String ":$($ServiceConfig.Port)"
    
    if ($portCheck) {
        # Extract process ID
        $portCheck | ForEach-Object {
            if ($_ -match ":$($ServiceConfig.Port)\s+.*LISTENING\s+(\d+)") {
                $processId = $matches[1]
                $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
                
                if ($process) {
                    Write-Host "   Status: ✅ RUNNING" -ForegroundColor Green
                    Write-Host "   Process ID: $processId" -ForegroundColor White
                    Write-Host "   Port: $($ServiceConfig.Port)" -ForegroundColor White
                    Write-Host "   Memory: $([math]::Round($process.WorkingSet64/1MB, 2)) MB" -ForegroundColor White
                    
                    # Health check
                    if ($ServiceConfig.HealthCheck) {
                        try {
                            $response = Invoke-WebRequest -Uri $ServiceConfig.HealthCheck -TimeoutSec 5 -UseBasicParsing
                            if ($response.StatusCode -eq 200) {
                                Write-Host "   Health: ✅ HEALTHY (Status: $($response.StatusCode))" -ForegroundColor Green
                            } else {
                                Write-Host "   Health: ⚠️ RESPONDING (Status: $($response.StatusCode))" -ForegroundColor Yellow
                            }
                        } catch {
                            Write-Host "   Health: ❌ UNHEALTHY" -ForegroundColor Red
                        }
                    }
                } else {
                    Write-Host "   Status: ⚠️ PORT OCCUPIED (Unknown Process)" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "   Status: ❌ STOPPED" -ForegroundColor Red
        Write-Host "   Port: $($ServiceConfig.Port) (Available)" -ForegroundColor Gray
    }
}

# Main execution logic
switch ($Action.ToLower()) {
    "start" {
        if ($Service -eq "all") {
            $Services.GetEnumerator() | ForEach-Object {
                Start-CodexService $_.Value $_.Key
            }
        } elseif ($Services.ContainsKey($Service)) {
            Start-CodexService $Services[$Service] $Service
        } else {
            Write-Host "❌ Unknown service: $Service" -ForegroundColor Red
            Write-Host "Available services: $($Services.Keys -join ', ')" -ForegroundColor Gray
        }
    }
    
    "stop" {
        if ($Service -eq "all") {
            $Services.GetEnumerator() | ForEach-Object {
                Stop-CodexService $_.Value $_.Key
            }
        } elseif ($Services.ContainsKey($Service)) {
            Stop-CodexService $Services[$Service] $Service
        } else {
            Write-Host "❌ Unknown service: $Service" -ForegroundColor Red
        }
    }
    
    "restart" {
        Write-Host "🔄 Restarting services..." -ForegroundColor Yellow
        & $MyInvocation.MyCommand.Path -Action "stop" -Service $Service
        Start-Sleep 2
        & $MyInvocation.MyCommand.Path -Action "start" -Service $Service
    }
    
    "status" {
        Write-Host "📋 Codex Dominion Service Status:" -ForegroundColor Cyan
        
        if ($Service -eq "all") {
            $Services.GetEnumerator() | ForEach-Object {
                Get-CodexServiceStatus $_.Value $_.Key
            }
        } elseif ($Services.ContainsKey($Service)) {
            Get-CodexServiceStatus $Services[$Service] $Service
        }
        
        Write-Host ""
        Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
        Write-Host "   API Documentation: http://127.0.0.1:8000/docs" -ForegroundColor White
        Write-Host "   Main Dashboard: http://127.0.0.1:8501" -ForegroundColor White
        Write-Host "   Portfolio Dashboard: http://127.0.0.1:8503" -ForegroundColor White
        Write-Host "   Reverse Proxy: http://127.0.0.1:3000" -ForegroundColor White
    }
    
    default {
        Write-Host "❓ USAGE:" -ForegroundColor Yellow
        Write-Host "  .\codex-service-manager.ps1 -Action start -Service [all|api|dashboard|portfolio|proxy]" -ForegroundColor White
        Write-Host "  .\codex-service-manager.ps1 -Action stop -Service [all|api|dashboard|portfolio|proxy]" -ForegroundColor White
        Write-Host "  .\codex-service-manager.ps1 -Action restart -Service [all|api|dashboard|portfolio|proxy]" -ForegroundColor White
        Write-Host "  .\codex-service-manager.ps1 -Action status -Service [all|api|dashboard|portfolio|proxy]" -ForegroundColor White
        Write-Host ""
        Write-Host "📋 Examples:" -ForegroundColor Cyan
        Write-Host "  .\codex-service-manager.ps1 -Action start -Service all" -ForegroundColor Gray
        Write-Host "  .\codex-service-manager.ps1 -Action status" -ForegroundColor Gray
        Write-Host "  .\codex-service-manager.ps1 -Action restart -Service dashboard" -ForegroundColor Gray
    }
}