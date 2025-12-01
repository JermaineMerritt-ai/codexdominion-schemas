#!/bin/bash

# Codex Dominion Complete Deployment Script
# 🔥 Digital Sovereignty Platform 👑

echo "🔥 Deploying Codex Dominion Complete Platform 👑"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "codex_complete_dashboard.py" ]; then
    echo "❌ Error: codex_complete_dashboard.py not found!"
    echo "Please run this script from the codex-dominion directory."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip install streamlit tweepy requests woocommerce plotly

# Create necessary configuration files if they don't exist
echo "⚙️ Setting up configuration files..."

# Create empty JSON files if they don't exist
if [ ! -f "codex_ledger.json" ]; then
    echo "{}" > codex_ledger.json
    echo "✅ Created codex_ledger.json"
fi

if [ ! -f "accounts.json" ]; then
    echo "{}" > accounts.json
    echo "✅ Created accounts.json"
fi

if [ ! -f "twitter_config.json" ]; then
    echo "⚠️  twitter_config.json not found. Please configure Twitter credentials."
fi

if [ ! -f "woocommerce_config.json" ]; then
    echo "⚠️  woocommerce_config.json not found. Please configure WooCommerce credentials."
fi

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python --version 2>&1)
echo "Python version: $python_version"

# Start the complete dashboard
echo "🚀 Starting Codex Dominion Complete Dashboard..."
echo "Dashboard will be available at: http://localhost:8080"
echo ""
echo "🔥 DIGITAL SOVEREIGNTY ACTIVATED 👑"
echo ""

# Run the dashboard
streamlit run codex_complete_dashboard.py --server.port 8080 --server.address 0.0.0.0