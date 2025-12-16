@echo off
title CODEX DOMINION - Workflow Builder Web UI
color 0B
cls
echo.
echo ============================================================
echo    CODEX DOMINION - WORKFLOW BUILDER
echo    Visual Automation Platform
echo ============================================================
echo.
echo Starting Web UI on http://localhost:5557
echo Press Ctrl+C to stop the server
echo.

call .venv\Scripts\activate.bat
python workflow_builder_web.py
