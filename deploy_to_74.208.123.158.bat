@echo off
REM CODEX DOMINION DEPLOYMENT - 74.208.123.158
REM Account: 314262397

echo.
echo 🔥 CODEX DOMINION - IONOS DEPLOYMENT
echo Server: 74.208.123.158
echo Account: 314262397
echo =======================================

set "SERVER=74.208.123.158"
set "USER=root"

echo.
echo 📋 DEPLOYMENT OPTIONS FOR YOUR IONOS SERVER:
echo.

echo OPTION 1: Test SSH Connection First
echo ===================================
echo ssh %USER%@%SERVER%
echo.

echo OPTION 2: Upload Individual Files
echo =================================
echo cd ionos_deployment_package
echo scp app.py %USER%@%SERVER%:/tmp/
echo scp codex_ledger.json %USER%@%SERVER%:/tmp/
echo scp omega_seal.py %USER%@%SERVER%:/tmp/
echo scp ionos_codex_deploy.sh %USER%@%SERVER%:/tmp/
echo scp ionos_systemctl_commands.sh %USER%@%SERVER%:/tmp/
echo scp ionos_nginx_codex.conf %USER%@%SERVER%:/tmp/
echo scp ionos_codex_dashboard.service %USER%@%SERVER%:/tmp/
echo scp requirements.txt %USER%@%SERVER%:/tmp/
echo.

echo OPTION 3: Archive Upload (Recommended)
echo =======================================
echo tar -czf codex_deployment.tar.gz ionos_deployment_package/
echo scp codex_deployment.tar.gz %USER%@%SERVER%:/tmp/
echo.

echo 🚀 AFTER UPLOAD - SSH COMMANDS:
echo ===============================
echo ssh %USER%@%SERVER%
echo cd /tmp
echo.
echo # If using archive:
echo tar -xzf codex_deployment.tar.gz
echo cd ionos_deployment_package
echo.
echo # Execute deployment:
echo chmod +x ionos_codex_deploy.sh
echo ./ionos_codex_deploy.sh
echo.
echo # Run your systemctl commands:
echo chmod +x ionos_systemctl_commands.sh
echo ./ionos_systemctl_commands.sh
echo.

echo 🎯 EXPECTED RESULT:
echo ===================
echo ✅ Codex Dashboard running on port 8095
echo ✅ Accessible at: http://74.208.123.158:8095
echo ✅ All systemctl commands executed
echo ✅ Nginx configured and running
echo.

echo 🔥 READY TO CONQUER 74.208.123.158! 🔥
echo.

pause