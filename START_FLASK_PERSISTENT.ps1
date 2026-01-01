# START_FLASK_PERSISTENT.ps1
# Persistent Flask launcher that prevents premature exit

Write-Host "🔥 CODEX DOMINION - PERSISTENT FLASK LAUNCHER 👑" -ForegroundColor Yellow
Write-Host ""

# Activate virtual environment
$venvPath = ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "⚠️ Virtual environment not found at $venvPath" -ForegroundColor Red
    exit 1
}

# Set environment variables
$env:FLASK_APP = "flask_dashboard"
$env:FLASK_ENV = "production"
$env:FLASK_DEBUG = "0"

Write-Host "✓ Environment variables set" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting Flask on http://localhost:5000" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

# Start Flask with error handling
try {
    # Run Flask in the foreground (not background) so we can see any errors
    python -m flask run --host=0.0.0.0 --port=5000 --no-reload --no-debugger
    
    # If we get here, Flask exited normally
    Write-Host ""
    Write-Host "✓ Flask stopped normally" -ForegroundColor Yellow
} catch {
    Write-Host ""
    Write-Host "❌ Flask crashed with error:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Stack trace:" -ForegroundColor Gray
    Write-Host $_.ScriptStackTrace -ForegroundColor Gray
    exit 1
}

# Keep window open so we can see what happened
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
