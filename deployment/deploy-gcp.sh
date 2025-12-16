#!/bin/bash
# =============================================================================
# DOT300 - Google Cloud Run Deployment
# =============================================================================

set -e

echo "🔥 DOT300 GCP Deployment Starting..."
echo ""

# Configuration
PROJECT_ID="dot300-production"
SERVICE_NAME="dot300-api"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/dot300-api:latest"
PORT=8300

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "  Project: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Service: $SERVICE_NAME"
echo ""

# Step 1: Set GCP Project
echo -e "${YELLOW}1. Setting GCP Project...${NC}"
gcloud config set project $PROJECT_ID

# Step 2: Enable Required APIs
echo -e "${YELLOW}2. Enabling Required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 3: Build Container Image
echo -e "${YELLOW}3. Building Container Image...${NC}"
cd ..
gcloud builds submit --tag $IMAGE_NAME \
    --dockerfile docker/Dockerfile.dot300 \
    --timeout 10m

# Step 4: Upload agents.json to Cloud Storage
echo -e "${YELLOW}4. Creating Cloud Storage Bucket...${NC}"
BUCKET_NAME="dot300-agents-data"
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME/ || echo "Bucket already exists"

echo -e "${YELLOW}5. Uploading agents.json...${NC}"
gsutil cp dot300_agents.json gs://$BUCKET_NAME/dot300_agents.json

# Make bucket publicly readable (or use signed URLs in production)
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME

# Step 5: Deploy to Cloud Run
echo -e "${YELLOW}6. Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --port $PORT \
    --max-instances 10 \
    --min-instances 1 \
    --set-env-vars PYTHONUNBUFFERED=1,AGENTS_URL=https://storage.googleapis.com/$BUCKET_NAME/dot300_agents.json \
    --timeout 300 \
    --concurrency 80

# Step 6: Get Service URL
echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo -e "${GREEN}🌍 DOT300 API URL: $SERVICE_URL${NC}"
echo ""

# Step 7: Test Deployment
echo -e "${YELLOW}7. Testing API...${NC}"
curl -s $SERVICE_URL/health | jq .
echo ""
curl -s $SERVICE_URL/api/stats | jq .
echo ""

# Step 8: Setup Cloud Load Balancer (Optional)
echo -e "${YELLOW}8. Cloud Load Balancer Setup (Manual):${NC}"
echo "For global load balancing, run:"
echo "  gcloud compute backend-services create dot300-backend --global"
echo "  gcloud compute url-maps create dot300-lb --default-service=dot300-backend"
echo ""

# Step 9: Setup Cloud CDN
echo -e "${YELLOW}9. Enabling Cloud CDN (Manual):${NC}"
echo "  gcloud compute backend-services update dot300-backend --enable-cdn --global"
echo ""

# Step 10: Setup Custom Domain
echo -e "${YELLOW}10. Custom Domain Setup:${NC}"
echo "  gcloud run domain-mappings create --service=$SERVICE_NAME --domain=api.dot300.ai --region=$REGION"
echo ""

echo -e "${GREEN}🔥 DOT300 is LIVE on GCP!${NC}"
echo "  Health: $SERVICE_URL/health"
echo "  Stats: $SERVICE_URL/api/stats"
echo "  Agents: $SERVICE_URL/api/agents"
echo ""
echo "Performance:"
echo "  - Auto-scaling: 1-10 instances"
echo "  - CPU: 2 cores"
echo "  - Memory: 2GB"
echo "  - Timeout: 300s"
echo "  - Concurrency: 80 requests/instance"
echo ""
echo "Next steps:"
echo "  1. Setup custom domain: api.dot300.ai"
echo "  2. Enable Cloud CDN for faster response"
echo "  3. Configure Cloud Monitoring"
echo "  4. Setup Cloud Armor for DDoS protection"
echo ""
