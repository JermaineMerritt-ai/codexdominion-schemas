# Azure Backend Deployment - FREE TIER (No Redis)
# Run this script to deploy Codex Dominion backend to Azure using Free tier

Write-Host "🔥 Codex Dominion - Azure Backend Deployment (FREE TIER)" -ForegroundColor Cyan
Write-Host "=========================================================`n" -ForegroundColor Cyan

# Configuration
$RESOURCE_GROUP = "codex-dominion-rg"
$LOCATION = "eastus"
$BACKEND_NAME = "codex-dominion-backend"
$PLAN_NAME = "codex-dominion-plan"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Resource Group: $RESOURCE_GROUP" -ForegroundColor Gray
Write-Host "   Location: $LOCATION" -ForegroundColor Gray
Write-Host "   Backend: $BACKEND_NAME" -ForegroundColor Gray
Write-Host "   Tier: F1 (Free)" -ForegroundColor Gray
Write-Host "   Redis: Skipped (using in-memory cache)`n" -ForegroundColor Gray

$confirm = Read-Host "Deploy to Azure? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit
}

Write-Host "`n🔐 Step 1: Azure Login" -ForegroundColor Cyan
az login

Write-Host "`n📦 Step 2: Create Resource Group" -ForegroundColor Cyan
az group create --name $RESOURCE_GROUP --location $LOCATION

Write-Host "`n🏗️  Step 3: Create App Service Plan (Free Tier)" -ForegroundColor Cyan
az appservice plan create `
    --name $PLAN_NAME `
    --resource-group $RESOURCE_GROUP `
    --is-linux `
    --sku F1

Write-Host "`n🐳 Step 4: Deploy Backend Container" -ForegroundColor Cyan
az webapp create `
    --resource-group $RESOURCE_GROUP `
    --plan $PLAN_NAME `
    --name $BACKEND_NAME `
    --deployment-container-image-name jmerritt48/codex-dominion-backend:2.0.0

Write-Host "`n🔐 Step 5: Generate Secure Secrets" -ForegroundColor Cyan
function New-SecureSecret {
    -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object { [char]$_ })
}

$SECRET_KEY = New-SecureSecret
$JWT_SECRET = New-SecureSecret
$API_KEY = New-SecureSecret

Write-Host "`n⚙️  Step 6: Configure Environment Variables" -ForegroundColor Cyan
az webapp config appsettings set `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_NAME `
    --settings `
        DATABASE_URL="sqlite:///./codex_dominion.db" `
        SECRET_KEY="$SECRET_KEY" `
        JWT_SECRET="$JWT_SECRET" `
        API_KEY="$API_KEY" `
        REDIS_URL="" `
        ENVIRONMENT="production" `
        WEBSITES_PORT="8001"

Write-Host "`n🔒 Step 7: Enable HTTPS Only" -ForegroundColor Cyan
az webapp update `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_NAME `
    --https-only true

Write-Host "`n🌐 Step 8: Configure CORS" -ForegroundColor Cyan
az webapp cors add `
    --resource-group $RESOURCE_GROUP `
    --name $BACKEND_NAME `
    --allowed-origins "https://codexdominion.app" "https://www.codexdominion.app"

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$BACKEND_URL = "https://$BACKEND_NAME.azurewebsites.net"

Write-Host "`n🌐 Backend URL:" -ForegroundColor Cyan
Write-Host "   $BACKEND_URL" -ForegroundColor White
Write-Host "   Health Check: $BACKEND_URL/health`n" -ForegroundColor Gray

Write-Host "📋 Save these secrets (you'll need them):" -ForegroundColor Yellow
Write-Host "   SECRET_KEY: $SECRET_KEY" -ForegroundColor Gray
Write-Host "   JWT_SECRET: $JWT_SECRET" -ForegroundColor Gray
Write-Host "   API_KEY: $API_KEY`n" -ForegroundColor Gray

Write-Host "📌 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Test backend: curl $BACKEND_URL/health" -ForegroundColor Gray
Write-Host "   2. Configure custom domain (optional):" -ForegroundColor Gray
Write-Host "      - Add CNAME in IONOS: api → $BACKEND_NAME.azurewebsites.net" -ForegroundColor Gray
Write-Host "      - Run: az webapp config hostname add --webapp-name $BACKEND_NAME --resource-group $RESOURCE_GROUP --hostname api.CodexDominion.app" -ForegroundColor Gray
Write-Host "   3. Update frontend .env with: NEXT_PUBLIC_API_URL=$BACKEND_URL`n" -ForegroundColor Gray

# Save deployment info
$deploymentInfo = @{
    resource_group = $RESOURCE_GROUP
    backend_name = $BACKEND_NAME
    backend_url = $BACKEND_URL
    location = $LOCATION
    tier = "F1 (Free)"
    secrets = @{
        secret_key = $SECRET_KEY
        jwt_secret = $JWT_SECRET
        api_key = $API_KEY
    }
    deployed_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
} | ConvertTo-Json

$deploymentInfo | Out-File "azure-deployment-info.json" -Encoding UTF8

Write-Host "🔥 The backend reigns eternal in Azure cloud." -ForegroundColor Cyan
Write-Host "💾 Deployment info saved to: azure-deployment-info.json`n" -ForegroundColor Gray
