# Codex Dashboard Windows Service Management
# PowerShell script to manage Codex Dashboard as Windows service

param(
    [Parameter(Position=0)]
    [ValidateSet("install", "start", "stop", "restart", "status", "uninstall", "logs")]
    [string]$Action = "status"
)

$ServiceName = "CodexDashboard"
$ServiceDisplayName = "Codex Dashboard - Digital Sovereignty Interface"
$ServiceDescription = "Streamlit dashboard for Codex Dominion digital sovereignty system"
$WorkingDirectory = Get-Location
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
$StreamlitScript = "app.py"  # Using the streamlined dashboard
$Port = 8095

Write-Host "🔥 CODEX DASHBOARD SERVICE MANAGEMENT" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Install-Service {
    Write-Host "🚀 Installing Codex Dashboard Service..." -ForegroundColor Green
    
    if (-not (Test-Administrator)) {
        Write-Host "❌ Administrator privileges required for service installation!" -ForegroundColor Red
        Write-Host "💡 Run PowerShell as Administrator and try again." -ForegroundColor Yellow
        return
    }
    
    # Check if NSSM is available
    $nssm = Get-Command nssm -ErrorAction SilentlyContinue
    if (-not $nssm) {
        Write-Host "⚠️  NSSM not found. Installing NSSM..." -ForegroundColor Yellow
        # You can download NSSM from https://nssm.cc/download
        Write-Host "📦 Please download NSSM from: https://nssm.cc/download" -ForegroundColor Cyan
        Write-Host "   Extract nssm.exe to your PATH or current directory" -ForegroundColor Cyan
        return
    }
    
    # Install service
    $Arguments = "-m streamlit run `"$StreamlitScript`" --server.port $Port --server.headless true"
    
    & nssm install $ServiceName $PythonPath $Arguments
    & nssm set $ServiceName DisplayName $ServiceDisplayName
    & nssm set $ServiceName Description $ServiceDescription
    & nssm set $ServiceName AppDirectory $WorkingDirectory
    & nssm set $ServiceName Start SERVICE_AUTO_START
    
    Write-Host "✅ Service installed successfully!" -ForegroundColor Green
    Write-Host "🎯 Service Name: $ServiceName" -ForegroundColor Cyan
    Write-Host "🌐 Dashboard URL: http://localhost:$Port" -ForegroundColor Cyan
}

function Start-DashboardService {
    Write-Host "🔥 Starting Codex Dashboard Service..." -ForegroundColor Green
    try {
        Start-Service -Name $ServiceName -ErrorAction Stop
        Write-Host "✅ Service started successfully!" -ForegroundColor Green
        Start-Sleep 3
        Get-ServiceStatus
    }
    catch {
        Write-Host "❌ Failed to start service: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Stop-DashboardService {
    Write-Host "🛑 Stopping Codex Dashboard Service..." -ForegroundColor Yellow
    try {
        Stop-Service -Name $ServiceName -ErrorAction Stop
        Write-Host "✅ Service stopped successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to stop service: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Restart-DashboardService {
    Write-Host "🔄 Restarting Codex Dashboard Service..." -ForegroundColor Yellow
    Stop-DashboardService
    Start-Sleep 2
    Start-DashboardService
}

function Get-ServiceStatus {
    Write-Host "📊 Codex Dashboard Service Status:" -ForegroundColor Cyan
    
    try {
        $service = Get-Service -Name $ServiceName -ErrorAction Stop
        $status = $service.Status
        $startType = (Get-WmiObject -Query "SELECT StartMode FROM Win32_Service WHERE Name='$ServiceName'").StartMode
        
        Write-Host "   Service Name: $ServiceName" -ForegroundColor White
        Write-Host "   Display Name: $($service.DisplayName)" -ForegroundColor White
        Write-Host "   Status: $status" -ForegroundColor $(if ($status -eq 'Running') { 'Green' } else { 'Red' })
        Write-Host "   Start Type: $startType" -ForegroundColor White
        
        if ($status -eq 'Running') {
            Write-Host "🌐 Dashboard URL: http://localhost:$Port" -ForegroundColor Green
            
            # Test if port is responding
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 5 -ErrorAction Stop
                Write-Host "✅ Dashboard is responding!" -ForegroundColor Green
            }
            catch {
                Write-Host "⚠️  Dashboard service running but not responding on port $Port" -ForegroundColor Yellow
            }
        }
    }
    catch {
        Write-Host "❌ Service not found: $ServiceName" -ForegroundColor Red
        Write-Host "💡 Run 'install' to create the service first." -ForegroundColor Yellow
    }
}

function Uninstall-Service {
    Write-Host "🗑️  Uninstalling Codex Dashboard Service..." -ForegroundColor Red
    
    if (-not (Test-Administrator)) {
        Write-Host "❌ Administrator privileges required!" -ForegroundColor Red
        return
    }
    
    try {
        Stop-Service -Name $ServiceName -ErrorAction SilentlyContinue
        & nssm remove $ServiceName confirm
        Write-Host "✅ Service uninstalled successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to uninstall service: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Get-ServiceLogs {
    Write-Host "📋 Recent Codex Dashboard Service Logs:" -ForegroundColor Cyan
    
    # Check Windows Event Log
    try {
        $events = Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Service Control Manager'} -MaxEvents 10 | 
                  Where-Object { $_.Message -like "*$ServiceName*" }
        
        if ($events) {
            $events | ForEach-Object {
                Write-Host "[$($_.TimeCreated)] $($_.LevelDisplayName): $($_.Message)" -ForegroundColor White
            }
        } else {
            Write-Host "No recent events found for $ServiceName" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "❌ Could not retrieve event logs: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Main execution
switch ($Action.ToLower()) {
    "install" { Install-Service }
    "start" { Start-DashboardService }
    "stop" { Stop-DashboardService }
    "restart" { Restart-DashboardService }
    "status" { Get-ServiceStatus }
    "uninstall" { Uninstall-Service }
    "logs" { Get-ServiceLogs }
    default { 
        Write-Host "Usage: .\windows-service-management.ps1 [install|start|stop|restart|status|uninstall|logs]" -ForegroundColor Yellow
        Get-ServiceStatus
    }
}

Write-Host ""
Write-Host "🔥 Codex Dashboard Service Management Complete!" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow