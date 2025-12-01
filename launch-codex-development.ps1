# Codex Dominion - Full Stack Development Launcher
# This script launches the complete trading platform development environment

Write-Host "🚀 Starting Codex Dominion Full-Stack Development Environment" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Yellow

# Change to the project root directory
$projectRoot = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
Set-Location $projectRoot

Write-Host "📁 Project Root: $projectRoot" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "🐍 Python detected: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "🟢 Node.js detected: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Install Python dependencies if not already installed
Write-Host "`n📦 Checking Python dependencies..." -ForegroundColor Cyan
$pythonPackages = @(
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "psycopg2-binary",
    "sqlalchemy",
    "python-multipart",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "requests",
    "aiofiles"
)

foreach ($package in $pythonPackages) {
    try {
        $result = pip show $package 2>$null
        if ($result) {
            Write-Host "  ✅ $package (installed)" -ForegroundColor Green
        } else {
            Write-Host "  📥 Installing $package..." -ForegroundColor Yellow
            pip install $package --quiet
            Write-Host "  ✅ $package (installed)" -ForegroundColor Green
        }
    } catch {
        Write-Host "  ❌ Failed to install $package" -ForegroundColor Red
    }
}

# Setup Frontend dependencies
Write-Host "`n🎨 Setting up Next.js frontend..." -ForegroundColor Cyan
if (-not (Test-Path "frontend\node_modules")) {
    Set-Location frontend
    Write-Host "  📥 Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install --silent
    Set-Location ..
    Write-Host "  ✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ✅ Frontend dependencies already installed" -ForegroundColor Green
}

# Start the backend API server
Write-Host "`n🔧 Starting FastAPI Backend Server..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
    python -c "
import uvicorn
from codex_ledger_api import app

print('🚀 FastAPI server starting on http://localhost:8001')
print('📚 API Documentation available at http://localhost:8001/docs')
print('🔍 Interactive API Explorer at http://localhost:8001/redoc')

uvicorn.run(app, host='0.0.0.0', port=8001, reload=True)
"
}

# Wait a moment for the backend to start
Start-Sleep -Seconds 3

# Start the frontend development server
Write-Host "`n🎨 Starting Next.js Frontend Server..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\frontend"
    npm run dev
}

# Wait a moment for the frontend to start
Start-Sleep -Seconds 5

# Display service status
Write-Host "`n🌟 Codex Dominion Development Environment is Running!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "🔗 Services Available:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  📊 Trading Dashboard:    http://localhost:3000" -ForegroundColor White
Write-Host "     └─ Main Dashboard     http://localhost:3000/" -ForegroundColor Gray
Write-Host "     └─ Treasury           http://localhost:3000/treasury" -ForegroundColor Gray
Write-Host "     └─ Signals            http://localhost:3000/signals" -ForegroundColor Gray
Write-Host "     └─ AMM Pools          http://localhost:3000/amm" -ForegroundColor Gray
Write-Host "     └─ Portfolio          http://localhost:3000/portfolio" -ForegroundColor Gray
Write-Host "     └─ Store              http://localhost:3000/store" -ForegroundColor Gray
Write-Host ""
Write-Host "  🔧 Backend API:          http://localhost:8001" -ForegroundColor White
Write-Host "     └─ Health Check       http://localhost:8001/health" -ForegroundColor Gray
Write-Host "     └─ API Docs           http://localhost:8001/docs" -ForegroundColor Gray
Write-Host "     └─ ReDoc              http://localhost:8001/redoc" -ForegroundColor Gray
Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow

# Monitor services
Write-Host "`n🔍 Service Monitor (Press Ctrl+C to stop all services)" -ForegroundColor Cyan
Write-Host "Backend Job ID: $($backendJob.Id)" -ForegroundColor Gray
Write-Host "Frontend Job ID: $($frontendJob.Id)" -ForegroundColor Gray

try {
    # Keep the script running and monitor jobs
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Check backend job status
        $backendState = Get-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
        if ($backendState.State -eq "Failed" -or $backendState.State -eq "Stopped") {
            Write-Host "❌ Backend service has stopped unexpectedly" -ForegroundColor Red
            break
        }
        
        # Check frontend job status
        $frontendState = Get-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
        if ($frontendState.State -eq "Failed" -or $frontendState.State -eq "Stopped") {
            Write-Host "❌ Frontend service has stopped unexpectedly" -ForegroundColor Red
            break
        }
        
        Write-Host "." -NoNewline -ForegroundColor Green
    }
} catch {
    Write-Host "`n🛑 Stopping all services..." -ForegroundColor Yellow
}
finally {
    # Clean up jobs when script exits
    Write-Host "`n🧹 Cleaning up services..." -ForegroundColor Yellow
    
    try {
        Stop-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
        Remove-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
        Write-Host "  ✅ Backend service stopped" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Backend service cleanup failed" -ForegroundColor Yellow
    }
    
    try {
        Stop-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
        Remove-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
        Write-Host "  ✅ Frontend service stopped" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Frontend service cleanup failed" -ForegroundColor Yellow
    }
    
    Write-Host "`n👋 Codex Dominion development environment stopped." -ForegroundColor Cyan
}