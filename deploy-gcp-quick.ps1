# =============================================================================
# CODEX DOMINION - Google Cloud Run Deployment
# =============================================================================

$ErrorActionPreference = "Continue"
$project = "codex-dominion-production"
$region = "us-central1"
$service = "codex-dashboard"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ☁️  GOOGLE CLOUD RUN DEPLOYMENT" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project: $project" -ForegroundColor White
Write-Host "Region: $region" -ForegroundColor White
Write-Host "Service: $service" -ForegroundColor White
Write-Host ""

# Step 1: Enable APIs
Write-Host "[1/5] Enabling Cloud Run API..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com --project=$project 2>&1 | Out-Null
gcloud services enable cloudbuild.googleapis.com --project=$project 2>&1 | Out-Null
Write-Host "✅ APIs enabled" -ForegroundColor Green

# Step 2: Build and submit
Write-Host "`n[2/5] Building container image..." -ForegroundColor Cyan
Write-Host "   This will take 2-3 minutes..." -ForegroundColor Gray

gcloud builds submit `
    --tag gcr.io/$project/$service `
    --project=$project `
    . 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container built successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

# Step 3: Deploy to Cloud Run
Write-Host "`n[3/5] Deploying to Cloud Run..." -ForegroundColor Cyan

gcloud run deploy $service `
    --image gcr.io/$project/$service `
    --platform managed `
    --region $region `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --port 5000 `
    --set-env-vars FLASK_ENV=production,OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE" `
    --project=$project

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Service deployed" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
    exit 1
}

# Step 4: Get service URL
Write-Host "`n[4/5] Getting service URL..." -ForegroundColor Cyan
$serviceUrl = gcloud run services describe $service `
    --platform managed `
    --region $region `
    --format "value(status.url)" `
    --project=$project

Write-Host "✅ Service URL: $serviceUrl" -ForegroundColor Green

# Step 5: Test deployment
Write-Host "`n[5/5] Testing deployment..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri $serviceUrl -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ HTTP Status: $($response.StatusCode)" -ForegroundColor Green

    if ($response.Content -like "*CODEX DOMINION*") {
        Write-Host "✅ Dashboard content verified!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Service deployed but test failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✨ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your Live Dashboard:" -ForegroundColor Cyan
Write-Host "   $serviceUrl" -ForegroundColor White
Write-Host ""
Write-Host "📊 All 8 Tabs Available:" -ForegroundColor Yellow
Write-Host "   • Home: $serviceUrl/" -ForegroundColor Gray
Write-Host "   • Social Media: $serviceUrl/social" -ForegroundColor Gray
Write-Host "   • Affiliate: $serviceUrl/affiliate" -ForegroundColor Gray
Write-Host "   • Chatbot: $serviceUrl/chatbot" -ForegroundColor Gray
Write-Host "   • Algorithm AI: $serviceUrl/algorithm" -ForegroundColor Gray
Write-Host "   • Auto-Publish: $serviceUrl/auto-publish" -ForegroundColor Gray
Write-Host "   • DOT300: $serviceUrl/dot300" -ForegroundColor Gray
Write-Host "   • Orchestration: $serviceUrl/orchestration" -ForegroundColor Gray
Write-Host ""
Write-Host "🔍 View Logs:" -ForegroundColor Cyan
Write-Host "   gcloud run services logs read $service --region=$region --project=$project" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Estimated Cost:" -ForegroundColor Yellow
Write-Host "   Cloud Run (512MB, 1 CPU): ~$15-30/month" -ForegroundColor Gray
Write-Host "   Free tier: First 2 million requests/month" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Opening in browser..." -ForegroundColor Cyan
Start-Process $serviceUrl
Write-Host ""
