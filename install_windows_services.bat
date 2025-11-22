@echo off
REM CODEX DOMINION - WINDOWS SERVICE DEPLOYMENT
REM This script creates Windows services for the Codex Dominion ecosystem using NSSM

echo 🔥 CODEX DOMINION - WINDOWS SERVICE DEPLOYMENT 🔥
echo ================================================

REM Check if NSSM is available
where nssm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ NSSM not found. Please install NSSM first:
    echo    Download from: https://nssm.cc/download
    echo    Add nssm.exe to your PATH
    pause
    exit /b 1
)

REM Set paths (adjust these for your environment)
set CODEX_PATH=C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
set PYTHON_PATH=python

echo 📁 Codex Path: %CODEX_PATH%
echo 🐍 Python Path: %PYTHON_PATH%

REM Create Codex Main Dashboard Service
echo.
echo 🎯 Creating Codex Main Dashboard Service...
nssm install "Codex-Main" "%PYTHON_PATH%" "-m streamlit run codex_summary.py --server.port=8080 --server.address=127.0.0.1"
nssm set "Codex-Main" AppDirectory "%CODEX_PATH%"
nssm set "Codex-Main" DisplayName "Codex Dominion - Main Dashboard"
nssm set "Codex-Main" Description "Main control interface for Codex Dominion digital sovereignty"
nssm set "Codex-Main" Start SERVICE_AUTO_START
nssm set "Codex-Main" AppStdout "%CODEX_PATH%\logs\codex-main.log"
nssm set "Codex-Main" AppStderr "%CODEX_PATH%\logs\codex-main-error.log"

REM Create Contributions Interface Service
echo.
echo 👥 Creating Contributions Interface Service...
nssm install "Codex-Contributions" "%PYTHON_PATH%" "-m streamlit run contributions.py --server.port=8083 --server.address=127.0.0.1"
nssm set "Codex-Contributions" AppDirectory "%CODEX_PATH%"
nssm set "Codex-Contributions" DisplayName "Codex Dominion - Community Contributions"
nssm set "Codex-Contributions" Description "Community interface for submitting sacred words"
nssm set "Codex-Contributions" Start SERVICE_AUTO_START
nssm set "Codex-Contributions" AppStdout "%CODEX_PATH%\logs\codex-contributions.log"
nssm set "Codex-Contributions" AppStderr "%CODEX_PATH%\logs\codex-contributions-error.log"

REM Create Council Oversight Service
echo.
echo 👑 Creating Council Oversight Service...
nssm install "Codex-Council" "%PYTHON_PATH%" "-m streamlit run enhanced_council_oversight.py --server.port=8086 --server.address=127.0.0.1"
nssm set "Codex-Council" AppDirectory "%CODEX_PATH%"
nssm set "Codex-Council" DisplayName "Codex Dominion - Council Oversight"
nssm set "Codex-Council" Description "Sacred council interface for governance authority"
nssm set "Codex-Council" Start SERVICE_AUTO_START
nssm set "Codex-Council" AppStdout "%CODEX_PATH%\logs\codex-council.log"
nssm set "Codex-Council" AppStderr "%CODEX_PATH%\logs\codex-council-error.log"

REM Create Contributions Viewer Service
echo.
echo 📊 Creating Contributions Viewer Service...
nssm install "Codex-Viewer" "%PYTHON_PATH%" "-m streamlit run contributions_viewer.py --server.port=8090 --server.address=127.0.0.1"
nssm set "Codex-Viewer" AppDirectory "%CODEX_PATH%"
nssm set "Codex-Viewer" DisplayName "Codex Dominion - Contributions Viewer"
nssm set "Codex-Viewer" Description "Public interface for viewing community contributions"
nssm set "Codex-Viewer" Start SERVICE_AUTO_START
nssm set "Codex-Viewer" AppStdout "%CODEX_PATH%\logs\codex-viewer.log"
nssm set "Codex-Viewer" AppStderr "%CODEX_PATH%\logs\codex-viewer-error.log"

REM Create logs directory
echo.
echo 📂 Creating logs directory...
if not exist "%CODEX_PATH%\logs" mkdir "%CODEX_PATH%\logs"

echo.
echo ✅ CODEX DOMINION SERVICES CREATED SUCCESSFULLY!
echo.
echo 🚀 To start services:
echo    net start "Codex-Main"
echo    net start "Codex-Contributions"  
echo    net start "Codex-Council"
echo    net start "Codex-Viewer"
echo.
echo 🛑 To stop services:
echo    net stop "Codex-Main"
echo    net stop "Codex-Contributions"
echo    net stop "Codex-Council"  
echo    net stop "Codex-Viewer"
echo.
echo 🗑️ To remove services:
echo    nssm remove "Codex-Main" confirm
echo    nssm remove "Codex-Contributions" confirm
echo    nssm remove "Codex-Council" confirm
echo    nssm remove "Codex-Viewer" confirm
echo.
echo 🔥 DIGITAL SOVEREIGNTY SERVICES READY! 🔥

pause