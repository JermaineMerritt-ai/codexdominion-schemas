# Azure Container Instance Environment Configuration Script
# Use this to update environment variables for the Codex backend

# Get ACR credentials
$acrPassword = (az acr credential show --name codexdominionacr --query "passwords[0].value" -o tsv)

# Define environment variables
$envVars = @(
    "PORT=8001",
    "ENVIRONMENT=production",
    "PYTHONUNBUFFERED=1",
    "ALLOWED_ORIGINS=https://codex-dominion.azurestaticapps.net,http://localhost:3001",
    "CORS_ENABLED=true"
    # Optional: Uncomment and configure as needed
    # "DATABASE_URL=postgresql://user:pass@host:5432/db",
    # "REDIS_URL=redis://:<password>@codex-redis.redis.cache.windows.net:6380?ssl=True",
    # "SECRET_KEY=your-secret-key",
    # "APPINSIGHTS_INSTRUMENTATIONKEY=your-key"
)

# Join environment variables with space
$envVarsString = $envVars -join " "

Write-Host "🔄 Deleting existing container..." -ForegroundColor Yellow
az container delete --resource-group codex-rg --name codex-backend --yes

Write-Host "🚀 Creating container with updated environment variables..." -ForegroundColor Cyan
az container create `
  --resource-group codex-rg `
  --name codex-backend `
  --image codexdominionacr.azurecr.io/codex-backend:prod `
  --os-type Linux `
  --cpu 1 `
  --memory 1 `
  --registry-login-server codexdominionacr.azurecr.io `
  --registry-username codexdominionacr `
  --registry-password $acrPassword `
  --dns-name-label codex-api `
  --ports 8001 `
  --protocol TCP `
  --environment-variables $envVarsString

Write-Host ""
Write-Host "✅ Container deployed!" -ForegroundColor Green
Write-Host "📍 URL: http://codex-api.eastus.azurecontainer.io:8001" -ForegroundColor Green
Write-Host ""
Write-Host "Testing health endpoint..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
$response = curl -s http://codex-api.eastus.azurecontainer.io:8001/health
Write-Host $response -ForegroundColor Green
