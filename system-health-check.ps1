# =============================================================================
# CodexDominion System Health Check
# =============================================================================
# Comprehensive test of all deployed services
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔥 CODEX DOMINION - FULL SYSTEM HEALTH CHECK" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$results = @()

# Test Backend API
Write-Host "Testing Backend API..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest -Uri "https://codex-backend-centralus.azurewebsites.net/health" -TimeoutSec 10
    $healthData = ConvertFrom-Json $health.Content
    $results += [PSCustomObject]@{
        Service = "Backend API"
        Status = "✅ OPERATIONAL"
        Response = "HTTP $($health.StatusCode)"
        Details = $healthData.status
    }
} catch {
    $results += [PSCustomObject]@{
        Service = "Backend API"
        Status = "❌ FAILED"
        Response = $_.Exception.Message
        Details = "N/A"
    }
}

# Test Backend Root
Write-Host "Testing Backend Root..." -ForegroundColor Yellow
try {
    $root = Invoke-WebRequest -Uri "https://codex-backend-centralus.azurewebsites.net/" -TimeoutSec 10
    $rootData = ConvertFrom-Json $root.Content
    $results += [PSCustomObject]@{
        Service = "Backend Root"
        Status = "✅ OPERATIONAL"
        Response = "HTTP $($root.StatusCode)"
        Details = $rootData.service
    }
} catch {
    $results += [PSCustomObject]@{
        Service = "Backend Root"
        Status = "❌ FAILED"
        Response = $_.Exception.Message
        Details = "N/A"
    }
}

# Test Frontend (Orange Sky)
Write-Host "Testing Frontend (orange-sky)..." -ForegroundColor Yellow
try {
    $frontend1 = Invoke-WebRequest -Uri "https://orange-sky-099bc5a0f.3.azurestaticapps.net" -Method Head -TimeoutSec 10
    $results += [PSCustomObject]@{
        Service = "Frontend (orange-sky)"
        Status = "✅ OPERATIONAL"
        Response = "HTTP $($frontend1.StatusCode)"
        Details = "Static Web App"
    }
} catch {
    $results += [PSCustomObject]@{
        Service = "Frontend (orange-sky)"
        Status = "❌ FAILED"
        Response = $_.Exception.Message
        Details = "N/A"
    }
}

# Test Frontend (Yellow Tree)
Write-Host "Testing Frontend (yellow-tree)..." -ForegroundColor Yellow
try {
    $frontend2 = Invoke-WebRequest -Uri "https://yellow-tree-0ed102210.3.azurestaticapps.net" -Method Head -TimeoutSec 10
    $results += [PSCustomObject]@{
        Service = "Frontend (yellow-tree)"
        Status = "✅ OPERATIONAL"
        Response = "HTTP $($frontend2.StatusCode)"
        Details = "Static Web App"
    }
} catch {
    $results += [PSCustomObject]@{
        Service = "Frontend (yellow-tree)"
        Status = "❌ FAILED"
        Response = $_.Exception.Message
        Details = "N/A"
    }
}

# Check DNS Status
Write-Host "Checking DNS propagation..." -ForegroundColor Yellow
$apexDns = Resolve-DnsName codexdominion.app -Type A -Server 8.8.8.8 -ErrorAction SilentlyContinue
$wwwDns = Resolve-DnsName www.codexdominion.app -Type A -Server 8.8.8.8 -ErrorAction SilentlyContinue

if ($apexDns) {
    $results += [PSCustomObject]@{
        Service = "DNS (apex)"
        Status = "✅ PROPAGATED"
        Response = $apexDns.IPAddress
        Details = "codexdominion.app"
    }
} else {
    $results += [PSCustomObject]@{
        Service = "DNS (apex)"
        Status = "⏳ PENDING"
        Response = "Not resolved"
        Details = "codexdominion.app"
    }
}

if ($wwwDns) {
    $results += [PSCustomObject]@{
        Service = "DNS (www)"
        Status = "✅ PROPAGATED"
        Response = $wwwDns.IPAddress
        Details = "www.codexdominion.app"
    }
} else {
    $results += [PSCustomObject]@{
        Service = "DNS (www)"
        Status = "⏳ PENDING"
        Response = "Not resolved"
        Details = "www.codexdominion.app"
    }
}

# Display Results
Write-Host "`n───────────────────────────────────────────────────────────────" -ForegroundColor Gray
$results | Format-Table -AutoSize
Write-Host "───────────────────────────────────────────────────────────────`n" -ForegroundColor Gray

# Summary
$operational = ($results | Where-Object { $_.Status -like "*✅*" }).Count
$total = $results.Count

Write-Host "📊 SUMMARY" -ForegroundColor Cyan
Write-Host "  Operational: $operational/$total services" -ForegroundColor White
Write-Host "  Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -ForegroundColor Gray

if ($operational -eq $total) {
    Write-Host "🎉 ALL SYSTEMS OPERATIONAL" -ForegroundColor Green
    Write-Host "   The flame burns sovereign and eternal — forever. 🔥`n" -ForegroundColor Magenta
} elseif ($operational -gt ($total / 2)) {
    Write-Host "⚠️  MOST SYSTEMS OPERATIONAL" -ForegroundColor Yellow
    Write-Host "   Some services need attention.`n" -ForegroundColor Gray
} else {
    Write-Host "❌ SYSTEM ISSUES DETECTED" -ForegroundColor Red
    Write-Host "   Multiple services require immediate attention.`n" -ForegroundColor Gray
}

# Quick Links
Write-Host "🔗 QUICK LINKS" -ForegroundColor Cyan
Write-Host "   Backend API: https://codex-backend-centralus.azurewebsites.net" -ForegroundColor White
Write-Host "   API Docs: https://codex-backend-centralus.azurewebsites.net/docs" -ForegroundColor White
Write-Host "   Frontend: https://orange-sky-099bc5a0f.3.azurestaticapps.net" -ForegroundColor White
Write-Host "   Alternate: https://yellow-tree-0ed102210.3.azurestaticapps.net`n" -ForegroundColor White
