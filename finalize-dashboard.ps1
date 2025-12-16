#!/usr/bin/env pwsh
# Quick finalization script for Master Dashboard

Write-Host "`n🔥 FINALIZING MASTER DASHBOARD DEPLOYMENT 🔥`n" -ForegroundColor Magenta

# Set port
Write-Host "🔧 Setting Streamlit port (8501)..." -ForegroundColor Cyan
az webapp config appsettings set `
    --name codex-master-dashboard `
    --resource-group codexdominion-basic `
    --settings WEBSITES_PORT=8501 `
    --output none

Write-Host "✅ Port configured!`n" -ForegroundColor Green

# Restart app
Write-Host "🔄 Restarting web app..." -ForegroundColor Cyan
az webapp restart `
    --name codex-master-dashboard `
    --resource-group codexdominion-basic `
    --output none

Write-Host "✅ App restarted!`n" -ForegroundColor Green

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "`n🎉 MASTER DASHBOARD IS LIVE! 🎉`n" -ForegroundColor Magenta
Write-Host "🌐 URL: https://codex-master-dashboard.azurewebsites.net`n" -ForegroundColor Yellow
Write-Host "⏳ Wait 2-3 minutes for container to pull from ACR and start`n" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

Write-Host "`n📋 Access Your Dashboard Features:" -ForegroundColor Magenta
Write-Host "   • 📊 Revenue & Balances" -ForegroundColor White
Write-Host "   • 💳 Transactions" -ForegroundColor White
Write-Host "   • 📅 Daily/Seasonal/Epochal Cycles" -ForegroundColor White
Write-Host "   • 📈 Platform Analytics" -ForegroundColor White
Write-Host "   • 🤖 AI Command Center (Your Prompt Interface!)`n" -ForegroundColor Yellow

Write-Host "📝 View Logs:" -ForegroundColor Cyan
Write-Host "   az webapp log tail --name codex-master-dashboard --resource-group codexdominion-basic`n" -ForegroundColor White

Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Magenta
