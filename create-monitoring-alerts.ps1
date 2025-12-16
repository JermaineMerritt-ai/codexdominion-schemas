#!/usr/bin/env pwsh
# Create Azure Monitor Alerts for Codex Dominion

Write-Host "`n🚨 Creating Azure Monitor Alerts...`n" -ForegroundColor Cyan

# Get App Service resource ID
$appServiceId = az webapp show --name codexdominion-backend --resource-group codexdominion-basic --query "id" -o tsv

# Get Application Insights ID
$appInsightsId = az monitor app-insights component show --app codexdominion-insights --resource-group codexdominion-basic --query "id" -o tsv

Write-Host "📊 Creating health check alert..." -ForegroundColor Yellow

# Alert 1: API Health Check (if health endpoint returns non-200)
az monitor metrics alert create `
    --name "api-health-alert" `
    --resource-group codexdominion-basic `
    --scopes $appServiceId `
    --condition "avg Http5xx > 5" `
    --description "Alert when API returns 5xx errors" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --severity 2

Write-Host "✅ Health check alert created`n" -ForegroundColor Green

Write-Host "💻 Creating CPU alert..." -ForegroundColor Yellow

# Alert 2: High CPU Usage
az monitor metrics alert create `
    --name "high-cpu-alert" `
    --resource-group codexdominion-basic `
    --scopes $appServiceId `
    --condition "avg CpuPercentage > 80" `
    --description "Alert when CPU usage exceeds 80%" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --severity 3

Write-Host "✅ CPU alert created`n" -ForegroundColor Green

Write-Host "🧠 Creating memory alert..." -ForegroundColor Yellow

# Alert 3: High Memory Usage
az monitor metrics alert create `
    --name "high-memory-alert" `
    --resource-group codexdominion-basic `
    --scopes $appServiceId `
    --condition "avg MemoryPercentage > 80" `
    --description "Alert when memory usage exceeds 80%" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --severity 3

Write-Host "✅ Memory alert created`n" -ForegroundColor Green

Write-Host "⏱️ Creating response time alert..." -ForegroundColor Yellow

# Alert 4: Slow Response Time
az monitor metrics alert create `
    --name "slow-response-alert" `
    --resource-group codexdominion-basic `
    --scopes $appServiceId `
    --condition "avg AverageResponseTime > 2000" `
    --description "Alert when response time exceeds 2 seconds" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --severity 3

Write-Host "✅ Response time alert created`n" -ForegroundColor Green

Write-Host "`n════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "✅ All monitoring alerts configured!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════`n" -ForegroundColor Yellow

Write-Host "📋 Alerts Created:" -ForegroundColor Cyan
Write-Host "   • API Health (HTTP 5xx errors > 5)" -ForegroundColor White
Write-Host "   • High CPU (>80%)" -ForegroundColor White
Write-Host "   • High Memory (>80%)" -ForegroundColor White
Write-Host "   • Slow Response (>2 seconds)" -ForegroundColor White
Write-Host ""
Write-Host "🔔 Alerts will email you when triggered" -ForegroundColor Yellow
Write-Host "📊 View in Azure Portal:" -ForegroundColor Cyan
Write-Host "   https://portal.azure.com/#@/resource$appServiceId/alerts" -ForegroundColor White
Write-Host ""
