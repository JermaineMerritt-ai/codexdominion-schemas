# 🔥 Codex Dominion - Google Cloud Platform Setup (PowerShell)
# Configures GCP authentication and deployment for Windows

Write-Host "🔥 === CODEX DOMINION GCP SETUP ===" -ForegroundColor Cyan
Write-Host "🕐 $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Check if gcloud is installed
try {
    gcloud --version | Out-Null
    Write-Host "✅ Google Cloud CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI not installed" -ForegroundColor Red
    Write-Host "📥 Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    Write-Host "   Or download: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -ForegroundColor Yellow
    exit 1
}

# Show current configuration
Write-Host "📊 Current GCP Configuration:" -ForegroundColor Cyan
gcloud config list --format="table(core.project,core.account,compute.region,compute.zone)"

Write-Host ""
Write-Host "🔐 === AUTHENTICATION ===" -ForegroundColor Cyan

# Login to Google Cloud
Write-Host "🔓 Logging into Google Cloud..." -ForegroundColor Yellow
Write-Host "This will open a browser window for authentication..." -ForegroundColor Yellow
Read-Host "Press ENTER to continue"

gcloud auth login

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Authentication successful" -ForegroundColor Green
} else {
    Write-Host "❌ Authentication failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏗️ === PROJECT CONFIGURATION ===" -ForegroundColor Cyan

# Show available projects
Write-Host "📋 Available GCP Projects:" -ForegroundColor Yellow
gcloud projects list --format="table(projectId,name,projectNumber)"

Write-Host ""
Write-Host "Select your project configuration:" -ForegroundColor Cyan
Write-Host "1. Create new project for Codex Dominion"
Write-Host "2. Use existing project"
Write-Host "3. Enter project ID manually"

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "🆕 Creating new Codex Dominion project..." -ForegroundColor Yellow
        $PROJECT_ID = Read-Host "Enter project ID (e.g., codex-dominion-prod)"
        $PROJECT_NAME = Read-Host "Enter project name (e.g., Codex Dominion Production)"
        
        gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Project created: $PROJECT_ID" -ForegroundColor Green
        } else {
            Write-Host "❌ Project creation failed" -ForegroundColor Red
            exit 1
        }
    }
    "2" {
        Write-Host "📋 Select from existing projects:" -ForegroundColor Yellow
        gcloud projects list --format="value(projectId)"
        $PROJECT_ID = Read-Host "Enter project ID"
    }
    "3" {
        $PROJECT_ID = Read-Host "Enter your GCP project ID"
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

# Set the project
Write-Host "⚙️ Setting project to: $PROJECT_ID" -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Project set successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to set project" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🌍 === REGION CONFIGURATION ===" -ForegroundColor Cyan

# Set compute region and zone
Write-Host "Available regions for Cloud Run and Compute Engine:" -ForegroundColor Yellow
Write-Host "  us-central1 (Iowa, USA)"
Write-Host "  us-east1 (South Carolina, USA)"
Write-Host "  europe-west1 (Belgium, Europe)"
Write-Host "  asia-east1 (Taiwan, Asia)"

$REGION = Read-Host "Enter preferred region (default: us-central1)"
if ([string]::IsNullOrWhiteSpace($REGION)) { $REGION = "us-central1" }

$ZONE = Read-Host "Enter preferred zone (default: $REGION-a)"
if ([string]::IsNullOrWhiteSpace($ZONE)) { $ZONE = "$REGION-a" }

gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

Write-Host "✅ Region set to: $REGION" -ForegroundColor Green
Write-Host "✅ Zone set to: $ZONE" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 === ENABLE REQUIRED APIS ===" -ForegroundColor Cyan

# Enable required GCP APIs
Write-Host "🔌 Enabling required APIs..." -ForegroundColor Yellow
$APIS = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "dns.googleapis.com",
    "cloudresourcemanager.googleapis.com"
)

foreach ($api in $APIS) {
    Write-Host "  Enabling $api..." -ForegroundColor Gray
    gcloud services enable $api
}

Write-Host "✅ APIs enabled" -ForegroundColor Green

Write-Host ""
Write-Host "🔐 === SERVICE ACCOUNT SETUP ===" -ForegroundColor Cyan

# Create service account for Codex Dominion
$SERVICE_ACCOUNT_NAME = "codex-dominion-sa"
$SERVICE_ACCOUNT_EMAIL = "$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"

Write-Host "👤 Creating service account: $SERVICE_ACCOUNT_NAME" -ForegroundColor Yellow
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME `
    --display-name="Codex Dominion Service Account" `
    --description="Service account for Codex Dominion deployment and operations"

# Grant necessary roles
Write-Host "🛡️ Granting IAM roles..." -ForegroundColor Yellow
$ROLES = @(
    "roles/run.admin",
    "roles/storage.admin",
    "roles/cloudbuild.builds.editor",
    "roles/artifactregistry.admin"
)

foreach ($role in $ROLES) {
    Write-Host "  Granting $role..." -ForegroundColor Gray
    gcloud projects add-iam-policy-binding $PROJECT_ID `
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" `
        --role="$role"
}

Write-Host "✅ Service account configured" -ForegroundColor Green

Write-Host ""
Write-Host "📦 === ARTIFACT REGISTRY SETUP ===" -ForegroundColor Cyan

# Create Artifact Registry repository
$REPO_NAME = "codex-dominion"
Write-Host "🏪 Creating Artifact Registry repository: $REPO_NAME" -ForegroundColor Yellow

gcloud artifacts repositories create $REPO_NAME `
    --repository-format=docker `
    --location=$REGION `
    --description="Codex Dominion container images"

Write-Host "✅ Artifact Registry repository created" -ForegroundColor Green

# Configure Docker authentication
Write-Host "🐳 Configuring Docker authentication..." -ForegroundColor Yellow
gcloud auth configure-docker "$REGION-docker.pkg.dev"

Write-Host ""
Write-Host "💾 === CONFIGURATION SUMMARY ===" -ForegroundColor Cyan

# Save configuration to file
$configContent = @"
# Codex Dominion GCP Configuration
# Generated on $(Get-Date)

`$env:GCP_PROJECT_ID = "$PROJECT_ID"
`$env:GCP_REGION = "$REGION"
`$env:GCP_ZONE = "$ZONE"
`$env:SERVICE_ACCOUNT_EMAIL = "$SERVICE_ACCOUNT_EMAIL"
`$env:ARTIFACT_REGISTRY_REPO = "$REPO_NAME"
`$env:DOCKER_REGISTRY = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME"

# Cloud Run service names
`$env:CODEX_PRODUCTION_SERVICE = "codex-production"
`$env:CODEX_STAGING_SERVICE = "codex-staging"

# Load this configuration with: . .\gcp-config.ps1
"@

$configContent | Out-File -FilePath "gcp-config.ps1" -Encoding UTF8

Write-Host "📄 Configuration saved to: gcp-config.ps1" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Final Configuration:" -ForegroundColor Cyan
Write-Host "  Project ID: $PROJECT_ID" -ForegroundColor White
Write-Host "  Region: $REGION" -ForegroundColor White
Write-Host "  Zone: $ZONE" -ForegroundColor White
Write-Host "  Service Account: $SERVICE_ACCOUNT_EMAIL" -ForegroundColor White
Write-Host "  Docker Registry: $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME" -ForegroundColor White

Write-Host ""
Write-Host "🏁 === GCP SETUP COMPLETE ===" -ForegroundColor Green
Write-Host "✅ Authentication configured" -ForegroundColor Green
Write-Host "✅ Project and region set" -ForegroundColor Green
Write-Host "✅ Required APIs enabled" -ForegroundColor Green
Write-Host "✅ Service account created" -ForegroundColor Green
Write-Host "✅ Artifact Registry ready" -ForegroundColor Green
Write-Host "✅ Docker authentication configured" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host "1. Load config: . .\gcp-config.ps1" -ForegroundColor White
Write-Host "2. Build and deploy: .\deploy-gcp.ps1" -ForegroundColor White
Write-Host "3. Access via Cloud Run URLs" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Ready to deploy Codex Dominion to Google Cloud! ✨" -ForegroundColor Magenta