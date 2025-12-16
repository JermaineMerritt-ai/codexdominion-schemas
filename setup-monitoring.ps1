# Azure Monitoring & Alerts Setup Script
# Creates action groups and metric alerts for Codex Dominion

$ErrorActionPreference = "Stop"

Write-Host "`n[Step 2/4] Setting Up Azure Monitoring & Alerts...`n" -ForegroundColor Cyan

# Configuration
$RG = "codex-rg"
$LOCATION = "eastus2"
$ACTION_GROUP = "codex-alerts"
$EMAIL = "MerrittMethod47@outlook.com"

# Create Action Group (for alert notifications)
Write-Host "Creating action group for notifications..." -ForegroundColor Yellow
az monitor action-group create `
    --name $ACTION_GROUP `
    --resource-group $RG `
    --short-name "CodexAlert" `
    --action email Admin $EMAIL `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Action group created: $ACTION_GROUP" -ForegroundColor Green
} else {
    Write-Host "⚠️  Action group may already exist" -ForegroundColor Yellow
}

# Get Container Instance resource ID
$containerId = az container show --resource-group $RG --name codex-backend --query id -o tsv

# Create CPU Alert
Write-Host "Creating CPU usage alert..." -ForegroundColor Yellow
az monitor metrics alert create `
    --name "codex-backend-high-cpu" `
    --resource-group $RG `
    --scopes $containerId `
    --condition "avg CpuUsage > 0.8" `
    --description "Alert when CPU usage exceeds 80%" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --action $ACTION_GROUP `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ CPU alert created" -ForegroundColor Green
} else {
    Write-Host "⚠️  CPU alert may already exist" -ForegroundColor Yellow
}

# Create Memory Alert
Write-Host "Creating memory usage alert..." -ForegroundColor Yellow
az monitor metrics alert create `
    --name "codex-backend-high-memory" `
    --resource-group $RG `
    --scopes $containerId `
    --condition "avg MemoryUsage > 858993459" `
    --description "Alert when memory usage exceeds 819MB (80% of 1GB)" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --action $ACTION_GROUP `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Memory alert created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Memory alert may already exist" -ForegroundColor Yellow
}

Write-Host "`n✅ Monitoring setup complete!" -ForegroundColor Green
Write-Host "   Email notifications will be sent to: $EMAIL" -ForegroundColor Gray
Write-Host ""
