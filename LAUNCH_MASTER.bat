@echo off
chcp 65001 >nul
title CODEX DOMINION - Master System Launcher

echo.
echo ================================================================
echo   🔥 CODEX DOMINION - MASTER SYSTEM LAUNCHER 👑
echo ================================================================
echo.
echo   Intelligent dashboard detection and launch system
echo   Automatically selects the best available dashboard
echo.
echo ================================================================
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
    echo.
)

REM Launch the Python master launcher
python MASTER_LAUNCHER.py

echo.
echo ================================================================
pause
