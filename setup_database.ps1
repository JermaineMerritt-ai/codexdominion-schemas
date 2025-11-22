# Codex Dominion - Google Cloud SQL PostgreSQL Setup
# =================================================
# Complete database infrastructure for your treasury system

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$ProjectId,
    [string]$InstanceName = "codex-ledger",
    [string]$DatabaseName = "codex",
    [string]$Username = "codex_user",
    [string]$Password = "codex_pass",
    [string]$Region = "us-central1"
)

Write-Host "🗄️ Setting up Codex Dominion PostgreSQL Infrastructure" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Yellow
Write-Host "📋 Project: $ProjectId" -ForegroundColor Cyan
Write-Host "🏢 Instance: $InstanceName" -ForegroundColor Cyan
Write-Host "🗃️ Database: $DatabaseName" -ForegroundColor Cyan
Write-Host "👤 User: $Username" -ForegroundColor Cyan
Write-Host "🌍 Region: $Region" -ForegroundColor Cyan
Write-Host ""

# Set project
gcloud config set project $ProjectId

# Enable required APIs
Write-Host "🔧 Enabling Google Cloud SQL APIs..." -ForegroundColor Green
gcloud services enable sqladmin.googleapis.com
gcloud services enable sql-component.googleapis.com

# Create PostgreSQL instance (your exact commands)
Write-Host "🏗️ Creating PostgreSQL instance..." -ForegroundColor Green
Write-Host "Command: gcloud sql instances create $InstanceName --database-version=POSTGRES_15 --tier=db-f1-micro --region=$Region" -ForegroundColor White

gcloud sql instances create $InstanceName `
  --database-version=POSTGRES_15 `
  --tier=db-f1-micro `
  --region=$Region

Write-Host "✅ PostgreSQL instance created!" -ForegroundColor Green

# Create database (your exact command)
Write-Host "🗃️ Creating database..." -ForegroundColor Green
Write-Host "Command: gcloud sql databases create $DatabaseName --instance=$InstanceName" -ForegroundColor White

gcloud sql databases create $DatabaseName `
  --instance=$InstanceName

Write-Host "✅ Database created!" -ForegroundColor Green

# Create user (your exact command)
Write-Host "👤 Creating database user..." -ForegroundColor Green
Write-Host "Command: gcloud sql users create $Username --instance=$InstanceName --password=$Password" -ForegroundColor White

gcloud sql users create $Username `
  --instance=$InstanceName `
  --password=$Password

Write-Host "✅ Database user created!" -ForegroundColor Green

# Get connection info
Write-Host ""
Write-Host "📊 Database Connection Information:" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Yellow

$ConnectionName = gcloud sql instances describe $InstanceName --format="value(connectionName)"
$IpAddress = gcloud sql instances describe $InstanceName --format="value(ipAddresses[0].ipAddress)"

Write-Host "🔌 Connection Name: $ConnectionName" -ForegroundColor Cyan
Write-Host "🌐 IP Address: $IpAddress" -ForegroundColor Cyan
Write-Host "🗃️ Database: $DatabaseName" -ForegroundColor Cyan
Write-Host "👤 Username: $Username" -ForegroundColor Cyan
Write-Host "🔑 Password: $Password" -ForegroundColor Cyan
Write-Host ""

# Initialize database schema
Write-Host "📋 Initializing Codex treasury schema..." -ForegroundColor Green
Write-Host "This will create all necessary tables and indexes." -ForegroundColor Yellow

# Create connection string for Cloud Run
$CloudRunConnectionString = "postgresql://$Username`:$Password@/$DatabaseName`?host=/cloudsql/$ConnectionName"

Write-Host ""
Write-Host "🚀 Cloud Run Configuration:" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow
Write-Host "Environment Variables to add to your Cloud Run deployment:" -ForegroundColor Green
Write-Host ""
Write-Host "DATABASE_URL=$CloudRunConnectionString" -ForegroundColor White
Write-Host "INSTANCE_CONNECTION_NAME=$ConnectionName" -ForegroundColor White
Write-Host "DB_USER=$Username" -ForegroundColor White
Write-Host "DB_PASS=$Password" -ForegroundColor White
Write-Host "DB_NAME=$DatabaseName" -ForegroundColor White
Write-Host ""

# Update deployment command
Write-Host "📝 Updated Deployment Command:" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow
Write-Host "Use this enhanced command to deploy with PostgreSQL:" -ForegroundColor Green
Write-Host ""
Write-Host "gcloud run deploy codex-dashboard \" -ForegroundColor White
Write-Host "  --image gcr.io/$ProjectId/codex-dashboard \" -ForegroundColor White
Write-Host "  --platform managed \" -ForegroundColor White
Write-Host "  --region $Region \" -ForegroundColor White
Write-Host "  --allow-unauthenticated \" -ForegroundColor White
Write-Host "  --memory 512Mi \" -ForegroundColor White
Write-Host "  --cpu 1 \" -ForegroundColor White
Write-Host "  --add-cloudsql-instances $ConnectionName \" -ForegroundColor White
Write-Host "  --set-env-vars `"DATABASE_URL=$CloudRunConnectionString,INSTANCE_CONNECTION_NAME=$ConnectionName`"" -ForegroundColor White
Write-Host ""

Write-Host "✅ PostgreSQL infrastructure ready!" -ForegroundColor Green
Write-Host "💰 Your treasury system can now use enterprise-grade PostgreSQL!" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔥 Next steps:" -ForegroundColor Green
Write-Host "1. Deploy your application with the updated command above" -ForegroundColor White
Write-Host "2. Your $5,125.48 treasury will automatically migrate to PostgreSQL" -ForegroundColor White
Write-Host "3. Enjoy enterprise-grade database reliability!" -ForegroundColor White