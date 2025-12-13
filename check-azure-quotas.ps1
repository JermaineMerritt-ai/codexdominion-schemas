# Azure Quota and Provider Check Script
# Run this to verify readiness for App Service/Functions deployment

$SUBSCRIPTION_ID = "f86506f8-7d33-48de-995d-f51e6f590cb1"
$LOCATION = "westus"

Write-Host "`n=== Azure Quota and Provider Readiness Check ===" -ForegroundColor Cyan
Write-Host "Subscription: $SUBSCRIPTION_ID" -ForegroundColor Gray
Write-Host "Location: $LOCATION`n" -ForegroundColor Gray

# Set subscription
az account set --subscription $SUBSCRIPTION_ID

# Check Resource Providers
Write-Host "`n[1] Resource Provider Registration Status" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray

$providers = @(
    "Microsoft.Web",
    "Microsoft.DBforPostgreSQL",
    "Microsoft.Cache",
    "Microsoft.KeyVault",
    "Microsoft.Insights",
    "Microsoft.ContainerRegistry",
    "microsoft.operationalinsights"
)

foreach ($provider in $providers) {
    $state = az provider show --namespace $provider --query "registrationState" -o tsv
    $status = if ($state -eq "Registered") { "✅" } else { "❌" }
    Write-Host "$status $provider : $state"
}

# Test App Service deployment capability
Write-Host "`n[2] App Service Deployment Test (Dry Run)" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray

Write-Host "`nTesting Free tier (F1) deployment capability..."
$testResult = az deployment group validate `
    --resource-group codex-rg `
    --template-file infra/main-private.bicep `
    --parameters '@infra/main-private.parameters.json' `
    --parameters pgAdminPassword="TestPassword123!" `
    2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Validation passed - deployment would succeed" -ForegroundColor Green
} else {
    if ($testResult -match "SubscriptionIsOverQuotaForSku") {
        Write-Host "❌ QUOTA ISSUE: Insufficient quota for deployment" -ForegroundColor Red
        if ($testResult -match "Free VMs.*0") {
            Write-Host "   - Free VMs: 0 (need at least 1)" -ForegroundColor Red
        }
        if ($testResult -match "Basic VMs.*0") {
            Write-Host "   - Basic VMs: 0 (need at least 1)" -ForegroundColor Red
        }
        if ($testResult -match "Dynamic VMs.*0") {
            Write-Host "   - Dynamic VMs: 0 (need at least 1)" -ForegroundColor Red
        }
    } elseif ($testResult -match "MissingSubscriptionRegistration") {
        Write-Host "❌ PROVIDER ISSUE: Some providers not registered" -ForegroundColor Red
    } else {
        Write-Host "❌ Validation failed (see details above)" -ForegroundColor Red
    }
}

# Current deployed resources
Write-Host "`n[3] Currently Deployed Resources" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
az resource list --resource-group codex-rg `
    --query "[?location=='westus'].{Name:name, Type:type, State:provisioningState}" `
    -o table

Write-Host "`n[4] Quota Request Instructions" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
Write-Host @"
If quota errors were shown above, request increases via Azure Portal:

1. Go to: https://portal.azure.com/#view/Microsoft_Azure_Capacity/QuotaMenuBlade/~/myQuotas
2. Select subscription: $SUBSCRIPTION_ID
3. Filter by Provider: Microsoft.Compute
4. Search and request increase for:
   - Standard BSv2 Family vCPUs (for Basic App Service) → Request: 2
   - Standard Av2 Family vCPUs (for Free App Service) → Request: 1
   - Total Regional vCPUs → Request: 10

5. OR search for 'App Service' specific quotas if available

Note: Data services (PostgreSQL, Redis, Key Vault, ACR, App Insights)
are already deployed successfully and don't require compute quota.
"@

Write-Host "`n=== Check Complete ===" -ForegroundColor Cyan
