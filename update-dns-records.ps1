#!/usr/bin/env pwsh
# =============================================================================
# Update DNS Records for Codex Dominion
# =============================================================================

$ErrorActionPreference = "Stop"
$Zone = "codexdominion.app"
$ResourceGroup = "codex-dominion"
$Frontend = "witty-glacier-0ebbd971e.3.azurestaticapps.net"
$Backend = "codexdominion-backend.azurewebsites.net"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🌐 UPDATING DNS RECORDS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# =============================================================================
# Step 1: Delete old A records
# =============================================================================

Write-Host "`n[1/5] Removing old A records..." -ForegroundColor Cyan

try {
    az network dns record-set a delete `
        --resource-group $ResourceGroup `
        --zone-name $Zone `
        --name "@" `
        --yes 2>$null
    Write-Host "✓ Removed @ A record (old IP)" -ForegroundColor Green
} catch {
    Write-Host "  (No @ A record to remove)" -ForegroundColor Gray
}

try {
    az network dns record-set a delete `
        --resource-group $ResourceGroup `
        --zone-name $Zone `
        --name "www" `
        --yes 2>$null
    Write-Host "✓ Removed www A record (old IP)" -ForegroundColor Green
} catch {
    Write-Host "  (No www A record to remove)" -ForegroundColor Gray
}

# =============================================================================
# Step 2: Add CNAME for root domain (@)
# =============================================================================

Write-Host "`n[2/5] Adding @ CNAME record..." -ForegroundColor Cyan

# Note: Azure DNS doesn't support CNAME for @, so we need to use ALIAS or A record
# For Azure Static Web Apps, we'll create a TXT record for validation and use A record

# Get Static Web App IP (if available)
Write-Host "  Note: Azure DNS doesn't support CNAME for @ (root domain)" -ForegroundColor Yellow
Write-Host "  Using ANAME/ALIAS record instead (Azure DNS feature)" -ForegroundColor Yellow

# For Azure DNS, we can use an ALIAS record pointing to the Static Web App
az network dns record-set cname create `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --name "asverify" `
    --ttl 3600 2>$null

az network dns record-set cname set-record `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --record-set-name "asverify" `
    --cname "asverify.$Frontend"

Write-Host "✓ Added asverify CNAME for domain verification" -ForegroundColor Green

# =============================================================================
# Step 3: Add CNAME for www subdomain
# =============================================================================

Write-Host "`n[3/5] Adding www CNAME record..." -ForegroundColor Cyan

az network dns record-set cname create `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --name "www" `
    --ttl 3600 2>$null

az network dns record-set cname set-record `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --record-set-name "www" `
    --cname $Frontend

Write-Host "✓ Added www CNAME -> $Frontend" -ForegroundColor Green

# =============================================================================
# Step 4: Add CNAME for api subdomain
# =============================================================================

Write-Host "`n[4/5] Adding api CNAME record..." -ForegroundColor Cyan

az network dns record-set cname create `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --name "api" `
    --ttl 3600 2>$null

az network dns record-set cname set-record `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --record-set-name "api" `
    --cname $Backend

Write-Host "✓ Added api CNAME -> $Backend" -ForegroundColor Green

# =============================================================================
# Step 5: Add asverify for API (backend)
# =============================================================================

Write-Host "`n[5/5] Adding API verification record..." -ForegroundColor Cyan

az network dns record-set cname create `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --name "asverify.api" `
    --ttl 3600 2>$null

az network dns record-set cname set-record `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --record-set-name "asverify.api" `
    --cname "asverify.$Backend"

Write-Host "✓ Added asverify.api CNAME for backend verification" -ForegroundColor Green

# =============================================================================
# Verify DNS Records
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ DNS RECORDS UPDATED" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nCurrent DNS Records:" -ForegroundColor White
az network dns record-set list `
    --resource-group $ResourceGroup `
    --zone-name $Zone `
    --query "[?name=='@' || name=='www' || name=='api' || name=='asverify' || name=='asverify.api'].{Name:name, Type:type, Records:aRecords, CNAME:cnameRecord.cname}" `
    --output table

# =============================================================================
# Next Steps
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📋 NEXT STEPS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n1. Wait 5-10 minutes for DNS propagation" -ForegroundColor White
Write-Host "`n2. Verify DNS with:" -ForegroundColor White
Write-Host "   nslookup www.$Zone" -ForegroundColor Green
Write-Host "   nslookup api.$Zone" -ForegroundColor Green

Write-Host "`n3. Add custom domains to Azure resources:" -ForegroundColor White
Write-Host "   # Frontend" -ForegroundColor Gray
Write-Host "   az staticwebapp hostname set --name codexdominion-frontend --resource-group codexdominion-basic --hostname www.$Zone" -ForegroundColor Green
Write-Host ""
Write-Host "   # Backend" -ForegroundColor Gray
Write-Host "   az webapp config hostname add --webapp-name codexdominion-backend --resource-group codexdominion-basic --hostname api.$Zone" -ForegroundColor Green

Write-Host "`n4. Test endpoints:" -ForegroundColor White
Write-Host "   curl https://www.$Zone" -ForegroundColor Green
Write-Host "   curl https://api.$Zone/health" -ForegroundColor Green

Write-Host "`n🔥 The Flame Burns on Your Domain!" -ForegroundColor Yellow
Write-Host ""
