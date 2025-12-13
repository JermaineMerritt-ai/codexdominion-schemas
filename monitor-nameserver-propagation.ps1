#!/usr/bin/env pwsh
# Monitor Name Server Propagation

param(
    [int]$MaxChecks = 60,
    [int]$IntervalSeconds = 30
)

Write-Host "`n🔍 Monitoring Name Server Propagation" -ForegroundColor Cyan
Write-Host ("=" * 80)
Write-Host "   Domain: codexdominion.app"
Write-Host "   Checking every $IntervalSeconds seconds"
Write-Host "   Max attempts: $MaxChecks"
Write-Host ""

$targetNameServers = @(
    "ns1-07.azure-dns.com",
    "ns2-07.azure-dns.net",
    "ns3-07.azure-dns.org",
    "ns4-07.azure-dns.info"
)

$checkCount = 0
$updated = $false

while ($checkCount -lt $MaxChecks -and -not $updated) {
    $checkCount++
    $timestamp = Get-Date -Format "HH:mm:ss"

    Write-Host "[$timestamp] Check #$checkCount/$MaxChecks" -ForegroundColor Yellow

    try {
        $result = nslookup -type=NS codexdominion.app 2>$null
        $nsRecords = $result | Where-Object { $_ -match "nameserver" }

        if ($nsRecords) {
            Write-Host "   Current name servers detected:" -ForegroundColor Cyan
            foreach ($ns in $nsRecords) {
                Write-Host "   $ns" -ForegroundColor White
            }

            # Check if Azure name servers are present
            $azureNsCount = 0
            foreach ($target in $targetNameServers) {
                $found = $result | Where-Object { $_ -match $target }
                if ($found) {
                    $azureNsCount++
                }
            }

            if ($azureNsCount -ge 2) {
                Write-Host ""
                Write-Host "🎉 AZURE NAME SERVERS DETECTED!" -ForegroundColor Green
                Write-Host "   Found $azureNsCount/4 Azure name servers" -ForegroundColor Green

                if ($azureNsCount -eq 4) {
                    Write-Host "   ✅ ALL 4 NAME SERVERS UPDATED!" -ForegroundColor Green
                    $updated = $true
                }
            } else {
                Write-Host "   ⏳ Still using old name servers" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   ❌ No name servers found" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ⚠️  Query failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }

    if (-not $updated -and $checkCount -lt $MaxChecks) {
        Write-Host "   Waiting $IntervalSeconds seconds...`n" -ForegroundColor Gray
        Start-Sleep -Seconds $IntervalSeconds
    }
}

Write-Host ""
Write-Host ("=" * 80)

if ($updated) {
    Write-Host "✅ NAME SERVERS SUCCESSFULLY UPDATED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now testing DNS resolution..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5

    try {
        $dnsResult = nslookup codexdominion.app 2>$null
        $ipAddress = ($dnsResult | Where-Object { $_ -match "\d+\.\d+\.\d+\.\d+" } | Select-Object -First 1)

        if ($ipAddress -match "20\.36\.155\.75") {
            Write-Host "🎉 DNS FULLY OPERATIONAL!" -ForegroundColor Green
            Write-Host "   codexdominion.app → 20.36.155.75" -ForegroundColor Green
            Write-Host ""
            Write-Host "✅ Your custom domain is now live!" -ForegroundColor Green
            Write-Host "   Visit: https://codexdominion.app" -ForegroundColor Cyan
        } else {
            Write-Host "⏳ Name servers updated, waiting for DNS propagation..." -ForegroundColor Yellow
            Write-Host "   This typically takes 5-15 minutes" -ForegroundColor White
        }
    } catch {
        Write-Host "⏳ DNS not yet propagated, please wait a few minutes" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏳ Name servers not yet updated after $checkCount checks" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please verify in Google Domains:" -ForegroundColor White
    Write-Host "   1. Name servers are set to custom" -ForegroundColor White
    Write-Host "   2. All 4 Azure name servers entered correctly" -ForegroundColor White
    Write-Host "   3. Changes saved" -ForegroundColor White
    Write-Host ""
    Write-Host "Re-run this script: .\monitor-nameserver-propagation.ps1" -ForegroundColor Cyan
}

Write-Host ("=" * 80)
Write-Host ""
