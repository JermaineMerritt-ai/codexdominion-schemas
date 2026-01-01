#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════════
# DEPLOY CODEX DOMINION TO AZURE CONTAINER APPS
# ═══════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Continue"

$rgName = "codexdominion-prod"
$location = "eastus"
$acrName = "codexacr1216"
$envName = "codex-env"
$appName = "codex-backend"

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║      🚀 DEPLOYING TO AZURE CONTAINER APPS 🚀                 ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

# Check if environment exists
Write-Host "🔍 Checking Container Apps environment..." -ForegroundColor Cyan
$envCheck = az containerapp env show --name $envName --resource-group $rgName 2>$null

if (-not $envCheck) {
    Write-Host "   ❌ Environment not found. Creating..." -ForegroundColor Yellow
    Write-Host "   ⏳ This takes 2-3 minutes...`n" -ForegroundColor Gray
    
    az containerapp env create `
        --name $envName `
        --resource-group $rgName `
        --location $location `
        --output none
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Environment creation failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✅ Environment created`n" -ForegroundColor Green
} else {
    Write-Host "   ✅ Environment ready`n" -ForegroundColor Green
}

# Get ACR credentials
Write-Host "🔑 Getting ACR credentials..." -ForegroundColor Cyan
$acrPassword = az acr credential show --name $acrName --query "passwords[0].value" -o tsv

if (-not $acrPassword) {
    Write-Host "   ❌ Failed to get ACR credentials" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Credentials retrieved`n" -ForegroundColor Green

# Deploy Container App
Write-Host "🚀 Deploying Container App..." -ForegroundColor Cyan
Write-Host "   App: $appName" -ForegroundColor Gray
Write-Host "   Image: ${acrName}.azurecr.io/codex-backend:latest`n" -ForegroundColor Gray

az containerapp create `
    --name $appName `
    --resource-group $rgName `
    --environment $envName `
    --image "${acrName}.azurecr.io/codex-backend:latest" `
    --registry-server "${acrName}.azurecr.io" `
    --registry-username $acrName `
    --registry-password $acrPassword `
    --target-port 5000 `
    --ingress external `
    --cpu 1.0 `
    --memory 2.0Gi `
    --min-replicas 1 `
    --max-replicas 3 `
    --env-vars `
        CODEX_ENVIRONMENT=production `
        CODEX_CLOUD_PROVIDER=azure `
        FLASK_APP=flask_dashboard `
        PYTHONUNBUFFERED=1 `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n   ❌ Deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n   ✅ Deployment successful!`n" -ForegroundColor Green

# Get app URL
Write-Host "🔍 Getting application URL..." -ForegroundColor Cyan
$appUrl = az containerapp show `
    --name $appName `
    --resource-group $rgName `
    --query "properties.configuration.ingress.fqdn" `
    -o tsv

if ($appUrl) {
    Write-Host "   ✅ Application URL: https://$appUrl`n" -ForegroundColor Green
    
    # Test health endpoint
    Write-Host "🏥 Testing health endpoint..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    try {
        $response = Invoke-WebRequest -Uri "https://$appUrl/health" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Health check passed!" -ForegroundColor Green
            Write-Host "   Response: $($response.Content)`n" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   ⚠️  Health check pending (app may still be starting)..." -ForegroundColor Yellow
        Write-Host "   You can check manually: https://$appUrl/health`n" -ForegroundColor Gray
    }
    
    # Display summary
    Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    🎉 DEPLOYMENT COMPLETE! 🎉                 ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
    
    Write-Host "📊 Your Flask Backend is LIVE!" -ForegroundColor Cyan
    Write-Host "`n🔗 URLs:" -ForegroundColor Yellow
    Write-Host "   Backend:  https://$appUrl" -ForegroundColor White
    Write-Host "   Health:   https://$appUrl/health" -ForegroundColor White
    Write-Host "   API:      https://$appUrl/api/..." -ForegroundColor White
    
    Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Test your backend: curl https://$appUrl/health" -ForegroundColor White
    Write-Host "   2. Build Next.js frontend with backend URL" -ForegroundColor White
    Write-Host "   3. Deploy frontend to IONOS VPS" -ForegroundColor White
    Write-Host "   4. Configure DNS at codexdominion.app`n" -ForegroundColor White
    
    Write-Host "🔥 The Dominion's Core is ALIVE! 👑`n" -ForegroundColor Yellow
    
} else {
    Write-Host "   ⚠️  Could not retrieve URL. Check manually with:" -ForegroundColor Yellow
    Write-Host "   az containerapp show --name $appName --resource-group $rgName --query 'properties.configuration.ingress.fqdn' -o tsv`n" -ForegroundColor Gray
}
