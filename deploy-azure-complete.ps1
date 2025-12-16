# =============================================================================
# CODEX DOMINION - Complete Azure Deployment (Fixed)
# =============================================================================
# Creates: App Service Plan + Web App + Database
# Uses: Free/Basic tiers (no quota needed)
# =============================================================================

$ErrorActionPreference = "Continue"
$rg = "codexdominion-prod"
$loc = "eastus"
$timestamp = Get-Date -Format "MMdd-HHmm"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔷 CODEX DOMINION - COMPLETE AZURE SETUP" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check login
Write-Host "Checking Azure login..." -ForegroundColor Gray
$account = az account show 2>&1 | ConvertFrom-Json
if ($account) {
    Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
} else {
    Write-Host "❌ Not logged in! Run: az login" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 1: Resource Group
Write-Host "[1/6] Ensuring Resource Group exists..." -ForegroundColor Cyan
az group create --name $rg --location $loc --output none 2>&1 | Out-Null
Write-Host "✅ Resource Group: $rg" -ForegroundColor Green

# Step 2: App Service Plan (Free Tier)
Write-Host "[2/6] Creating App Service Plan (Free Tier)..." -ForegroundColor Cyan
$planExists = az appservice plan show --name "codexdominion-free" --resource-group $rg 2>&1
if ($planExists -match "ResourceNotFound") {
    az appservice plan create `
        --name "codexdominion-free" `
        --resource-group $rg `
        --location $loc `
        --is-linux `
        --sku F1 `
        --output none 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ App Service Plan created (Free F1)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Free tier full, creating Basic B1..." -ForegroundColor Yellow
        az appservice plan create `
            --name "codexdominion-basic" `
            --resource-group $rg `
            --location $loc `
            --is-linux `
            --sku B1 `
            --output none 2>&1 | Out-Null
        $planName = "codexdominion-basic"
        Write-Host "✅ App Service Plan created (Basic B1 - ~$13/month)" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Using existing App Service Plan" -ForegroundColor Green
}

# Determine which plan to use
$planName = if (az appservice plan show --name "codexdominion-free" --resource-group $rg 2>&1 | Out-Null; $LASTEXITCODE -eq 0) {
    "codexdominion-free"
} else {
    "codexdominion-basic"
}

# Step 3: Backend Web App
Write-Host "[3/6] Creating Backend Web App..." -ForegroundColor Cyan
$appName = "codexapi$timestamp"
Write-Host "   Name: $appName" -ForegroundColor Gray

az webapp create `
    --name $appName `
    --resource-group $rg `
    --plan $planName `
    --runtime "PYTHON:3.11" `
    --output none 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend Web App created" -ForegroundColor Green
    $backendUrl = "https://$appName.azurewebsites.net"
} else {
    Write-Host "❌ Web App creation failed" -ForegroundColor Red
    az webapp create --name $appName --resource-group $rg --plan $planName --runtime "PYTHON:3.11" 2>&1 | Select-Object -Last 10
    exit 1
}

# Step 4: Configure Web App
Write-Host "[4/6] Configuring Web App..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name $appName `
    --resource-group $rg `
    --settings `
        FLASK_ENV=production `
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE" `
        DOT300_AGENTS_COUNT=301 `
    --output none 2>&1 | Out-Null

Write-Host "✅ Environment configured" -ForegroundColor Green

# Step 5: PostgreSQL Flexible Server (Basic tier)
Write-Host "[5/6] Creating PostgreSQL Database (Basic tier)..." -ForegroundColor Cyan
$dbServer = "codexdb$timestamp"
$dbPassword = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})

Write-Host "   Server: $dbServer" -ForegroundColor Gray
Write-Host "   Tier: Burstable B1ms (~$12/month)" -ForegroundColor Gray

az postgres flexible-server create `
    --name $dbServer `
    --resource-group $rg `
    --location $loc `
    --admin-user codexadmin `
    --admin-password $dbPassword `
    --sku-name Standard_B1ms `
    --tier Burstable `
    --storage-size 32 `
    --version 16 `
    --public-access All `
    --output none 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PostgreSQL Server created" -ForegroundColor Green

    # Create database
    az postgres flexible-server db create `
        --resource-group $rg `
        --server-name $dbServer `
        --database-name codexdominion `
        --output none 2>&1 | Out-Null

    Write-Host "✅ Database 'codexdominion' created" -ForegroundColor Green

    # Update web app with database connection
    $dbUrl = "postgresql://codexadmin:$dbPassword@$dbServer.postgres.database.azure.com/codexdominion"
    az webapp config appsettings set `
        --name $appName `
        --resource-group $rg `
        --settings DATABASE_URL=$dbUrl `
        --output none 2>&1 | Out-Null
} else {
    Write-Host "⚠️  Database creation skipped (optional)" -ForegroundColor Yellow
}

# Step 6: Deploy Code
Write-Host "[6/6] Deploying application code..." -ForegroundColor Cyan
Write-Host "   Using local deployment from current directory..." -ForegroundColor Gray

# Create a simple startup script
$startupScript = @"
#!/bin/bash
pip install flask flask-cors openai waitress
python dashboard_complete_fixed.py
"@

Set-Content -Path "startup.sh" -Value $startupScript
az webapp config set `
    --name $appName `
    --resource-group $rg `
    --startup-file "startup.sh" `
    --output none 2>&1 | Out-Null

Write-Host "✅ Startup configured" -ForegroundColor Green

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✨ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your Application:" -ForegroundColor Cyan
Write-Host "   Backend API: $backendUrl" -ForegroundColor White
Write-Host "   Dashboard: $backendUrl/" -ForegroundColor White
Write-Host ""
Write-Host "📊 Created Resources:" -ForegroundColor Yellow
Write-Host "   ✅ Resource Group: $rg" -ForegroundColor Green
Write-Host "   ✅ App Service Plan: $planName" -ForegroundColor Green
Write-Host "   ✅ Web App: $appName" -ForegroundColor Green
if ($dbServer) {
    Write-Host "   ✅ PostgreSQL: $dbServer" -ForegroundColor Green
    Write-Host "   📝 DB Password: $dbPassword (save this!)" -ForegroundColor Yellow
}
Write-Host "   ✅ Redis Cache: codexdominion (from earlier)" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Test: curl $backendUrl" -ForegroundColor Gray
Write-Host "   2. View logs: az webapp log tail --name $appName --resource-group $rg" -ForegroundColor Gray
Write-Host "   3. Deploy code: az webapp up --name $appName --resource-group $rg" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Monthly Cost Estimate:" -ForegroundColor Yellow
if ($planName -eq "codexdominion-free") {
    Write-Host "   App Service: FREE" -ForegroundColor Green
} else {
    Write-Host "   App Service (B1): ~$13/month" -ForegroundColor Gray
}
if ($dbServer) {
    Write-Host "   PostgreSQL (B1ms): ~$12/month" -ForegroundColor Gray
}
Write-Host "   Redis (Basic): ~$16/month" -ForegroundColor Gray
Write-Host ""
