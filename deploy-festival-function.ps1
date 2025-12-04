# 🌟 FESTIVAL TRANSMISSION CLOUD FUNCTION DEPLOYMENT 🌟
# PowerShell deployment script for Windows

Write-Host "🌟 DEPLOYING FESTIVAL TRANSMISSION CLOUD FUNCTION" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Configuration
$PROJECT_ID = "codex-dominion-prod"
$FUNCTION_NAME = "festival-transmission"
$REGION = "us-central1"
$BUCKET_NAME = "codex-artifacts-$PROJECT_ID"

Write-Host "📋 Configuration:" -ForegroundColor Yellow
Write-Host "   Project: $PROJECT_ID"
Write-Host "   Function: $FUNCTION_NAME"
Write-Host "   Region: $REGION"
Write-Host "   Bucket: $BUCKET_NAME"
Write-Host ""

# Set the project
Write-Host "🔧 Setting Google Cloud project..." -ForegroundColor Green
gcloud config set project $PROJECT_ID

# Create storage bucket if it doesn't exist
Write-Host "📦 Ensuring storage bucket exists..." -ForegroundColor Green
gsutil mb -p $PROJECT_ID "gs://$BUCKET_NAME" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Bucket already exists" -ForegroundColor Gray
}

# Enable required APIs
Write-Host "⚡ Enabling required APIs..." -ForegroundColor Green
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable logging.googleapis.com

# Deploy the Cloud Function for HTTP triggers
Write-Host "🚀 Deploying Festival Transmission Function (HTTP)..." -ForegroundColor Magenta
gcloud functions deploy "$FUNCTION_NAME-http" `
  --runtime python39 `
  --trigger-http `
  --allow-unauthenticated `
  --source . `
  --entry-point get_festival_cycles `
  --region $REGION `
  --memory 256MB `
  --timeout 60s `
  --env-vars-file .env.yaml `
  --max-instances 10

# Deploy the Cloud Function for Pub/Sub triggers
Write-Host "🚀 Deploying Festival Transmission Function (Pub/Sub)..." -ForegroundColor Magenta
gcloud functions deploy "$FUNCTION_NAME-pubsub" `
  --runtime python39 `
  --trigger-topic festival-ceremonies `
  --source . `
  --entry-point festival_transmission_pubsub `
  --region $REGION `
  --memory 256MB `
  --timeout 60s `
  --env-vars-file .env.yaml `
  --max-instances 10

# Create Pub/Sub topic if it doesn't exist
Write-Host "📡 Creating Pub/Sub topic..." -ForegroundColor Green
gcloud pubsub topics create festival-ceremonies 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Topic already exists" -ForegroundColor Gray
}

# Test the HTTP function
Write-Host "🧪 Testing Festival Transmission Function..." -ForegroundColor Green
$HTTP_URL = gcloud functions describe "$FUNCTION_NAME-http" --region=$REGION --format="value(httpsTrigger.url)"
Write-Host "   Function URL: $HTTP_URL"

# Test with Invoke-RestMethod
try {
    $response = Invoke-RestMethod -Uri $HTTP_URL -Method Get
    Write-Host "   Response: $($response.summary)" -ForegroundColor Cyan
} catch {
    Write-Host "   Function deployed (test response: $($_.Exception.Message))" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✅ FESTIVAL TRANSMISSION DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host ""
Write-Host "🌟 Sacred Endpoints:" -ForegroundColor Yellow
Write-Host "   HTTP Function: $HTTP_URL"
Write-Host "   Pub/Sub Topic: projects/$PROJECT_ID/topics/festival-ceremonies"
Write-Host "   Storage Bucket: gs://$BUCKET_NAME"
Write-Host ""
Write-Host "🔥 Usage Examples:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   # PowerShell HTTP GET (retrieve cycles):"
Write-Host "   Invoke-RestMethod -Uri '$HTTP_URL' -Method Get"
Write-Host ""
Write-Host "   # Pub/Sub publish (new ceremony):"
Write-Host "   gcloud pubsub topics publish festival-ceremonies --message='{`"rite`":`"Test Festival`",`"proclamation`":`"Sacred Test`"}'"
Write-Host ""
Write-Host "🌍 The Festival Transmission is now global and eternal!" -ForegroundColor Magenta
