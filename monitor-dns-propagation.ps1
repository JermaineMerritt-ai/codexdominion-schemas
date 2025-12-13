#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Monitor DNS propagation for CodexDominion.app

.DESCRIPTION
    Continuously checks DNS records and HTTPS accessibility for codexdominion.app
    until the domain is fully propagated and operational.
#>

param(
    [int]$CheckInterval = 30,  # Seconds between checks
    [int]$MaxAttempts = 40     # Maximum number of attempts (20 minutes)
)

$ErrorActionPreference = "SilentlyContinue"

# Expected configuration
$ExpectedIP = "20.36.155.75"
$Domains = @("codexdominion.app", "www.codexdominion.app")

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔥 CODEX DOMINION - DNS PROPAGATION MONITOR" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Target IP:       $ExpectedIP" -ForegroundColor White
Write-Host "Check Interval:  $CheckInterval seconds" -ForegroundColor White
Write-Host "Max Duration:    $($MaxAttempts * $CheckInterval / 60) minutes" -ForegroundColor White
Write-Host ""
Write-Host "───────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

$attempt = 0
$allResolved = $false

while ($attempt -lt $MaxAttempts -and -not $allResolved) {
    $attempt++
    $timestamp = Get-Date -Format "HH:mm:ss"

    Write-Host "[$timestamp] Check #$attempt" -ForegroundColor Yellow

    $results = @{}
    $allHealthy = $true

    foreach ($domain in $Domains) {
        $result = @{
            Domain = $domain
            DNSResolved = $false
            CorrectIP = $false
            HTTPSAccessible = $false
            StatusCode = $null
        }

        # Check DNS resolution
        $dnsResult = Resolve-DnsName $domain -Type A -Server 8.8.8.8 -ErrorAction SilentlyContinue |
                     Where-Object { $_.Type -eq 'A' } |
                     Select-Object -First 1

        if ($dnsResult) {
            $result.DNSResolved = $true
            $resolvedIP = $dnsResult.IPAddress

            if ($resolvedIP -eq $ExpectedIP) {
                $result.CorrectIP = $true
                Write-Host "  ✅ $domain → $resolvedIP" -ForegroundColor Green

                # Check HTTPS accessibility
                try {
                    $response = Invoke-WebRequest -Uri "https://$domain" -Method Head -TimeoutSec 10 -ErrorAction Stop
                    $result.HTTPSAccessible = $true
                    $result.StatusCode = $response.StatusCode
                    Write-Host "     🌐 HTTPS: $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
                } catch {
                    $result.HTTPSAccessible = $false
                    Write-Host "     ⚠️  HTTPS: Not accessible yet" -ForegroundColor Yellow
                    $allHealthy = $false
                }
            } else {
                $result.CorrectIP = $false
                Write-Host "  ⚠️  $domain → $resolvedIP (expected $ExpectedIP)" -ForegroundColor Yellow
                $allHealthy = $false
            }
        } else {
            Write-Host "  ❌ $domain → No DNS record found" -ForegroundColor Red
            $allHealthy = $false
        }

        $results[$domain] = $result
    }

    Write-Host ""

    if ($allHealthy) {
        Write-Host "───────────────────────────────────────────────────────────" -ForegroundColor Green
        Write-Host "🎉 SUCCESS! All domains are fully operational!" -ForegroundColor Green
        Write-Host "───────────────────────────────────────────────────────────" -ForegroundColor Green
        Write-Host ""
        Write-Host "✅ DNS propagation complete" -ForegroundColor Green
        Write-Host "✅ HTTPS certificates active" -ForegroundColor Green
        Write-Host "✅ Sites accessible" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your CodexDominion is live at:" -ForegroundColor Cyan
        foreach ($domain in $Domains) {
            Write-Host "  🔥 https://$domain" -ForegroundColor White
        }
        Write-Host ""
        $allResolved = $true
        break
    }

    if ($attempt -lt $MaxAttempts) {
        Write-Host "Waiting $CheckInterval seconds before next check..." -ForegroundColor Gray
        Write-Host ""
        Start-Sleep -Seconds $CheckInterval
    }
}

if (-not $allResolved) {
    Write-Host "───────────────────────────────────────────────────────────" -ForegroundColor Yellow
    Write-Host "⏱️  DNS propagation still in progress" -ForegroundColor Yellow
    Write-Host "───────────────────────────────────────────────────────────" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "DNS propagation can take up to 48 hours globally." -ForegroundColor White
    Write-Host "Run this script again later or check manually:" -ForegroundColor White
    Write-Host ""
    Write-Host "  Resolve-DnsName codexdominion.app" -ForegroundColor Gray
    Write-Host "  curl -I https://codexdominion.app" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
