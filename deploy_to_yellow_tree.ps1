# =============================================================================
# Deploy Codex Dominion Frontend to Yellow-Tree Azure Static Web App
# =============================================================================

Write-Host "`n🚀 DEPLOYING CODEX DOMINION TO AZURE" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray

$appName = "codex-frontend-centralus"
$resourceGroup = "codex-rg"
$frontendPath = "c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\frontend"

# Step 1: Get deployment token
Write-Host "`n🔑 Getting deployment token..." -ForegroundColor Yellow
$deploymentToken = az staticwebapp secrets list `
    --name $appName `
    --resource-group $resourceGroup `
    --query "properties.apiKey" -o tsv

if ($deploymentToken) {
    Write-Host "✅ Token retrieved" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to get token" -ForegroundColor Red
    exit 1
}

# Step 2: Check if SWA CLI is installed
Write-Host "`n📦 Checking Azure Static Web Apps CLI..." -ForegroundColor Yellow
$swaInstalled = Get-Command swa -ErrorAction SilentlyContinue

if (-not $swaInstalled) {
    Write-Host "Installing SWA CLI..." -ForegroundColor Yellow
    npm install -g @azure/static-web-apps-cli
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install SWA CLI" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ SWA CLI ready" -ForegroundColor Green

# Step 3: Navigate to frontend
Write-Host "`n📂 Navigating to frontend directory..." -ForegroundColor Yellow
cd $frontendPath

# Step 4: Check dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ npm install failed" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Dependencies ready" -ForegroundColor Green

# Step 5: Build frontend
Write-Host "`n🔨 Building Next.js application..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Build successful" -ForegroundColor Green

# Step 6: Deploy to Azure
Write-Host "`n🚀 Deploying to Azure Static Web Apps..." -ForegroundColor Yellow
Write-Host "   Target: yellow-tree-0ed102210.3.azurestaticapps.net" -ForegroundColor Cyan

swa deploy .next --deployment-token $deploymentToken --env production

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n" + "=" * 70 -ForegroundColor Green
    Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "`n📊 Your Codex Dominion Dashboard is LIVE:" -ForegroundColor Cyan
    Write-Host "   🌐 Home: https://yellow-tree-0ed102210.3.azurestaticapps.net" -ForegroundColor White
    Write-Host "   📊 Dashboard: https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard" -ForegroundColor White
    Write-Host "   📍 Backend: http://20.242.178.102:8001" -ForegroundColor White
    Write-Host "`n🔗 Configure Google Domains DNS:" -ForegroundColor Yellow
    Write-Host "   Go to: https://domains.google.com/registrar/codexdominion.app/dns" -ForegroundColor White
    Write-Host "   Add CNAME: @ -> yellow-tree-0ed102210.3.azurestaticapps.net" -ForegroundColor Gray
    Write-Host "   Add CNAME: www -> yellow-tree-0ed102210.3.azurestaticapps.net" -ForegroundColor Gray
    Write-Host "`n" + "=" * 70 -ForegroundColor Green
} else {
    Write-Host "`n❌ Deployment failed" -ForegroundColor Red
    exit 1
}

cd c:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
Write-Host "`n✨ Done! Your dashboard is live! 🚀" -ForegroundColor Green
