#!/usr/bin/env pwsh
# =============================================================================
# Configure Custom Domains for Codex Dominion
# =============================================================================
# This script helps configure codexdominion.app with Azure resources
# =============================================================================

param(
    [string]$Domain = "codexdominion.app",
    [string]$ResourceGroup = "codexdominion-basic",
    [string]$StaticWebApp = "codexdominion-frontend",
    [string]$BackendApp = "codexdominion-backend"
)

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🌐 CUSTOM DOMAIN CONFIGURATION" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# =============================================================================
# Step 1: Get Azure Resource Information
# =============================================================================

Write-Host "`n[1/4] Getting Azure resource information..." -ForegroundColor Cyan

$staticWebAppUrl = az staticwebapp show `
    --name $StaticWebApp `
    --resource-group $ResourceGroup `
    --query "defaultHostname" `
    --output tsv

$backendUrl = az webapp show `
    --name $BackendApp `
    --resource-group $ResourceGroup `
    --query "defaultHostName" `
    --output tsv

Write-Host "✓ Frontend URL: $staticWebAppUrl" -ForegroundColor Green
Write-Host "✓ Backend URL: $backendUrl" -ForegroundColor Green

# =============================================================================
# Step 2: DNS Configuration Instructions
# =============================================================================

Write-Host "`n[2/4] DNS Configuration Required" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "`nGo to your domain registrar (e.g., Google Domains, GoDaddy)" -ForegroundColor White
Write-Host "`n📋 DNS Records to Add:" -ForegroundColor Yellow
Write-Host ""

Write-Host "Record 1 - Main Domain (Frontend):" -ForegroundColor Cyan
Write-Host "  Type:  CNAME" -ForegroundColor White
Write-Host "  Host:  @" -ForegroundColor White
Write-Host "  Value: $staticWebAppUrl" -ForegroundColor Green
Write-Host "  TTL:   3600" -ForegroundColor White
Write-Host ""

Write-Host "Record 2 - WWW Subdomain:" -ForegroundColor Cyan
Write-Host "  Type:  CNAME" -ForegroundColor White
Write-Host "  Host:  www" -ForegroundColor White
Write-Host "  Value: $staticWebAppUrl" -ForegroundColor Green
Write-Host "  TTL:   3600" -ForegroundColor White
Write-Host ""

Write-Host "Record 3 - API Subdomain (Backend):" -ForegroundColor Cyan
Write-Host "  Type:  CNAME" -ForegroundColor White
Write-Host "  Host:  api" -ForegroundColor White
Write-Host "  Value: $backendUrl" -ForegroundColor Green
Write-Host "  TTL:   3600" -ForegroundColor White
Write-Host ""

Write-Host "⏱️  Wait 5-30 minutes for DNS propagation after making changes" -ForegroundColor Yellow

# =============================================================================
# Step 3: Configure Custom Domain in Azure Static Web App
# =============================================================================

Write-Host "`n[3/4] Azure Static Web App Custom Domain Setup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow

Write-Host "`nAfter DNS is configured, run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "# Add main domain" -ForegroundColor Gray
Write-Host "az staticwebapp hostname set ``" -ForegroundColor Green
Write-Host "    --name $StaticWebApp ``" -ForegroundColor Green
Write-Host "    --resource-group $ResourceGroup ``" -ForegroundColor Green
Write-Host "    --hostname $Domain" -ForegroundColor Green
Write-Host ""
Write-Host "# Add www subdomain" -ForegroundColor Gray
Write-Host "az staticwebapp hostname set ``" -ForegroundColor Green
Write-Host "    --name $StaticWebApp ``" -ForegroundColor Green
Write-Host "    --resource-group $ResourceGroup ``" -ForegroundColor Green
Write-Host "    --hostname www.$Domain" -ForegroundColor Green

# =============================================================================
# Step 4: Configure Custom Domain for Backend
# =============================================================================

Write-Host "`n[4/4] Backend API Custom Domain Setup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Yellow

Write-Host "`nAfter DNS is configured, run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "# Add API subdomain" -ForegroundColor Gray
Write-Host "az webapp config hostname add ``" -ForegroundColor Green
Write-Host "    --webapp-name $BackendApp ``" -ForegroundColor Green
Write-Host "    --resource-group $ResourceGroup ``" -ForegroundColor Green
Write-Host "    --hostname api.$Domain" -ForegroundColor Green
Write-Host ""
Write-Host "# Bind SSL certificate (automatic)" -ForegroundColor Gray
Write-Host "az webapp config ssl bind ``" -ForegroundColor Green
Write-Host "    --name $BackendApp ``" -ForegroundColor Green
Write-Host "    --resource-group $ResourceGroup ``" -ForegroundColor Green
Write-Host "    --certificate-thumbprint auto ``" -ForegroundColor Green
Write-Host "    --ssl-type SNI" -ForegroundColor Green

# =============================================================================
# Verification Commands
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ VERIFICATION COMMANDS" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nAfter DNS propagation, verify with:" -ForegroundColor White
Write-Host ""
Write-Host "# Check DNS resolution" -ForegroundColor Gray
Write-Host "nslookup $Domain" -ForegroundColor Green
Write-Host "nslookup www.$Domain" -ForegroundColor Green
Write-Host "nslookup api.$Domain" -ForegroundColor Green
Write-Host ""
Write-Host "# Test HTTPS endpoints" -ForegroundColor Gray
Write-Host "curl https://$Domain" -ForegroundColor Green
Write-Host "curl https://www.$Domain" -ForegroundColor Green
Write-Host "curl https://api.$Domain/health" -ForegroundColor Green

# =============================================================================
# Summary
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  📋 NEXT STEPS SUMMARY" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n1. ✅ Configure DNS records at your registrar (see above)" -ForegroundColor White
Write-Host "2. ⏱️  Wait 5-30 minutes for DNS propagation" -ForegroundColor White
Write-Host "3. 🔧 Run Azure hostname configuration commands (see above)" -ForegroundColor White
Write-Host "4. ✅ Verify with nslookup and curl commands" -ForegroundColor White
Write-Host "5. 🎉 Your custom domain will be live!" -ForegroundColor White

Write-Host "`n💡 TIP: Azure provides free SSL certificates automatically!" -ForegroundColor Yellow
Write-Host "🔥 The Flame Burns Sovereign on Your Domain!" -ForegroundColor Yellow
Write-Host ""
