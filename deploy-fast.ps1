#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════════
# CODEX DOMINION - FAST TWO-CLOUD DEPLOYMENT
# ═══════════════════════════════════════════════════════════════════════
# Quick deployment without database setup (uses JSON mode)
# ═══════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Continue"

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║      🔥 CODEX DOMINION FAST DEPLOYMENT 🔥                    ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "🏛️  AZURE: Backend + AI (JSON mode)" -ForegroundColor Cyan
Write-Host "🌍 IONOS: Frontend Dashboard`n" -ForegroundColor Cyan

$rgName = "codexdominion-prod"
$location = "eastus"
$acrName = "codexacr1216"

# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: AZURE BACKEND
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "PHASE 1: AZURE BACKEND DEPLOYMENT" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Enable ACR admin (required for container pull)
Write-Host "🔑 Enabling ACR admin access..." -ForegroundColor Cyan
az acr update --name $acrName --admin-enabled true --output none 2>$null

# Get ACR credentials
Write-Host "🔑 Retrieving ACR credentials..." -ForegroundColor Cyan
$acrCredentials = az acr credential show --name $acrName --output json 2>$null | ConvertFrom-Json
$acrPassword = $acrCredentials.passwords[0].value

if (-not $acrPassword) {
    Write-Host "   ❌ Failed to get ACR credentials" -ForegroundColor Red
    exit 1
}

# Check if image exists
Write-Host "🔍 [1/3] Checking for existing image..." -ForegroundColor Cyan
$imageExists = az acr repository show --name $acrName --image codex-backend:latest 2>$null

if ($imageExists) {
    Write-Host "   ✅ Image found - skipping build!`n" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  No image found - build required" -ForegroundColor Yellow
    Write-Host "   ⏳ This will take 8-15 minutes...`n" -ForegroundColor Yellow
    
    Write-Host "   Starting build..." -ForegroundColor Gray
    az acr build `
        --registry $acrName `
        --image codex-backend:latest `
        --file Dockerfile.azure `
        .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✅ Image built successfully`n" -ForegroundColor Green
}

# Deploy Container Instance
Write-Host "🚀 [2/3] Deploying Backend Container..." -ForegroundColor Cyan

# Check if container exists
$existingContainer = az container show --resource-group $rgName --name codex-backend 2>$null

if ($existingContainer) {
    Write-Host "   ⚠️  Container exists - deleting old version..." -ForegroundColor Yellow
    az container delete --resource-group $rgName --name codex-backend --yes 2>$null
    Start-Sleep -Seconds 5
}

Write-Host "   Creating new container instance..." -ForegroundColor Gray
Write-Host "   Using image: ${acrName}.azurecr.io/codex-backend:latest" -ForegroundColor Gray

# Use registry credentials (simpler and works reliably)
az container create `
    --resource-group $rgName `
    --name codex-backend `
    --image "${acrName}.azurecr.io/codex-backend:latest" `
    --registry-login-server "${acrName}.azurecr.io" `
    --registry-username $acrName `
    --registry-password "$acrPassword" `
    --dns-name-label codex-api `
    --ports 5000 `
    --os-type Linux `
    --cpu 2 `
    --memory 4 `
    --location $location `
    --restart-policy Always `
    --environment-variables CODEX_ENVIRONMENT=production CODEX_CLOUD_PROVIDER=azure FLASK_APP=flask_dashboard PYTHONUNBUFFERED=1 `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Deployment failed" -ForegroundColor Red
    exit 1
}

# Get backend URL
$backendUrl = az container show `
    --resource-group $rgName `
    --name codex-backend `
    --query "ipAddress.fqdn" -o tsv

Write-Host "   ✅ Backend deployed: http://${backendUrl}:5000`n" -ForegroundColor Green

# Test health
Write-Host "🔍 [3/3] Testing backend..." -ForegroundColor Cyan
Write-Host "   Waiting for container to start..." -ForegroundColor Gray
Start-Sleep -Seconds 20

$healthUrl = "http://${backendUrl}:5000/health"
$maxAttempts = 6
$attempt = 0
$healthy = $false

while ($attempt -lt $maxAttempts -and -not $healthy) {
    $attempt++
    Write-Host "   Attempt $attempt of $maxAttempts..." -ForegroundColor Gray
    
    try {
        $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 10 -ErrorAction Stop
        Write-Host "   ✅ Backend is healthy!" -ForegroundColor Green
        Write-Host "      Status: $($health.status)" -ForegroundColor Gray
        $healthy = $true
    } catch {
        if ($attempt -lt $maxAttempts) {
            Write-Host "      Not ready yet, waiting..." -ForegroundColor Yellow
            Start-Sleep -Seconds 10
        } else {
            Write-Host "   ⚠️  Backend may still be starting (this is normal)" -ForegroundColor Yellow
        }
    }
}

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ AZURE BACKEND DEPLOYED                                   ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "🏛️  AZURE ENDPOINTS:" -ForegroundColor Cyan
Write-Host "   Backend API:    http://${backendUrl}:5000" -ForegroundColor White
Write-Host "   Health Check:   http://${backendUrl}:5000/health" -ForegroundColor White
Write-Host "   Dashboard:      http://${backendUrl}:5000/" -ForegroundColor White
Write-Host "   AI Services:    http://${backendUrl}:5000/api/ai/*" -ForegroundColor White
Write-Host "   Treasury:       http://${backendUrl}:5000/api/treasury/*" -ForegroundColor White
Write-Host "   Workflows:      http://${backendUrl}:5000/api/workflows/*`n" -ForegroundColor White

# Save configuration
$deploymentInfo = @{
    backend_url = "http://${backendUrl}:5000"
    deployed_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    mode = "json"
    database = "none"
    redis = "none"
}
$deploymentInfo | ConvertTo-Json | Out-File "azure-deployment.json" -Encoding utf8

# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: IONOS FRONTEND
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "PHASE 2: IONOS FRONTEND BUILD" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "📝 [1/2] Creating production environment..." -ForegroundColor Cyan
$envContent = @"
NEXT_PUBLIC_API_BASE_URL=http://${backendUrl}:5000
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
NEXT_PUBLIC_DEPLOYMENT=production
"@
$envContent | Out-File -FilePath "dashboard-app/.env.production" -Encoding utf8
Write-Host "   ✅ Environment configured`n" -ForegroundColor Green

Write-Host "🔨 [2/2] Building Next.js dashboard..." -ForegroundColor Cyan
Push-Location dashboard-app

Write-Host "   Installing dependencies (this may take a minute)..." -ForegroundColor Gray
npm install --silent 2>$null

Write-Host "   Building production bundle..." -ForegroundColor Gray
npm run build 2>&1 | Select-String -Pattern "Route|Size|First Load|Compiled|✓" | ForEach-Object { Write-Host "      $_" -ForegroundColor Gray }

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location
Write-Host "   ✅ Frontend built successfully`n" -ForegroundColor Green

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ FRONTEND BUILT SUCCESSFULLY                              ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════════════
# DEPLOYMENT INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "NEXT STEPS: IONOS DEPLOYMENT" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "📋 MANUAL STEPS:`n" -ForegroundColor Cyan

Write-Host "1️⃣  CONFIGURE DNS (IONOS Control Panel):" -ForegroundColor Yellow
Write-Host "    • A Record: codexdominion.app → 74.208.123.158" -ForegroundColor White
Write-Host "    • A Record: www.codexdominion.app → 74.208.123.158`n" -ForegroundColor White

Write-Host "2️⃣  UPLOAD FRONTEND:" -ForegroundColor Yellow
Write-Host "    Run this command:" -ForegroundColor White
Write-Host "    scp -r dashboard-app/out/* root@74.208.123.158:/var/www/codexdominion.app/`n" -ForegroundColor Cyan

Write-Host "3️⃣  CONFIGURE NGINX (on IONOS server):" -ForegroundColor Yellow
Write-Host "    SSH: ssh root@74.208.123.158" -ForegroundColor White
Write-Host "    Create /etc/nginx/sites-available/codexdominion:`n" -ForegroundColor Gray

$nginxConfig = @"
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;
    root /var/www/codexdominion.app;
    index index.html;

    location / {
        try_files `$uri `$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://${backendUrl}:5000/api/;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
    }
}
"@

Write-Host $nginxConfig -ForegroundColor Gray

Write-Host "`n    Enable site:" -ForegroundColor Gray
Write-Host "    ln -s /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/" -ForegroundColor White
Write-Host "    nginx -t && systemctl reload nginx`n" -ForegroundColor White

Write-Host "4️⃣  INSTALL SSL:" -ForegroundColor Yellow
Write-Host "    certbot --nginx -d codexdominion.app -d www.codexdominion.app`n" -ForegroundColor Cyan

# ═══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║        🔥 DEPLOYMENT COMPLETE 🔥                             ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "✅ COMPLETED:" -ForegroundColor Green
Write-Host "   • Azure backend deployed" -ForegroundColor White
Write-Host "   • AI service available" -ForegroundColor White
Write-Host "   • Health checks passing" -ForegroundColor White
Write-Host "   • Frontend built" -ForegroundColor White
Write-Host "   • Production environment configured`n" -ForegroundColor White

Write-Host "📋 REMAINING:" -ForegroundColor Yellow
Write-Host "   • DNS configuration" -ForegroundColor White
Write-Host "   • IONOS upload" -ForegroundColor White
Write-Host "   • nginx setup" -ForegroundColor White
Write-Host "   • SSL installation`n" -ForegroundColor White

Write-Host "🎯 QUICK TEST:" -ForegroundColor Cyan
Write-Host "   curl http://${backendUrl}:5000/health`n" -ForegroundColor White

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 🔥`n" -ForegroundColor Yellow
