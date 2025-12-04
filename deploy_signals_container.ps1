#!/usr/bin/env powershell
<#
🔥 CODEX SIGNALS CONTAINER DEPLOYMENT 📊
Build and deploy Codex Signals to Google Cloud Run

The Merritt Method™ - Cloud-Native Portfolio Intelligence
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,

    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",

    [Parameter(Mandatory=$false)]
    [string]$ServiceName = "codex-signals",

    [Parameter(Mandatory=$false)]
    [switch]$BuildOnly = $false,

    [Parameter(Mandatory=$false)]
    [switch]$LocalTest = $false
)

Write-Host "🔥 CODEX SIGNALS CONTAINER DEPLOYMENT 📊" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Configuration
$ImageName = "gcr.io/$ProjectId/$ServiceName"
$DockerfilePath = "codex_signals/Dockerfile"

try {
    # Validate prerequisites
    Write-Host "🔍 Validating prerequisites..." -ForegroundColor Yellow

    # Check Docker
    if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker is not installed or not in PATH"
    }

    # Check gcloud (unless local test)
    if (!$LocalTest -and !(Get-Command gcloud -ErrorAction SilentlyContinue)) {
        throw "Google Cloud CLI is not installed or not in PATH"
    }

    # Check required files
    if (!(Test-Path $DockerfilePath)) {
        throw "Dockerfile not found at: $DockerfilePath"
    }

    if (!(Test-Path "main.py")) {
        throw "main.py not found in root directory"
    }

    if (!(Test-Path "requirements.txt")) {
        throw "requirements.txt not found in root directory"
    }

    Write-Host "✅ Prerequisites validated" -ForegroundColor Green

    if ($LocalTest) {
        # Local Docker testing
        Write-Host "🐳 Building Docker image locally..." -ForegroundColor Yellow
        docker build -f $DockerfilePath -t $ServiceName .

        if ($LASTEXITCODE -ne 0) {
            throw "Docker build failed"
        }

        Write-Host "✅ Docker image built successfully" -ForegroundColor Green
        Write-Host "🚀 Starting local container..." -ForegroundColor Yellow

        # Stop any existing container
        docker stop $ServiceName 2>$null
        docker rm $ServiceName 2>$null

        # Run the container
        docker run -d --name $ServiceName -p 8000:8080 $ServiceName

        if ($LASTEXITCODE -ne 0) {
            throw "Failed to start container"
        }

        Write-Host "✅ Container started successfully" -ForegroundColor Green
        Write-Host "🌐 API available at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 Documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "" -ForegroundColor White
        Write-Host "To stop: docker stop $ServiceName" -ForegroundColor Gray
        return
    }

    # Cloud deployment
    Write-Host "☁️ Configuring Google Cloud..." -ForegroundColor Yellow
    gcloud config set project $ProjectId

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set Google Cloud project"
    }

    # Enable required APIs
    Write-Host "🔧 Enabling required APIs..." -ForegroundColor Yellow
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com

    # Build with Cloud Build
    Write-Host "🏗️ Building container with Cloud Build..." -ForegroundColor Yellow
    gcloud builds submit --tag $ImageName

    if ($LASTEXITCODE -ne 0) {
        throw "Cloud Build failed"
    }

    Write-Host "✅ Container built successfully" -ForegroundColor Green

    if ($BuildOnly) {
        Write-Host "🎯 Build completed (BuildOnly flag set)" -ForegroundColor Cyan
        Write-Host "Image: $ImageName" -ForegroundColor Gray
        return
    }

    # Deploy to Cloud Run
    Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Yellow
    gcloud run deploy $ServiceName `
        --image $ImageName `
        --platform managed `
        --region $Region `
        --allow-unauthenticated `
        --memory 512Mi `
        --cpu 1 `
        --max-instances 5 `
        --timeout 60 `
        --port 8080 `
        --set-env-vars="ENVIRONMENT=production"

    if ($LASTEXITCODE -ne 0) {
        throw "Cloud Run deployment failed"
    }

    # Get service URL
    $ServiceUrl = gcloud run services describe $ServiceName --region $Region --format="value(status.url)"

    Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "🔥 CODEX SIGNALS API DEPLOYED 📊" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
    Write-Host "📚 API Docs: $ServiceUrl/docs" -ForegroundColor Cyan
    Write-Host "🏥 Health Check: $ServiceUrl/health" -ForegroundColor Cyan
    Write-Host "📊 Daily Signals: $ServiceUrl/signals/daily" -ForegroundColor Cyan
    Write-Host "📝 Bulletin: $ServiceUrl/bulletin?format=md" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor White

    # Test the deployment
    Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
    try {
        $healthResponse = Invoke-RestMethod -Uri "$ServiceUrl/health" -Method GET -TimeoutSec 30
        Write-Host "✅ Health check passed: $($healthResponse.status)" -ForegroundColor Green

        # Test bulletin endpoint
        $bulletinResponse = Invoke-RestMethod -Uri "$ServiceUrl/bulletin?format=md" -Method POST -TimeoutSec 30
        Write-Host "✅ Bulletin endpoint working: Generated $($bulletinResponse.tier_counts.Alpha + $bulletinResponse.tier_counts.Beta + $bulletinResponse.tier_counts.Gamma + $bulletinResponse.tier_counts.Delta) signals" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ Warning: Post-deployment test failed: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "   Service may still be starting up. Check manually: $ServiceUrl/health" -ForegroundColor Gray
    }

    Write-Host "" -ForegroundColor White
    Write-Host "🎯 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "- Set up Cloud Scheduler for automated signals generation" -ForegroundColor Gray
    Write-Host "- Configure Cloud SQL if using database persistence" -ForegroundColor Gray
    Write-Host "- Set up monitoring and alerting" -ForegroundColor Gray
    Write-Host "- Integrate with existing Codex Dominion dawn dispatch" -ForegroundColor Gray

}
catch {
    Write-Host "" -ForegroundColor White
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "" -ForegroundColor White
    Write-Host "🔍 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "- Check Docker installation: docker --version" -ForegroundColor Gray
    Write-Host "- Check gcloud auth: gcloud auth list" -ForegroundColor Gray
    Write-Host "- Check project access: gcloud projects list" -ForegroundColor Gray
    Write-Host "- Verify billing is enabled on project" -ForegroundColor Gray
    exit 1
}

Write-Host "" -ForegroundColor White
Write-Host "🔥 Codex Signals containerized deployment complete! 👑" -ForegroundColor Cyan
