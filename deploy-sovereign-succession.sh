#!/bin/bash
# Sovereign Succession - Google Cloud VM Deployment Script
# For Debian 12 (Bookworm) - Ultimate Continuity Authority
# The Codex endures radiant without end!

echo "🌟 SOVEREIGN SUCCESSION - CLOUD DEPLOYMENT INITIALIZATION 🌟"
echo "✨ Ultimate Continuity Authority - Google Cloud VM Setup ✨"
echo ""

# System Update and Nginx Installation (for your GCP VM)
echo "📦 Updating Debian 12 system packages..."
sudo apt update && sudo apt upgrade -y

echo "🔧 Installing Nginx and essential packages..."
sudo apt install nginx nodejs npm git ufw curl wget htop -y

# Enable and start Nginx
echo "🚀 Starting Nginx service..."
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx

# Firewall Configuration for GCP VM
echo "🔥 Configuring UFW firewall..."
sudo ufw --force enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS  
sudo ufw allow 3001/tcp  # Sovereign Succession Node.js server
sudo ufw allow 3002/tcp  # Next.js ceremonial constellation
sudo ufw status verbose

# Create ceremonial directories
echo "🏛️ Creating ceremonial directory structure..."
sudo mkdir -p /var/www/sovereign-succession
sudo mkdir -p /var/www/ceremonial-constellation
sudo chown -R $USER:$USER /var/www/sovereign-succession
sudo chown -R $USER:$USER /var/www/ceremonial-constellation

# Nginx Configuration for Sovereign Succession
echo "⚖️ Creating Sovereign Succession Nginx configuration..."
sudo tee /etc/nginx/sites-available/sovereign-succession > /dev/null << 'EOF'
# Sovereign Succession - Ultimate Continuity Authority
# The Codex endures radiant without end!

server {
    listen 80;
    listen [::]:80;
    server_name _;
    
    # Main ceremonial constellation proxy
    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Ultimate Continuity Authority Headers
        add_header X-Codex-Status "Endures-Radiant-Without-End" always;
        add_header X-Sovereignty-Level "Ultimate-Continuity-Authority" always;
        add_header X-Ceremonial-Constellation "Active" always;
    }
    
    # Direct Sovereign Succession endpoint
    location /sovereign-succession {
        proxy_pass http://localhost:3001/sovereign-succession;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Special Sovereign Succession Headers
        add_header X-Succession-Status "Custodian-Yields-Heirs-Inherit" always;
        add_header X-Continuity-Authority "Supreme" always;
        add_header X-Codex-Endurance "Radiant-Without-End" always;
    }
    
    # Health check for monitoring
    location /health {
        access_log off;
        return 200 "✨ Sovereign Succession - Ultimate Continuity Authority is alive! The Codex endures radiant without end! 🏆\\n";
        add_header Content-Type text/plain;
    }
    
    # Ceremonial constellation pages
    location ~ ^/(radiant-serenity|eternal-silence|dashboard-selector) {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        add_header X-Ceremonial-Page "Active" always;
        add_header X-Codex-Constellation "Complete" always;
    }
}
EOF

# Enable the site
echo "🔗 Enabling Sovereign Succession site..."
sudo ln -sf /etc/nginx/sites-available/sovereign-succession /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid!"
    sudo systemctl reload nginx
else
    echo "❌ Nginx configuration error - check the config file"
    exit 1
fi

# Create systemd service for Sovereign Succession Node.js server
echo "⚙️ Creating systemd service for Sovereign Succession server..."
sudo tee /etc/systemd/system/sovereign-succession.service > /dev/null << 'EOF'
[Unit]
Description=Sovereign Succession - Ultimate Continuity Authority Server
Documentation=https://codex-dominion.dev
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/sovereign-succession
Environment=NODE_ENV=production
Environment=PORT=3001
ExecStart=/usr/bin/node sovereign-server.js
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for ceremonial constellation (Next.js)
echo "🌟 Creating systemd service for ceremonial constellation..."
sudo tee /etc/systemd/system/ceremonial-constellation.service > /dev/null << 'EOF'
[Unit]
Description=Ceremonial Constellation - Next.js Frontend
Documentation=https://codex-dominion.dev
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ceremonial-constellation
Environment=NODE_ENV=production
Environment=PORT=3002
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

# Set up log rotation
echo "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/sovereign-succession > /dev/null << 'EOF'
/var/log/sovereign-succession/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload sovereign-succession
        systemctl reload ceremonial-constellation
    endscript
}
EOF

# Create monitoring script
echo "👁️ Creating monitoring script..."
sudo tee /usr/local/bin/sovereign-monitor.sh > /dev/null << 'EOF'
#!/bin/bash
# Sovereign Succession Monitoring Script
# The Codex endures radiant without end!

echo "🌟 Sovereign Succession System Status 🌟"
echo "Date: $(date)"
echo ""

# Check Nginx
echo "🔧 Nginx Status:"
systemctl is-active nginx && echo "✅ Nginx: Active" || echo "❌ Nginx: Inactive"

# Check Sovereign Succession server
echo "👑 Sovereign Succession Server:"
systemctl is-active sovereign-succession && echo "✅ Sovereign Succession: Active" || echo "❌ Sovereign Succession: Inactive"

# Check Ceremonial Constellation
echo "🌟 Ceremonial Constellation:"
systemctl is-active ceremonial-constellation && echo "✅ Ceremonial Constellation: Active" || echo "❌ Ceremonial Constellation: Inactive"

# Check ports
echo ""
echo "🔌 Port Status:"
netstat -tulnp | grep ":80\|:443\|:3001\|:3002" || echo "⚠️ Ports not listening"

# Check disk space
echo ""
echo "💾 Disk Usage:"
df -h / | tail -1

# Test endpoints
echo ""
echo "🧪 Endpoint Tests:"
curl -s -o /dev/null -w "Nginx (port 80): %{http_code}\n" http://localhost/health
curl -s -o /dev/null -w "Sovereign Succession: %{http_code}\n" http://localhost:3001/sovereign-succession
curl -s -o /dev/null -w "Ceremonial Constellation: %{http_code}\n" http://localhost:3002/

echo ""
echo "🏆 The Codex endures radiant without end!"
EOF

sudo chmod +x /usr/local/bin/sovereign-monitor.sh

# Create deployment ready message
echo ""
echo "🎉 SOVEREIGN SUCCESSION - DEPLOYMENT READY! 🎉"
echo "✨ Ultimate Continuity Authority configured for Google Cloud VM ✨"
echo ""
echo "📋 Next Steps for your GCP VM (Debian 12):"
echo "1. Upload this script to your VM"
echo "2. Upload your ceremonial constellation code"
echo "3. Run: chmod +x deploy-sovereign-succession.sh"
echo "4. Run: ./deploy-sovereign-succession.sh"
echo "5. Configure firewall in GCP Console (HTTP/HTTPS)"
echo "6. Reserve static IP address"
echo "7. Set up custom service account"
echo ""
echo "🔍 Monitoring Commands:"
echo "• sudo systemctl status nginx"
echo "• sudo systemctl status sovereign-succession"  
echo "• sudo systemctl status ceremonial-constellation"
echo "• sudo /usr/local/bin/sovereign-monitor.sh"
echo ""
echo "🏆 The Codex endures radiant without end!"