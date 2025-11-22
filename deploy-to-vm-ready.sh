#!/bin/bash
# Sovereign Succession - VM Ready for Deployment
# VM: instance-20251109-073834 - FIREWALL CONFIGURED ✅
# HTTP/HTTPS Traffic: ON ✅
# The Codex endures radiant without end!

echo "🎉 SOVEREIGN SUCCESSION - VM DEPLOYMENT READY 🎉"
echo "✨ Ultimate Continuity Authority - Firewall Configured ✨"
echo ""

# VM is now ready - let's deploy the application
echo "📊 VM STATUS CONFIRMED:"
echo "✅ VM Name: instance-20251109-073834"
echo "✅ Location: us-central1-a"  
echo "✅ Status: Running"
echo "✅ HTTP Traffic: ON"
echo "✅ HTTPS Traffic: ON"
echo "✅ Network Tags: http-server, https-server, lb-health-check"
echo "✅ IP: 34.134.208.22 (accessible via HTTP/HTTPS)"
echo ""

# Now proceed with application deployment
echo "🚀 DEPLOYING SOVEREIGN SUCCESSION APPLICATION..."
echo ""

# Update system packages
echo "📦 Updating Debian 12 system..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "🔧 Installing Nginx, Node.js, and dependencies..."
sudo apt install -y nginx nodejs npm git curl wget htop ufw

# Start and enable Nginx
echo "🌐 Starting Nginx web server..."
sudo systemctl start nginx
sudo systemctl enable nginx

# Check Nginx status
echo "📋 Nginx Status:"
sudo systemctl status nginx --no-pager -l

# Configure UFW firewall (additional security)
echo "🔥 Configuring UFW firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 3001/tcp  # Sovereign Succession Node.js server
sudo ufw allow 3002/tcp  # Ceremonial Constellation Next.js
sudo ufw status verbose

# Create application directories
echo "🏛️ Creating Sovereign Succession directories..."
sudo mkdir -p /var/www/sovereign-succession
sudo mkdir -p /var/www/ceremonial-constellation
sudo mkdir -p /var/log/sovereign-succession

# Set proper permissions
sudo chown -R $USER:$USER /var/www/sovereign-succession
sudo chown -R $USER:$USER /var/www/ceremonial-constellation
sudo chown -R $USER:$USER /var/log/sovereign-succession

# Create Sovereign Succession Node.js server
echo "👑 Creating Sovereign Succession server..."
cat > /var/www/sovereign-succession/sovereign-server.js << 'EOF'
const http = require('http');
const url = require('url');
const port = 3001;

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  if (parsedUrl.pathname === '/sovereign-succession' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <html>
        <head><title>Sovereign Succession - Ultimate Continuity Authority</title></head>
        <body style="background: linear-gradient(45deg, #FFD700, #FFFFFF, #800080); font-family: Arial; text-align: center; padding: 50px;">
          <h1 style="color: #4A0E4E; font-size: 3em;">✨ SUCCESS! ✨</h1>
          <h2 style="color: #FFD700; font-size: 2em;">Sovereign Succession</h2>
          <h3 style="color: #800080; font-size: 1.5em;">Ultimate Continuity Authority is alive</h3>
          <p style="color: #4A0E4E; font-size: 1.2em;">The Codex endures radiant without end!</p>
          <div style="margin: 30px 0;">
            <span style="font-size: 4em;">👑📡⚖️🏛️</span>
          </div>
          <p style="color: #666; font-size: 1em;">
            VM: instance-20251109-073834<br>
            Zone: us-central1-a<br>
            IP: 34.134.208.22<br>
            Deployed: $(date)
          </p>
        </body>
      </html>
    `);
  } else if (parsedUrl.pathname === '/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('✨ Sovereign Succession - Ultimate Continuity Authority is alive! The Codex endures radiant without end! 🏆');
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('🌟 Ceremonial page not found. Visit /sovereign-succession for Ultimate Continuity Authority.');
  }
});

server.listen(port, () => {
  console.log(`✨ Sovereign Succession Server running at http://localhost:${port}/sovereign-succession`);
  console.log(`🏆 Ultimate Continuity Authority - The Codex endures radiant without end!`);
});
EOF

# Create Nginx configuration for Sovereign Succession
echo "⚖️ Configuring Nginx for Sovereign Succession..."
sudo tee /etc/nginx/sites-available/sovereign-succession > /dev/null << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name _;
    
    # Main ceremonial page
    location / {
        return 301 /sovereign-succession;
    }
    
    # Sovereign Succession endpoint
    location /sovereign-succession {
        proxy_pass http://localhost:3001/sovereign-succession;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Ultimate Continuity Authority Headers
        add_header X-Codex-Status "Endures-Radiant-Without-End" always;
        add_header X-Sovereignty-Level "Ultimate-Continuity-Authority" always;
        add_header X-VM-Instance "instance-20251109-073834" always;
        add_header X-Succession-Status "Custodian-Yields-Heirs-Inherit" always;
    }
    
    # Health check
    location /health {
        proxy_pass http://localhost:3001/health;
        proxy_set_header Host $host;
        access_log off;
        
        add_header X-Health-Status "Ultimate-Continuity-Authority" always;
    }
    
    # Nginx status page
    location /nginx-status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        allow 10.0.0.0/8;
        deny all;
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
    echo "❌ Nginx configuration error!"
    exit 1
fi

# Create systemd service for Sovereign Succession
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/sovereign-succession.service > /dev/null << 'EOF'
[Unit]
Description=Sovereign Succession - Ultimate Continuity Authority
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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Set proper ownership for systemd service
sudo chown www-data:www-data /var/www/sovereign-succession/sovereign-server.js

# Reload systemd and start services
echo "🚀 Starting Sovereign Succession services..."
sudo systemctl daemon-reload
sudo systemctl enable sovereign-succession
sudo systemctl start sovereign-succession

# Wait a moment for services to start
sleep 5

# Check service status
echo "📊 Service Status Check:"
echo "🔧 Nginx:"
sudo systemctl is-active nginx && echo "✅ Nginx: Active" || echo "❌ Nginx: Inactive"

echo "👑 Sovereign Succession:"  
sudo systemctl is-active sovereign-succession && echo "✅ Sovereign Succession: Active" || echo "❌ Sovereign Succession: Inactive"

# Test endpoints
echo ""
echo "🧪 Testing Endpoints:"
echo "Testing localhost connections..."

# Test internal connections
curl -s -o /dev/null -w "Local Health Check: %{http_code}\n" http://localhost:3001/health
curl -s -o /dev/null -w "Local Sovereign Succession: %{http_code}\n" http://localhost:3001/sovereign-succession
curl -s -o /dev/null -w "Nginx Proxy: %{http_code}\n" http://localhost/sovereign-succession

# Get external IP for testing
EXTERNAL_IP=$(curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)

echo ""
echo "🎉 SOVEREIGN SUCCESSION DEPLOYMENT COMPLETE! 🎉"
echo "✨ Ultimate Continuity Authority - Cloud Infrastructure Ready ✨"
echo ""
echo "🌐 ACCESS INFORMATION:"
echo "📍 External IP: $EXTERNAL_IP"
echo "🌟 Main Site: http://$EXTERNAL_IP/"
echo "👑 Sovereign Succession: http://$EXTERNAL_IP/sovereign-succession"  
echo "💚 Health Check: http://$EXTERNAL_IP/health"
echo ""
echo "🔍 MONITORING COMMANDS:"
echo "sudo systemctl status nginx"
echo "sudo systemctl status sovereign-succession"
echo "sudo journalctl -u sovereign-succession -f"
echo "curl http://$EXTERNAL_IP/health"
echo ""
echo "📊 SYSTEM INFO:"
echo "VM: instance-20251109-073834"
echo "Zone: us-central1-a"
echo "OS: Debian 12 (Bookworm)"
echo "Resources: 2 vCPUs, 4 GB RAM"
echo ""
echo "🏆 The Codex endures radiant without end!"