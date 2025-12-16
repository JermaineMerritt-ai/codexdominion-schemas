@echo off
REM ============================================================================
REM CODEX DOMINION - COMPLETE SYSTEM LAUNCHER
REM ============================================================================

color 0B
title 🚀 Codex Dominion - Complete System Launcher

echo.
echo ============================================================================
echo              🚀 CODEX DOMINION - COMPLETE SYSTEM LAUNCHER
echo ============================================================================
echo.
echo Select what to launch:
echo.
echo  [1] Main Dashboard (Port 5555) - 13 tabs with ALL systems
echo  [2] Unified Launcher (Port 5556) - Access all 53+ dashboards
echo  [3] Audio Studio (Port 8502) - Voice, Music, Editing
echo  [4] Jermaine Super Action AI (Port 8501) - Interactive AI
echo  [5] All Systems (Main + Unified + Audio)
echo.
echo  [0] Exit
echo.
echo ============================================================================
echo.

set /p choice="Enter your choice (0-5): "

if "%choice%"=="1" goto main
if "%choice%"=="2" goto unified
if "%choice%"=="3" goto audio
if "%choice%"=="4" goto jermaine
if "%choice%"=="5" goto all
if "%choice%"=="0" goto end

echo Invalid choice!
pause
goto end

:main
echo.
echo ✅ Launching Main Dashboard on port 5555...
echo.
start cmd /k ".venv\Scripts\python.exe dashboard_working.py"
timeout /t 3
start "" "http://localhost:5555"
echo.
echo ✅ Main Dashboard launched!
echo 👉 Access at: http://localhost:5555
echo.
pause
goto end

:unified
echo.
echo ✅ Launching Unified Launcher on port 5556...
echo.
start cmd /k ".venv\Scripts\python.exe unified_launcher.py"
timeout /t 3
start "" "http://localhost:5556"
echo.
echo ✅ Unified Launcher launched!
echo 👉 Access at: http://localhost:5556
echo.
pause
goto end

:audio
echo.
echo ✅ Launching Audio Studio on port 8502...
echo.
start cmd /k ".venv\Scripts\python.exe -m streamlit run audio_studio.py --server.port 8502"
timeout /t 5
start "" "http://localhost:8502"
echo.
echo ✅ Audio Studio launched!
echo 👉 Access at: http://localhost:8502
echo.
pause
goto end

:jermaine
echo.
echo ✅ Launching Jermaine Super Action AI on port 8501...
echo.
start cmd /k ".venv\Scripts\python.exe -m streamlit run jermaine_super_action_ai.py --server.port 8501"
timeout /t 5
start "" "http://localhost:8501"
echo.
echo ✅ Jermaine Super Action AI launched!
echo 👉 Access at: http://localhost:8501
echo.
pause
goto end

:all
echo.
echo ✅ Launching ALL SYSTEMS...
echo.
echo Starting Main Dashboard (5555)...
start cmd /k ".venv\Scripts\python.exe dashboard_working.py"
timeout /t 3

echo Starting Unified Launcher (5556)...
start cmd /k ".venv\Scripts\python.exe unified_launcher.py"
timeout /t 3

echo Starting Audio Studio (8502)...
start cmd /k ".venv\Scripts\python.exe -m streamlit run audio_studio.py --server.port 8502"
timeout /t 5

echo.
echo ============================================================================
echo  ✅ ALL SYSTEMS LAUNCHED!
echo ============================================================================
echo.
echo  👉 Main Dashboard:      http://localhost:5555
echo  👉 Unified Launcher:    http://localhost:5556
echo  👉 Audio Studio:        http://localhost:8502
echo.
echo ============================================================================
echo.
start "" "http://localhost:5555"
timeout /t 2
start "" "http://localhost:5556"
echo.
pause
goto end

:end
echo.
echo ============================================================================
echo  🔥 The Flame Burns Sovereign and Eternal!
echo ============================================================================
echo.
