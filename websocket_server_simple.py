"""
Simplified WebSocket Demo Server - Avoids Windows UTF-8 Issues
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import uuid

# Initialize Flask
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Import WebSocket manager
from websocket_manager import WebSocketManager
ws_manager = WebSocketManager()
socketio = ws_manager.init_app(app, cors_allowed_origins="*")

# Try to load full orchestrator (graceful degradation if unavailable)
FULL_ORCHESTRATOR_AVAILABLE = False
orchestrator = None

try:
    from project_intelligence_core import ProjectIntelligenceCore
    from creative_intelligence_interfaces import UnifiedWorkflowOrchestrator
    # ... other imports would go here ...
    FULL_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    pass

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    return {'status': 'ok', 'message': 'WebSocket Demo Server Running', 'demo_url': '/websocket-demo'}

@app.route('/websocket-demo')
def websocket_demo():
    """Serve the WebSocket monitoring dashboard"""
    with open('templates/websocket_demo.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'websocket': 'enabled',
        'full_orchestrator': FULL_ORCHESTRATOR_AVAILABLE,
        'mode': 'production' if FULL_ORCHESTRATOR_AVAILABLE else 'demo'
    })

@app.route('/api/test-workflow', methods=['POST'])
def test_workflow():
    """Test endpoint to trigger a workflow"""
    try:
        data = request.get_json() or {}
        description = data.get('description', 'Test workflow')
        
        if FULL_ORCHESTRATOR_AVAILABLE and orchestrator:
            result = orchestrator.execute_complete_workflow(
                project_description=description,
                user_preferences=None,
                auto_execute=True
            )
            return jsonify(result)
        else:
            # Demo mode - simulate workflow
            result = simulate_workflow(description)
            return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def simulate_workflow(description: str) -> dict:
    """Simulate workflow with WebSocket events"""
    workflow_id = f"workflow_{uuid.uuid4().hex[:12]}"
    project_id = f"project_{uuid.uuid4().hex[:12]}"
    
    # Start workflow
    ws_manager.emit_workflow_started(
        workflow_id=workflow_id,
        project_id=project_id,
        workflow_type="creative_intelligence_demo",
        total_steps=7,
        metadata={"description": description[:200]}
    )
    
    # Simulate 7 steps
    steps = [
        ("PIC", "Project Intelligence Core"),
        ("CRE", "Creative Resonance Engine"),
        ("MMOE", "Multi-Medium Orchestration"),
        ("ADG", "Asset Dependency Graph"),
        ("CCS", "Creative Continuity System"),
        ("OAE", "Output Assembly Engine"),
        ("DASHBOARD", "Dashboard Generation")
    ]
    
    start_time = time.time()
    
    for i, (step_name, step_desc) in enumerate(steps, 1):
        # Step running
        ws_manager.emit_workflow_progress(
            workflow_id=workflow_id,
            project_id=project_id,
            current_step=i,
            total_steps=7,
            step_name=step_name,
            step_status="running"
        )
        
        time.sleep(0.5)  # Simulate processing
        
        # Step complete
        ws_manager.emit_workflow_progress(
            workflow_id=workflow_id,
            project_id=project_id,
            current_step=i,
            total_steps=7,
            step_name=step_name,
            step_status="complete",
            step_result={"step": step_desc, "simulated": True}
        )
    
    duration = time.time() - start_time
    
    # Complete workflow
    ws_manager.emit_workflow_complete(
        workflow_id=workflow_id,
        project_id=project_id,
        status="complete",
        duration_seconds=duration,
        results={
            "project_id": project_id,
            "assets_created": 5,
            "deliverables_ready": 3,
            "continuity_score": 0.95,
            "simulated": True
        }
    )
    
    return {
        'success': True,
        'workflow_id': workflow_id,
        'project_id': project_id,
        'duration': duration,
        'message': 'Simulated workflow completed',
        'mode': 'demo'
    }

# =============================================================================
# WEBSOCKET HANDLERS
# =============================================================================

@socketio.on('request_workflow_status')
def handle_workflow_status_request(data):
    """Handle workflow status requests"""
    workflow_id = data.get('workflow_id')
    # In production, query database for workflow status
    socketio.emit('workflow_status_response', {
        'workflow_id': workflow_id,
        'status': 'running',
        'progress': 50
    })

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("  CODEX DOMINION - WEBSOCKET DEMO SERVER")
    print("=" * 80)
    print(f"\n  Server: http://localhost:5000")
    print(f"  Dashboard: http://localhost:5000/websocket-demo")
    print(f"  Health: http://localhost:5000/health")
    print(f"\n  Mode: {'FULL' if FULL_ORCHESTRATOR_AVAILABLE else 'DEMO'}")
    print(f"  WebSocket: ENABLED")
    print(f"\n  Press Ctrl+C to stop\n")
    print("=" * 80 + "\n")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
        log_output=False  # Disable Flask's output to avoid UTF-8 issues
    )
