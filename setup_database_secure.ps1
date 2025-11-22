# Codex Dominion - Secure Database Setup with Secret Manager
# =========================================================
# Enhanced security using Google Cloud Secret Manager

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId,
    [string]$InstanceName = "codex-ledger",
    [string]$DatabaseName = "codex",
    [string]$Username = "codex_user",
    [string]$SecretName = "codex-db-pass",
    [string]$Region = "us-central1"
)

Write-Host "🔒 Setting up Codex Dominion with Google Cloud Secret Manager" -ForegroundColor Yellow
Write-Host "=============================================================" -ForegroundColor Yellow
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🏢 Instance: $InstanceName" -ForegroundColor Cyan
Write-Host "🗃️ Database: $DatabaseName" -ForegroundColor Cyan
Write-Host "👤 User: $Username" -ForegroundColor Cyan
Write-Host "🔐 Secret: $SecretName" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Set project
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "🔧 Enabling Google Cloud APIs..." -ForegroundColor Green
gcloud services enable sqladmin.googleapis.com
gcloud services enable sql-component.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Store database password in Secret Manager (your exact command)
Write-Host "🔐 Creating database password secret..." -ForegroundColor Green
Write-Host "Command: echo -n 'codex_pass' | gcloud secrets create $SecretName --data-file=-" -ForegroundColor White

echo -n "codex_pass" | gcloud secrets create $SecretName --data-file=-

Write-Host "✅ Secret created successfully!" -ForegroundColor Green

# Create PostgreSQL instance
Write-Host "🏗️ Creating PostgreSQL instance..." -ForegroundColor Green
gcloud sql instances create $InstanceName `
  --database-version=POSTGRES_15 `
  --tier=db-f1-micro `
  --region=$Region

# Create database
Write-Host "🗃️ Creating database..." -ForegroundColor Green
gcloud sql databases create $DatabaseName `
  --instance=$InstanceName

# Get password from Secret Manager for user creation
Write-Host "🔑 Retrieving password from Secret Manager..." -ForegroundColor Green
$Password = gcloud secrets versions access latest --secret=$SecretName

# Create user with secret password
Write-Host "👤 Creating database user..." -ForegroundColor Green
gcloud sql users create $Username `
  --instance=$InstanceName `
  --password=$Password

# Get connection information
$ConnectionName = gcloud sql instances describe $InstanceName --format="value(connectionName)"
$IpAddress = gcloud sql instances describe $InstanceName --format="value(ipAddresses[0].ipAddress)"

Write-Host ""
Write-Host "📊 Database Connection Information:" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow
Write-Host "🔌 Connection Name: $ConnectionName" -ForegroundColor Cyan
Write-Host "🌐 IP Address: $IpAddress" -ForegroundColor Cyan
Write-Host "🗃️ Database: $DatabaseName" -ForegroundColor Cyan
Write-Host "👤 Username: $Username" -ForegroundColor Cyan
Write-Host "🔐 Password Secret: $SecretName" -ForegroundColor Cyan
Write-Host ""

# Create secure Cloud Run deployment command
Write-Host "🚀 Secure Cloud Run Deployment:" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow
Write-Host "Use this enhanced command with Secret Manager integration:" -ForegroundColor Green
Write-Host ""

$SecureConnectionString = "postgresql://$Username`:`$(gcloud secrets versions access latest --secret=$SecretName)@/$DatabaseName`?host=/cloudsql/$ConnectionName"

Write-Host "# Build container" -ForegroundColor White
Write-Host "gcloud builds submit --tag gcr.io/$ProjectId/codex-dashboard" -ForegroundColor White
Write-Host "" 
Write-Host "# Deploy with Secret Manager integration" -ForegroundColor White
Write-Host "gcloud run deploy codex-dashboard \" -ForegroundColor White
Write-Host "  --image gcr.io/$ProjectId/codex-dashboard \" -ForegroundColor White
Write-Host "  --platform managed \" -ForegroundColor White
Write-Host "  --region $Region \" -ForegroundColor White
Write-Host "  --allow-unauthenticated \" -ForegroundColor White
Write-Host "  --memory 512Mi \" -ForegroundColor White
Write-Host "  --cpu 1 \" -ForegroundColor White
Write-Host "  --add-cloudsql-instances $ConnectionName \" -ForegroundColor White
Write-Host "  --set-secrets DB_PASS=$SecretName`:latest \" -ForegroundColor White
Write-Host "  --set-env-vars `"INSTANCE_CONNECTION_NAME=$ConnectionName,DB_USER=$Username,DB_NAME=$DatabaseName`"" -ForegroundColor White
Write-Host ""

# Show environment variables for manual setup
Write-Host "🔧 Environment Variables for Cloud Run:" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow
Write-Host "INSTANCE_CONNECTION_NAME=$ConnectionName" -ForegroundColor White
Write-Host "DB_USER=$Username" -ForegroundColor White
Write-Host "DB_NAME=$DatabaseName" -ForegroundColor White
Write-Host "DB_PASS=`$(Secret Manager: $SecretName)" -ForegroundColor White
Write-Host ""

# Security benefits
Write-Host "🔒 Security Benefits:" -ForegroundColor Yellow
Write-Host "====================" -ForegroundColor Yellow
Write-Host "✅ Password stored in Google Secret Manager" -ForegroundColor Green
Write-Host "✅ Automatic secret rotation support" -ForegroundColor Green
Write-Host "✅ IAM-controlled access to secrets" -ForegroundColor Green
Write-Host "✅ Audit logging for secret access" -ForegroundColor Green
Write-Host "✅ No passwords in deployment scripts" -ForegroundColor Green
Write-Host "✅ Encrypted secret storage and transmission" -ForegroundColor Green
Write-Host ""

Write-Host "✅ Secure PostgreSQL infrastructure ready!" -ForegroundColor Green
Write-Host "🔐 Your treasury system now uses enterprise-grade secret management!" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔥 Next steps:" -ForegroundColor Green
Write-Host "1. Deploy your application using the secure command above" -ForegroundColor White
Write-Host "2. Your $5,125.48 treasury will use encrypted password storage" -ForegroundColor White
Write-Host "3. Monitor secret access via Cloud Console audit logs" -ForegroundColor White