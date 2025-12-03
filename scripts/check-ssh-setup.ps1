#!/usr/bin/env pwsh
# SSH Setup Diagnostic Script

Write-Host "`n🔍 SSH Setup Diagnostics" -ForegroundColor Cyan
Write-Host "=" * 60

# 1. Check local public key
Write-Host "`n1️⃣ Local public key:" -ForegroundColor Yellow
$pubKey = Get-Content "$HOME\.ssh\ionos_codexdominion.pub"
Write-Host $pubKey -ForegroundColor White

# 2. Check private key permissions
Write-Host "`n2️⃣ Private key permissions:" -ForegroundColor Yellow
$privKey = "$HOME\.ssh\ionos_codexdominion"
if (Test-Path $privKey) {
    Write-Host "✅ Private key exists at: $privKey" -ForegroundColor Green
    $perms = icacls $privKey 2>&1 | Out-String
    if ($perms -match "JMerr") {
        Write-Host "✅ Permissions look correct" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Permissions might need adjustment" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Private key not found!" -ForegroundColor Red
}

# 3. Test SSH with verbose output
Write-Host "`n3️⃣ Testing SSH connection with verbose output..." -ForegroundColor Yellow
Write-Host "This will show detailed SSH debug information." -ForegroundColor Gray
Write-Host "Press Ctrl+C if it hangs." -ForegroundColor Gray
Write-Host ""

$sshCmd = "ssh -v -i `"$HOME\.ssh\ionos_codexdominion`" root@74.208.123.158 'cat ~/.ssh/authorized_keys'"
Write-Host "Command: $sshCmd" -ForegroundColor Cyan
Write-Host ""

# Run with verbose to see what's happening
ssh -v -i "$HOME\.ssh\ionos_codexdominion" root@74.208.123.158 "cat ~/.ssh/authorized_keys"

Write-Host "`n" -ForegroundColor White
Write-Host "=" * 60
Write-Host "`n📝 Common Issues:" -ForegroundColor Yellow
Write-Host "  1. If you see 'Publickey failed' - key not on server" -ForegroundColor Gray
Write-Host "  2. If you see 'Permission denied' - wrong permissions" -ForegroundColor Gray
Write-Host "  3. If you see password prompt - key not recognized" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  If the authorized_keys content shows above, compare it with your public key" -ForegroundColor Gray
Write-Host "  They should match exactly (including the github@codexdominion.app at the end)" -ForegroundColor Gray
Write-Host ""
