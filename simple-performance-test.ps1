#!/usr/bin/env pwsh
# Simple Performance Test

$BaseUrl = "https://codex-backend-centralus.azurewebsites.net"

Write-Host "`n🧪 PERFORMANCE TEST" -ForegroundColor Cyan
Write-Host ("=" * 60)

# Test Health Endpoint
Write-Host "`n1. Health Check (/health)" -ForegroundColor White
try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get -ResponseHeadersVariable healthHeaders
    Write-Host "   ✅ Status: OK" -ForegroundColor Green
    Write-Host "   ✅ Response: $($health.status)" -ForegroundColor Green

    if ($healthHeaders -and $healthHeaders['x-process-time']) {
        Write-Host "   ✅ X-Process-Time: $($healthHeaders['x-process-time'][0])" -ForegroundColor Green
    }
    if ($healthHeaders -and $healthHeaders['Cache-Control']) {
        Write-Host "   ✅ Cache-Control: $($healthHeaders['Cache-Control'][0])" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Capsules Endpoint
Write-Host "`n2. Capsules Endpoint (/capsules)" -ForegroundColor White
try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $capsules = Invoke-RestMethod -Uri "$BaseUrl/capsules" -Method Get -ResponseHeadersVariable capsulesHeaders
    $sw.Stop()

    Write-Host "   ✅ Status: OK" -ForegroundColor Green
    Write-Host "   ✅ Capsules Count: $($capsules.Count)" -ForegroundColor Green
    Write-Host "   ✅ Total Time: $($sw.ElapsedMilliseconds)ms" -ForegroundColor Green

    if ($capsulesHeaders -and $capsulesHeaders['x-process-time']) {
        Write-Host "   ✅ X-Process-Time: $($capsulesHeaders['x-process-time'][0])" -ForegroundColor Green
    }
    if ($capsulesHeaders -and $capsulesHeaders['Cache-Control']) {
        Write-Host "   ✅ Cache-Control: $($capsulesHeaders['Cache-Control'][0])" -ForegroundColor Green
    }
    if ($capsulesHeaders -and $capsulesHeaders['Content-Encoding']) {
        Write-Host "   ✅ Content-Encoding: $($capsulesHeaders['Content-Encoding'][0])" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test Response Times
Write-Host "`n3. Response Time Test (3 requests)" -ForegroundColor White
$times = @()
for ($i = 1; $i -le 3; $i++) {
    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $null = Invoke-RestMethod -Uri "$BaseUrl/capsules" -Method Get
        $sw.Stop()
        $times += $sw.ElapsedMilliseconds
        Write-Host "   Request $i`: $($sw.ElapsedMilliseconds)ms" -ForegroundColor Gray
    } catch {
        Write-Host "   Request $i`: Failed" -ForegroundColor Red
    }
}

if ($times.Count -gt 0) {
    $avg = [math]::Round(($times | Measure-Object -Average).Average, 2)
    Write-Host "   📈 Average: ${avg}ms" -ForegroundColor Cyan
}

Write-Host "`n" -NoNewline
Write-Host ("=" * 60)
Write-Host "✅ TEST COMPLETE" -ForegroundColor Green
Write-Host ("=" * 60)
Write-Host ""
