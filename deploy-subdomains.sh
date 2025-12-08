#!/bin/bash
# CodexDominion Subdomain Deployment Script
# Run this on your IONOS server after adding DNS A records

set -e

echo "=== CodexDominion Subdomain Deployment ==="
echo ""

# Configuration
DOMAIN="codexdominion.app"
SERVER_IP="74.208.123.158"
API_PORT="8000"
DASHBOARD_PORT="8501"
MONITORING_PORT="9090"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Checking DNS records...${NC}"
for subdomain in api dashboard monitoring; do
    echo "Checking $subdomain.$DOMAIN..."
    if host $subdomain.$DOMAIN > /dev/null 2>&1; then
        echo -e "${GREEN}✓ $subdomain.$DOMAIN DNS is configured${NC}"
    else
        echo "⚠ $subdomain.$DOMAIN DNS not found - please add A record pointing to $SERVER_IP"
        exit 1
    fi
done

echo ""
echo -e "${YELLOW}Step 2: Creating nginx configurations...${NC}"

# API subdomain configuration
cat > /etc/nginx/sites-available/api.codexdominion.app << 'EOF'
server {
    listen 80;
    server_name api.codexdominion.app;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # CORS headers for API
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
    }
}
EOF

# Dashboard subdomain configuration
cat > /etc/nginx/sites-available/dashboard.codexdominion.app << 'EOF'
server {
    listen 80;
    server_name dashboard.codexdominion.app;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# Monitoring subdomain configuration
cat > /etc/nginx/sites-available/monitoring.codexdominion.app << 'EOF'
server {
    listen 80;
    server_name monitoring.codexdominion.app;

    location / {
        proxy_pass http://localhost:9090;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

echo -e "${GREEN}✓ Nginx configurations created${NC}"

echo ""
echo -e "${YELLOW}Step 3: Enabling sites...${NC}"
ln -sf /etc/nginx/sites-available/api.codexdominion.app /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/dashboard.codexdominion.app /etc/nginx/sites-enabled/
ln -sf /etc/nginx/sites-available/monitoring.codexdominion.app /etc/nginx/sites-enabled/
echo -e "${GREEN}✓ Sites enabled${NC}"

echo ""
echo -e "${YELLOW}Step 4: Testing nginx configuration...${NC}"
nginx -t
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Nginx configuration is valid${NC}"
    systemctl reload nginx
    echo -e "${GREEN}✓ Nginx reloaded${NC}"
else
    echo "✗ Nginx configuration error"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 5: Obtaining SSL certificates...${NC}"
certbot --nginx -d api.codexdominion.app -d dashboard.codexdominion.app -d monitoring.codexdominion.app --non-interactive --agree-tos --email admin@codexdominion.app

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSL certificates obtained and configured${NC}"
else
    echo "⚠ SSL certificate setup had issues - you may need to run certbot manually"
fi

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""
echo "Your subdomains are now configured:"
echo "  • https://api.codexdominion.app (proxies to localhost:$API_PORT)"
echo "  • https://dashboard.codexdominion.app (proxies to localhost:$DASHBOARD_PORT)"
echo "  • https://monitoring.codexdominion.app (proxies to localhost:$MONITORING_PORT)"
echo ""
echo "Next steps:"
echo "  1. Ensure your API is running on port $API_PORT"
echo "  2. Ensure your dashboard is running on port $DASHBOARD_PORT"
echo "  3. Ensure your monitoring service is running on port $MONITORING_PORT"
echo ""
