#!/bin/bash
# Combined Local UFW + IONOS Cloud Firewall Configuration
# Configures both VPS firewall (UFW) and IONOS Cloud firewall

# --- Local VPS Firewall (UFW) ---
echo "========================================"
echo "🔥 Configuring UFW on VPS..."
echo "========================================"
sudo ufw allow 22/tcp   # SSH - CRITICAL, don't lock yourself out!
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 3000/tcp # Next.js
sudo ufw allow 8001/tcp # Backend API
sudo ufw allow 8080/tcp # Alt Backend
sudo ufw --force enable
sudo ufw reload
echo "✅ UFW rules applied."
echo ""

# --- IONOS Cloud Firewall ---
# Replace these with your IONOS credentials and IDs
IONOS_USER="${IONOS_USERNAME:-YOUR_IONOS_USERNAME}"
IONOS_PASS="${IONOS_PASSWORD:-YOUR_IONOS_PASSWORD}"
DATACENTER_ID="${IONOS_DATACENTER_ID:-7b3fa8e1-d7d7-4646-8005-9f59a8a004fe}"
SERVER_ID="${IONOS_SERVER_ID:-YOUR_SERVER_ID}"
NIC_ID="${IONOS_NIC_ID:-YOUR_NIC_ID}"

# Base API endpoint
API="https://api.ionos.com/cloudapi/v6"

# Function to add a firewall rule
add_rule() {
  local NAME=$1
  local PORT=$2

  echo "Adding rule: $NAME (Port $PORT)..."

  curl -X POST "$API/datacenters/$DATACENTER_ID/servers/$SERVER_ID/nics/$NIC_ID/firewallrules" \
    -u "$IONOS_USER:$IONOS_PASS" \
    -H "Content-Type: application/json" \
    -d "{
      \"properties\": {
        \"name\": \"$NAME\",
        \"protocol\": \"TCP\",
        \"sourceIp\": \"0.0.0.0/0\",
        \"portRangeStart\": $PORT,
        \"portRangeEnd\": $PORT,
        \"action\": \"ALLOW\"
      }
    }"

  echo ""
}

echo "========================================"
echo "☁️  Configuring IONOS Cloud Firewall..."
echo "========================================"
echo ""

# Add comprehensive rules for all required services
add_rule "Allow-HTTP" 80
add_rule "Allow-HTTPS" 443
add_rule "Allow-SSH" 22
add_rule "Allow-Next-Dev" 3000
add_rule "Allow-Backend-API" 8001
add_rule "Allow-Backend-Alt" 8080

echo ""
echo "✅ Firewall rules applied successfully!"
echo "⏳ Please wait 1–5 minutes for propagation."
echo ""
echo "To verify, run:"
echo "  curl http://74.208.123.158"
echo "  curl https://74.208.123.158"
