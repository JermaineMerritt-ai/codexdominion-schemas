#!/usr/bin/env pwsh
# =============================================================================
# Azure Auto-Scaling Configuration Script
# =============================================================================
# Configures auto-scaling rules for Codex Dominion backend

Write-Host "🔧 Configuring Auto-Scaling for Codex Dominion Backend" -ForegroundColor Cyan
Write-Host "=" * 60

$resourceGroup = "codex-dominion"
$autoscaleName = "codex-autoscale"

# Scale Out Rule (CPU > 75%)
Write-Host "`n📈 Creating scale-out rule (CPU > 75%)..."
az monitor autoscale rule create `
    --resource-group $resourceGroup `
    --autoscale-name $autoscaleName `
    --condition "CpuPercentage > 75 avg 5m" `
    --scale out 1 `
    --cooldown 5

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Scale-out rule created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Scale-out rule failed" -ForegroundColor Yellow
}

# Scale In Rule (CPU < 25%)
Write-Host "`n📉 Creating scale-in rule (CPU < 25%)..."
az monitor autoscale rule create `
    --resource-group $resourceGroup `
    --autoscale-name $autoscaleName `
    --condition "CpuPercentage < 25 avg 5m" `
    --scale in 1 `
    --cooldown 5

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Scale-in rule created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Scale-in rule failed" -ForegroundColor Yellow
}

# Scale Out Rule (Memory > 80%)
Write-Host "`n💾 Creating scale-out rule (Memory > 80%)..."
az monitor autoscale rule create `
    --resource-group $resourceGroup `
    --autoscale-name $autoscaleName `
    --condition "MemoryPercentage > 80 avg 5m" `
    --scale out 1 `
    --cooldown 5

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Memory scale-out rule created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Memory scale-out rule failed (may not be supported)" -ForegroundColor Yellow
}

Write-Host "`n" + ("=" * 60)
Write-Host "✅ Auto-Scaling Configuration Complete" -ForegroundColor Green
Write-Host "   Min Instances: 1" -ForegroundColor White
Write-Host "   Max Instances: 5" -ForegroundColor White
Write-Host "   Scale-out: CPU > 75% for 5 minutes" -ForegroundColor White
Write-Host "   Scale-in:  CPU < 25% for 5 minutes" -ForegroundColor White
Write-Host "   Cooldown:  5 minutes" -ForegroundColor White
