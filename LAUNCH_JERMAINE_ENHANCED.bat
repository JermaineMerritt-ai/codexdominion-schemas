@echo off
REM ============================================================================
REM JERMAINE SUPER ACTION AI - ENHANCED LAUNCHER
REM ============================================================================

echo.
echo ========================================================================
echo   JERMAINE SUPER ACTION AI - ENHANCED WITH COPILOT INSTRUCTIONS
echo ========================================================================
echo.
echo   Starting enhanced Jermaine with automatic instruction loading...
echo.
echo   Port: 8501
echo   Instructions: Auto-loaded from .github/copilot-instructions.md
echo.
echo   Press CTRL+C to stop
echo ========================================================================
echo.

REM Activate virtual environment and launch
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run jermaine_super_action_ai.py --server.port 8501

pause
