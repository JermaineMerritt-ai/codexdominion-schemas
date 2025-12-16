@echo off
REM ============================================================================
REM CODEX DOMINION - COMPLETE AUTOMATION SYSTEM LAUNCHER
REM ============================================================================
REM One-click launcher for the complete system with all new features
REM ============================================================================

echo.
echo ========================================================================
echo      CODEX DOMINION - COMPLETE AUTOMATION SYSTEM
echo ========================================================================
echo.
echo  Starting your digital empire control center...
echo.
echo  NEW FEATURES INCLUDED:
echo    - Website Builder
echo    - Store Builder
echo    - Social Media Automation (6 platforms)
echo    - Affiliate Marketing Manager
echo    - Action Chatbot AI
echo    - Algorithm Action AI
echo    - Auto-Publish Orchestration (Jermaine Super Action AI)
echo.
echo ========================================================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Launch the complete system
python launch_complete_system.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ========================================================================
    echo  ERROR: Something went wrong
    echo ========================================================================
    echo.
    pause
)
