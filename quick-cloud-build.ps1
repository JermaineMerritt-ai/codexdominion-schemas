# 🔥 CODEX DOMINION - Quick Cloud Build
# Simplified script for: gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/codex-dashboard

Write-Host "🔥 === QUICK CLOUD BUILD DEPLOYMENT ===" -ForegroundColor Cyan

# Get project ID
$PROJECT_ID = gcloud config get-value project 2>$null
if (-not $PROJECT_ID -or $PROJECT_ID -eq "(unset)") {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
    gcloud config set project $PROJECT_ID
}

Write-Host "🎯 Project: $PROJECT_ID" -ForegroundColor Green
Write-Host "🏗️ Building: gcr.io/$PROJECT_ID/codex-dashboard" -ForegroundColor Yellow

# Authenticate if needed
Write-Host "🔐 Checking authentication..." -ForegroundColor Yellow
gcloud auth list --filter=status:ACTIVE --format="value(account)" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔑 Please authenticate..." -ForegroundColor Yellow
    gcloud auth login
}

# Enable required APIs
Write-Host "⚡ Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com containerregistry.googleapis.com --quiet

# Configure Docker
Write-Host "🐳 Configuring Docker..." -ForegroundColor Yellow
gcloud auth configure-docker --quiet

# The main command you wanted
Write-Host "🚀 Running: gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-dashboard" -ForegroundColor Cyan
gcloud builds submit --tag "gcr.io/$PROJECT_ID/codex-dashboard"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host "📦 Image available: gcr.io/$PROJECT_ID/codex-dashboard" -ForegroundColor Green

    Write-Host ""
    Write-Host "🚀 Deploy to Cloud Run with:" -ForegroundColor Cyan
    Write-Host "gcloud run deploy codex-dashboard --image gcr.io/$PROJECT_ID/codex-dashboard --region us-central1 --allow-unauthenticated --port 8501" -ForegroundColor White
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
}
