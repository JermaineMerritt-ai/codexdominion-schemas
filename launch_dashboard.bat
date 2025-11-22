@echo off
echo 🔥 CODEX DASHBOARD QUICK LAUNCHER 👑
echo =====================================
echo.

REM Kill existing processes
echo 🧹 Cleaning up processes...
taskkill /f /im python.exe /t >nul 2>&1
timeout /t 2 /nobreak >nul

REM Check for virtual environment
if exist ".venv\Scripts\python.exe" (
    echo ✅ Using virtual environment
    set PYTHON_EXE=.venv\Scripts\python.exe
) else (
    echo ⚠️ Using system Python
    set PYTHON_EXE=python
)

REM Launch dashboard
echo 🚀 Starting Codex Dashboard...
echo.

REM Try different ports
for %%p in (18080 18081 18082 18083) do (
    echo Trying port %%p...
    start /min "" %PYTHON_EXE% -m streamlit run codex_simple_dashboard.py --server.port %%p --server.address 127.0.0.1
    timeout /t 3 /nobreak >nul
    
    REM Check if successful by trying to connect
    curl -s -o nul http://127.0.0.1:%%p --connect-timeout 2
    if %errorlevel%==0 (
        echo ✅ Dashboard running on port %%p
        echo.
        echo 🎯 ACCESS YOUR DASHBOARD:
        echo http://127.0.0.1:%%p
        echo.
        echo 📺 Available Features:
        echo • 🏛️ Dominion Central
        echo • 🌅 Dawn Dispatch  
        echo • 📺 YouTube Charts
        echo • 📊 System Status
        echo.
        start http://127.0.0.1:%%p
        goto :success
    )
)

echo ❌ Could not start dashboard on any port
goto :end

:success
echo 🔥 Dashboard launched successfully! 👑
echo Press any key to exit launcher...
pause >nul

:end