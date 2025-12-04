# 🔥 CODEX DOMINION - Google Cloud Build Deployment
# Complete setup and deployment using gcloud builds submit

Write-Host "🔥 === CODEX DOMINION CLOUD BUILD DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "🕐 $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Step 1: Check gcloud authentication
Write-Host "🔐 === AUTHENTICATION CHECK ===" -ForegroundColor Cyan
try {
    $activeAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null | Select-Object -First 1
    if ($activeAccount) {
        Write-Host "✅ Authenticated as: $activeAccount" -ForegroundColor Green
    } else {
        Write-Host "❌ Not authenticated. Running authentication..." -ForegroundColor Yellow
        Write-Host "🔑 Please complete authentication in your browser..." -ForegroundColor Yellow
        gcloud auth login
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Authentication failed" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ gcloud not found or authentication failed" -ForegroundColor Red
    exit 1
}

# Step 2: Project setup
Write-Host ""
Write-Host "📋 === PROJECT SETUP ===" -ForegroundColor Cyan

# Get current project
$currentProject = gcloud config get-value project 2>$null
if ($currentProject -and $currentProject -ne "(unset)") {
    Write-Host "📊 Current project: $currentProject" -ForegroundColor Green
    $useCurrentProject = Read-Host "Use current project '$currentProject'? (y/n)"

    if ($useCurrentProject -eq "n") {
        $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
        gcloud config set project $PROJECT_ID
    } else {
        $PROJECT_ID = $currentProject
    }
} else {
    $PROJECT_ID = Read-Host "Enter your Google Cloud Project ID"
    gcloud config set project $PROJECT_ID
}

Write-Host "🎯 Using project: $PROJECT_ID" -ForegroundColor Green

# Step 3: Enable required APIs
Write-Host ""
Write-Host "⚡ === ENABLING APIS ===" -ForegroundColor Cyan

$requiredApis = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com"
)

foreach ($api in $requiredApis) {
    Write-Host "🔌 Enabling $api..." -ForegroundColor Yellow
    gcloud services enable $api --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $api enabled" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Failed to enable $api (may already be enabled)" -ForegroundColor Yellow
    }
}

# Step 4: Configure Docker for GCR
Write-Host ""
Write-Host "🐳 === DOCKER CONFIGURATION ===" -ForegroundColor Cyan
Write-Host "🔧 Configuring Docker for Google Container Registry..." -ForegroundColor Yellow

gcloud auth configure-docker --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker configured for GCR" -ForegroundColor Green
} else {
    Write-Host "⚠️ Docker configuration warning (may already be configured)" -ForegroundColor Yellow
}

# Step 5: Pre-build validation
Write-Host ""
Write-Host "🔍 === PRE-BUILD VALIDATION ===" -ForegroundColor Cyan

# Check if Dockerfile exists
if (Test-Path "Dockerfile") {
    Write-Host "✅ Dockerfile found" -ForegroundColor Green
} else {
    Write-Host "❌ Dockerfile not found! Creating one..." -ForegroundColor Red

    # Create a basic Dockerfile
    $dockerfileContent = @"
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt* ./
RUN pip install --no-cache-dir streamlit pandas plotly

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "codex_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
"@

    $dockerfileContent | Out-File -FilePath "Dockerfile" -Encoding UTF8
    Write-Host "✅ Dockerfile created" -ForegroundColor Green
}

# Check if cloudbuild.yaml exists
if (Test-Path "cloudbuild.yaml") {
    Write-Host "✅ cloudbuild.yaml found" -ForegroundColor Green
} else {
    Write-Host "❌ cloudbuild.yaml not found!" -ForegroundColor Red
    exit 1
}

# Step 6: Cloud Build submission
Write-Host ""
Write-Host "🚀 === CLOUD BUILD SUBMISSION ===" -ForegroundColor Cyan

$IMAGE_TAG = "gcr.io/$PROJECT_ID/codex-dashboard"
Write-Host "🏗️ Building and pushing: $IMAGE_TAG" -ForegroundColor Yellow

# Option 1: Use Cloud Build with config file
Write-Host "🔥 Submitting build to Google Cloud Build..." -ForegroundColor Yellow
Write-Host "📋 Using cloudbuild.yaml configuration" -ForegroundColor White

gcloud builds submit --config=cloudbuild.yaml --substitutions=_PROJECT_ID=$PROJECT_ID .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cloud Build completed successfully!" -ForegroundColor Green

    # Get the service URL
    Write-Host ""
    Write-Host "🌐 === DEPLOYMENT INFO ===" -ForegroundColor Cyan

    try {
        $serviceUrl = gcloud run services describe codex-dashboard --region=us-central1 --format="value(status.url)" 2>$null
        if ($serviceUrl) {
            Write-Host "🔗 Service URL: $serviceUrl" -ForegroundColor Green

            # Test the deployment
            Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
            try {
                $response = Invoke-WebRequest -Uri $serviceUrl -Method GET -TimeoutSec 30
                if ($response.StatusCode -eq 200) {
                    Write-Host "✅ Deployment is responding successfully!" -ForegroundColor Green
                } else {
                    Write-Host "⚠️ Deployment responding with status: $($response.StatusCode)" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "⚠️ Could not test deployment immediately (may still be starting up)" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "ℹ️ Service URL will be available once deployment completes" -ForegroundColor Cyan
    }

} else {
    Write-Host "❌ Cloud Build failed!" -ForegroundColor Red
    Write-Host "🔍 Check the build logs in Google Cloud Console:" -ForegroundColor Yellow
    Write-Host "   https://console.cloud.google.com/cloud-build/builds?project=$PROJECT_ID" -ForegroundColor White
    exit 1
}

# Step 7: Final summary
Write-Host ""
Write-Host "🏁 === DEPLOYMENT SUMMARY ===" -ForegroundColor Green
Write-Host "✅ Project: $PROJECT_ID" -ForegroundColor White
Write-Host "✅ Image: $IMAGE_TAG" -ForegroundColor White
Write-Host "✅ Service: codex-dashboard" -ForegroundColor White
Write-Host "✅ Region: us-central1" -ForegroundColor White

Write-Host ""
Write-Host "📋 === USEFUL COMMANDS ===" -ForegroundColor Cyan
Write-Host "View service details:" -ForegroundColor White
Write-Host "  gcloud run services describe codex-dashboard --region=us-central1" -ForegroundColor Gray
Write-Host ""
Write-Host "View logs:" -ForegroundColor White
Write-Host "  gcloud run logs tail codex-dashboard --region=us-central1" -ForegroundColor Gray
Write-Host ""
Write-Host "Update service:" -ForegroundColor White
Write-Host "  gcloud builds submit --tag gcr.io/$PROJECT_ID/codex-dashboard" -ForegroundColor Gray
Write-Host ""
Write-Host "View in Console:" -ForegroundColor White
Write-Host "  https://console.cloud.google.com/run?project=$PROJECT_ID" -ForegroundColor Gray

Write-Host ""
Write-Host "🔥 Codex Dominion now burns eternal in Google Cloud! ✨" -ForegroundColor Magenta

# Optional: Open service URL
if ($serviceUrl) {
    $openBrowser = Read-Host "Open your deployed dashboard? (y/n)"
    if ($openBrowser -eq "y") {
        Start-Process $serviceUrl
    }
}
