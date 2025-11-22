# Generate Cloud Scheduler Command for Signals Daily
# This script outputs the exact gcloud command you need to run

param(
    [string]$ServiceHash = "YOUR-HASH-HERE",
    [string]$Region = "us-central1",
    [string]$ProjectId = "codex-dominion-production"
)

Write-Host "📋 Cloud Scheduler Command Generator for Signals Daily" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

if ($ServiceHash -eq "YOUR-HASH-HERE") {
    Write-Host "⚠️  Please replace 'YOUR-HASH-HERE' with your actual Cloud Run service hash" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To find your service hash:" -ForegroundColor Cyan
    Write-Host "1. Go to Google Cloud Console > Cloud Run" -ForegroundColor Cyan
    Write-Host "2. Find your codex-signals service" -ForegroundColor Cyan
    Write-Host "3. The URL will be like: https://codex-signals-abc123def.run.app" -ForegroundColor Cyan
    Write-Host "4. The hash is the part after 'codex-signals-': abc123def" -ForegroundColor Cyan
    Write-Host ""
}

$serviceUrl = "https://codex-signals-$ServiceHash.run.app"

Write-Host "🎯 Service URL: $serviceUrl" -ForegroundColor Cyan
Write-Host "📅 Schedule: Daily at 6:00 AM UTC (0 6 * * *)" -ForegroundColor Cyan
Write-Host "📦 Payload: {`"market`": [], `"positions`": []}" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 COPY AND RUN THIS COMMAND:" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow

$command = @"
gcloud scheduler jobs create http signals-daily \
  --schedule="0 6 * * *" \
  --uri="$serviceUrl/signals/daily" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body='{\"market\": [], \"positions\": []}' \
  --time-zone="UTC" \
  --location=$Region \
  --project=$ProjectId
"@

Write-Host $command -ForegroundColor White
Write-Host ""
Write-Host "===============================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "🔧 Additional useful commands:" -ForegroundColor Green
Write-Host ""
Write-Host "• List all scheduler jobs:" -ForegroundColor Cyan
Write-Host "  gcloud scheduler jobs list --location=$Region --project=$ProjectId" -ForegroundColor White
Write-Host ""
Write-Host "• Run the job immediately (for testing):" -ForegroundColor Cyan
Write-Host "  gcloud scheduler jobs run signals-daily --location=$Region --project=$ProjectId" -ForegroundColor White
Write-Host ""
Write-Host "• View job details:" -ForegroundColor Cyan
Write-Host "  gcloud scheduler jobs describe signals-daily --location=$Region --project=$ProjectId" -ForegroundColor White
Write-Host ""
Write-Host "• Delete the job:" -ForegroundColor Cyan
Write-Host "  gcloud scheduler jobs delete signals-daily --location=$Region --project=$ProjectId" -ForegroundColor White
Write-Host ""

# Also create a PowerShell version
Write-Host "📋 PowerShell version (for Windows):" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow

$psCommand = @"
gcloud scheduler jobs create http signals-daily `
  --schedule="0 6 * * *" `
  --uri="$serviceUrl/signals/daily" `
  --http-method=POST `
  --headers="Content-Type=application/json" `
  --message-body='{\"market\": [], \"positions\": []}' `
  --time-zone="UTC" `
  --location=$Region `
  --project=$ProjectId
"@

Write-Host $psCommand -ForegroundColor White
Write-Host "====================================" -ForegroundColor Yellow

Write-Host ""
Write-Host "💡 After creating the job, you can register it in the Capsules system:" -ForegroundColor Green
Write-Host ""
Write-Host "`$capsule = @{" -ForegroundColor White
Write-Host "    slug = `"signals-daily-scheduler`"" -ForegroundColor White  
Write-Host "    title = `"Daily Signals Engine (Automated)`"" -ForegroundColor White
Write-Host "    kind = `"engine`"" -ForegroundColor White
Write-Host "    mode = `"automated`"" -ForegroundColor White
Write-Host "    entrypoint = `"Cloud Scheduler -> $serviceUrl/signals/daily`"" -ForegroundColor White
Write-Host "    schedule = `"0 6 * * *`"" -ForegroundColor White
Write-Host "    version = `"3.0.0`"" -ForegroundColor White
Write-Host "} | ConvertTo-Json" -ForegroundColor White
Write-Host ""
Write-Host "Invoke-RestMethod -Uri `"http://localhost:8080/api/capsules`" -Method POST -ContentType `"application/json`" -Body `$capsule" -ForegroundColor White