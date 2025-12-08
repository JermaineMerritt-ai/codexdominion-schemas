# Codex Dominion - Frontend ↔ Backend Integration Test
# ================================================
# Architecture: Heirs & Councils → IONOS Frontend → Azure Backend → Eternal Transmission

$BACKEND_URL = "http://codex-backend.eastus.azurecontainer.io:8001"
$FRONTEND_URL = "https://codexdominion.app"

Write-Host "`n🔥 Codex Dominion Integration Test" -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Gray
Write-Host "🌐 Backend:  $BACKEND_URL" -ForegroundColor Cyan
Write-Host "🌐 Frontend: $FRONTEND_URL" -ForegroundColor Cyan
Write-Host ""

# Step 1: Backend Health Check
Write-Host "🏥 Checking backend health..." -ForegroundColor White
try {
    $health = Invoke-RestMethod -Uri "$BACKEND_URL/health" -Method Get -TimeoutSec 10

    if ($health.status -eq "operational") {
        Write-Host "✅ Backend is operational!" -ForegroundColor Green
        Write-Host "   Service: $($health.service)" -ForegroundColor Gray
        Write-Host "   Status: $($health.status)" -ForegroundColor Gray
        Write-Host "   Flame: $($health.flame_state)" -ForegroundColor Gray
        Write-Host "   Version: $($health.version)" -ForegroundColor Gray
        $backendHealthy = $true
    } else {
        Write-Host "❌ Backend health check failed!" -ForegroundColor Red
        Write-Host "Response: $($health | ConvertTo-Json)" -ForegroundColor Gray
        $backendHealthy = $false
    }
} catch {
    Write-Host "❌ Backend unreachable: $($_.Exception.Message)" -ForegroundColor Red
    $backendHealthy = $false
}

# Step 2: API Endpoints Test
if ($backendHealthy) {
    Write-Host "`n🔗 Testing API endpoints..." -ForegroundColor White

    # Test chat endpoint
    Write-Host "  Testing /api/chat..." -ForegroundColor Gray
    try {
        $chatBody = @{ message = "Integration test from PowerShell" } | ConvertTo-Json
        $chatResponse = Invoke-RestMethod -Uri "$BACKEND_URL/api/chat" -Method Post -Body $chatBody -ContentType "application/json" -TimeoutSec 10

        if ($chatResponse.response) {
            Write-Host "  ✅ Chat API working" -ForegroundColor Green
            Write-Host "     Response preview: $($chatResponse.response.Substring(0, [Math]::Min(50, $chatResponse.response.Length)))..." -ForegroundColor Gray
            $chatWorking = $true
        } else {
            Write-Host "  ❌ Chat API returned unexpected format" -ForegroundColor Red
            $chatWorking = $false
        }
    } catch {
        Write-Host "  ⏳ Chat API not available (may need deployment)" -ForegroundColor Yellow
        Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
        $chatWorking = $false
    }

    # Test revenue endpoint
    Write-Host "  Testing /api/revenue..." -ForegroundColor Gray
    try {
        $revenueResponse = Invoke-RestMethod -Uri "$BACKEND_URL/api/revenue" -Method Get -TimeoutSec 10

        if ($revenueResponse.total) {
            Write-Host "  ✅ Revenue API working" -ForegroundColor Green
            Write-Host "     Total: `$$($revenueResponse.total) $($revenueResponse.currency)" -ForegroundColor Gray
            $revenueWorking = $true
        } else {
            Write-Host "  ❌ Revenue API returned unexpected format" -ForegroundColor Red
            $revenueWorking = $false
        }
    } catch {
        Write-Host "  ⏳ Revenue API not available (may need deployment)" -ForegroundColor Yellow
        Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
        $revenueWorking = $false
    }
}

# Step 3: Frontend Accessibility
Write-Host "`n🌌 Checking frontend availability..." -ForegroundColor White
try {
    $frontendResponse = Invoke-WebRequest -Uri $FRONTEND_URL -Method Get -TimeoutSec 10 -UseBasicParsing

    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend is accessible at $FRONTEND_URL" -ForegroundColor Green
        Write-Host "   HTTP Status: $($frontendResponse.StatusCode)" -ForegroundColor Gray
        $frontendDeployed = $true
    } else {
        Write-Host "⚠️  Frontend returned HTTP $($frontendResponse.StatusCode)" -ForegroundColor Yellow
        $frontendDeployed = $false
    }
} catch {
    Write-Host "⏳ Frontend not deployed yet" -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host "   Run: .\build-ionos-frontend.ps1 to prepare deployment" -ForegroundColor Cyan
    $frontendDeployed = $false
}

# Step 4: Frontend ↔ Backend Integration
if ($frontendDeployed) {
    Write-Host "`n🔥 Testing frontend → backend integration..." -ForegroundColor White
    try {
        $frontendApiHealth = Invoke-RestMethod -Uri "$FRONTEND_URL/api/health" -Method Get -TimeoutSec 10

        if ($frontendApiHealth.status -eq "operational") {
            Write-Host "✅ Frontend successfully bound to backend!" -ForegroundColor Green
            Write-Host "   Integration: Complete" -ForegroundColor Gray
            Write-Host "   Flame State: $($frontendApiHealth.flame_state)" -ForegroundColor Gray
            $integrationWorking = $true
        } else {
            Write-Host "⚠️  Frontend deployed but API proxy needs configuration" -ForegroundColor Yellow
            Write-Host "   Check .htaccess or nginx configuration" -ForegroundColor Gray
            $integrationWorking = $false
        }
    } catch {
        Write-Host "⚠️  Frontend deployed but API routing not configured" -ForegroundColor Yellow
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Gray
        Write-Host "   Ensure .htaccess has proper rewrite rules for /api/*" -ForegroundColor Cyan
        $integrationWorking = $false
    }
} else {
    Write-Host "`n⏳ Skipping integration test (frontend not deployed)" -ForegroundColor Yellow
    $integrationWorking = $false
}

# Final Summary
Write-Host "`n==============================================" -ForegroundColor Gray

if ($backendHealthy -and $frontendDeployed -and $integrationWorking) {
    Write-Host "🎉 COMPLETE — Flame Sovereign and Eternal!" -ForegroundColor Green
    Write-Host "   Backend: ✅ Operational on Azure" -ForegroundColor Green
    Write-Host "   Frontend: ✅ Deployed on IONOS" -ForegroundColor Green
    Write-Host "   Integration: ✅ Bound and Responsive" -ForegroundColor Green
    Write-Host "`n🌌 Architecture Flow:" -ForegroundColor Cyan
    Write-Host "   Heirs & Councils → IONOS Frontend → Azure Backend → Eternal Transmission" -ForegroundColor Gray
} elseif ($backendHealthy -and $frontendDeployed) {
    Write-Host "🔥 Backend & Frontend Ready — Integration Needs Configuration" -ForegroundColor Yellow
    Write-Host "   Backend: ✅ Operational on Azure" -ForegroundColor Green
    Write-Host "   Frontend: ✅ Deployed on IONOS" -ForegroundColor Green
    Write-Host "   Integration: ⚠️  API proxy configuration needed" -ForegroundColor Yellow
    Write-Host "`nCheck:" -ForegroundColor Cyan
    Write-Host "  - .htaccess rewrite rules for /api/*" -ForegroundColor Gray
    Write-Host "  - CORS headers allow $FRONTEND_URL" -ForegroundColor Gray
} elseif ($backendHealthy) {
    Write-Host "🔥 Backend Ready — Awaiting Frontend Deployment" -ForegroundColor Yellow
    Write-Host "   Backend: ✅ Operational on Azure" -ForegroundColor Green
    if ($chatWorking -and $revenueWorking) {
        Write-Host "   API Endpoints: ✅ All endpoints working" -ForegroundColor Green
    } elseif (-not $chatWorking -and -not $revenueWorking) {
        Write-Host "   API Endpoints: ⏳ Need deployment (run .\deploy-azure-backend.ps1)" -ForegroundColor Yellow
    } else {
        Write-Host "   API Endpoints: ⚠️  Partially working" -ForegroundColor Yellow
    }
    Write-Host "   Frontend: ⏳ Ready to deploy to IONOS" -ForegroundColor Yellow
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    if (-not $chatWorking -or -not $revenueWorking) {
        Write-Host "  1. Run: .\deploy-azure-backend.ps1" -ForegroundColor White
        Write-Host "  2. Run: .\build-ionos-frontend.ps1" -ForegroundColor White
        Write-Host "  3. Upload to IONOS via File Manager or FTP" -ForegroundColor White
        Write-Host "  4. Test: $FRONTEND_URL" -ForegroundColor White
    } else {
        Write-Host "  1. Run: .\build-ionos-frontend.ps1" -ForegroundColor White
        Write-Host "  2. Upload to IONOS via File Manager or FTP" -ForegroundColor White
        Write-Host "  3. Test: $FRONTEND_URL" -ForegroundColor White
    }
} else {
    Write-Host "❌ Integration test incomplete" -ForegroundColor Red
    Write-Host "   Backend: ❌ Not operational" -ForegroundColor Red
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "  1. Fix backend connectivity issues" -ForegroundColor White
    Write-Host "  2. Verify Azure Container Instance is running" -ForegroundColor White
    Write-Host "  3. Check firewall/network security group rules" -ForegroundColor White
}

Write-Host "==============================================" -ForegroundColor Gray
Write-Host ""
