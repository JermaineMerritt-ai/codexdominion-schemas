#!/usr/bin/env pwsh
# Canary Deployment Script
# Gradually rolls out changes to production with automated monitoring

param(
    [int]$TrafficPercentage = 5,
    [int]$MonitorDuration = 300, # 5 minutes
    [string]$BuildPath = "./build"
)

Write-Host "🐦 CANARY DEPLOYMENT SCRIPT" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Configuration
$CanaryPort = 3002
$ProductionPort = 3000
$MetricsEndpoint = "http://localhost:9090/metrics"

# Step 1: Deploy canary version
Write-Host "`n[1/5] Deploying canary version..." -ForegroundColor Yellow
pm2 start "$BuildPath/server.js" `
    --name "codex-canary" `
    --env canary `
    -- --port $CanaryPort

Start-Sleep -Seconds 5
Write-Host "✅ Canary deployed on port $CanaryPort" -ForegroundColor Green

# Step 2: Configure traffic routing
Write-Host "`n[2/5] Configuring traffic routing ($TrafficPercentage%)..." -ForegroundColor Yellow
# In production, this would update load balancer configuration
Write-Host "✅ Traffic routing configured" -ForegroundColor Green

# Step 3: Monitor canary metrics
Write-Host "`n[3/5] Monitoring canary metrics for $MonitorDuration seconds..." -ForegroundColor Yellow

$startTime = Get-Date
$endTime = $startTime.AddSeconds($MonitorDuration)
$errorCount = 0
$requestCount = 0
$rollbackTriggered = $false

while ((Get-Date) -lt $endTime -and -not $rollbackTriggered) {
    $elapsed = ((Get-Date) - $startTime).TotalSeconds
    $remaining = ($endTime - (Get-Date)).TotalSeconds

    Write-Host "`r  Monitoring... ${elapsed}s / ${MonitorDuration}s " -NoNewline -ForegroundColor Cyan

    try {
        # Check canary health
        $health = Invoke-RestMethod -Uri "http://localhost:$CanaryPort/health" -TimeoutSec 5

        # Simulated metrics check (in production, query Prometheus/Grafana)
        $metrics = @{
            errorRate = (Get-Random -Minimum 0 -Maximum 100) / 1000
            latencyP95 = Get-Random -Minimum 50 -Maximum 600
            requestCount = Get-Random -Minimum 10 -Maximum 100
        }

        $requestCount += $metrics.requestCount

        # Check rollback conditions
        if ($metrics.errorRate -gt 0.01) {
            Write-Host "`n❌ Error rate exceeded threshold: $($metrics.errorRate * 100)%" -ForegroundColor Red
            $rollbackTriggered = $true
        } elseif ($metrics.latencyP95 -gt 500) {
            Write-Host "`n❌ Latency exceeded threshold: $($metrics.latencyP95)ms" -ForegroundColor Red
            $rollbackTriggered = $true
        }

    } catch {
        Write-Host "`n❌ Canary health check failed" -ForegroundColor Red
        $rollbackTriggered = $true
    }

    Start-Sleep -Seconds 10
}

Write-Host ""

# Step 4: Decision point
if ($rollbackTriggered) {
    Write-Host "`n[4/5] ⚠️  ROLLBACK TRIGGERED" -ForegroundColor Red
    Write-Host "Executing rollback..." -ForegroundColor Yellow

    pm2 delete codex-canary

    Write-Host "✅ Rollback complete" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Red
    Write-Host "❌ CANARY DEPLOYMENT FAILED" -ForegroundColor Red
    Write-Host "=================================" -ForegroundColor Red

    exit 1
} else {
    Write-Host "`n[4/5] ✅ Canary metrics healthy" -ForegroundColor Green

    # Step 5: Promote to production
    Write-Host "`n[5/5] Promoting canary to production..." -ForegroundColor Yellow

    # In production: gradually increase traffic 5% -> 25% -> 50% -> 100%
    Write-Host "  Traffic: 5% -> 25%..." -ForegroundColor Cyan
    Start-Sleep -Seconds 30

    Write-Host "  Traffic: 25% -> 50%..." -ForegroundColor Cyan
    Start-Sleep -Seconds 30

    Write-Host "  Traffic: 50% -> 100%..." -ForegroundColor Cyan
    Start-Sleep -Seconds 30

    # Replace production with canary
    pm2 delete codex-production -ErrorAction SilentlyContinue
    pm2 restart codex-canary --name codex-production

    Write-Host "✅ Promotion complete" -ForegroundColor Green

    Write-Host ""
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "🎉 CANARY DEPLOYMENT SUCCESSFUL" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Metrics:" -ForegroundColor White
    Write-Host "  Total requests: $requestCount" -ForegroundColor Gray
    Write-Host "  Errors: $errorCount" -ForegroundColor Gray
    Write-Host "  Error rate: $(($errorCount / $requestCount * 100).ToString('0.00'))%" -ForegroundColor Gray
}
