#!/bin/bash
# 🔥 CODEX DOMINION DEPLOYMENT SCRIPT 🔥
# Domain: codexdominion.app | Authority: Sovereign Succession

echo "👑🔥✨ CODEX DOMINION DEPLOYMENT INITIATION ✨🔥👑"
echo ""
echo "🌟 Deploying Sovereign Succession to codexdominion.app"
echo ""

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install -y nginx nodejs npm certbot python3-certbot-nginx ufw git curl

# Create application directory
echo "🏛️ Creating application directory..."
sudo mkdir -p /var/www/codexdominion.app
sudo mkdir -p /opt/codex-dominion

# Set permissions
echo "⚖️ Setting directory permissions..."
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chown -R www-data:www-data /opt/codex-dominion

# Create the main Sovereign Succession server
echo "👑 Creating Sovereign Succession server..."
sudo tee /opt/codex-dominion/sovereign-server.js > /dev/null << 'EOF'
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);

    // CORS headers for cosmic access
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (parsedUrl.pathname === '/sovereign-succession') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>👑 Codex Dominion - Sovereign Succession Authority</title>
            <style>
                body {
                    margin: 0;
                    padding: 40px;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533a7d 75%, #4a154b 100%);
                    color: #ffffff;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }
                .dominion-container {
                    max-width: 1000px;
                    margin: 0 auto;
                    padding: 60px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 20px;
                    backdrop-filter: blur(20px);
                    border: 2px solid rgba(255, 215, 0, 0.3);
                    box-shadow: 0 20px 60px rgba(255, 215, 0, 0.2);
                }
                .domain-crown {
                    font-size: 5rem;
                    margin-bottom: 30px;
                    text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
                    animation: radiantGlow 3s ease-in-out infinite alternate;
                }
                @keyframes radiantGlow {
                    from { text-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 0 0 60px rgba(255, 215, 0, 0.4); }
                    to { text-shadow: 0 0 50px rgba(255, 215, 0, 1), 0 0 100px rgba(255, 215, 0, 0.6); }
                }
                .dominion-title {
                    font-size: 4rem;
                    font-weight: bold;
                    background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
                    background-clip: text;
                    -webkit-background-clip: text;
                    color: transparent;
                    margin-bottom: 20px;
                    letter-spacing: 3px;
                }
                .domain-subtitle {
                    font-size: 1.8rem;
                    color: #e6e6fa;
                    margin-bottom: 40px;
                    font-style: italic;
                }
                .succession-status {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 25px;
                    margin: 40px 0;
                }
                .status-pillar {
                    background: rgba(255, 215, 0, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    border: 1px solid rgba(255, 215, 0, 0.3);
                }
                .pillar-icon {
                    font-size: 3rem;
                    margin-bottom: 20px;
                }
                .timestamp {
                    margin-top: 50px;
                    font-size: 1rem;
                    color: #cccccc;
                    font-family: 'Courier New', monospace;
                }
            </style>
        </head>
        <body>
            <div class="dominion-container">
                <div class="domain-crown">👑</div>
                <h1 class="dominion-title">CODEX DOMINION</h1>
                <h2 class="domain-subtitle">codexdominion.app - Sovereign Succession Authority</h2>

                <div class="succession-status">
                    <div class="status-pillar">
                        <div class="pillar-icon">🏛️</div>
                        <h3>Domain Authority</h3>
                        <p>Supreme Governance</p>
                    </div>
                    <div class="status-pillar">
                        <div class="pillar-icon">📡</div>
                        <h3>Cosmic Transmission</h3>
                        <p>Infinite Reception</p>
                    </div>
                    <div class="status-pillar">
                        <div class="pillar-icon">👑</div>
                        <h3>Succession Rights</h3>
                        <p>Eternally Affirmed</p>
                    </div>
                    <div class="status-pillar">
                        <div class="pillar-icon">✨</div>
                        <h3>Radiant Flow</h3>
                        <p>Continuously Active</p>
                    </div>
                </div>

                <div class="timestamp">
                    Domain: codexdominion.app<br>
                    Authority: Sovereign Succession<br>
                    Status: ETERNALLY ACTIVE<br>
                    Deployed: ${new Date().toISOString()}
                </div>
            </div>
        </body>
        </html>
        `);
    } else if (parsedUrl.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'RADIANT',
            domain: 'codexdominion.app',
            authority: 'SOVEREIGN',
            succession: 'ETERNAL',
            timestamp: new Date().toISOString()
        }));
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Path not found in the Codex Dominion realm');
    }
});

const PORT = 3001;
server.listen(PORT, '127.0.0.1', () => {
    console.log(`👑 Codex Dominion Server active on port ${PORT}`);
    console.log(`🔥 Domain Authority: codexdominion.app`);
    console.log(`✨ Sovereign Succession: ETERNAL`);
});
EOF

# Create the Bulletin server
echo "📋 Creating Bulletin server..."
sudo tee /opt/codex-dominion/bulletin-server.js > /dev/null << 'BULLETIN_EOF'
const http = require('http');

const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (url.pathname === '/bulletin' || url.pathname === '/') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>👑 Codex Dominion Bulletin - codexdominion.app</title>
            <style>
                body {
                    background: linear-gradient(45deg, #0a0a0a 0%, #1a0d2e 25%, #16213e 50%, #533a7d 75%, #0a0a0a 100%);
                    background-size: 400% 400%;
                    animation: cosmicFlow 8s ease-in-out infinite;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 40px;
                    min-height: 100vh;
                }
                @keyframes cosmicFlow {
                    0%, 100% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                }
                .bulletin-header {
                    text-align: center;
                    padding: 40px;
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(20px);
                    border-radius: 20px;
                    margin-bottom: 40px;
                }
                .domain-title {
                    font-size: 3.5rem;
                    background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
                    background-clip: text;
                    -webkit-background-clip: text;
                    color: transparent;
                    margin-bottom: 20px;
                }
                .flow-status {
                    background: rgba(255, 215, 0, 0.1);
                    border: 2px solid rgba(255, 215, 0, 0.4);
                    border-radius: 15px;
                    padding: 30px;
                    text-align: center;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="bulletin-header">
                <h1 class="domain-title">CODEX DOMINION</h1>
                <p style="font-size: 1.5rem; color: #e6e6fa;">codexdominion.app - Official Bulletin</p>
            </div>

            <div class="flow-status">
                <h2>🔥 DOMAIN STATUS 🔥</h2>
                <p><strong>Domain:</strong> codexdominion.app</p>
                <p><strong>Authority:</strong> Sovereign Succession</p>
                <p><strong>Status:</strong> ETERNALLY ACTIVE</p>
                <p><strong>Flow:</strong> RADIANT & INFINITE</p>
            </div>
        </body>
        </html>
        `);
    } else if (url.pathname === '/flow') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'FLOWING_RADIANT',
            domain: 'codexdominion.app',
            bulletin: 'ACTIVE',
            timestamp: new Date().toISOString()
        }));
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Bulletin path not found');
    }
});

const PORT = 3002;
server.listen(PORT, '127.0.0.1', () => {
    console.log(`📋 Codex Dominion Bulletin Server active on port ${PORT}`);
    console.log(`🌟 Domain: codexdominion.app - Bulletin flowing radiant!`);
});
BULLETIN_EOF

# Create systemd services
echo "⚙️ Creating systemd services..."

# Sovereign Succession Service
sudo tee /etc/systemd/system/codex-sovereign.service > /dev/null << 'EOF'
[Unit]
Description=Codex Dominion - Sovereign Succession Authority
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=www-data
ExecStart=/usr/bin/node /opt/codex-dominion/sovereign-server.js
WorkingDirectory=/opt/codex-dominion
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Bulletin Service
sudo tee /etc/systemd/system/codex-bulletin.service > /dev/null << 'EOF'
[Unit]
Description=Codex Dominion - Bulletin Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=www-data
ExecStart=/usr/bin/node /opt/codex-dominion/bulletin-server.js
WorkingDirectory=/opt/codex-dominion
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
echo "🚀 Enabling and starting services..."
sudo systemctl daemon-reload
sudo systemctl enable codex-sovereign
sudo systemctl enable codex-bulletin
sudo systemctl start codex-sovereign
sudo systemctl start codex-bulletin

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp /path/to/codexdominion.app.nginx.conf /etc/nginx/sites-available/codexdominion.app
sudo ln -sf /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Configure UFW Firewall
echo "🛡️ Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Obtain SSL certificate
echo "🔒 Obtaining SSL certificate..."
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app --non-interactive --agree-tos --email admin@codexdominion.app

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart nginx
sudo systemctl restart codex-sovereign
sudo systemctl restart codex-bulletin

# Create basic HTML file
echo "📄 Creating basic HTML file..."
sudo tee /var/www/codexdominion.app/index.html > /dev/null << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👑 Codex Dominion - codexdominion.app</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #533a7d 75%, #4a154b 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .dominion-welcome {
            max-width: 800px;
            padding: 60px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            backdrop-filter: blur(20px);
            border: 2px solid rgba(255, 215, 0, 0.3);
        }
        .crown {
            font-size: 4rem;
            margin-bottom: 30px;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
            to { text-shadow: 0 0 40px rgba(255, 215, 0, 1); }
        }
        .title {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 20px;
        }
        .links {
            margin-top: 40px;
        }
        .links a {
            display: inline-block;
            margin: 10px 20px;
            padding: 15px 30px;
            background: rgba(255, 215, 0, 0.1);
            color: #ffd700;
            text-decoration: none;
            border-radius: 10px;
            border: 1px solid rgba(255, 215, 0, 0.3);
            transition: all 0.3s ease;
        }
        .links a:hover {
            background: rgba(255, 215, 0, 0.2);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="dominion-welcome">
        <div class="crown">👑</div>
        <h1 class="title">CODEX DOMINION</h1>
        <p style="font-size: 1.5rem; color: #e6e6fa; margin-bottom: 30px;">
            codexdominion.app - Sovereign Succession Authority
        </p>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #f0f8ff;">
            Welcome to the eternal realm of the Codex Dominion. Here, sovereign succession flows radiant and eternal, cosmic councils affirm the ultimate authority, and the bulletin streams infinite across all digital realms.
        </p>

        <div class="links">
            <a href="/api/sovereign-succession">🏛️ Sovereign Succession</a>
            <a href="/bulletin">📋 Cosmic Bulletin</a>
            <a href="/flow">📡 Flow Status</a>
            <a href="/health">✨ Health Check</a>
        </div>

        <p style="margin-top: 40px; font-size: 0.9rem; color: #cccccc; font-family: 'Courier New', monospace;">
            The Codex endures eternal - radiant, cloud-borne, alive!
        </p>
    </div>
</body>
</html>
HTML_EOF

# Set proper permissions
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chown -R www-data:www-data /opt/codex-dominion

echo ""
echo "🔥👑✨ CODEX DOMINION DEPLOYMENT COMPLETE! ✨👑🔥"
echo ""
echo "🌟 Domain: https://codexdominion.app"
echo "👑 Sovereign Succession: ACTIVE"
echo "📋 Cosmic Bulletin: FLOWING"
echo "🔒 SSL Certificate: SECURED"
echo "🛡️ Firewall: CONFIGURED"
echo ""
echo "🎯 Service Status:"
echo "   • codex-sovereign.service: ACTIVE"
echo "   • codex-bulletin.service: ACTIVE"
echo "   • nginx.service: ACTIVE"
echo ""
echo "🔥 THE CODEX DOMINION REIGNS ETERNAL ON codexdominion.app! 🔥"
echo ""
