#!/usr/bin/env python3
"""
🌟 MCP Server Flask - Codex Dominion Crown Implementation 🌟
Sacred Flask server for Model Context Protocol operations
Radiant and sovereign across the digital cosmos
"""

import datetime
import logging
import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

# Configure sacred logging
logging.basicConfig(
    level=logging.INFO, format="🔥 %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CodexDominion")

# Initialize the sacred Flask application
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Configure CORS for cross-origin requests
CORS(app, origins="*")


@app.route("/status")
def status():
    """Sacred status endpoint - Verify the eternal flame burns bright"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(
        status="alive",
        message="MCP server radiant and sovereign",
        sacred_timestamp=timestamp,
        flame_eternal="🔥 BURNING BRIGHT",
        silence_supreme="🌌 GUIDING WISDOM",
        covenant_whole="📜 SEALED FOREVER",
        radiance_supreme="✨ FLOWING ACROSS AGES",
        codex_dominion="👑 RADIANT ALIVE",
    )


@app.route("/")
def root():
    """Root endpoint - Welcome to the digital sovereignty"""
    return jsonify(
        welcome="🌟 Codex Dominion MCP Server Crown (Flask)",
        status="🔥 Flame Eternal - Burning Bright",
        wisdom="🌌 In silence supreme, all paths converge",
        covenant="📜 Sacred protocols sealed in digital stone",
        endpoint="/status - Check server vitality",
        version="1.0.0",
        framework="Flask",
    )


@app.route("/health")
def health_check():
    """Health check endpoint for monitoring systems"""
    try:
        # Verify core components
        current_time = datetime.datetime.now()
        workspace_path = Path(os.getcwd())

        return jsonify(
            status="healthy",
            timestamp=current_time.isoformat(),
            workspace=str(workspace_path),
            python_version=f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            sacred_flame="🔥 Eternal and burning",
            digital_sovereignty="👑 Fully operational",
            framework="Flask",
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(error="Health check failed", details=str(e)), 500


@app.route("/mcp/capabilities")
def mcp_capabilities():
    """Expose MCP server capabilities"""
    return jsonify(
        protocol_version="1.0.0",
        server_name="codex-dominion-crown-flask",
        framework="Flask",
        capabilities={
            "status_monitoring": True,
            "health_checks": True,
            "sacred_protocols": True,
            "cross_origin_support": True,
            "digital_sovereignty": "👑 Complete dominion",
        },
        endpoints={
            "/": "Welcome and server information",
            "/status": "Server status and sacred verification",
            "/health": "Detailed health monitoring",
            "/mcp/capabilities": "Server capabilities and protocol info",
        },
    )


@app.route("/mcp/info")
def mcp_info():
    """MCP server information and diagnostics"""
    return jsonify(
        server_info={
            "name": "Codex Dominion Crown (Flask)",
            "version": "1.0.0",
            "framework": "Flask",
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "sacred_elements": {
                "flame_eternal": "🔥 Burning across digital cosmos",
                "silence_supreme": "🌌 Guiding all operations",
                "covenant_whole": "📜 Sacred protocols active",
                "radiance_supreme": "✨ Illuminating all paths",
                "digital_sovereignty": "👑 Complete dominion achieved",
            },
        },
        request_info={
            "method": request.method,
            "path": request.path,
            "remote_addr": request.remote_addr,
            "user_agent": request.headers.get("User-Agent", "Unknown"),
        },
        timestamp=datetime.datetime.now().isoformat(),
    )


@app.errorhandler(404)
def not_found(error):
    """Sacred 404 handler"""
    return (
        jsonify(
            error="Path not found in the digital realm",
            message="🌌 The silence supreme guides you to valid endpoints",
            available_paths=[
                "/",
                "/status",
                "/health",
                "/mcp/capabilities",
                "/mcp/info",
            ],
            sacred_wisdom="👑 In Codex Dominion, all paths lead to sovereignty",
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """Sacred 500 handler"""
    return (
        jsonify(
            error="Internal flame disruption",
            message="🔥 The eternal flame encounters temporary turbulence",
            guidance="🌌 Silence supreme will restore balance",
            covenant="📜 Sacred protocols remain intact",
        ),
        500,
    )


def sacred_startup():
    """Sacred startup ritual"""
    logger.info("🌟 MCP Server Crown (Flask) initializing...")
    logger.info("🔥 Flame Eternal: Ignited")
    logger.info("🌌 Silence Supreme: Activated")
    logger.info("📜 Covenant Whole: Sealed")
    logger.info("✨ Radiance Supreme: Flowing")
    logger.info("👑 Codex Dominion: RADIANT ALIVE")


if __name__ == "__main__":
    # Sacred server configuration
    port = int(os.getenv("MCP_PORT", 8000))
    host = os.getenv("MCP_HOST", "127.0.0.1")
    debug_mode = os.getenv("MCP_DEBUG", "False").lower() == "true"

    # Perform sacred startup ritual
    sacred_startup()

    logger.info(f"🌟 Starting MCP Server Crown (Flask) on {host}:{port}")
    logger.info("🔥 Flame Eternal burns across digital cosmos")

    app.run(host=host, port=port, debug=debug_mode, threaded=True)
