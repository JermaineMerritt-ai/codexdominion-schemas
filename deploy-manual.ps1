# =============================================================================
# CODEX DOMINION - Manual Deployment Steps
# =============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,

    [Parameter(Mandatory=$true)]
    [string]$Username,

    [Parameter(Mandatory=$false)]
    [string]$SSHKey = "$HOME\.ssh\id_rsa"
)

Write-Host "`n🔥 CODEX DOMINION - DEPLOYMENT 🔥`n" -ForegroundColor Cyan
Write-Host "Server: $ServerIP" -ForegroundColor Yellow
Write-Host "User: $Username`n"

$confirm = Read-Host "Ready to deploy? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    exit 0
}

# Step 1: Build
Write-Host "`n[Step 1] Building frontend..." -ForegroundColor Cyan
Push-Location frontend
npm run build
Pop-Location
Write-Host "✓ Build complete`n" -ForegroundColor Green

# Step 2: Package
Write-Host "[Step 2] Creating package..." -ForegroundColor Cyan
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archive = "codex_$timestamp.tar.gz"

Write-Host "Please run this in WSL or Git Bash:`n" -ForegroundColor Yellow
Write-Host "tar -czf $archive frontend/.next/standalone/ frontend/.next/static/ src/ deployment/ requirements.txt .env.production`n" -ForegroundColor White

Read-Host "Press Enter after creating the archive"

# Step 3: Upload
Write-Host "[Step 3] Uploading to server..." -ForegroundColor Cyan
scp -i $SSHKey $archive "${Username}@${ServerIP}:/tmp/"
Write-Host "✓ Upload complete`n" -ForegroundColor Green

# Step 4: Deploy
Write-Host "[Step 4] Deploying on server..." -ForegroundColor Cyan
Write-Host "Connecting to server...`n" -ForegroundColor Yellow

ssh -i $SSHKey "${Username}@${ServerIP}" @"
cd /tmp
tar -xzf $archive
sudo mkdir -p /var/www/codexdominion.app/frontend
sudo rsync -av frontend/.next/standalone/ /var/www/codexdominion.app/frontend/
sudo mkdir -p /var/www/codexdominion.app/frontend/.next
sudo rsync -av frontend/.next/static/ /var/www/codexdominion.app/frontend/.next/static/
sudo rsync -av src/ /var/www/codexdominion.app/src/
sudo rsync -av deployment/ /var/www/codexdominion.app/deployment/
sudo chown -R www-data:www-data /var/www/codexdominion.app
rm -rf frontend src deployment requirements.txt .env.production $archive
echo 'Deployment complete!'
"@

Write-Host "`n✓ DEPLOYMENT COMPLETE!`n" -ForegroundColor Green
