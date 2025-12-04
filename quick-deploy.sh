#!/bin/bash
# =============================================================================
# Quick Deployment Setup for Codex Dominion
# =============================================================================
# This script sets up your environment variables and runs the deployment
# =============================================================================

echo "🔥 CODEX DOMINION - DEPLOYMENT SETUP 🔥"
echo "========================================"
echo ""

# Prompt for server details
read -p "Enter IONOS Server IP Address: " SERVER_IP
read -p "Enter IONOS Username: " USERNAME
read -p "Enter SSH Key Path (press Enter for default ~/.ssh/id_rsa): " SSH_KEY_PATH

# Set defaults
SSH_KEY_PATH=${SSH_KEY_PATH:-$HOME/.ssh/id_rsa}

# Export environment variables
export IONOS_SERVER="$SERVER_IP"
export IONOS_USER="$USERNAME"
export SSH_KEY="$SSH_KEY_PATH"

echo ""
echo "Configuration Set:"
echo "  IONOS_SERVER: $IONOS_SERVER"
echo "  IONOS_USER: $IONOS_USER"
echo "  SSH_KEY: $SSH_KEY"
echo ""

# Test SSH connection
echo "Testing SSH connection..."
if ssh -i "$SSH_KEY" -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$IONOS_USER@$IONOS_SERVER" "echo 'Connection successful'" 2>/dev/null; then
    echo "✓ SSH connection successful!"
    echo ""
    read -p "Ready to deploy? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Starting deployment..."
        bash deploy-ionos.sh
    else
        echo "Deployment cancelled."
    fi
else
    echo "✗ SSH connection failed!"
    echo ""
    echo "Please check:"
    echo "  1. Server IP is correct"
    echo "  2. Username is correct"
    echo "  3. SSH key has correct permissions: chmod 600 $SSH_KEY"
    echo "  4. SSH key is added to server: ssh-copy-id -i $SSH_KEY $IONOS_USER@$IONOS_SERVER"
    echo ""
    echo "You can still run deployment with:"
    echo "  export IONOS_SERVER='$SERVER_IP'"
    echo "  export IONOS_USER='$USERNAME'"
    echo "  export SSH_KEY='$SSH_KEY_PATH'"
    echo "  bash deploy-ionos.sh"
fi
