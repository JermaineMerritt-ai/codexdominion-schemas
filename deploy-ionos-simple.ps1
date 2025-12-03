# 🔥 Simplified IONOS Deployment Script for CodexDominion.app
# Skips local Python compilation - will install dependencies on IONOS server

param(
    [string]$IonosServer = "your-ionos-server-ip",
    [string]$IonosUser = "your-ionos-username"
)

$ErrorActionPreference = "Continue"

Write-Host "`n🔥 CODEXDOMINION.APP - IONOS DEPLOYMENT PACKAGE 🔥" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

$Domain = "codexdominion.app"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$DeployArchive = "codexdominion_$Timestamp.zip"

Write-Host "📋 Configuration" -ForegroundColor Green
Write-Host "  Domain: $Domain" -ForegroundColor White
Write-Host "  Archive: $DeployArchive" -ForegroundColor White
Write-Host "  Timestamp: $Timestamp`n" -ForegroundColor White

# Step 1: Build Frontend (already done)
Write-Host "✅ Step 1: Frontend already built in frontend/out`n" -ForegroundColor Green

# Step 2: Create deployment package (without .venv)
Write-Host "📦 Step 2: Creating Deployment Package..." -ForegroundColor Green
Write-Host "-------------------------------------------" -ForegroundColor Cyan

# Create temporary staging directory
$StagingDir = ".\deploy-staging-$Timestamp"
Write-Host "  Creating staging directory..." -ForegroundColor White
New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null

# Copy files to staging
Write-Host "  Copying application files..." -ForegroundColor White

# Frontend build output
if (Test-Path "frontend\out") {
    Write-Host "    - Frontend build (frontend/out)" -ForegroundColor Cyan
    Copy-Item -Path "frontend\out" -Destination "$StagingDir\frontend\out" -Recurse -Force
}
if (Test-Path "frontend\.next") {
    Write-Host "    - Frontend next (frontend/.next)" -ForegroundColor Cyan
    Copy-Item -Path "frontend\.next" -Destination "$StagingDir\frontend\.next" -Recurse -Force
}
if (Test-Path "frontend\public") {
    Write-Host "    - Frontend public (frontend/public)" -ForegroundColor Cyan
    Copy-Item -Path "frontend\public" -Destination "$StagingDir\frontend\public" -Recurse -Force
}

# Backend source
if (Test-Path "src") {
    Write-Host "    - Backend source (src/)" -ForegroundColor Cyan
    Copy-Item -Path "src" -Destination "$StagingDir\src" -Recurse -Force
}

# Python package
if (Test-Path "codexdominion") {
    Write-Host "    - CodexDominion package (codexdominion/)" -ForegroundColor Cyan
    Copy-Item -Path "codexdominion" -Destination "$StagingDir\codexdominion" -Recurse -Force
}

# Artifacts
if (Test-Path "artifacts") {
    Write-Host "    - Artifacts (artifacts/)" -ForegroundColor Cyan
    Copy-Item -Path "artifacts" -Destination "$StagingDir\artifacts" -Recurse -Force
}

# Config files
Write-Host "    - Configuration files" -ForegroundColor Cyan
$ConfigFiles = @(
    "requirements.txt",
    "package.json",
    "package-lock.json",
    ".env.production.example"
)

foreach ($file in $ConfigFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $StagingDir -Force
    }
}

# Server configs
Write-Host "    - Server configurations" -ForegroundColor Cyan
$ServerFiles = @(
    "codexdominion-api.service",
    "nginx-codexdominion.conf",
    "IONOS_SETUP_GUIDE.md",
    "deploy-ionos.sh"
)

foreach ($file in $ServerFiles) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $StagingDir -Force
    }
}

# Create archive
Write-Host "  Compressing to $DeployArchive..." -ForegroundColor White
try {
    Compress-Archive -Path "$StagingDir\*" -DestinationPath $DeployArchive -Force
    $archiveSize = (Get-Item $DeployArchive).Length / 1MB
    Write-Host "✅ Deployment package created: $DeployArchive ($([math]::Round($archiveSize, 2)) MB)`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creating archive: $_`n" -ForegroundColor Red
    Remove-Item -Path $StagingDir -Recurse -Force
    exit 1
}

# Cleanup staging
Write-Host "  Cleaning up staging directory..." -ForegroundColor White
Remove-Item -Path $StagingDir -Recurse -Force

# Step 3: Upload instructions
Write-Host "🚀 Step 3: Upload to IONOS Server" -ForegroundColor Green
Write-Host "---------------------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "# 1. Upload deployment package" -ForegroundColor White
Write-Host "scp $DeployArchive ${IonosUser}@${IonosServer}:/tmp/" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 2. SSH to server and extract" -ForegroundColor White
Write-Host "ssh ${IonosUser}@${IonosServer}" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 3. On IONOS server, run:" -ForegroundColor White
Write-Host "sudo mkdir -p /var/www/codexdominion.app" -ForegroundColor Cyan
Write-Host "sudo unzip -o /tmp/$DeployArchive -d /var/www/codexdominion.app" -ForegroundColor Cyan
Write-Host "cd /var/www/codexdominion.app" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 4. Install Python dependencies on server (Linux has proper build tools)" -ForegroundColor White
Write-Host "python3 -m venv .venv" -ForegroundColor Cyan
Write-Host "source .venv/bin/activate" -ForegroundColor Cyan
Write-Host "pip install -r requirements.txt" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 5. Follow IONOS_SETUP_GUIDE.md for complete setup" -ForegroundColor White
Write-Host "cat IONOS_SETUP_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🔥 Ready to Deploy! 🔥" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Package Contents:" -ForegroundColor Green
Write-Host "  ✅ Frontend build (Next.js static export)" -ForegroundColor White
Write-Host "  ✅ Backend source code (FastAPI)" -ForegroundColor White
Write-Host "  ✅ CodexDominion package" -ForegroundColor White
Write-Host "  ✅ Artifacts and capsules" -ForegroundColor White
Write-Host "  ✅ Server configuration files" -ForegroundColor White
Write-Host "  ✅ Setup guide" -ForegroundColor White
Write-Host ""
Write-Host "Next: Upload $DeployArchive to IONOS server" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ CodexDominion.app deployment package ready! ✨" -ForegroundColor Yellow
Write-Host ""
