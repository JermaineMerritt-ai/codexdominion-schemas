# 🔥 CODEX DOMINION - GCP Setup Guide
# Complete guide for Google Cloud deployment with billing setup

Write-Host "🔥 === CODEX DOMINION GCP DEPLOYMENT GUIDE ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 === SETUP CHECKLIST ===" -ForegroundColor Yellow
Write-Host "We need to complete these steps:" -ForegroundColor White
Write-Host ""
Write-Host "1. ✅ Google Cloud Account - You have this" -ForegroundColor Green
Write-Host "2. ✅ gcloud CLI installed - You have this" -ForegroundColor Green
Write-Host "3. ✅ Docker installed - You have this" -ForegroundColor Green
Write-Host "4. ✅ Docker image built - You have this" -ForegroundColor Green
Write-Host "5. ❌ Billing account enabled - NEEDS SETUP" -ForegroundColor Red
Write-Host ""

Write-Host "💳 === BILLING SETUP REQUIRED ===" -ForegroundColor Red
Write-Host "Your project needs a billing account to use Google Cloud services." -ForegroundColor Yellow
Write-Host ""
Write-Host "To enable billing:" -ForegroundColor Cyan
Write-Host "1. Go to: https://console.cloud.google.com/billing" -ForegroundColor White
Write-Host "2. Create a billing account (Google often provides $300 free credits)" -ForegroundColor White
Write-Host "3. Link your project 'jermaine-super-action-agent' to the billing account" -ForegroundColor White
Write-Host ""

$setupBilling = Read-Host "Have you enabled billing for your project? (y/n)"

if ($setupBilling -eq "y") {
    Write-Host ""
    Write-Host "✅ Great! Let's continue with deployment..." -ForegroundColor Green

    # Enable APIs
    Write-Host "⚡ Enabling required APIs..." -ForegroundColor Yellow
    gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ APIs enabled successfully" -ForegroundColor Green

        # Push image again
        Write-Host "📤 Pushing Docker image to Container Registry..." -ForegroundColor Yellow
        docker push gcr.io/jermaine-super-action-agent/codex-dashboard

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Image pushed successfully!" -ForegroundColor Green

            # Deploy to Cloud Run
            Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow

            gcloud run deploy codex-dashboard `
                --image=gcr.io/jermaine-super-action-agent/codex-dashboard `
                --region=us-central1 `
                --platform=managed `
                --allow-unauthenticated `
                --port=8501 `
                --memory=1Gi `
                --cpu=1

            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Deployment successful!" -ForegroundColor Green

                $SERVICE_URL = gcloud run services describe codex-dashboard --region=us-central1 --format="value(status.url)"
                Write-Host ""
                Write-Host "🎉 === DEPLOYMENT COMPLETE ===" -ForegroundColor Green
                Write-Host "🔗 Your Codex Dashboard is live at:" -ForegroundColor Cyan
                Write-Host "   $SERVICE_URL" -ForegroundColor White
                Write-Host ""
                Write-Host "🔥 Codex Dominion now burns eternal in Google Cloud! ✨" -ForegroundColor Magenta

                # Open in browser
                $openBrowser = Read-Host "Open your dashboard in browser? (y/n)"
                if ($openBrowser -eq "y") {
                    Start-Process $SERVICE_URL
                }

            } else {
                Write-Host "❌ Deployment failed" -ForegroundColor Red
                Write-Host "Check the Cloud Run logs in the Google Cloud Console" -ForegroundColor Yellow
            }

        } else {
            Write-Host "❌ Image push failed" -ForegroundColor Red
            Write-Host "This might be due to authentication issues" -ForegroundColor Yellow
        }

    } else {
        Write-Host "❌ Failed to enable APIs" -ForegroundColor Red
    }

} else {
    Write-Host ""
    Write-Host "💡 === ALTERNATIVE DEPLOYMENT OPTIONS ===" -ForegroundColor Cyan
    Write-Host "While you set up billing, you can:" -ForegroundColor White
    Write-Host ""
    Write-Host "1. 🐳 Run locally with Docker:" -ForegroundColor Yellow
    Write-Host "   docker run -p 8080:8501 gcr.io/jermaine-super-action-agent/codex-dashboard" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. 🌊 Deploy to DigitalOcean App Platform (easier billing):" -ForegroundColor Yellow
    Write-Host "   - Create account at digitalocean.com" -ForegroundColor Gray
    Write-Host "   - Use App Platform with GitHub integration" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. 🚀 Deploy to Heroku (free tier available):" -ForegroundColor Yellow
    Write-Host "   - Create account at heroku.com" -ForegroundColor Gray
    Write-Host "   - Use Heroku CLI to deploy" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. 📡 Deploy to Railway (simple deployment):" -ForegroundColor Yellow
    Write-Host "   - Create account at railway.app" -ForegroundColor Gray
    Write-Host "   - Connect GitHub repo for auto-deploy" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📋 === YOUR CURRENT STATUS ===" -ForegroundColor Cyan
Write-Host "✅ Docker image built: gcr.io/jermaine-super-action-agent/codex-dashboard" -ForegroundColor Green
Write-Host "✅ Ready for deployment once billing is enabled" -ForegroundColor Green
Write-Host "✅ Can run locally with Docker right now" -ForegroundColor Green
