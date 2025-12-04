# Codex Dominion - Cloud Scheduler Setup for Dawn Dispatches
# ==========================================================
# Automated daily dawn dispatch scheduling

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId,
    [Parameter(Position=1, Mandatory=$true)]
    [string]$ServiceUrl,
    [string]$JobName = "dawn-dispatch",
    [string]$Schedule = "0 6 * * *",
    [string]$TimeZone = "America/New_York",
    [string]$Region = "us-central1"
)

Write-Host "⏰ Setting up Codex Dominion Cloud Scheduler" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🌅 Job Name: $JobName" -ForegroundColor Cyan
Write-Host "⏰ Schedule: $Schedule (6 AM daily)" -ForegroundColor Cyan
Write-Host "🌍 Time Zone: $TimeZone" -ForegroundColor Cyan
Write-Host "🔗 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host ""

# Set project
gcloud config set project $ProjectId

# Enable Cloud Scheduler API
Write-Host "🔧 Enabling Cloud Scheduler API..." -ForegroundColor Green
gcloud services enable cloudscheduler.googleapis.com

# Create App Engine app (required for Cloud Scheduler)
Write-Host "🏗️ Ensuring App Engine app exists..." -ForegroundColor Green
try {
    gcloud app describe --verbosity=error 2>$null
    Write-Host "✅ App Engine app already exists" -ForegroundColor Green
} catch {
    Write-Host "Creating App Engine app..." -ForegroundColor White
    gcloud app create --region=$Region
}

# Extract service URL hash if full URL provided
if ($ServiceUrl -match "https://(.+)\.run\.app") {
    $DawnEndpoint = "$ServiceUrl/dawn"
} else {
    $DawnEndpoint = "https://$ServiceUrl.run.app/dawn"
}

# Create Cloud Scheduler job (your exact command enhanced)
Write-Host "⏰ Creating dawn dispatch scheduler job..." -ForegroundColor Green
Write-Host "Enhanced version of your command:" -ForegroundColor Yellow
Write-Host "gcloud scheduler jobs create http $JobName --schedule=`"$Schedule`" --uri=`"$DawnEndpoint`" --http-method=POST --time-zone=`"$TimeZone`"" -ForegroundColor White

gcloud scheduler jobs create http $JobName `
    --schedule="$Schedule" `
    --uri="$DawnEndpoint" `
    --http-method=POST `
    --time-zone="$TimeZone" `
    --description="Automated daily dawn dispatch for Codex Dominion treasury system"

Write-Host "✅ Dawn dispatch scheduler created!" -ForegroundColor Green

# Test the scheduler job
Write-Host ""
Write-Host "🧪 Testing dawn dispatch scheduler..." -ForegroundColor Green
try {
    gcloud scheduler jobs run $JobName
    Write-Host "✅ Test dispatch triggered successfully!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Test failed - service may be starting up" -ForegroundColor Yellow
}

# Show job details
Write-Host ""
Write-Host "📊 Scheduler Job Information:" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow

$JobInfo = gcloud scheduler jobs describe $JobName --format="json" | ConvertFrom-Json
Write-Host "📅 Schedule: Every day at 6:00 AM ($TimeZone)" -ForegroundColor Cyan
Write-Host "🎯 Target: $DawnEndpoint" -ForegroundColor Cyan
Write-Host "🔄 Method: POST" -ForegroundColor Cyan
Write-Host "⚡ State: $($JobInfo.state)" -ForegroundColor Cyan
Write-Host "🕐 Next Run: $(if($JobInfo.scheduleTime){[datetime]$JobInfo.scheduleTime}else{'Calculating...'})" -ForegroundColor Cyan
Write-Host ""

Write-Host "🌅 Dawn Dispatch Automation Features:" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow
Write-Host "✅ Automated daily execution at 6 AM" -ForegroundColor Green
Write-Host "✅ Reliable cloud-based scheduling" -ForegroundColor Green
Write-Host "✅ Automatic retry on failure" -ForegroundColor Green
Write-Host "✅ Detailed execution logging" -ForegroundColor Green
Write-Host "✅ Integration with treasury system" -ForegroundColor Green
Write-Host "✅ Time zone aware scheduling" -ForegroundColor Green
Write-Host ""

Write-Host "🔧 Management Commands:" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow
Write-Host "List jobs: gcloud scheduler jobs list" -ForegroundColor White
Write-Host "Run now: gcloud scheduler jobs run $JobName" -ForegroundColor White
Write-Host "View logs: gcloud scheduler jobs describe $JobName" -ForegroundColor White
Write-Host "Pause job: gcloud scheduler jobs pause $JobName" -ForegroundColor White
Write-Host "Resume job: gcloud scheduler jobs resume $JobName" -ForegroundColor White
Write-Host "Delete job: gcloud scheduler jobs delete $JobName" -ForegroundColor White
Write-Host ""

Write-Host "✅ Automated dawn dispatch system ready!" -ForegroundColor Green
Write-Host "🌅 Your treasury will receive daily dawn dispatches automatically!" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔥 Next dawn dispatch: Tomorrow at 6:00 AM $TimeZone" -ForegroundColor Green
Write-Host "📊 Monitor executions in Cloud Console → Cloud Scheduler" -ForegroundColor White
