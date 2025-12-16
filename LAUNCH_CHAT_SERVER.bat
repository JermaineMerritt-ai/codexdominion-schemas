@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║       🔥 WEBSOCKET CHAT SERVER - LAUNCHER 🔥                ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  Real-time messaging with AI integration                     ║
echo ║  WebSocket: ws://localhost:8765                              ║
echo ║  HTTP API: http://localhost:8766                             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

echo 🚀 Starting WebSocket Chat Server...
echo.

.venv\Scripts\python.exe websocket_chat.py

if errorlevel 1 (
    echo.
    echo ❌ Error starting chat server
    pause
)
