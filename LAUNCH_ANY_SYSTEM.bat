@echo off
title CODEX DOMINION - System Launcher
color 0B
cls
echo.
echo ============================================================
echo    CODEX DOMINION - MASTER SYSTEM LAUNCHER
echo    Launch Any Service Instantly
echo ============================================================
echo.

.venv\Scripts\python.exe system_launcher.py
if errorlevel 1 (
    echo.
    echo Error running launcher. Press any key to exit.
    pause
)
