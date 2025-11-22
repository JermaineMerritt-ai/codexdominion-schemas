@echo off
echo.
echo ===============================================
echo   CODEX DOMINION FIREWALL CONFIGURATION
echo ===============================================
echo.

REM Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges
    echo Right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo Running with Administrator privileges...
echo.

echo Configuring Windows Firewall Rules...
echo.

echo Adding HTTP Port 80...
netsh advfirewall firewall add rule name="Codex HTTP Port 80" dir=in action=allow protocol=TCP localport=80

echo Adding HTTPS Port 443...  
netsh advfirewall firewall add rule name="Codex HTTPS Port 443" dir=in action=allow protocol=TCP localport=443

echo Adding API Port 8000...
netsh advfirewall firewall add rule name="Codex API Port 8000" dir=in action=allow protocol=TCP localport=8000

echo Adding Dashboard Port 8501...
netsh advfirewall firewall add rule name="Codex Dashboard Port 8501" dir=in action=allow protocol=TCP localport=8501

echo Adding Portfolio Port 8503...
netsh advfirewall firewall add rule name="Codex Portfolio Port 8503" dir=in action=allow protocol=TCP localport=8503

echo Adding Proxy Port 3000...
netsh advfirewall firewall add rule name="Codex Proxy Port 3000" dir=in action=allow protocol=TCP localport=3000

echo.
echo ===============================================
echo   FIREWALL CONFIGURATION COMPLETE!
echo ===============================================
echo.
echo Your Codex Dominion services are now accessible:
echo   HTTP: Port 80
echo   HTTPS: Port 443  
echo   API: Port 8000
echo   Dashboard: Port 8501
echo   Portfolio: Port 8503
echo   Proxy: Port 3000
echo.
pause