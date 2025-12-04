@echo off
echo 🔥 CODEX DOMINION - QUICK LAUNCHER 🔥
echo =====================================
echo.

REM Check if app.py exists
if not exist "app.py" (
    echo ❌ app.py not found in current directory
    echo    Please run this script from the Codex Dominion directory
    pause
    exit /b 1
)

echo 🚀 Starting Codex Dashboard...
echo    Access at: http://localhost:8095
echo    Press Ctrl+C to stop
echo.

python -m streamlit run app.py --server.port 8095

echo.
echo 🛑 Codex Dashboard stopped
pause
