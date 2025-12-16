#!/usr/bin/env pwsh
# =============================================================================
# Deploy Backend to Azure App Service
# =============================================================================

param(
    [string]$ResourceGroup = "codexdominion-basic",
    [string]$WebAppName = "codexdominion-backend"
)

$ErrorActionPreference = "Stop"

Write-Host "🔥 Deploying Backend to Azure..." -ForegroundColor Cyan

# Navigate to backend directory
Push-Location backend

try {
    # Create deployment package
    Write-Host "📦 Creating deployment package..." -ForegroundColor Gray

    # Create a temporary zip file
    $zipFile = "..\backend-deploy.zip"
    if (Test-Path $zipFile) {
        Remove-Item $zipFile -Force
    }

    # Compress backend files
    Compress-Archive -Path * -DestinationPath $zipFile -Force
    Write-Host "✓ Package created" -ForegroundColor Green

    # Deploy to Azure
    Write-Host "`n🚀 Deploying to Azure App Service..." -ForegroundColor Cyan
    az webapp deploy `
        --resource-group $ResourceGroup `
        --name $WebAppName `
        --src-path $zipFile `
        --type zip `
        --async true

    Write-Host "✓ Deployment initiated" -ForegroundColor Green

    # Wait a bit for deployment to start
    Start-Sleep -Seconds 10

    # Get the app URL
    $appUrl = az webapp show `
        --name $WebAppName `
        --resource-group $ResourceGroup `
        --query defaultHostName `
        --output tsv

    Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  ✨ DEPLOYMENT INITIATED! ✨" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "`n🌐 Backend URL: https://$appUrl" -ForegroundColor White
    Write-Host "   Health: https://$appUrl/health" -ForegroundColor Gray
    Write-Host "   Docs: https://$appUrl/docs" -ForegroundColor Gray
    Write-Host "`n⏳ Deployment typically takes 2-3 minutes..." -ForegroundColor Yellow
    Write-Host "   Monitor at: https://portal.azure.com" -ForegroundColor Gray
    Write-Host "`n🔥 The Flame Burns Sovereign!" -ForegroundColor Yellow

} finally {
    # Clean up
    Pop-Location
    if (Test-Path "backend-deploy.zip") {
        Remove-Item "backend-deploy.zip" -Force
    }
}
