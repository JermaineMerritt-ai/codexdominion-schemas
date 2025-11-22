@echo off
REM Windows simulation of: sudo nginx -t && sudo systemctl reload nginx

echo.
echo 🔥 NGINX TEST AND RELOAD SIMULATION
echo ==================================
echo Command: sudo nginx -t ^&^& sudo systemctl reload nginx
echo.

echo 📋 Step 1: Testing nginx configuration...
echo nginx: the configuration file syntax is ok
echo nginx: configuration file test is successful
echo.

echo 📋 Step 2: Reloading nginx service...
echo Reloading nginx configuration...
timeout /t 1 /nobreak > nul
echo nginx: signal process started
echo.

echo ✅ SUCCESS: Configuration test and reload completed!
echo.

echo 📊 Current Status:
REM Check if any web servers are running on common ports
netstat -an | findstr ":80 " > nul 2>&1
if %errorlevel%==0 (
    echo    Port 80: LISTENING
) else (
    echo    Port 80: Available
)

netstat -an | findstr ":443 " > nul 2>&1  
if %errorlevel%==0 (
    echo    Port 443: LISTENING
) else (
    echo    Port 443: Available
)

netstat -an | findstr ":8095 " > nul 2>&1
if %errorlevel%==0 (
    echo    Port 8095: LISTENING ^(Codex Dashboard^)
) else (
    echo    Port 8095: Available
)

echo.
echo 🌐 For IONOS Linux production:
echo    sudo nginx -t ^&^& sudo systemctl reload nginx
echo.
echo 🔥 Nginx management complete!

pause