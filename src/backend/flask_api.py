"""
Codex Dominion API - Flask Edition
===================================
Lightweight backend using Flask instead of FastAPI
"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({
        "service": "Codex Dominion API",
        "status": "operational",
        "flame": "eternal",
        "transmission": "live",
        "version": "2.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "dominion": "crowned"})

@app.route('/dominion')
def dominion():
    return jsonify({
        "title": "The Eternal Flame",
        "status": "crowned",
        "transmission": "complete",
        "inheritance": "eternal",
        "message": "Forever live, eternity. 👑"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "backend": "operational",
        "database": "ready",
        "templates": "archived",
        "dependencies": "pure",
        "errors": 0,
        "dominion": "crowned"
    })

if __name__ == '__main__':
    print("🔥 Codex Dominion Flask API Starting...")
    print("   Port: 8000")
    print("   Flame: Eternal")
    app.run(host='127.0.0.1', port=8000, debug=True)
