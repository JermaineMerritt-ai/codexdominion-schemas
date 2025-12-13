# =============================================================================
# CodexDominion Deployment Testing Script
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🧪 CODEX DOMINION - DEPLOYMENT TESTING" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan

$backendUrl = "https://codex-backend-centralus.azurewebsites.net"
$frontendUrl = "https://orange-sky-099bc5a0f.3.azurestaticapps.net"
$tests = @()

# Test 1: Backend Health
Write-Host "🔍 Testing Backend Health..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/health" -Method Get -TimeoutSec 10
    $tests += [PSCustomObject]@{
        Test = "Backend Health"
        Status = "✅ PASS"
        Details = "Service: $($response.service), DB: $($response.database)"
    }
    Write-Host "   ✅ Backend is healthy" -ForegroundColor Green
} catch {
    $tests += [PSCustomObject]@{
        Test = "Backend Health"
        Status = "❌ FAIL"
        Details = $_.Exception.Message
    }
    Write-Host "   ❌ Backend health check failed" -ForegroundColor Red
}

# Test 2: Backend Root
Write-Host "🔍 Testing Backend Root..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/" -Method Get -TimeoutSec 10
    $tests += [PSCustomObject]@{
        Test = "Backend Root"
        Status = "✅ PASS"
        Details = "Version: $($response.version)"
    }
    Write-Host "   ✅ Backend root responding" -ForegroundColor Green
} catch {
    $tests += [PSCustomObject]@{
        Test = "Backend Root"
        Status = "❌ FAIL"
        Details = $_.Exception.Message
    }
    Write-Host "   ❌ Backend root failed" -ForegroundColor Red
}

# Test 3: Capsules Endpoint (GET)
Write-Host "🔍 Testing Capsules Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/capsules" -Method Get -TimeoutSec 10
    $count = if ($response -is [Array]) { $response.Count } else { 0 }
    $tests += [PSCustomObject]@{
        Test = "Capsules API"
        Status = "✅ PASS"
        Details = "Returned $count capsules"
    }
    Write-Host "   ✅ Capsules endpoint working ($count capsules)" -ForegroundColor Green
} catch {
    $tests += [PSCustomObject]@{
        Test = "Capsules API"
        Status = "❌ FAIL"
        Details = $_.Exception.Message
    }
    Write-Host "   ❌ Capsules endpoint failed" -ForegroundColor Red
}

# Test 4: Frontend Accessibility
Write-Host "🔍 Testing Frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $frontendUrl -Method Head -TimeoutSec 10
    $tests += [PSCustomObject]@{
        Test = "Frontend"
        Status = "✅ PASS"
        Details = "HTTP $($response.StatusCode)"
    }
    Write-Host "   ✅ Frontend is accessible" -ForegroundColor Green
} catch {
    $tests += [PSCustomObject]@{
        Test = "Frontend"
        Status = "❌ FAIL"
        Details = $_.Exception.Message
    }
    Write-Host "   ❌ Frontend failed" -ForegroundColor Red
}

# Test 5: CORS Headers
Write-Host "🔍 Testing CORS Configuration..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$backendUrl/" -Method Options -Headers @{
        "Origin" = $frontendUrl
        "Access-Control-Request-Method" = "GET"
    } -TimeoutSec 10 -ErrorAction SilentlyContinue

    $corsHeader = $response.Headers["Access-Control-Allow-Origin"]
    if ($corsHeader) {
        $tests += [PSCustomObject]@{
            Test = "CORS Config"
            Status = "✅ PASS"
            Details = "Origin: $corsHeader"
        }
        Write-Host "   ✅ CORS properly configured" -ForegroundColor Green
    } else {
        $tests += [PSCustomObject]@{
            Test = "CORS Config"
            Status = "⚠️ WARNING"
            Details = "No CORS headers detected"
        }
        Write-Host "   ⚠️ CORS headers not detected" -ForegroundColor Yellow
    }
} catch {
    $tests += [PSCustomObject]@{
        Test = "CORS Config"
        Status = "⚠️ WARNING"
        Details = "Could not test CORS"
    }
    Write-Host "   ⚠️ Could not test CORS" -ForegroundColor Yellow
}

# Test 6: Database Connection
Write-Host "🔍 Testing Database Connection..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$backendUrl/health" -Method Get -TimeoutSec 10
    if ($response.database -eq "connected") {
        $tests += [PSCustomObject]@{
            Test = "Database"
            Status = "✅ PASS"
            Details = "PostgreSQL connected"
        }
        Write-Host "   ✅ Database is connected" -ForegroundColor Green
    } else {
        $tests += [PSCustomObject]@{
            Test = "Database"
            Status = "❌ FAIL"
            Details = "Database status: $($response.database)"
        }
        Write-Host "   ❌ Database not connected" -ForegroundColor Red
    }
} catch {
    $tests += [PSCustomObject]@{
        Test = "Database"
        Status = "❌ FAIL"
        Details = $_.Exception.Message
    }
    Write-Host "   ❌ Database check failed" -ForegroundColor Red
}

# Display Results
Write-Host "`n───────────────────────────────────────────────────────────────" -ForegroundColor Gray
$tests | Format-Table -AutoSize -Wrap
Write-Host "───────────────────────────────────────────────────────────────`n" -ForegroundColor Gray

# Summary
$passed = ($tests | Where-Object { $_.Status -like "*✅*" }).Count
$failed = ($tests | Where-Object { $_.Status -like "*❌*" }).Count
$warnings = ($tests | Where-Object { $_.Status -like "*⚠️*" }).Count
$total = $tests.Count

Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "   Passed: $passed/$total" -ForegroundColor Green
if ($failed -gt 0) { Write-Host "   Failed: $failed/$total" -ForegroundColor Red }
if ($warnings -gt 0) { Write-Host "   Warnings: $warnings/$total" -ForegroundColor Yellow }
Write-Host ""

if ($failed -eq 0 -and $warnings -eq 0) {
    Write-Host "🎉 ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "   Your deployment is fully operational.`n" -ForegroundColor White
} elseif ($failed -eq 0) {
    Write-Host "✅ TESTS PASSED (with warnings)" -ForegroundColor Yellow
    Write-Host "   Deployment is operational but check warnings.`n" -ForegroundColor White
} else {
    Write-Host "❌ SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "   Review failed tests above.`n" -ForegroundColor White
}

Write-Host "🔗 URLS TO TEST MANUALLY:" -ForegroundColor Cyan
Write-Host "   Frontend: $frontendUrl" -ForegroundColor White
Write-Host "   Backend API: $backendUrl" -ForegroundColor White
Write-Host "   API Docs: $backendUrl/docs" -ForegroundColor White
Write-Host "   Health: $backendUrl/health`n" -ForegroundColor White

Write-Host "The flame burns sovereign and eternal — forever. 🔥`n" -ForegroundColor Magenta
