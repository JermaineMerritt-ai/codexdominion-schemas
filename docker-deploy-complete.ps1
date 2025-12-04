# 🔥 CODEX DOMINION - Complete Docker Deployment (Windows)
# Builds, tests, and deploys your dashboard with Docker

Write-Host "🔥 === CODEX DOMINION DOCKER DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "🕐 $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Configuration
$IMAGE_NAME = "codex-dominion-dashboard"
$CONTAINER_NAME = "codex-dashboard"
$HOST_PORT = "8080"
$CONTAINER_PORT = "8501"
$DATA_DIR = "$(pwd)\data"

Write-Host "🏗️ === BUILDING DOCKER IMAGE ===" -ForegroundColor Cyan

# Create data directory if it doesn't exist
if (!(Test-Path $DATA_DIR)) {
    New-Item -ItemType Directory -Path $DATA_DIR -Force
    Write-Host "📁 Created data directory: $DATA_DIR" -ForegroundColor Green
}

# Build the Docker image
Write-Host "🔨 Building Docker image: $IMAGE_NAME" -ForegroundColor Yellow
docker build -t $IMAGE_NAME .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully!" -ForegroundColor Green

# Stop existing container if running
Write-Host ""
Write-Host "🔄 === CONTAINER MANAGEMENT ===" -ForegroundColor Cyan

$existing = docker ps -aq --filter "name=$CONTAINER_NAME"
if ($existing) {
    Write-Host "🛑 Stopping existing container..." -ForegroundColor Yellow
    docker stop $CONTAINER_NAME | Out-Null
    docker rm $CONTAINER_NAME | Out-Null
    Write-Host "✅ Existing container removed" -ForegroundColor Green
}

# Run the container
Write-Host ""
Write-Host "🚀 === LAUNCHING CONTAINER ===" -ForegroundColor Cyan

Write-Host "🔥 Starting Codex Dominion Dashboard..." -ForegroundColor Yellow
Write-Host "   📍 Local Access: http://localhost:$HOST_PORT" -ForegroundColor White
Write-Host "   📁 Data Volume: $DATA_DIR" -ForegroundColor White

docker run -d `
    --name $CONTAINER_NAME `
    -p "${HOST_PORT}:${CONTAINER_PORT}" `
    -v "${DATA_DIR}:/app/data" `
    -e STREAMLIT_SERVER_HEADLESS=true `
    -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false `
    -e CODEX_ENV=production `
    --restart unless-stopped `
    $IMAGE_NAME

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container started successfully!" -ForegroundColor Green

    # Wait for container to be ready
    Write-Host "⏳ Waiting for dashboard to initialize..." -ForegroundColor Yellow
    Start-Sleep 5

    # Check container status
    $status = docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    Write-Host ""
    Write-Host "📊 === CONTAINER STATUS ===" -ForegroundColor Cyan
    Write-Host $status -ForegroundColor Green

    # Show logs
    Write-Host ""
    Write-Host "📋 === RECENT LOGS ===" -ForegroundColor Cyan
    docker logs --tail 10 $CONTAINER_NAME

    # Summary
    Write-Host ""
    Write-Host "🏁 === DEPLOYMENT COMPLETE ===" -ForegroundColor Green
    Write-Host "✅ Codex Dominion Dashboard is now running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔍 Access your dashboard:" -ForegroundColor Cyan
    Write-Host "   🌐 Web Interface: http://localhost:$HOST_PORT" -ForegroundColor White
    Write-Host "   📊 Container Status: docker ps" -ForegroundColor White
    Write-Host "   📋 View Logs: docker logs $CONTAINER_NAME" -ForegroundColor White
    Write-Host "   🛑 Stop Container: docker stop $CONTAINER_NAME" -ForegroundColor White
    Write-Host ""

    # Open browser (optional)
    $open_browser = Read-Host "Open dashboard in browser? (y/n)"
    if ($open_browser -eq "y") {
        Start-Process "http://localhost:$HOST_PORT"
    }

    Write-Host "🔥 Sacred flames now burn eternal in Docker! ✨" -ForegroundColor Magenta

} else {
    Write-Host "❌ Failed to start container!" -ForegroundColor Red
    Write-Host "🔍 Checking for issues..." -ForegroundColor Yellow
    docker logs $CONTAINER_NAME
    exit 1
}

# Optional: Cloud deployment info
Write-Host ""
Write-Host "☁️ === CLOUD DEPLOYMENT OPTIONS ===" -ForegroundColor Cyan
Write-Host "Ready to deploy to cloud? Here are your options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. 🌊 DigitalOcean:" -ForegroundColor White
Write-Host "   docker tag $IMAGE_NAME registry.digitalocean.com/your-registry/$IMAGE_NAME" -ForegroundColor Gray
Write-Host "   docker push registry.digitalocean.com/your-registry/$IMAGE_NAME" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 🚀 Heroku:" -ForegroundColor White
Write-Host "   heroku container:push web --app your-app-name" -ForegroundColor Gray
Write-Host "   heroku container:release web --app your-app-name" -ForegroundColor Gray
Write-Host ""
Write-Host "3. ☁️ AWS ECS/EC2:" -ForegroundColor White
Write-Host "   docker tag $IMAGE_NAME your-ecr-repo-uri" -ForegroundColor Gray
Write-Host "   docker push your-ecr-repo-uri" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 🔥 Manual VPS:" -ForegroundColor White
Write-Host "   docker save $IMAGE_NAME | gzip > codex-dashboard.tar.gz" -ForegroundColor Gray
Write-Host "   # Upload to your server and: docker load < codex-dashboard.tar.gz" -ForegroundColor Gray
