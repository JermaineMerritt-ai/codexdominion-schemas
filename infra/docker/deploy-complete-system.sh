#!/bin/bash
# CodexDominion Complete System Deployment
# This script automates the entire deployment process

set -e

echo "=============================================="
echo "  CODEXDOMINION COMPLETE SYSTEM DEPLOYMENT"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="codexdominion.app"
SERVER_IP="74.208.123.158"
COMPOSE_FILE="docker-compose.yml"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: System Prerequisites${NC}"
echo "Updating system packages..."
apt update -qq && apt upgrade -y -qq

# Install required packages
PACKAGES=("docker.io" "docker-compose" "nginx" "certbot" "python3-certbot-nginx" "curl" "git")
for pkg in "${PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $pkg "; then
        echo "Installing $pkg..."
        apt install -y $pkg -qq
    fi
done

# Start Docker
systemctl enable docker
systemctl start docker

echo -e "${GREEN}✓ Prerequisites installed${NC}"
echo ""

echo -e "${BLUE}Step 2: DNS Verification${NC}"
SUBDOMAINS=("api" "dashboard" "monitoring")
DNS_OK=true

for sub in "${SUBDOMAINS[@]}"; do
    if host $sub.$DOMAIN > /dev/null 2>&1; then
        echo -e "${GREEN}✓ $sub.$DOMAIN DNS configured${NC}"
    else
        echo -e "${YELLOW}⚠ $sub.$DOMAIN DNS not found (continuing anyway)${NC}"
    fi
done

echo ""

echo -e "${BLUE}Step 3: Creating Directory Structure${NC}"
mkdir -p {data,logs/{api,cosmic},nginx/{conf.d,ssl,cache},grafana/{dashboards,datasources},monitoring,wp-content,mysql-config}
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

echo -e "${BLUE}Step 4: Prometheus Configuration${NC}"
cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'docker'
    static_configs:
      - targets: ['172.28.0.1:9323']

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
EOF

echo -e "${GREEN}✓ Prometheus configured${NC}"
echo ""

echo -e "${BLUE}Step 5: MySQL Configuration${NC}"
cat > mysql-config/my.cnf << 'EOF'
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 512M
innodb_log_file_size = 128M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT
query_cache_type = 1
query_cache_size = 32M
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
EOF

echo -e "${GREEN}✓ MySQL configured${NC}"
echo ""

echo -e "${BLUE}Step 6: PHP Upload Settings${NC}"
cat > php-uploads.ini << 'EOF'
upload_max_filesize = 100M
post_max_size = 100M
max_execution_time = 300
max_input_time = 300
memory_limit = 256M
EOF

echo -e "${GREEN}✓ PHP configured${NC}"
echo ""

echo -e "${BLUE}Step 7: Environment Variables${NC}"
if [ ! -f .env ]; then
    cat > .env << EOF
# Database
DB_ROOT_PASSWORD=$(openssl rand -base64 32)
DB_PASSWORD=$(openssl rand -base64 32)

# Grafana
GRAFANA_PASSWORD=$(openssl rand -base64 16)

# Application
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.${DOMAIN}
NEXT_PUBLIC_DOMAIN=https://${DOMAIN}
EOF
    echo -e "${GREEN}✓ Environment file created${NC}"
else
    echo -e "${YELLOW}⚠ .env already exists, skipping${NC}"
fi

echo ""

echo -e "${BLUE}Step 8: Docker Compose Deployment${NC}"
echo "Pulling Docker images..."
docker-compose pull

echo "Building custom images..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo -e "${GREEN}✓ Services started${NC}"
echo ""

echo -e "${BLUE}Step 9: Waiting for services to be healthy...${NC}"
sleep 30

# Check service health
SERVICES=("codex-web" "codex-api" "codex-db" "codex-redis" "codex-nginx")
for service in "${SERVICES[@]}"; do
    if docker ps | grep -q $service; then
        echo -e "${GREEN}✓ $service is running${NC}"
    else
        echo -e "${RED}✗ $service failed to start${NC}"
    fi
done

echo ""

echo -e "${BLUE}Step 10: SSL Certificate Setup${NC}"
if [ -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ]; then
    echo -e "${YELLOW}SSL certificate already exists for $DOMAIN${NC}"
else
    echo "Obtaining SSL certificates..."
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
fi

# Obtain certificates for subdomains
for sub in "${SUBDOMAINS[@]}"; do
    if host $sub.$DOMAIN > /dev/null 2>&1; then
        if [ ! -f /etc/letsencrypt/live/$sub.$DOMAIN/fullchain.pem ]; then
            certbot --nginx -d $sub.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
        fi
    fi
done

echo -e "${GREEN}✓ SSL certificates configured${NC}"
echo ""

echo -e "${BLUE}Step 11: Setting up monitoring dashboards${NC}"
# Copy pre-configured Grafana dashboards if they exist
if [ -d "./grafana-dashboards" ]; then
    cp -r ./grafana-dashboards/* ./grafana/dashboards/
fi

echo -e "${GREEN}✓ Monitoring configured${NC}"
echo ""

echo -e "${GREEN}=============================================="
echo "  DEPLOYMENT COMPLETE!"
echo "==============================================${NC}"
echo ""
echo "Your services are available at:"
echo "  • Main Site:    https://$DOMAIN"
echo "  • API:          https://api.$DOMAIN"
echo "  • Dashboard:    https://dashboard.$DOMAIN"
echo "  • Monitoring:   https://monitoring.$DOMAIN"
echo "  • WordPress:    http://$SERVER_IP:8080"
echo "  • Grafana:      http://$SERVER_IP:3001"
echo ""
echo "Service Status:"
docker-compose ps
echo ""
echo "Useful Commands:"
echo "  • View logs:     docker-compose logs -f [service-name]"
echo "  • Restart:       docker-compose restart [service-name]"
echo "  • Stop all:      docker-compose down"
echo "  • Start all:     docker-compose up -d"
echo "  • Check health:  docker-compose ps"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Configure WordPress at http://$SERVER_IP:8080"
echo "  2. Set up Grafana dashboards at http://$SERVER_IP:3001"
echo "  3. Deploy your application code to ./web and ./api"
echo "  4. Run: docker-compose restart web api"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
