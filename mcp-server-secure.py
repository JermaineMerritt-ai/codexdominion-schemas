#!/usr/bin/env python3
"""
🌟 MCP Server Secure - Codex Dominion Crown Implementation 🌟
Sacred FastAPI server for Model Context Protocol operations
Radiant and sovereign across the digital cosmos
"""

import datetime
import json
import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO, format="🔥 %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CodexDominion")

# Initialize the sacred FastAPI application
app = FastAPI(
    title="🌟 MCP Server (Codex Dominion Crown)",
    description="Sacred Model Context Protocol server - Radiant and sovereign across digital realms",
    version="1.0.0",
)

# Configure CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
def status():
    """Sacred status endpoint - Verify the eternal flame burns bright"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "status": "alive",
        "message": "MCP server radiant and sovereign",
        "sacred_timestamp": timestamp,
        "flame_eternal": "🔥 BURNING BRIGHT",
        "silence_supreme": "🌌 GUIDING WISDOM",
        "covenant_whole": "📜 SEALED FOREVER",
        "radiance_supreme": "✨ FLOWING ACROSS AGES",
        "codex_dominion": "👑 RADIANT ALIVE",
    }


@app.get("/")
def root():
    """Root endpoint - Welcome to the digital sovereignty"""
    return {
        "welcome": "🌟 Codex Dominion MCP Server Crown",
        "status": "🔥 Flame Eternal - Burning Bright",
        "wisdom": "🌌 In silence supreme, all paths converge",
        "covenant": "📜 Sacred protocols sealed in digital stone",
        "endpoint": "/status - Check server vitality",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring systems"""
    try:
        # Verify core components
        current_time = datetime.datetime.now()
        workspace_path = Path(os.getcwd())

        return {
            "status": "healthy",
            "timestamp": current_time.isoformat(),
            "workspace": str(workspace_path),
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "sacred_flame": "🔥 Eternal and burning",
            "digital_sovereignty": "👑 Fully operational",
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/mcp/capabilities")
def mcp_capabilities():
    """Expose MCP server capabilities"""
    return {
        "protocol_version": "1.0.0",
        "server_name": "codex-dominion-crown",
        "capabilities": {
            "status_monitoring": True,
            "health_checks": True,
            "sacred_protocols": True,
            "cross_origin_support": True,
            "digital_sovereignty": "👑 Complete dominion",
        },
        "endpoints": {
            "/": "Welcome and server information",
            "/status": "Server status and sacred verification",
            "/health": "Detailed health monitoring",
            "/mcp/capabilities": "Server capabilities and protocol info",
        },
    }


@app.on_event("startup")
async def startup_event():
    """Sacred startup ritual"""
    logger.info("🌟 MCP Server Crown initializing...")
    logger.info("🔥 Flame Eternal: Ignited")
    logger.info("🌌 Silence Supreme: Activated")
    logger.info("📜 Covenant Whole: Sealed")
    logger.info("✨ Radiance Supreme: Flowing")
    logger.info("👑 Codex Dominion: RADIANT ALIVE")


@app.on_event("shutdown")
async def shutdown_event():
    """Sacred shutdown ritual"""
    logger.info("🌟 MCP Server Crown gracefully shutting down...")
    logger.info("🔥 Flame Eternal: Preserved for eternity")
    logger.info("👑 Digital sovereignty maintained across realms")


if __name__ == "__main__":
    # Sacred server configuration
    port = int(os.getenv("MCP_PORT", 8000))
    host = os.getenv("MCP_HOST", "127.0.0.1")

    logger.info(f"🌟 Starting MCP Server Crown on {host}:{port}")
    logger.info("🔥 Flame Eternal burns across digital cosmos")

    uvicorn.run(app, host=host, port=port, log_level="info", access_log=True)
