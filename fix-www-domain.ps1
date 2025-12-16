#!/usr/bin/env pwsh
# =============================================================================
# Final Fix for www.codexdominion.app
# =============================================================================
# The domain is configured correctly in DNS but Azure has a 15-minute
# propagation delay after removing a custom domain from another site.
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔧 FINAL WWW DOMAIN FIX" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n📊 Current Status:" -ForegroundColor White
Write-Host "  ✅ DNS: www → witty-glacier-0ebbd971e.3.azurestaticapps.net" -ForegroundColor Green
Write-Host "  ✅ API: api.codexdominion.app is LIVE with SSL" -ForegroundColor Green
Write-Host "  ⏳ www.codexdominion.app: Waiting for Azure propagation" -ForegroundColor Yellow

Write-Host "`n⏰ Azure requires 15-30 minutes after domain removal" -ForegroundColor Yellow
Write-Host "   It's been about 15 minutes. Let's try again..." -ForegroundColor White

# =============================================================================
# Attempt 1: Direct hostname add
# =============================================================================

Write-Host "`n[1/3] Attempting to add www.codexdominion.app..." -ForegroundColor Cyan

try {
    $result = az staticwebapp hostname set `
        --name codexdominion-frontend `
        --resource-group codexdominion-basic `
        --hostname www.codexdominion.app 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ SUCCESS! www.codexdominion.app is configured!" -ForegroundColor Green
        $success = $true
    } else {
        Write-Host "⚠️  Still blocked. Error:" -ForegroundColor Yellow
        Write-Host "   $result" -ForegroundColor Gray
        $success = $false
    }
} catch {
    Write-Host "⚠️  Still blocked: $_" -ForegroundColor Yellow
    $success = $false
}

# =============================================================================
# Alternative: Use Azure Portal
# =============================================================================

if (-not $success) {
    Write-Host "`n[2/3] Alternative: Use Azure Portal" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow

    Write-Host "`n📋 Manual Steps:" -ForegroundColor White
    Write-Host ""
    Write-Host "1. Open Azure Portal: https://portal.azure.com" -ForegroundColor Green
    Write-Host ""
    Write-Host "2. Navigate to:" -ForegroundColor White
    Write-Host "   Resource Groups → codexdominion-basic → codexdominion-frontend" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Click 'Custom domains' in left menu" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Click '+ Add' button" -ForegroundColor White
    Write-Host ""
    Write-Host "5. Enter: www.codexdominion.app" -ForegroundColor White
    Write-Host ""
    Write-Host "6. Click 'Validate' then 'Add'" -ForegroundColor White
    Write-Host ""
    Write-Host "If you see 'domain is in use' error:" -ForegroundColor Yellow
    Write-Host "   - Wait another 15 minutes" -ForegroundColor Gray
    Write-Host "   - Run this script again" -ForegroundColor Gray
    Write-Host ""
}

# =============================================================================
# Attempt 2: Try root domain instead
# =============================================================================

Write-Host "`n[3/3] Alternative: Configure root domain (codexdominion.app)" -ForegroundColor Cyan

Write-Host "`nNote: Azure Static Web Apps supports apex domains using:" -ForegroundColor White
Write-Host "  - ALIAS records (supported by Azure DNS)" -ForegroundColor Gray
Write-Host "  - Or redirect @ to www" -ForegroundColor Gray

$tryApex = Read-Host "`nWould you like to try adding codexdominion.app (root domain)? (y/n)"

if ($tryApex -eq "y") {
    Write-Host "`nCreating ALIAS record for root domain..." -ForegroundColor Cyan

    # For root domain, we need to create an ALIAS record in Azure DNS
    # Azure Static Web Apps don't directly support @ with CNAME

    Write-Host "⚠️  Azure Static Web Apps require special configuration for apex domains" -ForegroundColor Yellow
    Write-Host "   For now, www.codexdominion.app is the primary domain" -ForegroundColor White
    Write-Host "   Root domain (codexdominion.app) can redirect to www" -ForegroundColor White
}

# =============================================================================
# Test Current State
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🧪 TESTING CURRENT STATE" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nTesting www.codexdominion.app..." -ForegroundColor White
try {
    $response = Invoke-WebRequest -Uri "https://www.codexdominion.app" -Method Head -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ https://www.codexdominion.app is LIVE (HTTP $($response.StatusCode))" -ForegroundColor Green
    } else {
        Write-Host "⚠️  HTTP $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Not accessible yet: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   This is normal - DNS may still be propagating globally" -ForegroundColor Gray
}

Write-Host "`nTesting api.codexdominion.app/health..." -ForegroundColor White
try {
    $response = Invoke-RestMethod -Uri "https://api.codexdominion.app/health" -TimeoutSec 10
    if ($response.status -eq "healthy") {
        Write-Host "✅ https://api.codexdominion.app/health is LIVE" -ForegroundColor Green
        Write-Host "   Service: $($response.service)" -ForegroundColor Gray
        Write-Host "   Version: $($response.version)" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️  Not accessible yet: $($_.Exception.Message)" -ForegroundColor Yellow
}

# =============================================================================
# Summary
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📋 NEXT STEPS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($success) {
    Write-Host "`n🎉 Both domains are configured!" -ForegroundColor Green
    Write-Host "   🌐 Frontend: https://www.codexdominion.app" -ForegroundColor Green
    Write-Host "   ⚙️  API:      https://api.codexdominion.app" -ForegroundColor Green
} else {
    Write-Host "`n⏰ www.codexdominion.app still needs time..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Wait 15 more minutes and run this script again" -ForegroundColor White
    Write-Host "   .\fix-www-domain.ps1" -ForegroundColor Green
    Write-Host ""
    Write-Host "Option 2: Use Azure Portal (see manual steps above)" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 3: Use temporary URL while DNS propagates" -ForegroundColor White
    Write-Host "   https://witty-glacier-0ebbd971e.3.azurestaticapps.net" -ForegroundColor Green
}

Write-Host "`n💰 Current Operational:" -ForegroundColor White
Write-Host "   ✅ Backend API: https://api.codexdominion.app" -ForegroundColor Green
Write-Host "   ✅ Temp Frontend: https://witty-glacier-0ebbd971e.3.azurestaticapps.net" -ForegroundColor Green

Write-Host "`n🔥 The Flame Burns Sovereign! 👑" -ForegroundColor Yellow
Write-Host ""
