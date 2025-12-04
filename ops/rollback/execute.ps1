#!/usr/bin/env pwsh
# Rollback Script
# Automated rollback to previous stable version

param(
    [string]$Version = "previous",
    [switch]$Force = $false
)

Write-Host "🔄 ROLLBACK SCRIPT" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Configuration
$BackupDir = "./backups"
$CurrentVersion = Get-Content "./.version" -ErrorAction SilentlyContinue

# Step 1: Verify rollback target
Write-Host "`n[1/5] Verifying rollback target..." -ForegroundColor Yellow

if ($Version -eq "previous") {
    $targetVersion = Get-ChildItem $BackupDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -Skip 1
} else {
    $targetVersion = Get-Item "$BackupDir/$Version" -ErrorAction SilentlyContinue
}

if (-not $targetVersion) {
    Write-Host "❌ Target version not found" -ForegroundColor Red
    exit 1
}

Write-Host "Current version: $CurrentVersion" -ForegroundColor Gray
Write-Host "Target version:  $($targetVersion.Name)" -ForegroundColor Gray

if (-not $Force) {
    $confirm = Read-Host "Proceed with rollback? (yes/no)"
    if ($confirm -ne "yes") {
        Write-Host "Rollback cancelled" -ForegroundColor Yellow
        exit 0
    }
}

# Step 2: Stop current services
Write-Host "`n[2/5] Stopping current services..." -ForegroundColor Yellow
pm2 stop all
Write-Host "✅ Services stopped" -ForegroundColor Green

# Step 3: Restore previous version
Write-Host "`n[3/5] Restoring previous version..." -ForegroundColor Yellow
Copy-Item -Path "$($targetVersion.FullName)/*" -Destination "./" -Recurse -Force
Write-Host "✅ Previous version restored" -ForegroundColor Green

# Step 4: Restart services
Write-Host "`n[4/5] Restarting services..." -ForegroundColor Yellow
pm2 restart all
Start-Sleep -Seconds 5
Write-Host "✅ Services restarted" -ForegroundColor Green

# Step 5: Verify rollback
Write-Host "`n[5/5] Verifying rollback..." -ForegroundColor Yellow

try {
    $health = Invoke-RestMethod -Uri "http://localhost:3000/health" -TimeoutSec 10
    if ($health.status -eq "operational") {
        Write-Host "✅ Health check passed" -ForegroundColor Green

        # Update version file
        $targetVersion.Name | Out-File "./.version"

        Write-Host ""
        Write-Host "=================================" -ForegroundColor Green
        Write-Host "✅ ROLLBACK SUCCESSFUL" -ForegroundColor Green
        Write-Host "=================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Rolled back to: $($targetVersion.Name)" -ForegroundColor White
    } else {
        throw "Health check failed"
    }
} catch {
    Write-Host "❌ Rollback verification failed: $_" -ForegroundColor Red
    Write-Host "Manual intervention required" -ForegroundColor Red
    exit 1
}
