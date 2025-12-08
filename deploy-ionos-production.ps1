#!/usr/bin/env pwsh
# =============================================================================
# Codex Dominion - IONOS Production Deployment Script
# =============================================================================
# Description: Complete deployment script for IONOS VPS
# Last Updated: December 7, 2025
# =============================================================================

param(
    [string]$DeploymentType = "full",  # Options: full, backend, frontend, database
    [switch]$SkipBackup,
    [switch]$Force,
    [switch]$UseACR,  # Use Azure Container Registry instead of local images
    [string]$ACRName = "codexdominion"  # ACR registry name
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# =============================================================================
# Configuration
# =============================================================================

$IONOS_HOST = "74.208.123.158"
$IONOS_USER = "root"
$DEPLOY_PATH = "/var/www/codexdominion"
$BACKUP_PATH = "/backups/codexdominion"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"

# Azure Container Registry configuration
if ($UseACR) {
    $ACR_LOGIN_SERVER = "$ACRName.azurecr.io"
    $BACKEND_IMAGE = "$ACR_LOGIN_SERVER/codexdominion-backend:production"
    $FRONTEND_IMAGE = "$ACR_LOGIN_SERVER/codexdominion-frontend:production"
    Write-Host "🔷 Azure Container Registry Mode Enabled" -ForegroundColor Blue
    Write-Host "   Registry: $ACR_LOGIN_SERVER" -ForegroundColor Gray
} else {
    $BACKEND_IMAGE = "codexdominion-backend:production"
    $FRONTEND_IMAGE = "codexdominion-frontend:production"
}
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔥 CODEX DOMINION - IONOS PRODUCTION DEPLOYMENT 🔥" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# =============================================================================
# Pre-Deployment Checks
# =============================================================================

Write-Host "[1/10] Running Pre-Deployment Checks..." -ForegroundColor Cyan

# Check if .env.production exists
if (-not (Test-Path ".\.env.production")) {
    Write-Host "❌ ERROR: .env.production file not found!" -ForegroundColor Red
    Write-Host "Please create .env.production file with production configuration." -ForegroundColor Yellow
    exit 1
}

# Check if SSH key exists or prompt for password
$sshKeyPath = "$env:USERPROFILE\.ssh\ionos_codexdominion"
if (Test-Path $sshKeyPath) {
    Write-Host "✓ SSH key found" -ForegroundColor Green
    $sshCommand = "ssh -i $sshKeyPath $IONOS_USER@$IONOS_HOST"
    $scpCommand = "scp -i $sshKeyPath"
} else {
    Write-Host "⚠ No SSH key found, will use password authentication" -ForegroundColor Yellow
    $sshCommand = "ssh $IONOS_USER@$IONOS_HOST"
    $scpCommand = "scp"
}

# Test SSH connection
Write-Host "Testing SSH connection to IONOS server..." -ForegroundColor Gray
$testConnection = Invoke-Expression "$sshCommand 'echo connected'" 2>&1
if ($testConnection -notcontains "connected") {
    Write-Host "❌ ERROR: Cannot connect to IONOS server!" -ForegroundColor Red
    Write-Host "Please check your SSH configuration and credentials." -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ SSH connection successful" -ForegroundColor Green

# =============================================================================
# Generate Cryptographic Keys
# =============================================================================

Write-Host "`n[2/10] Generating Cryptographic Keys..." -ForegroundColor Cyan

if (-not (Test-Path ".\keys")) {
    New-Item -ItemType Directory -Path ".\keys" | Out-Null
}

# Check if OpenSSL is available locally
$opensslAvailable = Get-Command openssl -ErrorAction SilentlyContinue

# Generate RSA keys for Digital Seal Service
if (-not (Test-Path ".\keys\rsa_private.pem")) {
    if ($opensslAvailable) {
        Write-Host "Generating RSA-2048 key pair locally..." -ForegroundColor Gray
        openssl genrsa -out .\keys\rsa_private.pem 2048 2>&1 | Out-Null
        openssl rsa -in .\keys\rsa_private.pem -pubout -out .\keys\rsa_public.pem 2>&1 | Out-Null
        Write-Host "✓ RSA keys generated" -ForegroundColor Green
    } else {
        Write-Host "⚠ OpenSSL not found locally - will generate keys on server" -ForegroundColor Yellow
        $generateOnServer = $true
    }
} else {
    Write-Host "✓ RSA keys already exist" -ForegroundColor Green
}

# Generate ECC keys for Digital Seal Service
if (-not (Test-Path ".\keys\ecc_private.pem")) {
    if ($opensslAvailable) {
        Write-Host "Generating ECC P-256 key pair locally..." -ForegroundColor Gray
        openssl ecparam -name prime256v1 -genkey -noout -out .\keys\ecc_private.pem 2>&1 | Out-Null
        openssl ec -in .\keys\ecc_private.pem -pubout -out .\keys\ecc_public.pem 2>&1 | Out-Null
        Write-Host "✓ ECC keys generated" -ForegroundColor Green
    } else {
        if (-not $generateOnServer) {
            Write-Host "⚠ OpenSSL not found locally - will generate keys on server" -ForegroundColor Yellow
        }
        $generateOnServer = $true
    }
} else {
    Write-Host "✓ ECC keys already exist" -ForegroundColor Green
}

# =============================================================================
# Create Backup
# =============================================================================

if (-not $SkipBackup) {
    Write-Host "`n[3/10] Creating Backup..." -ForegroundColor Cyan

    $backupScript = @"
mkdir -p $BACKUP_PATH
if [ -d "$DEPLOY_PATH" ]; then
    tar -czf $BACKUP_PATH/codexdominion_backup_$TIMESTAMP.tar.gz -C $DEPLOY_PATH . 2>/dev/null || true
    echo 'Backup created'
else
    echo 'No existing deployment to backup'
fi
"@

    Invoke-Expression "$sshCommand '$backupScript'"
    Write-Host "✓ Backup completed" -ForegroundColor Green
} else {
    Write-Host "`n[3/10] Skipping Backup..." -ForegroundColor Yellow
}

# =============================================================================
# Build Docker Images
# =============================================================================

Write-Host "`n[4/10] Building Docker Images..." -ForegroundColor Cyan

Write-Host "Building backend image..." -ForegroundColor Gray
docker build -t codexdominion-backend:production -f Dockerfile.backend .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Building frontend image..." -ForegroundColor Gray
Set-Location web
docker build -t codexdominion-frontend:production -f Dockerfile.production `
    --build-arg NEXT_PUBLIC_API_URL=https://api.codexdominion.app `
    --build-arg NEXT_PUBLIC_SITE_URL=https://codexdominion.app `
    --build-arg NEXT_PUBLIC_WS_URL=wss://api.codexdominion.app/ws .
Set-Location ..

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker images built successfully" -ForegroundColor Green

# Push to Azure Container Registry if enabled
if ($UseACR) {
    Write-Host "`n[4b/10] Pushing to Azure Container Registry..." -ForegroundColor Cyan

    Write-Host "Logging into ACR..." -ForegroundColor Gray
    az acr login --name $ACRName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ACR login failed! Run 'az login' first." -ForegroundColor Red
        exit 1
    }

    Write-Host "Tagging images for ACR..." -ForegroundColor Gray
    docker tag codexdominion-backend:production $BACKEND_IMAGE
    docker tag codexdominion-frontend:production $FRONTEND_IMAGE

    Write-Host "Pushing backend image to ACR..." -ForegroundColor Gray
    docker push $BACKEND_IMAGE
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Backend push failed!" -ForegroundColor Red
        exit 1
    }

    Write-Host "Pushing frontend image to ACR..." -ForegroundColor Gray
    docker push $FRONTEND_IMAGE
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Frontend push failed!" -ForegroundColor Red
        exit 1
    }

    Write-Host "✓ Images pushed to ACR successfully" -ForegroundColor Green
}

# =============================================================================
# Prepare Server
# =============================================================================

Write-Host "`n[5/10] Preparing IONOS Server..." -ForegroundColor Cyan

$prepareScript = @"
# Create directories
mkdir -p $DEPLOY_PATH/{backend,web,keys,uploads,logs,nginx}
mkdir -p /var/log/codexdominion

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo 'Installing Docker...'
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo 'Installing Docker Compose...'
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-`$(uname -s)-`$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Generate cryptographic keys if not uploaded
if [ ! -f "$DEPLOY_PATH/keys/rsa_private.pem" ]; then
    echo 'Generating RSA-2048 keys on server...'
    openssl genrsa -out $DEPLOY_PATH/keys/rsa_private.pem 2048 2>/dev/null
    openssl rsa -in $DEPLOY_PATH/keys/rsa_private.pem -pubout -out $DEPLOY_PATH/keys/rsa_public.pem 2>/dev/null
    echo 'RSA keys generated'
fi

if [ ! -f "$DEPLOY_PATH/keys/ecc_private.pem" ]; then
    echo 'Generating ECC P-256 keys on server...'
    openssl ecparam -name prime256v1 -genkey -noout -out $DEPLOY_PATH/keys/ecc_private.pem 2>/dev/null
    openssl ec -in $DEPLOY_PATH/keys/ecc_private.pem -pubout -out $DEPLOY_PATH/keys/ecc_public.pem 2>/dev/null
    echo 'ECC keys generated'
fi

echo 'Server prepared'
"@

Invoke-Expression "$sshCommand '$prepareScript'"
Write-Host "✓ Server prepared" -ForegroundColor Green

# =============================================================================
# Upload Files
# =============================================================================

Write-Host "`n[6/10] Uploading Files to IONOS..." -ForegroundColor Cyan

# Upload environment file
Invoke-Expression "$scpCommand .env.production $IONOS_USER@${IONOS_HOST}:$DEPLOY_PATH/.env"

# Upload Docker Compose
Invoke-Expression "$scpCommand docker-compose.prod.yml $IONOS_USER@${IONOS_HOST}:$DEPLOY_PATH/docker-compose.yml"

# Upload cryptographic keys (if generated locally)
if (Test-Path ".\keys\rsa_private.pem") {
    Write-Host "Uploading cryptographic keys..." -ForegroundColor Gray
    Invoke-Expression "$scpCommand keys/* $IONOS_USER@${IONOS_HOST}:$DEPLOY_PATH/keys/"
    Write-Host "✓ Keys uploaded" -ForegroundColor Green
} else {
    Write-Host "⚠ Keys will be generated on server" -ForegroundColor Yellow
}

Write-Host "✓ Files uploaded" -ForegroundColor Green

# =============================================================================
# Setup Database
# =============================================================================

Write-Host "`n[7/10] Setting Up PostgreSQL Database..." -ForegroundColor Cyan

$dbScript = @"
cd $DEPLOY_PATH

# Start PostgreSQL container
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo 'Waiting for PostgreSQL to start...'
sleep 10

# Run database migrations
docker-compose exec -T postgres psql -U codexdominion -d codex_dominion_prod -f /docker-entrypoint-initdb.d/init.sql || true

echo 'Database setup complete'
"@

Invoke-Expression "$sshCommand '$dbScript'"
Write-Host "✓ Database configured" -ForegroundColor Green

# =============================================================================
# Deploy Services
# =============================================================================

Write-Host "`n[8/10] Deploying Services..." -ForegroundColor Cyan

$deployScript = @"
cd $DEPLOY_PATH

# Pull images (if using registry)
# docker-compose pull

# Start all services
docker-compose up -d

# Wait for services to be healthy
echo 'Waiting for services to start...'
sleep 15

# Check service status
docker-compose ps

echo 'Services deployed'
"@

Invoke-Expression "$sshCommand '$deployScript'"
Write-Host "✓ Services deployed" -ForegroundColor Green

# =============================================================================
# Configure SSL
# =============================================================================

Write-Host "`n[9/10] Configuring SSL..." -ForegroundColor Cyan

$sslScript = @"
# Install certbot if not present
if ! command -v certbot &> /dev/null; then
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Obtain SSL certificate (if not exists)
if [ ! -f /etc/letsencrypt/live/codexdominion.app/fullchain.pem ]; then
    certbot certonly --standalone -d codexdominion.app -d www.codexdominion.app -d api.codexdominion.app --email admin@codexdominion.app --agree-tos --non-interactive || echo 'SSL setup skipped - configure manually'
else
    echo 'SSL certificates already exist'
fi

# Setup auto-renewal
if ! crontab -l | grep -q certbot; then
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet") | crontab -
fi

echo 'SSL configured'
"@

Invoke-Expression "$sshCommand '$sslScript'"
Write-Host "✓ SSL configured" -ForegroundColor Green

# =============================================================================
# Health Checks
# =============================================================================

Write-Host "`n[10/10] Running Health Checks..." -ForegroundColor Cyan

Start-Sleep -Seconds 5

# Check backend health
Write-Host "Checking backend health..." -ForegroundColor Gray
try {
    $backendHealth = Invoke-RestMethod -Uri "http://$IONOS_HOST:8000/health" -TimeoutSec 10
    Write-Host "✓ Backend is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠ Backend health check failed" -ForegroundColor Yellow
}

# Check frontend health
Write-Host "Checking frontend health..." -ForegroundColor Gray
try {
    $frontendHealth = Invoke-WebRequest -Uri "http://$IONOS_HOST:3000" -TimeoutSec 10 -UseBasicParsing
    Write-Host "✓ Frontend is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠ Frontend health check failed" -ForegroundColor Yellow
}

# =============================================================================
# Deployment Complete
# =============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✨ DEPLOYMENT COMPLETE! ✨" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Application URLs:" -ForegroundColor Yellow
Write-Host "   Frontend: https://codexdominion.app" -ForegroundColor White
Write-Host "   API:      https://api.codexdominion.app" -ForegroundColor White
Write-Host "   Docs:     https://api.codexdominion.app/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitoring:" -ForegroundColor Yellow
Write-Host "   View logs: ssh $IONOS_USER@$IONOS_HOST 'docker-compose -f $DEPLOY_PATH/docker-compose.yml logs -f'" -ForegroundColor White
Write-Host "   Status:    ssh $IONOS_USER@$IONOS_HOST 'docker-compose -f $DEPLOY_PATH/docker-compose.yml ps'" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Configure DNS A records to point to $IONOS_HOST" -ForegroundColor White
Write-Host "   2. Verify SSL certificates are working" -ForegroundColor White
Write-Host "   3. Test all features (spatial audio, exports, seals)" -ForegroundColor White
Write-Host "   4. Monitor logs for any errors" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
