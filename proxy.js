const http = require('http');
const url = require('url');

console.log('🚀 CODEX DOMINION REVERSE PROXY');
console.log('='.repeat(40));

// Service configuration
const services = {
  '/api': { host: '127.0.0.1', port: 8000 },
  '/portfolio': { host: '127.0.0.1', port: 8503 },
  '/': { host: '127.0.0.1', port: 8501 },
};

const PROXY_PORT = 3001;

function proxyRequest(clientReq, clientRes) {
  const reqUrl = url.parse(clientReq.url);
  let target = services['/']; // Default to main dashboard
  let targetPath = clientReq.url;

  // Find matching service and adjust path
  for (const [path, service] of Object.entries(services)) {
    if (path !== '/' && reqUrl.pathname.startsWith(path)) {
      target = service;
      targetPath = clientReq.url.replace(path, '');
      if (!targetPath.startsWith('/')) {
        targetPath = '/' + targetPath;
      }
      break;
    }
  }

  console.log(
    `🔀 ${clientReq.method} ${reqUrl.pathname} → ${target.host}:${target.port}${targetPath}`
  );

  const options = {
    hostname: target.host,
    port: target.port,
    path: targetPath,
    method: clientReq.method,
    headers: {
      ...clientReq.headers,
      host: `${target.host}:${target.port}`,
    },
  };

  const proxyReq = http.request(options, (proxyRes) => {
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes);
  });

  proxyReq.on('error', (err) => {
    console.error(`❌ Error: ${err.message}`);
    if (!clientRes.headersSent) {
      clientRes.writeHead(502, { 'Content-Type': 'text/plain' });
      clientRes.end(`Service unavailable: ${target.host}:${target.port}`);
    }
  });

  clientReq.pipe(proxyReq);
}

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(
      JSON.stringify({
        status: 'running',
        port: PROXY_PORT,
        services: services,
        urls: {
          dashboard: `http://localhost:${PROXY_PORT}/`,
          api: `http://localhost:${PROXY_PORT}/api/`,
          portfolio: `http://localhost:${PROXY_PORT}/portfolio/`,
        },
      })
    );
    return;
  }

  proxyRequest(req, res);
});

server.listen(PROXY_PORT, '127.0.0.1', () => {
  console.log('✅ PROXY READY!');
  console.log(`🌐 Dashboard: http://localhost:${PROXY_PORT}/`);
  console.log(`📊 API: http://localhost:${PROXY_PORT}/api/`);
  console.log(`💼 Portfolio: http://localhost:${PROXY_PORT}/portfolio/`);
  console.log(`🏥 Health: http://localhost:${PROXY_PORT}/health`);
  console.log('');
  console.log('Press Ctrl+C to stop');
});

server.on('error', (err) => {
  console.error('❌ Server error:', err.message);
  if (err.code === 'EADDRINUSE') {
    console.log(`Port ${PROXY_PORT} is busy, try a different port`);
  }
});

process.on('SIGINT', () => {
  console.log('\\n🛑 Stopping proxy...');
  server.close();
  process.exit(0);
});
