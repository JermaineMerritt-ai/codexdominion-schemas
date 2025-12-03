# 🔥 IONOS Production Deployment PowerShell Script
# CodexDominion.app - December 3, 2025

param(
    [string]$IonosServer = "your-ionos-server-ip",
    [string]$IonosUser = "your-ionos-username",
    [string]$DeployPath = "/var/www/codexdominion.app"
)

Write-Host "`n🔥 CODEXDOMINION.APP - IONOS PRODUCTION DEPLOYMENT 🔥" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$Domain = "codexdominion.app"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$DeployArchive = "codexdominion_$Timestamp.zip"
$BackupPath = "/var/backups/codexdominion"

Write-Host "📋 Deployment Configuration" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Cyan
Write-Host "  Domain: $Domain" -ForegroundColor White
Write-Host "  Server: $IonosServer" -ForegroundColor White
Write-Host "  Deploy Path: $DeployPath" -ForegroundColor White
Write-Host "  Archive: $DeployArchive`n" -ForegroundColor White

# Step 1: Build Frontend
Write-Host "🔨 Step 1: Building Frontend Applications..." -ForegroundColor Green
Write-Host "-------------------------------------------" -ForegroundColor Cyan

if (Test-Path "frontend") {
    Push-Location frontend
    Write-Host "  Installing dependencies..." -ForegroundColor White
    npm install --production --silent
    Write-Host "  Building production bundle..." -ForegroundColor White
    npm run build
    Pop-Location
    Write-Host "✅ Frontend build complete`n" -ForegroundColor Green
} else {
    Write-Host "⚠️ Frontend directory not found, skipping...`n" -ForegroundColor Yellow
}

# Step 2: Prepare Python Backend
Write-Host "🐍 Step 2: Preparing Python Backend..." -ForegroundColor Green
Write-Host "---------------------------------------" -ForegroundColor Cyan

if (Test-Path ".venv/Scripts/Activate.ps1") {
    & .venv/Scripts/Activate.ps1
} else {
    Write-Host "  Creating virtual environment..." -ForegroundColor White
    python -m venv .venv
    & .venv/Scripts/Activate.ps1
}

Write-Host "  Installing dependencies..." -ForegroundColor White
pip install -r requirements.txt --quiet
Write-Host "✅ Backend dependencies installed`n" -ForegroundColor Green

# Step 3: Create Deployment Package
Write-Host "📦 Step 3: Creating Deployment Package..." -ForegroundColor Green
Write-Host "-------------------------------------------" -ForegroundColor Cyan

# Create list of files to include
$FilesToInclude = @(
    "frontend/out/*",
    "frontend/.next/*",
    "src/*",
    "artifacts/*",
    "codexdominion/*",
    "requirements.txt",
    "package.json",
    ".env.production.example"
)

# Create exclusion list
$Excludes = @(
    "node_modules",
    ".venv",
    ".git",
    "*.pyc",
    "__pycache__",
    ".next/cache"
)

Write-Host "  Creating archive: $DeployArchive" -ForegroundColor White

# Create zip file
$compress = @{
    Path = $FilesToInclude
    CompressionLevel = "Optimal"
    DestinationPath = $DeployArchive
}

try {
    Compress-Archive @compress -Force
    $archiveSize = (Get-Item $DeployArchive).Length / 1MB
    Write-Host "✅ Deployment package created: $DeployArchive ($([math]::Round($archiveSize, 2)) MB)`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creating archive: $_`n" -ForegroundColor Red
    exit 1
}

# Step 4: Display Upload Instructions
Write-Host "🚀 Step 4: Upload to IONOS Server" -ForegroundColor Green
Write-Host "---------------------------------" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run these commands to deploy:" -ForegroundColor Yellow
Write-Host ""
Write-Host "# 1. Upload deployment package" -ForegroundColor White
Write-Host "scp $DeployArchive ${IonosUser}@${IonosServer}:/tmp/" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 2. SSH to IONOS server" -ForegroundColor White
Write-Host "ssh ${IonosUser}@${IonosServer}" -ForegroundColor Cyan
Write-Host ""
Write-Host "# 3. On IONOS server, run:" -ForegroundColor White
Write-Host "sudo mkdir -p $BackupPath" -ForegroundColor Cyan
Write-Host "sudo tar -czf $BackupPath/backup_$Timestamp.tar.gz -C $DeployPath ." -ForegroundColor Cyan
Write-Host "sudo unzip -o /tmp/$DeployArchive -d $DeployPath" -ForegroundColor Cyan
Write-Host "sudo chown -R www-data:www-data $DeployPath" -ForegroundColor Cyan
Write-Host "sudo systemctl restart codexdominion-api" -ForegroundColor Cyan
Write-Host "sudo systemctl restart nginx" -ForegroundColor Cyan
Write-Host "rm /tmp/$DeployArchive" -ForegroundColor Cyan
Write-Host ""

# Step 5: Environment Variables
Write-Host "⚙️ Step 5: Environment Configuration" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Create .env.production on IONOS server at: $DeployPath/.env.production" -ForegroundColor Yellow
Write-Host ""
Write-Host "Required variables:" -ForegroundColor White
Write-Host "  DATABASE_URL=postgresql://user:pass@localhost/codexdominion" -ForegroundColor Cyan
Write-Host "  API_BASE_URL=https://api.codexdominion.app" -ForegroundColor Cyan
Write-Host "  FRONTEND_URL=https://codexdominion.app" -ForegroundColor Cyan
Write-Host "  NODE_ENV=production" -ForegroundColor Cyan
Write-Host "  PYTHON_ENV=production" -ForegroundColor Cyan
Write-Host "  JWT_SECRET=your-super-secret-key-here" -ForegroundColor Cyan
Write-Host "  ALLOWED_ORIGINS=https://codexdominion.app,https://www.codexdominion.app" -ForegroundColor Cyan
Write-Host ""

# Step 6: Service Configuration Files
Write-Host "📝 Step 6: Service Configuration" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "See the following generated files for server configuration:" -ForegroundColor Yellow
Write-Host "  - codexdominion-api.service (systemd service)" -ForegroundColor White
Write-Host "  - nginx-codexdominion.conf (nginx configuration)" -ForegroundColor White
Write-Host "  - IONOS_SETUP_GUIDE.md (complete setup instructions)" -ForegroundColor White
Write-Host ""

# Step 7: SSL Certificate
Write-Host "🔒 Step 7: SSL Certificate Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "On IONOS server, run:" -ForegroundColor Yellow
Write-Host "  sudo apt install certbot python3-certbot-nginx" -ForegroundColor Cyan
Write-Host "  sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "🔥 Deployment Package Ready! 🔥" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "  1. Upload $DeployArchive to IONOS server" -ForegroundColor White
Write-Host "  2. Configure systemd service and nginx" -ForegroundColor White
Write-Host "  3. Set up SSL with certbot" -ForegroundColor White
Write-Host "  4. Configure environment variables" -ForegroundColor White
Write-Host "  5. Start services and verify" -ForegroundColor White
Write-Host ""
Write-Host "📖 Read IONOS_SETUP_GUIDE.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ CodexDominion.app is ready to go live! ✨" -ForegroundColor Yellow
Write-Host ""
