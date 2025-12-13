#!/usr/bin/env pwsh
# =============================================================================
# DNS Propagation Monitoring & SSL Certificate Automation
# =============================================================================
# Monitors DNS propagation and triggers SSL certificate provisioning

param(
    [string]$Domain = "codexdominion.app",
    [int]$MaxChecks = 120,
    [int]$IntervalSeconds = 30
)

Write-Host "🌐 DNS Propagation & SSL Automation" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host "   Domain: $Domain"
Write-Host "   Checking every $IntervalSeconds seconds"
Write-Host "   Max attempts: $MaxChecks"
Write-Host ()

$resourceGroup = "codex-dominion"
$staticWebAppName = "codex-frontend-centralus"
$targetIP = "20.36.155.75"
$checkCount = 0
$propagated = $false

function Test-DnsResolution {
    param([string]$DomainName)

    try {
        $result = Resolve-DnsName -Name $DomainName -Type A -ErrorAction Stop
        $resolvedIP = ($result | Where-Object { $_.Type -eq "A" })[0].IPAddress

        if ($resolvedIP -eq $targetIP) {
            return @{
                Success = $true
                IP = $resolvedIP
                Status = "✅ Propagated"
            }
        } else {
            return @{
                Success = $false
                IP = $resolvedIP
                Status = "⚠️  Wrong IP"
            }
        }
    } catch {
        return @{
            Success = $false
            IP = "N/A"
            Status = "❌ Not resolved"
        }
    }
}

function Add-CustomDomain {
    param([string]$DomainName)

    Write-Host "`n🔐 Adding custom domain to Static Web App..."

    try {
        az staticwebapp hostname set `
            --name $staticWebAppName `
            --resource-group $resourceGroup `
            --hostname $DomainName `
            --output table

        Write-Host "✅ Custom domain added successfully" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "⚠️  Failed to add custom domain: $_" -ForegroundColor Yellow
        return $false
    }
}

function Show-Progress {
    param([int]$Current, [int]$Total, [string]$Status)

    $percent = [math]::Round(($Current / $Total) * 100)
    $bar = "=" * [math]::Floor($percent / 2)
    $spaces = " " * (50 - $bar.Length)

    Write-Host -NoNewline "`r[$bar$spaces] $percent% - $Status"
}

# Main monitoring loop
Write-Host "🔍 Monitoring DNS propagation..."
Write-Host ()

while ($checkCount -lt $MaxChecks -and -not $propagated) {
    $checkCount++

    # Test main domain
    $mainResult = Test-DnsResolution -DomainName $Domain
    $wwwResult = Test-DnsResolution -DomainName "www.$Domain"

    # Display results
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Check #$checkCount/$MaxChecks"
    Write-Host "   @   $Domain : $($mainResult.Status) ($($mainResult.IP))"
    Write-Host "   www www.$Domain : $($wwwResult.Status) ($($wwwResult.IP))"

    # Check if both propagated
    if ($mainResult.Success -and $wwwResult.Success) {
        $propagated = $true
        Write-Host "`n🎉 DNS FULLY PROPAGATED!" -ForegroundColor Green
        Write-Host "=" * 60

        # Add custom domains to Static Web App
        Add-CustomDomain -DomainName $Domain
        Add-CustomDomain -DomainName "www.$Domain"

        # Trigger SSL certificate provisioning
        Write-Host "`n🔒 SSL certificate will be automatically provisioned by Azure"
        Write-Host "   This may take 5-10 minutes"
        Write-Host "   Check status: az staticwebapp hostname show --name $staticWebAppName --resource-group $resourceGroup"

        break
    }

    if ($checkCount -lt $MaxChecks) {
        Write-Host "   ⏳ Waiting $IntervalSeconds seconds..." -ForegroundColor Yellow
        Write-Host ()
        Start-Sleep -Seconds $IntervalSeconds
    }
}

if (-not $propagated) {
    Write-Host "`n⚠️  DNS has not fully propagated after $MaxChecks checks" -ForegroundColor Yellow
    Write-Host "   This is normal - DNS propagation can take 24-48 hours"
    Write-Host "   Continue monitoring manually or re-run this script later"
}

Write-Host "`n" + ("=" * 60)
Write-Host "📊 Monitoring Summary:" -ForegroundColor Cyan
Write-Host "   Total checks: $checkCount"
Write-Host "   Duration: $($checkCount * $IntervalSeconds / 60) minutes"
Write-Host "   Status: $(if ($propagated) { '✅ Complete' } else { '⏳ In Progress' })"
