# Codex Dashboard Windows Service - Exact Linux systemd equivalent
# This implements your Linux systemd configuration on Windows

param([string]$Action = "run")

# Configuration matching your systemd service file
$ServiceConfig = @{
    Description = "Codex Dashboard Service"
    User = "Administrator"  # Windows equivalent of root
    WorkingDirectory = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"  # Windows equivalent of /root/codex-dashboard
    ExecStart = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe"  # Windows equivalent of /usr/bin/streamlit
    ExecArgs = @("-m", "streamlit", "run", "codex_dashboard.py", "--server.port=8501", "--server.address=127.0.0.1")
    RestartPolicy = "always"
    ServiceName = "CodexDashboard"
    Port = 8501
}

Write-Host "CODEX DASHBOARD SERVICE (Windows Implementation)" -ForegroundColor Cyan
Write-Host "Equivalent to your Linux systemd configuration:" -ForegroundColor Gray
Write-Host "[Unit] Description=$($ServiceConfig.Description)" -ForegroundColor Gray
Write-Host "[Service] ExecStart=streamlit run codex_dashboard.py --server.port=8501" -ForegroundColor Gray

Set-Location $ServiceConfig.WorkingDirectory

function Start-CodexDashboardService {
    Write-Host ""
    Write-Host "Starting Codex Dashboard Service..." -ForegroundColor Green
    Write-Host "Working Directory: $($ServiceConfig.WorkingDirectory)" -ForegroundColor Gray
    Write-Host "Port: $($ServiceConfig.Port)" -ForegroundColor Gray
    
    # Kill any existing processes on port 8501
    $existingProcesses = netstat -ano | Select-String ":8501.*LISTENING"
    foreach ($process in $existingProcesses) {
        if ($process -match ":8501\s+.*LISTENING\s+(\d+)") {
            $processId = $matches[1]
            try {
                Stop-Process -Id $processId -Force -ErrorAction Stop
                Write-Host "Stopped existing process on port 8501 (PID: $processId)" -ForegroundColor Yellow
            } catch {
                Write-Host "Could not stop process $processId" -ForegroundColor Red
            }
        }
    }
    
    # Start the service with exact parameters from your systemd file
    try {
        $process = Start-Process -FilePath $ServiceConfig.ExecStart -ArgumentList $ServiceConfig.ExecArgs -WorkingDirectory $ServiceConfig.WorkingDirectory -WindowStyle Hidden -PassThru
        
        Write-Host "Service started with PID: $($process.Id)" -ForegroundColor Green
        
        # Wait a moment and verify
        Start-Sleep 3
        
        # Check if service is running
        $portCheck = netstat -ano | Select-String ":8501.*LISTENING"
        if ($portCheck) {
            Write-Host "SUCCESS: Codex Dashboard Service is running" -ForegroundColor Green
            Write-Host "Access at: http://127.0.0.1:8501" -ForegroundColor White
            
            # Test connectivity
            try {
                Invoke-WebRequest -Uri "http://127.0.0.1:8501" -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop | Out-Null
                Write-Host "Web interface is accessible" -ForegroundColor Green
            } catch {
                Write-Host "Service started but web interface not ready yet (may take a moment)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "WARNING: Service may not have started correctly" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "ERROR: Failed to start service" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

function Stop-CodexDashboardService {
    Write-Host ""
    Write-Host "Stopping Codex Dashboard Service..." -ForegroundColor Yellow
    
    # Find processes on port 8501
    $processes = netstat -ano | Select-String ":8501.*LISTENING"
    $stopped = $false
    
    foreach ($process in $processes) {
        if ($process -match ":8501\s+.*LISTENING\s+(\d+)") {
            $processId = $matches[1]
            try {
                Get-Process -Id $processId -ErrorAction Stop | Out-Null
                Stop-Process -Id $processId -Force -ErrorAction Stop
                Write-Host "Stopped Codex Dashboard Service (PID: $processId)" -ForegroundColor Green
                $stopped = $true
            } catch {
                Write-Host "Could not stop process $processId" -ForegroundColor Red
            }
        }
    }
    
    if (-not $stopped) {
        Write-Host "No Codex Dashboard Service found running on port 8501" -ForegroundColor Gray
    }
}

function Get-CodexDashboardStatus {
    Write-Host ""
    Write-Host "Codex Dashboard Service Status:" -ForegroundColor Cyan
    
    # Check port 8501
    $portCheck = netstat -ano | Select-String ":8501.*LISTENING"
    
    if ($portCheck) {
        $portCheck | ForEach-Object {
            if ($_ -match ":8501\s+.*LISTENING\s+(\d+)") {
                $processId = $matches[1]
                try {
                    $processObj = Get-Process -Id $processId -ErrorAction Stop
                    Write-Host "Status: ACTIVE (RUNNING)" -ForegroundColor Green
                    Write-Host "Main PID: $processId" -ForegroundColor White
                    Write-Host "Memory Usage: $([math]::Round($processObj.WorkingSet64/1MB, 2)) MB" -ForegroundColor White
                    Write-Host "Start Time: $($processObj.StartTime)" -ForegroundColor White
                    Write-Host "Port: 8501" -ForegroundColor White
                    Write-Host "Address: http://127.0.0.1:8501" -ForegroundColor White
                } catch {
                    Write-Host "Status: UNKNOWN (Port occupied by PID $processId)" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "Status: INACTIVE (NOT RUNNING)" -ForegroundColor Red
        Write-Host "Port 8501: Available" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Service Configuration:" -ForegroundColor Cyan
    Write-Host "Description: $($ServiceConfig.Description)" -ForegroundColor Gray
    Write-Host "Working Directory: $($ServiceConfig.WorkingDirectory)" -ForegroundColor Gray
    Write-Host "Command: streamlit run codex_dashboard.py --server.port=8501 --server.address=127.0.0.1" -ForegroundColor Gray
    Write-Host "Restart Policy: $($ServiceConfig.RestartPolicy)" -ForegroundColor Gray
}

function Install-WindowsService {
    Write-Host ""
    Write-Host "Installing Codex Dashboard as Windows Service..." -ForegroundColor Cyan
    
    $servicePath = "`"powershell.exe`" -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`" run"
    
    try {
        # Create the Windows service
        sc.exe create $ServiceConfig.ServiceName binPath= $servicePath displayName= $ServiceConfig.Description start= auto
        Write-Host "Windows Service created successfully" -ForegroundColor Green
        
        # Start the service
        sc.exe start $ServiceConfig.ServiceName
        Write-Host "Service installation complete" -ForegroundColor Green
        Write-Host ""
        Write-Host "Windows Service Commands:" -ForegroundColor Cyan
        Write-Host "sc start $($ServiceConfig.ServiceName)" -ForegroundColor Gray
        Write-Host "sc stop $($ServiceConfig.ServiceName)" -ForegroundColor Gray
        Write-Host "sc query $($ServiceConfig.ServiceName)" -ForegroundColor Gray
        
    } catch {
        Write-Host "Failed to install Windows Service" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

# Execute based on action
switch ($Action.ToLower()) {
    "run" {
        # This is called when running as a Windows Service
        Start-CodexDashboardService
        
        # Keep running (simulate systemd restart=always)
        while ($true) {
            Start-Sleep 10
            
            # Check if process is still running
            $portCheck = netstat -ano | Select-String ":8501.*LISTENING"
            if (-not $portCheck) {
                Write-Host "Service stopped unexpectedly, restarting..." -ForegroundColor Yellow
                Start-CodexDashboardService
            }
        }
    }
    "start" { 
        Start-CodexDashboardService 
    }
    "stop" { 
        Stop-CodexDashboardService 
    }
    "status" { 
        Get-CodexDashboardStatus 
    }
    "restart" {
        Stop-CodexDashboardService
        Start-Sleep 2
        Start-CodexDashboardService
    }
    "install" {
        Install-WindowsService
    }
    "uninstall" {
        Write-Host "Uninstalling Windows Service..." -ForegroundColor Yellow
        sc.exe stop $ServiceConfig.ServiceName
        sc.exe delete $ServiceConfig.ServiceName
        Write-Host "Service uninstalled" -ForegroundColor Green
    }
    default {
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "  .\codex-dashboard-exact.ps1 [start|stop|restart|status|install|uninstall]" -ForegroundColor White
        Write-Host ""
        Write-Host "SYSTEMD EQUIVALENTS:" -ForegroundColor Cyan
        Write-Host "  systemctl start codex-dashboard    =>  .\codex-dashboard-exact.ps1 start" -ForegroundColor Gray
        Write-Host "  systemctl stop codex-dashboard     =>  .\codex-dashboard-exact.ps1 stop" -ForegroundColor Gray
        Write-Host "  systemctl status codex-dashboard   =>  .\codex-dashboard-exact.ps1 status" -ForegroundColor Gray
        Write-Host "  systemctl restart codex-dashboard  =>  .\codex-dashboard-exact.ps1 restart" -ForegroundColor Gray
        Write-Host "  systemctl enable codex-dashboard   =>  .\codex-dashboard-exact.ps1 install" -ForegroundColor Gray
        Get-CodexDashboardStatus
    }
}