#!/usr/bin/env bash
# 🔥 CODEX SIGNALS QUICK DEPLOY 📊
# Simple deployment using your exact gcloud commands

set -e

# Check if PROJECT_ID is provided
if [ -z "$1" ]; then
    echo "Usage: $0 PROJECT_ID"
    echo "Example: $0 my-gcp-project"
    exit 1
fi

PROJECT_ID=$1

echo "🔥 CODEX SIGNALS QUICK DEPLOY 📊"
echo "================================="
echo "Project: $PROJECT_ID"
echo "Region: us-central1"
echo ""

# Build and push container
echo "🏗️ Building container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-signals

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully"

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy codex-signals \
  --image gcr.io/$PROJECT_ID/codex-signals \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 5 \
  --timeout 60

if [ $? -ne 0 ]; then
    echo "❌ Deploy failed"
    exit 1
fi

echo "✅ Deployment completed successfully"

# Get service URL
SERVICE_URL=$(gcloud run services describe codex-signals --region us-central1 --format="value(status.url)")

echo ""
echo "🎯 DEPLOYMENT COMPLETE"
echo "====================="
echo "🌐 Service URL: $SERVICE_URL"
echo "📚 API Docs: $SERVICE_URL/signals/docs"
echo "🏥 Health: $SERVICE_URL/signals/health"
echo "📊 Signals: $SERVICE_URL/signals/daily"
echo "📝 Bulletin: $SERVICE_URL/signals/bulletin?format=md"
echo ""
echo "🔥 Codex Signals deployed successfully! 👑"
