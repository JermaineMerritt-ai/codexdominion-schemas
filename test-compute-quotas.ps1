# Test if App Service quotas are available
# This will attempt to validate an App Service deployment

$SUBSCRIPTION_ID = "f86506f8-7d33-48de-995d-f51e6f590cb1"
$LOCATION = "westus"
$RESOURCE_GROUP = "codex-rg"

Write-Host "`n=== Testing App Service Quota Availability ===" -ForegroundColor Cyan

az account set --subscription $SUBSCRIPTION_ID

# Test 1: Free Tier (F1)
Write-Host "`n[Test 1] Free Tier (F1) App Service Plan" -ForegroundColor Yellow
Write-Host "Creating validation template for F1 tier..." -ForegroundColor Gray

$testTemplateF1 = @"
{
  "`$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2022-03-01",
      "name": "test-plan-f1",
      "location": "$LOCATION",
      "sku": {
        "name": "F1",
        "tier": "Free"
      }
    }
  ]
}
"@

$testTemplateF1 | Out-File -FilePath "test-f1.json" -Encoding UTF8

$result = az deployment group validate `
    --resource-group $RESOURCE_GROUP `
    --template-file test-f1.json `
    2>&1 | Out-String

if ($result -match "SubscriptionIsOverQuotaForSku.*Free VMs") {
    Write-Host "❌ Free Tier (F1): QUOTA NOT AVAILABLE" -ForegroundColor Red
    Write-Host "   Current: 0, Required: 1" -ForegroundColor Gray
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Free Tier (F1): QUOTA AVAILABLE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Free Tier (F1): Validation issue (not quota related)" -ForegroundColor Yellow
}

# Test 2: Basic Tier (B1)
Write-Host "`n[Test 2] Basic Tier (B1) App Service Plan" -ForegroundColor Yellow
Write-Host "Creating validation template for B1 tier..." -ForegroundColor Gray

$testTemplateB1 = @"
{
  "`$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2022-03-01",
      "name": "test-plan-b1",
      "location": "$LOCATION",
      "sku": {
        "name": "B1",
        "tier": "Basic"
      }
    }
  ]
}
"@

$testTemplateB1 | Out-File -FilePath "test-b1.json" -Encoding UTF8

$result = az deployment group validate `
    --resource-group $RESOURCE_GROUP `
    --template-file test-b1.json `
    2>&1 | Out-String

if ($result -match "SubscriptionIsOverQuotaForSku.*Basic VMs") {
    Write-Host "❌ Basic Tier (B1): QUOTA NOT AVAILABLE" -ForegroundColor Red
    Write-Host "   Current: 0, Required: 1" -ForegroundColor Gray
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Basic Tier (B1): QUOTA AVAILABLE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Basic Tier (B1): Validation issue (not quota related)" -ForegroundColor Yellow
}

# Test 3: Consumption Plan (Y1) for Functions
Write-Host "`n[Test 3] Consumption Tier (Y1) Functions Plan" -ForegroundColor Yellow
Write-Host "Creating validation template for Y1 tier..." -ForegroundColor Gray

$testTemplateY1 = @"
{
  "`$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Web/serverfarms",
      "apiVersion": "2022-03-01",
      "name": "test-plan-y1",
      "location": "$LOCATION",
      "kind": "functionapp",
      "sku": {
        "name": "Y1",
        "tier": "Dynamic"
      }
    }
  ]
}
"@

$testTemplateY1 | Out-File -FilePath "test-y1.json" -Encoding UTF8

$result = az deployment group validate `
    --resource-group $RESOURCE_GROUP `
    --template-file test-y1.json `
    2>&1 | Out-String

if ($result -match "SubscriptionIsOverQuotaForSku.*Dynamic VMs") {
    Write-Host "❌ Consumption Tier (Y1): QUOTA NOT AVAILABLE" -ForegroundColor Red
    Write-Host "   Current: 0, Required: 1" -ForegroundColor Gray
} elseif ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Consumption Tier (Y1): QUOTA AVAILABLE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Consumption Tier (Y1): Validation issue (not quota related)" -ForegroundColor Yellow
}

# Cleanup test files
Remove-Item test-f1.json -ErrorAction SilentlyContinue
Remove-Item test-b1.json -ErrorAction SilentlyContinue
Remove-Item test-y1.json -ErrorAction SilentlyContinue

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host @"

Based on the tests above:
- If all show ✅: You can deploy compute resources
- If any show ❌: Need to request quota increase for that tier

To request quota:
1. Visit: https://portal.azure.com/#view/Microsoft_Azure_Capacity/QuotaMenuBlade
2. Select your subscription
3. Click "Request increase"
4. Select region: West US
5. Request increases for failed tiers

Current Status:
- Data services (PostgreSQL, Redis, Key Vault, ACR): ✅ Deployed
- Compute services (App Service, Functions): Awaiting quota approval

"@
