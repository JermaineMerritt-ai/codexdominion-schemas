@echo off
echo.
echo ===============================================
echo  DOT300 ACTION AI - 300 AGENTS SYSTEM
echo  Multi-Agent Orchestration Platform
echo ===============================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run DOT300 system
python dot300_multi_agent.py

echo.
echo ===============================================
echo  DOT300 system execution complete!
echo ===============================================
echo.
echo Press any key to view agent data...
pause

REM Open agent database in default JSON viewer
start dot300_agents.json

pause
