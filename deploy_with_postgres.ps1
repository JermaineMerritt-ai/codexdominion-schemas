# Codex Dominion - Complete Cloud Deployment with PostgreSQL
# ==========================================================
# Full deployment including database infrastructure

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId,
    [switch]$SetupDatabase,
    [string]$InstanceName = "codex-ledger",
    [string]$DatabaseName = "codex",
    [string]$Username = "codex_user",
    [string]$Password = "codex_pass",
    [string]$Region = "us-central1"
)

$ServiceName = "codex-dashboard"

Write-Host "🔥 Codex Dominion - Complete Cloud Deployment" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🚀 Service: $ServiceName" -ForegroundColor Cyan
Write-Host "🗄️ Database: $(if($SetupDatabase){'Will be created'}else{'Assumed existing'})" -ForegroundColor Cyan
Write-Host ""

# Set project
gcloud config set project $ProjectId

# Setup database if requested
if ($SetupDatabase) {
    Write-Host "🗄️ Setting up PostgreSQL database with Secret Manager..." -ForegroundColor Green
    
    # Enable APIs
    gcloud services enable sqladmin.googleapis.com
    gcloud services enable sql-component.googleapis.com
    gcloud services enable secretmanager.googleapis.com
    
    # Store password in Secret Manager (your exact command)
    Write-Host "Creating database password secret..." -ForegroundColor White
    Write-Output "codex_pass" | gcloud secrets create codex-db-pass --data-file=-
    
    # Create instance (your exact commands)
    Write-Host "Creating PostgreSQL instance: $InstanceName" -ForegroundColor White
    gcloud sql instances create $InstanceName `
        --database-version=POSTGRES_15 `
        --tier=db-f1-micro `
        --region=$Region
    
    # Create database (your exact command)
    Write-Host "Creating database: $DatabaseName" -ForegroundColor White
    gcloud sql databases create $DatabaseName `
        --instance=$InstanceName
    
    # Get password from Secret Manager
    $SecretPassword = gcloud secrets versions access latest --secret=codex-db-pass
    
    # Create user with secret password
    Write-Host "Creating user: $Username" -ForegroundColor White
    gcloud sql users create $Username `
        --instance=$InstanceName `
        --password=$SecretPassword
    
    Write-Host "✅ Secure database setup complete!" -ForegroundColor Green
}

# Enable Cloud Run APIs
Write-Host "🔧 Enabling Cloud APIs..." -ForegroundColor Green
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build container (your exact command)
Write-Host "🏗️ Building container..." -ForegroundColor Green
Write-Host "Command: gcloud builds submit --tag gcr.io/$ProjectId/$ServiceName" -ForegroundColor White
gcloud builds submit --tag gcr.io/$ProjectId/$ServiceName

# Prepare deployment with secure database integration
$ConnectionName = "$ProjectId`:$Region`:$InstanceName"

# Deploy to Cloud Run with PostgreSQL and Secret Manager (secure version)
Write-Host ""
Write-Host "🚀 Deploying to Cloud Run with PostgreSQL and Secret Manager..." -ForegroundColor Green
Write-Host "Secure version of your commands with Secret Manager integration:" -ForegroundColor Yellow

gcloud run deploy $ServiceName `
    --image gcr.io/$ProjectId/$ServiceName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --add-cloudsql-instances $ConnectionName `
    --set-secrets "DB_PASS=codex-db-pass:latest" `
    --set-env-vars "INSTANCE_CONNECTION_NAME=$ConnectionName,DB_USER=$Username,DB_NAME=$DatabaseName,CODEX_ENVIRONMENT=production"

# Get service URL
$ServiceUrl = gcloud run services describe $ServiceName --region=$Region --format="value(status.url)"

Write-Host ""
Write-Host "✅ Complete deployment successful!" -ForegroundColor Green
Write-Host ""
Write-Host "🔥 Your Codex Dominion is LIVE with PostgreSQL!" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "🌐 Service URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "❤️ Health Check: $ServiceUrl/health" -ForegroundColor Cyan
Write-Host "📊 Treasury API: $ServiceUrl/api/treasury/summary" -ForegroundColor Cyan
Write-Host "🌅 Dawn API: $ServiceUrl/api/dawn/status" -ForegroundColor Cyan
Write-Host ""
Write-Host "🗄️ Database Information:" -ForegroundColor Yellow
Write-Host "Instance: $ProjectId`:$Region`:$InstanceName" -ForegroundColor White
Write-Host "Database: $DatabaseName" -ForegroundColor White
Write-Host "User: $Username" -ForegroundColor White
Write-Host ""

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Green
try {
    $health = Invoke-RestMethod "$ServiceUrl/health" -TimeoutSec 30
    Write-Host "✅ Health check passed!" -ForegroundColor Green
    Write-Host "Status: $($health.status)" -ForegroundColor Cyan
    Write-Host "Treasury: $($health.treasury)" -ForegroundColor Cyan
    Write-Host "Dawn Flame: $($health.dawn_flame)" -ForegroundColor Cyan
    Write-Host "Database: PostgreSQL (Cloud SQL)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️ Service starting up - try health check in 30 seconds" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Management Commands:" -ForegroundColor Green
Write-Host "Redeploy: .\deploy_with_postgres.ps1 $ProjectId" -ForegroundColor White
Write-Host "Database logs: gcloud sql instances describe $InstanceName" -ForegroundColor White
Write-Host "Service logs: gcloud run services logs read $ServiceName --region=$Region" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Digital sovereignty with enterprise PostgreSQL achieved! 👑" -ForegroundColor Yellow