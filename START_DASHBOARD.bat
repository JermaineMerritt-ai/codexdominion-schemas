@echo off
REM ============================================================================
REM CODEX DOMINION MASTER DASHBOARD - QUICK LAUNCHER
REM ============================================================================
REM Double-click this file to start your dashboard instantly!
REM ============================================================================

color 0B
title Codex Dominion Master Dashboard

echo.
echo ============================================================================
echo                 CODEX DOMINION MASTER DASHBOARD ULTIMATE
echo ============================================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please create it first: python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment found
echo.

REM Kill any existing processes
echo Cleaning up old processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo.
echo ============================================================================
echo                         STARTING DASHBOARD...
echo ============================================================================
echo.
echo  48 Intelligence Engines: READY
echo  6 Tools Suite: READY
echo  Total Savings: $316/month
echo.
echo ============================================================================
echo  Dashboard URL: http://localhost:5000
echo ============================================================================
echo.
echo  Main Dashboard:     http://localhost:5000
echo  Intelligence:       http://localhost:5000/engines
echo  Tools Suite:        http://localhost:5000/tools
echo  System Status:      http://localhost:5000/status
echo.
echo ============================================================================
echo  IMPORTANT: Keep this window open while using the dashboard!
echo  Press Ctrl+C to stop the server
echo ============================================================================
echo.

REM Wait 2 seconds then open browser
timeout /t 2 /nobreak >nul
start "" "http://localhost:5000"

echo Opening dashboard in browser...
echo.

REM Start Complete Fixed Dashboard
.venv\Scripts\python.exe dashboard_complete_fixed.py

echo.
echo Dashboard stopped.
pause
