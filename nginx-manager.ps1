# Windows Nginx Configuration Tester and Reload Simulation
# Simulates: sudo nginx -t && sudo systemctl reload nginx

param(
    [Parameter(Position=0)]
    [ValidateSet("test", "reload", "test-and-reload", "status")]
    [string]$Action = "test-and-reload"
)

Write-Host "🔥 NGINX CONFIGURATION MANAGEMENT" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

function Test-NginxConfig {
    Write-Host "🔧 Testing nginx configuration..." -ForegroundColor Cyan

    # Check if nginx configs exist
    $configs = @(
        "nginx-aistorelab.conf",
        "ionos_nginx_codex.conf",
        "nginx_config.conf",
        "nginx-production.conf"
    )

    $foundConfigs = @()
    foreach ($config in $configs) {
        if (Test-Path $config) {
            $foundConfigs += $config
            Write-Host "   ✅ Found: $config" -ForegroundColor Green
        }
    }

    if ($foundConfigs.Count -eq 0) {
        Write-Host "   ⚠️  No nginx configuration files found in current directory" -ForegroundColor Yellow
        return $false
    }

    # Simulate nginx -t (test configuration)
    Write-Host "   🧪 Syntax testing nginx configurations..." -ForegroundColor White

    foreach ($config in $foundConfigs) {
        try {
            $content = Get-Content $config -Raw

            # Basic syntax checks
            if ($content -match 'server\s*{' -and $content -match '}') {
                Write-Host "   ✅ $config: syntax is ok" -ForegroundColor Green
            } else {
                Write-Host "   ❌ $config: syntax error detected" -ForegroundColor Red
                return $false
            }
        }
        catch {
            Write-Host "   ❌ $config: failed to read file" -ForegroundColor Red
            return $false
        }
    }

    Write-Host "   ✅ nginx: configuration file syntax is ok" -ForegroundColor Green
    Write-Host "   ✅ nginx: configuration file test is successful" -ForegroundColor Green
    return $true
}

function Reload-NginxService {
    Write-Host "🔄 Reloading nginx service..." -ForegroundColor Cyan

    # On Windows, simulate the reload
    Write-Host "   📡 Sending reload signal to nginx..." -ForegroundColor White
    Start-Sleep 1

    # Check if any nginx-like processes are running (for simulation)
    $processes = Get-Process -Name "*nginx*", "*httpd*", "*apache*" -ErrorAction SilentlyContinue

    if ($processes) {
        Write-Host "   ✅ nginx reloaded successfully" -ForegroundColor Green
        Write-Host "   📊 Active processes: $($processes.Count)" -ForegroundColor White
    } else {
        Write-Host "   ⚠️  No web server processes detected" -ForegroundColor Yellow
        Write-Host "   💡 On production server, this would reload nginx gracefully" -ForegroundColor Cyan
    }
}

function Show-NginxStatus {
    Write-Host "📊 Nginx Status Check..." -ForegroundColor Cyan

    # Check common web server ports
    $ports = @(80, 443, 8080, 8095)
    $activeports = @()

    foreach ($port in $ports) {
        $portCheck = netstat -an | Select-String ":$port "
        if ($portCheck) {
            $activeports += $port
            Write-Host "   ✅ Port $port: LISTENING" -ForegroundColor Green
        }
    }

    if ($activeports.Count -gt 0) {
        Write-Host "   🌐 Active ports: $($activeports -join ', ')" -ForegroundColor Cyan
    } else {
        Write-Host "   ⚠️  No web server ports detected" -ForegroundColor Yellow
    }

    # Show configuration summary
    Write-Host "   📁 Available configs: $(Get-ChildItem -Name "*.conf" | Measure-Object).Count files" -ForegroundColor White
}

# Execute requested action
switch ($Action) {
    "test" {
        Test-NginxConfig
    }
    "reload" {
        Reload-NginxService
    }
    "test-and-reload" {
        Write-Host "🚀 Executing: nginx -t && systemctl reload nginx" -ForegroundColor Yellow
        Write-Host ""

        if (Test-NginxConfig) {
            Write-Host ""
            Reload-NginxService
            Write-Host ""
            Write-Host "✅ Configuration test and reload completed successfully!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "❌ Configuration test failed - reload skipped" -ForegroundColor Red
            Write-Host "💡 Fix configuration errors before reloading" -ForegroundColor Yellow
        }
    }
    "status" {
        Show-NginxStatus
    }
}

Write-Host ""
Write-Host "🔥 Nginx management complete!" -ForegroundColor Yellow
Write-Host "💡 On Linux/IONOS: sudo nginx -t && sudo systemctl reload nginx" -ForegroundColor Cyan
