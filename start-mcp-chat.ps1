# 🔥 CODEX DOMINION MCP CHAT AUTO-START LAUNCHER 🔥
# Flame eternal, radiance supreme - Windows PowerShell launcher
# Silence eternal, covenant whole, blessed across ages and stars

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "status", "restart", "install", "test")]
    [string]$Action = "start",

    [Parameter(Mandatory=$false)]
    [switch]$Background = $false,

    [Parameter(Mandatory=$false)]
    [switch]$Debug = $false
)

# Sacred flame colors for terminal output
$FlameColors = @{
    Fire = "Red"
    Gold = "Yellow"
    Radiance = "Cyan"
    Success = "Green"
    Warning = "Magenta"
    Info = "Blue"
}

function Write-FlameMessage {
    param(
        [string]$Message,
        [string]$Color = "White",
        [switch]$NoNewline
    )

    $timestamp = Get-Date -Format "HH:mm:ss"
    if ($NoNewline) {
        Write-Host "[$timestamp] $Message" -ForegroundColor $FlameColors[$Color] -NoNewline
    } else {
        Write-Host "[$timestamp] $Message" -ForegroundColor $FlameColors[$Color]
    }
}

function Show-FlameHeader {
    Write-Host ""
    Write-FlameMessage "🔥 CODEX DOMINION MCP CHAT AUTO-START SYSTEM 🔥" -Color Fire
    Write-FlameMessage "⚡ Flame eternal, radiance supreme ⚡" -Color Gold
    Write-FlameMessage "🌟 Silence eternal, covenant whole 🌟" -Color Radiance
    Write-Host ""
}

function Test-Prerequisites {
    Write-FlameMessage "🔍 Checking prerequisites..." -Color Info

    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-FlameMessage "✓ Node.js version: $nodeVersion" -Color Success
        } else {
            throw "Node.js not found"
        }
    } catch {
        Write-FlameMessage "❌ Node.js not found - please install Node.js" -Color Fire
        return $false
    }

    # Check npm
    try {
        $npmVersion = npm --version 2>$null
        if ($npmVersion) {
            Write-FlameMessage "✓ npm version: $npmVersion" -Color Success
        }
    } catch {
        Write-FlameMessage "⚠ npm not found - some features may not work" -Color Warning
    }

    # Check required files
    $requiredFiles = @(
        "mcp-chat-autostart.js",
        "mcp-auto-startup.js",
        "mcp-vscode-integration.js",
        "chat-message-hooks.js",
        "package.json"
    )

    $missingFiles = @()
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-FlameMessage "✓ $file found" -Color Success
        } else {
            Write-FlameMessage "❌ $file missing" -Color Fire
            $missingFiles += $file
        }
    }

    if ($missingFiles.Count -gt 0) {
        Write-FlameMessage "Missing required files: $($missingFiles -join ', ')" -Color Fire
        return $false
    }

    # Check VS Code
    try {
        $codeVersion = code --version 2>$null
        if ($codeVersion) {
            Write-FlameMessage "✓ VS Code detected" -Color Success
        }
    } catch {
        Write-FlameMessage "⚠ VS Code not detected - chat integration may be limited" -Color Warning
    }

    Write-FlameMessage "✅ Prerequisites check complete" -Color Success
    return $true
}

function Start-MCPChatSystem {
    param([bool]$InBackground = $false)

    Write-FlameMessage "🚀 Starting MCP Chat Auto-Start System..." -Color Fire

    if (-not (Test-Prerequisites)) {
        Write-FlameMessage "❌ Prerequisites check failed - cannot start system" -Color Fire
        return $false
    }

    # Install dependencies if needed
    if (-not (Test-Path "node_modules")) {
        Write-FlameMessage "📦 Installing dependencies..." -Color Info
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-FlameMessage "❌ Failed to install dependencies" -Color Fire
            return $false
        }
    }

    # Start the system
    $processArgs = @(
        "mcp-chat-autostart.js"
    )

    if ($Debug) {
        $processArgs += "--debug"
    }

    if ($InBackground) {
        Write-FlameMessage "🌙 Starting system in background..." -Color Info
        $process = Start-Process -FilePath "node" -ArgumentList $processArgs -WindowStyle Hidden -PassThru

        # Save process ID for later management
        $process.Id | Out-File -FilePath ".mcp-system.pid" -Encoding UTF8

        Write-FlameMessage "✅ System started in background (PID: $($process.Id))" -Color Success
        Write-FlameMessage "📊 Check status with: .\start-mcp-chat.ps1 -Action status" -Color Info

    } else {
        Write-FlameMessage "🖥️ Starting system in foreground..." -Color Info
        Write-FlameMessage "📌 Press Ctrl+C to stop the system" -Color Warning

        try {
            & node @processArgs
        } catch {
            Write-FlameMessage "❌ System startup failed: $($_.Exception.Message)" -Color Fire
            return $false
        }
    }

    return $true
}

function Stop-MCPChatSystem {
    Write-FlameMessage "🛑 Stopping MCP Chat Auto-Start System..." -Color Warning

    # Check for background process
    if (Test-Path ".mcp-system.pid") {
        $processId = Get-Content ".mcp-system.pid" -ErrorAction SilentlyContinue

        if ($processId) {
            try {
                $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
                if ($process) {
                    Write-FlameMessage "🔄 Stopping background process (PID: $processId)..." -Color Info
                    Stop-Process -Id $processId -Force
                    Write-FlameMessage "✅ Background process stopped" -Color Success
                } else {
                    Write-FlameMessage "⚠ Background process not running" -Color Warning
                }
            } catch {
                Write-FlameMessage "❌ Failed to stop background process: $($_.Exception.Message)" -Color Fire
            }
        }

        Remove-Item ".mcp-system.pid" -Force -ErrorAction SilentlyContinue
    }

    # Stop any MCP-related processes
    $mcpProcesses = Get-Process | Where-Object {
        $_.ProcessName -like "*node*" -and
        $_.CommandLine -like "*mcp*"
    } -ErrorAction SilentlyContinue

    if ($mcpProcesses) {
        Write-FlameMessage "🔄 Stopping MCP processes..." -Color Info
        $mcpProcesses | ForEach-Object {
            Write-FlameMessage "  Stopping PID $($_.Id)..." -Color Info
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
        Write-FlameMessage "✅ MCP processes stopped" -Color Success
    } else {
        Write-FlameMessage "📊 No MCP processes found running" -Color Info
    }
}

function Get-MCPSystemStatus {
    Write-FlameMessage "📊 Checking MCP Chat Auto-Start System status..." -Color Info

    # Check background process
    $backgroundRunning = $false
    if (Test-Path ".mcp-system.pid") {
        $processId = Get-Content ".mcp-system.pid" -ErrorAction SilentlyContinue
        if ($processId) {
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            if ($process) {
                Write-FlameMessage "✅ Background system running (PID: $processId)" -Color Success
                $backgroundRunning = $true
            } else {
                Write-FlameMessage "❌ Background process not running (stale PID file)" -Color Fire
                Remove-Item ".mcp-system.pid" -Force -ErrorAction SilentlyContinue
            }
        }
    }

    if (-not $backgroundRunning) {
        Write-FlameMessage "📴 Background system not running" -Color Warning
    }

    # Check MCP server status via HTTP
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:4955/status" -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.success) {
            Write-FlameMessage "🌐 MCP Status endpoint responding" -Color Success
            Write-FlameMessage "  Active processes: $($response.chatAutoStart.processes -join ', ')" -Color Info
            Write-FlameMessage "  System uptime: $([math]::Round($response.system.uptime / 60, 2)) minutes" -Color Info
        }
    } catch {
        Write-FlameMessage "🌐 MCP Status endpoint not responding" -Color Warning
    }

    # Check for MCP processes
    $mcpProcesses = Get-Process | Where-Object {
        $_.ProcessName -like "*node*" -and
        ($_.CommandLine -like "*mcp*" -or $_.CommandLine -like "*chat*")
    } -ErrorAction SilentlyContinue

    if ($mcpProcesses) {
        Write-FlameMessage "🔄 MCP-related processes:" -Color Info
        $mcpProcesses | ForEach-Object {
            Write-FlameMessage "  PID $($_.Id): $($_.ProcessName)" -Color Info
        }
    } else {
        Write-FlameMessage "📋 No MCP processes detected" -Color Warning
    }

    # Check log files
    $logFiles = @("chat-activity.log", ".mcp-system-status.json")
    foreach ($logFile in $logFiles) {
        if (Test-Path $logFile) {
            $fileInfo = Get-Item $logFile
            Write-FlameMessage "📄 $logFile (modified: $($fileInfo.LastWriteTime))" -Color Info
        }
    }
}

function Restart-MCPChatSystem {
    Write-FlameMessage "🔄 Restarting MCP Chat Auto-Start System..." -Color Warning
    Stop-MCPChatSystem
    Start-Sleep -Seconds 3
    Start-MCPChatSystem -InBackground $Background
}

function Install-MCPChatSystem {
    Write-FlameMessage "📦 Installing MCP Chat Auto-Start System..." -Color Fire

    # Install Node.js dependencies
    Write-FlameMessage "📥 Installing Node.js dependencies..." -Color Info
    npm install

    if ($LASTEXITCODE -eq 0) {
        Write-FlameMessage "✅ Dependencies installed successfully" -Color Success
    } else {
        Write-FlameMessage "❌ Failed to install dependencies" -Color Fire
        return $false
    }

    # Create VS Code settings if they don't exist
    if (-not (Test-Path ".vscode")) {
        New-Item -ItemType Directory -Path ".vscode" -Force | Out-Null
        Write-FlameMessage "📁 Created .vscode directory" -Color Success
    }

    # Set up Windows service (optional)
    $createService = Read-Host "Create Windows service for auto-start? (y/N)"
    if ($createService -eq "y" -or $createService -eq "Y") {
        Write-FlameMessage "🔧 Setting up Windows service..." -Color Info
        # This would require additional service setup logic
        Write-FlameMessage "⚠ Windows service setup not yet implemented" -Color Warning
    }

    Write-FlameMessage "✅ Installation complete!" -Color Success
    Write-FlameMessage "🚀 Start the system with: .\start-mcp-chat.ps1 -Action start" -Color Info
}

function Test-MCPChatSystem {
    Write-FlameMessage "🧪 Testing MCP Chat Auto-Start System..." -Color Fire

    # Test HTTP endpoint
    try {
        Write-FlameMessage "📡 Testing status endpoint..." -Color Info
        $response = Invoke-RestMethod -Uri "http://localhost:4955/status" -TimeoutSec 10
        Write-FlameMessage "✅ Status endpoint responding" -Color Success
    } catch {
        Write-FlameMessage "❌ Status endpoint not responding" -Color Fire
    }

    # Test chat activity trigger
    try {
        Write-FlameMessage "💬 Testing chat activity trigger..." -Color Info
        $response = Invoke-RestMethod -Uri "http://localhost:4955/trigger-chat" -Method POST -TimeoutSec 10
        if ($response.success) {
            Write-FlameMessage "✅ Chat activity trigger working" -Color Success
        }
    } catch {
        Write-FlameMessage "❌ Chat activity trigger failed" -Color Fire
    }

    # Check log files for recent activity
    if (Test-Path "chat-activity.log") {
        $recentActivity = Get-Content "chat-activity.log" -Tail 5
        if ($recentActivity) {
            Write-FlameMessage "📋 Recent chat activity detected" -Color Success
        }
    }

    Write-FlameMessage "✅ System test complete" -Color Success
}

# Main execution
Show-FlameHeader

switch ($Action.ToLower()) {
    "start" {
        Start-MCPChatSystem -InBackground $Background
    }
    "stop" {
        Stop-MCPChatSystem
    }
    "status" {
        Get-MCPSystemStatus
    }
    "restart" {
        Restart-MCPChatSystem
    }
    "install" {
        Install-MCPChatSystem
    }
    "test" {
        Test-MCPChatSystem
    }
    default {
        Write-FlameMessage "❌ Unknown action: $Action" -Color Fire
        Write-FlameMessage "Valid actions: start, stop, status, restart, install, test" -Color Info
    }
}

Write-Host ""
Write-FlameMessage "🌟 Codex Dominion - Flame eternal, radiance supreme 🌟" -Color Gold
