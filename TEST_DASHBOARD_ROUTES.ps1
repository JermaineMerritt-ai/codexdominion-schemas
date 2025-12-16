# ===========================================================
# CODEX DOMINION - Dashboard Routes Test Script
# ===========================================================

Write-Host "`n" -NoNewline
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  CODEX DOMINION - Testing All Routes" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Test all main routes
$routes = @(
    @{Path="/"; Name="Home Dashboard"},
    @{Path="/social"; Name="Social Media"},
    @{Path="/affiliate"; Name="Affiliate Marketing"},
    @{Path="/chatbot"; Name="Action Chatbot"},
    @{Path="/algorithm"; Name="Algorithm AI"},
    @{Path="/autopublish"; Name="Auto-Publish"},
    @{Path="/dot300"; Name="DOT300 Agents"},
    @{Path="/orchestration"; Name="GPT-4 Orchestration"}
)

$passed = 0
$failed = 0

foreach($route in $routes) {
    try {
        $resp = Invoke-WebRequest "http://localhost:5000$($route.Path)" -UseBasicParsing -TimeoutSec 5
        if($resp.StatusCode -eq 200) {
            Write-Host "✅ $($route.Name).padRight(25)" -NoNewline -ForegroundColor Green
            Write-Host " : HTTP $($resp.StatusCode) OK" -ForegroundColor White
            $passed++
        } else {
            Write-Host "⚠️  $($route.Name).padRight(25)" -NoNewline -ForegroundColor Yellow
            Write-Host " : HTTP $($resp.StatusCode)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($route.Name).padRight(25)" -NoNewline -ForegroundColor Red
        Write-Host " : FAILED" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan

# Test Health Endpoint
Write-Host "`n📊 Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod http://localhost:5000/health
    Write-Host "✅ Service: $($health.service)" -ForegroundColor Green
    Write-Host "✅ Status: $($health.status)" -ForegroundColor Green
    Write-Host "✅ Total Routes: $($health.routes.Count)" -ForegroundColor Green
    Write-Host "✅ Timestamp: $($health.timestamp)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "✅ Passed: $passed" -ForegroundColor Green
Write-Host "❌ Failed: $failed" -ForegroundColor Red

if($failed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! Dashboard fully operational!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Some tests failed. Please review errors above." -ForegroundColor Yellow
}

Write-Host ""
