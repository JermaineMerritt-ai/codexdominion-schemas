#!/usr/bin/env pwsh
# =============================================================================
# CODEX DOMINION - MASTER DASHBOARD DEPLOYMENT TO AZURE CONTAINER APPS
# =============================================================================

Write-Host "`n🔥 MASTER DASHBOARD - AZURE CONTAINER APPS DEPLOYMENT 🔥`n" -ForegroundColor Magenta

# Configuration
$ResourceGroup = "codex-rg"
$Location = "eastus2"
$ContainerRegistry = "codexdominionacr"
$AppName = "codex-master-dashboard"
$Environment = "codex-env"
$ImageTag = "latest"
$FullImageName = "$ContainerRegistry.azurecr.io/master-dashboard:$ImageTag"

Write-Host "📦 Configuration:" -ForegroundColor Cyan
Write-Host "  Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Container Registry: $ContainerRegistry" -ForegroundColor White
Write-Host "  App Name: $AppName" -ForegroundColor White
Write-Host "  Image: $FullImageName`n" -ForegroundColor White

# Step 1: Check Azure authentication
Write-Host "🔐 Step 1: Checking Azure authentication..." -ForegroundColor Cyan
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ Not logged in to Azure!" -ForegroundColor Red
    Write-Host "   Please run: az login" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "   Subscription: $($account.name)`n" -ForegroundColor Gray

# Step 2: Build Docker image
Write-Host "🐳 Step 2: Building Docker image..." -ForegroundColor Cyan
Write-Host "   This may take 2-3 minutes...`n" -ForegroundColor Gray
docker build -f Dockerfile.dashboard -t $FullImageName .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker image built successfully`n" -ForegroundColor Green

# Step 3: Login to Azure Container Registry
Write-Host "🔐 Step 3: Logging in to Azure Container Registry..." -ForegroundColor Cyan
az acr login --name $ContainerRegistry
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ACR login failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in to ACR`n" -ForegroundColor Green

# Step 4: Push image to registry
Write-Host "📤 Step 4: Pushing image to Azure Container Registry..." -ForegroundColor Cyan
Write-Host "   This may take 3-5 minutes...`n" -ForegroundColor Gray
docker push $FullImageName
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Image push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Image pushed successfully`n" -ForegroundColor Green

# Step 5: Check if Container Apps environment exists
Write-Host "🔍 Step 5: Checking Container Apps environment..." -ForegroundColor Cyan
$envExists = az containerapp env show --name $Environment --resource-group $ResourceGroup 2>$null
if (-not $envExists) {
    Write-Host "   Creating environment (this may take 5-10 minutes)..." -ForegroundColor Yellow
    az containerapp env create `
        --name $Environment `
        --resource-group $ResourceGroup `
        --location $Location
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Environment creation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Environment created`n" -ForegroundColor Green
} else {
    Write-Host "✅ Environment exists`n" -ForegroundColor Green
}

# Step 6: Deploy or update Container App
Write-Host "🚀 Step 6: Deploying Master Dashboard..." -ForegroundColor Cyan
$appExists = az containerapp show --name $AppName --resource-group $ResourceGroup 2>$null

if ($appExists) {
    Write-Host "   Updating existing app...`n" -ForegroundColor Yellow
    az containerapp update `
        --name $AppName `
        --resource-group $ResourceGroup `
        --image $FullImageName
} else {
    Write-Host "   Creating new app...`n" -ForegroundColor Yellow
    az containerapp create `
        --name $AppName `
        --resource-group $ResourceGroup `
        --environment $Environment `
        --image $FullImageName `
        --target-port 5000 `
        --ingress external `
        --min-replicas 1 `
        --max-replicas 3 `
        --cpu 1 `
        --memory 2Gi `
        --registry-server "$ContainerRegistry.azurecr.io"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Deployment successful!`n" -ForegroundColor Green

# Step 7: Get app URL
Write-Host "🌐 Step 7: Retrieving application URL..." -ForegroundColor Cyan
$fqdn = az containerapp show `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query "properties.configuration.ingress.fqdn" `
    --output tsv

$appUrl = "https://$fqdn"

Write-Host "`n✅ DEPLOYMENT COMPLETE! ✅`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "`n👑 YOUR MASTER DASHBOARD IS LIVE:`n" -ForegroundColor Magenta
Write-Host "   $appUrl`n" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n📋 Dashboard Features:" -ForegroundColor Cyan
Write-Host "   • 48 Intelligence Engines (6 Clusters)" -ForegroundColor White
Write-Host "   • 6 Codex Tools Suite" -ForegroundColor White
Write-Host "   • 52+ Integrated Dashboards" -ForegroundColor White
Write-Host "   • Health Monitoring" -ForegroundColor White
Write-Host "   • Auto-scaling (1-3 replicas)" -ForegroundColor White

Write-Host "`n🔗 Quick Links:" -ForegroundColor Cyan
Write-Host "   Dashboard:    $appUrl" -ForegroundColor White
Write-Host "   Health Check: $appUrl/api/health" -ForegroundColor White
Write-Host "   Engines:      $appUrl/engines" -ForegroundColor White
Write-Host "   Tools:        $appUrl/tools" -ForegroundColor White
Write-Host "   Dashboards:   $appUrl/dashboards`n" -ForegroundColor White

Write-Host "📊 View Logs:" -ForegroundColor Cyan
Write-Host "   az containerapp logs show --name $AppName --resource-group $ResourceGroup --follow`n" -ForegroundColor White

Write-Host "🔧 Manage App:" -ForegroundColor Cyan
Write-Host "   View in Portal: https://portal.azure.com" -ForegroundColor White
Write-Host "   Restart: az containerapp restart --name $AppName --resource-group $ResourceGroup`n" -ForegroundColor White

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Magenta

Write-Host "📦 Configuration:" -ForegroundColor Cyan
Write-Host "  Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "  App Service Plan: $AppServicePlan" -ForegroundColor White
Write-Host "  Web App: $WebAppName" -ForegroundColor White
Write-Host "  Container Image: $FullImageName`n" -ForegroundColor White

# Step 1: Get ACR credentials
Write-Host "🔐 Step 1: Getting ACR credentials..." -ForegroundColor Cyan
$acrUser = az acr credential show --name $AcrName --query "username" -o tsv
$acrPass = az acr credential show --name $AcrName --query "passwords[0].value" -o tsv

if (-not $acrUser -or -not $acrPass) {
    Write-Host "❌ Failed to get ACR credentials!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ ACR credentials retrieved`n" -ForegroundColor Green

# Step 2: Check if web app exists
Write-Host "🔍 Step 2: Checking if web app exists..." -ForegroundColor Cyan
$existingApp = az webapp show --name $WebAppName --resource-group $ResourceGroup 2>$null

if ($existingApp) {
    Write-Host "✅ Web app exists. Updating configuration...`n" -ForegroundColor Yellow
} else {
    Write-Host "📦 Creating new web app..." -ForegroundColor Yellow
    az webapp create `
        --resource-group $ResourceGroup `
        --plan $AppServicePlan `
        --name $WebAppName `
        --runtime "PYTHON:3.10"
    Write-Host "✅ Web app created`n" -ForegroundColor Green
}

# Step 3: Configure container settings
Write-Host "🔧 Step 3: Configuring container settings..." -ForegroundColor Cyan
az webapp config container set `
    --name $WebAppName `
    --resource-group $ResourceGroup `
    --docker-custom-image-name $FullImageName `
    --docker-registry-server-url "https://$AcrName.azurecr.io" `
    --docker-registry-server-user $acrUser `
    --docker-registry-server-password $acrPass

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to configure container!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Container configured`n" -ForegroundColor Green

# Step 4: Configure Streamlit port
Write-Host "🔧 Step 4: Configuring Streamlit port (8501)..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name $WebAppName `
    --resource-group $ResourceGroup `
    --settings WEBSITES_PORT=8501

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to set port!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Port configured`n" -ForegroundColor Green

# Step 5: Enable container logging
Write-Host "📝 Step 5: Enabling container logging..." -ForegroundColor Cyan
az webapp log config `
    --name $WebAppName `
    --resource-group $ResourceGroup `
    --docker-container-logging filesystem

Write-Host "✅ Logging enabled`n" -ForegroundColor Green

# Step 6: Restart web app
Write-Host "🔄 Step 6: Restarting web app..." -ForegroundColor Cyan
az webapp restart --name $WebAppName --resource-group $ResourceGroup
Write-Host "✅ Web app restarted`n" -ForegroundColor Green

# Step 7: Get web app URL
Write-Host "🌐 Step 7: Getting web app URL..." -ForegroundColor Cyan
$appUrl = az webapp show `
    --name $WebAppName `
    --resource-group $ResourceGroup `
    --query "defaultHostName" -o tsv

$fullUrl = "https://$appUrl"

Write-Host "`n✅ DEPLOYMENT COMPLETE! ✅`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "`n🎯 YOUR MASTER DASHBOARD IS LIVE:`n" -ForegroundColor Magenta
Write-Host "   $fullUrl`n" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n📋 Features Available:" -ForegroundColor Cyan
Write-Host "   • Revenue & Balances Tracking" -ForegroundColor White
Write-Host "   • Transaction Management" -ForegroundColor White
Write-Host "   • Daily/Seasonal/Epochal Cycles" -ForegroundColor White
Write-Host "   • Platform Analytics" -ForegroundColor White
Write-Host "   • AI Command Center (Give Your Prompts Here!)" -ForegroundColor White

Write-Host "`n📊 View Logs:" -ForegroundColor Cyan
Write-Host "   az webapp log tail --name $WebAppName --resource-group $ResourceGroup`n" -ForegroundColor White

Write-Host "`n🔧 Troubleshooting:" -ForegroundColor Cyan
Write-Host "   If the app shows an error, wait 2-3 minutes for container to pull and start" -ForegroundColor Yellow
Write-Host "   Check logs: az webapp log tail --name $WebAppName --resource-group $ResourceGroup`n" -ForegroundColor Yellow

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Magenta
