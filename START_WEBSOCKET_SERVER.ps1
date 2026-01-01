# =============================================================================
# START WEBSOCKET DEMO SERVER - PowerShell Launcher
# =============================================================================

Write-Host "=" -ForegroundColor Yellow -NoNewline
Write-Host ("=" * 79) -ForegroundColor Yellow
Write-Host "🔥 CODEX DOMINION - WEBSOCKET DEMO SERVER LAUNCHER 🔥" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Yellow -NoNewline
Write-Host ("=" * 79) -ForegroundColor Yellow
Write-Host ""

# Set UTF-8 encoding for console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Set environment variables for Python
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

Write-Host "📍 Starting WebSocket Demo Server..." -ForegroundColor Green
Write-Host "   - Server will run on: http://localhost:5000" -ForegroundColor White
Write-Host "   - Dashboard URL: http://localhost:5000/websocket-demo" -ForegroundColor White
Write-Host "   - Health Check: http://localhost:5000/health" -ForegroundColor White
Write-Host ""
Write-Host "✨ WebSocket Features:" -ForegroundColor Magenta
Write-Host "   - Real-time workflow progress updates" -ForegroundColor White
Write-Host "   - Live step-by-step execution tracking" -ForegroundColor White
Write-Host "   - Animated progress bars and indicators" -ForegroundColor White
Write-Host "   - Color-coded event logging" -ForegroundColor White
Write-Host ""
Write-Host "⚡ Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=" -ForegroundColor Yellow -NoNewline
Write-Host ("=" * 79) -ForegroundColor Yellow
Write-Host ""

# Start the Python server
try {
    python websocket_demo_server.py
} catch {
    Write-Host ""
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure Python virtual environment is activated" -ForegroundColor White
    Write-Host "2. Check if port 5000 is already in use" -ForegroundColor White
    Write-Host "3. Verify flask-socketio is installed: pip list | Select-String socketio" -ForegroundColor White
    Write-Host ""
    exit 1
}
