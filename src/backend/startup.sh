#!/bin/bash
# Azure App Service startup script for FastAPI backend

echo "🚀 Starting Codex Dominion Backend on Azure App Service..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if using Alembic)
if [ -f "alembic.ini" ]; then
    echo "📊 Running database migrations..."
    alembic upgrade head
fi

# Start Uvicorn with production settings
echo "🔥 Starting Uvicorn server..."
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    --access-log \
    --use-colors
