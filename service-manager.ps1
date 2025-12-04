# Codex Dashboard Windows Service Management (Simplified)
# PowerShell script to manage Codex Dashboard as Windows service

param(
    [Parameter(Position=0)]
    [ValidateSet("install", "start", "stop", "restart", "status", "uninstall")]
    [string]$Action = "status"
)

$ServiceName = "CodexDashboard"
$ServiceDisplayName = "Codex Dashboard - Digital Sovereignty Interface"
$WorkingDirectory = Get-Location
$StreamlitScript = "app.py"
$Port = 8095

Write-Host "🔥 CODEX DASHBOARD SERVICE MANAGEMENT" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Start-DashboardProcess {
    Write-Host "🚀 Starting Codex Dashboard directly..." -ForegroundColor Green

    $processArgs = @(
        "-m", "streamlit", "run", $StreamlitScript,
        "--server.port", $Port,
        "--server.headless", "true",
        "--server.address", "localhost"
    )

    try {
        $process = Start-Process -FilePath "python" -ArgumentList $processArgs -NoNewWindow -PassThru
        Write-Host "✅ Dashboard started with PID: $($process.Id)" -ForegroundColor Green
        Write-Host "🌐 Dashboard URL: http://localhost:$Port" -ForegroundColor Cyan
        Write-Host "💡 Process is running in background" -ForegroundColor Yellow
        return $process
    }
    catch {
        Write-Host "❌ Failed to start dashboard: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

function Stop-DashboardProcess {
    Write-Host "🛑 Stopping Codex Dashboard processes..." -ForegroundColor Yellow

    $processes = Get-Process | Where-Object {
        $_.ProcessName -eq "python" -and
        $_.CommandLine -like "*streamlit*" -and
        $_.CommandLine -like "*$StreamlitScript*"
    }

    if ($processes) {
        $processes | ForEach-Object {
            Write-Host "Stopping process PID: $($_.Id)" -ForegroundColor White
            $_ | Stop-Process -Force
        }
        Write-Host "✅ Dashboard processes stopped" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No running dashboard processes found" -ForegroundColor Yellow
    }
}

function Get-DashboardStatus {
    Write-Host "📊 Codex Dashboard Status:" -ForegroundColor Cyan

    # Check for running processes
    $processes = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like "*streamlit*" -and $_.CommandLine -like "*$StreamlitScript*"
    }

    if ($processes) {
        Write-Host "   Status: RUNNING" -ForegroundColor Green
        $processes | ForEach-Object {
            Write-Host "   PID: $($_.Id) | Started: $($_.StartTime)" -ForegroundColor White
        }

        # Test if port is responding
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
            Write-Host "🌐 Dashboard URL: http://localhost:$Port" -ForegroundColor Green
            Write-Host "✅ Dashboard is responding!" -ForegroundColor Green
        }
        catch {
            Write-Host "⚠️  Dashboard process running but not responding on port $Port" -ForegroundColor Yellow
            Write-Host "🌐 Expected URL: http://localhost:$Port" -ForegroundColor Cyan
        }
    } else {
        Write-Host "   Status: STOPPED" -ForegroundColor Red
        Write-Host "💡 Use 'start' to launch the dashboard" -ForegroundColor Yellow
    }

    # Show port usage
    $portCheck = netstat -an | Select-String ":$Port "
    if ($portCheck) {
        Write-Host "   Port $Port: IN USE" -ForegroundColor Green
    } else {
        Write-Host "   Port $Port: AVAILABLE" -ForegroundColor Yellow
    }
}

function Install-WindowsService {
    Write-Host "🔧 Windows Service Installation Info:" -ForegroundColor Cyan
    Write-Host "   For full Windows service installation, you need NSSM:" -ForegroundColor White
    Write-Host "   1. Download NSSM from: https://nssm.cc/download" -ForegroundColor White
    Write-Host "   2. Extract nssm.exe to your PATH" -ForegroundColor White
    Write-Host "   3. Run as Administrator:" -ForegroundColor White
    Write-Host "      nssm install $ServiceName" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 For now, using direct process management" -ForegroundColor Cyan
}

# Main execution
switch ($Action.ToLower()) {
    "install" {
        Install-WindowsService
        Get-DashboardStatus
    }
    "start" {
        Start-DashboardProcess
        Start-Sleep 2
        Get-DashboardStatus
    }
    "stop" {
        Stop-DashboardProcess
        Get-DashboardStatus
    }
    "restart" {
        Stop-DashboardProcess
        Start-Sleep 2
        Start-DashboardProcess
        Start-Sleep 2
        Get-DashboardStatus
    }
    "status" {
        Get-DashboardStatus
    }
    "uninstall" {
        Stop-DashboardProcess
        Write-Host "✅ Dashboard processes stopped (uninstalled)" -ForegroundColor Green
    }
    default {
        Write-Host "Usage: .\service-manager.ps1 [install|start|stop|restart|status|uninstall]" -ForegroundColor Yellow
        Get-DashboardStatus
    }
}

Write-Host ""
Write-Host "🔥 Codex Dashboard Management Complete!" -ForegroundColor Yellow
