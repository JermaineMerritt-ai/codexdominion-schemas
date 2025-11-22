#!/usr/bin/env powershell
<#
🔥 CODEX SIGNALS QUICK DEPLOY 📊
Simple deployment using exact gcloud commands
#>

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId
)

Write-Host "🔥 CODEX SIGNALS QUICK DEPLOY 📊" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Project: $ProjectId" -ForegroundColor Yellow
Write-Host "Region: us-central1" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

try {
    # Set project
    Write-Host "⚙️ Setting project..." -ForegroundColor Yellow
    gcloud config set project $ProjectId
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set project"
    }

    # Build and push container
    Write-Host "🏗️ Building container..." -ForegroundColor Yellow
    gcloud builds submit --tag "gcr.io/$ProjectId/codex-signals"
    
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed"
    }
    
    Write-Host "✅ Build completed successfully" -ForegroundColor Green

    # Deploy to Cloud Run
    Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
    gcloud run deploy codex-signals `
        --image "gcr.io/$ProjectId/codex-signals" `
        --platform managed `
        --region us-central1 `
        --allow-unauthenticated `
        --memory 512Mi `
        --cpu 1 `
        --max-instances 5 `
        --timeout 60

    if ($LASTEXITCODE -ne 0) {
        throw "Deploy failed"
    }

    Write-Host "✅ Deployment completed successfully" -ForegroundColor Green

    # Get service URL
    $ServiceUrl = gcloud run services describe codex-signals --region us-central1 --format="value(status.url)" 2>$null

    Write-Host "" -ForegroundColor White
    Write-Host "🎯 DEPLOYMENT COMPLETE" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
    Write-Host "📚 API Docs: $ServiceUrl/signals/docs" -ForegroundColor Cyan  
    Write-Host "🏥 Health: $ServiceUrl/signals/health" -ForegroundColor Cyan
    Write-Host "📊 Signals: $ServiceUrl/signals/daily" -ForegroundColor Cyan
    Write-Host "📝 Bulletin: $ServiceUrl/signals/bulletin?format=md" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor White
    Write-Host "🔥 Codex Signals deployed successfully! 👑" -ForegroundColor Yellow

    # Test the deployment
    Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
    try {
        $HealthUrl = "$ServiceUrl/signals/health"
        $response = Invoke-RestMethod -Uri $HealthUrl -Method GET -TimeoutSec 30
        Write-Host "✅ Health check passed: $($response.status)" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Warning: Health check failed (service may still be starting)" -ForegroundColor Yellow
        Write-Host "   Check manually: $ServiceUrl/signals/health" -ForegroundColor Gray
    }

}
catch {
    Write-Host "" -ForegroundColor White
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "" -ForegroundColor White
    Write-Host "🔍 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "- Check gcloud auth: gcloud auth list" -ForegroundColor Gray
    Write-Host "- Check project access: gcloud projects list" -ForegroundColor Gray
    Write-Host "- Verify billing enabled: gcloud billing accounts list" -ForegroundColor Gray
    Write-Host "- Enable APIs: gcloud services enable cloudbuild.googleapis.com run.googleapis.com" -ForegroundColor Gray
    exit 1
}