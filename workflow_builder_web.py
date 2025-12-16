"""
Codex Dominion - Workflow Builder Web UI
Direct launcher for web interface on port 5557
"""

from workflow_builder import app, print_header

if __name__ == "__main__":
    print_header("🔷 CODEX DOMINION - WORKFLOW BUILDER WEB UI")
    print("🚀 Starting server...")
    print("📍 URL: http://localhost:5557")
    print("Press Ctrl+C to stop\n")

    try:
        app.run(host='0.0.0.0', port=5557, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Workflow Builder stopped!")
