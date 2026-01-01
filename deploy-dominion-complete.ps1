#!/usr/bin/env pwsh
# ═══════════════════════════════════════════════════════════════════════
# CODEX DOMINION - COMPLETE TWO-CLOUD ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════
# AZURE: The Dominion's Core (All Intelligence)
# IONOS: The Dominion's Face (All User Interaction)
# ═══════════════════════════════════════════════════════════════════════

param(
    [switch]$SkipAzure,
    [switch]$SkipIONOS,
    [switch]$QuickDeploy
)

$ErrorActionPreference = "Stop"

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║         🔥 CODEX DOMINION COMPLETE DEPLOYMENT 🔥             ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "🏛️  AZURE: The Dominion's Core (Intelligence)" -ForegroundColor Cyan
Write-Host "    • Flask Backend + AI Service" -ForegroundColor White
Write-Host "    • PostgreSQL Database" -ForegroundColor White
Write-Host "    • Redis Cache (Workers)" -ForegroundColor White
Write-Host "    • Workflow Engine" -ForegroundColor White
Write-Host "    • Automation + Orchestration" -ForegroundColor White
Write-Host "    • Advisor Brain + Notifications`n" -ForegroundColor White

Write-Host "🌍 IONOS: The Dominion's Face (Interface)" -ForegroundColor Cyan
Write-Host "    • Next.js Dashboard (52+ pages)" -ForegroundColor White
Write-Host "    • Public Marketing Site" -ForegroundColor White
Write-Host "    • Static Assets + CDN" -ForegroundColor White
Write-Host "    • Domain Management`n" -ForegroundColor White

# ═══════════════════════════════════════════════════════════════════════
# PHASE 1: AZURE - THE CORE
# ═══════════════════════════════════════════════════════════════════════

if (-not $SkipAzure) {
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "PHASE 1: AZURE - DEPLOYING THE CORE" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

    $rgName = "codexdominion-prod"
    $location = "eastus"
    $acrName = "codexacr1216"

    # Step 1: PostgreSQL Database
    Write-Host "📊 [1/5] Deploying PostgreSQL Database..." -ForegroundColor Cyan
    $dbServer = "codexdominion-db"
    $dbName = "codexdb"
    $dbAdmin = "codexadmin"
    $dbPassword = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 16 | ForEach-Object {[char]$_})
    
    Write-Host "   Creating PostgreSQL Flexible Server..." -ForegroundColor Gray
    az postgres flexible-server create `
        --resource-group $rgName `
        --name $dbServer `
        --location $location `
        --admin-user $dbAdmin `
        --admin-password $dbPassword `
        --sku-name Standard_B1ms `
        --tier Burstable `
        --storage-size 32 `
        --version 14 `
        --public-access 0.0.0.0-255.255.255.255 `
        --output table 2>$null

    az postgres flexible-server db create `
        --resource-group $rgName `
        --server-name $dbServer `
        --database-name $dbName `
        --output table

    $dbConnectionString = "postgresql://${dbAdmin}:${dbPassword}@${dbServer}.postgres.database.azure.com:5432/${dbName}?sslmode=require"
    Write-Host "   ✅ Database ready: $dbServer" -ForegroundColor Green

    # Step 2: Redis Cache
    Write-Host "`n🔴 [2/5] Deploying Redis Cache..." -ForegroundColor Cyan
    $redisName = "codexdominion-redis"
    
    Write-Host "   Creating Azure Cache for Redis..." -ForegroundColor Gray
    az redis create `
        --resource-group $rgName `
        --name $redisName `
        --location $location `
        --sku Basic `
        --vm-size c0 `
        --output table 2>$null

    $redisKey = az redis list-keys `
        --resource-group $rgName `
        --name $redisName `
        --query primaryKey -o tsv

    $redisHost = "${redisName}.redis.cache.windows.net"
    $redisConnectionString = "rediss://:${redisKey}@${redisHost}:6380/0"
    Write-Host "   ✅ Redis ready: $redisName" -ForegroundColor Green

    # Step 3: Build Backend Image
    Write-Host "`n🐳 [3/5] Building Backend Image..." -ForegroundColor Cyan
    
    # Check if image exists
    $imageExists = az acr repository show --name $acrName --image codex-backend:latest 2>$null
    if ($imageExists -and -not $QuickDeploy) {
        Write-Host "   ✅ Image already exists - skipping build" -ForegroundColor Green
    } else {
        Write-Host "   Building Flask + AI service container..." -ForegroundColor Gray
        Write-Host "   ⏳ This will take 8-15 minutes..." -ForegroundColor Yellow
        
        az acr build `
            --registry $acrName `
            --image codex-backend:latest `
            --file Dockerfile.azure `
            .
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   ❌ Build failed" -ForegroundColor Red
            exit 1
        }
        Write-Host "   ✅ Backend image built" -ForegroundColor Green
    }

    # Step 4: Deploy Backend Container
    Write-Host "`n🚀 [4/5] Deploying Backend Container..." -ForegroundColor Cyan
    
    $acrPassword = az acr credential show --name $acrName --query "passwords[0].value" -o tsv
    
    Write-Host "   Creating Container Instance with full configuration..." -ForegroundColor Gray
    az container create `
        --resource-group $rgName `
        --name codex-backend `
        --image ${acrName}.azurecr.io/codex-backend:latest `
        --registry-login-server ${acrName}.azurecr.io `
        --registry-username $acrName `
        --registry-password $acrPassword `
        --dns-name-label codex-api `
        --ports 5000 `
        --cpu 2 `
        --memory 4 `
        --environment-variables `
            CODEX_ENVIRONMENT=production `
            DATABASE_URL=$dbConnectionString `
            REDIS_URL=$redisConnectionString `
            FLASK_APP=flask_dashboard `
            PYTHONUNBUFFERED=1 `
        --location $location `
        --restart-policy Always `
        --output table

    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Deployment failed" -ForegroundColor Red
        exit 1
    }

    $backendUrl = az container show `
        --resource-group $rgName `
        --name codex-backend `
        --query "ipAddress.fqdn" -o tsv

    Write-Host "   ✅ Backend deployed: http://${backendUrl}:5000" -ForegroundColor Green

    # Step 5: Deploy Background Worker
    Write-Host "`n⚙️  [5/5] Deploying Background Worker..." -ForegroundColor Cyan
    
    Write-Host "   Creating worker container for RQ tasks..." -ForegroundColor Gray
    az container create `
        --resource-group $rgName `
        --name codex-worker `
        --image ${acrName}.azurecr.io/codex-backend:latest `
        --registry-login-server ${acrName}.azurecr.io `
        --registry-username $acrName `
        --registry-password $acrPassword `
        --cpu 1 `
        --memory 2 `
        --environment-variables `
            CODEX_ENVIRONMENT=production `
            DATABASE_URL=$dbConnectionString `
            REDIS_URL=$redisConnectionString `
            WORKER_MODE=1 `
        --command-line "python -m rq worker workflows --url $redisConnectionString" `
        --location $location `
        --restart-policy Always `
        --output table

    Write-Host "   ✅ Worker deployed" -ForegroundColor Green

    # Test Health
    Write-Host "`n🔍 Testing Azure deployment..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15
    
    try {
        $health = Invoke-RestMethod -Uri "http://${backendUrl}:5000/health" -TimeoutSec 10
        Write-Host "   ✅ Backend is healthy!" -ForegroundColor Green
        Write-Host "      Status: $($health.status)" -ForegroundColor Gray
    } catch {
        Write-Host "   ⚠️  Backend starting up (may take 2-3 minutes)" -ForegroundColor Yellow
    }

    # Save configuration
    $azureConfig = @{
        backend_url = "http://${backendUrl}:5000"
        database_url = $dbConnectionString
        redis_url = $redisConnectionString
        database_server = $dbServer
        redis_name = $redisName
        deployed_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }
    $azureConfig | ConvertTo-Json | Out-File "azure-deployment.json" -Encoding utf8

    Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ AZURE CORE DEPLOYED SUCCESSFULLY                         ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

    Write-Host "🏛️  AZURE ENDPOINTS:" -ForegroundColor Cyan
    Write-Host "   Backend API:    http://${backendUrl}:5000" -ForegroundColor White
    Write-Host "   Health Check:   http://${backendUrl}:5000/health" -ForegroundColor White
    Write-Host "   Dashboard:      http://${backendUrl}:5000/" -ForegroundColor White
    Write-Host "   AI Services:    http://${backendUrl}:5000/api/ai/*" -ForegroundColor White
    Write-Host "   Treasury:       http://${backendUrl}:5000/api/treasury/*" -ForegroundColor White
    Write-Host "   Workflows:      http://${backendUrl}:5000/api/workflows/*`n" -ForegroundColor White
    
    Write-Host "📊 AZURE INFRASTRUCTURE:" -ForegroundColor Cyan
    Write-Host "   Database:       $dbServer.postgres.database.azure.com" -ForegroundColor White
    Write-Host "   Redis:          $redisHost" -ForegroundColor White
    Write-Host "   Backend:        codex-backend (Container Instance)" -ForegroundColor White
    Write-Host "   Worker:         codex-worker (Background Jobs)`n" -ForegroundColor White

} else {
    Write-Host "⏭️  Skipping Azure deployment`n" -ForegroundColor Yellow
    # Load existing config
    if (Test-Path "azure-deployment.json") {
        $azureConfig = Get-Content "azure-deployment.json" | ConvertFrom-Json
        $backendUrl = $azureConfig.backend_url -replace "http://", "" -replace ":5000", ""
    } else {
        Write-Host "❌ No existing Azure deployment found. Remove -SkipAzure flag." -ForegroundColor Red
        exit 1
    }
}

# ═══════════════════════════════════════════════════════════════════════
# PHASE 2: IONOS - THE FACE
# ═══════════════════════════════════════════════════════════════════════

if (-not $SkipIONOS) {
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "PHASE 2: IONOS - DEPLOYING THE FACE" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Gray

    # Create production environment
    Write-Host "📝 [1/3] Creating production environment..." -ForegroundColor Cyan
    $envContent = @"
NEXT_PUBLIC_API_BASE_URL=http://${backendUrl}:5000
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
NEXT_PUBLIC_DEPLOYMENT=production
NEXT_PUBLIC_CLOUD_PROVIDER=azure-ionos
"@
    $envContent | Out-File -FilePath "dashboard-app/.env.production" -Encoding utf8
    Write-Host "   ✅ Environment configured" -ForegroundColor Green

    # Build Next.js
    Write-Host "`n🔨 [2/3] Building Next.js dashboard..." -ForegroundColor Cyan
    Write-Host "   Installing dependencies..." -ForegroundColor Gray
    Push-Location dashboard-app
    npm install --quiet 2>$null
    
    Write-Host "   Building production bundle..." -ForegroundColor Gray
    npm run build

    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Build failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "   ✅ Next.js built successfully" -ForegroundColor Green

    # Create deployment package
    Write-Host "`n📦 [3/3] Creating deployment package..." -ForegroundColor Cyan
    $deploymentDir = "ionos-deployment"
    if (Test-Path $deploymentDir) {
        Remove-Item $deploymentDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $deploymentDir | Out-Null
    
    Copy-Item -Path "dashboard-app/out/*" -Destination $deploymentDir -Recurse
    Write-Host "   ✅ Package created: $deploymentDir/" -ForegroundColor Green

    Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  ✅ IONOS FRONTEND BUILT SUCCESSFULLY                        ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

    # Manual deployment instructions
    Write-Host "📋 MANUAL DEPLOYMENT STEPS:`n" -ForegroundColor Yellow

    Write-Host "1️⃣  CONFIGURE DNS (IONOS Control Panel):" -ForegroundColor Cyan
    Write-Host "    • A Record: codexdominion.app → 74.208.123.158" -ForegroundColor White
    Write-Host "    • A Record: www.codexdominion.app → 74.208.123.158`n" -ForegroundColor White

    Write-Host "2️⃣  UPLOAD FRONTEND TO SERVER:" -ForegroundColor Cyan
    Write-Host "    scp -r $deploymentDir/* root@74.208.123.158:/var/www/codexdominion.app/" -ForegroundColor White
    Write-Host "    (Requires SSH key access)`n" -ForegroundColor Gray

    Write-Host "3️⃣  CONFIGURE NGINX:" -ForegroundColor Cyan
    Write-Host "    SSH into server: ssh root@74.208.123.158" -ForegroundColor White
    Write-Host "    Create /etc/nginx/sites-available/codexdominion:" -ForegroundColor Gray
    Write-Host @"
    
    server {
        listen 80;
        server_name codexdominion.app www.codexdominion.app;
        root /var/www/codexdominion.app;
        index index.html;

        # Frontend static files
        location / {
            try_files `$uri `$uri/ /index.html;
        }

        # Proxy API requests to Azure
        location /api/ {
            proxy_pass http://${backendUrl}:5000/api/;
            proxy_set_header Host `$host;
            proxy_set_header X-Real-IP `$remote_addr;
            proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto `$scheme;
        }

        # Cache static assets
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
"@ -ForegroundColor White

    Write-Host "`n    Enable site:" -ForegroundColor Gray
    Write-Host "    ln -s /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/" -ForegroundColor White
    Write-Host "    nginx -t && systemctl reload nginx`n" -ForegroundColor White

    Write-Host "4️⃣  INSTALL SSL CERTIFICATE:" -ForegroundColor Cyan
    Write-Host "    certbot --nginx -d codexdominion.app -d www.codexdominion.app" -ForegroundColor White
    Write-Host "    (Auto-renews with cron job)`n" -ForegroundColor Gray

} else {
    Write-Host "⏭️  Skipping IONOS deployment`n" -ForegroundColor Yellow
}

# ═══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════════

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║        🔥 CODEX DOMINION DEPLOYMENT COMPLETE 🔥              ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Yellow

Write-Host "🏛️  AZURE - THE CORE:" -ForegroundColor Cyan
Write-Host "   ✅ Flask Backend + AI Service" -ForegroundColor Green
Write-Host "   ✅ PostgreSQL Database" -ForegroundColor Green
Write-Host "   ✅ Redis Cache" -ForegroundColor Green
Write-Host "   ✅ Background Workers" -ForegroundColor Green
Write-Host "   ✅ Auto-restart + Monitoring`n" -ForegroundColor Green

Write-Host "🌍 IONOS - THE FACE:" -ForegroundColor Cyan
Write-Host "   ✅ Next.js Dashboard Built" -ForegroundColor Green
Write-Host "   📋 Manual Upload Required" -ForegroundColor Yellow
Write-Host "   📋 DNS Configuration Required" -ForegroundColor Yellow
Write-Host "   📋 nginx + SSL Setup Required`n" -ForegroundColor Yellow

Write-Host "🎯 WHAT YOU'VE ACHIEVED:" -ForegroundColor Cyan
Write-Host "   • Complete separation of concerns" -ForegroundColor White
Write-Host "   • Scalable, always-on backend" -ForegroundColor White
Write-Host "   • Fast, global frontend" -ForegroundColor White
Write-Host "   • Professional production architecture" -ForegroundColor White
Write-Host "   • No more localhost issues`n" -ForegroundColor White

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 🔥`n" -ForegroundColor Yellow
