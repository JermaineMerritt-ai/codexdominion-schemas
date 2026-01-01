# Deploy Frontend to Azure Container Apps
# Complete automation script

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     🚀 DEPLOYING FRONTEND TO AZURE CONTAINER APPS 🚀        ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

# Step 1: Update Next.js config for standalone build
Write-Host "📝 Step 1: Configuring Next.js for standalone deployment..." -ForegroundColor Cyan

$nextConfig = @"
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',  // Required for Docker deployment
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  env: {
    FLASK_API_URL: process.env.FLASK_API_URL || 'http://localhost:5000',
  },
};

export default nextConfig;
"@

$nextConfig | Out-File -FilePath "dashboard-app/next.config.js" -Encoding utf8
Write-Host "✅ Next.js configured for standalone output`n" -ForegroundColor Green

# Step 2: Rebuild with standalone output
Write-Host "🔨 Step 2: Rebuilding Next.js with standalone output..." -ForegroundColor Cyan
cd dashboard-app
npm run build 2>&1 | Select-String -Pattern "Compiled|Route|Error" | Select-Object -Last 10
cd ..
Write-Host "✅ Build complete`n" -ForegroundColor Green

# Step 3: Build Docker image in ACR
Write-Host "🐳 Step 3: Building Docker image in Azure Container Registry..." -ForegroundColor Cyan
Write-Host "   (This will take 3-5 minutes)`n" -ForegroundColor Gray

az acr build --registry codexacr1216 `
  --image codex-frontend:latest `
  --file Dockerfile.frontend . `
  2>&1 | Select-String -Pattern "status|Succeeded|Failed|Run ID" | ForEach-Object { Write-Host $_ }

Write-Host "`n✅ Docker image built successfully`n" -ForegroundColor Green

# Step 4: Get ACR credentials
Write-Host "🔐 Step 4: Retrieving ACR credentials..." -ForegroundColor Cyan
$acrUsername = az acr credential show --name codexacr1216 --query "username" -o tsv
$acrPassword = az acr credential show --name codexacr1216 --query "passwords[0].value" -o tsv
Write-Host "✅ Credentials retrieved`n" -ForegroundColor Green

# Step 5: Deploy to Container Apps
Write-Host "🚀 Step 5: Deploying to Azure Container Apps..." -ForegroundColor Cyan

az containerapp create `
  --name codex-frontend `
  --resource-group codexdominion-prod `
  --environment codex-env `
  --image codexacr1216.azurecr.io/codex-frontend:latest `
  --target-port 3000 `
  --ingress external `
  --registry-server codexacr1216.azurecr.io `
  --registry-username $acrUsername `
  --registry-password $acrPassword `
  --min-replicas 1 `
  --max-replicas 3 `
  --cpu 1 `
  --memory 2Gi `
  --env-vars "NEXT_PUBLIC_API_BASE_URL=https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io" `
  --output table

Write-Host "`n✅ Container App deployed`n" -ForegroundColor Green

# Step 6: Get frontend URL
Write-Host "🌐 Step 6: Getting frontend URL..." -ForegroundColor Cyan
$frontendUrl = az containerapp show --name codex-frontend `
  --resource-group codexdominion-prod `
  --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  🎉 DEPLOYMENT SUCCESSFUL! 🎉                 ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📍 Frontend URL: https://$frontendUrl" -ForegroundColor Cyan
Write-Host "📍 Backend URL:  https://codex-backend.bravefield-eea1536e.eastus.azurecontainerapps.io`n" -ForegroundColor Cyan

Write-Host "🧪 Test Commands:" -ForegroundColor Yellow
Write-Host "   Invoke-WebRequest https://$frontendUrl" -ForegroundColor Gray
Write-Host "   Start-Process https://$frontendUrl`n" -ForegroundColor Gray

Write-Host "📊 Management Commands:" -ForegroundColor Yellow
Write-Host "   Logs:    az containerapp logs show --name codex-frontend --resource-group codexdominion-prod --tail 50" -ForegroundColor Gray
Write-Host "   Restart: az containerapp revision restart --name codex-frontend --resource-group codexdominion-prod" -ForegroundColor Gray
Write-Host "   Update:  az containerapp update --name codex-frontend --resource-group codexdominion-prod --image codexacr1216.azurecr.io/codex-frontend:latest`n" -ForegroundColor Gray

Write-Host "💰 Estimated Cost: ~$20-30/month (in addition to backend)" -ForegroundColor Yellow
Write-Host "🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Green
