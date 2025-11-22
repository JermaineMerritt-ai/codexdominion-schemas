#!/bin/bash
# 🔥 Codex Docker Deployment Script

echo "🔥 === CODEX DOMINION DOCKER DEPLOYMENT ==="
echo "🕐 $(date)"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs ssl nginx

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found in current directory"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in current directory"
    exit 1
fi

# Check if codex_dashboard.py exists
if [ ! -f "codex_dashboard.py" ]; then
    echo "❌ codex_dashboard.py not found in current directory"
    exit 1
fi

echo "✅ Required files found"

# Build Docker image
echo "🏗️  Building Codex Dashboard image..."
docker build -t codex-dashboard:latest . || {
    echo "❌ Docker build failed"
    exit 1
}

echo "✅ Docker image built successfully"

# Choose deployment method
echo
echo "Select deployment method:"
echo "1. Simple (codex_dashboard.py only)"
echo "2. Full (with nginx reverse proxy)"
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🚀 Starting simple deployment..."
        docker-compose -f docker-compose-simple.yml up -d
        ;;
    2)
        echo "🚀 Starting full deployment with nginx..."
        docker-compose up -d
        ;;
    *)
        echo "❌ Invalid choice. Using simple deployment..."
        docker-compose -f docker-compose-simple.yml up -d
        ;;
esac

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:8501/_stcore/health >/dev/null 2>&1; then
    echo "✅ Production service (8501) is healthy"
else
    echo "⚠️  Production service (8501) may not be ready yet"
fi

if curl -f http://localhost:8502/_stcore/health >/dev/null 2>&1; then
    echo "✅ Staging service (8502) is healthy"
else
    echo "⚠️  Staging service (8502) may not be ready yet"
fi

# Show running containers
echo
echo "📊 Running containers:"
docker ps --filter "name=codex"

echo
echo "🏁 === DEPLOYMENT COMPLETE ==="
echo "🔍 Access your Codex Dashboard:"
echo "   Production: http://localhost:8501"
echo "   Staging: http://localhost:8502"
echo
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Update: docker-compose pull && docker-compose up -d"
echo
echo "🔥 Sacred flames now burn in containers! ✨"