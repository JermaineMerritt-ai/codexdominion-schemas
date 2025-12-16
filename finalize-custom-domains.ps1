#!/usr/bin/env pwsh
# =============================================================================
# Final Custom Domain Configuration - Run after 15 minutes
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🌐 FINAL DOMAIN CONFIGURATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n⏱️  Azure requires 15 minutes after domain removal" -ForegroundColor Yellow
Write-Host "   Current time: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor White

$response = Read-Host "`nHas it been 15+ minutes since DNS update? (y/n)"
if ($response -ne "y") {
    Write-Host "⏰ Come back in 15 minutes and run this script again!" -ForegroundColor Yellow
    exit
}

# =============================================================================
# Step 1: Verify DNS Propagation
# =============================================================================

Write-Host "`n[1/4] Verifying DNS propagation..." -ForegroundColor Cyan

Write-Host "`nChecking www.codexdominion.app..." -ForegroundColor White
$dnsWww = nslookup www.codexdominion.app 2>&1 | Out-String
if ($dnsWww -match "witty-glacier" -or $dnsWww -match "azurestaticapps") {
    Write-Host "✓ www DNS is propagating" -ForegroundColor Green
} else {
    Write-Host "⚠️  www DNS not fully propagated yet" -ForegroundColor Yellow
}

Write-Host "`nChecking api.codexdominion.app..." -ForegroundColor White
$dnsApi = nslookup api.codexdominion.app 2>&1 | Out-String
if ($dnsApi -match "codexdominion-backend" -or $dnsApi -match "azurewebsites") {
    Write-Host "✓ api DNS is propagating" -ForegroundColor Green
} else {
    Write-Host "⚠️  api DNS not fully propagated yet" -ForegroundColor Yellow
}

# =============================================================================
# Step 2: Add www.codexdominion.app to Static Web App
# =============================================================================

Write-Host "`n[2/4] Adding www.codexdominion.app to Static Web App..." -ForegroundColor Cyan

try {
    az staticwebapp hostname set `
        --name codexdominion-frontend `
        --resource-group codexdominion-basic `
        --hostname www.codexdominion.app
    Write-Host "✓ www.codexdominion.app configured" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to add www domain" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host "   Try again in 5-10 minutes" -ForegroundColor Yellow
}

# =============================================================================
# Step 3: Add api.codexdominion.app to Backend
# =============================================================================

Write-Host "`n[3/4] Adding api.codexdominion.app to Backend..." -ForegroundColor Cyan

try {
    az webapp config hostname add `
        --webapp-name codexdominion-backend `
        --resource-group codexdominion-basic `
        --hostname api.codexdominion.app
    Write-Host "✓ api.codexdominion.app configured" -ForegroundColor Green

    # Enable SSL
    Write-Host "`nEnabling SSL for api subdomain..." -ForegroundColor White
    az webapp config ssl create `
        --name codexdominion-backend `
        --resource-group codexdominion-basic `
        --hostname api.codexdominion.app
    Write-Host "✓ SSL certificate provisioned" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API domain configuration incomplete" -ForegroundColor Yellow
    Write-Host "   This may succeed after DNS fully propagates" -ForegroundColor Gray
}

# =============================================================================
# Step 4: Verify Custom Domains
# =============================================================================

Write-Host "`n[4/4] Verifying custom domains..." -ForegroundColor Cyan

Start-Sleep -Seconds 5

Write-Host "`nStatic Web App Domains:" -ForegroundColor White
az staticwebapp show `
    --name codexdominion-frontend `
    --resource-group codexdominion-basic `
    --query "{DefaultHostname:defaultHostname, CustomDomains:customDomains}" `
    --output table

Write-Host "`nBackend App Domains:" -ForegroundColor White
az webapp show `
    --name codexdominion-backend `
    --resource-group codexdominion-basic `
    --query "{DefaultHostname:defaultHostName, CustomDomains:hostNames}" `
    --output table

# =============================================================================
# Test Endpoints
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🧪 TESTING ENDPOINTS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nTesting www.codexdominion.app..." -ForegroundColor White
try {
    $response = curl -s -o nul -w "%{http_code}" https://www.codexdominion.app
    if ($response -eq 200) {
        Write-Host "✓ https://www.codexdominion.app is LIVE (HTTP $response)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  HTTP $response - May need more time" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Not accessible yet - DNS still propagating" -ForegroundColor Yellow
}

Write-Host "`nTesting api.codexdominion.app/health..." -ForegroundColor White
try {
    $response = curl -s https://api.codexdominion.app/health | ConvertFrom-Json
    if ($response.status -eq "healthy") {
        Write-Host "✓ https://api.codexdominion.app/health is LIVE" -ForegroundColor Green
        Write-Host "  Service: $($response.service)" -ForegroundColor Gray
        Write-Host "  Version: $($response.version)" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️  Not accessible yet - DNS still propagating" -ForegroundColor Yellow
}

# =============================================================================
# Summary
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎉 DOMAIN CONFIGURATION COMPLETE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nYour Custom Domains:" -ForegroundColor White
Write-Host "  🌐 Frontend: https://www.codexdominion.app" -ForegroundColor Green
Write-Host "  ⚙️  API:      https://api.codexdominion.app" -ForegroundColor Green

Write-Host "`n💡 If domains aren't working yet:" -ForegroundColor Yellow
Write-Host "   - DNS can take up to 48 hours to fully propagate globally" -ForegroundColor Gray
Write-Host "   - SSL certificates may take 10-15 minutes to provision" -ForegroundColor Gray
Write-Host "   - Clear your browser cache (Ctrl+Shift+Del)" -ForegroundColor Gray

Write-Host "`n🔥 The Flame Burns Sovereign on codexdominion.app! 👑" -ForegroundColor Yellow
Write-Host ""
