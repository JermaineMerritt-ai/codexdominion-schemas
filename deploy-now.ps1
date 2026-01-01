#!/usr/bin/env pwsh
# =============================================================================
# CODEX DOMINION - STREAMLINED DEPLOYMENT SCRIPT
# =============================================================================
# Deploys to Azure (backend), GCP (AI), and optionally IONOS (frontend)
#
# Usage:
#   .\deploy-now.ps1                    # Deploy Azure + GCP
#   .\deploy-now.ps1 -IncludeIONOS      # Deploy all three clouds
#   .\deploy-now.ps1 -GCPProject "my-project-id" # Specify GCP project
# =============================================================================

param(
    [string]$GCPProject = $env:GCP_PROJECT_ID,
    [switch]$IncludeIONOS,
    [string]$IONOSServer = $env:IONOS_SERVER,
    [string]$IONOSUser = $env:IONOS_USER
)

$ErrorActionPreference = "Continue"

# =============================================================================
# CONFIGURATION
# =============================================================================

$AZURE_RG = "codexdominion-prod"
$AZURE_LOCATION = "eastus"
$AZURE_ACR = "codexacr1216"

Write-Host @"
╔════════════════════════════════════════════════════════════════════════════╗
║           🔥 CODEX DOMINION - MULTI-CLOUD DEPLOYMENT 🔥                   ║
║                                                                            ║
║  🏛️  Azure: Backend + Databases                                           ║
║  🤖 Google Cloud: AI Services                                             ║
$(if ($IncludeIONOS) {"║  🌍 IONOS: Frontend                                                       ║"})
╚════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# =============================================================================
# STEP 1: DEPLOY AZURE BACKEND
# =============================================================================

Write-Host "`n🏛️  STEP 1: AZURE BACKEND DEPLOYMENT" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────`n" -ForegroundColor Gray

# Check if image exists
Write-Host "Checking for existing backend image..." -ForegroundColor Cyan
$existingImage = az acr repository show --name $AZURE_ACR --image codex-backend:latest 2>$null

if ($existingImage) {
    Write-Host "✅ Backend image already exists in ACR" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backend image not found - building now..." -ForegroundColor Yellow
    Write-Host "This will take 5-10 minutes...`n" -ForegroundColor Gray
    
    az acr build `
        --registry $AZURE_ACR `
        --image codex-backend:latest `
        --file Dockerfile.azure `
        . `
        --no-logs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend image built successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Backend image build failed" -ForegroundColor Red
        exit 1
    }
}

# Deploy Container Instance
Write-Host "`nDeploying Flask API to Container Instance..." -ForegroundColor Cyan

$acrPassword = az acr credential show --name $AZURE_ACR --query "passwords[0].value" -o tsv

az container create `
    --resource-group $AZURE_RG `
    --name codex-backend `
    --image "$AZURE_ACR.azurecr.io/codex-backend:latest" `
    --registry-login-server "$AZURE_ACR.azurecr.io" `
    --registry-username $AZURE_ACR `
    --registry-password $acrPassword `
    --dns-name-label "codex-backend-api" `
    --ports 5000 `
    --cpu 2 `
    --memory 4 `
    --environment-variables `
        "CODEX_ENVIRONMENT=production" `
        "PORT=5000" `
    --output none

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container Instance deployed" -ForegroundColor Green
    
    # Get backend URL
    $backendFQDN = az container show `
        --resource-group $AZURE_RG `
        --name codex-backend `
        --query "ipAddress.fqdn" `
        -o tsv
    
    $backendUrl = "http://$backendFQDN:5000"
    Write-Host "Backend URL: $backendUrl" -ForegroundColor White
    
    # Test health endpoint
    Write-Host "`nTesting backend health..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    try {
        $healthCheck = Invoke-RestMethod -Uri "$backendUrl/health" -TimeoutSec 5
        Write-Host "✅ Backend is healthy!" -ForegroundColor Green
        Write-Host "   Status: $($healthCheck.status)" -ForegroundColor Gray
    } catch {
        Write-Host "⚠️  Backend health check failed (may still be starting)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Container deployment failed" -ForegroundColor Red
}

# =============================================================================
# STEP 2: DEPLOY GOOGLE CLOUD AI
# =============================================================================

Write-Host "`n🤖 STEP 2: GOOGLE CLOUD AI PIPELINE" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────`n" -ForegroundColor Gray

if (-not $GCPProject) {
    Write-Host "⚠️  GCP_PROJECT_ID not set - skipping Google Cloud deployment" -ForegroundColor Yellow
    Write-Host "`nTo deploy AI services, run:" -ForegroundColor Cyan
    Write-Host '   $env:GCP_PROJECT_ID = "your-gcp-project-id"' -ForegroundColor White
    Write-Host '   .\deploy-now.ps1 -GCPProject "your-gcp-project-id"' -ForegroundColor White
} else {
    Write-Host "Deploying AI service to Cloud Run..." -ForegroundColor Cyan
    Write-Host "Project: $GCPProject" -ForegroundColor Gray
    
    gcloud config set project $GCPProject 2>$null
    
    gcloud run deploy codex-ai-pipeline `
        --source . `
        --platform managed `
        --region us-central1 `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 2 `
        --port 8080 `
        --set-env-vars "CODEX_ENVIRONMENT=production" `
        --dockerfile Dockerfile.gcp `
        --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ AI Pipeline deployed" -ForegroundColor Green
        
        $aiUrl = gcloud run services describe codex-ai-pipeline `
            --region us-central1 `
            --format "value(status.url)" 2>$null
        
        Write-Host "AI URL: $aiUrl" -ForegroundColor White
        
        # Test AI health
        try {
            $aiHealth = Invoke-RestMethod -Uri "$aiUrl/health" -TimeoutSec 5
            Write-Host "✅ AI service is healthy!" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  AI health check failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ AI deployment failed" -ForegroundColor Red
    }
}

# =============================================================================
# STEP 3: DEPLOY IONOS FRONTEND (OPTIONAL)
# =============================================================================

if ($IncludeIONOS) {
    Write-Host "`n🌍 STEP 3: IONOS FRONTEND" -ForegroundColor Yellow
    Write-Host "───────────────────────────────────────`n" -ForegroundColor Gray
    
    if (-not $IONOSServer) {
        Write-Host "⚠️  IONOS_SERVER not set - skipping frontend deployment" -ForegroundColor Yellow
        Write-Host "`nTo deploy frontend:" -ForegroundColor Cyan
        Write-Host '   $env:IONOS_SERVER = "your.server.ip"' -ForegroundColor White
        Write-Host '   $env:IONOS_USER = "root"' -ForegroundColor White
        Write-Host '   .\deploy-now.ps1 -IncludeIONOS' -ForegroundColor White
    } else {
        Write-Host "Building Next.js frontend..." -ForegroundColor Cyan
        
        Push-Location dashboard-app
        npm run build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Next.js build succeeded" -ForegroundColor Green
            
            Write-Host "`nUploading to IONOS..." -ForegroundColor Cyan
            # Deployment logic here
            Write-Host "⚠️  Manual upload required - see MULTI_CLOUD_DEPLOYMENT_STATUS.md" -ForegroundColor Yellow
        } else {
            Write-Host "❌ Next.js build failed" -ForegroundColor Red
        }
        
        Pop-Location
    }
}

# =============================================================================
# DEPLOYMENT SUMMARY
# =============================================================================

Write-Host "`n╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     🔥 DEPLOYMENT SUMMARY 🔥                              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "🏛️  Azure Backend:" -ForegroundColor Yellow
if ($backendUrl) {
    Write-Host "   ✅ Deployed: $backendUrl" -ForegroundColor Green
    Write-Host "   📊 Dashboards: $backendUrl/" -ForegroundColor Gray
    Write-Host "   🔍 Health: $backendUrl/health" -ForegroundColor Gray
} else {
    Write-Host "   ❌ Not deployed" -ForegroundColor Red
}

Write-Host "`n🤖 Google Cloud AI:" -ForegroundColor Yellow
if ($aiUrl) {
    Write-Host "   ✅ Deployed: $aiUrl" -ForegroundColor Green
    Write-Host "   🎨 Generate Image: $aiUrl/api/ai/generate-image" -ForegroundColor Gray
    Write-Host "   🎬 Process Video: $aiUrl/api/ai/process-video" -ForegroundColor Gray
} elseif ($GCPProject) {
    Write-Host "   ⚠️  Deployment attempted - check logs" -ForegroundColor Yellow
} else {
    Write-Host "   ⏭️  Skipped (no GCP project)" -ForegroundColor Gray
}

if ($IncludeIONOS) {
    Write-Host "`n🌍 IONOS Frontend:" -ForegroundColor Yellow
    Write-Host "   📋 Ready for manual deployment" -ForegroundColor Yellow
}

Write-Host "`n🔥 The Flame Burns Across Multiple Clouds! 👑`n" -ForegroundColor Yellow

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test Azure backend: curl $backendUrl/health" -ForegroundColor White
if ($aiUrl) {
    Write-Host "2. Test AI service: curl $aiUrl/health" -ForegroundColor White
}
Write-Host "3. Review full docs: MULTI_CLOUD_DEPLOYMENT_STATUS.md" -ForegroundColor White
