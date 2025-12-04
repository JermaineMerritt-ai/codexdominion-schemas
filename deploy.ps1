# Codex Dominion - Google Cloud Deployment (PowerShell)
# =====================================================

param(
    [Parameter(Position=0)]
    [string]$ProjectId = "your-project-id"
)

$ServiceName = "codex-dashboard"
$Region = "us-central1"
$ImageName = "gcr.io/$ProjectId/$ServiceName"

Write-Host "🔥 Codex Dominion - Google Cloud Run Deployment" -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Yellow
Write-Host "📋 Project ID: $ProjectId" -ForegroundColor Cyan
Write-Host "🚀 Service: $ServiceName" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is configured
$currentProject = gcloud config get-value project 2>$null
if (!$currentProject) {
    Write-Host "❌ Please configure gcloud first:" -ForegroundColor Red
    Write-Host "   gcloud auth login"
    Write-Host "   gcloud config set project $ProjectId"
    exit 1
}

# Set the project
Write-Host "📝 Setting project..." -ForegroundColor Green
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "🔧 Enabling required APIs..." -ForegroundColor Green
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build using Cloud Build
Write-Host "🏗️  Building container image..." -ForegroundColor Green
gcloud builds submit --tag $ImageName .

# Deploy to Cloud Run (matching your exact commands)
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy $ServiceName `
    --image $ImageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1

# Get the service URL
Write-Host ""
Write-Host "✅ Deployment completed!" -ForegroundColor Green
$ServiceUrl = gcloud run services describe $ServiceName --region=$Region --format="value(status.url)"

Write-Host ""
Write-Host "🔥 Codex Dominion is live!" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow
Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "❤️  Health Check: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "📊 Treasury API: $ServiceUrl/api/treasury/summary" -ForegroundColor Cyan
Write-Host "🌅 Dawn API: $ServiceUrl/api/dawn/status" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Quick test:" -ForegroundColor Green
Write-Host "Invoke-RestMethod $ServiceUrl/health" -ForegroundColor White
Write-Host ""
Write-Host "🎯 To update your deployment:" -ForegroundColor Green
Write-Host ".\deploy.ps1 $ProjectId" -ForegroundColor White
Write-Host ""

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Green
try {
    $health = Invoke-RestMethod "$ServiceUrl/health" -TimeoutSec 30
    if ($health.status -eq "healthy") {
        Write-Host "✅ Health check passed!" -ForegroundColor Green
        Write-Host "Treasury Status: $($health.treasury)" -ForegroundColor Cyan
        Write-Host "Dawn Flame: $($health.dawn_flame)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️  Health check failed - service may still be starting" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔥 Digital sovereignty established on Google Cloud! 👑" -ForegroundColor Yellow
