@echo off
title CODEX DOMINION - Workflow Builder Setup
color 0B
echo.
echo ============================================================
echo    CODEX DOMINION - WORKFLOW BUILDER
echo    Installing Dependencies...
echo ============================================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install required packages
echo Installing Flask, requests, and schedule...
python -m pip install -q Flask==3.0.0 requests==2.31.0 schedule==1.2.0 Werkzeug==3.0.1

echo.
echo ============================================================
echo    Starting Workflow Builder...
echo ============================================================
echo.
echo Choose an option:
echo.
echo 1. Start Web UI (http://localhost:5557)
echo 2. CLI Interface
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Starting Web UI on http://localhost:5557
    echo Press Ctrl+C to stop
    echo.
    python workflow_builder_web.py
) else (
    python workflow_builder.py
)

pause
