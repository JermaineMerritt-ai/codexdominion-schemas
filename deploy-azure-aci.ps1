# Azure Backend Deployment - Container Instances
# Uses Azure Container Instances (ACI) instead of App Service

Write-Host "🔥 Codex Dominion - Azure Container Instances Deployment" -ForegroundColor Cyan
Write-Host "==========================================================`n" -ForegroundColor Cyan

# Configuration
$RESOURCE_GROUP = "codex-dominion-rg"
$LOCATION = "eastus"
$CONTAINER_NAME = "codex-dominion-backend"
$DNS_NAME = "codex-dominion-backend"
$IMAGE = "jmerritt48/codex-dominion-backend:2.0.0"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Resource Group: $RESOURCE_GROUP" -ForegroundColor Gray
Write-Host "   Location: $LOCATION" -ForegroundColor Gray
Write-Host "   Container: $CONTAINER_NAME" -ForegroundColor Gray
Write-Host "   DNS: $DNS_NAME.$LOCATION.azurecontainer.io" -ForegroundColor Gray
Write-Host "   Image: $IMAGE`n" -ForegroundColor Gray

$confirm = Read-Host "Deploy to Azure? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit
}

Write-Host "`n🔐 Step 1: Azure Login" -ForegroundColor Cyan
az login

Write-Host "`n📦 Step 2: Create Resource Group" -ForegroundColor Cyan
az group create --name $RESOURCE_GROUP --location $LOCATION

Write-Host "`n🔐 Step 3: Generate Secure Secrets" -ForegroundColor Cyan
function New-SecureSecret {
    -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object { [char]$_ })
}

$SECRET_KEY = New-SecureSecret
$JWT_SECRET = New-SecureSecret
$API_KEY = New-SecureSecret

Write-Host "`n🐳 Step 4: Deploy Container Instance" -ForegroundColor Cyan
az container create `
    --resource-group $RESOURCE_GROUP `
    --name $CONTAINER_NAME `
    --image $IMAGE `
    --dns-name-label $DNS_NAME `
    --os-type Linux `
    --ports 8001 `
    --cpu 1 `
    --memory 1 `
    --environment-variables `
        DATABASE_URL="sqlite:///./codex_dominion.db" `
        SECRET_KEY="$SECRET_KEY" `
        JWT_SECRET="$JWT_SECRET" `
        API_KEY="$API_KEY" `
        REDIS_URL="" `
        ENVIRONMENT="production" `
        PORT="8001"

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$BACKEND_URL = "http://$DNS_NAME.$LOCATION.azurecontainer.io:8001"

Write-Host "`n🌐 Backend URL:" -ForegroundColor Cyan
Write-Host "   $BACKEND_URL" -ForegroundColor White
Write-Host "   Health Check: $BACKEND_URL/health`n" -ForegroundColor Gray

Write-Host "📋 Save these secrets (you'll need them):" -ForegroundColor Yellow
Write-Host "   SECRET_KEY: $SECRET_KEY" -ForegroundColor Gray
Write-Host "   JWT_SECRET: $JWT_SECRET" -ForegroundColor Gray
Write-Host "   API_KEY: $API_KEY`n" -ForegroundColor Gray

Write-Host "⚠️  Note: Container Instance uses HTTP (not HTTPS)" -ForegroundColor Yellow
Write-Host "   For production HTTPS, you'll need to:" -ForegroundColor Yellow
Write-Host "   1. Set up Application Gateway with SSL" -ForegroundColor Yellow
Write-Host "   2. Or use Cloudflare proxy for SSL termination`n" -ForegroundColor Yellow

Write-Host "📌 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Test backend: curl $BACKEND_URL/health" -ForegroundColor Gray
Write-Host "   2. Update frontend .env with: NEXT_PUBLIC_API_URL=$BACKEND_URL" -ForegroundColor Gray
Write-Host "   3. Configure Cloudflare for HTTPS (recommended)`n" -ForegroundColor Gray

# Save deployment info
$deploymentInfo = @{
    resource_group = $RESOURCE_GROUP
    container_name = $CONTAINER_NAME
    backend_url = $BACKEND_URL
    location = $LOCATION
    deployment_type = "Azure Container Instances"
    secrets = @{
        secret_key = $SECRET_KEY
        jwt_secret = $JWT_SECRET
        api_key = $API_KEY
    }
    deployed_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
} | ConvertTo-Json

$deploymentInfo | Out-File "azure-deployment-info.json" -Encoding UTF8

Write-Host "🔥 The backend reigns eternal in Azure Container Instances." -ForegroundColor Cyan
Write-Host "💾 Deployment info saved to: azure-deployment-info.json`n" -ForegroundColor Gray
