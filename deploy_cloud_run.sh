# Codex Dominion - Cloud Run Deployment Script
# ===========================================

# Step 1: Build and Push Container (choose one method)

## Method A: Using gcloud builds (recommended for production)
# gcloud builds submit --tag gcr.io/codex-dominion-prod/codex-signals --timeout=20m

## Method B: Using Docker (if gcloud builds has issues)
# docker build -t gcr.io/codex-dominion-prod/codex-signals .
# docker push gcr.io/codex-dominion-prod/codex-signals

# Step 2: Deploy to Cloud Run
gcloud run deploy codex-signals \
  --image gcr.io/codex-dominion-prod/codex-signals \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=2Gi \
  --cpu=2 \
  --timeout=3600 \
  --concurrency=1000 \
  --min-instances=0 \
  --max-instances=100 \
  --set-env-vars="CODEX_ENVIRONMENT=production,CODEX_CLOUD_PROVIDER=gcp,PORT=8080"

# Step 3: Verify Deployment
echo "🚀 Deployment Status:"
gcloud run services describe codex-signals --region=us-central1 --format="value(status.url)"

echo "🔍 Service Status:"
gcloud run services list --region=us-central1

# Step 4: Test the Service
echo "🧪 Testing service health:"
SIGNAL_URL=$(gcloud run services describe codex-signals --region=us-central1 --format="value(status.url)")
echo "Service URL: $SIGNAL_URL"

# Uncomment to test endpoints:
# curl -X GET "$SIGNAL_URL/health"
# curl -X GET "$SIGNAL_URL/api/signals/daily"

echo "✅ Codex Signals deployed to Cloud Run!"
echo "🏛️ Operational Sovereignty Platform: Container Deployed"
