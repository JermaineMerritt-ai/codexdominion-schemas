@echo off
chcp 65001 >nul
echo CODEX DOMINION - COMPLETE AUTOMATION DASHBOARD (FIXED VERSION)
echo ================================================================
echo.

REM Kill existing Python processes
echo Cleaning up processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Launch dashboard in new window (using fixed dashboard_working.py)
echo Launching Flask dashboard...
start "CODEX DOMINION Dashboard" /D "%~dp0" cmd /k ".venv\Scripts\activate.bat && python dashboard_working.py"

REM Wait for Flask to start
timeout /t 4 /nobreak >nul

REM Open in default browser
start http://localhost:5000

echo.
echo ================================================================
echo   DASHBOARD LAUNCHED SUCCESSFULLY!
echo ================================================================
echo.
echo   Dashboard is running in a separate window
echo   Access: http://localhost:5000
echo.
echo   Available Tabs:
echo     - Home:          http://localhost:5000
echo     - Social Media:  http://localhost:5000/social
echo     - Affiliate:     http://localhost:5000/affiliate
echo     - Chatbot:       http://localhost:5000/chatbot
echo     - Algorithm:     http://localhost:5000/algorithm
echo     - Auto-Publish:  http://localhost:5000/autopublish
echo.
echo   13 tabs total - click through them all!
echo.
echo   Press any key to close this launcher window...
echo   (Dashboard will keep running in the other window)
echo ================================================================
pause >nul
goto :end

:success
echo 🔥 Dashboard launched successfully! 👑
echo Press any key to exit launcher...
pause >nul

:end
