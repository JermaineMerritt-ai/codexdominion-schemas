#!/usr/bin/env pwsh
# Test SSH Connection to IONOS Server

Write-Host "`n🔐 IONOS SSH Connection Test" -ForegroundColor Cyan
Write-Host "=" * 60

$IONOS_SERVER = "74.208.123.158"
$SSH_KEY = "$HOME\.ssh\ionos_codexdominion"

Write-Host "`n1️⃣ Testing SSH connection..." -ForegroundColor Yellow
Write-Host "Command: ssh -i $SSH_KEY root@$IONOS_SERVER" -ForegroundColor Gray
Write-Host ""

# Test connection
ssh -i $SSH_KEY -o StrictHostKeyChecking=no root@$IONOS_SERVER @"
echo '✅ SSH Connection Successful!'
echo ''
echo '📊 Server Information:'
echo '  Hostname: `$(hostname)'
echo '  OS: `$(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')'
echo '  Kernel: `$(uname -r)'
echo ''
echo '🔍 Checking installed software:'
echo -n '  Docker: '
if command -v docker &> /dev/null; then docker --version; else echo 'Not installed'; fi
echo -n '  Nginx: '
if command -v nginx &> /dev/null; then nginx -v 2>&1; else echo 'Not installed'; fi
echo -n '  Certbot: '
if command -v certbot &> /dev/null; then certbot --version 2>&1 | head -1; else echo 'Not installed'; fi
echo ''
echo '💾 Disk Space:'
df -h / | tail -1
echo ''
echo '🧠 Memory:'
free -h | grep Mem
echo ''
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! Passwordless SSH is working!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. ✅ SSH key configured"
    Write-Host "  2. ☐ Copy private key to GitHub secrets"
    Write-Host "  3. ☐ Run server setup script"
    Write-Host "  4. ☐ Purchase domain"
    Write-Host "  5. ☐ Configure DNS"
    Write-Host ""
    Write-Host "🔑 Copy private key to clipboard for GitHub?" -ForegroundColor Yellow
    Write-Host "   (y/n): " -NoNewline
    $response = Read-Host

    if ($response -eq 'y') {
        Get-Content $SSH_KEY | Set-Clipboard
        Write-Host ""
        Write-Host "✅ Private key copied to clipboard!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Now go to:" -ForegroundColor Cyan
        Write-Host "  https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions" -ForegroundColor White
        Write-Host ""
        Write-Host "Add new secret:" -ForegroundColor Cyan
        Write-Host "  Name: IONOS_SSH_KEY" -ForegroundColor White
        Write-Host "  Value: Paste from clipboard (Ctrl+V)" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "❌ SSH connection failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Make sure you ran the commands on the IONOS server"
    Write-Host "  2. Check authorized_keys file on server:"
    Write-Host "     ssh root@$IONOS_SERVER 'cat ~/.ssh/authorized_keys'"
    Write-Host "  3. Try manual SSH:"
    Write-Host "     ssh -i $SSH_KEY root@$IONOS_SERVER"
}
