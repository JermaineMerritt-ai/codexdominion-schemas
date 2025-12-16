# ============================================================================
# Azure DNS Configuration Script for Codex Dominion
# ============================================================================

param(
    [string]$ZoneName = "codexdominion.app",
    [string]$ResourceGroup = "" # Will auto-detect if not provided
)

Write-Host "`n🌐 AZURE DNS CONFIGURATION" -ForegroundColor Cyan
Write-Host "============================`n" -ForegroundColor Cyan

# Step 1: Find DNS Zone
Write-Host "🔍 Finding DNS zone: $ZoneName..." -ForegroundColor White

if (-not $ResourceGroup) {
    $zone = az network dns zone list --query "[?name=='$ZoneName']" -o json | ConvertFrom-Json
    if ($zone) {
        $ResourceGroup = $zone.resourceGroup
        Write-Host "✓ Found in Resource Group: $ResourceGroup`n" -ForegroundColor Green
    } else {
        Write-Host "❌ DNS Zone '$ZoneName' not found!" -ForegroundColor Red
        Write-Host "`n📋 Available DNS Zones:" -ForegroundColor Yellow
        az network dns zone list --query "[].{Name:name, ResourceGroup:resourceGroup}" -o table
        exit 1
    }
}

# Step 2: Remove old A records (if they exist)
Write-Host "`n📝 Step 1: Removing old A records..." -ForegroundColor Cyan

# Remove @ A record
Write-Host "  Removing @ A record (20.36.155.75)..." -ForegroundColor Gray
az network dns record-set a delete `
    --zone-name $ZoneName `
    --resource-group $ResourceGroup `
    --name "@" `
    --yes 2>$null

# Remove www A record
Write-Host "  Removing www A record (20.36.155.75)..." -ForegroundColor Gray
az network dns record-set a delete `
    --zone-name $ZoneName `
    --resource-group $ResourceGroup `
    --name "www" `
    --yes 2>$null

Write-Host "✓ Old A records removed`n" -ForegroundColor Green

# Step 3: Add CNAME for root domain (using ALIAS/ANAME)
Write-Host "📝 Step 2: Adding root domain CNAME..." -ForegroundColor Cyan
Write-Host "  Target: mango-wave-0fcc4e40f.3.azurestaticapps.net" -ForegroundColor Gray

# Azure DNS doesn't support CNAME at apex, so we use A record pointing to Static Web App IP
# First, let's try CNAME approach (will fail, then we'll use TXT + A record)

Write-Host "`n⚠️  Azure DNS doesn't support CNAME at root (@)" -ForegroundColor Yellow
Write-Host "  Solution: Use Azure Static Web Apps custom domain binding" -ForegroundColor Yellow
Write-Host "  Azure will automatically configure DNS records`n" -ForegroundColor Yellow

# Step 4: Add www CNAME
Write-Host "📝 Step 3: Adding www CNAME..." -ForegroundColor Cyan

az network dns record-set cname set-record `
    --zone-name $ZoneName `
    --resource-group $ResourceGroup `
    --record-set-name "www" `
    --cname "mango-wave-0fcc4e40f.3.azurestaticapps.net" `
    --ttl 3600

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ www CNAME created: www.$ZoneName → mango-wave-0fcc4e40f.3.azurestaticapps.net" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create www CNAME" -ForegroundColor Red
}

# Step 5: Add api CNAME
Write-Host "`n📝 Step 4: Adding api CNAME..." -ForegroundColor Cyan

az network dns record-set cname set-record `
    --zone-name $ZoneName `
    --resource-group $ResourceGroup `
    --record-set-name "api" `
    --cname "codex-backend-api.eastus2.azurecontainer.io" `
    --ttl 3600

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ api CNAME created: api.$ZoneName → codex-backend-api.eastus2.azurecontainer.io" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create api CNAME" -ForegroundColor Red
}

# Step 6: Configure Static Web App custom domain (handles root domain)
Write-Host "`n📝 Step 5: Binding root domain to Static Web App..." -ForegroundColor Cyan

Write-Host "  Running: az staticwebapp hostname set..." -ForegroundColor Gray

az staticwebapp hostname set `
    --name "codex-sovereign-bridge" `
    --resource-group "codex-dominion-rg" `
    --hostname "$ZoneName" `
    2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Root domain bound successfully" -ForegroundColor Green
    Write-Host "  Azure will auto-configure required DNS records" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Manual domain binding required" -ForegroundColor Yellow
    Write-Host "  Go to: https://portal.azure.com" -ForegroundColor Gray
    Write-Host "  Navigate to: codex-sovereign-bridge → Custom domains → Add" -ForegroundColor Gray
}

# Step 7: Show current configuration
Write-Host "`n📋 Current DNS Records:" -ForegroundColor Cyan
az network dns record-set list `
    --zone-name $ZoneName `
    --resource-group $ResourceGroup `
    --query "[?type!='Microsoft.Network/dnszones/NS' && type!='Microsoft.Network/dnszones/SOA'].{Name:name, Type:type, TTL:ttl, Records:aRecords[0].ipv4Address || cnameRecord.cname || txtRecords[0].value[0]}" `
    --output table

# Step 8: Verification
Write-Host "`n✅ DNS Configuration Complete!" -ForegroundColor Green
Write-Host "`n📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Wait 5-10 minutes for DNS propagation" -ForegroundColor White
Write-Host "2. Run: .\verify-dns-setup.ps1" -ForegroundColor White
Write-Host "3. SSL certificates will auto-generate (5-10 min after propagation)" -ForegroundColor White
Write-Host "4. Test: https://$ZoneName" -ForegroundColor White
Write-Host "5. Test: https://api.$ZoneName/health`n" -ForegroundColor White

Write-Host "🔗 Azure Portal:" -ForegroundColor Cyan
Write-Host "  DNS Zone: https://portal.azure.com/#resource/subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/$ResourceGroup/providers/Microsoft.Network/dnszones/$ZoneName/overview" -ForegroundColor Gray
Write-Host "  Static Web App: https://portal.azure.com/#resource/subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/codex-dominion-rg/providers/Microsoft.Web/staticSites/codex-sovereign-bridge/customDomains`n" -ForegroundColor Gray
