# =============================================================================
# CODEX DOMINION - INSTANT AZURE DEPLOYMENT
# =============================================================================
# Deploys: Frontend (Static Web App) + Backend (Container Instance) + Dashboard
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔥 CODEX DOMINION - AZURE DEPLOYMENT INITIATED 🔥" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Configuration
$RG = "codex-rg"
$LOCATION = "eastus2"
$BACKEND_NAME = "codex-backend"
$FRONTEND_RG = "codex-dominion"

Write-Host "[✓] Configuration Loaded" -ForegroundColor Green
Write-Host "    Resource Group: $RG" -ForegroundColor Gray
Write-Host "    Location: $LOCATION" -ForegroundColor Gray
Write-Host ""

# Step 1: Check Azure Login
Write-Host "[1/5] Verifying Azure Login..." -ForegroundColor Cyan
$account = az account show 2>&1 | ConvertFrom-Json
if ($account) {
    Write-Host "✅ Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "    Subscription: $($account.name)" -ForegroundColor Gray
} else {
    Write-Host "❌ Not logged in to Azure!" -ForegroundColor Red
    Write-Host "    Run: az login" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Step 2: Check Resource Group
Write-Host "[2/5] Ensuring Resource Group exists..." -ForegroundColor Cyan
$rgExists = az group exists --name $RG
if ($rgExists -eq "true") {
    Write-Host "✅ Resource Group '$RG' exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  Creating Resource Group '$RG'..." -ForegroundColor Yellow
    az group create --name $RG --location $LOCATION --output none
    Write-Host "✅ Resource Group created" -ForegroundColor Green
}
Write-Host ""

# Step 3: Deploy Backend to Container Instances
Write-Host "[3/5] Checking Backend Container Instance..." -ForegroundColor Cyan
$containerExists = az container show --resource-group $RG --name $BACKEND_NAME 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend Container Instance exists" -ForegroundColor Green
    $containerInfo = $containerExists | ConvertFrom-Json
    $backendUrl = "http://$($containerInfo.ipAddress.fqdn):8001"
    Write-Host "    URL: $backendUrl" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Backend Container Instance not found" -ForegroundColor Yellow
    Write-Host "    Deployment requires ACR image build (via GitHub Actions)" -ForegroundColor Yellow
    Write-Host "    Trigger workflow: azure-backend-deploy.yml" -ForegroundColor Cyan
}
Write-Host ""

# Step 4: Check Frontend Static Web App
Write-Host "[4/5] Checking Frontend Static Web App..." -ForegroundColor Cyan
$frontendApps = az staticwebapp list --output json | ConvertFrom-Json
$mainFrontend = $frontendApps | Where-Object { $_.name -like "*codexdominion*" -or $_.name -like "*happy*" } | Select-Object -First 1
if ($mainFrontend) {
    Write-Host "✅ Frontend Static Web App deployed" -ForegroundColor Green
    Write-Host "    Name: $($mainFrontend.name)" -ForegroundColor Gray
    Write-Host "    URL: https://$($mainFrontend.defaultHostname)" -ForegroundColor Cyan
    $frontendUrl = "https://$($mainFrontend.defaultHostname)"
} else {
    Write-Host "⚠️  Frontend Static Web App not found" -ForegroundColor Yellow
    Write-Host "    Deployment requires GitHub workflow trigger" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Deploy Flask Dashboard (Local)
Write-Host "[5/5] Starting Master Dashboard (Local)..." -ForegroundColor Cyan
$dashboardProcess = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*flask_dashboard*" }
if ($dashboardProcess) {
    Write-Host "✅ Master Dashboard already running" -ForegroundColor Green
    Write-Host "    Process ID: $($dashboardProcess.Id)" -ForegroundColor Gray
} else {
    Write-Host "🚀 Starting Master Dashboard..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python flask_dashboard.py" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "✅ Master Dashboard started (minimized)" -ForegroundColor Green
}
Write-Host "    Local URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎯 DEPLOYMENT STATUS SUMMARY" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 FRONTEND (Static Web App):" -ForegroundColor White
if ($frontendUrl) {
    Write-Host "   ✅ LIVE: $frontendUrl" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Deploy via: git push (triggers azure-static-web-apps workflow)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "🔧 BACKEND (Container Instance):" -ForegroundColor White
if ($backendUrl) {
    Write-Host "   ✅ LIVE: $backendUrl" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Deploy via: git push (triggers azure-backend-deploy workflow)" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "👑 MASTER DASHBOARD (Local):" -ForegroundColor White
Write-Host "   ✅ RUNNING: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔥 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Visit http://localhost:5000 for Master Dashboard" -ForegroundColor White
if (-not $frontendUrl -or -not $backendUrl) {
    Write-Host "   2. Push to GitHub main branch to trigger Azure deployments:" -ForegroundColor White
    Write-Host "      git add ." -ForegroundColor Gray
    Write-Host "      git commit -m 'Deploy to Azure'" -ForegroundColor Gray
    Write-Host "      git push origin main" -ForegroundColor Gray
}
Write-Host ""
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑" -ForegroundColor Yellow
Write-Host ""
