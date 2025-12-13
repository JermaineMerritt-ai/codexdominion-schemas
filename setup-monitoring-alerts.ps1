#!/usr/bin/env pwsh
# =============================================================================
# Health Monitoring Alerts Setup
# =============================================================================
# Creates alerts for backend health, performance, and availability

Write-Host "🚨 Setting Up Health Monitoring Alerts" -ForegroundColor Cyan
Write-Host "=" * 60

$resourceGroup = "codex-dominion"
$backendName = "codex-backend-centralus"
$appInsightsName = "codex-insights-centralus"

# Get resource IDs
Write-Host "`n🔍 Getting resource IDs..."
$backendId = az webapp show --name $backendName --resource-group $resourceGroup --query id --output tsv
$appInsightsId = az monitor app-insights component show --app $appInsightsName --resource-group $resourceGroup --query id --output tsv

Write-Host "✅ Backend ID: $backendId"
Write-Host "✅ App Insights ID: $appInsightsId"

# Create action group for email notifications
Write-Host "`n📧 Creating email action group..."
az monitor action-group create `
    --name "CodexAdminAlerts" `
    --resource-group $resourceGroup `
    --short-name "CodexAlert" `
    --email-receiver "admin" "jermaine@codexdominion.app" `
    --output table

# Alert 1: HTTP Server Errors (5xx)
Write-Host "`n⚠️  Creating alert: HTTP 5xx errors..."
az monitor metrics alert create `
    --name "codex-backend-5xx-errors" `
    --resource-group $resourceGroup `
    --scopes $backendId `
    --condition "count Http5xx > 5" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action "CodexAdminAlerts" `
    --description "Alert when backend returns more than 5 server errors in 5 minutes" `
    --severity 2 `
    --output table

# Alert 2: Response Time
Write-Host "`n⏱️  Creating alert: High response time..."
az monitor metrics alert create `
    --name "codex-backend-slow-response" `
    --resource-group $resourceGroup `
    --scopes $backendId `
    --condition "avg ResponseTime > 5000" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action "CodexAdminAlerts" `
    --description "Alert when average response time exceeds 5 seconds" `
    --severity 3 `
    --output table

# Alert 3: CPU High Usage
Write-Host "`n🔥 Creating alert: High CPU usage..."
az monitor metrics alert create `
    --name "codex-backend-high-cpu" `
    --resource-group $resourceGroup `
    --scopes $backendId `
    --condition "avg CpuPercentage > 90" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action "CodexAdminAlerts" `
    --description "Alert when CPU usage exceeds 90% for 5 minutes" `
    --severity 2 `
    --output table

# Alert 4: Memory High Usage
Write-Host "`n💾 Creating alert: High memory usage..."
az monitor metrics alert create `
    --name "codex-backend-high-memory" `
    --resource-group $resourceGroup `
    --scopes $backendId `
    --condition "avg MemoryPercentage > 85" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action "CodexAdminAlerts" `
    --description "Alert when memory usage exceeds 85% for 5 minutes" `
    --severity 2 `
    --output table

Write-Host "`n" + ("=" * 60)
Write-Host "✅ Monitoring Alerts Configured" -ForegroundColor Green
Write-Host "   Email: jermaine@codexdominion.app" -ForegroundColor White
Write-Host "   Alerts:" -ForegroundColor White
Write-Host "     - HTTP 5xx errors (>5 in 5 min)" -ForegroundColor White
Write-Host "     - Slow response (>5 sec avg)" -ForegroundColor White
Write-Host "     - High CPU (>90% for 5 min)" -ForegroundColor White
Write-Host "     - High memory (>85% for 5 min)" -ForegroundColor White
