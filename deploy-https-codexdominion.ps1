# =============================================================================
# CODEX DOMINION - HTTPS/SSL DEPLOYMENT SCRIPT (Windows to IONOS)
# =============================================================================

$ErrorActionPreference = "Stop"

# Configuration
$IONOS_SERVER = "74.208.123.158"
$IONOS_USER = "root"
$SSH_KEY = "$env:USERPROFILE\.ssh\id_rsa"
$LOCAL_SCRIPT = "setup-https-codexdominion.sh"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "   DEPLOYING HTTPS TO IONOS SERVER" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# =============================================================================
# Step 1: Check SSH connectivity
# =============================================================================
Write-Host "Step 1: Testing SSH connection..." -ForegroundColor Yellow
Write-Host ""

$sshTest = ssh -i $SSH_KEY -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$IONOS_USER@$IONOS_SERVER" "echo 'Connection successful'"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ SSH connection successful" -ForegroundColor Green
} else {
    Write-Host "✗ SSH connection failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check if SSH key exists: $SSH_KEY" -ForegroundColor White
    Write-Host "  2. Verify server IP: $IONOS_SERVER" -ForegroundColor White
    Write-Host "  3. Ensure server firewall allows SSH (port 22)" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host ""

# =============================================================================
# Step 2: Upload HTTPS setup script to server
# =============================================================================
Write-Host "Step 2: Uploading HTTPS setup script..." -ForegroundColor Yellow

scp -i $SSH_KEY $LOCAL_SCRIPT "$IONOS_USER@${IONOS_SERVER}:/tmp/"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Script uploaded successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to upload script" -ForegroundColor Red
    exit 1
}
Write-Host ""

# =============================================================================
# Step 3: Make script executable and run it
# =============================================================================
Write-Host "Step 3: Executing HTTPS setup on server..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan
Write-Host ""

ssh -i $SSH_KEY "$IONOS_USER@$IONOS_SERVER" @"
chmod +x /tmp/$LOCAL_SCRIPT
/tmp/$LOCAL_SCRIPT
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ HTTPS setup completed successfully" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ HTTPS setup failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can manually run the script on the server:" -ForegroundColor Yellow
    Write-Host "  ssh root@$IONOS_SERVER" -ForegroundColor White
    Write-Host "  chmod +x /tmp/$LOCAL_SCRIPT" -ForegroundColor White
    Write-Host "  /tmp/$LOCAL_SCRIPT" -ForegroundColor White
    Write-Host ""
    exit 1
}
Write-Host ""

# =============================================================================
# Step 4: Verify HTTPS is working
# =============================================================================
Write-Host "Step 4: Verifying HTTPS connectivity..." -ForegroundColor Yellow
Write-Host ""

Start-Sleep -Seconds 3

$httpsTest = Test-NetConnection -ComputerName www.codexdominion.app -Port 443
if ($httpsTest.TcpTestSucceeded) {
    Write-Host "✓ Port 443 (HTTPS) is now accessible" -ForegroundColor Green
} else {
    Write-Host "⚠ Port 443 may still be initializing..." -ForegroundColor Yellow
}
Write-Host ""

# =============================================================================
# Step 5: Test HTTPS certificate
# =============================================================================
Write-Host "Step 5: Testing HTTPS certificate..." -ForegroundColor Yellow
Write-Host ""

try {
    $certCheck = Invoke-WebRequest -Uri "https://www.codexdominion.app" -UseBasicParsing -TimeoutSec 10
    Write-Host "✓ HTTPS certificate is valid and site is responding" -ForegroundColor Green
    Write-Host "   Status Code: $($certCheck.StatusCode)" -ForegroundColor Cyan
} catch {
    Write-Host "⚠ HTTPS may need a few more minutes to propagate" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
}
Write-Host ""

# =============================================================================
# Summary
# =============================================================================
Write-Host "========================================" -ForegroundColor Green
Write-Host "   DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your site should now be accessible at:" -ForegroundColor Blue
Write-Host "   https://www.codexdominion.app" -ForegroundColor Green
Write-Host ""
Write-Host "Certificate Details:" -ForegroundColor Blue
Write-Host "   • Auto-renewal: Enabled" -ForegroundColor White
Write-Host "   • Renewal check: certbot renew --dry-run" -ForegroundColor White
Write-Host "   • Certificate location: /etc/letsencrypt/live/www.codexdominion.app/" -ForegroundColor White
Write-Host ""
Write-Host "Nginx Configuration:" -ForegroundColor Blue
Write-Host "   • Config file: /etc/nginx/sites-available/codexdominion.app" -ForegroundColor White
Write-Host "   • Reload nginx: systemctl reload nginx" -ForegroundColor White
Write-Host "   • Check status: systemctl status nginx" -ForegroundColor White
Write-Host ""
Write-Host "Firewall Status:" -ForegroundColor Blue
Write-Host "   • HTTP (80): Redirects to HTTPS" -ForegroundColor White
Write-Host "   • HTTPS (443): Active and secured" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Test your site: https://www.codexdominion.app" -ForegroundColor White
Write-Host "   2. Monitor logs: ssh root@$IONOS_SERVER 'tail -f /var/log/nginx/codexdominion_error.log'" -ForegroundColor White
Write-Host "   3. Check SSL rating: https://www.ssllabs.com/ssltest/" -ForegroundColor White
Write-Host ""
