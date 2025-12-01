# 🔥 Codex Dominion - Google Cloud Run Deployment (PowerShell)
# Deploys Codex Dashboard to Google Cloud Run on Windows

Write-Host "🔥 === CODEX DOMINION GCP DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "🕐 $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Load configuration
if (Test-Path "gcp-config.ps1") {
    . .\gcp-config.ps1
    Write-Host "✅ Configuration loaded from gcp-config.ps1" -ForegroundColor Green
} else {
    Write-Host "❌ Configuration file not found. Run setup-gcp.ps1 first." -ForegroundColor Red
    exit 1
}

# Verify gcloud authentication
Write-Host "🔐 Verifying authentication..." -ForegroundColor Yellow
try {
    $activeAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null | Select-Object -First 1
    if ($activeAccount) {
        Write-Host "✅ Authenticated as: $activeAccount" -ForegroundColor Green
    } else {
        throw "No active authentication"
    }
} catch {
    Write-Host "❌ Not authenticated. Run: gcloud auth login" -ForegroundColor Red
    exit 1
}

Write-Host "📊 Project: $env:GCP_PROJECT_ID" -ForegroundColor White
Write-Host "🌍 Region: $env:GCP_REGION" -ForegroundColor White

# Build and push Docker images
Write-Host ""
Write-Host "🏗️ === BUILDING DOCKER IMAGES ===" -ForegroundColor Cyan

# Production image
$PRODUCTION_IMAGE = "$env:DOCKER_REGISTRY/codex-production:latest"
Write-Host "🔨 Building production image: $PRODUCTION_IMAGE" -ForegroundColor Yellow

docker build -t $PRODUCTION_IMAGE .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build production image" -ForegroundColor Red
    exit 1
}

Write-Host "📤 Pushing production image..." -ForegroundColor Yellow
docker push $PRODUCTION_IMAGE
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push production image" -ForegroundColor Red
    exit 1
}

# Staging image (same image, different tag)
$STAGING_IMAGE = "$env:DOCKER_REGISTRY/codex-staging:latest"
Write-Host "🔨 Building staging image: $STAGING_IMAGE" -ForegroundColor Yellow
docker tag $PRODUCTION_IMAGE $STAGING_IMAGE
docker push $STAGING_IMAGE
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push staging image" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker images built and pushed" -ForegroundColor Green

# Deploy to Cloud Run
Write-Host ""
Write-Host "🚀 === DEPLOYING TO CLOUD RUN ===" -ForegroundColor Cyan

# Deploy production service
Write-Host "🌟 Deploying production service..." -ForegroundColor Yellow
gcloud run deploy $env:CODEX_PRODUCTION_SERVICE `
    --image=$PRODUCTION_IMAGE `
    --platform=managed `
    --region=$env:GCP_REGION `
    --allow-unauthenticated `
    --port=8501 `
    --memory=1Gi `
    --cpu=1 `
    --min-instances=0 `
    --max-instances=10 `
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false,CODEX_ENV=production" `
    --service-account=$env:SERVICE_ACCOUNT_EMAIL

if ($LASTEXITCODE -eq 0) {
    $PRODUCTION_URL = gcloud run services describe $env:CODEX_PRODUCTION_SERVICE --region=$env:GCP_REGION --format="value(status.url)"
    Write-Host "✅ Production deployed: $PRODUCTION_URL" -ForegroundColor Green
} else {
    Write-Host "❌ Production deployment failed" -ForegroundColor Red
    exit 1
}

# Deploy staging service
Write-Host "🔧 Deploying staging service..." -ForegroundColor Yellow
gcloud run deploy $env:CODEX_STAGING_SERVICE `
    --image=$STAGING_IMAGE `
    --platform=managed `
    --region=$env:GCP_REGION `
    --allow-unauthenticated `
    --port=8501 `
    --memory=1Gi `
    --cpu=1 `
    --min-instances=0 `
    --max-instances=5 `
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false,CODEX_ENV=staging" `
    --service-account=$env:SERVICE_ACCOUNT_EMAIL

if ($LASTEXITCODE -eq 0) {
    $STAGING_URL = gcloud run services describe $env:CODEX_STAGING_SERVICE --region=$env:GCP_REGION --format="value(status.url)"
    Write-Host "✅ Staging deployed: $STAGING_URL" -ForegroundColor Green
} else {
    Write-Host "❌ Staging deployment failed" -ForegroundColor Red
    exit 1
}

# Set up custom domain (optional)
Write-Host ""
Write-Host "🌐 === CUSTOM DOMAIN SETUP (OPTIONAL) ===" -ForegroundColor Cyan
$setup_domains = Read-Host "Do you want to set up custom domains? (y/n)"

if ($setup_domains -eq "y") {
    $PROD_DOMAIN = Read-Host "Enter production domain (e.g., app.codexdominion.com)"
    $STAGING_DOMAIN = Read-Host "Enter staging domain (e.g., staging.codexdominion.com)"
    
    if (![string]::IsNullOrWhiteSpace($PROD_DOMAIN)) {
        Write-Host "🔗 Mapping production domain: $PROD_DOMAIN" -ForegroundColor Yellow
        gcloud run domain-mappings create --service=$env:CODEX_PRODUCTION_SERVICE --domain=$PROD_DOMAIN --region=$env:GCP_REGION
    }
    
    if (![string]::IsNullOrWhiteSpace($STAGING_DOMAIN)) {
        Write-Host "🔗 Mapping staging domain: $STAGING_DOMAIN" -ForegroundColor Yellow
        gcloud run domain-mappings create --service=$env:CODEX_STAGING_SERVICE --domain=$STAGING_DOMAIN --region=$env:GCP_REGION
    }
}

# Save deployment info
Write-Host ""
Write-Host "💾 === SAVING DEPLOYMENT INFO ===" -ForegroundColor Cyan

$deploymentInfo = @{
    deployment_date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    project_id = $env:GCP_PROJECT_ID
    region = $env:GCP_REGION
    services = @{
        production = @{
            name = $env:CODEX_PRODUCTION_SERVICE
            url = $PRODUCTION_URL
            image = $PRODUCTION_IMAGE
        }
        staging = @{
            name = $env:CODEX_STAGING_SERVICE
            url = $STAGING_URL
            image = $STAGING_IMAGE
        }
    }
    docker_registry = $env:DOCKER_REGISTRY
} | ConvertTo-Json -Depth 4

$deploymentInfo | Out-File -FilePath "deployment-info.json" -Encoding UTF8

Write-Host "📄 Deployment info saved to: deployment-info.json" -ForegroundColor Green

# Show final summary
Write-Host ""
Write-Host "🏁 === DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host "✅ Services deployed to Google Cloud Run" -ForegroundColor Green
Write-Host "✅ Images pushed to Artifact Registry" -ForegroundColor Green
Write-Host "✅ Configuration saved" -ForegroundColor Green
Write-Host ""
Write-Host "🔍 Access your Codex Dashboard:" -ForegroundColor Cyan
Write-Host "   🌟 Production: $PRODUCTION_URL" -ForegroundColor White
Write-Host "   🔧 Staging: $STAGING_URL" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Cyan
Write-Host "   View logs: gcloud run logs tail $($env:CODEX_PRODUCTION_SERVICE) --region=$($env:GCP_REGION)" -ForegroundColor White
Write-Host "   Update service: gcloud run deploy $($env:CODEX_PRODUCTION_SERVICE) --image=$PRODUCTION_IMAGE --region=$($env:GCP_REGION)" -ForegroundColor White
Write-Host "   Delete service: gcloud run services delete $($env:CODEX_PRODUCTION_SERVICE) --region=$($env:GCP_REGION)" -ForegroundColor White
Write-Host "   Monitor: gcloud run services list --region=$($env:GCP_REGION)" -ForegroundColor White
Write-Host ""
Write-Host "💰 Estimated costs:" -ForegroundColor Cyan
Write-Host "   • Cloud Run: ~`$5-20/month (depends on usage)" -ForegroundColor White
Write-Host "   • Artifact Registry: ~`$0.10/GB/month" -ForegroundColor White
Write-Host "   • Networking: Minimal for normal usage" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Sacred flames now burn eternal in Google Cloud! ✨" -ForegroundColor Magenta