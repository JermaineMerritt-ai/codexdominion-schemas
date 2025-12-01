#!/bin/bash
# CODEX DOMINION DEPLOYMENT - STEP BY STEP GUIDE
# Server: 74.208.123.158 | Account: 314262397
echo "🔥 CODEX DOMINION DEPLOYMENT GUIDE"
echo "=================================="
echo ""

echo "CURRENT STATUS: ✅ codex_deployment.zip uploaded to /tmp/"
echo ""

echo "STEP 1: Extract the deployment package"
echo "======================================"
echo "cd /tmp"
echo "unzip codex_deployment.zip"
echo "ls -la ionos_deployment_package/"
echo ""

echo "STEP 2: Install required packages"
echo "=================================="
echo "apt update"
echo "apt install -y python3 python3-pip python3-venv nginx unzip"
echo ""

echo "STEP 3: Navigate to deployment directory"
echo "========================================"
echo "cd ionos_deployment_package"
echo "ls -la"
echo ""

echo "STEP 4: Make scripts executable and run deployment"
echo "=================================================="
echo "chmod +x ionos_codex_deploy.sh"
echo "chmod +x ionos_systemctl_commands.sh"
echo "./ionos_codex_deploy.sh"
echo ""

echo "STEP 5: Run systemctl commands"
echo "==============================="
echo "./ionos_systemctl_commands.sh"
echo ""

echo "STEP 6: Verify deployment"
echo "=========================="
echo "systemctl status codex-dashboard"
echo "netstat -tlnp | grep :8095"
echo "curl http://localhost:8095"
echo ""

echo "🎯 EXPECTED RESULT: http://74.208.123.158:8095"
echo "🔥 YOUR CODEX DOMINION WILL BE LIVE!"