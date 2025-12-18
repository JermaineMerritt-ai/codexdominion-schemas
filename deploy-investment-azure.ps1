# =============================================================================
# INVESTMENT APP - AZURE CONTAINER APPS DEPLOYMENT
# =============================================================================

Write-Host "`n🔥 INVESTMENT APP - AZURE CONTAINER APPS DEPLOYMENT 🔥`n" -ForegroundColor Cyan

# Configuration
$ResourceGroup = "codex-rg"
$Location = "eastus2"
$ContainerRegistry = "codexdominionacr"
$AppName = "codex-investment-app"
$Environment = "codex-env"
$ImageTag = "latest"
$FullImageName = "$ContainerRegistry.azurecr.io/investment-app:$ImageTag"

Write-Host "📦 Configuration:" -ForegroundColor Yellow
Write-Host "  Resource Group: $ResourceGroup"
Write-Host "  Location: $Location"
Write-Host "  Container Registry: $ContainerRegistry"
Write-Host "  App Name: $AppName"
Write-Host "  Image: $FullImageName`n"

# Step 1: Check Azure login
Write-Host "🔐 Step 1: Checking Azure login..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not logged in to Azure. Please run: az login" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in as: $($account.user.name)"
Write-Host "   Subscription: $($account.name)`n"

# Step 2: Build Docker image
Write-Host "🐳 Step 2: Building Docker image..." -ForegroundColor Yellow
Write-Host "   This may take 2-3 minutes...`n"
docker build -f Dockerfile.investment -t $FullImageName . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker image built successfully`n"

# Step 3: Login to ACR
Write-Host "🔐 Step 3: Logging in to Azure Container Registry..." -ForegroundColor Yellow
az acr login --name $ContainerRegistry 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ACR login failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Logged in to ACR`n"

# Step 4: Push image to ACR
Write-Host "📤 Step 4: Pushing image to Azure Container Registry..." -ForegroundColor Yellow
Write-Host "   This may take 3-5 minutes...`n"
docker push $FullImageName 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Image push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Image pushed successfully`n"

# Step 5: Check if environment exists
Write-Host "🔍 Step 5: Checking Container Apps environment..." -ForegroundColor Yellow
$envExists = az containerapp env show --name $Environment --resource-group $ResourceGroup 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Environment exists`n"
} else {
    Write-Host "📦 Creating environment..." -ForegroundColor Yellow
    az containerapp env create `
        --name $Environment `
        --resource-group $ResourceGroup `
        --location $Location 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Environment creation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Environment created`n"
}

# Step 6: Deploy or update Container App
Write-Host "🚀 Step 6: Deploying Investment App..." -ForegroundColor Yellow

$appExists = az containerapp show --name $AppName --resource-group $ResourceGroup 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Updating existing app...`n"
    az containerapp update `
        --name $AppName `
        --resource-group $ResourceGroup `
        --image $FullImageName 2>&1
} else {
    Write-Host "   Creating new app...`n"
    az containerapp create `
        --name $AppName `
        --resource-group $ResourceGroup `
        --environment $Environment `
        --image $FullImageName `
        --target-port 5001 `
        --ingress external `
        --min-replicas 1 `
        --max-replicas 3 `
        --cpu 1 `
        --memory 2Gi `
        --registry-server "$ContainerRegistry.azurecr.io" 2>&1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Deployment successful!`n"

# Step 7: Get application URL
Write-Host "🌐 Step 7: Retrieving application URL...`n" -ForegroundColor Yellow
$fqdn = az containerapp show `
    --name $AppName `
    --resource-group $ResourceGroup `
    --query properties.configuration.ingress.fqdn `
    --output tsv

$url = "https://$fqdn"

# Success banner
Write-Host "`n✅ DEPLOYMENT COMPLETE! ✅`n" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
Write-Host "👑 YOUR INVESTMENT APP IS LIVE:`n" -ForegroundColor Yellow
Write-Host "   $url`n" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "📋 Investment App Features:" -ForegroundColor Yellow
Write-Host "   • Portfolio Management (4 Risk Profiles)"
Write-Host "   • Real-time Stock Tracking"
Write-Host "   • AI-Powered Daily Picks"
Write-Host "   • Trade History & Analytics"
Write-Host "   • Email Newsletter System"
Write-Host "   • Auto-scaling (1-3 replicas)`n"

Write-Host "🔗 Quick Links:" -ForegroundColor Yellow
Write-Host "   Home:         $url"
Write-Host "   Login:        $url/auth/login"
Write-Host "   Register:     $url/auth/register"
Write-Host "   Daily Picks:  $url/ai/daily-picks`n"

Write-Host "📊 View Logs:" -ForegroundColor Yellow
Write-Host "   az containerapp logs show --name $AppName --resource-group $ResourceGroup --follow`n"

Write-Host "🔧 Manage App:" -ForegroundColor Yellow
Write-Host "   View in Portal: https://portal.azure.com"
Write-Host "   Restart: az containerapp restart --name $AppName --resource-group $ResourceGroup`n"

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Cyan
