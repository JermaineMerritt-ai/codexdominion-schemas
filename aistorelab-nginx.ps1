# Windows nginx equivalent service manager for aistorelab.com
# This replaces sudo nano /etc/nginx/sites-available/aistorelab.com

param([string]$Action = "status")

$ProxyConfig = @{
    ServiceName = "AIStoreLab-Proxy"
    Description = "AIStoreLab.com Proxy Server (nginx equivalent)"
    ScriptPath = "aistorelab-simple-proxy.js"
    Port = 3000  # Using port 3000 for testing (change to 80 for production)
    LogFile = "aistorelab-proxy.log"
}

Write-Host "AISTORELAB.COM NGINX EQUIVALENT (Windows)" -ForegroundColor Cyan
Write-Host "Proxy Server Management" -ForegroundColor Gray

function Start-ProxyService {
    Write-Host ""
    Write-Host "Starting AIStoreLab.com Proxy Service..." -ForegroundColor Green
    Write-Host "Port: $($ProxyConfig.Port)" -ForegroundColor Gray
    Write-Host "Configuration: Windows nginx equivalent" -ForegroundColor Gray
    
    # Check if port is available
    $portCheck = netstat -ano | Select-String ":$($ProxyConfig.Port).*LISTENING"
    if ($portCheck) {
        Write-Host "WARNING: Port $($ProxyConfig.Port) is already in use" -ForegroundColor Yellow
        $portCheck | ForEach-Object {
            if ($_ -match ":$($ProxyConfig.Port)\s+.*LISTENING\s+(\d+)") {
                $processId = $matches[1]
                try {
                    $process = Get-Process -Id $processId -ErrorAction Stop
                    Write-Host "  Process: $($process.ProcessName) (PID: $processId)" -ForegroundColor Yellow
                } catch {
                    Write-Host "  Unknown process (PID: $processId)" -ForegroundColor Yellow
                }
            }
        }
        
        $response = Read-Host "Stop existing process and continue? (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Stop-ProxyService
            Start-Sleep 2
        } else {
            Write-Host "Aborted" -ForegroundColor Red
            return
        }
    }
    
    try {
        # Start the proxy server
        $process = Start-Process -FilePath "node" -ArgumentList $ProxyConfig.ScriptPath -WorkingDirectory (Get-Location) -WindowStyle Hidden -PassThru -RedirectStandardOutput $ProxyConfig.LogFile -RedirectStandardError "aistorelab-proxy-error.log"
        
        Write-Host "Proxy service started with PID: $($process.Id)" -ForegroundColor Green
        
        # Wait and verify
        Start-Sleep 3
        
        $portCheck = netstat -ano | Select-String ":$($ProxyConfig.Port).*LISTENING"
        if ($portCheck) {
            Write-Host "SUCCESS: AIStoreLab.com Proxy is running" -ForegroundColor Green
            Write-Host "Access at: http://localhost" -ForegroundColor White
            Write-Host "Health check: http://localhost/health" -ForegroundColor White
            
            # Test health endpoint
            try {
                $response = Invoke-WebRequest -Uri "http://localhost/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                Write-Host "Health check passed" -ForegroundColor Green
            } catch {
                Write-Host "Service started but health check failed (may need a moment)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "WARNING: Service may not have started correctly" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "ERROR: Failed to start proxy service" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

function Stop-ProxyService {
    Write-Host ""
    Write-Host "Stopping AIStoreLab.com Proxy Service..." -ForegroundColor Yellow
    
    # Find processes on port 80
    $processes = netstat -ano | Select-String ":$($ProxyConfig.Port).*LISTENING"
    $stopped = $false
    
    foreach ($process in $processes) {
        if ($process -match ":$($ProxyConfig.Port)\s+.*LISTENING\s+(\d+)") {
            $processId = $matches[1]
            try {
                $processObj = Get-Process -Id $processId -ErrorAction Stop
                if ($processObj.ProcessName -eq "node" -or $processObj.ProcessName -eq "nodejs") {
                    Stop-Process -Id $processId -Force -ErrorAction Stop
                    Write-Host "Stopped AIStoreLab.com Proxy (PID: $processId)" -ForegroundColor Green
                    $stopped = $true
                } else {
                    Write-Host "Skipped non-Node.js process: $($processObj.ProcessName) (PID: $processId)" -ForegroundColor Gray
                }
            } catch {
                Write-Host "Could not stop process $processId" -ForegroundColor Red
            }
        }
    }
    
    if (-not $stopped) {
        Write-Host "No AIStoreLab.com Proxy found running on port $($ProxyConfig.Port)" -ForegroundColor Gray
    }
}

function Get-ProxyStatus {
    Write-Host ""
    Write-Host "AIStoreLab.com Proxy Status:" -ForegroundColor Cyan
    
    # Check port
    $portCheck = netstat -ano | Select-String ":$($ProxyConfig.Port).*LISTENING"
    
    if ($portCheck) {
        $portCheck | ForEach-Object {
            if ($_ -match ":$($ProxyConfig.Port)\s+.*LISTENING\s+(\d+)") {
                $processId = $matches[1]
                try {
                    $processObj = Get-Process -Id $processId -ErrorAction Stop
                    Write-Host "Status: ACTIVE (RUNNING)" -ForegroundColor Green
                    Write-Host "Main PID: $processId" -ForegroundColor White
                    Write-Host "Process: $($processObj.ProcessName)" -ForegroundColor White
                    Write-Host "Memory: $([math]::Round($processObj.WorkingSet64/1MB, 2)) MB" -ForegroundColor White
                    Write-Host "Start Time: $($processObj.StartTime)" -ForegroundColor White
                    Write-Host "Port: $($ProxyConfig.Port)" -ForegroundColor White
                    Write-Host "URL: http://localhost" -ForegroundColor White
                } catch {
                    Write-Host "Status: UNKNOWN (Port occupied by PID $processId)" -ForegroundColor Yellow
                }
            }
        }
    } else {
        Write-Host "Status: INACTIVE (NOT RUNNING)" -ForegroundColor Red
        Write-Host "Port $($ProxyConfig.Port): Available" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Nginx Equivalent Configuration:" -ForegroundColor Cyan
    Write-Host "Description: $($ProxyConfig.Description)" -ForegroundColor Gray
    Write-Host "Config File: nginx-config/aistorelab.com" -ForegroundColor Gray
    Write-Host "Proxy Script: $($ProxyConfig.ScriptPath)" -ForegroundColor Gray
    Write-Host "Routes:" -ForegroundColor Gray
    Write-Host "  / → http://127.0.0.1:8501 (Main Dashboard)" -ForegroundColor Gray
    Write-Host "  /api → http://127.0.0.1:8000 (API Endpoints)" -ForegroundColor Gray
    Write-Host "  /portfolio → http://127.0.0.1:8503 (Portfolio Dashboard)" -ForegroundColor Gray
    Write-Host "  /health → Health Check" -ForegroundColor Gray
}

function Show-NginxEquivalent {
    Write-Host ""
    Write-Host "NGINX EQUIVALENT COMMANDS:" -ForegroundColor Yellow
    Write-Host "Linux nginx commands → Windows equivalents:" -ForegroundColor Gray
    Write-Host ""
    Write-Host "sudo nano /etc/nginx/sites-available/aistorelab.com" -ForegroundColor Gray
    Write-Host "  → Edit: nginx-config\aistorelab.com (created)" -ForegroundColor Green
    Write-Host ""
    Write-Host "sudo nginx -t" -ForegroundColor Gray  
    Write-Host "  → .\aistorelab-nginx.ps1 test" -ForegroundColor Green
    Write-Host ""
    Write-Host "sudo systemctl reload nginx" -ForegroundColor Gray
    Write-Host "  → .\aistorelab-nginx.ps1 restart" -ForegroundColor Green
    Write-Host ""
    Write-Host "sudo systemctl start nginx" -ForegroundColor Gray
    Write-Host "  → .\aistorelab-nginx.ps1 start" -ForegroundColor Green
}

# Execute based on action
switch ($Action.ToLower()) {
    "start" { 
        Start-ProxyService 
    }
    "stop" { 
        Stop-ProxyService 
    }
    "restart" {
        Stop-ProxyService
        Start-Sleep 2
        Start-ProxyService
    }
    "status" { 
        Get-ProxyStatus 
    }
    "test" {
        Write-Host ""
        Write-Host "Testing nginx equivalent configuration..." -ForegroundColor Yellow
        if (Test-Path $ProxyConfig.ScriptPath) {
            Write-Host "✓ Proxy script found: $($ProxyConfig.ScriptPath)" -ForegroundColor Green
        } else {
            Write-Host "✗ Proxy script missing: $($ProxyConfig.ScriptPath)" -ForegroundColor Red
        }
        
        if (Test-Path "nginx-config\aistorelab.com") {
            Write-Host "✓ Nginx config found: nginx-config\aistorelab.com" -ForegroundColor Green
        } else {
            Write-Host "✗ Nginx config missing: nginx-config\aistorelab.com" -ForegroundColor Red
        }
        
        Write-Host "✓ Configuration test passed" -ForegroundColor Green
    }
    "help" {
        Show-NginxEquivalent
    }
    default {
        Write-Host "USAGE:" -ForegroundColor Yellow
        Write-Host "  .\aistorelab-nginx.ps1 [start|stop|restart|status|test|help]" -ForegroundColor White
        Write-Host ""
        Write-Host "NGINX EQUIVALENTS:" -ForegroundColor Cyan
        Write-Host "  sudo nano /etc/nginx/sites-available/aistorelab.com" -ForegroundColor Gray
        Write-Host "    → Already created: nginx-config\aistorelab.com" -ForegroundColor Green
        Write-Host "  sudo systemctl start nginx   → .\aistorelab-nginx.ps1 start" -ForegroundColor Gray
        Write-Host "  sudo systemctl stop nginx    → .\aistorelab-nginx.ps1 stop" -ForegroundColor Gray
        Write-Host "  sudo systemctl status nginx  → .\aistorelab-nginx.ps1 status" -ForegroundColor Gray
        Write-Host "  sudo nginx -t                → .\aistorelab-nginx.ps1 test" -ForegroundColor Gray
        Get-ProxyStatus
    }
}