Write-Host "`n🔍 CODEX DOMINION - DEPLOYMENT STATUS CHECK" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

Write-Host "Checking all resources...`n" -ForegroundColor White

# PostgreSQL
$pgStatus = az postgres flexible-server show --name "codex-postgres" --resource-group "codex-dominion-rg" --query "{Name:name, State:state, Version:version}" -o json 2>$null | ConvertFrom-Json
if ($pgStatus) {
    Write-Host "✅ PostgreSQL: $($pgStatus.State)" -ForegroundColor Green
    Write-Host "   Host: codex-postgres.postgres.database.azure.com" -ForegroundColor Gray
} else {
    Write-Host "❌ PostgreSQL: Not found" -ForegroundColor Red
}

# Redis
$redisStatus = az redis show --name "codex-redis-cache" --resource-group "codex-dominion-rg" --query "{Name:name, State:provisioningState}" -o json 2>$null | ConvertFrom-Json
if ($redisStatus) {
    $color = if ($redisStatus.State -eq "Succeeded") { "Green" } else { "Yellow" }
    Write-Host "$($redisStatus.State -eq 'Succeeded' ? '✅' : '⏳') Redis: $($redisStatus.State)" -ForegroundColor $color
    Write-Host "   Host: codex-redis-cache.redis.cache.windows.net" -ForegroundColor Gray
} else {
    Write-Host "⏳ Redis: Creating..." -ForegroundColor Yellow
}

# Static Web App
$swaStatus = az staticwebapp show --name "codex-sovereign-bridge" --resource-group "codex-dominion-rg" --query "{Name:name, Url:defaultHostname}" -o json 2>$null | ConvertFrom-Json
if ($swaStatus) {
    Write-Host "✅ Static Web App: Ready" -ForegroundColor Green
    Write-Host "   URL: https://$($swaStatus.Url)" -ForegroundColor Gray

    # Test API
    try {
        $apiTest = Invoke-WebRequest -Uri "https://$($swaStatus.Url)/api/agent-commands?taskId=status" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        Write-Host "   ✅ API: Live (HTTP $($apiTest.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "   ⏳ API: Provisioning..." -ForegroundColor Yellow
    }
} else {
    Write-Host "⏳ Static Web App: Provisioning..." -ForegroundColor Yellow
}

# Container Registry
$acrStatus = az acr show --name "codexdominion" --resource-group "codex-dominion-rg" --query "{Name:name, LoginServer:loginServer}" -o json 2>$null | ConvertFrom-Json
if ($acrStatus) {
    Write-Host "✅ Container Registry: Ready" -ForegroundColor Green
    Write-Host "   Server: $($acrStatus.LoginServer)" -ForegroundColor Gray
} else {
    Write-Host "❌ Container Registry: Not found" -ForegroundColor Red
}

Write-Host "`n✅ = Ready  |  ⏳ = In Progress  |  ❌ = Failed`n" -ForegroundColor Gray
