#!/usr/bin/env pwsh
# Codex Dominion - IONOS Frontend Deployment Script
# Packages and deploys Next.js frontend to IONOS VPS

$ErrorActionPreference = "Stop"

$IONOS_SERVER = "74.208.123.158"
$IONOS_USER = "root"
$DEPLOY_DIR = "/var/www/codexdominion"
$DOMAIN = "CodexDominion.app"

Write-Host "🚀 Codex Dominion - IONOS Deployment Preparation" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if frontend build exists
if (-not (Test-Path "frontend\.next\standalone")) {
    Write-Host "❌ Frontend not built with standalone mode!" -ForegroundColor Red
    Write-Host "Building frontend now..." -ForegroundColor Yellow

    Set-Location frontend
    npm run build
    Set-Location ..
}

Write-Host "✅ Frontend build found" -ForegroundColor Green

# Create deployment package
Write-Host "`n📦 Creating deployment package..." -ForegroundColor Cyan

$packageDir = "ionos_deployment_package"
if (Test-Path $packageDir) {
    Remove-Item $packageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy necessary files
Write-Host "  Copying standalone build..." -ForegroundColor Gray
Copy-Item -Path "frontend\.next\standalone\*" -Destination "$packageDir\" -Recurse

Write-Host "  Copying static files..." -ForegroundColor Gray
New-Item -ItemType Directory -Path "$packageDir\.next" -Force | Out-Null
Copy-Item -Path "frontend\.next\static" -Destination "$packageDir\.next\static" -Recurse

Write-Host "  Copying public files..." -ForegroundColor Gray
if (Test-Path "frontend\public") {
    Copy-Item -Path "frontend\public" -Destination "$packageDir\public" -Recurse
}

# Create startup script
$startupScript = @"
#!/bin/bash
# Codex Dominion Frontend Startup Script

export NODE_ENV=production
export PORT=3000
export HOSTNAME=0.0.0.0

cd /var/www/codexdominion
node server.js
"@

Set-Content -Path "$packageDir\start.sh" -Value $startupScript
Write-Host "  Created startup script" -ForegroundColor Gray

# Create systemd service file
$serviceFile = @"
[Unit]
Description=Codex Dominion Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/codexdominion
ExecStart=/usr/bin/node /var/www/codexdominion/server.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000
Environment=HOSTNAME=0.0.0.0

[Install]
WantedBy=multi-user.target
"@

Set-Content -Path "$packageDir\codexdominion.service" -Value $serviceFile
Write-Host "  Created systemd service file" -ForegroundColor Gray

# Create nginx configuration
$nginxConfig = @"
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
        proxy_cache_bypass `$http_upgrade;
    }
}
"@

Set-Content -Path "$packageDir\nginx-codexdominion.conf" -Value $nginxConfig
Write-Host "  Created nginx configuration" -ForegroundColor Gray

# Create deployment instructions
$deployInstructions = @'
# Codex Dominion - IONOS Deployment Instructions

## Server Information
- IP Address: 74.208.123.158
- Domain: CodexDominion.app
- Deployment Directory: /var/www/codexdominion

## Step 1: Upload Files to IONOS Server

### Option A: Using SCP (Recommended)
tar -czf codexdominion-frontend.tar.gz ionos_deployment_package/
scp codexdominion-frontend.tar.gz root@74.208.123.158:/tmp/

### Option B: Using SFTP
sftp root@74.208.123.158
put -r ionos_deployment_package /tmp/
exit

## Step 2: SSH into IONOS Server
ssh root@74.208.123.158

## Step 3: Deploy on Server

### Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

### Extract and Setup Application
cd /tmp
tar -xzf codexdominion-frontend.tar.gz
sudo mkdir -p /var/www/codexdominion
sudo cp -r ionos_deployment_package/* /var/www/codexdominion/
sudo chown -R www-data:www-data /var/www/codexdominion
sudo chmod +x /var/www/codexdominion/start.sh

### Setup Systemd Service
sudo cp /var/www/codexdominion/codexdominion.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable codexdominion
sudo systemctl start codexdominion
sudo systemctl status codexdominion

### Setup Nginx
sudo apt-get install -y nginx
sudo cp /var/www/codexdominion/nginx-codexdominion.conf /etc/nginx/sites-available/codexdominion
sudo ln -s /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

## Step 4: Configure DNS
In IONOS DNS Manager:
1. A Record: @ -> 74.208.123.158
2. CNAME: www -> CodexDominion.app

## Step 5: Setup SSL
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d CodexDominion.app -d www.CodexDominion.app

## Verification
curl http://localhost:3000
sudo journalctl -u codexdominion -f
'@

Set-Content -Path "$packageDir\DEPLOYMENT_INSTRUCTIONS.md" -Value $deployInstructions
Write-Host "  Created deployment instructions" -ForegroundColor Gray

# Create tarball
Write-Host "`n📦 Creating deployment archive..." -ForegroundColor Cyan
if (Get-Command tar -ErrorAction SilentlyContinue) {
    tar -czf "codexdominion-frontend-deployment.tar.gz" $packageDir
    Write-Host "✅ Created codexdominion-frontend-deployment.tar.gz" -ForegroundColor Green
} else {
    Write-Host "⚠️  tar command not found. Skipping archive creation." -ForegroundColor Yellow
    Write-Host "   You can manually zip the $packageDir folder" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "✅ Deployment Package Ready!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan

Write-Host "`nPackage Location: $packageDir" -ForegroundColor Cyan
Write-Host "Archive: codexdominion-frontend-deployment.tar.gz" -ForegroundColor Cyan

Write-Host "`n📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review: $packageDir\DEPLOYMENT_INSTRUCTIONS.md" -ForegroundColor White
Write-Host "2. Upload archive to IONOS server (74.208.123.158)" -ForegroundColor White
Write-Host "3. Follow deployment instructions to setup systemd & nginx" -ForegroundColor White
Write-Host "4. Configure DNS to point $DOMAIN to $IONOS_SERVER" -ForegroundColor White

Write-Host "`n🚀 Quick Deploy Command:" -ForegroundColor Cyan
Write-Host "   scp codexdominion-frontend-deployment.tar.gz ${IONOS_USER}@${IONOS_SERVER}:/tmp/" -ForegroundColor White

Write-Host "`n🔗 IONOS SSH:" -ForegroundColor Cyan
Write-Host "   ssh ${IONOS_USER}@${IONOS_SERVER}" -ForegroundColor White
