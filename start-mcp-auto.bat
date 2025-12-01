@echo off
REM MCP Auto-Startup Launcher for Windows
REM Automatically starts MCP servers when chat messages are sent

echo.
echo ============================================
echo   Codex Dominion MCP Auto-Startup System
echo ============================================
echo.

echo [INFO] Initializing MCP Auto-Startup System...

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not available
    echo Please ensure npm is installed with Node.js
    pause
    exit /b 1
)

echo [INFO] Node.js and npm found
echo [INFO] Checking dependencies...

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo [INFO] Installing required dependencies...
    npm install @modelcontextprotocol/sdk express cors ws axios
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed successfully
)

REM Verify critical files exist
echo [INFO] Verifying system files...

if not exist "mcp-server-secure.js" (
    echo [ERROR] Missing mcp-server-secure.js
    echo Please ensure all MCP server files are present
    pause
    exit /b 1
)

if not exist "mcp-auto-startup.js" (
    echo [ERROR] Missing mcp-auto-startup.js
    echo Auto-startup system file not found
    pause
    exit /b 1
)

echo [SUCCESS] All required files verified

REM Create logs directory if it doesn't exist
if not exist "logs" (
    mkdir logs
    echo [INFO] Created logs directory
)

echo.
echo [INFO] Starting MCP Auto-Startup System...
echo [INFO] This system will automatically start MCP servers when chat activity is detected
echo [INFO] Press Ctrl+C to stop the system
echo.

REM Start the auto-startup system
node mcp-auto-startup.js

REM If we get here, the system has stopped
echo.
echo [INFO] MCP Auto-Startup System stopped
echo Press any key to exit...
pause >nul