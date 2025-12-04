# Frontend Capsules Integration Setup
# Run this script to test the capsules page integration

Write-Host "🚀 Setting up Codex Capsules Frontend Integration..." -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "frontend")) {
    Write-Host "❌ Run this from the codex-dominion root directory" -ForegroundColor Red
    Write-Host "Expected structure: codex-dominion/frontend/" -ForegroundColor Cyan
    exit 1
}

# 1. Check if capsules service is running
Write-Host "1. Checking Capsules API service..." -ForegroundColor Yellow
try {
    $capsulesHealth = Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET -TimeoutSec 5
    Write-Host "✅ Capsules service is running: $($capsulesHealth.service)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Capsules service not running. Starting it..." -ForegroundColor Yellow

    # Check if the capsules directory exists
    if (Test-Path "codex_capsules") {
        Write-Host "Starting capsules service in background..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-Command", "cd codex_capsules; python -m uvicorn main:app --host 0.0.0.0 --port 8080" -WindowStyle Hidden

        # Wait for startup
        Write-Host "Waiting for service to start..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5

        try {
            $capsulesHealth = Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET -TimeoutSec 5
            Write-Host "✅ Capsules service started successfully!" -ForegroundColor Green
        } catch {
            Write-Host "❌ Could not start capsules service. Please start it manually:" -ForegroundColor Red
            Write-Host "   cd codex_capsules && python -m uvicorn main:app --port 8080" -ForegroundColor Cyan
        }
    } else {
        Write-Host "❌ Capsules directory not found. Please ensure the capsules service is set up." -ForegroundColor Red
    }
}

# 2. Check frontend dependencies
Write-Host ""
Write-Host "2. Checking frontend setup..." -ForegroundColor Yellow
Set-Location frontend

if (!(Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    npm install
} else {
    Write-Host "✅ Frontend dependencies already installed" -ForegroundColor Green
}

# 3. Verify capsules pages exist
Write-Host ""
Write-Host "3. Verifying capsules pages..." -ForegroundColor Yellow

$pagesCreated = @()
if (Test-Path "pages/capsules.tsx") {
    $pagesCreated += "capsules.tsx (Enhanced)"
    Write-Host "✅ Enhanced capsules page found" -ForegroundColor Green
}
if (Test-Path "pages/capsules-simple.tsx") {
    $pagesCreated += "capsules-simple.tsx (Simple)"
    Write-Host "✅ Simple capsules page found" -ForegroundColor Green
}
if (Test-Path "pages/test-capsules.tsx") {
    $pagesCreated += "test-capsules.tsx (Test)"
    Write-Host "✅ Test capsules page found" -ForegroundColor Green
}

# 4. Start frontend dev server
Write-Host ""
Write-Host "4. Frontend development server..." -ForegroundColor Yellow
Write-Host "To start the frontend server, run:" -ForegroundColor Cyan
Write-Host "   cd frontend && npm run dev" -ForegroundColor White
Write-Host ""

Write-Host "📋 Summary of created pages:" -ForegroundColor Green
foreach ($page in $pagesCreated) {
    Write-Host "   • $page" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Green
Write-Host "1. Start frontend: cd frontend && npm run dev" -ForegroundColor Cyan
Write-Host "2. Visit: http://localhost:3000/capsules" -ForegroundColor Cyan
Write-Host "3. Test API: http://localhost:8080/api/capsules" -ForegroundColor Cyan
Write-Host ""
Write-Host "🏛️ The capsules page shows all registered operational capsules!" -ForegroundColor Green
Write-Host "   - View registered capsules (engines, ceremonies, etc.)" -ForegroundColor Cyan
Write-Host "   - Track execution runs and artifacts" -ForegroundColor Cyan
Write-Host "   - Monitor operational sovereignty metrics" -ForegroundColor Cyan
