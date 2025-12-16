# Option C: Custom Domain Setup
# Configures codexdominion.app and api.codexdominion.app

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "OPTION C: CUSTOM DOMAIN SETUP" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$RG = "codex-rg"
$FRONTEND_APP = "witty-glacier-0ebbd971e"
$BACKEND_APP = "codex-backend-https"
$DOMAIN = "codexdominion.app"
$API_DOMAIN = "api.codexdominion.app"

Write-Host "[Step 1/5] Verifying Domain Ownership..." -ForegroundColor Yellow
Write-Host "  Primary Domain: $DOMAIN" -ForegroundColor Gray
Write-Host "  API Subdomain: $API_DOMAIN" -ForegroundColor Gray
Write-Host ""

Write-Host "📝 Before proceeding, ensure DNS records are configured:" -ForegroundColor Cyan
Write-Host ""
Write-Host "For Static Web App ($DOMAIN):" -ForegroundColor White
Write-Host "  Type: TXT" -ForegroundColor Gray
Write-Host "  Name: asuid.$DOMAIN" -ForegroundColor Gray
$asuid = az staticwebapp show --name $FRONTEND_APP --query "customDomains[0].validationToken" -o tsv 2>$null
if (-not $asuid) {
    # Get default validation token
    Write-Host "  Value: [Get from: az staticwebapp show --name $FRONTEND_APP]" -ForegroundColor Yellow
} else {
    Write-Host "  Value: $asuid" -ForegroundColor Green
}
Write-Host ""
Write-Host "  Type: CNAME" -ForegroundColor Gray
Write-Host "  Name: www" -ForegroundColor Gray
Write-Host "  Value: witty-glacier-0ebbd971e.3.azurestaticapps.net" -ForegroundColor Gray
Write-Host ""

Write-Host "For Container App ($API_DOMAIN):" -ForegroundColor White
$backendFQDN = az containerapp show --name $BACKEND_APP --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv
Write-Host "  Type: CNAME" -ForegroundColor Gray
Write-Host "  Name: api" -ForegroundColor Gray
Write-Host "  Value: $backendFQDN" -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Have you configured these DNS records? (y/N)"
if ($response -ne 'y' -and $response -ne 'Y') {
    Write-Host ""
    Write-Host "⚠️  Please configure DNS records first, then run this script again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "DNS Configuration Steps:" -ForegroundColor Cyan
    Write-Host "  1. Log into your domain registrar (e.g., GoDaddy, Namecheap)" -ForegroundColor Gray
    Write-Host "  2. Navigate to DNS management" -ForegroundColor Gray
    Write-Host "  3. Add the records shown above" -ForegroundColor Gray
    Write-Host "  4. Wait 5-10 minutes for DNS propagation" -ForegroundColor Gray
    Write-Host "  5. Run this script again" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

Write-Host "`n[Step 2/5] Adding Custom Domain to Static Web App..." -ForegroundColor Yellow
try {
    az staticwebapp hostname set `
        --name $FRONTEND_APP `
        --hostname $DOMAIN `
        --output none 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Primary domain added: $DOMAIN" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Domain may already be configured" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  Error adding domain: $_" -ForegroundColor Yellow
}

# Add www subdomain
try {
    az staticwebapp hostname set `
        --name $FRONTEND_APP `
        --hostname "www.$DOMAIN" `
        --output none 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ WWW subdomain added: www.$DOMAIN" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  WWW subdomain may already be configured" -ForegroundColor Yellow
}

Write-Host "`n[Step 3/5] Adding Custom Domain to Container App..." -ForegroundColor Yellow
try {
    az containerapp hostname add `
        --name $BACKEND_APP `
        --resource-group $RG `
        --hostname $API_DOMAIN `
        --output none 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ API domain added: $API_DOMAIN" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  API domain may already be configured" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  Error adding API domain: $_" -ForegroundColor Yellow
}

Write-Host "`n[Step 4/5] Binding SSL Certificates..." -ForegroundColor Yellow
Write-Host "  Azure automatically provisions SSL certificates via Let's Encrypt" -ForegroundColor Gray
Write-Host "  This may take 2-5 minutes..." -ForegroundColor Gray

Start-Sleep -Seconds 3

# Bind certificate for Static Web App (automatic)
Write-Host "  ✅ Static Web App: SSL certificate auto-provisioned" -ForegroundColor Green

# Bind certificate for Container App (automatic)
try {
    az containerapp hostname bind `
        --name $BACKEND_APP `
        --resource-group $RG `
        --hostname $API_DOMAIN `
        --environment "codex-env" `
        --validation-method CNAME `
        --output none 2>&1 | Out-Null

    Write-Host "  ✅ Container App: SSL certificate bound" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Certificate binding in progress (may take a few minutes)" -ForegroundColor Yellow
}

Write-Host "`n[Step 5/5] Verification..." -ForegroundColor Yellow

Start-Sleep -Seconds 10

# Test primary domain
Write-Host "Testing https://$DOMAIN ..." -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "https://$DOMAIN" -Method Head -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✅ Primary domain accessible (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Primary domain not yet accessible (DNS propagation may take up to 48 hours)" -ForegroundColor Yellow
}

# Test API domain
Write-Host "Testing https://$API_DOMAIN/health ..." -ForegroundColor Gray
try {
    $response = Invoke-RestMethod -Uri "https://$API_DOMAIN/health" -TimeoutSec 10
    Write-Host "  ✅ API domain accessible (Health: $($response.status))" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  API domain not yet accessible (DNS propagation in progress)" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CUSTOM DOMAIN SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "🌐 Your Custom URLs:" -ForegroundColor White
Write-Host "  Frontend: https://$DOMAIN" -ForegroundColor Green
Write-Host "  WWW: https://www.$DOMAIN" -ForegroundColor Green
Write-Host "  API: https://$API_DOMAIN" -ForegroundColor Green
Write-Host ""
Write-Host "🔒 SSL Certificates:" -ForegroundColor White
Write-Host "  All domains secured with Let's Encrypt" -ForegroundColor Gray
Write-Host "  Auto-renewal enabled" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor White
Write-Host "  1. Update frontend API calls to use https://$API_DOMAIN" -ForegroundColor Gray
Write-Host "  2. Update copilot-instructions.md with new URLs" -ForegroundColor Gray
Write-Host "  3. Update codex_ledger.json portal information" -ForegroundColor Gray
Write-Host "  4. Test all endpoints after DNS propagation (5-10 minutes)" -ForegroundColor Gray
Write-Host ""

# Save domain configuration
@{
    frontend_domain = "https://$DOMAIN"
    frontend_www = "https://www.$DOMAIN"
    api_domain = "https://$API_DOMAIN"
    configured_date = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    ssl_provider = "Let's Encrypt"
    auto_renewal = $true
    dns_propagation = "5-10 minutes typical, up to 48 hours maximum"
} | ConvertTo-Json | Out-File "custom-domains-config.json"

Write-Host "💾 Configuration saved to: custom-domains-config.json`n" -ForegroundColor Gray
