const http = require('http');
const url = require('url');

console.log('🚀 CODEX DOMINION SIMPLE REVERSE PROXY');
console.log('=' .repeat(45));

// Service configuration
const services = {
    '/api': { host: '127.0.0.1', port: 8000 },
    '/portfolio': { host: '127.0.0.1', port: 8503 },
    '/': { host: '127.0.0.1', port: 8501 }
};

// Simple proxy function
function proxyRequest(clientReq, clientRes) {
    const reqUrl = url.parse(clientReq.url);
    let target = null;
    
    // Find matching service
    for (const [path, service] of Object.entries(services)) {
        if (reqUrl.pathname.startsWith(path) || path === '/') {
            target = service;
            break;
        }
    }
    
    if (!target) {
        clientRes.writeHead(404, {'Content-Type': 'text/plain'});
        clientRes.end('Service not found');
        return;
    }
    
    console.log(`🔀 Proxying ${clientReq.method} ${clientReq.url} → ${target.host}:${target.port}`);
    
    // Proxy options
    const options = {
        hostname: target.host,
        port: target.port,
        path: clientReq.url,
        method: clientReq.method,
        headers: {
            ...clientReq.headers,
            'host': `${target.host}:${target.port}`,
            'x-forwarded-for': clientReq.connection.remoteAddress,
            'x-forwarded-proto': 'http'
        }
    };
    
    // Create proxy request
    const proxyReq = http.request(options, (proxyRes) => {
        // Copy headers
        clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
        
        // Pipe response
        proxyRes.pipe(clientRes, { end: true });
    });
    
    // Handle errors
    proxyReq.on('error', (err) => {
        console.error(`❌ Proxy error for ${clientReq.url}:`, err.message);
        clientRes.writeHead(502, {'Content-Type': 'text/plain'});
        clientRes.end('Bad Gateway - Service Unavailable');
    });
    
    // Pipe request body
    clientReq.pipe(proxyReq, { end: true });
}

// Create server
const server = http.createServer((req, res) => {
    // Health check
    if (req.url === '/health') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({
            status: 'healthy',
            services: services,
            proxy_port: 80,
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // Add CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    // Handle preflight requests
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // Proxy the request
    proxyRequest(req, res);
});

// Handle WebSocket upgrades
server.on('upgrade', (request, socket, head) => {
    const reqUrl = url.parse(request.url);
    let target = null;
    
    // Find target service
    for (const [path, service] of Object.entries(services)) {
        if (reqUrl.pathname.startsWith(path) || path === '/') {
            target = service;
            break;
        }
    }
    
    if (!target) {
        socket.end();
        return;
    }
    
    console.log(`🔌 WebSocket upgrade ${request.url} → ${target.host}:${target.port}`);
    
    // Create connection to target
    const targetSocket = new require('net').Socket();
    
    targetSocket.connect(target.port, target.host, () => {
        // Send upgrade request to target
        targetSocket.write(`${request.method} ${request.url} HTTP/1.1\r\n`);
        
        for (const [key, value] of Object.entries(request.headers)) {
            targetSocket.write(`${key}: ${value}\r\n`);
        }
        
        targetSocket.write('\r\n');
        targetSocket.write(head);
        
        // Pipe bidirectional
        socket.pipe(targetSocket);
        targetSocket.pipe(socket);
    });
    
    targetSocket.on('error', () => {
        socket.end();
    });
});

// Start server
server.listen(80, '0.0.0.0', () => {
    console.log('✅ Reverse Proxy Status:');
    console.log('-'.repeat(25));
    console.log('🌐 Main Dashboard: http://localhost/');
    console.log('📊 API Endpoints: http://localhost/api/');
    console.log('💼 Portfolio: http://localhost/portfolio/');
    console.log('🏥 Health Check: http://localhost/health');
    console.log('');
    console.log('🔗 Backend Services:');
    console.log('-'.repeat(20));
    console.log('⚡ FastAPI: 127.0.0.1:8000');
    console.log('📈 Main Dashboard: 127.0.0.1:8501');
    console.log('💰 Portfolio Dashboard: 127.0.0.1:8503');
    console.log('');
    console.log('✨ Simple proxy server running on port 80');
    console.log('🔄 WebSocket support enabled');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down proxy server...');
    server.close(() => {
        console.log('✅ Proxy server stopped');
        process.exit(0);
    });
});

// Error handling
server.on('error', (error) => {
    if (error.code === 'EACCES') {
        console.error('❌ Permission denied - Port 80 requires admin privileges');
        console.log('💡 Try running as Administrator or use a different port');
        console.log('💡 Alternative: Start with port 3000 instead of 80');
        process.exit(1);
    } else if (error.code === 'EADDRINUSE') {
        console.error('❌ Port 80 already in use');
        console.log('💡 Stop other web servers or use a different port');
        process.exit(1);
    } else {
        console.error('❌ Server error:', error.message);
        process.exit(1);
    }
});