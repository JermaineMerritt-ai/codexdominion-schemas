#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick fix for critical deployment blockers
#>

$ErrorActionPreference = "Continue"
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot

Write-Host "`n⚡ QUICK FIX - Critical Deployment Blockers" -ForegroundColor Cyan
Write-Host "=" * 50

# 1. Fix Terraform PATH (immediate)
Write-Host "`n🔧 Fixing Terraform PATH..." -ForegroundColor Yellow
$env:Path = "$PSScriptRoot;$env:Path"
Write-Host "✅ Terraform added to PATH (current session)" -ForegroundColor Green

# 2. Configure GCP
Write-Host "`n☁️  Configuring GCP project..." -ForegroundColor Yellow
$gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
if ($gcloud) {
    gcloud config set project codex-dominion-prod 2>&1 | Out-Null
    Write-Host "✅ GCP project: codex-dominion-prod" -ForegroundColor Green
} else {
    Write-Host "⚠️  gcloud not found - skip" -ForegroundColor Yellow
}

# 3. Generate secure credentials
Write-Host "`n🔐 Generating secure credentials..." -ForegroundColor Yellow
$dbPass = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
$env:TF_VAR_db_pass = $dbPass
Write-Host "✅ Generated secure database password" -ForegroundColor Green

# 4. Save to .env
$envContent = @"
# Auto-generated $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
TF_VAR_db_pass=$dbPass
# TF_VAR_cloudflare_api_token=YOUR_NEW_TOKEN_HERE
"@

$envContent | Out-File -FilePath "$PSScriptRoot\.env" -Encoding utf8 -Force
Write-Host "✅ Saved to .env file" -ForegroundColor Green

# 5. Initialize Terraform
Write-Host "`n🔨 Initializing Terraform..." -ForegroundColor Yellow
Push-Location $PSScriptRoot
if (Test-Path "./terraform.exe") {
    .\terraform.exe init -upgrade 2>&1 | Out-Host
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Terraform initialized" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Terraform init had warnings" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ terraform.exe not found" -ForegroundColor Red
}
Pop-Location

Write-Host "`n🎯 IMMEDIATE ACTIONS NEEDED:" -ForegroundColor Cyan
Write-Host "1. Rotate Cloudflare token: https://dash.cloudflare.com/profile/api-tokens" -ForegroundColor White
Write-Host "   - Delete token: WuKuLdijG-JVTyTqH8SA7K3rOTBOB8DAePOd14On" -ForegroundColor Red
Write-Host "   - Create new token and update .env file" -ForegroundColor White
Write-Host ""
Write-Host "2. Install GitHub CLI (restart PowerShell after):" -ForegroundColor White
Write-Host "   winget install GitHub.cli" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Authenticate:" -ForegroundColor White
Write-Host "   gh auth login" -ForegroundColor Yellow
Write-Host "   gcloud auth login" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Run full setup:" -ForegroundColor White
Write-Host "   .\complete-deployment-setup.ps1" -ForegroundColor Yellow
Write-Host ""
