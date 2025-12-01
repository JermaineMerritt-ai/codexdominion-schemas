const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const fs = require('fs');
const https = require('https');

const app = express();

// Security headers middleware
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer-when-downgrade');
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self' http: https: data: blob: 'unsafe-inline'"
  );
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      dashboard: 'http://127.0.0.1:8501',
      api: 'http://127.0.0.1:8000',
      portfolio: 'http://127.0.0.1:8503',
    },
  });
});

// API proxy (equivalent to nginx location /api/)
app.use(
  '/api',
  createProxyMiddleware({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    pathRewrite: {
      '^/api': '', // Remove /api prefix when forwarding
    },
    ws: true, // Enable WebSocket proxying
    onError: (err, req, res) => {
      console.error('API Proxy Error:', err.message);
      res.status(502).json({ error: 'API service unavailable' });
    },
  })
);

// Portfolio Dashboard proxy (equivalent to nginx location /portfolio/)
app.use(
  '/portfolio',
  createProxyMiddleware({
    target: 'http://127.0.0.1:8503',
    changeOrigin: true,
    pathRewrite: {
      '^/portfolio': '', // Remove /portfolio prefix when forwarding
    },
    ws: true, // Enable WebSocket proxying for Streamlit
    onError: (err, req, res) => {
      console.error('Portfolio Proxy Error:', err.message);
      res.status(502).json({ error: 'Portfolio service unavailable' });
    },
  })
);

// Main dashboard proxy (equivalent to nginx location /)
app.use(
  '/',
  createProxyMiddleware({
    target: 'http://127.0.0.1:8501',
    changeOrigin: true,
    ws: true, // Enable WebSocket proxying for Streamlit
    onError: (err, req, res) => {
      console.error('Dashboard Proxy Error:', err.message);
      res.status(502).json({ error: 'Dashboard service unavailable' });
    },
  })
);

// Start HTTP server (equivalent to nginx listen 80)
const httpPort = 80;
app.listen(httpPort, () => {
  console.log(`🚀 AIStoreLab.com Proxy Server running on port ${httpPort}`);
  console.log('📊 Routes configured:');
  console.log('  / → http://127.0.0.1:8501 (Main Dashboard)');
  console.log('  /api → http://127.0.0.1:8000 (API Endpoints)');
  console.log('  /portfolio → http://127.0.0.1:8503 (Portfolio Dashboard)');
  console.log('  /health → Health Check');
  console.log('');
  console.log('🔗 Access your site at: http://localhost');
  console.log('📋 Health check: http://localhost/health');
});

// HTTPS server setup (equivalent to nginx listen 443 ssl)
// Uncomment and configure when you have SSL certificates
/*
const httpsOptions = {
    key: fs.readFileSync('/path/to/ssl/private.key'),
    cert: fs.readFileSync('/path/to/ssl/certificate.crt')
};

const httpsPort = 443;
https.createServer(httpsOptions, app).listen(httpsPort, () => {
    console.log(`🔒 HTTPS Server running on port ${httpsPort}`);
    console.log('🔗 Access your site at: https://localhost');
});
*/

// Export for testing
module.exports = app;
