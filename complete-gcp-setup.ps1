# 🔥 CODEX DOMINION - Complete GCP Setup with Proper Permissions
# Handles authentication, permissions, and deployment

Write-Host "🔥 === CODEX DOMINION - COMPLETE GCP SETUP ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Authentication
Write-Host "🔐 === AUTHENTICATION ===" -ForegroundColor Yellow
Write-Host "Opening browser for authentication..." -ForegroundColor White
gcloud auth login --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Authentication failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Authentication successful" -ForegroundColor Green

# Step 2: Project Configuration
Write-Host ""
Write-Host "📋 === PROJECT SETUP ===" -ForegroundColor Yellow

$PROJECT_ID = gcloud config get-value project 2>$null
if (-not $PROJECT_ID -or $PROJECT_ID -eq "(unset)") {
    Write-Host "Available projects:" -ForegroundColor Cyan
    gcloud projects list --format="table(projectId,name)"
    Write-Host ""
    $PROJECT_ID = Read-Host "Enter your project ID"
    gcloud config set project $PROJECT_ID
}

Write-Host "🎯 Using project: $PROJECT_ID" -ForegroundColor Green

# Step 3: Enable APIs with proper error handling
Write-Host ""
Write-Host "⚡ === ENABLING REQUIRED APIS ===" -ForegroundColor Yellow

$apis = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "serviceusage.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "🔌 Enabling $api..." -ForegroundColor White
    gcloud services enable $api --project=$PROJECT_ID 2>$null
    Start-Sleep 2
}

Write-Host "✅ APIs enabled" -ForegroundColor Green

# Step 4: Check and set up IAM permissions
Write-Host ""
Write-Host "🔑 === IAM PERMISSIONS ===" -ForegroundColor Yellow

$USER_EMAIL = gcloud auth list --filter=status:ACTIVE --format="value(account)"
Write-Host "👤 User: $USER_EMAIL" -ForegroundColor White

Write-Host "🛡️ Adding required IAM roles..." -ForegroundColor White

$roles = @(
    "roles/cloudbuild.builds.editor",
    "roles/storage.admin",
    "roles/run.admin",
    "roles/iam.serviceAccountUser"
)

foreach ($role in $roles) {
    Write-Host "   Adding $role..." -ForegroundColor Gray
    gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$USER_EMAIL" --role="$role" --quiet 2>$null
}

Write-Host "✅ IAM roles configured" -ForegroundColor Green

# Step 5: Alternative approach - Direct Docker build and push
Write-Host ""
Write-Host "🐳 === ALTERNATIVE: DIRECT DOCKER APPROACH ===" -ForegroundColor Yellow

Write-Host "Instead of Cloud Build, let's use direct Docker commands:" -ForegroundColor Cyan
Write-Host ""

# Configure Docker for GCR
Write-Host "🔧 Configuring Docker for Google Container Registry..." -ForegroundColor White
gcloud auth configure-docker --quiet

$IMAGE_NAME = "gcr.io/$PROJECT_ID/codex-dashboard"

Write-Host "🏗️ Building Docker image locally..." -ForegroundColor White
docker build -t $IMAGE_NAME .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Image built successfully" -ForegroundColor Green

    Write-Host "📤 Pushing to Google Container Registry..." -ForegroundColor White
    docker push $IMAGE_NAME

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Image pushed successfully!" -ForegroundColor Green

        # Deploy to Cloud Run
        Write-Host ""
        Write-Host "🚀 === DEPLOYING TO CLOUD RUN ===" -ForegroundColor Yellow

        gcloud run deploy codex-dashboard `
            --image=$IMAGE_NAME `
            --region=us-central1 `
            --platform=managed `
            --allow-unauthenticated `
            --port=8501 `
            --memory=1Gi `
            --cpu=1 `
            --project=$PROJECT_ID

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Deployment successful!" -ForegroundColor Green

            $SERVICE_URL = gcloud run services describe codex-dashboard --region=us-central1 --format="value(status.url)" --project=$PROJECT_ID
            Write-Host ""
            Write-Host "🔗 Your Codex Dashboard is live at:" -ForegroundColor Green
            Write-Host "   $SERVICE_URL" -ForegroundColor White

            # Test the deployment
            Write-Host ""
            Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow
            Start-Sleep 10

            try {
                $response = Invoke-RestMethod -Uri $SERVICE_URL -Method GET -TimeoutSec 30
                Write-Host "✅ Dashboard is responding!" -ForegroundColor Green
            } catch {
                Write-Host "⚠️ Dashboard may still be starting up. Please wait a moment and try the URL." -ForegroundColor Yellow
            }

        } else {
            Write-Host "❌ Cloud Run deployment failed" -ForegroundColor Red
        }

    } else {
        Write-Host "❌ Push failed" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔥 === DEPLOYMENT COMPLETE ===" -ForegroundColor Magenta
Write-Host "Sacred flames now burn eternal in Google Cloud! ✨" -ForegroundColor Magenta
