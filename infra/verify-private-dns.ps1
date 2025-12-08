# Private DNS Verification Script
# Checks if private DNS zones and A records are properly configured

param(
    [string]$ResourceGroup = "codex-rg",
    [string]$BaseName = "codex"
)

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Private DNS Verification Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if logged in to Azure
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "ERROR: Not logged in to Azure. Please run 'az login' first." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "✓ Subscription: $($account.name)" -ForegroundColor Green
Write-Host ""

# Check if resource group exists
Write-Host "Checking resource group '$ResourceGroup'..." -ForegroundColor Yellow
$rg = az group show --name $ResourceGroup 2>$null | ConvertFrom-Json
if (-not $rg) {
    Write-Host "ERROR: Resource group '$ResourceGroup' not found." -ForegroundColor Red
    Write-Host "Please deploy infrastructure first using deploy-private-infrastructure.yml workflow." -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Resource group exists in $($rg.location)" -ForegroundColor Green
Write-Host ""

# Define DNS zones to check
$dnsZones = @(
    @{
        Name = "privatelink.postgres.database.azure.com"
        RecordName = "$BaseName-pg"
        Service = "PostgreSQL"
    },
    @{
        Name = "privatelink.redis.cache.windows.net"
        RecordName = "$BaseName-redis"
        Service = "Redis"
    },
    @{
        Name = "privatelink.vaultcore.azure.net"
        RecordName = "$BaseName-kv"
        Service = "Key Vault"
    }
)

$allSuccess = $true

foreach ($zone in $dnsZones) {
    Write-Host "Checking $($zone.Service) DNS configuration..." -ForegroundColor Yellow

    # Check if DNS zone exists
    $dnsZone = az network private-dns zone show `
        --resource-group $ResourceGroup `
        --name $zone.Name 2>$null | ConvertFrom-Json

    if (-not $dnsZone) {
        Write-Host "  ✗ DNS zone '$($zone.Name)' not found" -ForegroundColor Red
        $allSuccess = $false
        continue
    }
    Write-Host "  ✓ DNS zone exists" -ForegroundColor Green

    # Check VNet link
    $vnetLinks = az network private-dns link vnet list `
        --resource-group $ResourceGroup `
        --zone-name $zone.Name 2>$null | ConvertFrom-Json

    if ($vnetLinks.Count -eq 0) {
        Write-Host "  ✗ No VNet links found" -ForegroundColor Red
        $allSuccess = $false
    } else {
        Write-Host "  ✓ VNet link: $($vnetLinks[0].name)" -ForegroundColor Green
    }

    # Check A record
    $aRecord = az network private-dns record-set a show `
        --resource-group $ResourceGroup `
        --zone-name $zone.Name `
        --name $zone.RecordName 2>$null | ConvertFrom-Json

    if (-not $aRecord) {
        Write-Host "  ✗ A record '$($zone.RecordName)' not found" -ForegroundColor Red
        $allSuccess = $false
        continue
    }

    if ($aRecord.aRecords.Count -eq 0) {
        Write-Host "  ✗ A record exists but has no IP addresses" -ForegroundColor Red
        Write-Host "    Run DNS finalizer workflow to populate IPs" -ForegroundColor Yellow
        $allSuccess = $false
    } else {
        $ip = $aRecord.aRecords[0].ipv4Address
        Write-Host "  ✓ A record: $($zone.RecordName) -> $ip" -ForegroundColor Green

        # Verify IP is in private range
        if ($ip -match "^10\.10\.2\.") {
            Write-Host "  ✓ IP is in private subnet (10.10.2.0/24)" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ IP '$ip' is not in expected private subnet" -ForegroundColor Yellow
        }
    }

    Write-Host ""
}

# Check private endpoints
Write-Host "Checking private endpoints..." -ForegroundColor Yellow
$privateEndpoints = @(
    "$BaseName-pg-pe",
    "$BaseName-redis-pe",
    "$BaseName-kv-pe"
)

foreach ($peName in $privateEndpoints) {
    $pe = az network private-endpoint show `
        --name $peName `
        --resource-group $ResourceGroup 2>$null | ConvertFrom-Json

    if (-not $pe) {
        Write-Host "  ✗ Private endpoint '$peName' not found" -ForegroundColor Red
        $allSuccess = $false
    } else {
        $state = $pe.provisioningState
        if ($state -eq "Succeeded") {
            Write-Host "  ✓ $peName : $state" -ForegroundColor Green

            # Show private IP
            if ($pe.customDnsConfigs -and $pe.customDnsConfigs.Count -gt 0) {
                $ip = $pe.customDnsConfigs[0].ipAddresses[0]
                Write-Host "    Private IP: $ip" -ForegroundColor Cyan
            }
        } else {
            Write-Host "  ⚠ $peName : $state" -ForegroundColor Yellow
            $allSuccess = $false
        }
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan

if ($allSuccess) {
    Write-Host "✓ All DNS configurations verified successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test DNS resolution from App Service (see VERIFICATION_GUIDE.md)" -ForegroundColor White
    Write-Host "2. Deploy backend: backend-deploy.yml workflow" -ForegroundColor White
    Write-Host "3. Deploy frontend: frontend-deploy.yml workflow" -ForegroundColor White
} else {
    Write-Host "✗ Some DNS configurations are missing or incomplete" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Ensure infrastructure is deployed: deploy-private-infrastructure.yml" -ForegroundColor White
    Write-Host "2. Run DNS finalizer if A records are empty: finalize-private-dns.yml" -ForegroundColor White
    Write-Host "3. Check Azure Portal for deployment errors" -ForegroundColor White
    exit 1
}
