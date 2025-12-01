#!/bin/bash
# 🌟 FESTIVAL TRANSMISSION CLOUD FUNCTION DEPLOYMENT 🌟

echo "🌟 DEPLOYING FESTIVAL TRANSMISSION CLOUD FUNCTION"
echo "================================================="

# Configuration
PROJECT_ID="codex-dominion-prod"
FUNCTION_NAME="festival-transmission"
REGION="us-central1"
BUCKET_NAME="codex-artifacts-${PROJECT_ID}"

echo "📋 Configuration:"
echo "   Project: $PROJECT_ID"
echo "   Function: $FUNCTION_NAME"
echo "   Region: $REGION"
echo "   Bucket: $BUCKET_NAME"
echo ""

# Set the project
echo "🔧 Setting Google Cloud project..."
gcloud config set project $PROJECT_ID

# Create storage bucket if it doesn't exist
echo "📦 Ensuring storage bucket exists..."
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME 2>/dev/null || echo "   Bucket already exists"

# Enable required APIs
echo "⚡ Enabling required APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable logging.googleapis.com

# Deploy the Cloud Function for HTTP triggers
echo "🚀 Deploying Festival Transmission Function (HTTP)..."
gcloud functions deploy ${FUNCTION_NAME}-http \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --source . \
  --entry-point get_festival_cycles \
  --region $REGION \
  --memory 256MB \
  --timeout 60s \
  --env-vars-file .env.yaml \
  --max-instances 10

# Deploy the Cloud Function for Pub/Sub triggers
echo "🚀 Deploying Festival Transmission Function (Pub/Sub)..."
gcloud functions deploy ${FUNCTION_NAME}-pubsub \
  --runtime python39 \
  --trigger-topic festival-ceremonies \
  --source . \
  --entry-point festival_transmission_pubsub \
  --region $REGION \
  --memory 256MB \
  --timeout 60s \
  --env-vars-file .env.yaml \
  --max-instances 10

# Create Pub/Sub topic if it doesn't exist
echo "📡 Creating Pub/Sub topic..."
gcloud pubsub topics create festival-ceremonies 2>/dev/null || echo "   Topic already exists"

# Test the HTTP function
echo "🧪 Testing Festival Transmission Function..."
HTTP_URL=$(gcloud functions describe ${FUNCTION_NAME}-http --region=$REGION --format="value(httpsTrigger.url)")
echo "   Function URL: $HTTP_URL"

# Test with curl
curl -s "$HTTP_URL" | jq .summary 2>/dev/null || echo "   Function deployed (jq not available for pretty printing)"

echo ""
echo "✅ FESTIVAL TRANSMISSION DEPLOYMENT COMPLETE"
echo ""
echo "🌟 Sacred Endpoints:"
echo "   HTTP Function: $HTTP_URL"
echo "   Pub/Sub Topic: projects/$PROJECT_ID/topics/festival-ceremonies"
echo "   Storage Bucket: gs://$BUCKET_NAME"
echo ""
echo "🔥 Usage Examples:"
echo ""
echo "   # HTTP GET (retrieve cycles):"
echo "   curl '$HTTP_URL'"
echo ""
echo "   # Pub/Sub publish (new ceremony):"
echo "   gcloud pubsub topics publish festival-ceremonies --message='{\"rite\":\"Test Festival\",\"proclamation\":\"Sacred Test\"}'"
echo ""
echo "🌍 The Festival Transmission is now global and eternal!"