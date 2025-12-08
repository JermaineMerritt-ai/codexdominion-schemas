# =============================================================================
# Azure Infrastructure Deployment Script
# =============================================================================
# Deploys complete Codex Dominion infrastructure using Bicep

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "codex-rg",

    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",

    [Parameter(Mandatory=$false)]
    [string]$Environment = "prod",

    [Parameter(Mandatory=$false)]
    [string]$BaseName = "codex",

    [Parameter(Mandatory=$true)]
    [SecureString]$PostgresPassword,

    [Parameter(Mandatory=$false)]
    [switch]$WhatIf
)

# Error handling
$ErrorActionPreference = "Stop"

# Display banner
Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔥 CODEX DOMINION - AZURE INFRASTRUCTURE DEPLOYMENT 🔥      ║
║                                                               ║
║   Provisioning complete infrastructure with:                 ║
║   • Static Web Apps (Frontend)                               ║
║   • App Service (Backend with Docker)                        ║
║   • Azure Container Registry                                 ║
║   • PostgreSQL Flexible Server                               ║
║   • Azure Cache for Redis                                    ║
║   • Application Insights                                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""

# Check Azure CLI
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✅ Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI not found. Please install: https://aka.ms/azure-cli" -ForegroundColor Red
    exit 1
}

# Check login status
Write-Host "🔍 Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "⚠️  Not logged in. Running az login..." -ForegroundColor Yellow
    az login
    $account = az account show | ConvertFrom-Json
}
Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "✅ Subscription: $($account.name)" -ForegroundColor Green

# Create Resource Group
Write-Host ""
Write-Host "📦 Creating Resource Group: $ResourceGroupName" -ForegroundColor Cyan
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "false") {
    az group create --name $ResourceGroupName --location $Location --tags "application=codex-dominion" "environment=$Environment" "managedBy=bicep"
    Write-Host "✅ Resource Group created" -ForegroundColor Green
} else {
    Write-Host "✅ Resource Group already exists" -ForegroundColor Green
}

# Validate Bicep template
Write-Host ""
Write-Host "✔️  Validating Bicep template..." -ForegroundColor Cyan
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bicepFile = Join-Path $scriptDir "main.bicep"

if (-not (Test-Path $bicepFile)) {
    Write-Host "❌ Bicep file not found: $bicepFile" -ForegroundColor Red
    exit 1
}

try {
    az deployment group validate `
        --resource-group $ResourceGroupName `
        --template-file $bicepFile `
        --parameters environment=$Environment `
        --parameters baseName=$BaseName `
        --parameters pgAdminPassword=$PostgresPassword `
        --output none
    Write-Host "✅ Bicep template validation passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Bicep template validation failed" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# What-If analysis
if ($WhatIf) {
    Write-Host ""
    Write-Host "🔮 Running What-If analysis..." -ForegroundColor Cyan
    az deployment group what-if `
        --resource-group $ResourceGroupName `
        --template-file $bicepFile `
        --parameters environment=$Environment `
        --parameters baseName=$BaseName `
        --parameters pgAdminPassword=$PostgresPassword

    Write-Host ""
    Write-Host "ℹ️  What-If analysis complete. No changes were made." -ForegroundColor Yellow
    exit 0
}

# Confirm deployment
Write-Host ""
Write-Host "⚠️  DEPLOYMENT SUMMARY" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "Resource Group:  $ResourceGroupName"
Write-Host "Location:        $Location"
Write-Host "Environment:     $Environment"
Write-Host "Base Name:       $BaseName"
Write-Host ""
Write-Host "Resources to create:"
Write-Host "  • Static Web App (Frontend)       - $0/month (Free tier)"
Write-Host "  • App Service Plan (B1)           - ~$13/month"
Write-Host "  • App Service (Backend)           - Included in plan"
Write-Host "  • Container Registry (Basic)      - ~$5/month"
Write-Host "  • PostgreSQL Flexible (B1ms)      - ~$12-15/month"
Write-Host "  • Redis Cache (Basic C0)          - ~$15/month"
Write-Host "  • Application Insights            - ~$2/month (5GB free)"
Write-Host "  • Log Analytics Workspace         - Included"
Write-Host ""
Write-Host "Estimated Total: ~$47-50/month" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Do you want to proceed with deployment? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Deploy infrastructure
Write-Host ""
Write-Host "🚀 Deploying infrastructure..." -ForegroundColor Cyan
Write-Host "⏳ This may take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

$deploymentName = "codex-$Environment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

try {
    $deployment = az deployment group create `
        --resource-group $ResourceGroupName `
        --name $deploymentName `
        --template-file $bicepFile `
        --parameters environment=$Environment `
        --parameters baseName=$BaseName `
        --parameters pgAdminPassword=$PostgresPassword `
        --output json | ConvertFrom-Json

    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "║               ✅ DEPLOYMENT SUCCESSFUL! ✅                     ║" -ForegroundColor Green
    Write-Host "║                                                               ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""

    # Get outputs
    $outputs = $deployment.properties.outputs

    Write-Host "📋 DEPLOYMENT OUTPUTS" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🌐 Frontend URL:" -ForegroundColor Yellow
    Write-Host "   https://$($outputs.staticWebAppHostname.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Backend URL:" -ForegroundColor Yellow
    Write-Host "   $($outputs.backendUrl.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "🐳 Container Registry:" -ForegroundColor Yellow
    Write-Host "   $($outputs.acrLoginServer.value)" -ForegroundColor White
    Write-Host "   Username: $($outputs.acrUsername.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "🗄️  PostgreSQL:" -ForegroundColor Yellow
    Write-Host "   $($outputs.postgresFqdn.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "⚡ Redis:" -ForegroundColor Yellow
    Write-Host "   $($outputs.redisHostname.value):$($outputs.redisSslPort.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Application Insights:" -ForegroundColor Yellow
    Write-Host "   Key: $($outputs.appInsightsKey.value)" -ForegroundColor White
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""

    # Save outputs to file
    $outputFile = Join-Path $scriptDir "deployment-outputs.json"
    $outputs | ConvertTo-Json -Depth 10 | Out-File $outputFile
    Write-Host "💾 Outputs saved to: $outputFile" -ForegroundColor Green
    Write-Host ""

    # Next steps
    Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Add GitHub Secrets:" -ForegroundColor White
    Write-Host "   • AZURE_STATIC_WEB_APPS_API_TOKEN = $($outputs.staticWebAppToken.value)"
    Write-Host "   • AZURE_CREDENTIALS (service principal JSON)"
    Write-Host ""
    Write-Host "2. Build and push Docker image:" -ForegroundColor White
    Write-Host "   cd src/backend"
    Write-Host "   az acr login --name $($outputs.acrLoginServer.value)"
    Write-Host "   docker build -t $($outputs.acrLoginServer.value)/codex-backend:latest ."
    Write-Host "   docker push $($outputs.acrLoginServer.value)/codex-backend:latest"
    Write-Host ""
    Write-Host "3. Update frontend API URL in next.config.js:" -ForegroundColor White
    Write-Host "   NEXT_PUBLIC_API_URL = '$($outputs.backendUrl.value)'"
    Write-Host ""
    Write-Host "4. Deploy frontend:" -ForegroundColor White
    Write-Host "   cd frontend"
    Write-Host "   npm run build"
    Write-Host "   swa deploy out --deployment-token <token>"
    Write-Host ""
    Write-Host "5. Test endpoints:" -ForegroundColor White
    Write-Host "   curl https://$($outputs.staticWebAppHostname.value)"
    Write-Host "   curl $($outputs.backendUrl.value)/health"
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "❌ DEPLOYMENT FAILED" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "📝 Check deployment logs:" -ForegroundColor Yellow
    Write-Host "   az deployment group show --resource-group $ResourceGroupName --name $deploymentName"
    exit 1
}

Write-Host "🔥 The flame burns sovereign and eternal — forever. 🔥" -ForegroundColor Cyan
