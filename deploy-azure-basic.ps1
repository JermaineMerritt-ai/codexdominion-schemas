#!/usr/bin/env pwsh
# =============================================================================
# Codex Dominion - Azure Basic Deployment (No Quota Required)
# =============================================================================

param(
    [string]$ResourceGroup = "codexdominion-basic",
    [string]$Location = "westus2"  # Try different region
)

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔥 CODEX DOMINION - AZURE BASIC DEPLOYMENT 🔥" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Check Azure login
$account = az account show 2>&1 | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ Not logged in. Run: az login" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Logged in as: $($account.user.name)" -ForegroundColor Green

# Create Resource Group
Write-Host "`n[1/4] Creating resource group..." -ForegroundColor Cyan
az group create --name $ResourceGroup --location $Location --output none
Write-Host "✓ Resource group created" -ForegroundColor Green

# Create App Service Plan (B1 Basic - No quota required)
Write-Host "`n[2/4] Creating App Service Plan (Basic)..." -ForegroundColor Cyan
az appservice plan create `
    --name "codexdominion-basic-plan" `
    --resource-group $ResourceGroup `
    --is-linux `
    --sku B1 `
    --location $Location `
    --output none
Write-Host "✓ App Service Plan created (B1)" -ForegroundColor Green

# Create Static Web App for Frontend (FREE tier)
Write-Host "`n[3/4] Creating Static Web App for Frontend..." -ForegroundColor Cyan
$staticApp = az staticwebapp create `
    --name "codexdominion-frontend" `
    --resource-group $ResourceGroup `
    --location $Location `
    --sku Free `
    --output json | ConvertFrom-Json

$deploymentToken = $staticApp.properties.apiKey
$frontendUrl = $staticApp.defaultHostname

Write-Host "✓ Static Web App created" -ForegroundColor Green
Write-Host "   URL: https://$frontendUrl" -ForegroundColor Gray

# Create Web App for Backend (Python on Linux)
Write-Host "`n[4/4] Creating Web App for Backend..." -ForegroundColor Cyan
az webapp create `
    --name "codexdominion-backend" `
    --resource-group $ResourceGroup `
    --plan "codexdominion-basic-plan" `
    --runtime "PYTHON:3.11" `
    --output none

Write-Host "✓ Backend Web App created" -ForegroundColor Green

# Configure backend
Write-Host "`nConfiguring backend..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name "codexdominion-backend" `
    --resource-group $ResourceGroup `
    --settings `
        PYTHON_VERSION="3.11" `
        SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
        DATABASE_URL="sqlite:///./codex.db" `
        PORT="8000" `
    --output none

# Get backend URL
$backendUrl = az webapp show `
    --name "codexdominion-backend" `
    --resource-group $ResourceGroup `
    --query defaultHostName `
    --output tsv

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✨ DEPLOYMENT COMPLETE! ✨" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`n📌 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Add GitHub Secret:" -ForegroundColor White
Write-Host "   Name:  AZURE_STATIC_WEB_APPS_API_TOKEN_BASIC" -ForegroundColor Gray
Write-Host "   Value: $deploymentToken" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Application URLs:" -ForegroundColor White
Write-Host "   Frontend: https://$frontendUrl" -ForegroundColor Gray
Write-Host "   Backend:  https://$backendUrl" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy Code:" -ForegroundColor White
Write-Host "   git push (triggers GitHub Actions)" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Monthly Cost: ~$13.87 (B1 tier)" -ForegroundColor Cyan
Write-Host "🔥 The Flame Burns Sovereign!" -ForegroundColor Yellow
