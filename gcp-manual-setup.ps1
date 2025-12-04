# 🔥 CODEX DOMINION - Google Cloud Setup (No CLI Required)
# Instructions for manual GCP deployment

Write-Host "🔥 === CODEX DOMINION GCP SETUP (MANUAL) ===" -ForegroundColor Cyan
Write-Host "This script provides instructions for GCP deployment without gcloud CLI" -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 === PREREQUISITES ===" -ForegroundColor Cyan
Write-Host "1. Google Cloud Account" -ForegroundColor White
Write-Host "2. Docker installed ✅" -ForegroundColor Green
Write-Host "3. Web browser for Google Cloud Console" -ForegroundColor White
Write-Host ""

Write-Host "🚀 === DEPLOYMENT OPTIONS ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Option 1: 🌐 Google Cloud Console (Manual)" -ForegroundColor Green
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host "1. Go to: https://console.cloud.google.com" -ForegroundColor White
Write-Host "2. Create new project or select existing" -ForegroundColor White
Write-Host "3. Enable Cloud Run API" -ForegroundColor White
Write-Host "4. Go to Cloud Run → Create Service" -ForegroundColor White
Write-Host "5. Choose 'Deploy one revision from existing container image'" -ForegroundColor White
Write-Host "6. Use our pre-built image: 'gcr.io/cloudrun/hello'" -ForegroundColor White
Write-Host "7. Configure: Port 8501, Memory 1GB, CPU 1" -ForegroundColor White
Write-Host "8. Allow unauthenticated invocations" -ForegroundColor White
Write-Host "9. Deploy!" -ForegroundColor White
Write-Host ""

Write-Host "Option 2: 🐳 Docker Hub + Cloud Run" -ForegroundColor Blue
Write-Host "-----------------------------------" -ForegroundColor Gray
Write-Host "1. Build and push to Docker Hub:" -ForegroundColor White
Write-Host "   docker build -t your-username/codex-dominion ." -ForegroundColor Gray
Write-Host "   docker push your-username/codex-dominion" -ForegroundColor Gray
Write-Host "2. Use this image in Cloud Run console" -ForegroundColor White
Write-Host ""

Write-Host "Option 3: 📦 Container Registry Upload" -ForegroundColor Magenta
Write-Host "------------------------------------" -ForegroundColor Gray
Write-Host "1. Build local image:" -ForegroundColor White
Write-Host "   docker build -t codex-dominion ." -ForegroundColor Gray
Write-Host "2. Save image:" -ForegroundColor White
Write-Host "   docker save codex-dominion:latest | gzip > codex-dominion.tar.gz" -ForegroundColor Gray
Write-Host "3. Upload via Google Cloud Console" -ForegroundColor White
Write-Host ""

Write-Host "💡 === QUICK START RECOMMENDATION ===" -ForegroundColor Yellow
Write-Host "For fastest deployment:" -ForegroundColor White
Write-Host ""
Write-Host "1. Run our Docker deployment locally first:" -ForegroundColor Cyan
Write-Host "   .\docker-deploy-complete.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Test everything works on http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Then choose cloud option above" -ForegroundColor Cyan
Write-Host ""

# Check if user wants to install gcloud CLI
$install_gcloud = Read-Host "Would you like to install Google Cloud CLI for automatic deployment? (y/n)"

if ($install_gcloud -eq "y") {
    Write-Host ""
    Write-Host "🔧 === INSTALLING GOOGLE CLOUD CLI ===" -ForegroundColor Cyan
    Write-Host "Installing Google Cloud CLI..." -ForegroundColor Yellow

    # Download and install gcloud CLI
    $gcloud_url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
    $installer_path = "$env:TEMP\GoogleCloudSDKInstaller.exe"

    Write-Host "📥 Downloading installer..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $gcloud_url -OutFile $installer_path
        Write-Host "✅ Downloaded successfully!" -ForegroundColor Green

        Write-Host "🚀 Starting installer..." -ForegroundColor Yellow
        Start-Process -FilePath $installer_path -Wait

        Write-Host "✅ Installation complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Restart PowerShell" -ForegroundColor White
        Write-Host "2. Run: gcloud auth login" -ForegroundColor White
        Write-Host "3. Run: .\setup-gcp.ps1" -ForegroundColor White
        Write-Host "4. Run: .\deploy-gcp.ps1" -ForegroundColor White

    } catch {
        Write-Host "❌ Download failed. Please install manually from:" -ForegroundColor Red
        Write-Host "https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "✅ Manual deployment instructions provided above" -ForegroundColor Green
    Write-Host "💡 Run .\docker-deploy-complete.ps1 to start with local deployment" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔥 Ready to ignite the sacred flames in the cloud! ✨" -ForegroundColor Magenta
