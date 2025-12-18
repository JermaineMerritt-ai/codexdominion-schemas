# Set Environment Variables for Investment App
# Run this script: .\setup-env.ps1

Write-Host "Setting up Investment App environment variables..." -ForegroundColor Green

# Flask Configuration
$env:SECRET_KEY = "dev-secret-key-CHANGE-IN-PRODUCTION"
$env:FLASK_DEBUG = "True"
$env:DATABASE_URL = "postgresql://pgadmin:Jer47@localhost:5432/codex"

# AI Provider Configuration
$env:AI_PROVIDER = "openai"  # Change to "anthropic" if using Claude
$env:AI_MODEL = "gpt-4o-mini"  # Fast and cheap for development
# $env:AI_MODEL = "gpt-4"  # Uncomment for production quality

# OpenAI API Key (get from https://platform.openai.com/api-keys)
$env:OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"  # REPLACE WITH YOUR KEY

# Anthropic API Key (optional, get from https://console.anthropic.com/)
# $env:ANTHROPIC_API_KEY = "sk-ant-YOUR-KEY-HERE"

# Stock Data API (optional - defaults to database)
$env:STOCK_API_PROVIDER = "database"  # Use "polygon" or "alphavantage" for real-time data
# $env:STOCK_API_KEY = "YOUR-STOCK-API-KEY"

# Email Configuration (optional - for newsletters)
# $env:MAIL_SERVER = "smtp.gmail.com"
# $env:MAIL_PORT = "587"
# $env:MAIL_USERNAME = "your-email@gmail.com"
# $env:MAIL_PASSWORD = "your-app-password"

Write-Host ""
Write-Host "Environment variables set for current session!" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Update OPENAI_API_KEY with your actual key!" -ForegroundColor Yellow
Write-Host ""
Write-Host "To make permanent, add to:" -ForegroundColor Cyan
Write-Host "  1. System Environment Variables (Windows Settings)" -ForegroundColor Cyan
Write-Host "  2. Or create .env file (copy from .env.example)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check AI status: http://localhost:5000/health" -ForegroundColor Cyan
Write-Host ""
