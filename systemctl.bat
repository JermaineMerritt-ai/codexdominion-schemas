@echo off
REM Windows equivalent of systemctl commands for Codex Dominion
REM Usage: systemctl.bat [action] [service]

setlocal EnableDelayedExpansion

set "ACTION=%1"
set "SERVICE=%2"
set "SCRIPT_DIR=%~dp0"

if "%ACTION%"=="" set "ACTION=status"
if "%SERVICE%"=="" set "SERVICE=all"

echo.
echo � CODEX DOMINION SERVICE CONTROL (Windows)
echo ==========================================
echo Equivalent to: sudo systemctl %ACTION% codex-dashboard
echo.

REM Map systemctl commands to our actions
if "%ACTION%"=="daemon-reload" goto :daemon_reload
if "%ACTION%"=="enable" goto :enable_service
if "%ACTION%"=="disable" goto :disable_service
if "%ACTION%"=="start" goto :start_service
if "%ACTION%"=="stop" goto :stop_service
if "%ACTION%"=="restart" goto :restart_service
if "%ACTION%"=="reload" goto :restart_service
if "%ACTION%"=="status" goto :service_status

echo Usage: %0 [daemon-reload^|enable^|disable^|start^|stop^|restart^|reload^|status] [all^|api^|dashboard^|portfolio^|proxy]
echo.
echo SYSTEMCTL EQUIVALENTS:
echo   sudo systemctl start codex-dashboard    ==^>  %0 start dashboard
echo   sudo systemctl stop codex-dashboard     ==^>  %0 stop dashboard  
echo   sudo systemctl restart codex-dashboard  ==^>  %0 restart dashboard
echo   sudo systemctl reload nginx             ==^>  %0 reload proxy
echo   sudo systemctl status codex-dashboard   ==^>  %0 status dashboard
goto :end

:daemon_reload
echo 🔄 Reloading service configuration...
echo ✅ Configuration reloaded (Windows equivalent)
goto :end

:enable_service
echo ⚡ Enabling Codex services...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-service-manager.ps1" -Action install -Service %SERVICE%
goto :end

:disable_service
echo 🚫 Disabling Codex services...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-service-manager.ps1" -Action uninstall -Service %SERVICE%
goto :end

:start_service
echo Starting Codex services...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-systemctl.ps1" start
goto :end

:stop_service
echo Stopping Codex services...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-systemctl.ps1" stop
goto :end

:restart_service
echo Restarting Codex services...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-systemctl.ps1" restart
goto :end

:service_status
echo Checking Codex service status...
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%codex-systemctl.ps1" status
goto :end

:end
echo.
echo ✨ Codex Dominion service control complete!
echo 🌐 Access your services at:
echo    Main Dashboard: http://127.0.0.1:8501
echo    Portfolio: http://127.0.0.1:8503  
echo    API Docs: http://127.0.0.1:8000/docs