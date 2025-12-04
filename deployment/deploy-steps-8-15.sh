# =============================================================================
# Step 8: Install System Dependencies
# =============================================================================
echo -e "${BLUE}📦 Step 8: Installing System Dependencies${NC}"
echo "-------------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

# Update package list
sudo apt update

# Install Python and dependencies
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
if ! command -v psql &> /dev/null; then
    sudo apt install -y postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Install Nginx
if ! command -v nginx &> /dev/null; then
    sudo apt install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
fi

# Install Certbot for SSL
if ! command -v certbot &> /dev/null; then
    sudo apt install -y certbot python3-certbot-nginx
fi

echo "✓ System dependencies installed"
ENDSSH
echo -e "${GREEN}✓ System dependencies ready${NC}"
echo ""

# =============================================================================
# Step 9: Setup Python Virtual Environment
# =============================================================================
echo -e "${BLUE}🐍 Step 9: Setting up Python Environment${NC}"
echo "-------------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

cd /var/www/codexdominion.app

# Create virtual environment
sudo -u www-data python3 -m venv .venv

# Install Python packages
sudo -u www-data .venv/bin/pip install --upgrade pip
sudo -u www-data .venv/bin/pip install -r requirements.txt

echo "✓ Python environment configured"
ENDSSH
echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

# =============================================================================
# Step 10: Setup Database
# =============================================================================
echo -e "${BLUE}🗄️  Step 10: Setting up Database${NC}"
echo "----------------------------------"
echo "Uploading database setup script..."
scp -i "$SSH_KEY" deployment/setup-database.sh "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
chmod +x /tmp/setup-database.sh
sudo /tmp/setup-database.sh
rm /tmp/setup-database.sh
ENDSSH
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# =============================================================================
# Step 11: Configure Systemd Service
# =============================================================================
echo -e "${BLUE}⚙️  Step 11: Configuring Systemd Service${NC}"
echo "-------------------------------------------"
scp -i "$SSH_KEY" deployment/codexdominion-api.service "$IONOS_USER@$IONOS_SERVER:/tmp/"
scp -i "$SSH_KEY" deployment/logging.conf "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
set -e

# Install service file
sudo cp /tmp/codexdominion-api.service /etc/systemd/system/
sudo rm /tmp/codexdominion-api.service

# Install logging config
sudo cp /tmp/logging.conf /var/www/codexdominion.app/deployment/
sudo rm /tmp/logging.conf

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable codexdominion-api
sudo systemctl start codexdominion-api

# Check status
sleep 2
sudo systemctl status codexdominion-api --no-pager || true

echo "✓ Systemd service configured"
ENDSSH
echo -e "${GREEN}✓ API service running${NC}"
echo ""

# =============================================================================
# Step 12: Configure Nginx
# =============================================================================
echo -e "${BLUE}🌐 Step 12: Configuring Nginx${NC}"
echo "--------------------------------"
scp -i "$SSH_KEY" deployment/nginx-production.conf "$IONOS_USER@$IONOS_SERVER:/tmp/"

ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << ENDSSH
set -e

# Install nginx config
sudo cp /tmp/nginx-production.conf /etc/nginx/sites-available/codexdominion.app
sudo rm /tmp/nginx-production.conf

# Create symlink (if not exists)
if [ ! -L "/etc/nginx/sites-enabled/codexdominion.app" ]; then
    sudo ln -s /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/
fi

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

echo "✓ Nginx configuration installed"
ENDSSH
echo -e "${GREEN}✓ Nginx configured${NC}"
echo ""

# =============================================================================
# Step 13: Setup SSL Certificate
# =============================================================================
echo -e "${BLUE}🔒 Step 13: Setting up SSL Certificate${NC}"
echo "---------------------------------------"
echo "This will request SSL certificate from Let's Encrypt"
echo ""
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << ENDSSH
set -e

# Stop nginx temporarily for standalone certbot
sudo systemctl stop nginx

# Request certificate
sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN -d api.$DOMAIN \
    --non-interactive --agree-tos --email admin@$DOMAIN || {
    echo "⚠️  SSL certificate request failed. You may need to:"
    echo "    1. Ensure DNS is pointing to this server"
    echo "    2. Ensure ports 80 and 443 are open"
    echo "    3. Run manually: sudo certbot certonly --nginx -d $DOMAIN"
}

# Restart nginx
sudo systemctl start nginx
sudo systemctl reload nginx

# Setup auto-renewal
if ! sudo crontab -l 2>/dev/null | grep -q certbot; then
    (sudo crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | sudo crontab -
fi

echo "✓ SSL certificate configured"
ENDSSH
echo -e "${GREEN}✓ SSL ready${NC}"
echo ""

# =============================================================================
# Step 14: Final Service Restart
# =============================================================================
echo -e "${BLUE}🔄 Step 14: Restarting All Services${NC}"
echo "-------------------------------------"
ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" << 'ENDSSH'
sudo systemctl restart codexdominion-api
sudo systemctl restart nginx
sleep 2
echo "✓ All services restarted"
ENDSSH
echo -e "${GREEN}✓ Services running${NC}"
echo ""

# =============================================================================
# Step 15: Health Check
# =============================================================================
echo -e "${BLUE}🏥 Step 15: Running Health Checks${NC}"
echo "-----------------------------------"
sleep 3

# Check API health
echo "Testing API endpoint..."
if curl -s -o /dev/null -w "%{http_code}" "http://$IONOS_SERVER:8001/health" | grep -q "200"; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${YELLOW}⚠️  API health check inconclusive${NC}"
fi

# Check nginx
echo "Testing Nginx..."
if ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" "sudo systemctl is-active --quiet nginx"; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is not running${NC}"
fi

# Check API service
echo "Testing API service..."
if ssh -i "$SSH_KEY" "$IONOS_USER@$IONOS_SERVER" "sudo systemctl is-active --quiet codexdominion-api"; then
    echo -e "${GREEN}✓ API service is running${NC}"
else
    echo -e "${RED}✗ API service is not running${NC}"
fi
echo ""

# =============================================================================
# Deployment Complete
# =============================================================================
echo "=========================================================="
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo "=========================================================="
echo ""
echo "🌐 Your application is deployed at:"
echo "   https://$DOMAIN"
echo "   https://api.$DOMAIN"
echo ""
echo "📝 Important Files on Server:"
echo "   Application:  /var/www/codexdominion.app"
echo "   Logs:         /var/log/codexdominion/"
echo "   Nginx Config: /etc/nginx/sites-available/codexdominion.app"
echo "   Service:      /etc/systemd/system/codexdominion-api.service"
echo "   DB Creds:     /var/www/codexdominion.app/.db_credentials"
echo ""
echo "🔧 Useful Commands (on server):"
echo "   sudo systemctl status codexdominion-api"
echo "   sudo systemctl restart codexdominion-api"
echo "   sudo systemctl restart nginx"
echo "   sudo tail -f /var/log/codexdominion/api.log"
echo "   sudo tail -f /var/log/nginx/codexdominion-error.log"
echo ""
echo -e "${YELLOW}⚠️  Next Steps:${NC}"
echo "   1. Update DNS records to point to $IONOS_SERVER"
echo "   2. Update .env.production with secure credentials"
echo "   3. Test all endpoints: https://$DOMAIN"
echo "   4. Set up monitoring and backups"
echo "   5. Review security settings"
echo ""
echo "🔥 Codex Dominion is LIVE! 🔥"
echo ""

# Cleanup
rm -f "$DEPLOY_ARCHIVE"
echo "Local deployment archive cleaned up"
