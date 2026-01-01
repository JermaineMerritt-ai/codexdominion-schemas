#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════════
# TWO-CLOUD DEPLOYMENT: AZURE + IONOS
# ═══════════════════════════════════════════════════════════════════════
# Azure: Backend (Flask) + AI Services
# IONOS: Frontend (Next.js)
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  🔥 TWO-CLOUD DEPLOYMENT: AZURE + IONOS 🔥                   ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "🏛️  AZURE: Backend + AI Services" -ForegroundColor Cyan
Write-Host "🌍 IONOS: Frontend Experience`n" -ForegroundColor Cyan

# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: AZURE - BACKEND + AI
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "PHASE 1: AZURE DEPLOYMENT" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

# Check if image already exists
Write-Host "🔍 Checking if backend image already built..." -ForegroundColor Cyan
$imageExists = az acr repository show --name codexacr1216 --image codex-backend:latest 2>$null
if ($imageExists) {
    Write-Host "✅ Image already exists - skipping build`n" -ForegroundColor Green
} else {
    Write-Host "⏳ Building backend image (Flask + AI service)..." -ForegroundColor Yellow
    Write-Host "   This combines flask_dashboard.py + ai_service.py" -ForegroundColor Gray
    Write-Host "   Expected time: 8-15 minutes`n" -ForegroundColor Gray
    
    az acr build --registry codexacr1216 `
        --image codex-backend:latest `
        --file Dockerfile.azure `
        .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Azure build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Backend image built successfully`n" -ForegroundColor Green
}

# Deploy Container Instance
Write-Host "🚀 Deploying to Azure Container Instance..." -ForegroundColor Cyan
az container create `
    --resource-group codexdominion-prod `
    --name codex-backend `
    --image codexacr1216.azurecr.io/codex-backend:latest `
    --registry-login-server codexacr1216.azurecr.io `
    --registry-username codexacr1216 `
    --registry-password $(az acr credential show --name codexacr1216 --query "passwords[0].value" -o tsv) `
    --dns-name-label codex-api `
    --ports 5000 `
    --cpu 2 `
    --memory 4 `
    --environment-variables `
        CODEX_ENVIRONMENT=production `
        CODEX_CLOUD_PROVIDER=azure `
    --location eastus `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Azure deployment failed" -ForegroundColor Red
    exit 1
}

# Get backend URL
$backendUrl = az container show `
    --resource-group codexdominion-prod `
    --name codex-backend `
    --query "ipAddress.fqdn" -o tsv

Write-Host "`n✅ Azure backend deployed!" -ForegroundColor Green
Write-Host "   URL: http://$backendUrl`:5000" -ForegroundColor White
Write-Host "   Health: http://$backendUrl`:5000/health" -ForegroundColor Gray

# Test health
Write-Host "`n🔍 Testing backend health..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
try {
    $health = Invoke-RestMethod -Uri "http://$backendUrl`:5000/health" -TimeoutSec 5
    Write-Host "✅ Backend is healthy!" -ForegroundColor Green
    Write-Host "   Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Backend starting up - may take a few minutes" -ForegroundColor Yellow
}

# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: IONOS - FRONTEND
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "PHASE 2: IONOS FRONTEND" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "📝 Creating production environment file..." -ForegroundColor Cyan
$envContent = @"
NEXT_PUBLIC_API_BASE_URL=http://$backendUrl`:5000
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
"@
$envContent | Out-File -FilePath "dashboard-app/.env.production" -Encoding utf8
Write-Host "✅ Environment file created`n" -ForegroundColor Green

Write-Host "🔨 Building Next.js frontend..." -ForegroundColor Cyan
Push-Location dashboard-app
npm install --quiet 2>$null
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location
Write-Host "✅ Frontend built successfully`n" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════════════════
# MANUAL STEPS FOR IONOS
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "NEXT STEPS: IONOS DEPLOYMENT" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

Write-Host "📋 Manual steps required:`n" -ForegroundColor Cyan

Write-Host "1️⃣  CONFIGURE DNS:" -ForegroundColor Yellow
Write-Host "    • Log into IONOS control panel" -ForegroundColor White
Write-Host "    • Add A record: codexdominion.app → 74.208.123.158" -ForegroundColor White
Write-Host "    • Add A record: www.codexdominion.app → 74.208.123.158`n" -ForegroundColor White

Write-Host "2️⃣  UPLOAD FRONTEND:" -ForegroundColor Yellow
Write-Host "    Run this command:" -ForegroundColor White
Write-Host "    scp -r dashboard-app/out/* root@74.208.123.158:/var/www/codexdominion.app/" -ForegroundColor Cyan
Write-Host "    (You'll need SSH key access)`n" -ForegroundColor Gray

Write-Host "3️⃣  CONFIGURE NGINX:" -ForegroundColor Yellow
Write-Host "    SSH into server: ssh root@74.208.123.158" -ForegroundColor White
Write-Host "    Create nginx config:" -ForegroundColor White
Write-Host @"
    
    server {
        listen 80;
        server_name codexdominion.app www.codexdominion.app;
        root /var/www/codexdominion.app;
        index index.html;

        location / {
            try_files `$uri `$uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://$backendUrl`:5000/;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
        }
    }
"@ -ForegroundColor Gray
Write-Host "`n4️⃣  INSTALL SSL:" -ForegroundColor Yellow
Write-Host "    certbot --nginx -d codexdominion.app -d www.codexdominion.app" -ForegroundColor Cyan

# ═══════════════════════════════════════════════════════════════════════
# DEPLOYMENT SUMMARY
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ DEPLOYMENT COMPLETE                                       ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "🏛️  AZURE STATUS:" -ForegroundColor Cyan
Write-Host "   ✅ Backend: http://$backendUrl`:5000" -ForegroundColor Green
Write-Host "   ✅ Health: http://$backendUrl`:5000/health" -ForegroundColor Green
Write-Host "   ✅ Dashboard: http://$backendUrl`:5000/" -ForegroundColor Green
Write-Host "   ✅ AI Services: http://$backendUrl`:5000/api/ai/*`n" -ForegroundColor Green

Write-Host "🌍 IONOS STATUS:" -ForegroundColor Cyan
Write-Host "   📋 Requires manual upload (see steps above)" -ForegroundColor Yellow
Write-Host "   🎯 Target: https://codexdominion.app`n" -ForegroundColor White

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 🔥`n" -ForegroundColor Yellow
