#!/bin/bash
# Set Environment Variables for Investment App
# Run this script: source setup-env.sh

echo "Setting up Investment App environment variables..."

# Flask Configuration
export SECRET_KEY="dev-secret-key-CHANGE-IN-PRODUCTION"
export FLASK_DEBUG="True"
export DATABASE_URL="postgresql://pgadmin:Jer47@localhost:5432/codex"

# AI Provider Configuration
export AI_PROVIDER="openai"  # Change to "anthropic" if using Claude
export AI_MODEL="gpt-4o-mini"  # Fast and cheap for development
# export AI_MODEL="gpt-4"  # Uncomment for production quality

# OpenAI API Key (get from https://platform.openai.com/api-keys)
export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"  # REPLACE WITH YOUR KEY

# Anthropic API Key (optional, get from https://console.anthropic.com/)
# export ANTHROPIC_API_KEY="sk-ant-YOUR-KEY-HERE"

# Stock Data API (optional - defaults to database)
export STOCK_API_PROVIDER="database"  # Use "polygon" or "alphavantage" for real-time data
# export STOCK_API_KEY="YOUR-STOCK-API-KEY"

# Email Configuration (optional - for newsletters)
# export MAIL_SERVER="smtp.gmail.com"
# export MAIL_PORT="587"
# export MAIL_USERNAME="your-email@gmail.com"
# export MAIL_PASSWORD="your-app-password"

echo ""
echo "Environment variables set for current session!"
echo ""
echo "IMPORTANT: Update OPENAI_API_KEY with your actual key!"
echo ""
echo "To make permanent, add to ~/.bashrc or ~/.zshrc"
echo "Or create .env file (copy from .env.example)"
echo ""
echo "Check AI status: http://localhost:5000/health"
echo ""
