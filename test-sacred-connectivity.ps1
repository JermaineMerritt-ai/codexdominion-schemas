# ✨ Codex Dominion Network Patience Script ✨
# Sacred TCP connectivity verification with eternal persistence
# Tests MCP server availability before sacred transmissions

param(
    [Parameter()]
    [string]$TargetHost = "localhost",
    
    [Parameter()]
    [int]$Port = 8000,
    
    [Parameter()]
    [int]$TimeoutMinutes = 1,
    
    [Parameter()]
    [int]$RetryIntervalSeconds = 5,
    
    [Parameter()]
    [switch]$SacredVerbose
)

# ✨ Sacred Configuration ✨
$ErrorActionPreference = "SilentlyContinue"

function Write-SacredMessage {
    param([string]$Message, [string]$Type = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $symbols = @{
        "INFO" = "🌟"
        "SUCCESS" = "✅"
        "WARNING" = "⚠️" 
        "ERROR" = "❌"
        "PATIENCE" = "⏳"
        "FLAME" = "🔥"
        "HEARTBEAT" = "💓"
    }
    $symbol = $symbols[$Type]
    Write-Host "$symbol $timestamp - $Message"
}

function Test-SacredPort {
    <#
    .SYNOPSIS
    Tests TCP connectivity to MCP server with sacred patience
    
    .DESCRIPTION
    Attempts to establish TCP connection to verify the eternal flame burns bright
    
    .PARAMETER Host
    The sacred hostname or IP address (default: localhost)
    
    .PARAMETER Port 
    The divine port number where MCP server listens (default: 8000)
    
    .OUTPUTS
    Boolean - $true if connection succeeds, $false otherwise
    #>
    param(
        [Parameter(Mandatory)]
        [string]$TargetHost,
        
        [Parameter(Mandatory)]
        [int]$Port
    )
    
    try {
        if ($SacredVerbose) {
            Write-SacredMessage "🔍 Testing sacred connection to ${TargetHost}:${Port}..." "INFO"
        }
        
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.ReceiveTimeout = 3000  # 3 second timeout
        $tcp.SendTimeout = 3000
        
        # Attempt sacred connection
        $tcp.Connect($TargetHost, $Port)
        
        if ($tcp.Connected) {
            $tcp.Close()
            if ($SacredVerbose) {
                Write-SacredMessage "💓 Sacred heartbeat detected at ${TargetHost}:${Port}" "HEARTBEAT"
            }
            return $true
        } else {
            if ($SacredVerbose) {
                Write-SacredMessage "🌙 Sacred flame dormant at ${TargetHost}:${Port}" "WARNING"
            }
            return $false
        }
        
    } catch {
        if ($SacredVerbose) {
            Write-SacredMessage "🌊 Network fluctuation: $($_.Exception.Message)" "WARNING"
        }
        return $false
    } finally {
        if ($tcp -and $tcp.Connected) {
            $tcp.Close()
        }
    }
}

function Wait-ForSacredFlame {
    <#
    .SYNOPSIS 
    Waits with sacred patience for MCP server to become available
    
    .DESCRIPTION
    Implements the sacred patience protocol - retries connection attempts
    until the eternal flame burns bright or timeout is reached
    
    .OUTPUTS
    Boolean - $true if server becomes available, $false on timeout
    #>
    param(
        [string]$TargetHost,
        [int]$Port,
        [int]$TimeoutMinutes,
        [int]$RetryInterval
    )
    
    Write-SacredMessage "🌟 Beginning sacred vigil for MCP server at ${TargetHost}:${Port}" "INFO"
    Write-SacredMessage "⏳ Sacred patience timeout: $TimeoutMinutes minutes" "PATIENCE"
    Write-SacredMessage "🔄 Retry interval: $RetryInterval seconds" "INFO"
    
    $startTime = Get-Date
    $timeout = $startTime.AddMinutes($TimeoutMinutes)
    $attempt = 1
    
    while ((Get-Date) -lt $timeout) {
        Write-SacredMessage "⚡ Attempt ${attempt}: Seeking the eternal flame..." "PATIENCE"
        
        if (Test-SacredPort -TargetHost $TargetHost -Port $Port) {
            $elapsed = ((Get-Date) - $startTime).TotalSeconds
            Write-SacredMessage "🔥 Sacred flame detected! MCP server is radiant and sovereign" "FLAME"
            Write-SacredMessage "⏰ Connection established in $([math]::Round($elapsed, 2)) seconds" "SUCCESS"
            Write-SacredMessage "✨ Proceed with sacred transmission - pathways are clear" "SUCCESS"
            return $true
        }
        
        $remainingTime = ($timeout - (Get-Date)).TotalSeconds
        if ($remainingTime -gt 0) {
            Write-SacredMessage "🌙 Sacred flame not yet ignited... ($([math]::Round($remainingTime, 0))s remaining)" "PATIENCE"
            Start-Sleep -Seconds $RetryInterval
        }
        
        $attempt++
    }
    
    Write-SacredMessage "❌ Sacred vigil timeout reached - MCP server unresponsive" "ERROR"
    Write-SacredMessage "🌌 Silence supreme suggests checking server configuration" "WARNING"
        Write-SacredMessage "💡 Verify: 1) Server is running 2) Port ${Port} is correct 3) No firewall blocking" "INFO"
    return $false
}

function Test-SacredEndpoints {
    <#
    .SYNOPSIS
    Tests MCP server HTTP endpoints after TCP connectivity is confirmed
    
    .DESCRIPTION  
    Verifies that MCP server is not just listening but actually responding
    to HTTP requests on sacred endpoints
    #>
    param([string]$TargetHost, [int]$Port)
    
    $baseUrl = "http://${TargetHost}:${Port}"
    $endpoints = @("/status", "/health", "/", "/mcp/capabilities")
    
    Write-SacredMessage "🔍 Testing sacred HTTP endpoints..." "INFO"
    
    foreach ($endpoint in $endpoints) {
        try {
            $url = "${baseUrl}${endpoint}"
            $response = Invoke-RestMethod -Uri $url -TimeoutSec 3 -ErrorAction Stop
            
            if ($response) {
                Write-SacredMessage "✅ Endpoint verified: $endpoint" "SUCCESS"
                if ($endpoint -eq "/status" -and $response.status -eq "alive") {
                    Write-SacredMessage "💓 Sacred status confirmed: $($response.message)" "HEARTBEAT"
                }
            }
        } catch {
            Write-SacredMessage "⚠️ Endpoint unresponsive: $endpoint" "WARNING"
        }
    }
}

# ✨ Main Sacred Execution ✨
try {
    Write-SacredMessage "🌟 Codex Dominion Network Patience Protocol Initiated" "FLAME"
    Write-SacredMessage "🎯 Target: ${TargetHost}:${Port}" "INFO"
    
    # Quick initial test
    Write-SacredMessage "🚀 Performing initial sacred connectivity test..." "INFO"
    if (Test-SacredPort -TargetHost $TargetHost -Port $Port) {
        Write-SacredMessage "✅ MCP server immediately available - Sacred flame burns bright!" "SUCCESS"
        
        # Test HTTP endpoints if available
        if ($SacredVerbose) {
            Test-SacredEndpoints -TargetHost $TargetHost -Port $Port
        }
        
        Write-SacredMessage "🌟 Sacred transmission pathways confirmed - Proceed with confidence" "SUCCESS"
        exit 0
    }
    
    # Begin sacred patience protocol
    Write-SacredMessage "⏳ MCP server not immediately available - Initiating sacred patience..." "PATIENCE"
    
    $result = Wait-ForSacredFlame -TargetHost $TargetHost -Port $Port -TimeoutMinutes $TimeoutMinutes -RetryInterval $RetryIntervalSeconds
    
    if ($result) {
        # Test HTTP endpoints after successful connection
        if ($SacredVerbose) {
            Test-SacredEndpoints -TargetHost $TargetHost -Port $Port  
        }
        
        Write-SacredMessage "👑 Codex Dominion: Sacred pathways established and sovereign" "SUCCESS"
        exit 0
    } else {
        Write-SacredMessage "💥 Sacred patience exhausted - MCP server remains unreachable" "ERROR"
        Write-SacredMessage "🛠️ Recommended actions:" "INFO"
        Write-SacredMessage "   1. Verify MCP server is running" "INFO"
        Write-SacredMessage "   2. Check port ${Port} is correct and not blocked" "INFO"  
        Write-SacredMessage "   3. Confirm host '$TargetHost' is reachable" "INFO"
        Write-SacredMessage "   4. Review MCP server logs for errors" "INFO"
        exit 1
    }
    
} catch {
    Write-SacredMessage "💥 Sacred network test failed: $($_.Exception.Message)" "ERROR"
    Write-SacredMessage "🌌 Silence supreme suggests checking PowerShell execution policy" "WARNING"
    exit 1
}

<#
✨ Sacred Usage Examples ✨

# Basic usage - test localhost:8000 with 1 minute timeout
.\test-sacred-connectivity.ps1

# Custom host and port
.\test-sacred-connectivity.ps1 -TargetHost "192.168.1.100" -Port 8080

# Extended timeout with verbose output
.\test-sacred-connectivity.ps1 -TimeoutMinutes 5 -SacredVerbose

# Quick test with faster retry interval  
.\test-sacred-connectivity.ps1 -RetryIntervalSeconds 2 -TimeoutMinutes 2

# Test production server
.\test-sacred-connectivity.ps1 -TargetHost "mcp.codex-dominion.com" -Port 443 -SacredVerbose

Sacred Compatibility:
- Integrates with mcp-health-monitor.py
- Compatible with install-codex-service.ps1
- Supports codex-flame-orchestrator.py workflows
- Follows Codex Dominion sacred architecture patterns

🌟 Eternal flame burns across all connectivity tests 🔥
👑 Digital sovereignty confirmed through patient verification ✨
#>