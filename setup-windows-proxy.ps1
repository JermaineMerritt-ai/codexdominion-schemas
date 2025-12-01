# Codex Dominion - Windows Reverse Proxy Setup
# PowerShell script for setting up URL routing on Windows

$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up Codex Dominion Reverse Proxy for Windows" -ForegroundColor Green
Write-Host "=" * 60

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit 1
}

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    } catch {
        return $false
    }
}

# Check if required ports are running
Write-Host "🔍 Checking Codex services..." -ForegroundColor Cyan

$services = @{
    8501 = "Main Dashboard"
    8503 = "Portfolio Dashboard"  
    8000 = "FastAPI Backend"
}

$runningServices = @()

foreach ($port in $services.Keys) {
    $connections = netstat -an | Select-String ":$port.*LISTENING"
    if ($connections) {
        Write-Host "✅ $($services[$port]) running on port $port" -ForegroundColor Green
        $runningServices += $port
    } else {
        Write-Host "❌ $($services[$port]) not running on port $port" -ForegroundColor Red
    }
}

if ($runningServices.Count -eq 0) {
    Write-Host "⚠️  No Codex services are currently running!" -ForegroundColor Yellow
    Write-Host "Please start your services first:" -ForegroundColor Yellow
    Write-Host "  python -m streamlit run codex_simple_dashboard.py --server.port 8501" -ForegroundColor Cyan
    Write-Host "  python -m streamlit run codex_portfolio_dashboard.py --server.port 8503" -ForegroundColor Cyan
    Write-Host "  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000" -ForegroundColor Cyan
}

# Create URL reservations for port 80 (requires admin)
Write-Host "🔧 Setting up URL reservations..." -ForegroundColor Cyan

$urlReservations = @(
    "http://+:80/",
    "http://+:80/portfolio/",
    "http://+:80/api/",
    "http://+:80/docs/",
    "http://+:80/health/"
)

foreach ($url in $urlReservations) {
    try {
        netsh http add urlacl url=$url user=Everyone 2>$null
        Write-Host "✅ Added URL reservation: $url" -ForegroundColor Green
    } catch {
        Write-Host "ℹ️  URL reservation may already exist: $url" -ForegroundColor Yellow
    }
}

# Create a simple Node.js reverse proxy
Write-Host "📦 Creating reverse proxy server..." -ForegroundColor Cyan

$proxyScript = @"
const http = require('http');
const httpProxy = require('http-proxy');

// Create proxy server
const proxy = httpProxy.createProxyServer();

// Error handling
proxy.on('error', (err, req, res) => {
    console.log('Proxy error:', err.message);
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Service temporarily unavailable');
});

// Create main server
const server = http.createServer((req, res) => {
    const url = req.url;
    
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    console.log(`[`${new Date().toISOString()}`] `${req.method} `${url}`);
    
    // Route requests
    if (url.startsWith('/portfolio')) {
        // Portfolio Dashboard (port 8503)
        proxy.web(req, res, { 
            target: 'http://127.0.0.1:8503',
            changeOrigin: true
        });
    } else if (url.startsWith('/api') || url.startsWith('/docs') || url.startsWith('/openapi.json') || url.startsWith('/health')) {
        // FastAPI Backend (port 8000)
        proxy.web(req, res, { 
            target: 'http://127.0.0.1:8000',
            changeOrigin: true
        });
    } else {
        // Main Dashboard (port 8501)
        proxy.web(req, res, { 
            target: 'http://127.0.0.1:8501',
            changeOrigin: true
        });
    }
});

// WebSocket proxying
server.on('upgrade', (req, socket, head) => {
    const url = req.url;
    
    if (url.startsWith('/portfolio')) {
        proxy.ws(req, socket, head, { target: 'http://127.0.0.1:8503' });
    } else {
        proxy.ws(req, socket, head, { target: 'http://127.0.0.1:8501' });
    }
});

const PORT = 80;
server.listen(PORT, () => {
    console.log('🚀 Codex Dominion Reverse Proxy Server running on port', PORT);
    console.log('📊 Main Dashboard: http://localhost/');
    console.log('💼 Portfolio Manager: http://localhost/portfolio');  
    console.log('🔗 API Backend: http://localhost/api');
    console.log('📚 API Docs: http://localhost/docs');
});

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log('❌ Port 80 is already in use. Stop other web servers or run on different port.');
    } else {
        console.log('Server error:', err);
    }
});
"@

# Write proxy script
$proxyScript | Out-File -FilePath "codex-proxy-server.js" -Encoding utf8

Write-Host "✅ Created reverse proxy script: codex-proxy-server.js" -ForegroundColor Green

# Create batch file to start proxy
$batchScript = @"
@echo off
echo 🚀 Starting Codex Dominion Reverse Proxy...
echo.
echo Make sure Node.js is installed and run:
echo   npm install http-proxy
echo   node codex-proxy-server.js
echo.
pause
"@

$batchScript | Out-File -FilePath "start-codex-proxy.bat" -Encoding ascii

Write-Host "✅ Created startup script: start-codex-proxy.bat" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Windows reverse proxy setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Install Node.js if not already installed" -ForegroundColor Yellow
Write-Host "2. Run: npm install http-proxy" -ForegroundColor Yellow
Write-Host "3. Run: node codex-proxy-server.js" -ForegroundColor Yellow
Write-Host "   OR double-click: start-codex-proxy.bat" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Your services will be available at:" -ForegroundColor Cyan
Write-Host "   Main Dashboard:     http://localhost/" -ForegroundColor White
Write-Host "   Portfolio Manager:  http://localhost/portfolio" -ForegroundColor White
Write-Host "   API Backend:        http://localhost/api" -ForegroundColor White
Write-Host "   API Documentation:  http://localhost/docs" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue..."