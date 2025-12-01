# 🚀 CODEX DASHBOARD SERVICE MANAGEMENT (Windows Testing)
# PowerShell equivalent for systemctl commands

param(
    [Parameter()]
    [ValidateSet("status", "enabled", "start", "stop", "restart", "install", "uninstall")]
    [string]$Action = "status"
)

# Colors for output
function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    switch ($Color) {
        "Red" { Write-Host $Text -ForegroundColor Red }
        "Green" { Write-Host $Text -ForegroundColor Green }
        "Yellow" { Write-Host $Text -ForegroundColor Yellow }
        "Blue" { Write-Host $Text -ForegroundColor Blue }
        "Cyan" { Write-Host $Text -ForegroundColor Cyan }
        "Magenta" { Write-Host $Text -ForegroundColor Magenta }
        default { Write-Host $Text }
    }
}

function Write-Header {
    param([string]$Title)
    Write-ColorText "`n🚀 $Title" "Cyan"
    Write-ColorText ("=" * ($Title.Length + 4)) "Cyan"
}

# Configuration
$ServiceName = "CodexDashboard"
$DisplayName = "Codex Dashboard - Digital Sovereignty Platform"
$WorkingDir = "C:\codex-dominion"
$PythonScript = "$WorkingDir\sovereignty_dashboard.py"
$Port = 8095

Write-Header "CODEX DASHBOARD SERVICE MANAGEMENT"

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Service status check function
function Get-ServiceStatus {
    Write-ColorText "`n📊 Checking Windows Service Status..." "Yellow"
    
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    
    if ($service) {
        Write-ColorText "✅ Service found: $($service.DisplayName)" "Green"
        Write-ColorText "   Status: $($service.Status)" "Cyan"
        Write-ColorText "   Start Type: $((Get-WmiObject -Class Win32_Service -Filter "Name='$ServiceName'").StartMode)" "Cyan"
        
        # Check if service is set to start automatically (equivalent to is-enabled)
        $startMode = (Get-WmiObject -Class Win32_Service -Filter "Name='$ServiceName'").StartMode
        if ($startMode -eq "Auto") {
            Write-ColorText "✅ Service is enabled (Auto start)" "Green"
        } else {
            Write-ColorText "⚠️ Service start mode: $startMode" "Yellow"
        }
    } else {
        Write-ColorText "❌ Service '$ServiceName' not found" "Red"
        Write-ColorText "💡 Use -Action install to create the service" "Yellow"
    }
    
    # Test connectivity
    Write-ColorText "`n🌐 Testing Dashboard Connectivity..." "Yellow"
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-ColorText "✅ Dashboard responding on port $Port" "Green"
        } else {
            Write-ColorText "⚠️ Dashboard returned status code: $($response.StatusCode)" "Yellow"
        }
    } catch {
        Write-ColorText "❌ Dashboard not responding on port $Port" "Red"
        Write-ColorText "   Error: $($_.Exception.Message)" "Red"
    }
    
    # Show process information
    Write-ColorText "`n💻 Process Information..." "Yellow"
    $processes = Get-Process | Where-Object { $_.ProcessName -like "*python*" -and $_.CommandLine -like "*sovereignty_dashboard*" } -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-ColorText "   🔥 PID: $($proc.Id)" "Cyan"
            Write-ColorText "   📈 Memory: $([math]::Round($proc.WorkingSet / 1MB, 2)) MB" "Cyan"
            Write-ColorText "   ⏱️ CPU Time: $($proc.TotalProcessorTime)" "Cyan"
        }
    } else {
        Write-ColorText "   ⚠️ No Codex Dashboard processes found" "Yellow"
    }
}

# Start service function
function Start-CodexService {
    Write-ColorText "`n🚀 Starting Codex Dashboard Service..." "Yellow"
    
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($service) {
        if ($service.Status -eq "Running") {
            Write-ColorText "✅ Service is already running" "Green"
        } else {
            try {
                Start-Service -Name $ServiceName
                Write-ColorText "✅ Service started successfully" "Green"
                
                Start-Sleep -Seconds 5
                
                # Verify it's running
                $updatedService = Get-Service -Name $ServiceName
                if ($updatedService.Status -eq "Running") {
                    Write-ColorText "✅ Service is now running" "Green"
                } else {
                    Write-ColorText "❌ Service failed to start properly" "Red"
                }
            } catch {
                Write-ColorText "❌ Failed to start service: $($_.Exception.Message)" "Red"
            }
        }
    } else {
        Write-ColorText "❌ Service not installed. Use -Action install first." "Red"
    }
}

# Stop service function
function Stop-CodexService {
    Write-ColorText "`n🛑 Stopping Codex Dashboard Service..." "Yellow"
    
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq "Running") {
        try {
            Stop-Service -Name $ServiceName -Force
            Write-ColorText "✅ Service stopped successfully" "Green"
        } catch {
            Write-ColorText "❌ Failed to stop service: $($_.Exception.Message)" "Red"
        }
    } else {
        Write-ColorText "⚠️ Service is not running or not installed" "Yellow"
    }
}

# Restart service function
function Restart-CodexService {
    Stop-CodexService
    Start-Sleep -Seconds 3
    Start-CodexService
}

# Install service function
function Install-CodexService {
    if (-not (Test-Administrator)) {
        Write-ColorText "❌ Administrator privileges required to install service" "Red"
        Write-ColorText "💡 Run PowerShell as Administrator and try again" "Yellow"
        return
    }
    
    Write-ColorText "`n📦 Installing Codex Dashboard Windows Service..." "Yellow"
    
    # Check if service already exists
    $existingService = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($existingService) {
        Write-ColorText "⚠️ Service already exists. Uninstall first if you want to reinstall." "Yellow"
        return
    }
    
    # Create service using sc.exe (Windows service control)
    $pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonExe) {
        Write-ColorText "❌ Python not found in PATH" "Red"
        return
    }
    
    $serviceBinary = "`"$pythonExe`" `"$PythonScript`""
    
    try {
        # Create the service
        $result = sc.exe create $ServiceName binPath= $serviceBinary DisplayName= $DisplayName start= auto
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "✅ Windows service created successfully" "Green"
            
            # Set service description
            sc.exe description $ServiceName "Codex Dashboard - Digital Sovereignty Platform for AI-powered analytics and ceremonial inscriptions"
            
            Write-ColorText "✅ Service '$ServiceName' installed and configured for automatic startup" "Green"
        } else {
            Write-ColorText "❌ Failed to create service. Output: $result" "Red"
        }
    } catch {
        Write-ColorText "❌ Error installing service: $($_.Exception.Message)" "Red"
    }
}

# Uninstall service function
function Uninstall-CodexService {
    if (-not (Test-Administrator)) {
        Write-ColorText "❌ Administrator privileges required to uninstall service" "Red"
        return
    }
    
    Write-ColorText "`n🗑️ Uninstalling Codex Dashboard Service..." "Yellow"
    
    # Stop service first if running
    $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq "Running") {
        Write-ColorText "🛑 Stopping service first..." "Yellow"
        Stop-Service -Name $ServiceName -Force
    }
    
    try {
        $result = sc.exe delete $ServiceName
        if ($LASTEXITCODE -eq 0) {
            Write-ColorText "✅ Service uninstalled successfully" "Green"
        } else {
            Write-ColorText "❌ Failed to uninstall service. Output: $result" "Red"
        }
    } catch {
        Write-ColorText "❌ Error uninstalling service: $($_.Exception.Message)" "Red"
    }
}

# Display commands equivalent to Linux systemctl
function Show-EquivalentCommands {
    Write-Header "LINUX SYSTEMCTL EQUIVALENT COMMANDS"
    
    Write-ColorText "`n🐧 Your Linux Commands (for IONOS server):" "Green"
    Write-ColorText "   systemctl status codex-dashboard.service" "White"
    Write-ColorText "   systemctl is-enabled codex-dashboard.service" "White"
    
    Write-ColorText "`n🪟 Windows PowerShell Equivalents:" "Blue"
    Write-ColorText "   Get-Service -Name CodexDashboard" "White"
    Write-ColorText "   .\codex-service.ps1 -Action status" "White"
    Write-ColorText "   .\codex-service.ps1 -Action enabled" "White"
    
    Write-ColorText "`n🔧 Additional Management Commands:" "Cyan"
    Write-ColorText "   Windows:" "Yellow"
    Write-ColorText "     .\codex-service.ps1 -Action start" "White"
    Write-ColorText "     .\codex-service.ps1 -Action stop" "White"
    Write-ColorText "     .\codex-service.ps1 -Action restart" "White"
    Write-ColorText "     .\codex-service.ps1 -Action install" "White"
    Write-ColorText "     .\codex-service.ps1 -Action uninstall" "White"
    
    Write-ColorText "`n   Linux:" "Yellow"
    Write-ColorText "     sudo systemctl start codex-dashboard.service" "White"
    Write-ColorText "     sudo systemctl stop codex-dashboard.service" "White"
    Write-ColorText "     sudo systemctl restart codex-dashboard.service" "White"
    Write-ColorText "     sudo systemctl enable codex-dashboard.service" "White"
    Write-ColorText "     sudo systemctl disable codex-dashboard.service" "White"
}

# Main execution based on action
switch ($Action) {
    "status" { 
        Get-ServiceStatus
        Show-EquivalentCommands
    }
    "enabled" {
        Write-ColorText "`n🔍 Checking if service is enabled..." "Yellow"
        $service = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
        if ($service) {
            $startMode = (Get-WmiObject -Class Win32_Service -Filter "Name='$ServiceName'").StartMode
            Write-ColorText "Service start mode: $startMode" "Cyan"
            if ($startMode -eq "Auto") {
                Write-ColorText "✅ enabled" "Green"
            } else {
                Write-ColorText "❌ disabled" "Red"
            }
        } else {
            Write-ColorText "❌ Service not found" "Red"
        }
    }
    "start" { Start-CodexService }
    "stop" { Stop-CodexService }
    "restart" { Restart-CodexService }
    "install" { Install-CodexService }
    "uninstall" { Uninstall-CodexService }
}

Write-ColorText "`n✨ Codex Dashboard Service Management Complete!" "Green"
Write-ColorText "🌍 Dashboard should be available at: http://localhost:$Port" "Cyan"