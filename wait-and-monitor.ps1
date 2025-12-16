# ============================================================================
# Codex Dominion - Deployment Monitor
# Runs periodic checks while infrastructure provisions
# ============================================================================

param(
    [int]$Iterations = 10,
    [int]$IntervalSeconds = 120  # Check every 2 minutes
)

Write-Host "`n⏰ DEPLOYMENT MONITOR - Starting..." -ForegroundColor Cyan
Write-Host "Will check status every $IntervalSeconds seconds ($Iterations times)`n" -ForegroundColor Gray

for ($i = 1; $i -le $Iterations; $i++) {
    $timestamp = Get-Date -Format "HH:mm:ss"

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "🔍 CHECK #$i at $timestamp" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

    $allReady = $true

    # ========================================================================
    # 1. DNS Propagation Check
    # ========================================================================

    Write-Host "1️⃣  DNS Configuration:" -ForegroundColor Yellow

    try {
        $rootDns = Resolve-DnsName -Name "codexdominion.app" -Type TXT -ErrorAction SilentlyContinue |
                   Where-Object { $_.Strings -like "*azurestaticapps*" }

        if ($rootDns) {
            Write-Host "   ✅ Root domain TXT record propagated" -ForegroundColor Green
        } else {
            Write-Host "   ⏳ Root domain TXT not propagated yet" -ForegroundColor Yellow
            $allReady = $false
        }
    } catch {
        Write-Host "   ⏳ Root domain TXT not propagated yet" -ForegroundColor Yellow
        $allReady = $false
    }

    try {
        $wwwDns = Resolve-DnsName -Name "www.codexdominion.app" -Type CNAME -ErrorAction SilentlyContinue
        if ($wwwDns -and $wwwDns.NameHost -like "*azurestaticapps*") {
            Write-Host "   ✅ www CNAME propagated" -ForegroundColor Green
        } else {
            Write-Host "   ⏳ www CNAME not propagated yet" -ForegroundColor Yellow
            $allReady = $false
        }
    } catch {
        Write-Host "   ⏳ www CNAME not propagated yet" -ForegroundColor Yellow
        $allReady = $false
    }

    try {
        $apiDns = Resolve-DnsName -Name "api.codexdominion.app" -Type CNAME -ErrorAction SilentlyContinue
        if ($apiDns -and $apiDns.NameHost -like "*azurecontainer*") {
            Write-Host "   ✅ api CNAME propagated" -ForegroundColor Green
        } else {
            Write-Host "   ⏳ api CNAME not propagated yet" -ForegroundColor Yellow
            $allReady = $false
        }
    } catch {
        Write-Host "   ⏳ api CNAME not propagated yet" -ForegroundColor Yellow
        $allReady = $false
    }

    # ========================================================================
    # 2. Redis Cache Status
    # ========================================================================

    Write-Host "`n2️⃣  Redis Cache:" -ForegroundColor Yellow

    $redis = az redis show --name "codex-redis-cache" --resource-group "codex-dominion-rg" `
        --query "{State:provisioningState, Host:hostName, Port:sslPort}" -o json 2>$null | ConvertFrom-Json

    if ($redis) {
        if ($redis.State -eq "Succeeded") {
            Write-Host "   ✅ READY: $($redis.Host):$($redis.Port)" -ForegroundColor Green
        } else {
            Write-Host "   ⏳ STATUS: $($redis.State)" -ForegroundColor Yellow
            $allReady = $false
        }
    } else {
        Write-Host "   ⏳ Creating..." -ForegroundColor Yellow
        $allReady = $false
    }

    # ========================================================================
    # 3. PostgreSQL Status
    # ========================================================================

    Write-Host "`n3️⃣  PostgreSQL:" -ForegroundColor Yellow

    $pg = az postgres flexible-server show --name "codex-postgres" --resource-group "codex-dominion-rg" `
        --query "{State:state, Host:fullyQualifiedDomainName}" -o json 2>$null | ConvertFrom-Json

    if ($pg -and $pg.State -eq "Ready") {
        Write-Host "   ✅ OPERATIONAL: $($pg.Host)" -ForegroundColor Green
    } else {
        Write-Host "   ⏳ Not ready" -ForegroundColor Yellow
        $allReady = $false
    }

    # ========================================================================
    # 4. Static Web App Status
    # ========================================================================

    Write-Host "`n4️⃣  Sovereign Bridge API:" -ForegroundColor Yellow

    try {
        $swa = Invoke-WebRequest -Uri "https://mango-wave-0fcc4e40f.3.azurestaticapps.net" `
            -Method Get -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop

        Write-Host "   ✅ LIVE: HTTP $($swa.StatusCode)" -ForegroundColor Green

        # Test API endpoint
        try {
            $api = Invoke-RestMethod -Uri "https://mango-wave-0fcc4e40f.3.azurestaticapps.net/api/agent-commands?taskId=test" `
                -Method Get -TimeoutSec 5 -ErrorAction Stop
            Write-Host "   ✅ API responding" -ForegroundColor Green
        } catch {
            Write-Host "   ⏳ API not responding yet" -ForegroundColor Yellow
            $allReady = $false
        }
    } catch {
        Write-Host "   ⏳ Provisioning..." -ForegroundColor Yellow
        $allReady = $false
    }

    # ========================================================================
    # 5. Custom Domain SSL
    # ========================================================================

    Write-Host "`n5️⃣  Custom Domain SSL:" -ForegroundColor Yellow

    try {
        $customDomain = Invoke-WebRequest -Uri "https://codexdominion.app" `
            -Method Get -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop

        Write-Host "   ✅ HTTPS working on custom domain!" -ForegroundColor Green
    } catch {
        Write-Host "   ⏳ SSL certificate generating..." -ForegroundColor Yellow
        $allReady = $false
    }

    # ========================================================================
    # Summary
    # ========================================================================

    Write-Host "`n" -NoNewline

    if ($allReady) {
        Write-Host "🎉 ALL SYSTEMS READY!" -ForegroundColor Green
        Write-Host "`n✅ Next Steps:" -ForegroundColor Cyan
        Write-Host "  1. Deploy FastAPI backend container" -ForegroundColor White
        Write-Host "  2. Test all endpoints" -ForegroundColor White
        Write-Host "  3. Run security hardening script`n" -ForegroundColor White
        break
    } else {
        $remaining = $Iterations - $i
        if ($remaining -gt 0) {
            Write-Host "⏳ Some services still provisioning..." -ForegroundColor Yellow
            Write-Host "   Waiting $IntervalSeconds seconds before next check..." -ForegroundColor Gray
            Write-Host "   ($remaining checks remaining)`n" -ForegroundColor Gray
            Start-Sleep -Seconds $IntervalSeconds
        } else {
            Write-Host "⚠️  Some services not ready after $Iterations checks" -ForegroundColor Yellow
            Write-Host "   Check Azure Portal for details`n" -ForegroundColor Gray
        }
    }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
Write-Host "Monitor complete. Run manually anytime with:" -ForegroundColor White
Write-Host "  .\check-deployment-status.ps1`n" -ForegroundColor Cyan
