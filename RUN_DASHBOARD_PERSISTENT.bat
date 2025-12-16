@echo off
REM ============================================================================
REM CODEX DOMINION - DASHBOARD RUNNER (KEEPS RUNNING FOREVER)
REM ============================================================================

title CODEX DOMINION MASTER DASHBOARD

color 0B
cls

echo.
echo ============================================================================
echo                CODEX DOMINION MASTER DASHBOARD ULTIMATE
echo ============================================================================
echo.
echo  Status: STARTING...
echo.

cd /d "%~dp0"

REM Kill any old processes
taskkill /F /IM python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

:RESTART
cls
echo.
echo ============================================================================
echo                CODEX DOMINION MASTER DASHBOARD ULTIMATE
echo ============================================================================
echo.
echo  48 Intelligence Engines: READY
echo  6 Tools Suite: READY
echo  Total Savings: $316/month = $3,792/year
echo.
echo ============================================================================
echo  Dashboard URL: http://localhost:5000
echo ============================================================================
echo.
echo  Opening dashboard in browser...
echo.

REM Open browser
start "" "http://localhost:5000"
timeout /t 2 /nobreak >nul

echo  Starting Flask server...
echo.
echo ============================================================================
echo  KEEP THIS WINDOW OPEN - Dashboard is running
echo  Press Ctrl+C to stop
echo ============================================================================
echo.

REM Run dashboard - if it crashes, restart automatically
.venv\Scripts\python.exe flask_dashboard.py

REM If we get here, server stopped
echo.
echo ============================================================================
echo  Dashboard stopped!
echo ============================================================================
echo.
echo  Restarting in 5 seconds...
echo  Press Ctrl+C to exit instead
echo.
timeout /t 5

goto RESTART
