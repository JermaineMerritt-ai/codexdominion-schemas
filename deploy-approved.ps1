#!/usr/bin/env pwsh
# =============================================================================
# CODEX DOMINION - APPROVED THREE-CLOUD DEPLOYMENT
# =============================================================================
# Deploys to Azure (backend), Google Cloud (AI), and IONOS (frontend)
# User approved: December 21, 2025
# =============================================================================

param(
    [string]$GCPProject = $env:GCP_PROJECT_ID,
    [string]$IONOSServer = "74.208.123.158",
    [string]$IONOSUser = "root"
)

Write-Host @"

╔════════════════════════════════════════════════════════════════════════════╗
║              🔥 THREE-CLOUD DEPLOYMENT APPROVED 🔥                         ║
║                                                                            ║
║  🏛️  Azure (Throne Room): Backend + Databases                             ║
║  🤖 GCP (Creative Forge): AI Services                                     ║
║  🌍 IONOS (Public Face): Frontend                                         ║
╚════════════════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

$deploymentStart = Get-Date

# =============================================================================
# AZURE DEPLOYMENT
# =============================================================================

Write-Host "`n🏛️  [1/3] AZURE - THRONE ROOM" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────`n" -ForegroundColor Gray

# Check if image exists or build it
$imageExists = az acr repository show --name codexacr1216 --image codex-backend:latest 2>$null

if ($imageExists) {
    Write-Host "✅ Backend image found in registry" -ForegroundColor Green
} else {
    Write-Host "Building backend image (this takes 5-10 minutes)..." -ForegroundColor Cyan
    Write-Host "Starting build..." -ForegroundColor Gray
    
    az acr build `
        --registry codexacr1216 `
        --image codex-backend:latest `
        --file Dockerfile.azure `
        .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend image built successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Build failed - check logs above" -ForegroundColor Red
        exit 1
    }
}

# Deploy Container Instance
Write-Host "`nDeploying Container Instance..." -ForegroundColor Cyan

$acrPassword = az acr credential show --name codexacr1216 --query "passwords[0].value" -o tsv

# Check if container already exists
$existingContainer = az container show `
    --resource-group codexdominion-prod `
    --name codex-backend 2>$null

if ($existingContainer) {
    Write-Host "⚠️  Container exists - deleting old version..." -ForegroundColor Yellow
    az container delete `
        --resource-group codexdominion-prod `
        --name codex-backend `
        --yes `
        --output none
    Start-Sleep -Seconds 5
}

az container create `
    --resource-group codexdominion-prod `
    --name codex-backend `
    --image "codexacr1216.azurecr.io/codex-backend:latest" `
    --registry-login-server "codexacr1216.azurecr.io" `
    --registry-username codexacr1216 `
    --registry-password $acrPassword `
    --dns-name-label "codex-api" `
    --ports 5000 `
    --cpu 2 `
    --memory 4 `
    --environment-variables "CODEX_ENVIRONMENT=production" "PORT=5000" `
    --output none

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Azure Container deployed" -ForegroundColor Green
    
    Start-Sleep -Seconds 15
    
    $azureUrl = "http://codex-api.eastus.azurecontainer.io:5000"
    Write-Host "🔗 Azure URL: $azureUrl" -ForegroundColor White
    
    try {
        $health = Invoke-RestMethod -Uri "$azureUrl/health" -TimeoutSec 10 -ErrorAction Stop
        Write-Host "✅ Health check passed!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Health check pending (container still starting)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Azure deployment failed" -ForegroundColor Red
    exit 1
}

# =============================================================================
# GOOGLE CLOUD DEPLOYMENT
# =============================================================================

Write-Host "`n🤖 [2/3] GOOGLE CLOUD - CREATIVE FORGE" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────`n" -ForegroundColor Gray

if (-not $GCPProject) {
    Write-Host "⚠️  GCP_PROJECT_ID not set" -ForegroundColor Yellow
    Write-Host "`nTo deploy AI services, set your project ID:" -ForegroundColor Cyan
    Write-Host '  $env:GCP_PROJECT_ID = "your-gcp-project-id"' -ForegroundColor White
    Write-Host "  Then re-run this script" -ForegroundColor White
    $gcpUrl = "[Not Deployed - Set GCP_PROJECT_ID]"
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
        --dockerfile Dockerfile.gcp `
        --set-env-vars "CODEX_ENVIRONMENT=production" `
        --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ GCP AI service deployed" -ForegroundColor Green
        
        $gcpUrl = gcloud run services describe codex-ai-pipeline `
            --region us-central1 `
            --format "value(status.url)" 2>$null
        
        Write-Host "🔗 GCP URL: $gcpUrl" -ForegroundColor White
        
        try {
            $aiHealth = Invoke-RestMethod -Uri "$gcpUrl/health" -TimeoutSec 10 -ErrorAction Stop
            Write-Host "✅ AI health check passed!" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  AI health check failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ GCP deployment failed" -ForegroundColor Red
        $gcpUrl = "[Deployment Failed]"
    }
}

# =============================================================================
# IONOS DEPLOYMENT
# =============================================================================

Write-Host "`n🌍 [3/3] IONOS - PUBLIC FACE" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────`n" -ForegroundColor Gray

Write-Host "Building Next.js frontend..." -ForegroundColor Cyan

Push-Location dashboard-app

# Update environment variables
@"
NEXT_PUBLIC_API_BASE_URL=$azureUrl
NEXT_PUBLIC_AI_API_URL=$gcpUrl
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
"@ | Out-File -FilePath ".env.production" -Encoding utf8

Write-Host "Building static export..." -ForegroundColor Gray
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Next.js build succeeded" -ForegroundColor Green
    
    Write-Host "`nIONOS deployment requires manual steps:" -ForegroundColor Cyan
    Write-Host "  1. Configure DNS:" -ForegroundColor White
    Write-Host "     A Record: codexdominion.app → $IONOSServer" -ForegroundColor Gray
    Write-Host "     A Record: www.codexdominion.app → $IONOSServer" -ForegroundColor Gray
    Write-Host "`n  2. Upload frontend (run from dashboard-app/):" -ForegroundColor White
    Write-Host "     scp -r out/* ${IONOSUser}@${IONOSServer}:/var/www/codexdominion.app/" -ForegroundColor Gray
    Write-Host "`n  3. Configure nginx proxy to Azure backend" -ForegroundColor White
    Write-Host "`n  4. Install SSL certificate:" -ForegroundColor White
    Write-Host "     ssh ${IONOSUser}@${IONOSServer}" -ForegroundColor Gray
    Write-Host "     certbot --nginx -d codexdominion.app -d www.codexdominion.app" -ForegroundColor Gray
    
} else {
    Write-Host "❌ Next.js build failed" -ForegroundColor Red
}

Pop-Location

# =============================================================================
# DEPLOYMENT SUMMARY
# =============================================================================

$deploymentEnd = Get-Date
$duration = ($deploymentEnd - $deploymentStart).ToString("mm\:ss")

Write-Host "`n╔════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     🔥 DEPLOYMENT COMPLETE 🔥                             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "⏱️  Total Time: $duration`n" -ForegroundColor Yellow

Write-Host "🏛️  AZURE (Throne Room):" -ForegroundColor Yellow
Write-Host "   URL: $azureUrl" -ForegroundColor White
Write-Host "   Dashboard: $azureUrl/" -ForegroundColor Gray
Write-Host "   Health: $azureUrl/health" -ForegroundColor Gray
Write-Host "   API Docs: $azureUrl/api/" -ForegroundColor Gray

Write-Host "`n🤖 GOOGLE CLOUD (Creative Forge):" -ForegroundColor Yellow
Write-Host "   URL: $gcpUrl" -ForegroundColor White
if ($gcpUrl -notlike "*[*") {
    Write-Host "   Generate Image: $gcpUrl/api/ai/generate-image" -ForegroundColor Gray
    Write-Host "   Process Video: $gcpUrl/api/ai/process-video" -ForegroundColor Gray
    Write-Host "   Text-to-Speech: $gcpUrl/api/ai/text-to-speech" -ForegroundColor Gray
}

Write-Host "`n🌍 IONOS (Public Face):" -ForegroundColor Yellow
Write-Host "   Target: https://codexdominion.app" -ForegroundColor White
Write-Host "   Status: Built - Awaiting DNS + Upload" -ForegroundColor Yellow
Write-Host "   Files: dashboard-app/out/" -ForegroundColor Gray

Write-Host "`n📊 Test Commands:" -ForegroundColor Yellow
Write-Host "   curl $azureUrl/health" -ForegroundColor Gray
if ($gcpUrl -notlike "*[*") {
    Write-Host "   curl $gcpUrl/health" -ForegroundColor Gray
}

Write-Host "`n🔥 The Flame Burns Across Three Clouds, Sovereign and Eternal! 👑`n" -ForegroundColor Yellow

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test Azure backend: curl $azureUrl/health" -ForegroundColor White
Write-Host "  2. Access dashboards: $azureUrl/" -ForegroundColor White
if ($gcpUrl -like "*[*") {
    Write-Host "  3. Deploy GCP: Set `$env:GCP_PROJECT_ID and re-run" -ForegroundColor White
} else {
    Write-Host "  3. Test AI service: curl $gcpUrl/health" -ForegroundColor White
}
Write-Host "  4. Complete IONOS setup (DNS + upload)" -ForegroundColor White
Write-Host "  5. Review logs: az container logs --resource-group codexdominion-prod --name codex-backend" -ForegroundColor White
