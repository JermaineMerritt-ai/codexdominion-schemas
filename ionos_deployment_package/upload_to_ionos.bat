@echo off
REM Windows batch script to upload Codex Dashboard files to IONOS server
REM Usage: upload_to_ionos.bat [server-ip-or-domain] [username]

setlocal

if "%1"=="" (
    echo Usage: %0 [server-ip] [username]
    echo Example: %0 your-server.com ubuntu
    exit /b 1
)

set "SERVER=%1"
set "USER=%2"
if "%USER%"=="" set "USER=root"

echo.
echo 🔥 UPLOADING CODEX DASHBOARD TO IONOS
echo ====================================
echo 📡 Server: %SERVER%
echo 👤 User: %USER%
echo.

REM Check if files exist
if not exist "app.py" (
    echo ❌ app.py not found in current directory
    exit /b 1
)

if not exist "codex_ledger.json" (
    echo ❌ codex_ledger.json not found in current directory
    exit /b 1
)

echo 📤 Uploading application files...
scp app.py codex_ledger.json omega_seal.py %USER%@%SERVER%:/tmp/
if %errorlevel% neq 0 (
    echo ❌ Failed to upload application files
    exit /b 1
)

echo 📤 Uploading deployment scripts...
scp ionos_codex_deploy.sh ionos_systemctl_commands.sh %USER%@%SERVER%:/tmp/
if %errorlevel% neq 0 (
    echo ❌ Failed to upload deployment scripts
    exit /b 1
)

echo 📤 Uploading configuration files...
scp ionos_codex_dashboard.service ionos_nginx_codex.conf %USER%@%SERVER%:/tmp/
if %errorlevel% neq 0 (
    echo ❌ Failed to upload configuration files
    exit /b 1
)

echo.
echo ✅ All files uploaded successfully!
echo.
echo 🚀 Next steps on your IONOS server:
echo    ssh %USER%@%SERVER%
echo    chmod +x /tmp/ionos_codex_deploy.sh
echo    sudo /tmp/ionos_codex_deploy.sh
echo.
echo 🎯 Then run your systemctl commands:
echo    sudo systemctl daemon-reload
echo    sudo systemctl enable codex-dashboard  
echo    sudo systemctl start codex-dashboard
echo    sudo systemctl status codex-dashboard
echo.
echo 🔥 Codex Dashboard ready for IONOS deployment!

pause