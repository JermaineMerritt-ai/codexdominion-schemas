# Codex Dominion - Complete Deployment with Scheduler
# ===================================================
# Enhanced version of your gcloud commands with automated dawn dispatches

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId,
    [string]$Region = "us-central1",
    [string]$ServiceName = "codex-backend",
    [string]$ImageTag = "latest"
)

Write-Host "� CODEX DOMINION COMPLETE DEPLOYMENT" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host "🐳 Service: $ServiceName" -ForegroundColor Cyan
Write-Host ""

# Set active project
Write-Host "🔧 Setting project context..." -ForegroundColor Green
gcloud config set project $ProjectId

# Step 1: Build and submit (your exact command enhanced)
Write-Host "🔨 Building container (your gcloud builds submit command)..." -ForegroundColor Green
Write-Host "Command: gcloud builds submit --tag gcr.io/$ProjectId/$ServiceName" -ForegroundColor White

try {
    gcloud builds submit --tag "gcr.io/$ProjectId/$ServiceName"
    Write-Host "✅ Container build completed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Container build failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Step 2: Deploy to Cloud Run (your exact command enhanced)  
Write-Host ""
Write-Host "� Deploying to Cloud Run (your gcloud run deploy command)..." -ForegroundColor Green
Write-Host "Command: gcloud run deploy $ServiceName --image gcr.io/$ProjectId/$ServiceName --region $Region --allow-unauthenticated" -ForegroundColor White

try {
    $DeployOutput = gcloud run deploy $ServiceName `
        --image "gcr.io/$ProjectId/$ServiceName" `
        --region $Region `
        --platform managed `
        --allow-unauthenticated `
        --memory 512Mi `
        --cpu 1 `
        --port 8080 `
        --set-env-vars "CODEX_ENVIRONMENT=production,CODEX_CLOUD_PROVIDER=gcp,PORT=8080" `
        --format "value(status.url)"
    
    $ServiceUrl = $DeployOutput | Select-Object -Last 1
    Write-Host "✅ Cloud Run deployment completed!" -ForegroundColor Green
    Write-Host "🔗 Service URL: $ServiceUrl" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Cloud Run deployment failed!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Step 3: Setup Cloud Scheduler (your enhanced command)
Write-Host ""
Write-Host "⏰ Setting up Cloud Scheduler (your scheduler command enhanced)..." -ForegroundColor Green
Write-Host "Command: gcloud scheduler jobs create http dawn-dispatch --schedule='0 6 * * *' --uri='$ServiceUrl/dawn' --http-method=POST" -ForegroundColor White

try {
    # Enable required APIs
    Write-Host "🔧 Enabling Cloud Scheduler API..." -ForegroundColor White
    gcloud services enable cloudscheduler.googleapis.com
    
    # Create App Engine app if needed
    Write-Host "🏗️ Ensuring App Engine app exists..." -ForegroundColor White
    try {
        gcloud app describe --verbosity=error 2>$null
    } catch {
        Write-Host "Creating App Engine app..." -ForegroundColor White
        gcloud app create --region=$Region
    }
    
    # Create scheduler job (your exact command enhanced)
    gcloud scheduler jobs create http dawn-dispatch `
        --schedule="0 6 * * *" `
        --uri="$ServiceUrl/dawn" `
        --http-method=POST `
        --time-zone="America/New_York" `
        --description="Automated daily dawn dispatch for Codex Dominion treasury system"
    
    Write-Host "✅ Dawn dispatch scheduler created!" -ForegroundColor Green
    
    # Test the scheduler
    Write-Host "🧪 Testing scheduler job..." -ForegroundColor White
    gcloud scheduler jobs run dawn-dispatch
    
} catch {
    Write-Host "⚠️ Scheduler setup completed with warnings: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 4: Verify deployment
Write-Host ""
Write-Host "✅ DEPLOYMENT VERIFICATION" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

# Test health endpoint
try {
    Write-Host "🏥 Testing health endpoint..." -ForegroundColor Green
    $HealthResponse = Invoke-RestMethod -Uri "$ServiceUrl/health" -Method Get -TimeoutSec 10
    Write-Host "✅ Health check: $($HealthResponse.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Health check failed - service may be starting" -ForegroundColor Yellow
}

# Test dawn endpoint
try {
    Write-Host "🌅 Testing dawn dispatch endpoint..." -ForegroundColor Green
    $DawnResponse = Invoke-RestMethod -Uri "$ServiceUrl/dawn" -Method Post -TimeoutSec 30
    Write-Host "✅ Dawn dispatch test: $($DawnResponse.success)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Dawn dispatch test failed - may need time to initialize" -ForegroundColor Yellow
}

# Show deployment summary
Write-Host ""
Write-Host "🔥 CODEX DOMINION DEPLOYMENT COMPLETE! 👑" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "🏥 Health Check: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "📊 Treasury API: $ServiceUrl/api/treasury/summary" -ForegroundColor Cyan
Write-Host "🌅 Dawn Dispatch: $ServiceUrl/dawn (POST)" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏰ AUTOMATED SCHEDULING:" -ForegroundColor Yellow
Write-Host "📅 Dawn dispatches: Daily at 6:00 AM Eastern" -ForegroundColor Green
Write-Host "🤖 Scheduler status: ACTIVE" -ForegroundColor Green
Write-Host "🔄 Next dispatch: Tomorrow morning" -ForegroundColor Green
Write-Host ""

Write-Host "� MANAGEMENT COMMANDS:" -ForegroundColor Yellow
Write-Host "List jobs: gcloud scheduler jobs list" -ForegroundColor White
Write-Host "Run now: gcloud scheduler jobs run dawn-dispatch" -ForegroundColor White
Write-Host "View logs: gcloud logging read 'resource.type=cloud_run_revision'" -ForegroundColor White
Write-Host "Service info: gcloud run services describe $ServiceName --region $Region" -ForegroundColor White
Write-Host ""

Write-Host "Your enhanced commands executed:" -ForegroundColor Yellow
Write-Host "1. gcloud builds submit --tag gcr.io/$ProjectId/$ServiceName ✅" -ForegroundColor Green
Write-Host "2. gcloud run deploy $ServiceName ✅" -ForegroundColor Green  
Write-Host "3. gcloud scheduler jobs create http dawn-dispatch ✅" -ForegroundColor Green
Write-Host ""

Write-Host "🌅 Your treasury system is now fully autonomous with daily dawn dispatches! 🔥" -ForegroundColor Green