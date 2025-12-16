# =====================================================
# Codex Dominion - Streamlit Dashboard ACR Deployment
# =====================================================
#
# Builds and deploys the Streamlit dashboard to Azure Container Registry
# Usage: .\deploy-streamlit-acr.ps1 [-Tag <version>]
#
# Prerequisites:
# - Azure CLI installed and authenticated
# - Docker installed (only for local builds)
# - Access to codexdominion ACR

param(
    [string]$Tag = "latest",
    [switch]$LocalBuild = $false,
    [switch]$PushOnly = $false
)

$ErrorActionPreference = "Stop"

# Configuration
$ACR_NAME = "codexdominion4607"  # Update based on: az acr list -o table
$IMAGE_NAME = "streamlit-dashboard"
$DOCKERFILE = "Dockerfile.dashboard"
$RESOURCE_GROUP = "codexdominion-basic"
$APP_SERVICE_PLAN = "codexdominion-basic-plan"
$WEBAPP_NAME = "codex-streamlit-dashboard"

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Streamlit Dashboard ACR Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Registry: $ACR_NAME.azurecr.io" -ForegroundColor Yellow
Write-Host "Image: ${IMAGE_NAME}:${Tag}" -ForegroundColor Yellow
Write-Host "Dockerfile: $DOCKERFILE" -ForegroundColor Yellow
Write-Host ""

# Verify Dockerfile exists
if (-not (Test-Path $DOCKERFILE)) {
    Write-Host "ERROR: $DOCKERFILE not found!" -ForegroundColor Red
    exit 1
}

# Verify Azure CLI authentication
Write-Host "Verifying Azure CLI authentication..." -ForegroundColor Cyan
try {
    $account = az account show 2>&1 | ConvertFrom-Json
    Write-Host "✓ Authenticated as: $($account.user.name)" -ForegroundColor Green
    Write-Host "✓ Subscription: $($account.name)" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Not authenticated to Azure CLI" -ForegroundColor Red
    Write-Host "Run: az login" -ForegroundColor Yellow
    exit 1
}

# Login to ACR
Write-Host ""
Write-Host "Logging into ACR..." -ForegroundColor Cyan
try {
    az acr login --name $ACR_NAME
    Write-Host "✓ Successfully logged into $ACR_NAME" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to login to ACR" -ForegroundColor Red
    Write-Host "Ensure you have access to the registry" -ForegroundColor Yellow
    exit 1
}

if ($LocalBuild) {
    # Build locally and push
    Write-Host ""
    Write-Host "Building image locally..." -ForegroundColor Cyan
    $imageTag = "$ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}"

    docker build -f $DOCKERFILE -t $imageTag .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Image built successfully" -ForegroundColor Green

    if (-not $PushOnly) {
        Write-Host ""
        Write-Host "Pushing image to ACR..." -ForegroundColor Cyan
        docker push $imageTag
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Docker push failed" -ForegroundColor Red
            exit 1
        }
        Write-Host "✓ Image pushed successfully" -ForegroundColor Green
    }
} else {
    # Build directly in ACR (recommended - faster)
    Write-Host ""
    Write-Host "Building image in ACR (this may take a few minutes)..." -ForegroundColor Cyan

    az acr build `
        --registry $ACR_NAME `
        --image "${IMAGE_NAME}:${Tag}" `
        --file $DOCKERFILE `
        .

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: ACR build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Image built and pushed successfully" -ForegroundColor Green
}

# Tag as latest if not already
if ($Tag -ne "latest") {
    Write-Host ""
    Write-Host "Tagging as 'latest'..." -ForegroundColor Cyan
    az acr import `
        --name $ACR_NAME `
        --source "$ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}" `
        --image "${IMAGE_NAME}:latest" `
        --force
    Write-Host "✓ Tagged as latest" -ForegroundColor Green
}

# Show image info
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Image: $ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}" -ForegroundColor Yellow
Write-Host ""
Write-Host "To pull this image:" -ForegroundColor Cyan
Write-Host "  docker pull $ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}" -ForegroundColor White
Write-Host ""
Write-Host "To run locally:" -ForegroundColor Cyan
Write-Host "  docker run -p 8501:8501 $ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}" -ForegroundColor White
Write-Host ""
Write-Host "To deploy to Azure Container Instances:" -ForegroundColor Cyan
Write-Host "  az container create --name streamlit-dashboard \\" -ForegroundColor White
Write-Host "    --resource-group codexdominion-prod \\" -ForegroundColor White
Write-Host "    --image $ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag} \\" -ForegroundColor White
Write-Host "    --dns-name-label streamlit-dashboard \\" -ForegroundColor White
Write-Host "    --ports 8501" -ForegroundColor White
Write-Host ""

# List recent tags
Write-Host "Available tags:" -ForegroundColor Cyan
az acr repository show-tags --name $ACR_NAME --repository $IMAGE_NAME --output table

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Deploying to Azure Web App..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if webapp exists
$webappExists = az webapp show --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating new Web App: $WEBAPP_NAME" -ForegroundColor Yellow
    az webapp create `
        --resource-group $RESOURCE_GROUP `
        --plan $APP_SERVICE_PLAN `
        --name $WEBAPP_NAME `
        --deployment-container-image-name "$ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}"
} else {
    Write-Host "Web App exists, updating container image..." -ForegroundColor Yellow
}

# Configure container
Write-Host "Configuring container settings..." -ForegroundColor Cyan
az webapp config container set `
    --name $WEBAPP_NAME `
    --resource-group $RESOURCE_GROUP `
    --container-image-name "$ACR_NAME.azurecr.io/${IMAGE_NAME}:${Tag}" `
    --container-registry-url "https://$ACR_NAME.azurecr.io"

# Configure app settings
Write-Host "Configuring Streamlit settings..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name $WEBAPP_NAME `
    --resource-group $RESOURCE_GROUP `
    --settings WEBSITES_PORT=8501 STREAMLIT_SERVER_PORT=8501 STREAMLIT_SERVER_HEADLESS=true

# Restart webapp
Write-Host "Restarting Web App..." -ForegroundColor Cyan
az webapp restart --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "Web App Deployment Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""
Write-Host "URL: https://$WEBAPP_NAME.azurewebsites.net" -ForegroundColor Yellow
Write-Host ""
Write-Host "View logs:" -ForegroundColor Cyan
Write-Host "  az webapp log tail --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP" -ForegroundColor White
Write-Host ""

Write-Host ""
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑" -ForegroundColor Magenta
