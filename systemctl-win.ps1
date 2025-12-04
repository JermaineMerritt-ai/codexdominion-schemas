# PowerShell systemctl simulation
param(
    [Parameter(Position=0)][string]$Command,
    [Parameter(Position=1)][string]$Service = "codex-dashboard"
)

$Port = 8095
$Script = "app.py"

Write-Host ""
Write-Host "🔥 SYSTEMCTL SIMULATION - CODEX DASHBOARD" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Yellow

switch ($Command) {
    "daemon-reload" {
        Write-Host "🔄 Reloading systemd daemon..." -ForegroundColor Cyan
        Start-Sleep 1
        Write-Host "✅ Daemon reloaded successfully" -ForegroundColor Green
    }

    "enable" {
        Write-Host "⚡ Enabling $Service service..." -ForegroundColor Cyan
        Write-Host "Created symlink /etc/systemd/system/multi-user.target.wants/codex-dashboard.service → /etc/systemd/system/codex-dashboard.service" -ForegroundColor White
        Write-Host "✅ Service enabled" -ForegroundColor Green
    }

    "start" {
        Write-Host "🚀 Starting $Service service..." -ForegroundColor Cyan

        # Start the dashboard
        $ProcessArgs = @("-m", "streamlit", "run", $Script, "--server.port", $Port, "--server.headless", "true")
        $Process = Start-Process -FilePath "python" -ArgumentList $ProcessArgs -NoNewWindow -PassThru

        Start-Sleep 3
        Write-Host "✅ Service started successfully" -ForegroundColor Green
        Write-Host "   Process ID: $($Process.Id)" -ForegroundColor White
    }

    "status" {
        Write-Host "📊 $Service.service - Codex Dashboard Digital Sovereignty Interface" -ForegroundColor Cyan
        Write-Host "   Loaded: loaded (/etc/systemd/system/codex-dashboard.service; enabled; vendor preset: enabled)" -ForegroundColor White

        # Check if port is listening
        $PortCheck = netstat -an | Select-String ":$Port.*LISTENING"

        if ($PortCheck) {
            $CurrentTime = Get-Date -Format "ddd yyyy-MM-dd HH:mm:ss"
            Write-Host "   Active: active (running) since $CurrentTime" -ForegroundColor Green
            Write-Host "     Docs: man:streamlit(1)" -ForegroundColor White

            # Find streamlit process
            $StreamlitProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {
                $_.CommandLine -like "*streamlit*" -and $_.CommandLine -like "*$Script*"
            }

            if ($StreamlitProcess) {
                Write-Host "  Process: $($StreamlitProcess.Id) (streamlit)" -ForegroundColor White
                Write-Host "     Main PID: $($StreamlitProcess.Id) (python)" -ForegroundColor White
            }

            Write-Host "    Status: ✅ Dashboard operational on port $Port" -ForegroundColor Green
            Write-Host "      URL: http://localhost:$Port" -ForegroundColor Cyan
        } else {
            Write-Host "   Active: inactive (dead)" -ForegroundColor Red
            Write-Host "    Status: ❌ Service not running" -ForegroundColor Red
        }
    }

    default {
        Write-Host "Usage: .\systemctl-win.ps1 {daemon-reload|enable|start|status} [service-name]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "systemctl commands:" -ForegroundColor White
        Write-Host "  daemon-reload              Reload systemd manager configuration" -ForegroundColor White
        Write-Host "  enable codex-dashboard     Enable service to start on boot" -ForegroundColor White
        Write-Host "  start codex-dashboard      Start the service" -ForegroundColor White
        Write-Host "  status codex-dashboard     Show service status" -ForegroundColor White
        return
    }
}

Write-Host ""
Write-Host "🔥 Command completed successfully!" -ForegroundColor Yellow
Write-Host ""
