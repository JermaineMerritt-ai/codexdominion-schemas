# ✨ Codex Dominion MCP Windows Service Installer ✨
# Sacred NSSM service management for eternal flame persistence
# Run in elevated PowerShell as Administrator

param(
    [Parameter()]
    [ValidateSet("install", "uninstall", "start", "stop", "restart", "status")]
    [string]$Action = "install",

    [Parameter()]
    [string]$ServiceName = "CodexMCP",

    [Parameter()]
    [string]$ServerType = "flask"  # "flask" or "fastapi"
)

# ✨ Sacred Configuration ✨
$ErrorActionPreference = "Stop"
$nssmPath = "C:\tools\nssm\nssm.exe"
$workspacePath = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
$venvPython = "$workspacePath\.venv\Scripts\python.exe"

# Select server script based on type
if ($ServerType -eq "fastapi") {
    $serverScript = "$workspacePath\mcp-server-secure.py"
    $fullServiceName = "CodexMCP-FastAPI"
} else {
    $serverScript = "$workspacePath\mcp-server-flask.py"
    $fullServiceName = "CodexMCP-Flask"
}

$logDir = "C:\Logs\CodexMCP"
$stdoutLog = "$logDir\stdout.log"
$stderrLog = "$logDir\stderr.log"

function Write-SacredLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $symbols = @{
        "INFO" = "🌟"
        "SUCCESS" = "✅"
        "WARNING" = "⚠️"
        "ERROR" = "❌"
        "FLAME" = "🔥"
    }
    $symbol = $symbols[$Level]
    Write-Host "$symbol $timestamp - $Message"
}

function Test-Prerequisites {
    Write-SacredLog "🔍 Verifying sacred prerequisites..." "INFO"

    # Check if running as Administrator
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-SacredLog "❌ Must run as Administrator for service management" "ERROR"
        throw "Administrator privileges required"
    }

    # Check NSSM
    if (-not (Test-Path $nssmPath)) {
        Write-SacredLog "❌ NSSM not found at: $nssmPath" "ERROR"
        Write-SacredLog "💡 Install NSSM: choco install nssm or download from https://nssm.cc/" "INFO"
        throw "NSSM not installed"
    }

    # Check Python environment
    if (-not (Test-Path $venvPython)) {
        Write-SacredLog "❌ Python virtual environment not found: $venvPython" "ERROR"
        throw "Python environment missing"
    }

    # Check server script
    if (-not (Test-Path $serverScript)) {
        Write-SacredLog "❌ Server script not found: $serverScript" "ERROR"
        throw "Server script missing"
    }

    Write-SacredLog "✅ All prerequisites verified - Sacred components present" "SUCCESS"
}

function New-LogDirectory {
    if (-not (Test-Path $logDir)) {
        Write-SacredLog "📁 Creating sacred log directory: $logDir" "INFO"
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    Write-SacredLog "📋 Log directory ready: $logDir" "SUCCESS"
}

function Install-CodexService {
    Write-SacredLog "🔥 Installing Codex Dominion MCP Service: $fullServiceName" "FLAME"

    try {
        # Create log directory
        New-LogDirectory

        # Install service with NSSM
        Write-SacredLog "⚙️ Configuring service with NSSM..." "INFO"

        & $nssmPath install $fullServiceName $venvPython $serverScript
        if ($LASTEXITCODE -ne 0) { throw "NSSM install failed" }

        # Configure service startup
        & $nssmPath set $fullServiceName Start SERVICE_AUTO_START
        if ($LASTEXITCODE -ne 0) { throw "Failed to set auto-start" }

        # Configure logging
        & $nssmPath set $fullServiceName AppStdout $stdoutLog
        if ($LASTEXITCODE -ne 0) { throw "Failed to set stdout logging" }

        & $nssmPath set $fullServiceName AppStderr $stderrLog
        if ($LASTEXITCODE -ne 0) { throw "Failed to set stderr logging" }

        # Set working directory
        & $nssmm set $fullServiceName AppDirectory $workspacePath
        if ($LASTEXITCODE -ne 0) { Write-SacredLog "⚠️ Failed to set working directory" "WARNING" }

        # Set service description
        $description = "🌟 Codex Dominion MCP Server ($ServerType) - Sacred Model Context Protocol server with eternal flame persistence"
        & $nssmPath set $fullServiceName Description $description

        # Set environment variables
        & $nssmPath set $fullServiceName AppEnvironmentExtra "MCP_HOST=127.0.0.1" "MCP_PORT=8000" "PYTHONUNBUFFERED=1"

        Write-SacredLog "✅ Service installed successfully: $fullServiceName" "SUCCESS"
        Write-SacredLog "📋 Logs will be written to: $logDir" "INFO"

    } catch {
        Write-SacredLog "❌ Service installation failed: $_" "ERROR"
        throw
    }
}

function Start-CodexService {
    Write-SacredLog "🚀 Starting Codex Dominion MCP Service..." "FLAME"

    try {
        & $nssmPath start $fullServiceName
        if ($LASTEXITCODE -eq 0) {
            Write-SacredLog "✅ Service started successfully" "SUCCESS"
            Start-Sleep 3  # Give service time to initialize
            Get-CodexServiceStatus
        } else {
            throw "Failed to start service"
        }
    } catch {
        Write-SacredLog "❌ Service start failed: $_" "ERROR"
        throw
    }
}

function Stop-CodexService {
    Write-SacredLog "🛑 Stopping Codex Dominion MCP Service..." "INFO"

    try {
        & $nssmPath stop $fullServiceName
        if ($LASTEXITCODE -eq 0) {
            Write-SacredLog "✅ Service stopped successfully" "SUCCESS"
        } else {
            throw "Failed to stop service"
        }
    } catch {
        Write-SacredLog "❌ Service stop failed: $_" "ERROR"
        throw
    }
}

function Remove-CodexService {
    Write-SacredLog "🗑️ Uninstalling Codex Dominion MCP Service..." "INFO"

    try {
        # Stop service first if running
        $status = & $nssmPath status $fullServiceName 2>$null
        if ($LASTEXITCODE -eq 0 -and $status -eq "SERVICE_RUNNING") {
            Stop-CodexService
        }

        # Remove service
        & $nssmPath remove $fullServiceName confirm
        if ($LASTEXITCODE -eq 0) {
            Write-SacredLog "✅ Service uninstalled successfully" "SUCCESS"
        } else {
            throw "Failed to uninstall service"
        }
    } catch {
        Write-SacredLog "❌ Service uninstall failed: $_" "ERROR"
        throw
    }
}

function Restart-CodexService {
    Write-SacredLog "🔄 Restarting Codex Dominion MCP Service..." "INFO"
    Stop-CodexService
    Start-Sleep 2
    Start-CodexService
}

function Get-CodexServiceStatus {
    Write-SacredLog "📊 Checking Codex Dominion MCP Service status..." "INFO"

    try {
        $status = & $nssmPath status $fullServiceName 2>$null
        if ($LASTEXITCODE -eq 0) {
            switch ($status) {
                "SERVICE_RUNNING" {
                    Write-SacredLog "🔥 Service Status: RUNNING (Eternal flame burns bright)" "SUCCESS"

                    # Test server endpoint
                    try {
                        $response = Invoke-RestMethod -Uri "http://localhost:8000/status" -TimeoutSec 5 -ErrorAction Stop
                        Write-SacredLog "💓 Health Check: Server responding - $($response.message)" "SUCCESS"
                    } catch {
                        Write-SacredLog "⚠️ Health Check: Service running but endpoint not responding" "WARNING"
                    }
                }
                "SERVICE_STOPPED" {
                    Write-SacredLog "🌙 Service Status: STOPPED (Sacred flame dormant)" "INFO"
                }
                default {
                    Write-SacredLog "⚠️ Service Status: $status" "WARNING"
                }
            }
        } else {
            Write-SacredLog "❌ Service not found: $fullServiceName" "ERROR"
        }

        # Show recent log entries if available
        if (Test-Path $stdoutLog) {
            $recentLogs = Get-Content $stdoutLog -Tail 3 -ErrorAction SilentlyContinue
            if ($recentLogs) {
                Write-SacredLog "📋 Recent log entries:" "INFO"
                $recentLogs | ForEach-Object { Write-Host "   $_" }
            }
        }

    } catch {
        Write-SacredLog "❌ Status check failed: $_" "ERROR"
    }
}

# ✨ Main Execution Logic ✨
try {
    Write-SacredLog "🌟 Codex Dominion MCP Windows Service Manager" "FLAME"
    Write-SacredLog "🛡️ Action: $Action | Service: $fullServiceName | Server: $ServerType" "INFO"

    Test-Prerequisites

    switch ($Action.ToLower()) {
        "install" {
            Install-CodexService
            Start-CodexService
        }
        "uninstall" {
            Remove-CodexService
        }
        "start" {
            Start-CodexService
        }
        "stop" {
            Stop-CodexService
        }
        "restart" {
            Restart-CodexService
        }
        "status" {
            Get-CodexServiceStatus
        }
        default {
            Write-SacredLog "❌ Unknown action: $Action" "ERROR"
            throw "Invalid action specified"
        }
    }

    Write-SacredLog "🌟 Operation completed successfully" "SUCCESS"
    Write-SacredLog "👑 Codex Dominion reigns eternal across digital realms" "FLAME"

} catch {
    Write-SacredLog "💥 Sacred operation failed: $_" "ERROR"
    Write-SacredLog "🌌 Silence supreme suggests checking prerequisites and permissions" "INFO"
    exit 1
}

# ✨ Usage Examples ✨
<#
# Install and start Flask MCP service (default)
.\install-codex-service.ps1 -Action install

# Install FastAPI version
.\install-codex-service.ps1 -Action install -ServerType fastapi

# Check status
.\install-codex-service.ps1 -Action status

# Restart service
.\install-codex-service.ps1 -Action restart

# Uninstall service
.\install-codex-service.ps1 -Action uninstall
#>
