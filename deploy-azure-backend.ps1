# Azure Backend Deployment - Azure Container Instances
# Run this script to deploy Codex Dominion backend to Azure ACI

Write-Host "🔥 Codex Dominion - Azure Container Instances Deployment" -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# Configuration
$RESOURCE_GROUP = "codex-dominion-rg"
$LOCATION = "eastus"
$CONTAINER_NAME = "codex-backend"
$DNS_NAME = "codex-backend"
$ACR_NAME = "codexdominionacr"
$IMAGE_NAME = "codex-dominion-backend:latest"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Yellow
Write-Host "   Resource Group: $RESOURCE_GROUP" -ForegroundColor Gray
Write-Host "   Location: $LOCATION" -ForegroundColor Gray
Write-Host "   Container: $CONTAINER_NAME" -ForegroundColor Gray
Write-Host "   ACR: $ACR_NAME" -ForegroundColor Gray
Write-Host "   DNS: $DNS_NAME.eastus.azurecontainer.io`n" -ForegroundColor Gray

$confirm = Read-Host "Deploy to Azure Container Instances? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit
}

Write-Host "`n🔐 Step 1: Azure Login" -ForegroundColor Cyan
az login

Write-Host "`n📦 Step 2: Create Resource Group" -ForegroundColor Cyan
az group create --name $RESOURCE_GROUP --location $LOCATION

Write-Host "`n🏗️  Step 3: Create Azure Container Registry" -ForegroundColor Cyan
az acr create --resource-group $RESOURCE_GROUP `
  --name $ACR_NAME `
  --sku Basic `
  --location $LOCATION

Write-Host "`n🔑 Step 4: Enable ACR Admin & Get Credentials" -ForegroundColor Cyan
az acr update -n $ACR_NAME --admin-enabled true
$ACR_SERVER = az acr show --name $ACR_NAME --query loginServer --output tsv
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username --output tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv

Write-Host "`n🐳 Step 5: Build and Push Docker Image" -ForegroundColor Cyan
Write-Host "   Building image..." -ForegroundColor Gray
cd src\backend
docker build -t $IMAGE_NAME .
cd ..\..

Write-Host "   Logging into ACR: $ACR_SERVER" -ForegroundColor Gray
docker login $ACR_SERVER -u $ACR_USERNAME -p $ACR_PASSWORD

Write-Host "   Tagging and pushing image..." -ForegroundColor Gray
docker tag $IMAGE_NAME "$ACR_SERVER/$IMAGE_NAME"
docker push "$ACR_SERVER/$IMAGE_NAME"

Write-Host "`n🚀 Step 6: Deploy to Azure Container Instances" -ForegroundColor Cyan
Write-Host "`n🚀 Step 6: Deploy to Azure Container Instances" -ForegroundColor Cyan
az container create `
  --resource-group $RESOURCE_GROUP `
  --name $CONTAINER_NAME `
  --image "$ACR_SERVER/$IMAGE_NAME" `
  --dns-name-label $DNS_NAME `
  --ports 8001 `
  --cpu 2 `
  --memory 4 `
  --registry-login-server $ACR_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --environment-variables `
    PYTHON_ENV=production `
    API_HOST=0.0.0.0 `
    API_PORT=8001 `
    DATABASE_URL="sqlite:///./codex_dominion.db" `
  --location $LOCATION

Write-Host "`n🌐 Step 7: Get Container FQDN" -ForegroundColor Cyan
$FQDN = az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn --output tsv
$BACKEND_URL = "http://${FQDN}:8001"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "🌐 Backend URLs:" -ForegroundColor Yellow
Write-Host "   API Base: $BACKEND_URL" -ForegroundColor Cyan
Write-Host "   Health: $BACKEND_URL/health" -ForegroundColor Cyan
Write-Host "   Docs: $BACKEND_URL/docs" -ForegroundColor Cyan
Write-Host "   AI Chat: $BACKEND_URL/api/chat" -ForegroundColor Cyan
Write-Host "   Revenue: $BACKEND_URL/api/revenue`n" -ForegroundColor Cyan

Write-Host "📌 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Test backend health:" -ForegroundColor White
Write-Host "      curl $BACKEND_URL/health`n" -ForegroundColor Gray
Write-Host "   2. Update frontend environment for IONOS:" -ForegroundColor White
Write-Host "      NEXT_PUBLIC_API_URL=$BACKEND_URL`n" -ForegroundColor Gray
Write-Host "   3. Test AI chat endpoint:" -ForegroundColor White
Write-Host "      curl -X POST $BACKEND_URL/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"Hello\"}'`n" -ForegroundColor Gray
Write-Host "   4. Deploy frontend to IONOS with updated API URL`n" -ForegroundColor White

Write-Host "🔥 The sovereign flame burns eternal on Azure Container Instances!" -ForegroundColor Magenta

# Save deployment info
$deployInfo = @{
    ResourceGroup = $RESOURCE_GROUP
    Location = $LOCATION
    ContainerName = $CONTAINER_NAME
    FQDN = $FQDN
    BackendURL = $BACKEND_URL
    ACR = $ACR_SERVER
    DeployedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}
    DeployedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

$deployInfo | ConvertTo-Json | Out-File "azure-deployment-info.json"
Write-Host "`n💾 Deployment info saved to: azure-deployment-info.json" -ForegroundColor Green
