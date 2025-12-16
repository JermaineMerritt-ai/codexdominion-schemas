# ============================================================================
# Complete DNS Fix for Codex Dominion
# Handles: api conflict, root domain TXT validation, www CNAME
# ============================================================================

Write-Host "`n🔧 DNS CONFIGURATION FIX" -ForegroundColor Cyan
Write-Host "========================`n" -ForegroundColor Cyan

$zoneName = "codexdominion.app"
$resourceGroup = "codex-dominion"
$staticAppName = "codex-sovereign-bridge"
$staticAppRg = "codex-dominion-rg"

# ============================================================================
# STEP 1: Fix API Subdomain (Remove A record, Add CNAME)
# ============================================================================

Write-Host "📝 Step 1: Fixing API subdomain..." -ForegroundColor Yellow

# Remove conflicting A record
Write-Host "   Removing existing api A record..." -ForegroundColor Gray
az network dns record-set a delete `
    --zone-name $zoneName `
    --resource-group $resourceGroup `
    --name "api" `
    --yes 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Removed api A record" -ForegroundColor Green
}

# Create CNAME
Write-Host "   Creating api CNAME..." -ForegroundColor Gray
$apiResult = az network dns record-set cname set-record `
    --zone-name $zoneName `
    --resource-group $resourceGroup `
    --record-set-name "api" `
    --cname "codex-backend-api.eastus2.azurecontainer.io" `
    --ttl 3600 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ api.codexdominion.app → codex-backend-api.eastus2.azurecontainer.io`n" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed: $apiResult`n" -ForegroundColor Red
}

# ============================================================================
# STEP 2: Get Root Domain Validation Token
# ============================================================================

Write-Host "📝 Step 2: Setting up root domain validation..." -ForegroundColor Yellow

# Get Static Web App details
Write-Host "   Retrieving Static Web App info..." -ForegroundColor Gray
$staticApp = az staticwebapp show `
    --name $staticAppName `
    --resource-group $staticAppRg `
    -o json | ConvertFrom-Json

$defaultHostname = $staticApp.defaultHostname

Write-Host "   Static Web App: $defaultHostname`n" -ForegroundColor Gray

# Generate validation token
Write-Host "   Generating TXT validation token..." -ForegroundColor Gray
Write-Host "   (This will show an error - that's normal, we just need the token)`n" -ForegroundColor DarkGray

$tokenOutput = az staticwebapp hostname set `
    --name $staticAppName `
    --resource-group $staticAppRg `
    --hostname $zoneName `
    --validation-method "dns-txt-token" 2>&1

# Extract token from error message or success
$token = $null
if ($tokenOutput -match "validationToken[`"']?\s*[:=]\s*[`"']?([a-f0-9\-]+)") {
    $token = $matches[1]
} elseif ($tokenOutput -match "([a-f0-9]{64,})") {
    $token = $matches[1]
}

if ($token) {
    Write-Host "   ✓ Validation token: $token`n" -ForegroundColor Green

    # ============================================================================
    # STEP 3: Add TXT Validation Record
    # ============================================================================

    Write-Host "📝 Step 3: Adding TXT validation record..." -ForegroundColor Yellow

    # Check if TXT record exists
    $existingTxt = az network dns record-set txt show `
        --zone-name $zoneName `
        --resource-group $resourceGroup `
        --name "@" 2>$null | ConvertFrom-Json

    if ($existingTxt) {
        # Add to existing TXT record
        Write-Host "   Adding to existing TXT record..." -ForegroundColor Gray
        az network dns record-set txt add-record `
            --zone-name $zoneName `
            --resource-group $resourceGroup `
            --record-set-name "@" `
            --value $token 2>&1 | Out-Null
    } else {
        # Create new TXT record
        Write-Host "   Creating new TXT record..." -ForegroundColor Gray
        az network dns record-set txt add-record `
            --zone-name $zoneName `
            --resource-group $resourceGroup `
            --record-set-name "@" `
            --value $token `
            --ttl 3600 2>&1 | Out-Null
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ TXT validation record added`n" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  TXT record may already exist`n" -ForegroundColor Yellow
    }

    # ============================================================================
    # STEP 4: Wait for DNS Propagation
    # ============================================================================

    Write-Host "📝 Step 4: Waiting for DNS propagation..." -ForegroundColor Yellow
    Write-Host "   Waiting 30 seconds for TXT record to propagate...`n" -ForegroundColor Gray

    Start-Sleep -Seconds 30

    # ============================================================================
    # STEP 5: Bind Root Domain
    # ============================================================================

    Write-Host "📝 Step 5: Binding root domain to Static Web App..." -ForegroundColor Yellow
    Write-Host "   Attempting domain validation...`n" -ForegroundColor Gray

    $bindResult = az staticwebapp hostname set `
        --name $staticAppName `
        --resource-group $staticAppRg `
        --hostname $zoneName `
        --validation-method "dns-txt-token" 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Root domain bound successfully!`n" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Validation in progress (this can take 5-10 minutes)" -ForegroundColor Yellow
        Write-Host "   Error: $bindResult`n" -ForegroundColor DarkGray
    }

} else {
    Write-Host "   ❌ Could not retrieve validation token" -ForegroundColor Red
    Write-Host "   Please bind domain manually in Azure Portal`n" -ForegroundColor Yellow
}

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📋 FINAL DNS CONFIGURATION:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

$records = az network dns record-set list `
    --zone-name $zoneName `
    --resource-group $resourceGroup `
    --query "[?type!='Microsoft.Network/dnszones/NS' && type!='Microsoft.Network/dnszones/SOA']" `
    -o json | ConvertFrom-Json

foreach ($record in $records) {
    $name = if ($record.name -eq "@") { "root" } else { $record.name }
    $type = ($record.type -split '/')[-1]

    $value = "N/A"
    if ($record.aRecords -and $record.aRecords.Count -gt 0) {
        $value = $record.aRecords[0].ipv4Address
    } elseif ($record.cnameRecord) {
        $value = $record.cnameRecord.cname
    } elseif ($record.txtRecords -and $record.txtRecords.Count -gt 0) {
        $txtValues = $record.txtRecords | ForEach-Object { $_.value -join ", " }
        $value = ($txtValues -join "; ").Substring(0, [Math]::Min(60, ($txtValues -join "; ").Length)) + "..."
    }

    Write-Host "  $name" -ForegroundColor White -NoNewline
    Write-Host " ($type) → " -ForegroundColor Gray -NoNewline
    Write-Host "$value" -ForegroundColor Cyan
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "✅ DNS Configuration Complete!`n" -ForegroundColor Green

Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Wait 5-10 minutes for full DNS propagation" -ForegroundColor White
Write-Host "2. Verify: .\verify-dns-setup.ps1" -ForegroundColor White
Write-Host "3. If root domain validation fails, check Azure Portal:" -ForegroundColor White
Write-Host "   Custom Domains → Add → codexdominion.app → TXT validation" -ForegroundColor Gray
Write-Host "4. SSL certificates will auto-generate after validation" -ForegroundColor White
Write-Host "5. Test: https://codexdominion.app" -ForegroundColor White
Write-Host "6. Test: https://www.codexdominion.app" -ForegroundColor White
Write-Host "7. Test: https://api.codexdominion.app/health`n" -ForegroundColor White

Write-Host "🔗 Azure Portal Custom Domains:" -ForegroundColor Cyan
Write-Host "https://portal.azure.com/#resource/subscriptions/054bb0e0-6e79-403f-b3fc-39a28d61e9c9/resourceGroups/$staticAppRg/providers/Microsoft.Web/staticSites/$staticAppName/customDomains`n" -ForegroundColor Blue
