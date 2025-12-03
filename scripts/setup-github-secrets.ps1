#!/usr/bin/env pwsh
# Script to prepare GitHub Secrets for Multi-Cloud Deployment

Write-Host "`n🔐 GitHub Secrets Setup for CodexDominion Multi-Cloud Deployment" -ForegroundColor Cyan
Write-Host "=" * 70

# 1. IONOS SSH Key
Write-Host "`n1️⃣ IONOS_SSH_KEY" -ForegroundColor Yellow
Write-Host "=" * 70
$privateKey = Get-Content "$HOME\.ssh\ionos_codexdominion" -Raw
Set-Clipboard -Value $privateKey
Write-Host "✅ Private key copied to clipboard!" -ForegroundColor Green
Write-Host ""
Write-Host "Secret Name: IONOS_SSH_KEY" -ForegroundColor White
Write-Host "Secret Value: [Copied to clipboard - paste with Ctrl+V]" -ForegroundColor Gray
Write-Host ""

# 2. DOCKERHUB_TOKEN
Write-Host "`n2️⃣ DOCKERHUB_TOKEN" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host "Docker Hub account: jmerritt48" -ForegroundColor White
Write-Host ""
Write-Host "To create a token:" -ForegroundColor Gray
Write-Host "  1. Go to: https://hub.docker.com/settings/security" -ForegroundColor Cyan
Write-Host "  2. Click 'New Access Token'" -ForegroundColor Gray
Write-Host "  3. Description: CodexDominion GitHub Actions" -ForegroundColor Gray
Write-Host "  4. Permissions: Read, Write, Delete" -ForegroundColor Gray
Write-Host "  5. Copy the token" -ForegroundColor Gray
Write-Host ""
Write-Host "Secret Name: DOCKERHUB_TOKEN" -ForegroundColor White
Write-Host "Secret Value: [Your Docker Hub access token]" -ForegroundColor Gray
Write-Host ""

# 3. DOCKERHUB_USERNAME
Write-Host "`n3️⃣ DOCKERHUB_USERNAME" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host "Secret Name: DOCKERHUB_USERNAME" -ForegroundColor White
Write-Host "Secret Value: jmerritt48" -ForegroundColor White
Write-Host ""

# 4. AZURE_CREDENTIALS
Write-Host "`n4️⃣ AZURE_CREDENTIALS" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host "To create Azure Service Principal:" -ForegroundColor Gray
Write-Host "  Run this command in Azure CLI:" -ForegroundColor Gray
Write-Host ""
Write-Host "  az ad sp create-for-rbac --name 'codexdominion-github' ``" -ForegroundColor Cyan
Write-Host "    --role contributor ``" -ForegroundColor Cyan
Write-Host "    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID ``" -ForegroundColor Cyan
Write-Host "    --sdk-auth" -ForegroundColor Cyan
Write-Host ""
Write-Host "Secret Name: AZURE_CREDENTIALS" -ForegroundColor White
Write-Host "Secret Value: [JSON output from above command]" -ForegroundColor Gray
Write-Host ""

# GitHub URL
Write-Host "`n🌐 Add secrets at:" -ForegroundColor Yellow
Write-Host "   https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "`n📝 Summary - Add these 4 secrets:" -ForegroundColor Yellow
Write-Host "=" * 70
Write-Host "  1. IONOS_SSH_KEY       - ✅ In clipboard" -ForegroundColor Green
Write-Host "  2. DOCKERHUB_TOKEN     - Create at hub.docker.com" -ForegroundColor White
Write-Host "  3. DOCKERHUB_USERNAME  - jmerritt48" -ForegroundColor White
Write-Host "  4. AZURE_CREDENTIALS   - Run az ad sp command" -ForegroundColor White
Write-Host ""

Write-Host "💡 After adding secrets, your GitHub Actions workflow will be ready!" -ForegroundColor Cyan
Write-Host ""

# Offer to open GitHub
$response = Read-Host "Open GitHub Secrets page in browser? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Start-Process "https://github.com/JermaineMerritt-ai/codexdominion-schemas/settings/secrets/actions"
}

Write-Host "`n✨ Next: Run setup script on IONOS server" -ForegroundColor Yellow
Write-Host "   ssh -i `$HOME\.ssh\ionos_codexdominion root@74.208.123.158" -ForegroundColor Cyan
Write-Host "   Then upload and run: scripts/setup-ionos-server.sh" -ForegroundColor Cyan
Write-Host ""
