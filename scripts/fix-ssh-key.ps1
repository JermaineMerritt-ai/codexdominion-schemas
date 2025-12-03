#!/usr/bin/env pwsh
# Script to properly add SSH key to IONOS server

Write-Host "`n🔧 Fix SSH Key on IONOS Server" -ForegroundColor Cyan
Write-Host "=" * 60

# Get the public key
$pubKey = Get-Content "$HOME\.ssh\ionos_codexdominion.pub"

Write-Host "`n📋 Your public key:" -ForegroundColor Yellow
Write-Host $pubKey -ForegroundColor White

Write-Host "`n📝 Copy this command and run it on your IONOS server:" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Gray

$sshCommand = @"
mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$pubKey' > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && cat ~/.ssh/authorized_keys
"@

Write-Host $sshCommand -ForegroundColor Green

Write-Host "=" * 60 -ForegroundColor Gray

Write-Host "`n💡 Steps:" -ForegroundColor Yellow
Write-Host "  1. Copy the green command above" -ForegroundColor Gray
Write-Host "  2. Connect to IONOS: ssh root@74.208.123.158" -ForegroundColor Gray
Write-Host "  3. Paste and run the command" -ForegroundColor Gray
Write-Host "  4. Verify you see your key printed" -ForegroundColor Gray
Write-Host "  5. Type 'exit' to disconnect" -ForegroundColor Gray
Write-Host "  6. Test: ssh -i `$HOME\.ssh\ionos_codexdominion root@74.208.123.158" -ForegroundColor Gray

Write-Host "`n✨ Or run this single command to do it all:" -ForegroundColor Cyan
$oneLiner = "ssh root@74.208.123.158 `"mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$pubKey' > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && cat ~/.ssh/authorized_keys`""
Write-Host $oneLiner -ForegroundColor Magenta

Write-Host "`n"
