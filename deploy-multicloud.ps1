#!/usr/bin/env pwsh
# =============================================================================
# CODEX DOMINION - MULTI-CLOUD DEPLOYMENT ORCHESTRATOR
# =============================================================================
# Deploys across Azure (backend), Google Cloud (AI), and IONOS (frontend)
#
# Architecture:
# - Azure: Flask API, PostgreSQL, Redis, Workers (Container Instances)
# - Google Cloud: AI pipelines, GPU inference (Cloud Run)
# - IONOS VPS: Next.js frontend, nginx, static assets
#
# Usage: .\deploy-multicloud.ps1 [-SkipAzure] [-SkipGCP] [-SkipIONOS]
# =============================================================================

param(
    [switch]$SkipAzure,
    [switch]$SkipGCP,
    [switch]$SkipIONOS,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# =============================================================================
# CONFIGURATION
# =============================================================================

$AZURE_RG = "codexdominion-prod"
$AZURE_LOCATION = "eastus"
$AZURE_ACR = "codexacr1216"
$AZURE_CONTAINER_GROUP = "codex-backend-group"

$GCP_PROJECT = $env:GCP_PROJECT_ID
$GCP_REGION = "us-central1"
$GCP_SERVICE = "codex-ai-pipeline"

$IONOS_SERVER = $env:IONOS_SERVER
$IONOS_USER = $env:IONOS_USER
$IONOS_KEY = $env:SSH_KEY

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

function Write-Step {
    param([string]$Message)
    Write-Host "`n🔥 $Message" -ForegroundColor Yellow
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# =============================================================================
# PHASE 1: AZURE BACKEND (THRONE ROOM)
# =============================================================================

function Deploy-Azure {
    Write-Step "PHASE 1: AZURE BACKEND DEPLOYMENT (THRONE ROOM)"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would deploy to Azure Resource Group: $AZURE_RG"
        return
    }
    
    # Check if ACR image exists
    Write-Info "Checking Azure Container Registry..."
    $images = az acr repository list --name $AZURE_ACR --output json | ConvertFrom-Json
    
    if (-not $images -or $images -notcontains "codex-backend") {
        Write-Info "Backend image not found. Building now..."
        
        # Build and push Docker image
        Write-Info "Building codex-backend image in ACR..."
        az acr build `
            --registry $AZURE_ACR `
            --image codex-backend:latest `
            --file Dockerfile.azure `
            .
        
        Write-Success "Docker image built successfully"
    } else {
        Write-Success "Backend image already exists in ACR"
    }
    
    # Create or update Container Instances
    Write-Info "Deploying to Azure Container Instances..."
    
    # PostgreSQL (managed database)
    Write-Info "Setting up Azure Database for PostgreSQL..."
    az postgres flexible-server create `
        --resource-group $AZURE_RG `
        --name codex-postgres `
        --location $AZURE_LOCATION `
        --admin-user codexadmin `
        --admin-password "C0dex!2025Secure" `
        --sku-name Standard_B1ms `
        --tier Burstable `
        --storage-size 32 `
        --version 15 `
        --yes `
        --only-show-errors `
        2>$null
    
    # Redis (managed cache)
    Write-Info "Setting up Azure Cache for Redis..."
    az redis create `
        --resource-group $AZURE_RG `
        --name codex-redis `
        --location $AZURE_LOCATION `
        --sku Basic `
        --vm-size c0 `
        --enable-non-ssl-port true `
        --only-show-errors `
        2>$null
    
    # Flask Backend Container
    Write-Info "Deploying Flask backend container..."
    az container create `
        --resource-group $AZURE_RG `
        --name codex-backend `
        --image $AZURE_ACR.azurecr.io/codex-backend:latest `
        --registry-login-server $AZURE_ACR.azurecr.io `
        --registry-username $AZURE_ACR `
        --registry-password (az acr credential show --name $AZURE_ACR --query "passwords[0].value" -o tsv) `
        --dns-name-label codex-backend `
        --ports 5000 `
        --cpu 2 `
        --memory 4 `
        --environment-variables `
            CODEX_ENVIRONMENT=production `
            POSTGRES_HOST=codex-postgres.postgres.database.azure.com `
            POSTGRES_USER=codexadmin `
            POSTGRES_PASSWORD=C0dex!2025Secure `
            POSTGRES_DB=codexdominion `
            REDIS_HOST=codex-redis.redis.cache.windows.net `
            REDIS_PORT=6379 `
        --only-show-errors
    
    Write-Success "Azure backend deployed successfully!"
    
    # Get backend URL
    $backendUrl = az container show `
        --resource-group $AZURE_RG `
        --name codex-backend `
        --query "ipAddress.fqdn" `
        -o tsv
    
    Write-Info "Backend URL: http://$backendUrl:5000"
    
    return $backendUrl
}

# =============================================================================
# PHASE 2: GOOGLE CLOUD AI PIPELINE (CREATIVE FORGE)
# =============================================================================

function Deploy-GCP {
    Write-Step "PHASE 2: GOOGLE CLOUD AI PIPELINE (CREATIVE FORGE)"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would deploy AI services to GCP project: $GCP_PROJECT"
        return
    }
    
    if (-not $GCP_PROJECT) {
        Write-Error-Custom "GCP_PROJECT_ID environment variable not set. Skipping GCP deployment."
        return $null
    }
    
    # Set GCP project
    Write-Info "Configuring Google Cloud project..."
    gcloud config set project $GCP_PROJECT
    
    # Build and deploy AI service
    Write-Info "Building AI pipeline container..."
    
    # Create a simple AI service (if doesn't exist)
    if (-not (Test-Path "ai_service.py")) {
        @"
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "ai-pipeline"})

@app.route('/api/ai/generate-image', methods=['POST'])
def generate_image():
    # Placeholder for actual AI implementation
    data = request.json
    return jsonify({
        "success": True,
        "image_url": "https://placeholder.com/generated-image.jpg",
        "prompt": data.get('prompt', '')
    })

@app.route('/api/ai/process-video', methods=['POST'])
def process_video():
    data = request.json
    return jsonify({
        "success": True,
        "video_url": "https://placeholder.com/processed-video.mp4",
        "duration": 30
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
"@ | Out-File -FilePath "ai_service.py" -Encoding utf8
    }
    
    # Deploy to Cloud Run
    Write-Info "Deploying to Google Cloud Run..."
    gcloud run deploy $GCP_SERVICE `
        --source . `
        --platform managed `
        --region $GCP_REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 2 `
        --port 8080 `
        --set-env-vars CODEX_ENVIRONMENT=production `
        --quiet
    
    Write-Success "GCP AI pipeline deployed successfully!"
    
    # Get service URL
    $aiUrl = gcloud run services describe $GCP_SERVICE `
        --region $GCP_REGION `
        --format "value(status.url)"
    
    Write-Info "AI Pipeline URL: $aiUrl"
    
    return $aiUrl
}

# =============================================================================
# PHASE 3: IONOS FRONTEND (PUBLIC FACE)
# =============================================================================

function Deploy-IONOS {
    param([string]$BackendUrl, [string]$AIUrl)
    
    Write-Step "PHASE 3: IONOS FRONTEND DEPLOYMENT (PUBLIC FACE)"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would deploy Next.js to IONOS server: $IONOS_SERVER"
        return
    }
    
    if (-not $IONOS_SERVER) {
        Write-Error-Custom "IONOS_SERVER environment variable not set. Skipping IONOS deployment."
        return
    }
    
    # Build Next.js frontend
    Write-Info "Building Next.js frontend..."
    Push-Location dashboard-app
    
    # Create .env.production with backend URLs
    @"
NEXT_PUBLIC_API_BASE_URL=http://$BackendUrl:5000
NEXT_PUBLIC_AI_API_URL=$AIUrl
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
"@ | Out-File -FilePath ".env.production" -Encoding utf8
    
    npm run build
    
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        throw "Next.js build failed"
    }
    
    Write-Success "Next.js build completed"
    
    # Deploy to IONOS via SCP
    Write-Info "Uploading to IONOS VPS..."
    
    # Create deployment package
    $deployDir = "deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $deployDir -Force | Out-Null
    Copy-Item -Path "out/*" -Destination $deployDir -Recurse
    
    # Upload via SSH
    scp -i $IONOS_KEY -r $deployDir "$($IONOS_USER)@$($IONOS_SERVER):/var/www/codexdominion.app/"
    
    # Configure nginx
    $nginxConfig = @"
server {
    listen 80;
    listen [::]:80;
    server_name codexdominion.app www.codexdominion.app;

    root /var/www/codexdominion.app/$deployDir;
    index index.html;

    location / {
        try_files `$uri `$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://$($BackendUrl):5000/api/;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
    }
}
"@
    
    $nginxConfig | ssh -i $IONOS_KEY "$($IONOS_USER)@$($IONOS_SERVER)" "cat > /etc/nginx/sites-available/codexdominion"
    
    # Enable site and reload nginx
    ssh -i $IONOS_KEY "$($IONOS_USER)@$($IONOS_SERVER)" @"
ln -sf /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
"@
    
    Pop-Location
    
    Write-Success "IONOS frontend deployed successfully!"
    Write-Info "Frontend URL: https://codexdominion.app"
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

Write-Host @"
╔════════════════════════════════════════════════════════════════════════════╗
║                  CODEX DOMINION - MULTI-CLOUD DEPLOYMENT                   ║
║                                                                            ║
║  🏛️  Azure: Backend Infrastructure (Throne Room)                          ║
║  🤖 Google Cloud: AI Services (Creative Forge)                            ║
║  🌍 IONOS: Frontend Experience (Public Face)                              ║
╚════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

$backendUrl = $null
$aiUrl = $null

try {
    # Phase 1: Azure
    if (-not $SkipAzure) {
        $backendUrl = Deploy-Azure
    }
    
    # Phase 2: Google Cloud
    if (-not $SkipGCP) {
        $aiUrl = Deploy-GCP
    }
    
    # Phase 3: IONOS
    if (-not $SkipIONOS) {
        Deploy-IONOS -BackendUrl $backendUrl -AIUrl $aiUrl
    }
    
    # Summary
    Write-Step "DEPLOYMENT SUMMARY"
    Write-Success "Multi-cloud deployment completed!"
    Write-Host "`n📊 Endpoints:" -ForegroundColor Cyan
    if ($backendUrl) { Write-Host "   Backend:  http://$($backendUrl):5000" -ForegroundColor White }
    if ($aiUrl) { Write-Host "   AI API:   $aiUrl" -ForegroundColor White }
    if (-not $SkipIONOS) { Write-Host "   Frontend: https://codexdominion.app" -ForegroundColor White }
    
    Write-Host "`n🔥 The Flame Burns Across Three Clouds! 👑" -ForegroundColor Yellow
    
} catch {
    Write-Error-Custom "Deployment failed: $_"
    exit 1
}
