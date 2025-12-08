#!/bin/bash
set -e

echo "🔧 Fixing Codex Dominion Frontend Deployment"
echo "============================================="

DOMAIN="codexdominion.app"
BACKEND_URL="http://codex-backend.eastus.azurecontainer.io:8001"
APP_DIR="/opt/codex-dominion"

# Ensure SSL certificates are in place
echo "📋 Copying SSL certificates..."
mkdir -p $APP_DIR/ssl
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $APP_DIR/ssl/
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $APP_DIR/ssl/
chmod 644 $APP_DIR/ssl/*.pem

# Create Docker Compose file
echo "🐳 Creating docker-compose.yml..."
cat > $APP_DIR/docker-compose.yml <<'EOF'
version: '3.8'

services:
  frontend:
    image: jmerritt48/codex-dominion-frontend:2.0.0
    container_name: codex-frontend
    restart: unless-stopped
    environment:
      - NEXT_PUBLIC_API_URL=http://codex-backend.eastus.azurecontainer.io:8001
      - NODE_ENV=production
    networks:
      - codex-network

  nginx:
    image: nginx:alpine
    container_name: codex-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
    networks:
      - codex-network

networks:
  codex-network:
    driver: bridge
EOF

# Start services
echo "🚀 Starting services..."
cd $APP_DIR
docker-compose down 2>/dev/null || true
docker-compose pull
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 15

# Check status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Frontend: https://$DOMAIN"
echo "🔥 Backend: $BACKEND_URL/health"
echo ""
echo "Test with: curl -k https://$DOMAIN"
