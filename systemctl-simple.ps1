# Simple systemctl simulation for Windows
param([string]$Command, [string]$Service = "codex-dashboard")

$Port = 8095

Write-Host ""
Write-Host "SYSTEMCTL SIMULATION - CODEX DASHBOARD" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Yellow

switch ($Command) {
    "daemon-reload" {
        Write-Host "Reloading systemd daemon..." -ForegroundColor Cyan
        Write-Host "Daemon reloaded successfully" -ForegroundColor Green
    }
    
    "enable" {
        Write-Host "Enabling $Service service..." -ForegroundColor Cyan
        Write-Host "Service enabled for automatic startup" -ForegroundColor Green
    }
    
    "start" {
        Write-Host "Starting $Service service..." -ForegroundColor Cyan
        
        # Start the dashboard
        $args = @("-m", "streamlit", "run", "app.py", "--server.port", $Port, "--server.headless", "true")
        $process = Start-Process -FilePath "python" -ArgumentList $args -NoNewWindow -PassThru
        
        Start-Sleep 3
        Write-Host "Service started successfully" -ForegroundColor Green
        Write-Host "Process ID: $($process.Id)" -ForegroundColor White
        Write-Host "Dashboard URL: http://localhost:$Port" -ForegroundColor Cyan
    }
    
    "status" {
        Write-Host "$Service.service - Codex Dashboard" -ForegroundColor Cyan
        
        $portInUse = netstat -an | Select-String ":$Port.*LISTENING"
        
        if ($portInUse) {
            Write-Host "Active: RUNNING" -ForegroundColor Green
            Write-Host "Status: Dashboard operational on port $Port" -ForegroundColor Green
            Write-Host "URL: http://localhost:$Port" -ForegroundColor Cyan
        } else {
            Write-Host "Active: STOPPED" -ForegroundColor Red  
            Write-Host "Status: Service not running" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "Usage: systemctl-simple.ps1 {daemon-reload|enable|start|status}"
        Write-Host "Available commands:"
        Write-Host "  daemon-reload  - Reload configuration"
        Write-Host "  enable        - Enable service"  
        Write-Host "  start         - Start service"
        Write-Host "  status        - Show status"
    }
}

Write-Host ""