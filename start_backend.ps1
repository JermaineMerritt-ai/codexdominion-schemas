# Start Codex Dominion Backend API Server
# This script starts the FastAPI backend on http://127.0.0.1:8001

Write-Host "🔥 Starting Codex Dominion Backend API..." -ForegroundColor Cyan

# Set working directory
Set-Location $PSScriptRoot

# Set Python path
$env:PYTHONPATH = $PSScriptRoot

# Start uvicorn server
& "$PSScriptRoot\.venv\Scripts\python.exe" -m uvicorn src.backend.main:app --host 127.0.0.1 --port 8001 --reload

Write-Host "✅ Backend API server started on http://127.0.0.1:8001" -ForegroundColor Green
Write-Host "📖 API Documentation: http://127.0.0.1:8001/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
