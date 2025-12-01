@echo off
REM Codex Dominion Production Startup Script for Windows

echo Starting Codex Dominion Production Environment...

REM Check for .env file
if not exist .env (
    echo ERROR: .env file not found
    exit /b 1
)

echo Environment variables loaded from .env

REM Start backend (Streamlit)
echo Starting Streamlit backend on port 8501...
start "Codex Backend" cmd /c "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start frontend (Next.js)
echo Starting Next.js frontend on port 3001...
cd frontend
start "Codex Frontend" cmd /c "npm run build && npm start"
cd ..

REM Wait for services to start
timeout /t 10 /nobreak >nul

echo.
echo Codex Dominion is starting up...
echo Backend: http://localhost:8501  
echo Frontend: http://localhost:3001
echo.
echo Press any key to stop services...
pause >nul

REM Stop services (this is basic - production would use proper process management)
taskkill /f /im python.exe /fi "WINDOWTITLE eq Codex Backend*" 2>nul
taskkill /f /im node.exe /fi "WINDOWTITLE eq Codex Frontend*" 2>nul

echo Services stopped.