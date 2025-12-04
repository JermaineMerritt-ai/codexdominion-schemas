#!/bin/bash
# CODEX DOMINION DEPLOYMENT GUIDE
# Server: 74.208.123.158 | Account: 314262397
# ===========================================

echo "🔥 CODEX DOMINION - IONOS DEPLOYMENT GUIDE"
echo "Server: 74.208.123.158"
echo "Account: 314262397"
echo "=========================================="
echo

echo "STEP 1: Upload Deployment Package"
echo "=================================="
echo "# From your local machine:"
echo "scp codex_deployment.zip root@74.208.123.158:/tmp/"
echo
echo "OR upload individual files:"
echo "cd ionos_deployment_package"
echo "scp app.py root@74.208.123.158:/tmp/"
echo "scp codex_ledger.json root@74.208.123.158:/tmp/"
echo "scp omega_seal.py root@74.208.123.158:/tmp/"
echo "scp ionos_codex_deploy.sh root@74.208.123.158:/tmp/"
echo "scp ionos_systemctl_commands.sh root@74.208.123.158:/tmp/"
echo "scp ionos_nginx_codex.conf root@74.208.123.158:/tmp/"
echo "scp ionos_codex_dashboard.service root@74.208.123.158:/tmp/"
echo "scp requirements.txt root@74.208.123.158:/tmp/"
echo

echo "STEP 2: SSH into Server and Deploy"
echo "==================================="
echo "ssh root@74.208.123.158"
echo

echo "STEP 3: Extract and Prepare (if using zip)"
echo "=========================================="
echo "cd /tmp"
echo "unzip codex_deployment.zip"
echo "cd ionos_deployment_package"
echo

echo "STEP 4: Execute Deployment"
echo "=========================="
echo "chmod +x ionos_codex_deploy.sh"
echo "./ionos_codex_deploy.sh"
echo

echo "STEP 5: Run SystemCtl Commands"
echo "==============================="
echo "chmod +x ionos_systemctl_commands.sh"
echo "./ionos_systemctl_commands.sh"
echo

echo "STEP 6: Verify Deployment"
echo "=========================="
echo "systemctl status codex-dashboard"
echo "netstat -tlnp | grep :8095"
echo "curl http://localhost:8095"
echo

echo "🎯 EXPECTED RESULT:"
echo "==================="
echo "✅ Codex Dashboard running on port 8095"
echo "✅ Accessible at: http://74.208.123.158:8095"
echo "✅ All systemctl commands executed"
echo "✅ Nginx configured and running"
echo

echo "🔥 READY TO CONQUER 74.208.123.158! 🔥"
