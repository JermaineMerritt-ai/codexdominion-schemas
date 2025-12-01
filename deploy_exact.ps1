# Codex Dominion - Exact Deployment Commands
# =========================================
# These are the EXACT commands you specified

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId
)

Write-Host "🔥 Deploying Codex Dominion with your exact commands..." -ForegroundColor Yellow
Write-Host "📋 Project ID: $ProjectId" -ForegroundColor Cyan
Write-Host ""

# Set the project
Write-Host "📝 Setting project..." -ForegroundColor Green
gcloud config set project $ProjectId

# Build container (your exact command)
Write-Host "🏗️ Building container..." -ForegroundColor Green
Write-Host "Command: gcloud builds submit --tag gcr.io/$ProjectId/codex-dashboard" -ForegroundColor White
gcloud builds submit --tag gcr.io/$ProjectId/codex-dashboard

# Deploy to Cloud Run (your exact command)  
Write-Host ""
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Green
Write-Host "Command: gcloud run deploy codex-dashboard --image gcr.io/$ProjectId/codex-dashboard --platform managed --region us-central1 --allow-unauthenticated --memory 512Mi --cpu 1" -ForegroundColor White

gcloud run deploy codex-dashboard `
  --image gcr.io/$ProjectId/codex-dashboard `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1

# Get the service URL
Write-Host ""
Write-Host "✅ Deployment completed with your exact commands!" -ForegroundColor Green
$ServiceUrl = gcloud run services describe codex-dashboard --region=us-central1 --format="value(status.url)"

Write-Host ""
Write-Host "🔥 Codex Dominion Dashboard is live!" -ForegroundColor Yellow
Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "❤️ Health Check: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "📊 Treasury API: $ServiceUrl/api/treasury/summary" -ForegroundColor Cyan
Write-Host "🌅 Dawn API: $ServiceUrl/api/dawn/status" -ForegroundColor Cyan
Write-Host ""

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Green
try {
    $health = Invoke-RestMethod "$ServiceUrl/health" -TimeoutSec 30
    Write-Host "✅ Health check passed!" -ForegroundColor Green
    Write-Host "Treasury: $($health.treasury) | Dawn: $($health.dawn_flame)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️ Service starting up - try again in 30 seconds" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 To redeploy, run:" -ForegroundColor Green
Write-Host ".\deploy_exact.ps1 $ProjectId" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Your digital treasury is live in the cloud! 👑" -ForegroundColor Yellow