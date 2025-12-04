#!/usr/bin/env pwsh
# Sandbox Deployment Script
# Deploys application to isolated sandbox environment for testing

param(
    [string]$BuildPath = "./build",
    [string]$Environment = "sandbox",
    [switch]$SkipTests = $false
)

Write-Host "🏗️  SANDBOX DEPLOYMENT SCRIPT" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Configuration
$SandboxHost = "sandbox.codexdominion.local"
$SandboxPort = 4000
$BackendPort = 4001

# Step 1: Pre-deployment validation
Write-Host "`n[1/7] Validating build artifacts..." -ForegroundColor Yellow
if (-not (Test-Path $BuildPath)) {
    Write-Host "❌ Build path not found: $BuildPath" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Build artifacts validated" -ForegroundColor Green

# Step 2: Stop existing sandbox instances
Write-Host "`n[2/7] Stopping existing sandbox instances..." -ForegroundColor Yellow
pm2 delete codex-sandbox-frontend -ErrorAction SilentlyContinue
pm2 delete codex-sandbox-backend -ErrorAction SilentlyContinue
Write-Host "✅ Existing instances stopped" -ForegroundColor Green

# Step 3: Deploy frontend
Write-Host "`n[3/7] Deploying frontend to sandbox..." -ForegroundColor Yellow
$env:NODE_ENV = "sandbox"
$env:PORT = $SandboxPort
$env:NEXT_PUBLIC_API_URL = "http://localhost:$BackendPort"

pm2 start "$BuildPath/frontend/server.js" `
    --name "codex-sandbox-frontend" `
    --env sandbox `
    -- --port $SandboxPort

Write-Host "✅ Frontend deployed on port $SandboxPort" -ForegroundColor Green

# Step 4: Deploy backend
Write-Host "`n[4/7] Deploying backend to sandbox..." -ForegroundColor Yellow
pm2 start "$BuildPath/server.js" `
    --name "codex-sandbox-backend" `
    --env sandbox `
    -- --port $BackendPort

Write-Host "✅ Backend deployed on port $BackendPort" -ForegroundColor Green

# Step 5: Health checks
Write-Host "`n[5/7] Running health checks..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $backendHealth = Invoke-RestMethod -Uri "http://localhost:$BackendPort/health" -TimeoutSec 10
    if ($backendHealth.status -eq "operational") {
        Write-Host "✅ Backend health check passed" -ForegroundColor Green
    } else {
        throw "Backend health check failed"
    }
} catch {
    Write-Host "❌ Backend health check failed: $_" -ForegroundColor Red
    pm2 logs codex-sandbox-backend --lines 50
    exit 1
}

# Step 6: Smoke tests
if (-not $SkipTests) {
    Write-Host "`n[6/7] Running smoke tests..." -ForegroundColor Yellow

    # Test backend endpoints
    $endpoints = @(
        "http://localhost:$BackendPort/health",
        "http://localhost:$BackendPort/api/empire/status"
    )

    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-RestMethod -Uri $endpoint -TimeoutSec 5
            Write-Host "  ✅ $endpoint" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ $endpoint failed" -ForegroundColor Red
        }
    }

    Write-Host "✅ Smoke tests completed" -ForegroundColor Green
} else {
    Write-Host "`n[6/7] Skipping smoke tests" -ForegroundColor Yellow
}

# Step 7: Display status
Write-Host "`n[7/7] Deployment summary" -ForegroundColor Yellow
pm2 list
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🎉 SANDBOX DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend: http://localhost:$SandboxPort" -ForegroundColor White
Write-Host "Backend:  http://localhost:$BackendPort" -ForegroundColor White
Write-Host "Health:   http://localhost:$BackendPort/health" -ForegroundColor White
Write-Host ""
Write-Host "Logs: pm2 logs codex-sandbox-*" -ForegroundColor Gray
Write-Host "Stop: pm2 delete codex-sandbox-*" -ForegroundColor Gray
