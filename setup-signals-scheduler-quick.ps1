# Quick Cloud Scheduler Setup for Signals Daily
# Direct execution of the gcloud scheduler command

param(
    [string]$ServiceHash = "",
    [string]$Region = "us-central1"
)

Write-Host "🕒 Creating Cloud Scheduler job for Signals Daily..." -ForegroundColor Green

if (-not $ServiceHash) {
    Write-Host "⚠️  Service hash not provided. Attempting to auto-detect..." -ForegroundColor Yellow

    # Try to get the service URL and extract hash
    try {
        $fullUrl = gcloud run services describe codex-signals --platform managed --region $Region --format "value(status.url)"
        if ($fullUrl -match "codex-signals-([a-z0-9]+)\.run\.app") {
            $ServiceHash = $matches[1]
            Write-Host "✅ Detected service hash: $ServiceHash" -ForegroundColor Green
        } else {
            Write-Host "❌ Could not extract service hash from URL: $fullUrl" -ForegroundColor Red
            Write-Host "Please provide the hash manually: .\setup-signals-scheduler-quick.ps1 -ServiceHash 'your-hash'" -ForegroundColor Cyan
            exit 1
        }
    } catch {
        Write-Host "❌ Could not detect service. Please provide hash manually." -ForegroundColor Red
        Write-Host "Usage: .\setup-signals-scheduler-quick.ps1 -ServiceHash 'your-hash'" -ForegroundColor Cyan
        exit 1
    }
}

$serviceUrl = "https://codex-signals-$ServiceHash.run.app"
Write-Host "🎯 Target URL: $serviceUrl/signals/daily" -ForegroundColor Cyan

# Execute the gcloud command
Write-Host ""
Write-Host "Executing Cloud Scheduler job creation..." -ForegroundColor Yellow

$command = @"
gcloud scheduler jobs create http signals-daily ``
  --schedule="0 6 * * *" ``
  --uri="$serviceUrl/signals/daily" ``
  --http-method=POST ``
  --headers="Content-Type=application/json" ``
  --message-body='{\"market\": [], \"positions\": []}' ``
  --time-zone="UTC" ``
  --location=$Region
"@

Write-Host "Command: $command" -ForegroundColor DarkGray
Write-Host ""

try {
    # Create the job
    gcloud scheduler jobs create http signals-daily `
      --schedule="0 6 * * *" `
      --uri="$serviceUrl/signals/daily" `
      --http-method=POST `
      --headers="Content-Type=application/json" `
      --message-body='{"market": [], "positions": []}' `
      --time-zone="UTC" `
      --location=$Region

    Write-Host "✅ Cloud Scheduler job 'signals-daily' created successfully!" -ForegroundColor Green

} catch {
    if ($_.Exception.Message -like "*already exists*") {
        Write-Host "⚠️  Job already exists. Updating..." -ForegroundColor Yellow

        gcloud scheduler jobs update http signals-daily `
          --schedule="0 6 * * *" `
          --uri="$serviceUrl/signals/daily" `
          --http-method=POST `
          --headers="Content-Type=application/json" `
          --message-body='{"market": [], "positions": []}' `
          --time-zone="UTC" `
          --location=$Region

        Write-Host "✅ Job updated!" -ForegroundColor Green
    } else {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Test the job immediately
Write-Host ""
Write-Host "🧪 Testing the scheduler job..." -ForegroundColor Yellow
try {
    gcloud scheduler jobs run signals-daily --location=$Region
    Write-Host "✅ Test execution triggered!" -ForegroundColor Green
    Write-Host "Check the Cloud Run logs to see if the request was received." -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  Could not trigger test run: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Signals Daily is now automated!" -ForegroundColor Green
Write-Host "   📅 Runs daily at 6:00 AM UTC" -ForegroundColor Cyan
Write-Host "   🎯 Target: $serviceUrl/signals/daily" -ForegroundColor Cyan
Write-Host "   📋 Payload: {\"market\": [], \"positions\": []}" -ForegroundColor Cyan
