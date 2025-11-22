// Simple nginx equivalent proxy server for aistorelab.com (Windows)
// No external dependencies - uses only Node.js built-in modules

const http = require('http');
const httpProxy = require('http');
const url = require('url');

// Configuration equivalent to nginx sites-available/aistorelab.com
// Matches your nginx server block exactly
const CONFIG = {
    port: 3000, // Using port 3000 for testing (change to 80 when ready for production)
    server_name: ['aistorelab.com', 'www.aistorelab.com'],
    routes: {
        '/': { target: 'http://127.0.0.1:8501', description: 'Main Dashboard (Codex) - matches your nginx config' },
        '/health': { local: true, description: 'Health Check' }
    }
};

// Simple proxy function
function proxyRequest(req, res, targetUrl) {
    const parsedTarget = url.parse(targetUrl);
    const options = {
        hostname: parsedTarget.hostname,
        port: parsedTarget.port,
        path: req.url,
        method: req.method,
        headers: {
            ...req.headers,
            'host': req.headers.host || 'aistorelab.com',
            'x-real-ip': req.connection.remoteAddress,
            'x-forwarded-for': req.headers['x-forwarded-for'] ? 
                req.headers['x-forwarded-for'] + ', ' + req.connection.remoteAddress : 
                req.connection.remoteAddress
        }
    };

    const proxyReq = http.request(options, (proxyRes) => {
        // Pass through response headers (matches nginx behavior)
        res.writeHead(proxyRes.statusCode, proxyRes.headers);
        proxyRes.pipe(res, { end: true });
    });

    proxyReq.on('error', (err) => {
        console.error(`Proxy error for ${req.url}:`, err.message);
        res.writeHead(502, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            error: 'Service Unavailable', 
            message: 'Backend service is not responding',
            timestamp: new Date().toISOString()
        }));
    });

    req.pipe(proxyReq, { end: true });
}

// Health check handler
function handleHealth(req, res) {
    const healthData = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        server: 'AIStoreLab.com Proxy (Windows nginx equivalent)',
        routes: Object.keys(CONFIG.routes).map(route => ({
            path: route,
            target: CONFIG.routes[route].target || 'local',
            description: CONFIG.routes[route].description
        })),
        uptime: process.uptime()
    };

    res.writeHead(200, { 
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    });
    res.end(JSON.stringify(healthData, null, 2));
}

// Main server (equivalent to nginx server block)
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url);
    const pathname = parsedUrl.pathname;

    console.log(`${new Date().toISOString()} - ${req.method} ${pathname} - ${req.headers.host || 'localhost'}`);

    // Route matching (equivalent to nginx location blocks)
    if (pathname === '/health') {
        return handleHealth(req, res);
    }

    // Simple routing - matches your nginx config exactly
    // location / { proxy_pass http://127.0.0.1:8501; }
    proxyRequest(req, res, 'http://127.0.0.1:8501');
});

// Error handling
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`❌ Port ${CONFIG.port} is already in use`);
        console.log('Try these alternatives:');
        console.log('  1. Stop any existing web server on port 80');
        console.log('  2. Run as Administrator');
        console.log('  3. Change port in CONFIG.port and restart');
        process.exit(1);
    } else {
        console.error('Server error:', err);
    }
});

// Start HTTP server
server.listen(CONFIG.port, () => {
    console.log('🚀 AIStoreLab.com Proxy Server Started');
    console.log('=' * 50);
    console.log(`📡 HTTP Server: port ${CONFIG.port}`);
    console.log(`🌐 HTTP Access: http://localhost:${CONFIG.port}`);
    
    // Start HTTPS server if SSL certificates are available (certbot equivalent)
    if (sslOptions) {
        const httpsPort = 3443; // Using 3443 for testing (443 in production)
        
        // Create HTTPS server with same request handler
        const httpsServer = https.createServer(sslOptions, (req, res) => {
            const parsedUrl = url.parse(req.url);
            const pathname = parsedUrl.pathname;

            console.log(`${new Date().toISOString()} - HTTPS ${req.method} ${pathname} - ${req.headers.host || 'localhost'}`);

            // Route matching (same as HTTP)
            if (pathname === '/health') {
                return handleHealth(req, res);
            }

            // Proxy to Codex Dashboard
            proxyRequest(req, res, 'http://127.0.0.1:8501');
        });

        httpsServer.listen(httpsPort, () => {
            console.log(`🔒 HTTPS Server: port ${httpsPort}`);
            console.log(`🌐 HTTPS Access: https://localhost:${httpsPort}`);
            console.log('📋 SSL Certificate: ACTIVE (aistorelab.com)');
        }).on('error', (err) => {
            if (err.code === 'EADDRINUSE') {
                console.log(`⚠️  Port ${httpsPort} in use - HTTPS disabled`);
            } else {
                console.error('HTTPS Server Error:', err.message);
            }
        });
    }
    
    console.log('');
    console.log('📋 Route Configuration (nginx server block equivalent):');
    Object.entries(CONFIG.routes).forEach(([path, config]) => {
        if (config.target) {
            console.log(`  ${path.padEnd(12)} → ${config.target} (${config.description})`);
        } else {
            console.log(`  ${path.padEnd(12)} → Local Handler (${config.description})`);
        }
    });
    console.log('');
    console.log('🔧 Management:');
    console.log('  Health Check: http://localhost:${CONFIG.port}/health');
    if (sslOptions) {
        console.log('  HTTPS Health: https://localhost:3443/health');
    }
    console.log('  Stop Server: Ctrl+C');
    console.log('');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down AIStoreLab.com proxy server...');
    server.close(() => {
        console.log('✅ Server stopped gracefully');
        process.exit(0);
    });
});

process.on('SIGTERM', () => {
    console.log('\n🛑 SIGTERM received, shutting down...');
    server.close(() => {
        console.log('✅ Server stopped');
        process.exit(0);
    });
});

// HTTPS Configuration (certbot SSL equivalent)
const https = require('https');
const fs = require('fs');
const path = require('path');

// SSL Certificate setup (equivalent to certbot generated certificates)
const sslCertPath = path.join('ssl-certificates', 'aistorelab.com.pfx');
let sslOptions = null;

if (fs.existsSync(sslCertPath)) {
    try {
        sslOptions = {
            pfx: fs.readFileSync(sslCertPath),
            passphrase: 'aistorelab2025'
        };
        console.log('📋 SSL certificates found - HTTPS will be available');
    } catch (err) {
        console.log('⚠️  SSL certificate error:', err.message);
    }
} else {
    console.log('⚠️  SSL certificates not found - HTTPS disabled');
}

console.log('AIStoreLab.com Proxy Server (Windows nginx equivalent)');
console.log('Starting up...');