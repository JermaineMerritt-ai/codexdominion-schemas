#!/usr/bin/env pwsh
# =============================================================================
# Codex Dominion - Azure Production Deployment Script
# =============================================================================
# Description: Complete deployment script for Azure App Service
# Last Updated: December 7, 2025
# =============================================================================

param(
    [string]$ResourceGroup = "codexdominion-prod",
    [string]$Location = "eastus",
    [switch]$CreateResources,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔥 CODEX DOMINION - AZURE PRODUCTION DEPLOYMENT 🔥" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# =============================================================================
# Pre-Deployment Checks
# =============================================================================

Write-Host "[1/9] Running Pre-Deployment Checks..." -ForegroundColor Cyan

# Check Azure CLI
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "❌ ERROR: Azure CLI is not installed!" -ForegroundColor Red
    Write-Host "Please install from: https://docs.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Azure CLI installed" -ForegroundColor Green

# Check login status
$account = az account show 2>&1 | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ ERROR: Not logged in to Azure!" -ForegroundColor Red
    Write-Host "Please run: az login" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Logged in to Azure as: $($account.user.name)" -ForegroundColor Green

# Check .env.production
if (-not (Test-Path ".\.env.production")) {
    Write-Host "❌ ERROR: .env.production file not found!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Environment configuration found" -ForegroundColor Green

# =============================================================================
# Create Azure Resources
# =============================================================================

if ($CreateResources) {
    Write-Host "`n[2/9] Creating Azure Resources..." -ForegroundColor Cyan

    # Create Resource Group
    Write-Host "Creating resource group..." -ForegroundColor Gray
    az group create --name $ResourceGroup --location $Location --output none
    Write-Host "✓ Resource group created" -ForegroundColor Green

    # Create App Service Plan
    Write-Host "Creating App Service Plan..." -ForegroundColor Gray
    az appservice plan create `
        --name "codexdominion-plan" `
        --resource-group $ResourceGroup `
        --is-linux `
        --sku P1V2 `
        --output none
    Write-Host "✓ App Service Plan created" -ForegroundColor Green

    # Create Web App for Frontend
    Write-Host "Creating Web App for Frontend..." -ForegroundColor Gray
    az webapp create `
        --name "codexdominion" `
        --resource-group $ResourceGroup `
        --plan "codexdominion-plan" `
        --runtime "NODE|18-lts" `
        --output none
    Write-Host "✓ Frontend Web App created" -ForegroundColor Green

    # Create Web App for Backend API
    Write-Host "Creating Web App for Backend API..." -ForegroundColor Gray
    az webapp create `
        --name "codexdominion-api" `
        --resource-group $ResourceGroup `
        --plan "codexdominion-plan" `
        --runtime "PYTHON|3.11" `
        --output none
    Write-Host "✓ Backend Web App created" -ForegroundColor Green

    # Create PostgreSQL Database
    Write-Host "Creating Azure Database for PostgreSQL..." -ForegroundColor Gray
    az postgres flexible-server create `
        --name "codexdominion-db" `
        --resource-group $ResourceGroup `
        --location $Location `
        --admin-user "codexadmin" `
        --admin-password (Read-Host -AsSecureString "Enter database admin password" | ConvertFrom-SecureString -AsPlainText) `
        --sku-name "Standard_B1ms" `
        --tier "Burstable" `
        --storage-size 32 `
        --version 16 `
        --public-access "All" `
        --output none

    az postgres flexible-server db create `
        --resource-group $ResourceGroup `
        --server-name "codexdominion-db" `
        --database-name "codexdominion" `
        --output none
    Write-Host "✓ PostgreSQL database created" -ForegroundColor Green

    # Create Redis Cache
    Write-Host "Creating Azure Cache for Redis..." -ForegroundColor Gray
    az redis create `
        --name "codexdominion" `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku "Basic" `
        --vm-size "C0" `
        --output none
    Write-Host "✓ Redis cache created" -ForegroundColor Green

    # Create Storage Account for Blob Storage
    Write-Host "Creating Storage Account..." -ForegroundColor Gray
    az storage account create `
        --name "codexdominion" `
        --resource-group $ResourceGroup `
        --location $Location `
        --sku "Standard_LRS" `
        --output none

    az storage container create `
        --name "exports" `
        --account-name "codexdominion" `
        --output none
    Write-Host "✓ Storage account created" -ForegroundColor Green

    Write-Host "`n✨ All Azure resources created successfully!" -ForegroundColor Green
} else {
    Write-Host "`n[2/9] Skipping Resource Creation..." -ForegroundColor Yellow
}

# =============================================================================
# Configure Environment Variables
# =============================================================================

Write-Host "`n[3/9] Configuring Environment Variables..." -ForegroundColor Cyan

# Read .env.production
$envVars = @{}
Get-Content ".env.production" | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Configure Frontend Web App
Write-Host "Configuring frontend environment..." -ForegroundColor Gray
$frontendSettings = @(
    "NODE_ENV=production"
    "NEXT_PUBLIC_API_URL=$($envVars['AZURE_API_URL'])"
    "NEXT_PUBLIC_SITE_URL=$($envVars['AZURE_SITE_URL'])"
    "WEBSITE_NODE_DEFAULT_VERSION=~18"
)
az webapp config appsettings set `
    --name "codexdominion" `
    --resource-group $ResourceGroup `
    --settings $frontendSettings `
    --output none

# Configure Backend Web App
Write-Host "Configuring backend environment..." -ForegroundColor Gray
$backendSettings = @(
    "PYTHON_VERSION=3.11"
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true"
    "DATABASE_URL=$($envVars['AZURE_DATABASE_URL'])"
    "REDIS_URL=$($envVars['AZURE_REDIS_URL'])"
    "API_BASE_URL=$($envVars['AZURE_API_URL'])"
    "CORS_ORIGINS=$($envVars['AZURE_SITE_URL'])"
)
az webapp config appsettings set `
    --name "codexdominion-api" `
    --resource-group $ResourceGroup `
    --settings $backendSettings `
    --output none

Write-Host "✓ Environment variables configured" -ForegroundColor Green

# =============================================================================
# Build Application
# =============================================================================

if (-not $SkipBuild) {
    Write-Host "`n[4/9] Building Application..." -ForegroundColor Cyan

    # Build Frontend
    Write-Host "Building frontend..." -ForegroundColor Gray
    Set-Location web
    npm install
    npm run build
    Set-Location ..
    Write-Host "✓ Frontend built" -ForegroundColor Green

    # Backend doesn't need pre-build (done on Azure)
    Write-Host "✓ Backend will build on Azure" -ForegroundColor Green
} else {
    Write-Host "`n[4/9] Skipping Build..." -ForegroundColor Yellow
}

# =============================================================================
# Deploy Frontend
# =============================================================================

Write-Host "`n[5/9] Deploying Frontend to Azure..." -ForegroundColor Cyan

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Gray
Set-Location web
Compress-Archive -Path * -DestinationPath "../frontend-deploy.zip" -Force
Set-Location ..

# Deploy to Azure
Write-Host "Deploying to Azure Web App..." -ForegroundColor Gray
az webapp deployment source config-zip `
    --name "codexdominion" `
    --resource-group $ResourceGroup `
    --src "frontend-deploy.zip" `
    --output none

Remove-Item "frontend-deploy.zip"
Write-Host "✓ Frontend deployed" -ForegroundColor Green

# =============================================================================
# Deploy Backend
# =============================================================================

Write-Host "`n[6/9] Deploying Backend to Azure..." -ForegroundColor Cyan

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Gray
Compress-Archive -Path backend/* -DestinationPath "backend-deploy.zip" -Force

# Deploy to Azure
Write-Host "Deploying to Azure Web App..." -ForegroundColor Gray
az webapp deployment source config-zip `
    --name "codexdominion-api" `
    --resource-group $ResourceGroup `
    --src "backend-deploy.zip" `
    --output none

Remove-Item "backend-deploy.zip"
Write-Host "✓ Backend deployed" -ForegroundColor Green

# =============================================================================
# Configure Custom Domains
# =============================================================================

Write-Host "`n[7/9] Configuring Custom Domains..." -ForegroundColor Cyan

Write-Host "⚠ Manual DNS configuration required:" -ForegroundColor Yellow
Write-Host "   1. Add CNAME record: codexdominion.app -> codexdominion.azurewebsites.net" -ForegroundColor White
Write-Host "   2. Add CNAME record: api.codexdominion.app -> codexdominion-api.azurewebsites.net" -ForegroundColor White
Write-Host "   3. Run these commands after DNS propagation:" -ForegroundColor White
Write-Host ""
Write-Host "   az webapp config hostname add --webapp-name codexdominion -g $ResourceGroup --hostname codexdominion.app" -ForegroundColor Gray
Write-Host "   az webapp config hostname add --webapp-name codexdominion-api -g $ResourceGroup --hostname api.codexdominion.app" -ForegroundColor Gray
Write-Host ""
Write-Host "   az webapp config ssl bind --name codexdominion -g $ResourceGroup --certificate-thumbprint auto --ssl-type SNI" -ForegroundColor Gray
Write-Host "   az webapp config ssl bind --name codexdominion-api -g $ResourceGroup --certificate-thumbprint auto --ssl-type SNI" -ForegroundColor Gray

# =============================================================================
# Run Database Migrations
# =============================================================================

Write-Host "`n[8/9] Running Database Migrations..." -ForegroundColor Cyan

# TODO: Add database migration script
Write-Host "⚠ Manual database setup may be required" -ForegroundColor Yellow

# =============================================================================
# Health Checks
# =============================================================================

Write-Host "`n[9/9] Running Health Checks..." -ForegroundColor Cyan

Start-Sleep -Seconds 10

# Check frontend
try {
    $frontendUrl = az webapp show --name "codexdominion" -g $ResourceGroup --query "defaultHostName" -o tsv
    $response = Invoke-WebRequest -Uri "https://$frontendUrl" -TimeoutSec 30 -UseBasicParsing
    Write-Host "✓ Frontend is healthy: https://$frontendUrl" -ForegroundColor Green
} catch {
    Write-Host "⚠ Frontend health check failed" -ForegroundColor Yellow
}

# Check backend
try {
    $backendUrl = az webapp show --name "codexdominion-api" -g $ResourceGroup --query "defaultHostName" -o tsv
    $response = Invoke-RestMethod -Uri "https://$backendUrl/health" -TimeoutSec 30
    Write-Host "✓ Backend is healthy: https://$backendUrl" -ForegroundColor Green
} catch {
    Write-Host "⚠ Backend health check failed" -ForegroundColor Yellow
}

# =============================================================================
# Deployment Complete
# =============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✨ AZURE DEPLOYMENT COMPLETE! ✨" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Application URLs:" -ForegroundColor Yellow
Write-Host "   Frontend: https://codexdominion.azurewebsites.net" -ForegroundColor White
Write-Host "   API:      https://codexdominion-api.azurewebsites.net" -ForegroundColor White
Write-Host "   Docs:     https://codexdominion-api.azurewebsites.net/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitoring:" -ForegroundColor Yellow
Write-Host "   Portal: https://portal.azure.com" -ForegroundColor White
Write-Host "   Logs:   az webapp log tail --name codexdominion -g $ResourceGroup" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
