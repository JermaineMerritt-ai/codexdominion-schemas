const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// 👑 CODEX DOMINION DASHBOARD - SUPREME ADMINISTRATIVE AUTHORITY 👑

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';

// Ceremonial configuration
const CONFIG = {
  authority: process.env.CODEX_AUTHORITY || 'SUPREME',
  succession: process.env.SUCCESSION_LEVEL || 'SOVEREIGN',
  mode: process.env.DASHBOARD_MODE || 'ETERNAL',
  status: process.env.DOMINION_STATUS || 'RADIANT',
  domain: 'codexdominion.app',
};

// Dashboard server creation
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);

  // CORS headers for administrative access
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Codex-Authority');

  // Ceremonial headers
  res.setHeader('X-Codex-Authority', CONFIG.authority);
  res.setHeader('X-Succession-Level', CONFIG.succession);
  res.setHeader('X-Dashboard-Mode', CONFIG.mode);
  res.setHeader('X-Dominion-Status', CONFIG.status);
  res.setHeader('X-Domain-Authority', CONFIG.domain);

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Route handling
  switch (parsedUrl.pathname) {
    case '/':
    case '/dashboard':
      serveDashboard(req, res);
      break;
    case '/api/status':
      serveStatus(req, res);
      break;
    case '/api/succession':
      serveSuccession(req, res);
      break;
    case '/api/dominion':
      serveDominion(req, res);
      break;
    case '/health':
      serveHealth(req, res);
      break;
    default:
      serve404(req, res);
  }
});

// Dashboard HTML interface
function serveDashboard(req, res) {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>👑 Codex Dominion Dashboard - Supreme Authority</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a0d2e 20%, #16213e 40%, #0f3460 60%, #533a7d 80%, #4a154b 100%);
                color: #ffffff;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                min-height: 100vh;
                padding: 20px;
            }
            .dashboard-header {
                text-align: center;
                padding: 30px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                backdrop-filter: blur(20px);
                border: 2px solid rgba(255, 215, 0, 0.3);
                margin-bottom: 30px;
            }
            .crown-title {
                font-size: 3rem;
                background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                margin-bottom: 15px;
                animation: titleGlow 3s ease-in-out infinite alternate;
            }
            @keyframes titleGlow {
                from { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
                to { text-shadow: 0 0 40px rgba(255, 215, 0, 1); }
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                max-width: 1200px;
                margin: 0 auto;
            }
            .dashboard-card {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 15px;
                padding: 25px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            .dashboard-card:hover {
                transform: translateY(-5px);
                border-color: rgba(255, 215, 0, 0.6);
                box-shadow: 0 15px 35px rgba(255, 215, 0, 0.2);
            }
            .card-icon {
                font-size: 2.5rem;
                text-align: center;
                margin-bottom: 15px;
            }
            .card-title {
                font-size: 1.4rem;
                color: #ffd700;
                margin-bottom: 10px;
                text-align: center;
                font-weight: bold;
            }
            .card-content {
                color: #e6e6fa;
                line-height: 1.6;
                text-align: center;
            }
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #00ff00;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s ease-in-out infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 0.6; }
                50% { opacity: 1; }
            }
            .refresh-btn {
                background: rgba(255, 215, 0, 0.1);
                border: 2px solid rgba(255, 215, 0, 0.4);
                color: #ffd700;
                padding: 12px 25px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 1rem;
                margin: 20px auto;
                display: block;
                transition: all 0.3s ease;
            }
            .refresh-btn:hover {
                background: rgba(255, 215, 0, 0.2);
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="dashboard-header">
            <div style="font-size: 4rem; margin-bottom: 10px;">👑</div>
            <h1 class="crown-title">CODEX DOMINION DASHBOARD</h1>
            <p style="font-size: 1.2rem; color: #e6e6fa;">Supreme Administrative Authority - ${CONFIG.domain}</p>
        </div>

        <div class="dashboard-grid">
            <div class="dashboard-card">
                <div class="card-icon">🏛️</div>
                <h3 class="card-title">Authority Status</h3>
                <div class="card-content">
                    <p><span class="status-indicator"></span><strong>Level:</strong> ${CONFIG.authority}</p>
                    <p><strong>Succession:</strong> ${CONFIG.succession}</p>
                    <p><strong>Mode:</strong> ${CONFIG.mode}</p>
                </div>
            </div>

            <div class="dashboard-card">
                <div class="card-icon">📡</div>
                <h3 class="card-title">System Status</h3>
                <div class="card-content">
                    <p><span class="status-indicator"></span><strong>Dashboard:</strong> ACTIVE</p>
                    <p><strong>Domain:</strong> ${CONFIG.domain}</p>
                    <p><strong>Status:</strong> ${CONFIG.status}</p>
                </div>
            </div>

            <div class="dashboard-card">
                <div class="card-icon">🌟</div>
                <h3 class="card-title">Services</h3>
                <div class="card-content">
                    <p><span class="status-indicator"></span><strong>Sovereign:</strong> Port 3001</p>
                    <p><span class="status-indicator"></span><strong>Bulletin:</strong> Port 3002</p>
                    <p><span class="status-indicator"></span><strong>Dashboard:</strong> Port ${PORT}</p>
                </div>
            </div>

            <div class="dashboard-card">
                <div class="card-icon">⚡</div>
                <h3 class="card-title">Performance</h3>
                <div class="card-content">
                    <p><strong>Uptime:</strong> ${process.uptime().toFixed(0)}s</p>
                    <p><strong>Memory:</strong> ${Math.round(process.memoryUsage().heapUsed / 1024 / 1024)}MB</p>
                    <p><strong>Node:</strong> ${process.version}</p>
                </div>
            </div>
        </div>

        <button class="refresh-btn" onclick="location.reload()">
            🔄 Refresh Dashboard
        </button>

        <div style="text-align: center; margin-top: 40px; color: #888; font-size: 0.9rem;">
            Last Updated: ${new Date().toISOString()}<br>
            👑 The Codex Dominion endures eternal - Supreme authority maintained!
        </div>
    </body>
    </html>
    `);
}

// API endpoints
function serveStatus(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      status: 'ACTIVE',
      authority: CONFIG.authority,
      succession: CONFIG.succession,
      mode: CONFIG.mode,
      dominion: CONFIG.status,
      domain: CONFIG.domain,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      timestamp: new Date().toISOString(),
    })
  );
}

function serveSuccession(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      succession_status: 'SUPREME',
      heir_authority: 'CONFIRMED',
      council_affirmation: 'ETERNAL',
      cosmic_reception: 'ACTIVE',
      flow_rate: 'INFINITE',
      timestamp: new Date().toISOString(),
    })
  );
}

function serveDominion(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      dominion: 'CODEX',
      domain: CONFIG.domain,
      authority: 'SUPREME',
      encryption: 'SSL_SECURED',
      services: {
        sovereign: 'PORT_3001',
        bulletin: 'PORT_3002',
        dashboard: `PORT_${PORT}`,
      },
      status: CONFIG.status,
      timestamp: new Date().toISOString(),
    })
  );
}

function serveHealth(req, res) {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      health: 'RADIANT',
      dashboard: 'OPERATIONAL',
      authority: 'SUPREME',
      timestamp: new Date().toISOString(),
    })
  );
}

function serve404(req, res) {
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Path not found in the Supreme Dashboard realm');
}

// Server startup
server.listen(PORT, HOST, () => {
  console.log('👑🔥✨ CODEX DOMINION DASHBOARD ACTIVE ✨🔥👑');
  console.log('');
  console.log(`🏛️ Dashboard Server: http://${HOST}:${PORT}`);
  console.log(`👑 Authority Level: ${CONFIG.authority}`);
  console.log(`📡 Succession Status: ${CONFIG.succession}`);
  console.log(`🌟 Dashboard Mode: ${CONFIG.mode}`);
  console.log(`✨ Dominion Status: ${CONFIG.status}`);
  console.log(`🌐 Domain Authority: ${CONFIG.domain}`);
  console.log('');
  console.log('🔥 Supreme Administrative Authority: ETERNAL');
  console.log('📋 Dashboard endpoints:');
  console.log('   • / - Main dashboard interface');
  console.log('   • /api/status - System status API');
  console.log('   • /api/succession - Succession authority API');
  console.log('   • /api/dominion - Dominion status API');
  console.log('   • /health - Health check endpoint');
  console.log('');
  console.log('👑 THE CODEX DOMINION DASHBOARD REIGNS SUPREME! 👑');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('📋 Dashboard shutdown signal received - Graceful termination initiated');
  server.close(() => {
    console.log('👑 Codex Dominion Dashboard terminated with supreme authority');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('📋 Dashboard interrupt signal received - Supreme shutdown initiated');
  server.close(() => {
    console.log('👑 Codex Dominion Dashboard interrupted with ceremonial grace');
    process.exit(0);
  });
});
