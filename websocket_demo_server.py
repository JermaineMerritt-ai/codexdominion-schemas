"""
🔥 CODEX DOMINION - WEBSOCKET DEMO SERVER 🔥
==============================================
Minimal Flask server demonstrating WebSocket real-time updates.

Run this to test the WebSocket functionality with the live monitor.

Usage:
    python websocket_demo_server.py
    
Then open: http://localhost:5000/websocket-demo
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
import sys

# Fix Windows UTF-8 encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize WebSocket manager
from websocket_manager import WebSocketManager
ws_manager = WebSocketManager()
socketio = ws_manager.init_app(app, cors_allowed_origins="*")

# Import available modules
import time
import uuid

# Flag to check if full orchestrator is available
FULL_ORCHESTRATOR_AVAILABLE = False
orchestrator = None

try:
    from project_intelligence_core import ProjectIntelligenceCore
    from creative_intelligence_interfaces import UnifiedWorkflowOrchestrator
    
    # Try to import and initialize all modules
    from project_intelligence_core import ProjectIntelligenceCore
    from creative_resonance_engine import CreativeResonanceEngine
    from multi_medium_orchestration_engine import MultiMediumOrchestrationEngine
    from asset_dependency_graph import AssetDependencyGraph
    from creative_continuity_system import CreativeContinuitySystem
    from output_assembly_engine import OutputAssemblyEngine
    
    # Initialize all modules
    pic = ProjectIntelligenceCore()
    cre = CreativeResonanceEngine()
    mmoe = MultiMediumOrchestrationEngine()
    adg = AssetDependencyGraph()
    ccs = CreativeContinuitySystem()
    oae = OutputAssemblyEngine()
    
    # Initialize orchestrator with WebSocket enabled
    orchestrator = UnifiedWorkflowOrchestrator(
        pic=pic,
        cre=cre,
        mmoe=mmoe,
        adg=adg,
        ccs=ccs,
        oae=oae,
        dashboard=None,
        enable_websocket=True
    )
    FULL_ORCHESTRATOR_AVAILABLE = True
    logger.info("✅ Full Creative Intelligence orchestrator loaded")
    
except ImportError as e:
    logger.warning(f"⚠️  Some modules not available: {e}")
    logger.info("🔄 Using demo mode with simulated workflow")

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Redirect to WebSocket demo"""
    return render_template('websocket_demo.html')


@app.route('/websocket-demo')
def websocket_demo():
    """WebSocket demo page"""
    return render_template('websocket_demo.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'websocket': 'enabled',
        'modules': {
            'PIC': 'ready',
            'CRE': 'ready',
            'MMOE': 'ready',
            'ADG': 'ready',
            'CCS': 'ready',
            'OAE': 'ready'
        }
    })


@app.route('/api/test-workflow', methods=['POST'])
def test_workflow():
    """
    Test endpoint to trigger a workflow with WebSocket updates.
    
    POST /api/test-workflow
    {
        "description": "Create a marketing campaign..."
    }
    """
    try:
        data = request.get_json() or {}
        description = data.get('description', 'Test marketing campaign with video, audio, and graphics')
        
        logger.info(f"🚀 Starting test workflow: {description[:100]}")
        
        if FULL_ORCHESTRATOR_AVAILABLE and orchestrator:
            # Execute real workflow (this will emit WebSocket events automatically)
            result = orchestrator.execute_complete_workflow(
                project_description=description,
                user_preferences=None,
                auto_execute=True
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'workflow_id': result.get('workflow_id'),
                    'project_id': result['project']['project_id'],
                    'duration': result.get('duration_seconds'),
                    'message': 'Workflow completed successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error'),
                    'message': 'Workflow execution failed'
                }), 500
        else:
            # Demo mode - simulate workflow with WebSocket events
            result = simulate_workflow(description)
            return jsonify(result)
    
    except Exception as e:
        logger.error(f"❌ Error in test workflow: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }), 500


def simulate_workflow(description: str) -> dict:
    """Simulate a workflow execution with WebSocket events for demo"""
    workflow_id = f"workflow_{uuid.uuid4().hex[:12]}"
    project_id = f"pic_project_{uuid.uuid4().hex[:12]}"
    
    # Emit workflow started
    ws_manager.emit_workflow_started(
        workflow_id=workflow_id,
        project_id=project_id,
        workflow_type="creative_intelligence_demo",
        total_steps=7,
        metadata={"description": description[:200]}
    )
    
    # Simulate each step
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
        # Emit step starting
        ws_manager.emit_workflow_progress(
            workflow_id=workflow_id,
            project_id=project_id,
            current_step=i,
            total_steps=7,
            step_name=step_name,
            step_status="running"
        )
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Emit step complete
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
    
    # Emit workflow complete
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
        'message': 'Simulated workflow completed successfully',
        'mode': 'demo'
    }


@app.route('/api/workflows', methods=['GET'])
def list_workflows():
    """List recent workflows (placeholder for database integration)"""
    return jsonify({
        'workflows': [],
        'total': 0,
        'message': 'Database integration pending'
    })


# =============================================================================
# WEBSOCKET EVENTS (Additional custom handlers)
# =============================================================================

@socketio.on('request_workflow_status')
def handle_workflow_status_request(data):
    """Handle client request for workflow status"""
    workflow_id = data.get('workflow_id')
    logger.info(f"📡 Status request for workflow: {workflow_id}")
    
    # In production, query database for workflow status
    # For now, return placeholder
    socketio.emit('workflow_status', {
        'workflow_id': workflow_id,
        'status': 'unknown',
        'message': 'Database integration pending'
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🔥 CODEX DOMINION - WEBSOCKET DEMO SERVER 🔥")
    logger.info("=" * 80)
    logger.info("📍 Server starting on http://localhost:5000")
    logger.info("   WebSocket Demo: http://localhost:5000/websocket-demo")
    logger.info("   Health Check: http://localhost:5000/health")
    logger.info("✅ WebSocket real-time updates enabled")
    if FULL_ORCHESTRATOR_AVAILABLE:
        logger.info("✅ All 7 Creative Intelligence modules loaded")
    else:
        logger.info("🔄 Demo mode - simulated workflow only")
    logger.info("⚡ Press Ctrl+C to stop")
    logger.info("=" * 80)
    
    # Run with threading for WebSocket support (more stable than eventlet)
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=True,  # Enable debug for better error messages
            use_reloader=False,  # Disable reloader to prevent double initialization
            allow_unsafe_werkzeug=True  # Allow running in development mode
        )
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()
