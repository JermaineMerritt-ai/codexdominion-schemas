# Quick Deploy - Codex Master Dashboard to Azure App Service
# This is faster and cheaper than Container Instances

Write-Host "`n🔥 QUICK DEPLOY - MASTER DASHBOARD`n" -ForegroundColor Magenta

# Configuration
$ResourceGroup = "codexdominion-basic"
$AppServicePlan = "codex-dashboard-plan"
$WebAppName = "codex-master-dashboard"
$Location = "westus2"

Write-Host "📦 Step 1: Creating App Service Plan (FREE tier)...`n" -ForegroundColor Cyan
az appservice plan create `
    --name $AppServicePlan `
    --resource-group $ResourceGroup `
    --location $Location `
    --sku F1 `
    --is-linux

Write-Host "`n🚀 Step 2: Creating Web App for Containers...`n" -ForegroundColor Cyan
az webapp create `
    --resource-group $ResourceGroup `
    --plan $AppServicePlan `
    --name $WebAppName `
    --deployment-container-image-name "python:3.10-slim"

Write-Host "`n⚙️  Step 3: Configuring startup command...`n" -ForegroundColor Cyan
az webapp config set `
    --resource-group $ResourceGroup `
    --name $WebAppName `
    --startup-file "streamlit run codex_master_dashboard.py --server.port=8000 --server.address=0.0.0.0 --server.headless=true"

Write-Host "`n📦 Step 4: Deploying code...`n" -ForegroundColor Cyan

# Create deployment package
Compress-Archive -Path "codex_master_dashboard.py","codex_multi_cycle_orchestrator.py","codex_ledger.json","accounts.json","proclamations.json","cycles.json","dashboard-requirements.txt" -DestinationPath "dashboard-deploy.zip" -Force

# Rename requirements for Azure
Copy-Item "dashboard-requirements.txt" "requirements.txt" -Force
Compress-Archive -Path "codex_master_dashboard.py","codex_multi_cycle_orchestrator.py","codex_ledger.json","accounts.json","proclamations.json","cycles.json","requirements.txt" -DestinationPath "dashboard-deploy.zip" -Force -Update

az webapp deploy `
    --resource-group $ResourceGroup `
    --name $WebAppName `
    --src-path "dashboard-deploy.zip" `
    --type zip

Write-Host "`n✅ DEPLOYMENT COMPLETE!`n" -ForegroundColor Green
Write-Host "🌐 Your Master Dashboard URL:`n" -ForegroundColor Cyan
Write-Host "   https://${WebAppName}.azurewebsites.net`n" -ForegroundColor White
Write-Host "⏳ Note: First load may take 2-3 minutes to start up`n" -ForegroundColor Yellow
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Magenta
