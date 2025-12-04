# 🔥 CODEX DOMINION QUICK LAUNCHER 👑
# Bulletproof launcher for Digital Sovereignty Dashboard

Write-Host "🔥 LAUNCHING CODEX DOMINION DASHBOARD 👑" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Yellow

# Check if we're in the right directory
if (-not (Test-Path "codex_simple_dashboard.py")) {
    Write-Host "❌ Error: codex_simple_dashboard.py not found!" -ForegroundColor Red
    Write-Host "Please run this script from the codex-dominion directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "⚠️ Virtual environment not found. Using system Python." -ForegroundColor Yellow
    $pythonCmd = "python"
} else {
    Write-Host "✅ Using virtual environment Python" -ForegroundColor Green
    $pythonCmd = ".venv\Scripts\python.exe"
}

# Install streamlit if needed
Write-Host "📦 Checking Streamlit installation..." -ForegroundColor Cyan
try {
    & $pythonCmd -c "import streamlit; print('Streamlit available')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installing Streamlit..." -ForegroundColor Cyan
        & $pythonCmd -m pip install streamlit
    }
} catch {
    Write-Host "📦 Installing Streamlit..." -ForegroundColor Cyan
    & $pythonCmd -m pip install streamlit
}

# Create necessary JSON files if they don't exist
Write-Host "⚙️ Checking configuration files..." -ForegroundColor Cyan

if (-not (Test-Path "codex_ledger.json")) {
    "{}" | Out-File -FilePath "codex_ledger.json" -Encoding utf8
    Write-Host "✅ Created codex_ledger.json" -ForegroundColor Green
}

if (-not (Test-Path "accounts.json")) {
    "{}" | Out-File -FilePath "accounts.json" -Encoding utf8
    Write-Host "✅ Created accounts.json" -ForegroundColor Green
}

# Check Dawn Dispatch availability
Write-Host "🌅 Checking Dawn Dispatch system..." -ForegroundColor Cyan
try {
    & $pythonCmd -c "from codex_dawn_dispatch import dawn_dispatch; print('Dawn Dispatch ready')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dawn Dispatch system available" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Dawn Dispatch not available (dependencies missing)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Dawn Dispatch not available" -ForegroundColor Yellow
}

# Launch the dashboard
Write-Host ""
Write-Host "🚀 Launching Codex Dominion Dashboard..." -ForegroundColor Green
Write-Host "Dashboard will be available at: http://127.0.0.1:18080" -ForegroundColor White
Write-Host ""
Write-Host "🔥 DIGITAL SOVEREIGNTY ACTIVATED 👑" -ForegroundColor Yellow
Write-Host ""

# Kill any existing Streamlit processes
try {
    Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*streamlit*"} | Stop-Process -Force
} catch {
    # Ignore errors if no processes found
}

# Launch the dashboard
& $pythonCmd -m streamlit run codex_simple_dashboard.py --server.port 18080 --server.address 127.0.0.1
