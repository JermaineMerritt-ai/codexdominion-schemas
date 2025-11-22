@echo off
REM CODEX DOMINION - IONOS DEPLOYMENT LAUNCHER
REM Quick deployment script for Windows users

setlocal
set "DEPLOY_DIR=ionos_deployment_package"

echo.
echo 🔥 CODEX DOMINION - IONOS DEPLOYMENT LAUNCHER
echo ===============================================
echo.

if "%1"=="" (
    echo Usage: %0 [server-address] [username]
    echo Example: %0 your-server.aistorelab.com root
    echo          %0 192.168.1.100 ubuntu
    echo.
    echo Available deployment files:
    dir /b %DEPLOY_DIR% 2>nul || echo   No deployment package found - run deploy_to_ionos.py first
    echo.
    pause
    exit /b 1
)

set "SERVER=%1"
set "USERNAME=%2"
if "%USERNAME%"=="" set "USERNAME=root"

echo 📡 Target Server: %SERVER%
echo 👤 Username: %USERNAME%
echo 📁 Package: %DEPLOY_DIR%
echo.

if not exist "%DEPLOY_DIR%" (
    echo ❌ Deployment package not found!
    echo 💡 Run: python deploy_to_ionos.py
    pause
    exit /b 1
)

echo 📤 Starting file upload to IONOS...
echo.

REM Upload all files
cd %DEPLOY_DIR%
echo Uploading deployment files...
scp * %USERNAME%@%SERVER%:/tmp/

if %errorlevel% neq 0 (
    echo.
    echo ❌ Upload failed!
    echo 💡 Check your SSH connection and credentials
    pause
    exit /b 1
)

echo.
echo ✅ Files uploaded successfully!
echo.
echo 🚀 Next steps - SSH to your IONOS server:
echo.
echo    ssh %USERNAME%@%SERVER%
echo    cd /tmp
echo    chmod +x ionos_codex_deploy.sh
echo    sudo ./ionos_codex_deploy.sh
echo.
echo After deployment setup:
echo    chmod +x ionos_systemctl_commands.sh  
echo    sudo ./ionos_systemctl_commands.sh
echo.
echo 🔥 Your Codex Dominion will be available at:
echo    https://codex.aistorelab.com
echo.

pause