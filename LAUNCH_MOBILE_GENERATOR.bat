@echo off
echo.
echo ===============================================
echo  CODEX DOMINION - MOBILE APP GENERATOR
echo  Auto-generating Flutter + React Native Apps
echo ===============================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run generator with option 3 (both apps)
echo 3 | python mobile_dashboard.py

echo.
echo ===============================================
echo  Mobile apps generated successfully!
echo ===============================================
echo.
echo Press any key to view the generated files...
pause

REM Open the mobile_apps directory in Explorer
explorer mobile_apps

pause
