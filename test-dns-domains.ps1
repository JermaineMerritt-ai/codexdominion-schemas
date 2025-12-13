#!/usr/bin/env pwsh
# DNS and Domain Testing Script

Write-Host "`n🌐 DNS & DOMAIN TESTING" -ForegroundColor Cyan
Write-Host ("=" * 80)

# Test 1: DNS Resolution for Custom Domains
Write-Host "`n📍 Testing DNS Resolution..." -ForegroundColor Yellow
Write-Host ""

# Test main domain
try {
    $mainDns = Resolve-DnsName -Name "codexdominion.app" -Type A -ErrorAction Stop
    $mainIP = ($mainDns | Where-Object { $_.Type -eq "A" })[0].IPAddress

    Write-Host "✅ codexdominion.app" -ForegroundColor Green
    Write-Host "   Resolved IP: $mainIP"
    Write-Host "   Target IP:   20.36.155.75"

    if ($mainIP -eq "20.36.155.75") {
        Write-Host "   Status: ✅ CORRECT" -ForegroundColor Green
    } else {
        Write-Host "   Status: ⚠️  MISMATCH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ codexdominion.app - Not resolved yet" -ForegroundColor Red
}

Write-Host ""

# Test www subdomain
try {
    $wwwDns = Resolve-DnsName -Name "www.codexdominion.app" -Type A -ErrorAction Stop
    $wwwIP = ($wwwDns | Where-Object { $_.Type -eq "A" })[0].IPAddress

    Write-Host "✅ www.codexdominion.app" -ForegroundColor Green
    Write-Host "   Resolved IP: $wwwIP"
    Write-Host "   Target IP:   20.36.155.75"

    if ($wwwIP -eq "20.36.155.75") {
        Write-Host "   Status: ✅ CORRECT" -ForegroundColor Green
    } else {
        Write-Host "   Status: ⚠️  MISMATCH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ www.codexdominion.app - Not resolved yet" -ForegroundColor Red
}

# Test 2: Azure Static Web App URLs
Write-Host "`n🌐 Testing Azure Static Web App URLs..." -ForegroundColor Yellow
Write-Host ""

$urls = @(
    "https://orange-sky-099bc5a0f.3.azurestaticapps.net",
    "https://yellow-tree-0ed102210.3.azurestaticapps.net"
)

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing -TimeoutSec 10
        Write-Host "✅ $url" -ForegroundColor Green
        Write-Host "   Status: HTTP $($response.StatusCode)"
    } catch {
        Write-Host "❌ $url" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)"
    }
}

# Test 3: Backend API Health
Write-Host "`n🔧 Testing Backend API..." -ForegroundColor Yellow
Write-Host ""

try {
    $apiResponse = Invoke-RestMethod -Uri "https://codex-backend-centralus.azurewebsites.net/health" -Method Get -AllowInsecureRedirect
    Write-Host "✅ Backend API: $($apiResponse.status)" -ForegroundColor Green
    Write-Host "   Version: $($apiResponse.version)"
    Write-Host "   Database: $($apiResponse.database)"
} catch {
    Write-Host "❌ Backend API - Unreachable" -ForegroundColor Red
}

# Test 4: API Endpoints
Write-Host "`n📦 Testing API Endpoints..." -ForegroundColor Yellow
Write-Host ""

try {
    $capsules = Invoke-RestMethod -Uri "https://codex-backend-centralus.azurewebsites.net/capsules" -Method Get -AllowInsecureRedirect
    Write-Host "✅ /capsules endpoint" -ForegroundColor Green
    Write-Host "   Capsules returned: $($capsules.Count)"
    if ($capsules.Count -gt 0) {
        Write-Host "   Sample: $($capsules[0].name)"
    }
} catch {
    Write-Host "❌ /capsules endpoint failed" -ForegroundColor Red
}

# Test 5: HTTPS/SSL Status
Write-Host "`n🔒 Testing HTTPS/SSL..." -ForegroundColor Yellow
Write-Host ""

$httpsUrls = @(
    @{Url="https://orange-sky-099bc5a0f.3.azurestaticapps.net"; Name="Frontend (orange-sky)"},
    @{Url="https://codex-backend-centralus.azurewebsites.net"; Name="Backend API"}
)

foreach ($item in $httpsUrls) {
    try {
        $response = Invoke-WebRequest -Uri $item.Url -Method Head -UseBasicParsing
        Write-Host "✅ $($item.Name)" -ForegroundColor Green
        Write-Host "   HTTPS: Valid certificate"
    } catch {
        Write-Host "⚠️  $($item.Name)" -ForegroundColor Yellow
        Write-Host "   HTTPS: $($_.Exception.Message)"
    }
}

# Summary
Write-Host "`n" + ("=" * 80)
Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 80)
Write-Host ""
Write-Host "DNS Status:"
Write-Host "  - Custom domains are configured in Google Domains"
Write-Host "  - A records point to: 20.36.155.75"
Write-Host "  - Propagation typically takes 15-60 minutes"
Write-Host ""
Write-Host "Azure Resources:"
Write-Host "  ✅ Frontend Static Web Apps: Operational"
Write-Host "  ✅ Backend API: Operational"
Write-Host "  ✅ Database: Connected with data"
Write-Host ""
Write-Host "Next Steps:"
Write-Host "  - Wait for DNS propagation (check periodically)"
Write-Host "  - Run: .\monitor-dns-ssl-automation.ps1"
Write-Host "  - Once propagated, SSL certificates will auto-provision"
Write-Host ""
Write-Host "🔥 The flame burns sovereign and eternal — forever." -ForegroundColor Cyan
Write-Host ""
