#!/usr/bin/env pwsh
# SSH Setup Helper for IONOS Server
# Generated: December 2, 2025

$IONOS_SERVER = "74.208.123.158"
$SSH_KEY = "$HOME\.ssh\ionos_codexdominion"
$SSH_PUB_KEY = "$HOME\.ssh\ionos_codexdominion.pub"

Write-Host "🔑 IONOS SSH Setup Helper" -ForegroundColor Cyan
Write-Host "=" * 60

# Check if keys exist
if (Test-Path $SSH_KEY) {
    Write-Host "✅ SSH keys found!" -ForegroundColor Green
    Write-Host "   Private: $SSH_KEY"
    Write-Host "   Public:  $SSH_PUB_KEY"
} else {
    Write-Host "❌ SSH keys not found!" -ForegroundColor Red
    Write-Host "   Run: ssh-keygen -t ed25519 -C 'github@codexdominion.app' -f $SSH_KEY"
    exit 1
}

Write-Host ""
Write-Host "📋 STEP 1: Copy Public Key to IONOS Server" -ForegroundColor Yellow
Write-Host "=" * 60

$publicKey = Get-Content $SSH_PUB_KEY
Write-Host "Public Key:" -ForegroundColor Cyan
Write-Host $publicKey -ForegroundColor White

Write-Host ""
Write-Host "Run these commands on your IONOS server:" -ForegroundColor Yellow
Write-Host "  1. SSH into server: ssh root@$IONOS_SERVER" -ForegroundColor Gray
Write-Host "  2. Create .ssh directory: mkdir -p ~/.ssh" -ForegroundColor Gray
Write-Host "  3. Add public key: echo '$publicKey' >> ~/.ssh/authorized_keys" -ForegroundColor Gray
Write-Host "  4. Set permissions: chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray

Write-Host ""
Write-Host "📋 STEP 2: Test SSH Connection" -ForegroundColor Yellow
Write-Host "=" * 60
Write-Host "Press Enter to test SSH connection..." -ForegroundColor Cyan
$null = Read-Host

Write-Host "Testing connection to $IONOS_SERVER..." -ForegroundColor Yellow
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$IONOS_SERVER "echo '✅ SSH connection successful!' && uname -a"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ SSH connection working!" -ForegroundColor Green
} else {
    Write-Host "❌ SSH connection failed. Make sure public key is added to server." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 STEP 3: Add Private Key to GitHub" -ForegroundColor Yellow
Write-Host "=" * 60
Write-Host "1. Go to: https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions" -ForegroundColor Gray
Write-Host "2. Click 'New repository secret'" -ForegroundColor Gray
Write-Host "3. Name: IONOS_SSH_KEY" -ForegroundColor Gray
Write-Host "4. Value: Copy content from file below" -ForegroundColor Gray
Write-Host ""
Write-Host "Private Key File: $SSH_KEY" -ForegroundColor Cyan
Write-Host ""
Write-Host "Copy private key to clipboard? (y/n): " -ForegroundColor Yellow -NoNewline
$copy = Read-Host

if ($copy -eq 'y') {
    Get-Content $SSH_KEY | Set-Clipboard
    Write-Host "✅ Private key copied to clipboard!" -ForegroundColor Green
    Write-Host "   Paste this into GitHub secret IONOS_SSH_KEY" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📋 STEP 4: Verify Server Setup" -ForegroundColor Yellow
Write-Host "=" * 60
Write-Host "Press Enter to check if IONOS server has required software..." -ForegroundColor Cyan
$null = Read-Host

Write-Host "Checking server configuration..." -ForegroundColor Yellow
ssh -i $SSH_KEY root@$IONOS_SERVER @"
echo '🔍 Server Status Check'
echo '======================'
echo ''
echo '📦 Operating System:'
cat /etc/os-release | grep PRETTY_NAME
echo ''
echo '🐳 Docker:'
if command -v docker &> /dev/null; then
    docker --version
else
    echo '❌ Docker not installed'
fi
echo ''
echo '🌐 Nginx:'
if command -v nginx &> /dev/null; then
    nginx -v
else
    echo '❌ Nginx not installed'
fi
echo ''
echo '🔒 Certbot:'
if command -v certbot &> /dev/null; then
    certbot --version
else
    echo '❌ Certbot not installed'
fi
echo ''
echo '💾 Disk Space:'
df -h / | tail -1
echo ''
echo '🧠 Memory:'
free -h | grep Mem
"@

Write-Host ""
Write-Host "🎉 SSH Setup Complete!" -ForegroundColor Green
Write-Host "=" * 60
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. ✅ SSH key generated and tested"
Write-Host "  2. ☐ Add IONOS_SSH_KEY to GitHub secrets"
Write-Host "  3. ☐ Run server setup: ./scripts/setup-ionos-server.sh"
Write-Host "  4. ☐ Purchase CodexDominion.app domain"
Write-Host "  5. ☐ Configure DNS in Google Domains"
Write-Host "  6. ☐ Deploy via GitHub Actions"
Write-Host ""
Write-Host "📖 Full guide: MULTI_CLOUD_DEPLOYMENT_GUIDE.md" -ForegroundColor Gray
