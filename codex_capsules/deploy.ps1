# codex_capsules/deploy.ps1
# Codex Capsules Service Deployment Script

param(
    [string]$ProjectId = "codex-dominion-production",
    [string]$ServiceName = "codex-capsules",
    [string]$Region = "us-central1"
)

Write-Host "🚀 Deploying Codex Capsules Service..." -ForegroundColor Green

# Build and push container
Write-Host "📦 Building container..." -ForegroundColor Yellow
gcloud builds submit --tag gcr.io/$ProjectId/$ServiceName .

# Deploy to Cloud Run
Write-Host "🌐 Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --image gcr.io/$ProjectId/$ServiceName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 512Mi `
    --max-instances 5 `
    --timeout 60 `
    --set-env-vars "DATABASE_URL=$env:DATABASE_URL"

Write-Host "✅ Codex Capsules Service deployed successfully!" -ForegroundColor Green
Write-Host "🔗 Service URL: " -NoNewline -ForegroundColor Cyan
gcloud run services describe $ServiceName --platform managed --region $Region --format "value(status.url)"
