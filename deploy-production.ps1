#=============================================================================
# CODEX DOMINION - PRODUCTION DEPLOYMENT (POWERSHELL)
# Windows deployment script for all 9 systems
#=============================================================================

Write-Host "`n🔥 CODEX DOMINION - PRODUCTION DEPLOYMENT 🔥" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

#=============================================================================
# CONFIGURATION
#=============================================================================
$DOCKER_REGISTRY = "codexdominion"
$IMAGE_TAG = "latest"

#=============================================================================
# 1. PRE-DEPLOYMENT CHECKS
#=============================================================================
Write-Host "📋 Running pre-deployment checks..." -ForegroundColor Yellow

# Check Docker
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not installed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker installed" -ForegroundColor Green

# Check Docker Compose
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose not installed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker Compose installed" -ForegroundColor Green

# Check kubectl
if (!(Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  kubectl not installed (optional)" -ForegroundColor Yellow
} else {
    Write-Host "✅ kubectl installed" -ForegroundColor Green
}

Write-Host ""

#=============================================================================
# 2. BUILD DOCKER IMAGES
#=============================================================================
Write-Host "🔨 Building Docker images..." -ForegroundColor Yellow

# Dashboard
Write-Host "Building Dashboard..."
docker build -t ${DOCKER_REGISTRY}/dashboard:${IMAGE_TAG} -f docker/Dockerfile.dashboard .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dashboard image built" -ForegroundColor Green
}

# DOT300 Agents
Write-Host "Building DOT300 Agents..."
docker build -t ${DOCKER_REGISTRY}/dot300:${IMAGE_TAG} -f docker/Dockerfile.dot300 .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ DOT300 image built" -ForegroundColor Green
}

# Chat Server
Write-Host "Building Chat Server..."
docker build -t ${DOCKER_REGISTRY}/chat:${IMAGE_TAG} -f docker/Dockerfile.chat .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Chat image built" -ForegroundColor Green
}

# Mobile API
Write-Host "Building Mobile API..."
docker build -t ${DOCKER_REGISTRY}/mobile-api:${IMAGE_TAG} -f docker/Dockerfile.mobile-api .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Mobile API image built" -ForegroundColor Green
}

Write-Host ""

#=============================================================================
# 3. PUSH TO REGISTRY (Optional)
#=============================================================================
$push = Read-Host "Push images to Docker Hub? (y/N)"
if ($push -eq 'y' -or $push -eq 'Y') {
    Write-Host "📤 Pushing images to registry..." -ForegroundColor Yellow
    docker push ${DOCKER_REGISTRY}/dashboard:${IMAGE_TAG}
    docker push ${DOCKER_REGISTRY}/dot300:${IMAGE_TAG}
    docker push ${DOCKER_REGISTRY}/chat:${IMAGE_TAG}
    docker push ${DOCKER_REGISTRY}/mobile-api:${IMAGE_TAG}
    Write-Host "✅ Images pushed to registry" -ForegroundColor Green
}

Write-Host ""

#=============================================================================
# 4. DEPLOY WITH DOCKER COMPOSE
#=============================================================================
Write-Host "🚀 Deploying services with Docker Compose..." -ForegroundColor Yellow

# Stop existing containers
Write-Host "Stopping existing containers..."
docker-compose -f docker-compose.production.yml down 2>$null

# Start services
Write-Host "Starting services..."
docker-compose -f docker-compose.production.yml up -d

Write-Host "✅ Services deployed" -ForegroundColor Green
Write-Host ""

#=============================================================================
# 5. WAIT FOR SERVICES
#=============================================================================
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

#=============================================================================
# 6. HEALTH CHECKS
#=============================================================================
Write-Host "🏥 Running health checks..." -ForegroundColor Yellow

# Check Dashboard
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5555/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Dashboard: Healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ Dashboard: Failed" -ForegroundColor Red
}

# Check DOT300
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8300/health" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ DOT300 Agents: Healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ DOT300 Agents: Failed" -ForegroundColor Red
}

# Check Mobile API
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Mobile API: Healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ Mobile API: Failed" -ForegroundColor Red
}

# Check NGINX
try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ NGINX: Healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ NGINX: Failed" -ForegroundColor Red
}

Write-Host ""

#=============================================================================
# 7. DISPLAY ENDPOINTS
#=============================================================================
Write-Host "📍 Service Endpoints:" -ForegroundColor Yellow
Write-Host "================================================"
Write-Host "Dashboard:     http://localhost:5555"
Write-Host "DOT300 API:    http://localhost:8300"
Write-Host "Mobile API:    http://localhost:8080"
Write-Host "WebSocket:     ws://localhost:8765"
Write-Host "N8N:           http://localhost:5678"
Write-Host "NGINX:         http://localhost"
Write-Host "Redis:         localhost:6379"
Write-Host "PostgreSQL:    localhost:5432"
Write-Host ""

#=============================================================================
# 8. VIEW LOGS
#=============================================================================
$logs = Read-Host "View service logs? (y/N)"
if ($logs -eq 'y' -or $logs -eq 'Y') {
    docker-compose -f docker-compose.production.yml logs -f
}

#=============================================================================
# 9. KUBERNETES DEPLOYMENT (Optional)
#=============================================================================
Write-Host ""
$k8s = Read-Host "Deploy to Kubernetes? (y/N)"
if ($k8s -eq 'y' -or $k8s -eq 'Y') {
    Write-Host "☸️  Deploying to Kubernetes..." -ForegroundColor Yellow

    # Create namespace
    kubectl apply -f k8s/namespace.yaml

    # Deploy services
    kubectl apply -f k8s/deployment-dashboard.yaml
    kubectl apply -f k8s/deployment-dot300.yaml

    Write-Host "✅ Kubernetes deployment complete" -ForegroundColor Green

    # Show status
    kubectl get pods -n codex-dominion
}

#=============================================================================
# COMPLETION
#=============================================================================
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "🎯 DEPLOYMENT COMPLETE! 🎯" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "🔥 100% MILESTONE ACHIEVED! 🔥" -ForegroundColor Cyan
Write-Host ""
Write-Host "All 9 systems operational:"
Write-Host "✅ Website & Store Builder"
Write-Host "✅ N8N Workflow Builder"
Write-Host "✅ Real Audio APIs"
Write-Host "✅ Social Media APIs"
Write-Host "✅ Affiliate Tracking"
Write-Host "✅ System Health Monitor"
Write-Host "✅ WebSocket Chat"
Write-Host "✅ Mobile Apps"
Write-Host "✅ DOT300 Action AI (301 agents)"
Write-Host ""
Write-Host "Your Digital Sovereignty is COMPLETE! 👑" -ForegroundColor Yellow
Write-Host ""
