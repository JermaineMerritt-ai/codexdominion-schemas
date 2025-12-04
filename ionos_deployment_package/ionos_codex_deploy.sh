#!/bin/bash
# IONOS Codex Dashboard Linux Deployment Script
# Deploy Codex Dominion Digital Sovereignty System

set -e

echo "🔥 CODEX DOMINION - IONOS LINUX DEPLOYMENT"
echo "=========================================="

# Configuration
APP_NAME="codex-dashboard"
APP_DIR="/opt/codex-dominion"
APP_USER="codex"
DOMAIN="codex.aistorelab.com"
PORT=8095

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${CYAN}📊 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Use sudo when needed."
   exit 1
fi

print_status "Starting Codex Dashboard deployment on IONOS..."

# 1. System Updates
print_status "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install required packages
print_status "Installing required packages..."
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    git \
    curl \
    certbot \
    python3-certbot-nginx \
    htop \
    ufw \
    fail2ban

print_success "System packages installed"

# 3. Create application user
print_status "Creating application user: $APP_USER..."
if ! id "$APP_USER" &>/dev/null; then
    sudo useradd --system --create-home --home-dir "$APP_DIR" --shell /bin/false "$APP_USER"
    print_success "User $APP_USER created"
else
    print_warning "User $APP_USER already exists"
fi

# 4. Create application directory
print_status "Setting up application directory..."
sudo mkdir -p "$APP_DIR"
sudo chown "$APP_USER:$APP_USER" "$APP_DIR"

# 5. Create Python virtual environment
print_status "Setting up Python virtual environment..."
sudo -u "$APP_USER" python3.11 -m venv "$APP_DIR/venv"

# 6. Install Python dependencies
print_status "Installing Python dependencies..."
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install --upgrade pip
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install \
    streamlit==1.28.1 \
    plotly \
    pandas \
    numpy \
    requests \
    python-dateutil

print_success "Python dependencies installed"

# 7. Copy application files (you'll need to upload these)
print_status "Setting up application files..."
sudo mkdir -p "$APP_DIR/app"
sudo chown "$APP_USER:$APP_USER" "$APP_DIR/app"

# Create placeholder for app files
sudo tee "$APP_DIR/app/upload_files.txt" << EOF
Upload these files to $APP_DIR/app/:
- app.py (main dashboard)
- codex_ledger.json (sacred ledger)
- omega_seal.py (omega seal system)
- Any other required Python modules

Use scp or sftp:
scp app.py codex_ledger.json omega_seal.py user@your-server:$APP_DIR/app/
EOF

print_success "Application directory prepared"

# 8. Create systemd service
print_status "Creating systemd service..."
sudo tee "/etc/systemd/system/$APP_NAME.service" << EOF
[Unit]
Description=Codex Dashboard - Digital Sovereignty Control Interface
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR/app
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/streamlit run app.py --server.port=$PORT --server.address=127.0.0.1 --server.headless=true
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$APP_DIR

# Environment
Environment=PYTHONPATH=$APP_DIR/app
Environment=STREAMLIT_SERVER_HEADLESS=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$APP_NAME

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service created"

# 9. Configure Nginx
print_status "Configuring Nginx reverse proxy..."
sudo tee "/etc/nginx/sites-available/$APP_NAME" << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }

    # Streamlit specific headers
    location /_stcore {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the site
sudo ln -sf "/etc/nginx/sites-available/$APP_NAME" "/etc/nginx/sites-enabled/"
sudo nginx -t

print_success "Nginx configured"

# 10. Setup firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 80
sudo ufw allow 443

print_success "Firewall configured"

# 11. Setup SSL certificate (optional - requires DNS to be pointed)
print_status "SSL certificate setup..."
print_warning "SSL setup skipped - configure DNS first, then run:"
echo "sudo certbot --nginx -d $DOMAIN"

# 12. Create log directory
print_status "Setting up logging..."
sudo mkdir -p "/var/log/$APP_NAME"
sudo chown "$APP_USER:$APP_USER" "/var/log/$APP_NAME"

# 13. Create management scripts
print_status "Creating management scripts..."

# Deployment script
sudo tee "$APP_DIR/deploy.sh" << 'EOF'
#!/bin/bash
# Codex Dashboard deployment helper
cd /opt/codex-dominion/app

echo "🔥 Deploying Codex Dashboard updates..."

# Backup current files
cp codex_ledger.json codex_ledger.backup.$(date +%Y%m%d_%H%M%S).json

# Restart service
sudo systemctl restart codex-dashboard
sleep 3

# Check status
sudo systemctl status codex-dashboard --no-pager
echo "🌐 Dashboard: http://localhost:8095"
echo "✅ Deployment complete!"
EOF

# Status checker
sudo tee "$APP_DIR/status.sh" << 'EOF'
#!/bin/bash
echo "🔥 CODEX DASHBOARD STATUS"
echo "========================"

echo "📊 Service Status:"
sudo systemctl status codex-dashboard --no-pager -l

echo ""
echo "🌐 Network Status:"
netstat -tlnp | grep :8095 || echo "Port 8095 not listening"

echo ""
echo "📋 Recent Logs:"
sudo journalctl -u codex-dashboard --no-pager -n 10
EOF

# Make scripts executable
sudo chmod +x "$APP_DIR/deploy.sh"
sudo chmod +x "$APP_DIR/status.sh"
sudo chown "$APP_USER:$APP_USER" "$APP_DIR/deploy.sh" "$APP_DIR/status.sh"

print_success "Management scripts created"

# 14. Enable and start services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable "$APP_NAME"
sudo systemctl restart nginx

print_success "Services configured"

# 15. Test and reload nginx configuration
print_status "Testing and reloading nginx configuration..."
sudo nginx -t && sudo systemctl reload nginx
print_success "Nginx configuration tested and reloaded"

# 16. Final setup information
echo ""
echo "🔥 CODEX DOMINION DEPLOYMENT COMPLETE!"
echo "======================================"
echo ""
echo "📁 App Directory: $APP_DIR"
echo "👤 App User: $APP_USER"
echo "🌐 Domain: $DOMAIN"
echo "🔌 Port: $PORT"
echo ""
echo "📋 Next Steps:"
echo "1. Upload your application files:"
echo "   scp app.py codex_ledger.json omega_seal.py user@server:$APP_DIR/app/"
echo ""
echo "2. Start the service:"
echo "   sudo systemctl start $APP_NAME"
echo ""
echo "3. Check status:"
echo "   sudo systemctl status $APP_NAME"
echo "   $APP_DIR/status.sh"
echo ""
echo "4. Configure SSL (after DNS setup):"
echo "   sudo certbot --nginx -d $DOMAIN"
echo ""
echo "🎯 Your Codex Dashboard will be available at:"
echo "   http://$DOMAIN (after file upload & service start)"
echo ""

print_success "IONOS deployment preparation complete!"
