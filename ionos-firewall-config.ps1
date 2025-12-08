# IONOS Cloud Firewall Configuration Script (PowerShell)
# Adds firewall rules to IONOS Cloud server via REST API
# Usage: .\ionos-firewall-config.ps1

# ============================================================================
# CONFIGURATION - Set your IONOS credentials and resource IDs
# ============================================================================
$IONOS_USERNAME = $env:IONOS_USERNAME
$IONOS_PASSWORD = $env:IONOS_PASSWORD
$DATACENTER_ID = $env:IONOS_DATACENTER_ID
$SERVER_ID = $env:IONOS_SERVER_ID
$NIC_ID = $env:IONOS_NIC_ID

# If not set via environment variables, set them here:
if (-not $IONOS_USERNAME) {
    Write-Host "❌ Error: IONOS_USERNAME not set" -ForegroundColor Red
    Write-Host "Set environment variables or edit this script to add credentials." -ForegroundColor Yellow
    exit 1
}

# Base URL for IONOS Cloud API v6
$BASE_URL = "https://api.ionos.com/cloudapi/v6"
$AUTH = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${IONOS_USERNAME}:${IONOS_PASSWORD}"))
$HEADERS = @{
    "Authorization" = "Basic $AUTH"
    "Content-Type" = "application/json"
}

Write-Host "=== IONOS Cloud Firewall Configuration ===" -ForegroundColor Cyan
Write-Host "Datacenter: $DATACENTER_ID" -ForegroundColor Gray
Write-Host "Server: $SERVER_ID" -ForegroundColor Gray
Write-Host "NIC: $NIC_ID" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# Firewall Rules Configuration
# ============================================================================
$firewallRules = @(
    @{
        name = "Allow HTTP"
        protocol = "TCP"
        portRangeStart = 80
        portRangeEnd = 80
        sourceIp = $null
    },
    @{
        name = "Allow HTTPS"
        protocol = "TCP"
        portRangeStart = 443
        portRangeEnd = 443
        sourceIp = $null
    },
    @{
        name = "Allow SSH"
        protocol = "TCP"
        portRangeStart = 22
        portRangeEnd = 22
        sourceIp = $null
    },
    @{
        name = "Allow Next.js Dev Server"
        protocol = "TCP"
        portRangeStart = 3000
        portRangeEnd = 3000
        sourceIp = $null
    },
    @{
        name = "Allow Backend API"
        protocol = "TCP"
        portRangeStart = 8001
        portRangeEnd = 8001
        sourceIp = $null
    },
    @{
        name = "Allow Alt Backend"
        protocol = "TCP"
        portRangeStart = 8080
        portRangeEnd = 8080
        sourceIp = $null
    },
    @{
        name = "Allow PostgreSQL"
        protocol = "TCP"
        portRangeStart = 5432
        portRangeEnd = 5432
        sourceIp = $null
    },
    @{
        name = "Allow Redis"
        protocol = "TCP"
        portRangeStart = 6379
        portRangeEnd = 6379
        sourceIp = $null
    }
)

# ============================================================================
# Function to create firewall rule
# ============================================================================
function Add-IONOSFirewallRule {
    param (
        [string]$RuleName,
        [string]$Protocol,
        [int]$PortStart,
        [int]$PortEnd,
        [string]$SourceIp
    )

    $endpoint = "$BASE_URL/datacenters/$DATACENTER_ID/servers/$SERVER_ID/nics/$NIC_ID/firewallrules"

    $body = @{
        properties = @{
            name = $RuleName
            protocol = $Protocol
            portRangeStart = $PortStart
            portRangeEnd = $PortEnd
        }
    }

    # Add sourceIp only if specified
    if ($SourceIp) {
        $body.properties.sourceIp = $SourceIp
    }

    $jsonBody = $body | ConvertTo-Json -Depth 10

    try {
        Write-Host "⏳ Creating rule: $RuleName (Port $PortStart)" -ForegroundColor Yellow

        $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $HEADERS -Body $jsonBody -ErrorAction Stop

        Write-Host "✅ Successfully created: $RuleName" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to create: $RuleName" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red

        if ($_.ErrorDetails.Message) {
            Write-Host "   Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }

        return $false
    }
}

# ============================================================================
# Create all firewall rules
# ============================================================================
$successCount = 0
$failCount = 0

foreach ($rule in $firewallRules) {
    $result = Add-IONOSFirewallRule -RuleName $rule.name `
                                     -Protocol $rule.protocol `
                                     -PortStart $rule.portRangeStart `
                                     -PortEnd $rule.portRangeEnd `
                                     -SourceIp $rule.sourceIp

    if ($result) {
        $successCount++
    } else {
        $failCount++
    }

    Start-Sleep -Milliseconds 500  # Brief pause between requests
}

# ============================================================================
# Summary
# ============================================================================
Write-Host ""
Write-Host "=== Configuration Complete ===" -ForegroundColor Cyan
Write-Host "✅ Successfully created: $successCount rules" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "❌ Failed to create: $failCount rules" -ForegroundColor Red
}
Write-Host ""
Write-Host "⏰ Wait 1-5 minutes for rules to propagate, then test connectivity:" -ForegroundColor Yellow
Write-Host "   Test-NetConnection -ComputerName 74.208.123.158 -Port 443" -ForegroundColor Gray
Write-Host "   curl https://74.208.123.158" -ForegroundColor Gray
Write-Host ""
