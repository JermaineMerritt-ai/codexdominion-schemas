# CODEX DOMINION - WINDOWS SERVICE MANAGEMENT (PowerShell)
# Advanced service deployment and management for Windows environments

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("install", "start", "stop", "restart", "status", "remove")]
    [string]$Action = "status",

    [Parameter(Mandatory=$false)]
    [string]$CodexPath = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion",

    [Parameter(Mandatory=$false)]
    [string]$PythonPath = "python"
)

# Service definitions
$services = @(
    @{
        Name = "Codex-Main"
        DisplayName = "Codex Dominion - Main Dashboard"
        Description = "Main control interface for Codex Dominion digital sovereignty"
        Script = "codex_summary.py"
        Port = 8080
    },
    @{
        Name = "Codex-Contributions"
        DisplayName = "Codex Dominion - Community Contributions"
        Description = "Community interface for submitting sacred words"
        Script = "contributions.py"
        Port = 8083
    },
    @{
        Name = "Codex-Council"
        DisplayName = "Codex Dominion - Council Oversight"
        Description = "Sacred council interface for governance authority"
        Script = "enhanced_council_oversight.py"
        Port = 8086
    },
    @{
        Name = "Codex-Viewer"
        DisplayName = "Codex Dominion - Contributions Viewer"
        Description = "Public interface for viewing community contributions"
        Script = "contributions_viewer.py"
        Port = 8090
    }
)

function Write-CodexHeader {
    Write-Host "🔥 CODEX DOMINION - WINDOWS SERVICE MANAGEMENT 🔥" -ForegroundColor Yellow
    Write-Host "===================================================" -ForegroundColor Yellow
    Write-Host ""
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-NSSM {
    try {
        $null = Get-Command nssm -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

function Install-CodexServices {
    Write-Host "🚀 Installing Codex Dominion Services..." -ForegroundColor Green

    if (-not (Test-Administrator)) {
        Write-Host "❌ Administrator privileges required for service installation" -ForegroundColor Red
        return
    }

    if (-not (Test-NSSM)) {
        Write-Host "❌ NSSM not found. Please install NSSM first:" -ForegroundColor Red
        Write-Host "   Download from: https://nssm.cc/download" -ForegroundColor White
        Write-Host "   Add nssm.exe to your PATH" -ForegroundColor White
        return
    }

    # Create logs directory
    $logsPath = Join-Path $CodexPath "logs"
    if (-not (Test-Path $logsPath)) {
        New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
        Write-Host "📂 Created logs directory: $logsPath" -ForegroundColor Blue
    }

    foreach ($service in $services) {
        Write-Host "⚡ Installing $($service.DisplayName)..." -ForegroundColor Cyan

        $arguments = "-m streamlit run $($service.Script) --server.port=$($service.Port) --server.address=127.0.0.1"

        # Install service
        & nssm install $service.Name $PythonPath $arguments
        & nssm set $service.Name AppDirectory $CodexPath
        & nssm set $service.Name DisplayName $service.DisplayName
        & nssm set $service.Name Description $service.Description
        & nssm set $service.Name Start SERVICE_AUTO_START
        & nssm set $service.Name AppStdout (Join-Path $logsPath "$($service.Name.ToLower()).log")
        & nssm set $service.Name AppStderr (Join-Path $logsPath "$($service.Name.ToLower())-error.log")

        Write-Host "   ✅ $($service.Name) installed successfully" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "🔥 All Codex Dominion services installed!" -ForegroundColor Green
    Write-Host "Use 'Start-CodexServices' to begin digital sovereignty" -ForegroundColor White
}

function Start-CodexServices {
    Write-Host "🚀 Starting Codex Dominion Digital Empire..." -ForegroundColor Green

    foreach ($service in $services) {
        Write-Host "⚡ Starting $($service.DisplayName)..." -ForegroundColor Cyan
        Start-Service $service.Name -ErrorAction SilentlyContinue

        $status = Get-Service $service.Name -ErrorAction SilentlyContinue
        if ($status -and $status.Status -eq "Running") {
            Write-Host "   ✅ $($service.Name) running on port $($service.Port)" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Failed to start $($service.Name)" -ForegroundColor Red
        }
    }

    Write-Host ""
    Write-Host "🔥 Digital sovereignty activated!" -ForegroundColor Yellow
}

function Stop-CodexServices {
    Write-Host "🛑 Stopping Codex Dominion services..." -ForegroundColor Yellow

    foreach ($service in $services) {
        Write-Host "⏹️ Stopping $($service.DisplayName)..." -ForegroundColor Cyan
        Stop-Service $service.Name -Force -ErrorAction SilentlyContinue
        Write-Host "   ✅ $($service.Name) stopped" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "💤 Services stopped" -ForegroundColor White
}

function Get-CodexServiceStatus {
    Write-Host "📊 Codex Dominion Service Status:" -ForegroundColor Blue
    Write-Host "=================================" -ForegroundColor Blue
    Write-Host ""

    $allRunning = $true

    foreach ($service in $services) {
        $status = Get-Service $service.Name -ErrorAction SilentlyContinue
        if ($status) {
            $statusColor = if ($status.Status -eq "Running") { "Green" } else { "Red" }
            $statusIcon = if ($status.Status -eq "Running") { "✅" } else { "❌" }

            Write-Host "$statusIcon $($service.DisplayName): " -NoNewline
            Write-Host "$($status.Status)" -ForegroundColor $statusColor -NoNewline
            Write-Host " (Port $($service.Port))" -ForegroundColor White

            if ($status.Status -ne "Running") {
                $allRunning = $false
            }
        } else {
            Write-Host "❌ $($service.DisplayName): Not Installed" -ForegroundColor Red
            $allRunning = $false
        }
    }

    Write-Host ""
    if ($allRunning) {
        Write-Host "🔥 DIGITAL EMPIRE STATUS: FULLY OPERATIONAL" -ForegroundColor Green
    } else {
        Write-Host "⚠️ DIGITAL EMPIRE STATUS: PARTIAL OR OFFLINE" -ForegroundColor Yellow
    }
}

function Remove-CodexServices {
    Write-Host "🗑️ Removing Codex Dominion services..." -ForegroundColor Red

    if (-not (Test-Administrator)) {
        Write-Host "❌ Administrator privileges required for service removal" -ForegroundColor Red
        return
    }

    foreach ($service in $services) {
        Write-Host "🗑️ Removing $($service.DisplayName)..." -ForegroundColor Yellow

        # Stop service first
        Stop-Service $service.Name -Force -ErrorAction SilentlyContinue

        # Remove with NSSM
        & nssm remove $service.Name confirm
        Write-Host "   ✅ $($service.Name) removed" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "🔥 All services removed" -ForegroundColor Red
}

# Main execution
Write-CodexHeader

switch ($Action.ToLower()) {
    "install" {
        Install-CodexServices
    }
    "start" {
        Start-CodexServices
    }
    "stop" {
        Stop-CodexServices
    }
    "restart" {
        Stop-CodexServices
        Start-Sleep -Seconds 3
        Start-CodexServices
    }
    "status" {
        Get-CodexServiceStatus
    }
    "remove" {
        Remove-CodexServices
    }
    default {
        Write-Host "Usage: .\manage-codex-services.ps1 -Action [install|start|stop|restart|status|remove]" -ForegroundColor White
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Yellow
        Write-Host "  .\manage-codex-services.ps1 -Action install" -ForegroundColor White
        Write-Host "  .\manage-codex-services.ps1 -Action start" -ForegroundColor White
        Write-Host "  .\manage-codex-services.ps1 -Action status" -ForegroundColor White
    }
}
