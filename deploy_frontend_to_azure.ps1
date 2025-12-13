# =============================================================================
# Codex Dominion - Frontend Deployment to Azure Static Web Apps
# =============================================================================

Write-Host "`n🚀 Deploying Codex Dominion Frontend to Azure..." -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray

# Configuration
$resourceGroup = "codex-dominion-rg"
$location = "eastus"
$appName = "codexdominion-frontend"
$frontendPath = "c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\frontend"

# Step 1: Check if Static Web App exists
Write-Host "`n📋 Step 1: Checking for existing Static Web App..." -ForegroundColor Yellow
$existingApp = az staticwebapp list --resource-group $resourceGroup --query "[?name=='$appName'].name" -o tsv

if ($existingApp) {
    Write-Host "✅ Static Web App '$appName' already exists" -ForegroundColor Green
} else {
    Write-Host "📦 Creating new Static Web App '$appName'..." -ForegroundColor Yellow

    az staticwebapp create `
        --name $appName `
        --resource-group $resourceGroup `
        --location $location `
        --sku Free `
        --source https://github.com/JermaineMerritt-ai/codexdominion-schemas `
        --branch main `
        --app-location "/frontend" `
        --output-location ".next"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Static Web App created successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create Static Web App" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Get deployment token
Write-Host "`n🔑 Step 2: Getting deployment token..." -ForegroundColor Yellow
$deploymentToken = az staticwebapp secrets list `
    --name $appName `
    --resource-group $resourceGroup `
    --query "properties.apiKey" -o tsv

if ($deploymentToken) {
    Write-Host "✅ Deployment token retrieved" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to get deployment token" -ForegroundColor Red
    exit 1
}

# Step 3: Build frontend
Write-Host "`n🔨 Step 3: Building frontend..." -ForegroundColor Yellow
cd $frontendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "🔨 Building Next.js application..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

# Step 4: Deploy using SWA CLI
Write-Host "`n🚀 Step 4: Deploying to Azure..." -ForegroundColor Yellow

# Check if SWA CLI is installed
$swaInstalled = Get-Command swa -ErrorAction SilentlyContinue

if (-not $swaInstalled) {
    Write-Host "📦 Installing Azure Static Web Apps CLI..." -ForegroundColor Yellow
    npm install -g @azure/static-web-apps-cli
}

Write-Host "📤 Uploading build to Azure..." -ForegroundColor Yellow
swa deploy .next --deployment-token $deploymentToken --env production

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}

# Step 5: Get deployment URL
Write-Host "`n🌐 Step 5: Getting deployment URL..." -ForegroundColor Yellow
$url = az staticwebapp show `
    --name $appName `
    --resource-group $resourceGroup `
    --query "defaultHostname" -o tsv

if ($url) {
    Write-Host "`n" + "=" * 70 -ForegroundColor Green
    Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "`n📊 Your Codex Dominion is LIVE at:" -ForegroundColor Cyan
    Write-Host "   🌐 Home: https://$url" -ForegroundColor White
    Write-Host "   📊 Dashboard: https://$url/main-dashboard" -ForegroundColor White
    Write-Host "   📍 API Backend: http://20.242.178.102:8001" -ForegroundColor White
    Write-Host "`n🔗 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Configure custom domain (codexdominion.app):" -ForegroundColor White
    Write-Host "      az staticwebapp hostname set --name $appName --resource-group $resourceGroup --hostname codexdominion.app" -ForegroundColor Gray
    Write-Host "   2. Update DNS CNAME record:" -ForegroundColor White
    Write-Host "      Type: CNAME" -ForegroundColor Gray
    Write-Host "      Name: @" -ForegroundColor Gray
    Write-Host "      Value: $url" -ForegroundColor Gray
    Write-Host "      TTL: 300" -ForegroundColor Gray
    Write-Host "`n" + "=" * 70 -ForegroundColor Green
} else {
    Write-Host "❌ Failed to get deployment URL" -ForegroundColor Red
    exit 1
}

# Return to original directory
cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion

Write-Host "`n✨ Deployment complete! Your dashboard is live! 🚀" -ForegroundColor Green
