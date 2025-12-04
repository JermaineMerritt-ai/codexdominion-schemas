# =============================================================================
# CODEX DOMINION - Simplified PowerShell Deployment
# =============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,

    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$false)]
    [string]$SSHKey = "$HOME\.ssh\id_rsa"
)

$ErrorActionPreference = "Stop"

Write-Host "`n🔥 CODEX DOMINION - DEPLOYMENT 🔥`n" -ForegroundColor Cyan
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server: $ServerIP"
Write-Host "  User: $Username"
Write-Host "  SSH Key: $SSHKey"
Write-Host ""

$confirm = Read-Host "Ready to deploy? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 1: Build Frontend
Write-Host "`n[1/3] Building Frontend...`n" -ForegroundColor Cyan
Set-Location frontend
npm install --production=false
npm run build
Set-Location ..
Write-Host "✓ Frontend build complete`n" -ForegroundColor Green

# Step 2: Create deployment package
Write-Host "[2/3] Creating deployment package...`n" -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveName = "codexdominion_$timestamp.tar.gz"

# Check if WSL tar is available
if (Get-Command wsl -ErrorAction SilentlyContinue) {
    # Convert path for WSL
    $wslPath = $PWD.Path -replace '^([A-Z]):', { "/mnt/$($_.Groups[1].Value.ToLower())" } -replace '\\', '/'

    wsl bash -c "cd '$wslPath' && tar -czf '$archiveName' frontend/.next/standalone/ frontend/.next/static/ frontend/public/ src/ deployment/ requirements.txt .env.production 2>/dev/null || tar -czf '$archiveName' frontend/.next/standalone/ frontend/.next/static/ src/ deployment/ requirements.txt .env.production"

    Write-Host "✓ Package created: $archiveName`n" -ForegroundColor Green
} else {
    Write-Host "✗ WSL not found. Please install WSL or use Git Bash manually." -ForegroundColor Red
    exit 1
}

# Step 3: Deploy to server
Write-Host "[3/3] Deploying to server...`n" -ForegroundColor Cyan

# Upload archive
Write-Host "Uploading files..." -ForegroundColor Yellow
scp -i $SSHKey $archiveName "${Username}@${ServerIP}:/tmp/"

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Upload failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Upload complete`n" -ForegroundColor Green

# Execute deployment on server
Write-Host "Deploying on server..." -ForegroundColor Yellow

$deployScript = @"
set -e
echo 'Creating directories...'
sudo mkdir -p /var/www/codexdominion.app/frontend
sudo mkdir -p /var/log/codexdominion
sudo mkdir -p /var/log/codexdominion-frontend

echo 'Extracting files...'
cd /tmp
tar -xzf $archiveName

echo 'Moving files to deployment directory...'
sudo rsync -av frontend/.next/standalone/ /var/www/codexdominion.app/frontend/ || true
sudo mkdir -p /var/www/codexdominion.app/frontend/.next
sudo rsync -av frontend/.next/static/ /var/www/codexdominion.app/frontend/.next/static/ || true
sudo rsync -av frontend/public/ /var/www/codexdominion.app/frontend/public/ 2>/dev/null || true
sudo rsync -av src/ /var/www/codexdominion.app/src/ || true
sudo rsync -av deployment/ /var/www/codexdominion.app/deployment/ || true
sudo cp requirements.txt /var/www/codexdominion.app/ || true
sudo cp .env.production /var/www/codexdominion.app/ || true

echo 'Cleaning up...'
cd /tmp
rm -rf frontend src deployment requirements.txt .env.production
rm $archiveName

echo 'Setting permissions...'
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chmod -R 755 /var/www/codexdominion.app
sudo chmod 600 /var/www/codexdominion.app/.env.production 2>/dev/null || true

echo 'Installing Node.js if needed...'
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo 'Node version:'
node --version || echo 'Node.js not installed'

echo ''
echo '✓ Deployment complete!'
echo ''
echo 'Next steps:'
echo '1. Install systemd services (deployment/codexdominion-frontend.service)'
echo '2. Configure nginx (deployment/nginx-production.conf)'
echo '3. Setup database (deployment/setup-database.sh)'
echo '4. Start services: sudo systemctl start codexdominion-frontend'
"@

ssh -i $SSHKey "${Username}@${ServerIP}" $deployScript

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ DEPLOYMENT SUCCESSFUL!`n" -ForegroundColor Green
    Write-Host "Application deployed to: /var/www/codexdominion.app" -ForegroundColor Cyan
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "1. SSH to server: ssh -i $SSHKey ${Username}@${ServerIP}"
    Write-Host "2. Install services: cd /var/www/codexdominion.app/deployment"
    Write-Host "3. Setup database: sudo bash setup-database.sh"
    Write-Host "4. Install systemd services and configure nginx"
} else {
    Write-Host "`n✗ Deployment failed!`n" -ForegroundColor Red
    exit 1
}
