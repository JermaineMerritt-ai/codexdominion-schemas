#!/usr/bin/env pwsh
# =============================================================================
# CODEX DOMINION - MASTER DASHBOARD DEPLOYMENT TO AZURE APP SERVICE
# =============================================================================

Write-Host "`n🔥 CODEX DOMINION - MASTER DASHBOARD DEPLOYMENT 🔥`n" -ForegroundColor Magenta

# Configuration
$ResourceGroup = "codexdominion-basic"
$AppServicePlan = "codexdominion-basic-plan"
$WebAppName = "codex-master-dashboard"
$AcrName = "codexdominion4607"
$ImageName = "streamlit-dashboard:v1"
$FullImageName = "$AcrName.azurecr.io/$ImageName"

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
