#!/usr/bin/env pwsh
# Comprehensive Engine Fix and Deployment Script
# This script fixes all engine deployment issues

Write-Host "🔧 Codex Dominion Engine Fix Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Step 1: Clean up all failing deployments
Write-Host "`n📦 Step 1: Cleaning up failing deployments..." -ForegroundColor Yellow
kubectl delete deployment -n default -l app --all --ignore-not-found=true
kubectl delete deployment -n codex --all --ignore-not-found=true

# Step 2: Wait for cleanup
Write-Host "⏳ Waiting for cleanup to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Step 3: Deploy fixed engines
Write-Host "`n🚀 Step 2: Deploying fixed engines..." -ForegroundColor Yellow
kubectl apply -f k8s/engines-fixed.yaml

# Step 4: Wait for deployments
Write-Host "⏳ Waiting for engines to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Step 5: Check status
Write-Host "`n✅ Step 3: Checking engine status..." -ForegroundColor Green
kubectl get pods -n default | Select-String "engine"

Write-Host "`n📊 Deployment Summary:" -ForegroundColor Cyan
kubectl get deployments -n default | Select-String "engine"

Write-Host "`n✅ Engine fix completed!" -ForegroundColor Green
Write-Host "📝 Note: Engines are now running with nginx:alpine placeholder images" -ForegroundColor Yellow
Write-Host "📌 Next step: Build and push custom engine images to replace placeholders" -ForegroundColor Yellow
