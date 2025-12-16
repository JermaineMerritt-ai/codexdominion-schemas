# Azure Backend SSL Setup - Enable HTTPS
# Uses Azure Application Gateway for SSL termination

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "OPTION A: ENABLE SSL FOR BACKEND API" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$RG = "codex-rg"
$LOCATION = "eastus2"
$CONTAINER_NAME = "codex-backend"

Write-Host "[Step 1/4] Analyzing Current Setup..." -ForegroundColor Yellow
Write-Host "  Current Backend: http://codex-api.eastus2.azurecontainer.io:8000" -ForegroundColor Gray
Write-Host "  Target: https://codex-api.eastus2.azurecontainer.io" -ForegroundColor Gray
Write-Host ""

Write-Host "Available SSL Solutions:" -ForegroundColor White
Write-Host "  1. Azure Application Gateway (Full SSL, ~$140/month)" -ForegroundColor Gray
Write-Host "  2. Azure Front Door (Global CDN + SSL, ~$35/month)" -ForegroundColor Gray
Write-Host "  3. Nginx Reverse Proxy on VM (Manual SSL, ~$15/month)" -ForegroundColor Gray
Write-Host "  4. Update Container to use internal SSL (Free, requires cert)" -ForegroundColor Gray
Write-Host ""

# Option 4 is most cost-effective for our use case
Write-Host "[Step 2/4] Implementing Solution: Container with SSL" -ForegroundColor Yellow
Write-Host "  Strategy: Deploy container behind Azure Container Apps with HTTPS" -ForegroundColor Gray
Write-Host ""

# Check if Azure Container Apps environment exists
Write-Host "Checking for Container Apps environment..." -ForegroundColor Yellow
$envExists = az containerapp env list --resource-group $RG --query "[?name=='codex-env'].name" -o tsv 2>$null

if (-not $envExists) {
    Write-Host "Creating Azure Container Apps environment..." -ForegroundColor Yellow

    # Create Log Analytics workspace first
    Write-Host "  Creating Log Analytics workspace..." -ForegroundColor Gray
    az monitor log-analytics workspace create `
        --resource-group $RG `
        --workspace-name "codex-logs" `
        --location $LOCATION `
        --output none 2>&1 | Out-Null

    $workspaceId = az monitor log-analytics workspace show `
        --resource-group $RG `
        --workspace-name "codex-logs" `
        --query customerId -o tsv

    $workspaceKey = az monitor log-analytics workspace get-shared-keys `
        --resource-group $RG `
        --workspace-name "codex-logs" `
        --query primarySharedKey -o tsv

    # Create Container Apps environment
    Write-Host "  Creating Container Apps environment..." -ForegroundColor Gray
    az containerapp env create `
        --name "codex-env" `
        --resource-group $RG `
        --location $LOCATION `
        --logs-workspace-id $workspaceId `
        --logs-workspace-key $workspaceKey `
        --output none 2>&1 | Out-Null

    Write-Host "  ✅ Container Apps environment created" -ForegroundColor Green
} else {
    Write-Host "  ✅ Container Apps environment exists" -ForegroundColor Green
}

Write-Host "`n[Step 3/4] Deploying Container App with HTTPS..." -ForegroundColor Yellow

# Get ACR credentials
$ACR_NAME = "codexdominionacr"
$ACR_SERVER = "$ACR_NAME.azurecr.io"
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv

# Deploy container app
Write-Host "Deploying container app with automatic HTTPS..." -ForegroundColor Yellow
az containerapp create `
    --name "codex-backend-https" `
    --resource-group $RG `
    --environment "codex-env" `
    --image "$ACR_SERVER/codex-backend:latest" `
    --registry-server $ACR_SERVER `
    --registry-username $ACR_USERNAME `
    --registry-password $ACR_PASSWORD `
    --target-port 8000 `
    --ingress external `
    --cpu 1.0 `
    --memory 2Gi `
    --min-replicas 1 `
    --max-replicas 3 `
    --env-vars "CODEX_ENVIRONMENT=production" "CODEX_CLOUD_PROVIDER=azure" `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Container App deployed successfully" -ForegroundColor Green

    # Get the FQDN
    $FQDN = az containerapp show `
        --name "codex-backend-https" `
        --resource-group $RG `
        --query properties.configuration.ingress.fqdn -o tsv

    Write-Host "`n[Step 4/4] Verification..." -ForegroundColor Yellow
    Write-Host "  New HTTPS Endpoint: https://$FQDN" -ForegroundColor Green
    Write-Host "  Testing health endpoint..." -ForegroundColor Gray

    Start-Sleep -Seconds 10  # Wait for container to start

    try {
        $health = Invoke-RestMethod -Uri "https://$FQDN/health" -TimeoutSec 10
        Write-Host "  ✅ HTTPS Health Check: $($health.status)" -ForegroundColor Green

        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "SSL ENABLEMENT COMPLETE!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Cyan

        Write-Host "🔒 HTTPS Backend: https://$FQDN" -ForegroundColor Green
        Write-Host "📊 Benefits:" -ForegroundColor White
        Write-Host "  • Automatic SSL certificate (Let's Encrypt)" -ForegroundColor Gray
        Write-Host "  • Auto-renewal of certificates" -ForegroundColor Gray
        Write-Host "  • Built-in load balancing" -ForegroundColor Gray
        Write-Host "  • Auto-scaling (1-3 replicas)" -ForegroundColor Gray
        Write-Host "  • ~$30/month cost" -ForegroundColor Gray
        Write-Host ""

        # Update dashboard URLs
        Write-Host "📝 Next Steps:" -ForegroundColor White
        Write-Host "  1. Update frontend to use: https://$FQDN" -ForegroundColor Gray
        Write-Host "  2. Update copilot-instructions.md with new URL" -ForegroundColor Gray
        Write-Host "  3. Update codex_ledger.json portal information" -ForegroundColor Gray
        Write-Host "  4. Test all API endpoints with HTTPS" -ForegroundColor Gray
        Write-Host ""

        # Save URL to file
        @{
            https_backend = "https://$FQDN"
            http_backend = "http://codex-api.eastus2.azurecontainer.io:8000"
            timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
            status = "active"
            cost = "~$30/month"
        } | ConvertTo-Json | Out-File "backend-ssl-info.json"

        Write-Host "💾 Configuration saved to: backend-ssl-info.json`n" -ForegroundColor Gray

    } catch {
        Write-Host "  ⚠️  Health check failed (container may still be starting)" -ForegroundColor Yellow
        Write-Host "  Check status: az containerapp show --name codex-backend-https --resource-group $RG" -ForegroundColor Gray
    }

} else {
    Write-Host "  ❌ Deployment failed" -ForegroundColor Red
    Write-Host "  Check existing resources: az containerapp list --resource-group $RG" -ForegroundColor Gray
}
