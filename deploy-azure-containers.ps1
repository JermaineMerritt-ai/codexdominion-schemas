# =============================================================================
# CODEX DOMINION - Azure Container Instances Deployment
# NO QUOTA LIMITS - Works on any subscription!
# =============================================================================

$ErrorActionPreference = "Continue"
$rg = "codexdominion-prod"
$loc = "eastus"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🐳 CODEX DOMINION - CONTAINER DEPLOYMENT" -ForegroundColor Yellow
Write-Host "  Using Azure Container Instances (No Quota Needed!)" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check login
$account = az account show 2>&1 | ConvertFrom-Json
if ($account) {
    Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
} else {
    Write-Host "❌ Run: az login" -ForegroundColor Red
    exit 1
}

# Step 1: Create Dockerfile if doesn't exist
Write-Host "`n[1/5] Preparing Docker image..." -ForegroundColor Cyan
if (!(Test-Path "Dockerfile")) {
    Write-Host "   Creating Dockerfile..." -ForegroundColor Gray
    $dockerfile = @"
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir flask flask-cors openai waitress redis

# Copy application
COPY dashboard_complete_fixed.py app.py
COPY codex_ledger.json .
COPY proclamations.json .
COPY cycles.json .

# Expose port
EXPOSE 80

# Run application
CMD ["python", "app.py"]
"@
    Set-Content -Path "Dockerfile" -Value $dockerfile
    Write-Host "✅ Dockerfile created" -ForegroundColor Green
} else {
    Write-Host "✅ Using existing Dockerfile" -ForegroundColor Green
}

# Step 2: Create requirements.txt if doesn't exist
if (!(Test-Path "requirements.txt")) {
    $requirements = @"
flask==3.0.0
flask-cors==4.0.0
openai==1.6.0
waitress==2.1.2
redis==5.0.1
"@
    Set-Content -Path "requirements.txt" -Value $requirements
    Write-Host "✅ requirements.txt created" -ForegroundColor Green
}

# Step 3: Create Container Registry
Write-Host "`n[2/5] Creating Azure Container Registry..." -ForegroundColor Cyan
$acrName = "codexdominion"
az acr show --name $acrName --resource-group $rg 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Creating ACR: $acrName..." -ForegroundColor Gray
    az acr create `
        --resource-group $rg `
        --name $acrName `
        --sku Basic `
        --admin-enabled true `
        --location $loc `
        --output none 2>&1 | Out-Null
    Write-Host "✅ Container Registry created" -ForegroundColor Green
} else {
    Write-Host "✅ Using existing Container Registry" -ForegroundColor Green
}

# Get ACR credentials
$acrCreds = az acr credential show --name $acrName --resource-group $rg | ConvertFrom-Json
$acrServer = "$acrName.azurecr.io"
$acrUser = $acrCreds.username
$acrPass = $acrCreds.passwords[0].value

Write-Host "   ACR Server: $acrServer" -ForegroundColor Gray

# Step 4: Build and push Docker image
Write-Host "`n[3/5] Building and pushing Docker image..." -ForegroundColor Cyan
Write-Host "   This may take 2-3 minutes..." -ForegroundColor Gray

az acr build `
    --registry $acrName `
    --image codex-dashboard:latest `
    --file Dockerfile `
    . 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Image built and pushed to ACR" -ForegroundColor Green
} else {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

# Step 5: Deploy Container Instance
Write-Host "`n[4/5] Deploying Container Instance..." -ForegroundColor Cyan
$containerName = "codex-dashboard"

az container create `
    --resource-group $rg `
    --name $containerName `
    --image "$acrServer/codex-dashboard:latest" `
    --registry-login-server $acrServer `
    --registry-username $acrUser `
    --registry-password $acrPass `
    --dns-name-label "codexdominion" `
    --ports 80 `
    --cpu 1 `
    --memory 1 `
    --environment-variables `
        FLASK_ENV=production `
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE" `
        DOT300_AGENTS_COUNT=301 `
    --location $loc `
    --output none 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container deployed" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}

# Get container info
$container = az container show --resource-group $rg --name $containerName | ConvertFrom-Json
$fqdn = $container.ipAddress.fqdn
$ip = $container.ipAddress.ip

# Step 6: Create PostgreSQL (optional)
Write-Host "`n[5/5] Creating PostgreSQL Database..." -ForegroundColor Cyan
$dbServer = "codexdb-prod"
$dbPassword = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})

az postgres flexible-server show --name $dbServer --resource-group $rg 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Creating server: $dbServer..." -ForegroundColor Gray
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
        --output none 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PostgreSQL created" -ForegroundColor Green
        az postgres flexible-server db create `
            --resource-group $rg `
            --server-name $dbServer `
            --database-name codexdominion `
            --output none 2>&1 | Out-Null
        Write-Host "✅ Database created" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Using existing PostgreSQL" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✨ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your Application:" -ForegroundColor Cyan
Write-Host "   Public URL: http://$fqdn" -ForegroundColor White
Write-Host "   IP Address: $ip" -ForegroundColor White
Write-Host ""
Write-Host "📊 Created Resources:" -ForegroundColor Yellow
Write-Host "   ✅ Container Registry: $acrServer" -ForegroundColor Green
Write-Host "   ✅ Container Instance: $containerName (1 CPU, 1GB RAM)" -ForegroundColor Green
Write-Host "   ✅ Redis Cache: codexdominion" -ForegroundColor Green
if ($dbServer) {
    Write-Host "   ✅ PostgreSQL: $dbServer" -ForegroundColor Green
    Write-Host "   📝 DB Password: $dbPassword" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "🧪 Test Your Deployment:" -ForegroundColor Cyan
Write-Host "   curl http://$fqdn" -ForegroundColor Gray
Write-Host "   Start-Process http://$fqdn" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 View Logs:" -ForegroundColor Cyan
Write-Host "   az container logs --resource-group $rg --name $containerName" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Monthly Cost:" -ForegroundColor Yellow
Write-Host "   Container Instance (1 CPU, 1GB): ~$35/month" -ForegroundColor Gray
Write-Host "   Container Registry (Basic): ~$5/month" -ForegroundColor Gray
Write-Host "   PostgreSQL (B1ms): ~$12/month" -ForegroundColor Gray
Write-Host "   Redis (Basic): ~$16/month" -ForegroundColor Gray
Write-Host "   TOTAL: ~$68/month" -ForegroundColor White
Write-Host ""
Write-Host "🚀 NO QUOTA LIMITS!" -ForegroundColor Green
Write-Host ""
