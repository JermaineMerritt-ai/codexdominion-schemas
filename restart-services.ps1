# Quick service diagnostics and restart
Write-Host "🔧 Codex Services Diagnostic & Restart" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check current directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Cyan

# Check if we're in the right place
if (Test-Path "codex_capsules\main.py") {
    Write-Host "✅ Found capsules service files" -ForegroundColor Green
} else {
    Write-Host "❌ Capsules service files not found" -ForegroundColor Red
    Write-Host "Expected: codex_capsules\main.py" -ForegroundColor Yellow
    exit 1
}

if (Test-Path "frontend\package.json") {
    Write-Host "✅ Found frontend files" -ForegroundColor Green
} else {
    Write-Host "❌ Frontend files not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Yellow

# Kill any existing processes on our ports
Write-Host "Cleaning up existing processes..." -ForegroundColor Cyan
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*next*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Start capsules service
Write-Host "Starting Capsules API on port 8080..." -ForegroundColor Yellow
$capsulesJob = Start-Job -ScriptBlock {
    Set-Location $using:currentDir
    Set-Location "codex_capsules"
    python -m uvicorn main:app --host 0.0.0.0 --port 8080
}

# Start frontend service
Write-Host "Starting Frontend on port 3001..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:currentDir
    Set-Location "frontend"
    npx next dev -p 3001
}

# Wait for services to start
Write-Host "Waiting for services to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Test services
Write-Host ""
Write-Host "🧪 Testing services..." -ForegroundColor Yellow

# Test port connectivity
$port8080 = Test-NetConnection -ComputerName localhost -Port 8080 -InformationLevel Quiet
$port3001 = Test-NetConnection -ComputerName localhost -Port 3001 -InformationLevel Quiet

if ($port8080) {
    Write-Host "✅ Port 8080 (Capsules API): Accessible" -ForegroundColor Green
    
    # Test API endpoint
    try {
        $apiTest = Invoke-RestMethod -Uri "http://localhost:8080/api/capsules" -Method GET -TimeoutSec 5
        Write-Host "✅ Capsules API: Working ($($apiTest.Count) capsules)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Capsules API: Port open but API not responding" -ForegroundColor Yellow
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkGray
    }
} else {
    Write-Host "❌ Port 8080 (Capsules API): Not accessible" -ForegroundColor Red
}

if ($port3001) {
    Write-Host "✅ Port 3001 (Frontend): Accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Port 3001 (Frontend): Not accessible" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Service Status:" -ForegroundColor Green
Write-Host "• Capsules API: http://localhost:8080/api/capsules" -ForegroundColor Cyan
Write-Host "• Frontend: http://localhost:3001/capsules" -ForegroundColor Cyan
Write-Host "• Dashboard: http://localhost:3001/" -ForegroundColor Cyan

Write-Host ""
Write-Host "💡 Job IDs for monitoring:" -ForegroundColor Yellow
Write-Host "• Capsules Job: $($capsulesJob.Id)" -ForegroundColor Cyan
Write-Host "• Frontend Job: $($frontendJob.Id)" -ForegroundColor Cyan
Write-Host ""
Write-Host "To check job status: Get-Job" -ForegroundColor Gray
Write-Host "To stop jobs: Stop-Job -Id <JobId>" -ForegroundColor Gray