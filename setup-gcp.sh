#!/bin/bash
# 🔥 Codex Dominion - Google Cloud Platform Setup Script
# Configures GCP authentication and deployment for Codex Dashboard

echo "🔥 === CODEX DOMINION GCP SETUP ==="
echo "🕐 $(date)"
echo

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not installed"
    echo "📥 Install from: https://cloud.google.com/sdk/docs/install"
    echo "   Or run: curl https://sdk.cloud.google.com | bash"
    exit 1
fi

echo "✅ Google Cloud CLI found"

# Show current configuration
echo "📊 Current GCP Configuration:"
gcloud config list --format="table(core.project,core.account,compute.region,compute.zone)"

echo
echo "🔐 === AUTHENTICATION ==="

# Login to Google Cloud
echo "🔓 Logging into Google Cloud..."
echo "This will open a browser window for authentication..."
read -p "Press ENTER to continue..."

gcloud auth login

if [ $? -eq 0 ]; then
    echo "✅ Authentication successful"
else
    echo "❌ Authentication failed"
    exit 1
fi

echo
echo "🏗️ === PROJECT CONFIGURATION ==="

# Show available projects
echo "📋 Available GCP Projects:"
gcloud projects list --format="table(projectId,name,projectNumber)"

echo
echo "Select your project configuration:"
echo "1. Create new project for Codex Dominion"
echo "2. Use existing project"
echo "3. Enter project ID manually"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🆕 Creating new Codex Dominion project..."
        read -p "Enter project ID (e.g., codex-dominion-prod): " PROJECT_ID
        read -p "Enter project name (e.g., Codex Dominion Production): " PROJECT_NAME
        
        gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
        if [ $? -eq 0 ]; then
            echo "✅ Project created: $PROJECT_ID"
        else
            echo "❌ Project creation failed"
            exit 1
        fi
        ;;
    2)
        echo "📋 Select from existing projects:"
        gcloud projects list --format="value(projectId)"
        read -p "Enter project ID: " PROJECT_ID
        ;;
    3)
        read -p "Enter your GCP project ID: " PROJECT_ID
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Set the project
echo "⚙️ Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

if [ $? -eq 0 ]; then
    echo "✅ Project set successfully"
else
    echo "❌ Failed to set project"
    exit 1
fi

echo
echo "🌍 === REGION CONFIGURATION ==="

# Set compute region and zone
echo "Available regions for Cloud Run and Compute Engine:"
echo "  us-central1 (Iowa, USA)"
echo "  us-east1 (South Carolina, USA)"  
echo "  europe-west1 (Belgium, Europe)"
echo "  asia-east1 (Taiwan, Asia)"

read -p "Enter preferred region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

read -p "Enter preferred zone (default: ${REGION}-a): " ZONE
ZONE=${ZONE:-${REGION}-a}

gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

echo "✅ Region set to: $REGION"
echo "✅ Zone set to: $ZONE"

echo
echo "🔧 === ENABLE REQUIRED APIS ==="

# Enable required GCP APIs
echo "🔌 Enabling required APIs..."
APIS=(
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "containerregistry.googleapis.com"
    "artifactregistry.googleapis.com"
    "compute.googleapis.com"
    "dns.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "  Enabling $api..."
    gcloud services enable $api
done

echo "✅ APIs enabled"

echo
echo "🔐 === SERVICE ACCOUNT SETUP ==="

# Create service account for Codex Dominion
SERVICE_ACCOUNT_NAME="codex-dominion-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "👤 Creating service account: $SERVICE_ACCOUNT_NAME"
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="Codex Dominion Service Account" \
    --description="Service account for Codex Dominion deployment and operations"

# Grant necessary roles
echo "🛡️ Granting IAM roles..."
ROLES=(
    "roles/run.admin"
    "roles/storage.admin"
    "roles/cloudbuild.builds.editor"
    "roles/artifactregistry.admin"
)

for role in "${ROLES[@]}"; do
    echo "  Granting $role..."
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role"
done

echo "✅ Service account configured"

echo
echo "📦 === ARTIFACT REGISTRY SETUP ==="

# Create Artifact Registry repository
REPO_NAME="codex-dominion"
echo "🏪 Creating Artifact Registry repository: $REPO_NAME"

gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Codex Dominion container images"

echo "✅ Artifact Registry repository created"

# Configure Docker authentication
echo "🐳 Configuring Docker authentication..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev

echo
echo "💾 === CONFIGURATION SUMMARY ==="

# Save configuration to file
cat > gcp-config.env << EOF
# Codex Dominion GCP Configuration
# Generated on $(date)

export GCP_PROJECT_ID="$PROJECT_ID"
export GCP_REGION="$REGION"
export GCP_ZONE="$ZONE"
export SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_EMAIL"
export ARTIFACT_REGISTRY_REPO="$REPO_NAME"
export DOCKER_REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}"

# Cloud Run service names
export CODEX_PRODUCTION_SERVICE="codex-production"
export CODEX_STAGING_SERVICE="codex-staging"

# Load this configuration with: source gcp-config.env
EOF

echo "📄 Configuration saved to: gcp-config.env"
echo
echo "📊 Final Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Zone: $ZONE"
echo "  Service Account: $SERVICE_ACCOUNT_EMAIL"
echo "  Docker Registry: ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}"

echo
echo "🏁 === GCP SETUP COMPLETE ==="
echo "✅ Authentication configured"
echo "✅ Project and region set"
echo "✅ Required APIs enabled"
echo "✅ Service account created"
echo "✅ Artifact Registry ready"
echo "✅ Docker authentication configured"
echo
echo "🚀 Next steps:"
echo "1. Load config: source gcp-config.env"
echo "2. Build and deploy: ./deploy-gcp.sh"
echo "3. Access via Cloud Run URLs"
echo
echo "🔥 Ready to deploy Codex Dominion to Google Cloud! ✨"