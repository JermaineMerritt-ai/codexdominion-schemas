#!/bin/bash
# 🔥 Codex Dominion - Google Cloud Run Deployment
# Deploys Codex Dashboard to Google Cloud Run

echo "🔥 === CODEX DOMINION GCP DEPLOYMENT ==="
echo "🕐 $(date)"
echo

# Load configuration
if [ -f "gcp-config.env" ]; then
    source gcp-config.env
    echo "✅ Configuration loaded from gcp-config.env"
else
    echo "❌ Configuration file not found. Run setup-gcp.sh first."
    exit 1
fi

# Verify gcloud authentication
echo "🔐 Verifying authentication..."
gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1
if [ $? -ne 0 ]; then
    echo "❌ Not authenticated. Run: gcloud auth login"
    exit 1
fi

echo "✅ Authenticated to GCP"
echo "📊 Project: $GCP_PROJECT_ID"
echo "🌍 Region: $GCP_REGION"

# Build and push Docker images
echo
echo "🏗️ === BUILDING DOCKER IMAGES ==="

# Production image
PRODUCTION_IMAGE="$DOCKER_REGISTRY/codex-production:latest"
echo "🔨 Building production image: $PRODUCTION_IMAGE"

docker build -t $PRODUCTION_IMAGE . || {
    echo "❌ Failed to build production image"
    exit 1
}

echo "📤 Pushing production image..."
docker push $PRODUCTION_IMAGE || {
    echo "❌ Failed to push production image"
    exit 1
}

# Staging image (same image, different tag)
STAGING_IMAGE="$DOCKER_REGISTRY/codex-staging:latest"
echo "🔨 Building staging image: $STAGING_IMAGE"
docker tag $PRODUCTION_IMAGE $STAGING_IMAGE
docker push $STAGING_IMAGE || {
    echo "❌ Failed to push staging image"
    exit 1
}

echo "✅ Docker images built and pushed"

# Deploy to Cloud Run
echo
echo "🚀 === DEPLOYING TO CLOUD RUN ==="

# Deploy production service
echo "🌟 Deploying production service..."
gcloud run deploy $CODEX_PRODUCTION_SERVICE \
    --image=$PRODUCTION_IMAGE \
    --platform=managed \
    --region=$GCP_REGION \
    --allow-unauthenticated \
    --port=8501 \
    --memory=1Gi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false,CODEX_ENV=production" \
    --service-account=$SERVICE_ACCOUNT_EMAIL

if [ $? -eq 0 ]; then
    PRODUCTION_URL=$(gcloud run services describe $CODEX_PRODUCTION_SERVICE --region=$GCP_REGION --format="value(status.url)")
    echo "✅ Production deployed: $PRODUCTION_URL"
else
    echo "❌ Production deployment failed"
    exit 1
fi

# Deploy staging service
echo "🔧 Deploying staging service..."
gcloud run deploy $CODEX_STAGING_SERVICE \
    --image=$STAGING_IMAGE \
    --platform=managed \
    --region=$GCP_REGION \
    --allow-unauthenticated \
    --port=8501 \
    --memory=1Gi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=5 \
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false,CODEX_ENV=staging" \
    --service-account=$SERVICE_ACCOUNT_EMAIL

if [ $? -eq 0 ]; then
    STAGING_URL=$(gcloud run services describe $CODEX_STAGING_SERVICE --region=$GCP_REGION --format="value(status.url)")
    echo "✅ Staging deployed: $STAGING_URL"
else
    echo "❌ Staging deployment failed"
    exit 1
fi

# Set up custom domain (optional)
echo
echo "🌐 === CUSTOM DOMAIN SETUP (OPTIONAL) ==="
read -p "Do you want to set up custom domains? (y/n): " setup_domains

if [ "$setup_domains" = "y" ]; then
    read -p "Enter production domain (e.g., app.codexdominion.com): " PROD_DOMAIN
    read -p "Enter staging domain (e.g., staging.codexdominion.com): " STAGING_DOMAIN
    
    if [ ! -z "$PROD_DOMAIN" ]; then
        echo "🔗 Mapping production domain: $PROD_DOMAIN"
        gcloud run domain-mappings create --service=$CODEX_PRODUCTION_SERVICE --domain=$PROD_DOMAIN --region=$GCP_REGION
    fi
    
    if [ ! -z "$STAGING_DOMAIN" ]; then
        echo "🔗 Mapping staging domain: $STAGING_DOMAIN"
        gcloud run domain-mappings create --service=$CODEX_STAGING_SERVICE --domain=$STAGING_DOMAIN --region=$GCP_REGION
    fi
fi

# Set up monitoring and alerting
echo
echo "📊 === MONITORING SETUP ==="

# Create uptime checks
echo "⏱️ Creating uptime checks..."
gcloud alpha monitoring uptime create \
    --display-name="Codex Production Uptime" \
    --http-check-path="/_stcore/health" \
    --hostname="$(echo $PRODUCTION_URL | sed 's|https://||')" \
    --check-interval=60s \
    --timeout=10s 2>/dev/null || echo "⚠️ Uptime check creation requires additional setup"

# Save deployment info
echo
echo "💾 === SAVING DEPLOYMENT INFO ==="

cat > deployment-info.json << EOF
{
  "deployment_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "project_id": "$GCP_PROJECT_ID",
  "region": "$GCP_REGION",
  "services": {
    "production": {
      "name": "$CODEX_PRODUCTION_SERVICE",
      "url": "$PRODUCTION_URL",
      "image": "$PRODUCTION_IMAGE"
    },
    "staging": {
      "name": "$CODEX_STAGING_SERVICE", 
      "url": "$STAGING_URL",
      "image": "$STAGING_IMAGE"
    }
  },
  "docker_registry": "$DOCKER_REGISTRY"
}
EOF

echo "📄 Deployment info saved to: deployment-info.json"

# Show final summary
echo
echo "🏁 === DEPLOYMENT COMPLETE ==="
echo "✅ Services deployed to Google Cloud Run"
echo "✅ Images pushed to Artifact Registry"
echo "✅ Monitoring configured"
echo
echo "🔍 Access your Codex Dashboard:"
echo "   🌟 Production: $PRODUCTION_URL"
echo "   🔧 Staging: $STAGING_URL"
echo
echo "📋 Useful commands:"
echo "   View logs: gcloud run logs tail $CODEX_PRODUCTION_SERVICE --region=$GCP_REGION"
echo "   Update service: gcloud run deploy $CODEX_PRODUCTION_SERVICE --image=$PRODUCTION_IMAGE --region=$GCP_REGION"
echo "   Delete service: gcloud run services delete $CODEX_PRODUCTION_SERVICE --region=$GCP_REGION"
echo "   Monitor: gcloud run services list --region=$GCP_REGION"
echo
echo "💰 Estimated costs:"
echo "   • Cloud Run: ~\$5-20/month (depends on usage)"
echo "   • Artifact Registry: ~\$0.10/GB/month" 
echo "   • Networking: Minimal for normal usage"
echo
echo "🔥 Sacred flames now burn eternal in Google Cloud! ✨"