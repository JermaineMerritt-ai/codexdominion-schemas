@echo off
REM MCP Server Startup Script for Windows
REM Starts the MCP server with monitoring for production use

echo.
echo ========================================
echo   Codex Dominion MCP Server Startup
echo ========================================
echo.

echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [INFO] Node.js found
echo [INFO] Checking dependencies...

if not exist "node_modules" (
    echo [INFO] Installing dependencies...
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies ready
echo [INFO] Starting MCP Server with monitoring...
echo.

REM Start the MCP server monitor
node mcp-monitor.js

echo.
echo [INFO] MCP Server stopped
pause
