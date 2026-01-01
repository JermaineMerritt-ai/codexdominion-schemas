"""
🔥 CREATIVE AGENTS - QUICK DEMO 🔥
===================================
A simple Flask server to showcase the Genesis Protocol creative agents
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from db import SessionLocal
from models import Agent
from creative_agents_template import CREATIVE_AGENTS_HTML

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Main page with Creative Agents"""
    return render_template_string(CREATIVE_AGENTS_HTML)

@app.route('/api/agents/creative')
def api_creative_agents():
    """Get all creative agents from Genesis Protocol"""
    session = SessionLocal()
    try:
        # Query creative agents (Generation 1)
        creative_agents = session.query(Agent).filter(
            Agent.id.like("agent_%")
        ).order_by(Agent.created_at).all()
        
        agents_data = [agent.to_dict() for agent in creative_agents]
        
        return jsonify({
            "agents": agents_data,
            "count": len(agents_data),
            "generation": 1,
            "status": "active"
        })
    except Exception as e:
        return jsonify({"error": str(e), "agents": [], "count": 0}), 500
    finally:
        session.close()

if __name__ == '__main__':
    print("🔥 CREATIVE AGENTS DASHBOARD")
    print("=" * 70)
    print("Starting server on http://localhost:5555")
    print("=" * 70)
    app.run(debug=True, port=5555, host='0.0.0.0')
