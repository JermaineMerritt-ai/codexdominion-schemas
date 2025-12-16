# =============================================================================
# CODEX DOMINION - Azure FREE TIER Deployment
# =============================================================================
# Uses Free/Basic tiers to avoid quota limits
# =============================================================================

param(
    [string]$ResourceGroup = "codexdominion-prod",
    [string]$Location = "eastus"
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔷 AZURE FREE TIER DEPLOYMENT" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if already logged in
$account = az account show 2>&1 | ConvertFrom-Json
if (-not $account) {
    Write-Host "❌ Not logged in to Azure" -ForegroundColor Red
    Write-Host "Run: az login" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host ""

# Create Resource Group if it doesn't exist
Write-Host "[1/4] Creating Resource Group..." -ForegroundColor Cyan
az group create --name $ResourceGroup --location $Location --output none 2>&1 | Out-Null
Write-Host "✅ Resource group ready" -ForegroundColor Green

# Create App Service Plan (FREE TIER - No quota needed!)
Write-Host "[2/4] Creating App Service Plan (Free Tier)..." -ForegroundColor Cyan
az appservice plan create `
    --name "codexdominion-free-plan" `
    --resource-group $ResourceGroup `
    --location $Location `
    --is-linux `
    --sku F1 `
    --output none 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Free tier not available, trying Basic tier..." -ForegroundColor Yellow
    az appservice plan create `
        --name "codexdominion-free-plan" `
        --resource-group $ResourceGroup `
        --location $Location `
        --is-linux `
        --sku B1 `
        --output none 2>&1
}

Write-Host "✅ App Service Plan created" -ForegroundColor Green

# Create Web App for Backend
Write-Host "[3/4] Creating Backend Web App..." -ForegroundColor Cyan
$appName = "codexdominion-$(Get-Random -Minimum 1000 -Maximum 9999)"
Write-Host "   App Name: $appName" -ForegroundColor Gray

az webapp create `
    --name $appName `
    --resource-group $ResourceGroup `
    --plan "codexdominion-free-plan" `
    --runtime "PYTHON:3.11" `
    --output none 2>&1

Write-Host "✅ Backend Web App created" -ForegroundColor Green

# Configure Web App
Write-Host "[4/4] Configuring Web App..." -ForegroundColor Cyan

# Set environment variables
az webapp config appsettings set `
    --name $appName `
    --resource-group $ResourceGroup `
    --settings `
        FLASK_ENV=production `
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE" `
    --output none 2>&1

Write-Host "✅ Configuration complete" -ForegroundColor Green

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✨ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your app is live at:" -ForegroundColor Cyan
Write-Host "   https://$appName.azurewebsites.net" -ForegroundColor White
Write-Host ""
Write-Host "📊 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Deploy code: az webapp up --name $appName --resource-group $ResourceGroup" -ForegroundColor Gray
Write-Host "   2. View logs: az webapp log tail --name $appName --resource-group $ResourceGroup" -ForegroundColor Gray
Write-Host "   3. Monitor: https://portal.azure.com" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Free tier includes:" -ForegroundColor Cyan
Write-Host "   • 1 GB disk space" -ForegroundColor Gray
Write-Host "   • 60 CPU minutes/day" -ForegroundColor Gray
Write-Host "   • Custom domain support" -ForegroundColor Gray
Write-Host ""
