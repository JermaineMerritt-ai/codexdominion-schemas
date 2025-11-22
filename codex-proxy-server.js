const http = require('http');
const httpProxy = require('http-proxy-middleware');
const express = require('express');

console.log('🚀 CODEX DOMINION REVERSE PROXY SERVER');
console.log('=' .repeat(50));

const app = express();

// Create proxy middleware for each service
const apiProxy = httpProxy({
    target: 'http://127.0.0.1:8000',
    changeOrigin: true,
    ws: true,
    logLevel: 'info'
});

const dashboardProxy = httpProxy({
    target: 'http://127.0.0.1:8501', 
    changeOrigin: true,
    ws: true,
    logLevel: 'info'
});

const portfolioProxy = httpProxy({
    target: 'http://127.0.0.1:8503',
    changeOrigin: true, 
    ws: true,
    logLevel: 'info'
});

// Route configuration
app.use('/api', apiProxy);
app.use('/portfolio', portfolioProxy);
app.use('/', dashboardProxy);

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        services: {
            'api': 'http://127.0.0.1:8000',
            'dashboard': 'http://127.0.0.1:8501', 
            'portfolio': 'http://127.0.0.1:8503'
        },
        proxy_port: 80
    });
});

const server = app.listen(80, '0.0.0.0', () => {
    console.log('✅ Proxy Server Status:');
    console.log('-'.repeat(25));
    console.log('🌐 Main URL: http://localhost');
    console.log('📊 API: http://localhost/api');
    console.log('💼 Portfolio: http://localhost/portfolio');
    console.log('🏥 Health: http://localhost/health');
    console.log('');
    console.log('🔗 Backend Services:');
    console.log('-'.repeat(20));
    console.log('⚡ FastAPI: 127.0.0.1:8000');
    console.log('📈 Dashboard: 127.0.0.1:8501');
    console.log('💰 Portfolio: 127.0.0.1:8503');
    console.log('');
    console.log('✨ Proxy server running on port 80');
});

// Handle WebSocket upgrades
server.on('upgrade', (request, socket, head) => {
    const url = request.url;
    
    if (url.startsWith('/api')) {
        apiProxy.upgrade(request, socket, head);
    } else if (url.startsWith('/portfolio')) {
        portfolioProxy.upgrade(request, socket, head);
    } else {
        dashboardProxy.upgrade(request, socket, head);
    }
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
process.on('uncaughtException', (error) => {
    console.error('❌ Uncaught Exception:', error.message);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Rejection:', reason);
});