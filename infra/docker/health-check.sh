#!/bin/bash
# Quick System Health Check Script

echo "=== CODEXDOMINION SYSTEM HEALTH CHECK ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Docker
if systemctl is-active --quiet docker; then
    echo -e "${GREEN}✓ Docker is running${NC}"
else
    echo -e "${RED}✗ Docker is not running${NC}"
fi

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is not running${NC}"
fi

echo ""
echo "=== Container Status ==="
docker-compose ps

echo ""
echo "=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "=== Disk Usage ==="
docker system df

echo ""
echo "=== SSL Certificate Status ==="
certbot certificates 2>/dev/null | grep -E "Certificate Name|Expiry Date" || echo "No certificates found"

echo ""
echo "=== Network Connectivity ==="
ENDPOINTS=(
    "https://codexdominion.app"
    "https://api.codexdominion.app"
    "https://dashboard.codexdominion.app"
    "https://monitoring.codexdominion.app"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -f -s -o /dev/null -w "%{http_code}" "$endpoint" | grep -q "200\|301\|302"; then
        echo -e "${GREEN}✓ $endpoint is accessible${NC}"
    else
        echo -e "${RED}✗ $endpoint is not accessible${NC}"
    fi
done

echo ""
echo "=== Recent Errors (last 10 lines) ==="
docker-compose logs --tail=10 2>&1 | grep -i "error\|fail\|fatal" || echo "No recent errors"

echo ""
echo "=== System Load ==="
uptime

echo ""
echo "Health check complete!"
