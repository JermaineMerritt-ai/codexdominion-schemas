# Quick Azure Backend Deployment Script
# Deploys backend container to Azure Container Instance

$ErrorActionPreference = "Stop"

Write-Host "🚀 Deploying Codex Backend to Azure..." -ForegroundColor Cyan

# Get ACR credentials
$acrPassword = az acr credential show --name codexdominionacr --query "passwords[0].value" -o tsv

# Deploy container
Write-Host "Creating Container Instance..." -ForegroundColor Yellow
az container create `
    --resource-group codex-rg `
    --name codex-backend `
    --image codexdominionacr.azurecr.io/codex-backend:latest `
    --registry-login-server codexdominionacr.azurecr.io `
    --registry-username codexdominionacr `
    --registry-password $acrPassword `
    --dns-name-label codex-api `
    --ports 8000 `
    --cpu 1 `
    --memory 1 `
    --os-type Linux `
    --environment-variables PORT=8000 ENVIRONMENT=production PYTHONUNBUFFERED=1 `
    --location eastus2

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend deployed successfully!" -ForegroundColor Green
    Write-Host "🌐 URL: http://codex-api.eastus2.azurecontainer.io:8001" -ForegroundColor Cyan

    # Test health endpoint
    Write-Host "`nTesting health endpoint..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    try {
        $response = Invoke-WebRequest -Uri "http://codex-api.eastus2.azurecontainer.io:8001/health" -UseBasicParsing
        Write-Host "✅ Backend is healthy! Status: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Backend starting up, may take a minute..." -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
}
