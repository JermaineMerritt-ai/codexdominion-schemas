# Setup Cloud Scheduler for Signals Daily Capsule
# This script creates a Cloud Scheduler job and registers it with Codex Capsules

param(
    [string]$ProjectId = "codex-dominion-production",
    [string]$Region = "us-central1",
    [string]$ServiceUrl = "",  # Will be auto-detected if not provided
    [string]$JobName = "signals-daily"
)

Write-Host "🕒 Setting up Cloud Scheduler for Signals Daily Capsule..." -ForegroundColor Green
Write-Host ""

# 1. Get the Cloud Run service URL if not provided
if (-not $ServiceUrl) {
    Write-Host "1. Detecting Cloud Run service URL..." -ForegroundColor Yellow
    try {
        $ServiceUrl = gcloud run services describe codex-signals --platform managed --region $Region --format "value(status.url)"
        if ($ServiceUrl) {
            Write-Host "✅ Found service URL: $ServiceUrl" -ForegroundColor Green
        } else {
            Write-Host "❌ Could not find codex-signals service. Please deploy it first." -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "❌ Error getting service URL: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "1. Using provided service URL: $ServiceUrl" -ForegroundColor Green
}

# 2. Create the Cloud Scheduler job
Write-Host ""
Write-Host "2. Creating Cloud Scheduler job..." -ForegroundColor Yellow

$schedulerCommand = @"
gcloud scheduler jobs create http $JobName `
  --schedule="0 6 * * *" `
  --uri="$ServiceUrl/signals/daily" `
  --http-method=POST `
  --headers="Content-Type=application/json" `
  --message-body='{"market": [], "positions": []}' `
  --time-zone="UTC" `
  --location=$Region `
  --project=$ProjectId
"@

try {
    Write-Host "Executing: $schedulerCommand" -ForegroundColor Cyan
    Invoke-Expression $schedulerCommand
    Write-Host "✅ Cloud Scheduler job '$JobName' created successfully!" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -like "*already exists*") {
        Write-Host "⚠️  Job already exists, updating..." -ForegroundColor Yellow
        
        # Update existing job
        $updateCommand = @"
gcloud scheduler jobs update http $JobName `
  --schedule="0 6 * * *" `
  --uri="$ServiceUrl/signals/daily" `
  --http-method=POST `
  --headers="Content-Type=application/json" `
  --message-body='{"market": [], "positions": []}' `
  --time-zone="UTC" `
  --location=$Region `
  --project=$ProjectId
"@
        
        Invoke-Expression $updateCommand
        Write-Host "✅ Cloud Scheduler job updated!" -ForegroundColor Green
    } else {
        Write-Host "❌ Error creating scheduler job: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# 3. Register/Update the capsule in Codex Capsules system
Write-Host ""
Write-Host "3. Registering capsule in Codex Capsules system..." -ForegroundColor Yellow

$capsuleData = @{
    slug = "signals-daily"
    title = "Daily Signals Engine (Cloud Scheduler)"
    kind = "engine"
    mode = "automated"
    version = "2.1.0"
    status = "active"
    entrypoint = "POST $ServiceUrl/signals/daily"
    schedule = "0 6 * * *"
} | ConvertTo-Json

try {
    # Check if capsules service is running
    $capsulesUrl = "http://localhost:8080"
    $health = Invoke-RestMethod -Uri "$capsulesUrl/" -Method GET -ErrorAction SilentlyContinue
    
    if ($health) {
        $result = Invoke-RestMethod -Uri "$capsulesUrl/api/capsules" -Method POST -ContentType "application/json" -Body $capsuleData
        Write-Host "✅ Capsule registered in tracking system!" -ForegroundColor Green
        Write-Host "   Slug: $($result.slug)" -ForegroundColor Cyan
        Write-Host "   Mode: $($result.mode) (automated via Cloud Scheduler)" -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  Capsules service not running locally. Capsule not registered in tracking system." -ForegroundColor Yellow
        Write-Host "   Start the capsules service to enable tracking: cd codex_capsules && python -m uvicorn main:app --port 8080" -ForegroundColor Cyan
    }
} catch {
    Write-Host "⚠️  Could not register capsule in tracking system: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 4. Show job details
Write-Host ""
Write-Host "4. Scheduler job details..." -ForegroundColor Yellow
try {
    gcloud scheduler jobs describe $JobName --location=$Region --project=$ProjectId
} catch {
    Write-Host "❌ Error getting job details: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Signals Daily Capsule is now scheduled!" -ForegroundColor Green
Write-Host "   📅 Schedule: Daily at 6:00 AM UTC" -ForegroundColor Cyan
Write-Host "   🎯 Target: $ServiceUrl/signals/daily" -ForegroundColor Cyan
Write-Host "   ⚙️  Job Name: $JobName" -ForegroundColor Cyan
Write-Host "   🌐 Region: $Region" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Useful commands:" -ForegroundColor Yellow
Write-Host "   • List jobs: gcloud scheduler jobs list --location=$Region" -ForegroundColor Cyan
Write-Host "   • Run now: gcloud scheduler jobs run $JobName --location=$Region" -ForegroundColor Cyan
Write-Host "   • View logs: gcloud scheduler jobs describe $JobName --location=$Region" -ForegroundColor Cyan
Write-Host "   • Delete job: gcloud scheduler jobs delete $JobName --location=$Region" -ForegroundColor Cyan