# Signals Daily Cloud Scheduler Setup Guide

## 🎯 Overview
This guide provides the exact commands needed to set up Google Cloud Scheduler for your Daily Signals Engine, automating the execution at 6:00 AM UTC daily.

## 📋 Prerequisites
1. **Google Cloud Project** with billing enabled
2. **APIs Enabled**:
   - Cloud Scheduler API
   - Cloud Run API (if not already enabled)
3. **Cloud Run Service** deployed (codex-signals)

## 🚀 Step 1: Get Your Service Hash

1. Go to [Google Cloud Console > Cloud Run](https://console.cloud.google.com/run)
2. Find your `codex-signals` service
3. Note the URL format: `https://codex-signals-ABC123DEF.run.app`
4. Extract the hash: `ABC123DEF` (the part after `codex-signals-`)

## ⚙️ Step 2: Create the Scheduler Job

Replace `<YOUR-HASH>` with your actual service hash:

### Linux/macOS (bash):
```bash
gcloud scheduler jobs create http signals-daily \
  --schedule="0 6 * * *" \
  --uri="https://codex-signals-<YOUR-HASH>.run.app/signals/daily" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body='{"market": [], "positions": []}' \
  --time-zone="UTC" \
  --location=us-central1 \
  --project=codex-dominion-production
```

### Windows (PowerShell):
```powershell
gcloud scheduler jobs create http signals-daily `
  --schedule="0 6 * * *" `
  --uri="https://codex-signals-<YOUR-HASH>.run.app/signals/daily" `
  --http-method=POST `
  --headers="Content-Type=application/json" `
  --message-body='{"market": [], "positions": []}' `
  --time-zone="UTC" `
  --location=us-central1 `
  --project=codex-dominion-production
```

## 🧪 Step 3: Test the Job

Run the job immediately to test:
```bash
gcloud scheduler jobs run signals-daily --location=us-central1 --project=codex-dominion-production
```

## 📊 Step 4: Register in Codex Capsules System

If you have the Codex Capsules service running locally:

```powershell
$capsule = @{
    slug = "signals-daily-scheduler"
    title = "Daily Signals Engine (Cloud Scheduler)"
    kind = "engine"
    mode = "automated"
    entrypoint = "Cloud Scheduler -> https://codex-signals-<YOUR-HASH>.run.app/signals/daily"
    schedule = "0 6 * * *"
    version = "3.0.0"
    status = "active"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8080/api/capsules" -Method POST -ContentType "application/json" -Body $capsule
```

## 🔧 Management Commands

### List all scheduler jobs:
```bash
gcloud scheduler jobs list --location=us-central1 --project=codex-dominion-production
```

### View job details:
```bash
gcloud scheduler jobs describe signals-daily --location=us-central1 --project=codex-dominion-production
```

### Update the job:
```bash
gcloud scheduler jobs update http signals-daily \
  --schedule="0 6 * * *" \
  --uri="https://codex-signals-<YOUR-HASH>.run.app/signals/daily" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body='{"market": [], "positions": []}' \
  --time-zone="UTC" \
  --location=us-central1 \
  --project=codex-dominion-production
```

### Delete the job:
```bash
gcloud scheduler jobs delete signals-daily --location=us-central1 --project=codex-dominion-production
```

## 📈 Monitoring

1. **Cloud Scheduler Logs**: Check execution history in Cloud Console
2. **Cloud Run Logs**: Monitor your service receiving the scheduled requests
3. **Codex Capsules**: Track performance via the capsules API (if registered)

## 🎉 Result

Once set up, your Daily Signals Engine will automatically execute every day at 6:00 AM UTC, sending a POST request with the payload `{"market": [], "positions": []}` to trigger your signals processing workflow.

## 📋 Current Capsules Status

Two capsules are now registered in the Codex Capsules system:

1. **signals-daily** (custodian mode) - Manual execution version
2. **signals-daily-scheduler** (automated mode) - Cloud Scheduler version

Both track the same operation but represent different execution modes for complete operational sovereignty tracking.