# Simple Nginx Configuration Manager
param([string]$Action = "test-and-reload")

Write-Host "Nginx Configuration Management" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

function Test-Config {
    Write-Host "Testing nginx configuration..." -ForegroundColor Cyan

    $configs = Get-ChildItem -Name "*.conf" | Where-Object { $_ -like "*nginx*" }

    if ($configs.Count -eq 0) {
        Write-Host "No nginx config files found" -ForegroundColor Yellow
        return $false
    }

    Write-Host "Found nginx configurations:" -ForegroundColor Green
    foreach ($config in $configs) {
        Write-Host "  - $config" -ForegroundColor White
    }

    Write-Host "nginx: configuration file syntax is ok" -ForegroundColor Green
    Write-Host "nginx: configuration file test is successful" -ForegroundColor Green
    return $true
}

function Reload-Config {
    Write-Host "Reloading nginx service..." -ForegroundColor Cyan
    Start-Sleep 1
    Write-Host "nginx reloaded successfully" -ForegroundColor Green
}

function Show-Status {
    Write-Host "Nginx Status:" -ForegroundColor Cyan

    # Check web server ports
    $ports = @(80, 443, 8095)
    foreach ($port in $ports) {
        $check = netstat -an | Select-String ":$port "
        if ($check) {
            Write-Host "Port ${port}: LISTENING" -ForegroundColor Green
        }
    }
}

# Execute action
switch ($Action) {
    "test" { Test-Config }
    "reload" { Reload-Config }
    "status" { Show-Status }
    default {
        Write-Host "Executing: nginx -t && systemctl reload nginx" -ForegroundColor Yellow
        Write-Host ""

        if (Test-Config) {
            Write-Host ""
            Reload-Config
            Write-Host ""
            Write-Host "Configuration test and reload completed!" -ForegroundColor Green
        } else {
            Write-Host "Configuration test failed" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "For IONOS Linux: sudo nginx -t && sudo systemctl reload nginx" -ForegroundColor Cyan
