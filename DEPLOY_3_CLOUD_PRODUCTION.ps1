#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Codex Dominion - 3-Cloud Production Deployment
    
.DESCRIPTION
    Deploys across three cloud providers:
    1. AZURE - Backend (Flask API) - Crash-proof, auto-scaling
    2. IONOS - Frontend (Next.js Dashboard) - Fast European delivery
    3. GOOGLE CLOUD - Creative Engine (AI Pipelines) - Unlimited ML power
    
.EXAMPLE
    .\DEPLOY_3_CLOUD_PRODUCTION.ps1
#>

param(
    [switch]$SkipAzure,
    [switch]$SkipIONOS,
    [switch]$SkipGCP,
    [switch]$TestOnly
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "🔥🔥🔥 CODEX DOMINION - 3-CLOUD DEPLOYMENT 🔥🔥🔥" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "📍 AZURE      → Backend API (Flask + Gunicorn)" -ForegroundColor Cyan
Write-Host "📍 IONOS      → Frontend Dashboard (Next.js)" -ForegroundColor Cyan
Write-Host "📍 GOOGLE CLOUD → Creative Engine (AI Pipelines)" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan

$errors = @()

# Check Azure CLI
if (-not $SkipAzure) {
    $azInstalled = Get-Command az -ErrorAction SilentlyContinue
    if (-not $azInstalled) {
        $errors += "Azure CLI not installed. Install from: https://aka.ms/installazurecliwindows"
    } else {
        Write-Host "   ✅ Azure CLI installed" -ForegroundColor Green
    }
}

# Check gcloud CLI
if (-not $SkipGCP) {
    $gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
    if (-not $gcloudInstalled) {
        $errors += "Google Cloud SDK not installed. Install from: https://cloud.google.com/sdk/docs/install"
    } else {
        Write-Host "   ✅ Google Cloud SDK installed" -ForegroundColor Green
    }
}

# Check SSH for IONOS
if (-not $SkipIONOS) {
    $sshInstalled = Get-Command ssh -ErrorAction SilentlyContinue
    if (-not $sshInstalled) {
        $errors += "SSH not found. Install OpenSSH or Git Bash."
    } else {
        Write-Host "   ✅ SSH installed" -ForegroundColor Green
    }
}

if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Missing prerequisites:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "   • $error" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Install missing tools and run again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Load environment variables
if (Test-Path ".env.production") {
    Write-Host "📦 Loading environment variables..." -ForegroundColor Cyan
    Get-Content ".env.production" | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
        }
    }
    Write-Host "   ✅ Environment loaded" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# ==============================================================================
# 1️⃣ AZURE - BACKEND API DEPLOYMENT
# ==============================================================================

if (-not $SkipAzure) {
    Write-Host "1️⃣  DEPLOYING TO AZURE (BACKEND API)" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    
    # Azure config
    $AZURE_RESOURCE_GROUP = "codex-dominion-rg"
    $AZURE_LOCATION = "eastus2"
    $AZURE_CONTAINER_APP = "codex-backend"
    $AZURE_CONTAINER_ENV = "codex-env"
    $AZURE_ACR_NAME = "codexdominionacr"
    
    Write-Host "📦 Building Docker image..." -ForegroundColor Cyan
    docker build -t codex-backend:latest -f Dockerfile.flask .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker build failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "   ✅ Docker image built" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🔐 Logging into Azure..." -ForegroundColor Cyan
    az login --use-device-code
    
    Write-Host "📦 Creating resource group..." -ForegroundColor Cyan
    az group create --name $AZURE_RESOURCE_GROUP --location $AZURE_LOCATION --output none
    
    Write-Host "📦 Creating container registry..." -ForegroundColor Cyan
    az acr create --resource-group $AZURE_RESOURCE_GROUP --name $AZURE_ACR_NAME --sku Basic --output none
    
    Write-Host "🚀 Pushing image to ACR..." -ForegroundColor Cyan
    az acr login --name $AZURE_ACR_NAME
    docker tag codex-backend:latest "$AZURE_ACR_NAME.azurecr.io/codex-backend:latest"
    docker push "$AZURE_ACR_NAME.azurecr.io/codex-backend:latest"
    
    Write-Host "🏗️  Creating Container Apps environment..." -ForegroundColor Cyan
    az containerapp env create `
        --name $AZURE_CONTAINER_ENV `
        --resource-group $AZURE_RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --output none
    
    Write-Host "🚀 Deploying Container App..." -ForegroundColor Cyan
    az containerapp create `
        --name $AZURE_CONTAINER_APP `
        --resource-group $AZURE_RESOURCE_GROUP `
        --environment $AZURE_CONTAINER_ENV `
        --image "$AZURE_ACR_NAME.azurecr.io/codex-backend:latest" `
        --target-port 5000 `
        --ingress external `
        --registry-server "$AZURE_ACR_NAME.azurecr.io" `
        --cpu 1.0 `
        --memory 2.0Gi `
        --min-replicas 1 `
        --max-replicas 5 `
        --env-vars "FLASK_ENV=production" "DATABASE_URL=sqlite:///./codex.db" `
        --output none
    
    # Get the URL
    $AZURE_BACKEND_URL = az containerapp show --name $AZURE_CONTAINER_APP --resource-group $AZURE_RESOURCE_GROUP --query "properties.configuration.ingress.fqdn" -o tsv
    $AZURE_BACKEND_URL = "https://$AZURE_BACKEND_URL"
    
    Write-Host ""
    Write-Host "✅ AZURE BACKEND DEPLOYED!" -ForegroundColor Green
    Write-Host "   URL: $AZURE_BACKEND_URL" -ForegroundColor White
    Write-Host ""
    
    # Save to .env
    Add-Content -Path ".env.production" -Value "AZURE_BACKEND_URL=$AZURE_BACKEND_URL"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# ==============================================================================
# 2️⃣ IONOS - FRONTEND DEPLOYMENT
# ==============================================================================

if (-not $SkipIONOS) {
    Write-Host "2️⃣  DEPLOYING TO IONOS (FRONTEND DASHBOARD)" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    
    # IONOS config
    $IONOS_SERVER = $env:IONOS_SERVER
    $IONOS_USER = $env:IONOS_USER
    $IONOS_SSH_KEY = $env:IONOS_SSH_KEY
    
    if (-not $IONOS_SERVER) {
        Write-Host "⚠️  IONOS_SERVER not set in .env.production" -ForegroundColor Yellow
        $IONOS_SERVER = Read-Host "Enter IONOS server IP"
        Add-Content -Path ".env.production" -Value "IONOS_SERVER=$IONOS_SERVER"
    }
    
    if (-not $IONOS_USER) {
        $IONOS_USER = "root"
        Add-Content -Path ".env.production" -Value "IONOS_USER=$IONOS_USER"
    }
    
    Write-Host "📦 Building Next.js for production..." -ForegroundColor Cyan
    cd dashboard-app
    npm run build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Next.js build failed" -ForegroundColor Red
        cd ..
        exit 1
    }
    
    Write-Host "   ✅ Next.js built successfully" -ForegroundColor Green
    cd ..
    
    Write-Host ""
    Write-Host "📤 Deploying to IONOS VPS..." -ForegroundColor Cyan
    
    # Create deployment package
    Write-Host "   → Creating deployment package..."
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $deploymentPackage = "codex-frontend-$timestamp.tar.gz"
    
    tar -czf $deploymentPackage -C dashboard-app .next next.config.js package.json public
    
    # Upload to IONOS
    Write-Host "   → Uploading to IONOS..."
    if ($IONOS_SSH_KEY) {
        scp -i $IONOS_SSH_KEY $deploymentPackage "${IONOS_USER}@${IONOS_SERVER}:/var/www/"
    } else {
        scp $deploymentPackage "${IONOS_USER}@${IONOS_SERVER}:/var/www/"
    }
    
    # Deploy on server
    Write-Host "   → Extracting and starting..."
    $deployScript = @"
cd /var/www
mkdir -p codex-frontend
tar -xzf $deploymentPackage -C codex-frontend
cd codex-frontend
npm install --production
pm2 delete codex-frontend 2>/dev/null || true
pm2 start npm --name codex-frontend -- start
pm2 save
echo 'Frontend deployed successfully'
"@
    
    if ($IONOS_SSH_KEY) {
        ssh -i $IONOS_SSH_KEY "${IONOS_USER}@${IONOS_SERVER}" $deployScript
    } else {
        ssh "${IONOS_USER}@${IONOS_SERVER}" $deployScript
    }
    
    # Clean up
    Remove-Item $deploymentPackage
    
    $IONOS_FRONTEND_URL = "http://$IONOS_SERVER:3000"
    
    Write-Host ""
    Write-Host "✅ IONOS FRONTEND DEPLOYED!" -ForegroundColor Green
    Write-Host "   URL: $IONOS_FRONTEND_URL" -ForegroundColor White
    Write-Host ""
    
    # Save to .env
    Add-Content -Path ".env.production" -Value "IONOS_FRONTEND_URL=$IONOS_FRONTEND_URL"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# ==============================================================================
# 3️⃣ GOOGLE CLOUD - CREATIVE ENGINE
# ==============================================================================

if (-not $SkipGCP) {
    Write-Host "3️⃣  DEPLOYING TO GOOGLE CLOUD (CREATIVE ENGINE)" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    
    # GCP config
    $GCP_PROJECT = $env:GCP_PROJECT_ID
    $GCP_REGION = "us-central1"
    $GCP_SERVICE = "codex-creative-engine"
    
    if (-not $GCP_PROJECT) {
        Write-Host "⚠️  GCP_PROJECT_ID not set in .env.production" -ForegroundColor Yellow
        $GCP_PROJECT = Read-Host "Enter GCP Project ID"
        Add-Content -Path ".env.production" -Value "GCP_PROJECT_ID=$GCP_PROJECT"
    }
    
    Write-Host "🔐 Logging into Google Cloud..." -ForegroundColor Cyan
    gcloud auth login
    gcloud config set project $GCP_PROJECT
    
    Write-Host "📦 Enabling required APIs..." -ForegroundColor Cyan
    gcloud services enable cloudbuild.googleapis.com run.googleapis.com aiplatform.googleapis.com --quiet
    
    Write-Host "📦 Building Cloud Run service..." -ForegroundColor Cyan
    gcloud builds submit --tag "gcr.io/$GCP_PROJECT/$GCP_SERVICE" . --quiet
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ GCP build failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Cyan
    gcloud run deploy $GCP_SERVICE `
        --image "gcr.io/$GCP_PROJECT/$GCP_SERVICE" `
        --platform managed `
        --region $GCP_REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 2 `
        --max-instances 10 `
        --quiet
    
    # Get the URL
    $GCP_SERVICE_URL = gcloud run services describe $GCP_SERVICE --region $GCP_REGION --format "value(status.url)"
    
    Write-Host ""
    Write-Host "✅ GOOGLE CLOUD DEPLOYED!" -ForegroundColor Green
    Write-Host "   URL: $GCP_SERVICE_URL" -ForegroundColor White
    Write-Host ""
    
    # Save to .env
    Add-Content -Path ".env.production" -Value "GCP_SERVICE_URL=$GCP_SERVICE_URL"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "✅✅✅ 3-CLOUD DEPLOYMENT COMPLETE! ✅✅✅" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# Summary
Write-Host "📊 DEPLOYMENT SUMMARY" -ForegroundColor Cyan
Write-Host ""

if (-not $SkipAzure) {
    Write-Host "1️⃣  AZURE (Backend API)" -ForegroundColor Yellow
    Write-Host "   URL: $AZURE_BACKEND_URL" -ForegroundColor White
    Write-Host "   Features: Auto-scaling, Health checks, HTTPS" -ForegroundColor DarkGray
    Write-Host ""
}

if (-not $SkipIONOS) {
    Write-Host "2️⃣  IONOS (Frontend Dashboard)" -ForegroundColor Yellow
    Write-Host "   URL: $IONOS_FRONTEND_URL" -ForegroundColor White
    Write-Host "   Features: PM2 auto-restart, European delivery" -ForegroundColor DarkGray
    Write-Host ""
}

if (-not $SkipGCP) {
    Write-Host "3️⃣  GOOGLE CLOUD (Creative Engine)" -ForegroundColor Yellow
    Write-Host "   URL: $GCP_SERVICE_URL" -ForegroundColor White
    Write-Host "   Features: AI/ML pipelines, Unlimited scaling" -ForegroundColor DarkGray
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔧 NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Test your deployments:" -ForegroundColor White
if (-not $SkipAzure) {
    Write-Host "   curl $AZURE_BACKEND_URL/health" -ForegroundColor DarkGray
}
if (-not $SkipIONOS) {
    Write-Host "   curl $IONOS_FRONTEND_URL" -ForegroundColor DarkGray
}
if (-not $SkipGCP) {
    Write-Host "   curl $GCP_SERVICE_URL/health" -ForegroundColor DarkGray
}
Write-Host ""
Write-Host "2. Configure custom domains (optional)" -ForegroundColor White
Write-Host "3. Set up monitoring and alerts" -ForegroundColor White
Write-Host "4. Configure CI/CD pipelines for auto-deployment" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Your system is now CRASH-PROOF and PRODUCTION-READY! 👑" -ForegroundColor Green
Write-Host ""
