#!/usr/bin/env pwsh
# Test Performance Optimizations

param(
    [string]$BaseUrl = "https://codex-backend-centralus.azurewebsites.net"
)

Write-Host "`n🧪 TESTING PERFORMANCE OPTIMIZATIONS" -ForegroundColor Cyan
Write-Host ("=" * 80)
Write-Host ""

# Test 1: Health Endpoint
Write-Host "1. Testing /health endpoint..." -ForegroundColor White
try {
    $health = Invoke-WebRequest -Uri "$BaseUrl/health" -Method Get -UseBasicParsing
    Write-Host "   ✅ Status: $($health.StatusCode)" -ForegroundColor Green

    if ($health.Headers['x-process-time']) {
        Write-Host "   ✅ X-Process-Time: $($health.Headers['x-process-time'][0])ms" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  X-Process-Time: Not found" -ForegroundColor Yellow
    }

    if ($health.Headers['Cache-Control']) {
        Write-Host "   ✅ Cache-Control: $($health.Headers['Cache-Control'][0])" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Cache-Control: Not found" -ForegroundColor Yellow
    }

    if ($health.Headers['Content-Encoding']) {
        Write-Host "   ✅ Content-Encoding: $($health.Headers['Content-Encoding'][0])" -ForegroundColor Green
    } else {
        Write-Host "   ℹ️  Content-Encoding: None (response too small for GZip)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Write-Host ""

# Test 2: Capsules Endpoint
Write-Host "2. Testing /capsules endpoint..." -ForegroundColor White
try {
    $capsules = Invoke-WebRequest -Uri "$BaseUrl/capsules" -Method Get -UseBasicParsing -MaximumRedirection 0 -ErrorAction SilentlyContinue
    if (!$capsules -or $capsules.StatusCode -ge 300) {
        # Try with redirection allowed
        $capsules = Invoke-WebRequest -Uri "$BaseUrl/capsules" -Method Get -UseBasicParsing
    }
    Write-Host "   ✅ Status: $($capsules.StatusCode)" -ForegroundColor Green

    if ($capsules.Headers['x-process-time']) {
        Write-Host "   ✅ X-Process-Time: $($capsules.Headers['x-process-time'][0])ms" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  X-Process-Time: Not found" -ForegroundColor Yellow
    }

    if ($capsules.Headers['Cache-Control']) {
        Write-Host "   ✅ Cache-Control: $($capsules.Headers['Cache-Control'][0])" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Cache-Control: Not found" -ForegroundColor Yellow
    }

    if ($capsules.Headers['Content-Encoding']) {
        Write-Host "   ✅ Content-Encoding: $($capsules.Headers['Content-Encoding'][0])" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Content-Encoding: Not found" -ForegroundColor Yellow
    }

    $size = $capsules.RawContentLength
    Write-Host "   📦 Response Size: $size bytes" -ForegroundColor Cyan

    # Parse JSON to count capsules
    $data = $capsules.Content | ConvertFrom-Json
    Write-Host "   📊 Capsules Returned: $($data.Count)" -ForegroundColor Cyan

} catch {
    Write-Host "   ❌ Error: $_" -ForegroundColor Red
}

Write-Host ""

# Test 3: Response Time Comparison (3 requests)
Write-Host "3. Testing response time consistency..." -ForegroundColor White
$times = @()
for ($i = 1; $i -le 3; $i++) {
    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $test = Invoke-WebRequest -Uri "$BaseUrl/capsules" -Method Get -UseBasicParsing -MaximumRedirection 5
        $sw.Stop()
        $times += $sw.ElapsedMilliseconds

        if ($test.Headers['x-process-time']) {
            $serverTime = $test.Headers['x-process-time'][0]
            $totalMs = $sw.ElapsedMilliseconds
            Write-Host "   Request ${i}: ${totalMs}ms total, ${serverTime}ms server" -ForegroundColor Gray
        } else {
            $totalMs = $sw.ElapsedMilliseconds
            Write-Host "   Request ${i}: ${totalMs}ms total" -ForegroundColor Gray
        }
    } catch {
        Write-Host "   Request ${i}: Failed" -ForegroundColor Red
    }
}

if ($times.Count -gt 0) {
    $avg = ($times | Measure-Object -Average).Average
    Write-Host "   📈 Average Response Time: $([math]::Round($avg, 2))ms" -ForegroundColor Cyan
}

Write-Host ""
Write-Host ("=" * 80)
Write-Host "✅ PERFORMANCE TEST COMPLETE" -ForegroundColor Green
Write-Host ("=" * 80)
Write-Host ""

# Check if performance module is loaded
Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
Write-Host "   If headers are missing, check backend logs:" -ForegroundColor White
Write-Host "   az webapp log tail --name codex-backend-centralus --resource-group codex-dominion" -ForegroundColor Gray
Write-Host ""
Write-Host "   View app settings:" -ForegroundColor White
Write-Host "   az webapp config appsettings list --name codex-backend-centralus --resource-group codex-dominion" -ForegroundColor Gray
Write-Host ""
