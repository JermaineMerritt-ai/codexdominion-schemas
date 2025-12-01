const http = require('http');
const url = require('url');

console.log('🚀 CODEX DOMINION REVERSE PROXY SERVER');
console.log('='.repeat(45));

// Service configuration
const services = {
  '/api': { host: '127.0.0.1', port: 8000 },
  '/portfolio': { host: '127.0.0.1', port: 8503 },
  '/': { host: '127.0.0.1', port: 8501 },
};

// Simple proxy function
function proxyRequest(clientReq, clientRes) {
  const reqUrl = url.parse(clientReq.url);
  let target = null;

  // Find matching service
  for (const [path, service] of Object.entries(services)) {
    if (reqUrl.pathname.startsWith(path)) {
      target = service;
      // Remove path prefix for API and portfolio
      if (path !== '/') {
        clientReq.url = clientReq.url.replace(path, '');
        if (!clientReq.url.startsWith('/')) {
          clientReq.url = '/' + clientReq.url;
        }
      }
      break;
    }
  }

  // Default to main dashboard
  if (!target) {
    target = services['/'];
  }

  console.log(`🔀 ${clientReq.method} ${reqUrl.pathname} → ${target.host}:${target.port}`);

  // Proxy options
  const options = {
    hostname: target.host,
    port: target.port,
    path: clientReq.url,
    method: clientReq.method,
    headers: {
      ...clientReq.headers,
      host: `${target.host}:${target.port}`,
      'x-forwarded-for': clientReq.socket.remoteAddress,
      'x-forwarded-proto': 'http',
      'x-forwarded-host': clientReq.headers.host,
    },
  };

  // Create proxy request
  const proxyReq = http.request(options, (proxyRes) => {
    // Copy status and headers
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);

    // Pipe response
    proxyRes.pipe(clientRes, { end: true });
  });

  // Handle errors
  proxyReq.on('error', (err) => {
    console.error(`❌ Proxy error for ${reqUrl.pathname}:`, err.message);
    if (!clientRes.headersSent) {
      clientRes.writeHead(502, { 'Content-Type': 'text/plain' });
      clientRes.end(
        'Bad Gateway - Service Unavailable\\n\\nTarget: ' + target.host + ':' + target.port
      );
    }
  });

  // Pipe request body
  clientReq.pipe(proxyReq, { end: true });
}

// Create server
const server = http.createServer((req, res) => {
  // Health check endpoint
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(
      JSON.stringify(
        {
          status: 'healthy',
          services: services,
          proxy_port: 3000,
          timestamp: new Date().toISOString(),
          endpoints: {
            dashboard: 'http://localhost:3000/',
            api: 'http://localhost:3000/api/',
            portfolio: 'http://localhost:3000/portfolio/',
            health: 'http://localhost:3000/health',
          },
        },
        null,
        2
      )
    );
    return;
  }

  // Add CORS headers for API requests
  if (req.url.startsWith('/api')) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

    // Handle preflight requests
    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }
  }

  // Proxy the request
  proxyRequest(req, res);
});

// Handle WebSocket upgrades for Streamlit
server.on('upgrade', (request, socket, head) => {
  const reqUrl = url.parse(request.url);
  let target = services['/']; // Default to main dashboard

  // Find target service for WebSocket
  for (const [path, service] of Object.entries(services)) {
    if (reqUrl.pathname.startsWith(path) && path !== '/') {
      target = service;
      break;
    }
  }

  console.log(`🔌 WebSocket ${request.url} → ${target.host}:${target.port}`);

  // Create WebSocket proxy
  const net = require('net');
  const targetSocket = new net.Socket();

  targetSocket.connect(target.port, target.host, () => {
    // Forward the upgrade request
    const headers = [];
    headers.push(`GET ${request.url} HTTP/1.1`);

    for (const [key, value] of Object.entries(request.headers)) {
      headers.push(`${key}: ${value}`);
    }

    headers.push('');
    headers.push('');

    targetSocket.write(headers.join('\\r\\n'));

    // Pipe the sockets together
    socket.pipe(targetSocket);
    targetSocket.pipe(socket);

    // Handle cleanup
    const cleanup = () => {
      try {
        socket.destroy();
        targetSocket.destroy();
      } catch (e) {
        // Ignore cleanup errors
      }
    };

    socket.on('error', cleanup);
    socket.on('close', cleanup);
    targetSocket.on('error', cleanup);
    targetSocket.on('close', cleanup);
  });

  targetSocket.on('error', (err) => {
    console.error('🔌 WebSocket proxy error:', err.message);
    try {
      socket.destroy();
    } catch (e) {
      // Ignore cleanup errors
    }
  });
});

// Start server on port 3000
const PORT = 3000;
server.listen(PORT, '127.0.0.1', () => {
  console.log('✅ Reverse Proxy Server Running!');
  console.log('-'.repeat(35));
  console.log('🌐 Main Dashboard: http://localhost:3000/');
  console.log('📊 API Endpoints: http://localhost:3000/api/');
  console.log('💼 Portfolio: http://localhost:3000/portfolio/');
  console.log('🏥 Health Check: http://localhost:3000/health');
  console.log('');
  console.log('🔗 Proxying to Backend Services:');
  console.log('-'.repeat(32));
  console.log('⚡ FastAPI (8000) → /api/*');
  console.log('📈 Main Dashboard (8501) → /*');
  console.log('💰 Portfolio (8503) → /portfolio/*');
  console.log('');
  console.log(`✨ Proxy listening on http://127.0.0.1:${PORT}`);
  console.log('🔄 WebSocket support enabled for Streamlit');
  console.log('');
  console.log('🎯 This replaces nginx reload functionality!');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\\n🛑 Shutting down reverse proxy...');
  server.close(() => {
    console.log('✅ Proxy server stopped gracefully');
    process.exit(0);
  });
});

// Error handling
server.on('error', (error) => {
  if (error.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use`);
    console.log('💡 Stop other services or choose a different port');
  } else if (error.code === 'EACCES') {
    console.error(`❌ Permission denied for port ${PORT}`);
    console.log('💡 Try running as Administrator');
  } else {
    console.error('❌ Server error:', error.message);
  }
  process.exit(1);
});
