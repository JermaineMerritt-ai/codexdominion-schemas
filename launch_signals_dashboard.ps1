# 🔥 Codex Signals Dashboard Launcher
# ===================================

Write-Host "🔥 LAUNCHING CODEX SIGNALS DASHBOARD 📊" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow
Write-Host "The Merritt Method™ - Advanced Market Intelligence" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "codex_signals\dashboard.py")) {
    Write-Host "❌ Error: codex_signals\dashboard.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the codex-dominion directory." -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host "📦 Installing required packages..." -ForegroundColor Green
pip install streamlit plotly pandas dataclasses

# Launch dashboard
Write-Host ""
Write-Host "🚀 Starting Codex Signals Dashboard..." -ForegroundColor Green
Write-Host "Dashboard will be available at: http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "🔥 PORTFOLIO SIGNALS & MARKET INTELLIGENCE ACTIVATED 👑" -ForegroundColor Yellow
Write-Host ""

# Run the dashboard
streamlit run codex_signals/dashboard.py --server.port 8501 --server.address 0.0.0.0
