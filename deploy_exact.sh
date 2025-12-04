#!/bin/bash
# Codex Dominion - Exact Deployment Commands (Bash)
# =================================================
# Your EXACT commands in bash script format

set -e

PROJECT_ID="${1}"

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Usage: ./deploy_exact.sh PROJECT_ID"
    echo "   Example: ./deploy_exact.sh my-gcp-project"
    exit 1
fi

echo "🔥 Deploying Codex Dominion with your exact commands..."
echo "📋 Project ID: $PROJECT_ID"
echo ""

# Set the project
echo "📝 Setting project..."
gcloud config set project $PROJECT_ID

# Build container (your exact command)
echo "🏗️ Building container..."
echo "Command: gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-dashboard"
gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-dashboard

# Deploy to Cloud Run (your exact command)
echo ""
echo "🚀 Deploying to Cloud Run..."
echo "Command: gcloud run deploy codex-dashboard --image gcr.io/$PROJECT_ID/codex-dashboard --platform managed --region us-central1 --allow-unauthenticated --memory 512Mi --cpu 1"

gcloud run deploy codex-dashboard \
  --image gcr.io/$PROJECT_ID/codex-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1

# Get the service URL
echo ""
echo "✅ Deployment completed with your exact commands!"
SERVICE_URL=$(gcloud run services describe codex-dashboard --region=us-central1 --format="value(status.url)")

echo ""
echo "🔥 Codex Dominion Dashboard is live!"
echo "🌐 Service URL: $SERVICE_URL"
echo "❤️ Health Check: $SERVICE_URL/health"
echo "📊 Treasury API: $SERVICE_URL/api/treasury/summary"
echo "🌅 Dawn API: $SERVICE_URL/api/dawn/status"
echo ""

# Test the deployment
echo "🧪 Testing deployment..."
if curl -f "$SERVICE_URL/health" >/dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "⚠️ Service starting up - try again in 30 seconds"
fi

echo ""
echo "🎯 To redeploy, run:"
echo "./deploy_exact.sh $PROJECT_ID"
echo ""
echo "🔥 Your digital treasury is live in the cloud! 👑"
