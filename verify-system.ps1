# Comprehensive System Verification Script
# Tests all Codex Dominion services and generates final report

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "CODEX DOMINION - FINAL VERIFICATION" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Configuration
$backend = "http://codex-api.eastus2.azurecontainer.io:8000"
$frontend = "https://witty-glacier-0ebbd971e.3.azurestaticapps.net"
$dashboard = "http://localhost:5000"

$results = @()

# Test 1: Backend API Health
Write-Host "[1/6] Testing Backend API..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$backend/health" -Method Get
    if ($health.status -eq "healthy") {
        Write-Host "      ✅ Backend: Healthy (v$($health.version))" -ForegroundColor Green
        $results += @{test="Backend API"; status="PASS"; detail=$health.service}
    } else {
        Write-Host "      ❌ Backend: Unhealthy" -ForegroundColor Red
        $results += @{test="Backend API"; status="FAIL"; detail="Unhealthy response"}
    }
} catch {
    Write-Host "      ❌ Backend: Error - $_" -ForegroundColor Red
    $results += @{test="Backend API"; status="FAIL"; detail=$_.Exception.Message}
}

# Test 2: Frontend Static Web App
Write-Host "`n[2/6] Testing Frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $frontend -Method Head -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "      ✅ Frontend: Online (200 OK)" -ForegroundColor Green
        $results += @{test="Frontend"; status="PASS"; detail="Static Web App accessible"}
    }
} catch {
    Write-Host "      ❌ Frontend: Offline" -ForegroundColor Red
    $results += @{test="Frontend"; status="FAIL"; detail=$_.Exception.Message}
}

# Test 3: Dashboard (if running)
Write-Host "`n[3/6] Testing Dashboard..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $dashboard -Method Head -UseBasicParsing -TimeoutSec 5
    Write-Host "      ✅ Dashboard: Online" -ForegroundColor Green
    $results += @{test="Dashboard"; status="PASS"; detail="Master Dashboard accessible"}
} catch {
    Write-Host "      ⚠️  Dashboard: Not running locally" -ForegroundColor Yellow
    $results += @{test="Dashboard"; status="WARNING"; detail="Not started"}
}

# Test 4: Azure Resources
Write-Host "`n[4/6] Verifying Azure Resources..." -ForegroundColor Yellow
$rg = "codex-rg"

$containerStatus = az container show --resource-group $rg --name codex-backend --query "instanceView.state" -o tsv 2>$null
if ($containerStatus -eq "Running") {
    Write-Host "      ✅ Container Instance: Running" -ForegroundColor Green
    $results += @{test="Container Instance"; status="PASS"; detail="Running state"}
} else {
    Write-Host "      ❌ Container Instance: $containerStatus" -ForegroundColor Red
    $results += @{test="Container Instance"; status="FAIL"; detail=$containerStatus}
}

$staticWebApp = az staticwebapp show --name witty-glacier-0ebbd971e --query "defaultHostname" -o tsv 2>$null
if ($staticWebApp) {
    Write-Host "      ✅ Static Web App: Configured" -ForegroundColor Green
    $results += @{test="Static Web App"; status="PASS"; detail=$staticWebApp}
}

# Test 5: Monitoring Alerts
Write-Host "`n[5/6] Checking Monitoring..." -ForegroundColor Yellow
$alerts = az monitor metrics alert list --resource-group $rg --query "length([])" -o tsv 2>$null
if ($alerts -gt 0) {
    Write-Host "      ✅ Alerts: $alerts configured" -ForegroundColor Green
    $results += @{test="Monitoring Alerts"; status="PASS"; detail="$alerts alerts active"}
} else {
    Write-Host "      ⚠️  Alerts: None found" -ForegroundColor Yellow
    $results += @{test="Monitoring Alerts"; status="WARNING"; detail="No alerts"}
}

# Test 6: Data Integration
Write-Host "`n[6/6] Verifying Data Integration..." -ForegroundColor Yellow
if (Test-Path "dashboard_data.json") {
    $data = Get-Content "dashboard_data.json" | ConvertFrom-Json
    Write-Host "      ✅ Dashboard Data: Generated" -ForegroundColor Green
    Write-Host "         Revenue Target: `$$($data.revenue.total_monthly_target)" -ForegroundColor Gray
    Write-Host "         Affiliate Earnings: `$$([math]::Round($data.affiliate.commission_earned, 2))" -ForegroundColor Gray
    $results += @{test="Data Integration"; status="PASS"; detail="dashboard_data.json exists"}
} else {
    Write-Host "      ⚠️  Dashboard Data: Not found" -ForegroundColor Yellow
    $results += @{test="Data Integration"; status="WARNING"; detail="dashboard_data.json missing"}
}

# Summary Report
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$passed = ($results | Where-Object { $_.status -eq "PASS" }).Count
$failed = ($results | Where-Object { $_.status -eq "FAIL" }).Count
$warnings = ($results | Where-Object { $_.status -eq "WARNING" }).Count

Write-Host "Total Tests: $($results.Count)" -ForegroundColor White
Write-Host "✅ Passed: $passed" -ForegroundColor Green
Write-Host "❌ Failed: $failed" -ForegroundColor Red
Write-Host "⚠️  Warnings: $warnings" -ForegroundColor Yellow

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT STATUS: " -NoNewline -ForegroundColor Cyan
if ($failed -eq 0) {
    Write-Host "✅ SUCCESS" -ForegroundColor Green
} elseif ($failed -le 2) {
    Write-Host "⚠️  PARTIAL" -ForegroundColor Yellow
} else {
    Write-Host "❌ FAILED" -ForegroundColor Red
}
Write-Host "========================================`n" -ForegroundColor Cyan

# Save detailed report
$report = @{
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    results = $results
    summary = @{
        total = $results.Count
        passed = $passed
        failed = $failed
        warnings = $warnings
    }
    endpoints = @{
        backend = $backend
        frontend = $frontend
        dashboard = $dashboard
    }
}

$report | ConvertTo-Json -Depth 10 | Out-File "verification_report.json"
Write-Host "Detailed report saved to: verification_report.json" -ForegroundColor Gray
Write-Host ""
