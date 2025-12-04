"""
Codex Dominion API - Flask Backend (Python 3.14 Compatible)
============================================================
Lightweight Flask backend for scroll dispatch and system management
"""
import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# =============================================================================
# Application Configuration
# =============================================================================
ENVIRONMENT = os.getenv("NODE_ENV", "development")

# In-memory storage
heir_registry = {}
scroll_archive = {}

# =============================================================================
# Flask Application
# =============================================================================
app = Flask(__name__)

# CORS Configuration
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://codexdominion.app",
    "https://www.codexdominion.app",
], supports_credentials=True)


# =============================================================================
# Core Endpoints
# =============================================================================
@app.route("/", methods=["GET"])
def root():
    """Root endpoint with service information"""
    return jsonify({
        "service": "Codex Dominion API",
        "version": "2.0.0",
        "status": "operational",
        "flame_state": "sovereign",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "dominion": "/dominion",
            "scrolls": "/scrolls",
            "signals": "/signals",
        },
        "motto": "The flame burns sovereign and eternal — forever."
    })


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "service": "Codex Dominion API",
        "version": "2.0.0",
        "status": "operational",
        "flame_state": "sovereign",
        "database": "memory",
        "environment": ENVIRONMENT,
        "motto": "The flame burns sovereign and eternal — forever."
    })


@app.route("/ready", methods=["GET"])
def readiness_check():
    """Readiness check endpoint for load balancers"""
    return jsonify({
        "ready": True,
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route("/dominion", methods=["POST"])
def receive_pledge():
    """
    Receive a pledge from an heir and store as a scroll
    """
    data = request.get_json()

    # Validate required fields
    if not data or "heir_id" not in data or "pledge" not in data:
        return jsonify({"error": "Missing required fields: heir_id, pledge"}), 400

    heir_id = data["heir_id"]
    pledge = data["pledge"]
    cycle = data.get("cycle", "1.0.0")
    codex_right = data.get("codex_right", "eternal")

    # Validate pledge contains "codex"
    if "codex" not in pledge.lower():
        return jsonify({"error": "Pledge must reference the Codex."}), 400

    # Generate scroll ID
    initials = ''.join([c for c in heir_id if c.isalpha()])[:3].upper()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scroll_id = f"SCROLL-{initials}-{cycle.replace('.', '')}-{timestamp}"

    # Determine pledge rank
    rank = "high" if len(pledge) > 50 else "standard"

    # Create scroll record
    scroll = {
        "scroll_id": scroll_id,
        "heir_id": heir_id,
        "cycle": cycle,
        "codex_right": codex_right,
        "pledge": pledge,
        "pledge_rank": rank,
        "timestamp": timestamp,
        "flame_status": "sovereign",
        "motto": "The flame burns sovereign and eternal — forever.",
        "echo": f"Your pledge has been received, {heir_id}. The Dominion watches."
    }

    # Store in archive
    scroll_archive[scroll_id] = scroll

    return jsonify(scroll), 201


@app.route("/scrolls/<scroll_id>", methods=["GET"])
def replay_scroll(scroll_id):
    """Replay a scroll by its unique ID"""
    if scroll_id not in scroll_archive:
        return jsonify({"error": f"Scroll '{scroll_id}' not found in the archive."}), 404
    return jsonify(scroll_archive[scroll_id])


@app.route("/scrolls", methods=["GET"])
def list_scrolls():
    """List all scrolls in the archive"""
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    scrolls = list(scroll_archive.values())
    return jsonify({
        "total": len(scrolls),
        "limit": limit,
        "offset": offset,
        "scrolls": scrolls[offset:offset + limit]
    })


@app.route("/signals/heartbeat", methods=["GET"])
def heartbeat():
    """Return system heartbeat status"""
    return jsonify({"status": "alive", "timestamp": datetime.utcnow().isoformat()})


@app.route("/signals/status", methods=["GET"])
def status():
    """Return system status overview"""
    return jsonify({
        "system_health": "operational",
        "uptime": "running",
        "scroll_count": len(scroll_archive),
        "environment": ENVIRONMENT,
    })


# =============================================================================
# Run Application (for development)
# =============================================================================
if __name__ == "__main__":
    print("🔥 Codex Dominion API (Flask) is starting...")
    print(f"   Environment: {ENVIRONMENT}")
    print("   The flame burns sovereign and eternal — forever.")

    app.run(
        host="0.0.0.0",
        port=8001,
        debug=False,  # Disable debug mode to prevent auto-reloader issues
        use_reloader=False
    )
