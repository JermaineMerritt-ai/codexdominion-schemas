# Codex Dominion - Google Cloud Run Deployment Guide

# =================================================

This guide explains how to deploy your Codex Dominion Treasury & Dawn Dispatch system to Google Cloud Run.

## Prerequisites

1. **Google Cloud Project**: Create or select a project

1. **gcloud CLI**: Install and authenticate

   ```bash
   # Install gcloud CLI (if not installed)
   # Follow: https://cloud.google.com/sdk/docs/install

   # Authenticate
   gcloud auth login

   # Set project
   gcloud config set project YOUR_PROJECT_ID
   ```

1. **Enable APIs**:

   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

## Quick Deployment

### Option 1: Using Cloud Build (Recommended)

```bash
# Replace YOUR_PROJECT_ID with your actual project ID
export PROJECT_ID="your-project-id"

# Deploy using Cloud Build configuration
gcloud builds submit --config cloudbuild.yaml
```

### Option 2: Manual Build and Deploy

```bash
# Replace YOUR_PROJECT_ID with your actual project ID
export PROJECT_ID="your-project-id"

# Build container
gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-backend

# Deploy to Cloud Run
gcloud run deploy codex-backend \
  --image gcr.io/$PROJECT_ID/codex-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --port 8080 \
  --set-env-vars CODEX_ENVIRONMENT=production,CODEX_CLOUD_PROVIDER=gcp
```

### Option 3: Using PowerShell Script (Windows)

```powershell
# Run the deployment script
.\deploy.ps1 your-project-id
```

## Verification

After deployment, test your service:

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe codex-backend --region=us-central1 --format="value(status.url)")

# Health check
curl $SERVICE_URL/health

# Treasury summary
curl "$SERVICE_URL/api/treasury/summary?days=7"

# Dawn dispatch status
curl $SERVICE_URL/api/dawn/status
```

## Available Endpoints

- **Health Check**: `/health`
- **Treasury Summary**: `/api/treasury/summary?days=N`
- **Dawn Status**: `/api/dawn/status`
- **Main Page**: `/`

## Configuration

The system automatically detects Cloud Run environment and:

- Uses PORT environment variable
- Operates in JSON-only mode (PostgreSQL optional)
- Provides full treasury and dawn dispatch functionality
- Maintains all existing CLI functionality

## Updating Deployment

To update your deployment:

```bash
# Rebuild and redeploy
gcloud builds submit --config cloudbuild.yaml
```

## Monitoring

View logs:

```bash
gcloud run services logs read codex-backend --region=us-central1
```

## Cost Optimization

The service is configured with:

- **CPU**: 1 vCPU
- **Memory**: 512Mi
- **Min Instances**: 0 (scales to zero when not in use)
- **Max Instances**: 10
- **Concurrency**: 80 requests per instance

This configuration minimizes costs while providing good performance.

## Security

- Service allows unauthenticated access (suitable for APIs)
- All treasury data stored in secure JSON ledger
- Health checks validate system integrity
- Built-in error handling and graceful degradation

## Support

For issues or questions:

1. Check service logs: `gcloud run services logs read codex-backend --region=us-central1`
1. Verify health endpoint: `curl SERVICE_URL/health`
1. Test individual components with the unified launcher CLI

---

🔥 **Your Digital Sovereignty Awaits in the Cloud!** 👑
