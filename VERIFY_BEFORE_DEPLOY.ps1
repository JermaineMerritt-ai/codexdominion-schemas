#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Pre-Deployment Verification - Test local system before cloud deployment
#>

Write-Host ""
Write-Host "🔍 PRE-DEPLOYMENT VERIFICATION" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Test Flask Backend
Write-Host "1️⃣  Testing Flask Backend (localhost:5000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Flask is responding" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Flask returned status $($response.StatusCode)" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "   ❌ Flask is NOT responding" -ForegroundColor Red
    Write-Host "      Error: $($_.Exception.Message)" -ForegroundColor DarkRed
    $allGood = $false
}

Write-Host ""

# Test Next.js Frontend
Write-Host "2️⃣  Testing Next.js Frontend (localhost:3003)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3003" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Next.js is responding" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Next.js returned status $($response.StatusCode)" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "   ❌ Next.js is NOT responding" -ForegroundColor Red
    Write-Host "      Error: $($_.Exception.Message)" -ForegroundColor DarkRed
    $allGood = $false
}

Write-Host ""

# Test Database
Write-Host "3️⃣  Testing Database..." -ForegroundColor Yellow
if (Test-Path "codex.db") {
    $dbSize = (Get-Item "codex.db").Length / 1KB
    Write-Host "   ✅ Database exists ($([math]::Round($dbSize, 2)) KB)" -ForegroundColor Green
    
    # Test database connection
    try {
        $result = & .\.venv\Scripts\python.exe -c "from db import engine; from models import Base; print('OK')" 2>&1
        if ($result -match "OK") {
            Write-Host "   ✅ Database connection OK" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Database connection issue" -ForegroundColor Yellow
            $allGood = $false
        }
    } catch {
        Write-Host "   ❌ Database connection failed" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "   ⚠️  Database file not found" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host ""

# Check environment files
Write-Host "4️⃣  Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env.production") {
    Write-Host "   ✅ .env.production exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  .env.production not found" -ForegroundColor Yellow
    Write-Host "      Run: Copy-Item .env.3cloud.example .env.production" -ForegroundColor DarkGray
}

Write-Host ""

# Check CLI tools
Write-Host "5️⃣  Checking deployment tools..." -ForegroundColor Yellow

$azInstalled = Get-Command az -ErrorAction SilentlyContinue
if ($azInstalled) {
    Write-Host "   ✅ Azure CLI installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Azure CLI not installed" -ForegroundColor Yellow
    Write-Host "      Install: winget install Microsoft.AzureCLI" -ForegroundColor DarkGray
}

$gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
if ($gcloudInstalled) {
    Write-Host "   ✅ Google Cloud SDK installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Google Cloud SDK not installed" -ForegroundColor Yellow
    Write-Host "      Install: https://cloud.google.com/sdk/docs/install" -ForegroundColor DarkGray
}

$sshInstalled = Get-Command ssh -ErrorAction SilentlyContinue
if ($sshInstalled) {
    Write-Host "   ✅ SSH installed" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  SSH not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✅ SYSTEM READY FOR DEPLOYMENT!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Configure .env.production with your cloud credentials" -ForegroundColor White
    Write-Host "2. Run: .\DEPLOY_3_CLOUD_PRODUCTION.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "⚠️  SOME ISSUES DETECTED" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Fix the issues above, then run this script again." -ForegroundColor White
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
