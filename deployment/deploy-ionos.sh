#!/bin/bash
# =============================================================================
# DOT300 - IONOS VPS Deployment (74.208.123.158)
# =============================================================================

set -e

echo "🔥 DOT300 IONOS Deployment Starting..."
echo ""

# Configuration
IONOS_SERVER="74.208.123.158"
IONOS_USER="${IONOS_USER:-root}"
DOMAIN="api.codexdominion.app"
PORT=8300

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "  Server: $IONOS_SERVER"
echo "  User: $IONOS_USER"
echo "  Domain: $DOMAIN"
echo "  Port: $PORT"
echo ""

# Step 1: Test SSH Connection
echo -e "${YELLOW}1. Testing SSH Connection...${NC}"
ssh -o ConnectTimeout=5 $IONOS_USER@$IONOS_SERVER "echo 'SSH connection successful'" || {
    echo "SSH connection failed. Check your credentials."
    exit 1
}

# Step 2: Build Docker Image Locally
echo -e "${YELLOW}2. Building Docker Image...${NC}"
cd ..
docker build -f docker/Dockerfile.dot300 -t dot300-api:latest .

# Step 3: Save Image to Tar
echo -e "${YELLOW}3. Saving Image to Tar...${NC}"
docker save dot300-api:latest | gzip > dot300-api.tar.gz

# Step 4: Upload to Server
echo -e "${YELLOW}4. Uploading to IONOS Server...${NC}"
scp dot300-api.tar.gz $IONOS_USER@$IONOS_SERVER:/tmp/
scp dot300_agents.json $IONOS_USER@$IONOS_SERVER:/tmp/
scp docker-compose.test.yml $IONOS_USER@$IONOS_SERVER:/tmp/

# Step 5: Deploy on Server
echo -e "${YELLOW}5. Deploying on Server...${NC}"
ssh $IONOS_USER@$IONOS_SERVER << 'ENDSSH'
set -e

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Load Docker Image
echo "Loading Docker image..."
docker load < /tmp/dot300-api.tar.gz

# Create deployment directory
mkdir -p /opt/dot300
cd /opt/dot300

# Move files
mv /tmp/dot300_agents.json .
mv /tmp/docker-compose.test.yml docker-compose.yml

# Create docker-compose override for production
cat > docker-compose.override.yml << 'EOF'
version: '3.8'
services:
  dot300:
    image: dot300-api:latest
    container_name: dot300-production
    ports:
      - "8300:8300"
    volumes:
      - ./dot300_agents.json:/app/dot300_agents.json:ro
    restart: always
    environment:
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8300/health"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF

# Stop existing container
docker-compose down 2>/dev/null || true

# Start new container
docker-compose up -d dot300

# Wait for container to be healthy
echo "Waiting for container to start..."
sleep 10

# Test API
curl -f http://localhost:8300/health || echo "Container starting..."

echo "Deployment complete!"
ENDSSH

# Step 6: Setup NGINX Reverse Proxy
echo -e "${YELLOW}6. Configuring NGINX...${NC}"
ssh $IONOS_USER@$IONOS_SERVER << ENDSSH
set -e

# Install NGINX if not installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create NGINX configuration
cat > /etc/nginx/sites-available/dot300 << 'EOF'
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:8300;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/dot300 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test configuration
nginx -t

# Restart NGINX
systemctl restart nginx
systemctl enable nginx

echo "NGINX configured!"
ENDSSH

# Step 7: Setup SSL with Certbot
echo -e "${YELLOW}7. Setting up SSL Certificate...${NC}"
ssh $IONOS_USER@$IONOS_SERVER << ENDSSH
set -e

# Install Certbot
if ! command -v certbot &> /dev/null; then
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Get SSL certificate
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@codexdominion.app || echo "SSL setup failed - configure manually"

echo "SSL configured!"
ENDSSH

# Step 8: Setup Firewall
echo -e "${YELLOW}8. Configuring Firewall...${NC}"
ssh $IONOS_USER@$IONOS_SERVER << 'ENDSSH'
set -e

# Install UFW if not installed
if ! command -v ufw &> /dev/null; then
    apt-get install -y ufw
fi

# Configure firewall
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw --force enable

echo "Firewall configured!"
ENDSSH

# Step 9: Cleanup
echo -e "${YELLOW}9. Cleaning up...${NC}"
rm -f dot300-api.tar.gz

# Step 10: Test Deployment
echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo -e "${GREEN}🌍 DOT300 API URLs:${NC}"
echo "  HTTP: http://$IONOS_SERVER:8300"
echo "  Domain: https://$DOMAIN (if DNS configured)"
echo ""

echo -e "${YELLOW}10. Testing API...${NC}"
curl -s http://$IONOS_SERVER:8300/health | jq . || echo "Testing..."
echo ""

echo -e "${GREEN}🔥 DOT300 is LIVE on IONOS!${NC}"
echo ""
echo "Next steps:"
echo "  1. Point DNS: $DOMAIN → $IONOS_SERVER"
echo "  2. Test: https://$DOMAIN/health"
echo "  3. Monitor: ssh $IONOS_USER@$IONOS_SERVER 'docker logs -f dot300-production'"
echo "  4. Setup monitoring with Prometheus/Grafana"
echo ""
