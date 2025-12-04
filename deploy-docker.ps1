# 🔥 Codex Docker Deployment Script (PowerShell)
# Deploy Codex Dominion Dashboard with Docker on Windows

Write-Host "🔥 === CODEX DOMINION DOCKER DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "🕐 $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose not found. Please install Docker Desktop with Compose." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data", "logs", "ssl", "nginx" | Out-Null

# Check required files
$requiredFiles = @("Dockerfile", "requirements.txt", "codex_dashboard.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        exit 1
    }
}

# Build Docker image
Write-Host "🏗️  Building Codex Dashboard image..." -ForegroundColor Yellow
docker build -t codex-dashboard:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Choose deployment method
Write-Host ""
Write-Host "Select deployment method:" -ForegroundColor Cyan
Write-Host "1. Simple (codex_dashboard.py only)"
Write-Host "2. Full (with nginx reverse proxy)"
$choice = Read-Host "Enter choice (1 or 2)"

switch ($choice) {
    "1" {
        Write-Host "🚀 Starting simple deployment..." -ForegroundColor Yellow
        docker-compose -f docker-compose-simple.yml up -d
    }
    "2" {
        Write-Host "🚀 Starting full deployment with nginx..." -ForegroundColor Yellow
        docker-compose up -d
    }
    default {
        Write-Host "❌ Invalid choice. Using simple deployment..." -ForegroundColor Red
        docker-compose -f docker-compose-simple.yml up -d
    }
}

# Wait for services to start
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Production service (8501) is healthy" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Production service (8501) may not be ready yet" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8502/_stcore/health" -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Staging service (8502) is healthy" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Staging service (8502) may not be ready yet" -ForegroundColor Yellow
}

# Show running containers
Write-Host ""
Write-Host "📊 Running containers:" -ForegroundColor Cyan
docker ps --filter "name=codex"

Write-Host ""
Write-Host "🏁 === DEPLOYMENT COMPLETE ===" -ForegroundColor Green
Write-Host "🔍 Access your Codex Dashboard:" -ForegroundColor Cyan
Write-Host "   Production: http://localhost:8501" -ForegroundColor White
Write-Host "   Staging: http://localhost:8502" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Cyan
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop services: docker-compose down" -ForegroundColor White
Write-Host "   Restart: docker-compose restart" -ForegroundColor White
Write-Host "   Update: docker-compose pull; docker-compose up -d" -ForegroundColor White
Write-Host ""
Write-Host "🔥 Sacred flames now burn in containers! ✨" -ForegroundColor Magenta
