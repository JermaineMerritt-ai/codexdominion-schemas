#!/bin/bash
# 🔥 COSMIC DOMINION - DEPLOYMENT SCRIPT 🔥
# Deploy the complete cosmic dashboard suite to production server

echo "🔥 COSMIC DOMINION DEPLOYMENT SCRIPT 🔥"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="aistorelab.com"
PROJECT_DIR="/var/www/cosmic-dominion"
NGINX_CONFIG="/etc/nginx/sites-available/cosmic-dominion"
SYSTEMD_DIR="/etc/systemd/system"
USER="www-data"

echo -e "${BLUE}🌟 Starting Cosmic Dominion deployment...${NC}"

# 1. Update system packages
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Install required packages
echo -e "${YELLOW}⚙️ Installing required packages...${NC}"
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

# 3. Create project directory
echo -e "${YELLOW}📁 Setting up project directory...${NC}"
sudo mkdir -p $PROJECT_DIR
sudo chown -R $USER:$USER $PROJECT_DIR

# 4. Clone/copy project files
echo -e "${YELLOW}📋 Deploying project files...${NC}"
# If deploying from git:
# sudo -u $USER git clone https://github.com/yourusername/codex-dominion.git $PROJECT_DIR
# Or copy files manually

# 5. Set up Python environment
echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
cd $PROJECT_DIR
sudo -u $USER python3 -m venv venv
sudo -u $USER ./venv/bin/pip install --upgrade pip
sudo -u $USER ./venv/bin/pip install streamlit pandas pathlib

# 6. Create systemd service files for each dashboard
echo -e "${YELLOW}⚙️ Creating systemd services...${NC}"

# Install systemd services using the comprehensive installer
echo -e "${YELLOW}⚙️ Installing systemd services...${NC}"

# Copy systemd service files
sudo mkdir -p $SYSTEMD_DIR
sudo cp systemd/cosmic-dashboard.service $SYSTEMD_DIR/
sudo cp systemd/cosmic-ledger.service $SYSTEMD_DIR/
sudo cp systemd/cosmic-rhythm.service $SYSTEMD_DIR/

# Set proper permissions
sudo chmod 644 $SYSTEMD_DIR/cosmic-*.service
sudo chown root:root $SYSTEMD_DIR/cosmic-*.service

# Run the comprehensive service installer
chmod +x install_services.sh
./install_services.sh

# 7. Enable and start services
echo -e "${YELLOW}🚀 Starting cosmic services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable cosmic-dashboard.service
sudo systemctl enable cosmic-ledger.service
sudo systemctl enable cosmic-rhythm.service
sudo systemctl start cosmic-dashboard.service
sudo systemctl start cosmic-ledger.service
sudo systemctl start cosmic-rhythm.service

# 8. Configure Nginx
echo -e "${YELLOW}🌐 Configuring Nginx...${NC}"
sudo cp nginx_config.conf $NGINX_CONFIG
sudo ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 9. Set up SSL with Certbot
echo -e "${YELLOW}🔒 Setting up SSL certificates...${NC}"
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Enable automatic certificate renewal
echo -e "${YELLOW}🔄 Setting up automatic SSL renewal...${NC}"
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test certificate renewal
echo -e "${YELLOW}🧪 Testing SSL renewal process...${NC}"
sudo certbot renew --dry-run

# 10. Create firewall rules
echo -e "${YELLOW}🛡️ Configuring firewall...${NC}"
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# 11. Create deployment status check
cat << EOF | sudo tee /usr/local/bin/cosmic-status
#!/bin/bash
echo "🔥 COSMIC DOMINION STATUS 🔥"
echo "============================"
echo "📊 Main Dashboard: \$(systemctl is-active cosmic-main.service)"
echo "📋 Sacred Ledger: \$(systemctl is-active cosmic-ledger.service)"
echo "🎵 Cosmic Rhythm: \$(systemctl is-active cosmic-rhythm.service)"
echo "🌐 Nginx Status: \$(systemctl is-active nginx)"
echo "🔒 SSL Status: \$(certbot certificates | grep -c 'Certificate Name')"
echo ""
echo "🌍 Live URLs:"
echo "   Main: https://$DOMAIN"
echo "   Ledger: https://$DOMAIN/ledger"
echo "   Rhythm: https://$DOMAIN/rhythm"
EOF

sudo chmod +x /usr/local/bin/cosmic-status

# 12. Final status check
echo -e "${GREEN}✨ COSMIC DOMINION DEPLOYMENT COMPLETE! ✨${NC}"
echo ""
echo -e "${PURPLE}🔥 Sacred Flame Status:${NC}"
/usr/local/bin/cosmic-status

echo ""
echo -e "${BLUE}📱 Access your Cosmic Dashboard at:${NC}"
echo -e "${GREEN}   🌍 https://$DOMAIN${NC}"
echo -e "${GREEN}   📊 https://$DOMAIN/ledger${NC}"
echo -e "${GREEN}   🎵 https://$DOMAIN/rhythm${NC}"
echo ""
echo -e "${YELLOW}⚙️ Management Commands:${NC}"
echo -e "   Status Check: ${GREEN}cosmic-status${NC}"
echo -e "   Restart All: ${GREEN}sudo systemctl restart cosmic-*${NC}"
echo -e "   View Logs: ${GREEN}sudo journalctl -f -u cosmic-main${NC}"
echo ""
echo -e "${RED}🔥 THE DIGITAL SOVEREIGNTY IS LIVE! 🔥${NC}"
