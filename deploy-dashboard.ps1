# Codex Master Dashboard - Azure Deployment Script
# Deploys Streamlit dashboard to Azure Container Instances

param(
    [string]$ResourceGroup = "codexdominion-basic",
    [string]$Location = "westus2",
    [string]$ContainerName = "codex-dashboard",
    [string]$DnsName = "codex-dashboard",
    [string]$Port = "8501"
)

Write-Host "`n🔥 DEPLOYING CODEX MASTER DASHBOARD TO AZURE`n" -ForegroundColor Magenta
Write-Host "════════════════════════════════════════════════`n" -ForegroundColor DarkGray

# Step 1: Build Docker image
Write-Host "📦 Building Docker image...`n" -ForegroundColor Cyan
docker build -f dashboard.Dockerfile -t codex-dashboard:latest . `
    --build-arg REQUIREMENTS_FILE=dashboard-requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully`n" -ForegroundColor Green

# Step 2: Tag for Azure Container Registry (optional) or push to Docker Hub
$AcrName = "codexdominion"
$ImageTag = "${AcrName}.azurecr.io/codex-dashboard:latest"

Write-Host "🏷️  Tagging image for deployment...`n" -ForegroundColor Cyan
docker tag codex-dashboard:latest $ImageTag

# Step 3: Push to registry (if using ACR)
# Uncomment if you want to use Azure Container Registry
# Write-Host "⬆️  Pushing to Azure Container Registry...`n" -ForegroundColor Cyan
# az acr login --name $AcrName
# docker push $ImageTag

# Step 4: Deploy to Azure Container Instances
Write-Host "🚀 Deploying to Azure Container Instances...`n" -ForegroundColor Cyan

az container create `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --image codex-dashboard:latest `
    --dns-name-label $DnsName `
    --ports $Port `
    --cpu 1 `
    --memory 2 `
    --restart-policy OnFailure `
    --location $Location `
    --environment-variables `
        STREAMLIT_SERVER_PORT=$Port `
        STREAMLIT_SERVER_HEADLESS=true `
        STREAMLIT_SERVER_ENABLE_CORS=false

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

# Step 5: Get the URL
Write-Host "`n✅ DEPLOYMENT COMPLETE!`n" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════`n" -ForegroundColor DarkGray

$fqdn = az container show `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --query "ipAddress.fqdn" `
    --output tsv

Write-Host "🌐 Your Master Dashboard is now live at:`n" -ForegroundColor Cyan
Write-Host "   http://${fqdn}:${Port}`n" -ForegroundColor White
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Magenta
