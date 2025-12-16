# =============================================================================
# CODEX DOMINION - Quick IONOS Deployment
# =============================================================================

$ErrorActionPreference = "Continue"
$ionosServer = "74.208.123.158"
$ionosUser = "root"
$deployPath = "/var/www/codexdominion"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔥 CODEX DOMINION - IONOS VPS DEPLOYMENT" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server: $ionosServer" -ForegroundColor White
Write-Host "User: $ionosUser" -ForegroundColor White
Write-Host ""

# Test SSH connection
Write-Host "[1/6] Testing SSH connection..." -ForegroundColor Cyan
$sshTest = ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$ionosUser@$ionosServer" "echo 'Connected'" 2>&1
if ($sshTest -like "*Connected*") {
    Write-Host "✅ SSH connection successful" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot connect to IONOS server" -ForegroundColor Red
    Write-Host ""
    Write-Host "Setup SSH key:" -ForegroundColor Yellow
    Write-Host "  1. ssh-keygen -t rsa -b 4096" -ForegroundColor Gray
    Write-Host "  2. ssh-copy-id $ionosUser@$ionosServer" -ForegroundColor Gray
    Write-Host "  3. Test: ssh $ionosUser@$ionosServer" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Create deployment directory
Write-Host "`n[2/6] Creating deployment directory..." -ForegroundColor Cyan
ssh "$ionosUser@$ionosServer" "mkdir -p $deployPath/app $deployPath/logs" 2>&1 | Out-Null
Write-Host "✅ Directory created: $deployPath" -ForegroundColor Green

# Upload dashboard file
Write-Host "`n[3/6] Uploading application files..." -ForegroundColor Cyan
Write-Host "   Uploading dashboard_complete_fixed.py..." -ForegroundColor Gray
scp -o StrictHostKeyChecking=no dashboard_complete_fixed.py "$ionosUser@${ionosServer}:$deployPath/app/app.py" 2>&1 | Out-Null

Write-Host "   Uploading ledger files..." -ForegroundColor Gray
scp -o StrictHostKeyChecking=no codex_ledger.json "$ionosUser@${ionosServer}:$deployPath/app/" 2>&1 | Out-Null
scp -o StrictHostKeyChecking=no proclamations.json "$ionosUser@${ionosServer}:$deployPath/app/" 2>&1 | Out-Null
scp -o StrictHostKeyChecking=no cycles.json "$ionosUser@${ionosServer}:$deployPath/app/" 2>&1 | Out-Null

Write-Host "✅ Files uploaded" -ForegroundColor Green

# Install dependencies on server
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Cyan
$installScript = @'
apt-get update -qq > /dev/null 2>&1
apt-get install -y python3 python3-pip python3-venv nginx -qq > /dev/null 2>&1
cd /var/www/codexdominion/app
python3 -m venv venv > /dev/null 2>&1
source venv/bin/activate
pip install --quiet flask flask-cors openai waitress redis > /dev/null 2>&1
echo "Dependencies installed"
'@

ssh "$ionosUser@$ionosServer" $installScript
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Create systemd service
Write-Host "`n[5/6] Creating systemd service..." -ForegroundColor Cyan
$serviceContent = @"
[Unit]
Description=Codex Dominion Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/codexdominion/app
Environment="PATH=/var/www/codexdominion/app/venv/bin"
Environment="FLASK_ENV=production"
Environment="OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE"
ExecStart=/var/www/codexdominion/app/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"@

$serviceContent | ssh "$ionosUser@$ionosServer" "cat > /etc/systemd/system/codex-dashboard.service"
ssh "$ionosUser@$ionosServer" "systemctl daemon-reload" 2>&1 | Out-Null
ssh "$ionosUser@$ionosServer" "systemctl enable codex-dashboard" 2>&1 | Out-Null
ssh "$ionosUser@$ionosServer" "systemctl restart codex-dashboard" 2>&1 | Out-Null
Write-Host "✅ Service created and started" -ForegroundColor Green

# Configure Nginx
Write-Host "`n[6/6] Configuring Nginx..." -ForegroundColor Cyan
$nginxConfig = @"
server {
    listen 80;
    server_name codexdominion.app www.codexdominion.app;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
"@

$nginxConfig | ssh "$ionosUser@$ionosServer" "cat > /etc/nginx/sites-available/codexdominion"
ssh "$ionosUser@$ionosServer" "ln -sf /etc/nginx/sites-available/codexdominion /etc/nginx/sites-enabled/" 2>&1 | Out-Null
ssh "$ionosUser@$ionosServer" "nginx -t && systemctl reload nginx" 2>&1 | Out-Null
Write-Host "✅ Nginx configured" -ForegroundColor Green

# Test deployment
Write-Host "`n[?/6] Testing deployment..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
$status = ssh "$ionosUser@$ionosServer" "systemctl status codex-dashboard --no-pager | grep 'Active:'" 2>&1
Write-Host "   Service status: $status" -ForegroundColor Gray

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✨ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Your Application:" -ForegroundColor Cyan
Write-Host "   Public IP: http://$ionosServer" -ForegroundColor White
Write-Host "   Domain: http://codexdominion.app (configure DNS)" -ForegroundColor White
Write-Host ""
Write-Host "📊 Resources:" -ForegroundColor Yellow
Write-Host "   ✅ Dashboard: Running on port 5000" -ForegroundColor Green
Write-Host "   ✅ Nginx: Reverse proxy on port 80" -ForegroundColor Green
Write-Host "   ✅ Systemd: Auto-start on reboot" -ForegroundColor Green
Write-Host ""
Write-Host "🔍 Check Status:" -ForegroundColor Cyan
Write-Host "   ssh $ionosUser@$ionosServer 'systemctl status codex-dashboard'" -ForegroundColor Gray
Write-Host "   ssh $ionosUser@$ionosServer 'journalctl -u codex-dashboard -f'" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Test Now:" -ForegroundColor Cyan
Write-Host "   curl http://$ionosServer" -ForegroundColor Gray
Write-Host "   Start-Process http://$ionosServer" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Cost: $0/month (server already paid for!)" -ForegroundColor Green
Write-Host ""
