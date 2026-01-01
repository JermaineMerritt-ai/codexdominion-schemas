"""
🔥 CREATIVE INTELLIGENCE ENGINE — FLASK DASHBOARD ROUTES 🔥

Add these routes to flask_dashboard.py to integrate the Creative Intelligence Engine.

Routes provided:
- /creative-engine - Main dashboard interface
- /api/creative/project/create - Create new project
- /api/creative/project/<id>/status - Get project status
- /api/creative/dashboard/<id> - Get complete dashboard view
"""

from flask import Blueprint, render_template_string, jsonify, request
from creative_intelligence_interfaces import get_unified_orchestrator

# Create blueprint
creative_engine_bp = Blueprint('creative_engine', __name__, url_prefix='/creative')

# Initialize unified orchestrator
unified_orchestrator = get_unified_orchestrator()

# ═══════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD ROUTE
# ═══════════════════════════════════════════════════════════════════════════

@creative_engine_bp.route('/')
@creative_engine_bp.route('/dashboard')
def main_dashboard():
    """Main Creative Intelligence Engine dashboard"""
    return render_template_string(DASHBOARD_HTML_TEMPLATE)

# ═══════════════════════════════════════════════════════════════════════════
# API ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@creative_engine_bp.route('/api/project/create', methods=['POST'])
def create_project():
    """
    Create a new creative project using unified workflow orchestrator
    
    POST /api/project/create
    {
        "description": "Create a youth entrepreneurship video course...",
        "auto_execute": false
    }
    """
    data = request.get_json()
    description = data.get('description', '')
    auto_execute = data.get('auto_execute', False)
    
    if not description:
        return jsonify({"error": "Description required"}), 400
    
    # Execute unified workflow
    result = unified_orchestrator.execute_complete_workflow(
        project_description=description,
        auto_execute=auto_execute
    )
    
    if result['success']:
        project = result['project']
        return jsonify({
            "success": True,
            "project_id": project['project_id'],
            "project_type": project['project_type'],
            "complexity": project['complexity'],
            "required_mediums": project['required_mediums'],
            "workflow_complete": True
        })
    else:
        return jsonify({
            "success": False,
            "error": result.get('error', 'Unknown error')
        }), 500

@creative_engine_bp.route('/api/project/<project_id>/status', methods=['GET'])
def project_status(project_id):
    """
    Get project status
    
    GET /api/project/<id>/status
    """
    # Get project from unified orchestrator's PIC
    project = unified_orchestrator.pic.get_project(project_id)
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    return jsonify({
        "project_id": project_id,
        "status": project.get('status', 'unknown'),
        "type": project.get('type'),
        "created_at": project.get('created_at')
    })

@creative_engine_bp.route('/api/dashboard/<project_id>', methods=['GET'])
def get_dashboard_data(project_id):
    """
    Get complete dashboard view for a project
    
    GET /api/dashboard/<id>
    
    Returns complete dashboard with all 6 panels populated
    """
    # Get project from unified orchestrator
    project = unified_orchestrator.pic.get_project(project_id)
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    # Execute complete workflow to generate dashboard
    # (In production, this would retrieve cached results)
    result = unified_orchestrator.execute_complete_workflow(
        project_description=project.get('brief', ''),
        auto_execute=False
    )
    
    if result['success']:
        return jsonify(result['dashboard'])
    else:
        return jsonify({"error": result.get('error')}), 500

@creative_engine_bp.route('/api/projects', methods=['GET'])
def list_projects():
    """
    List all projects
    
    GET /api/projects
    """
    projects = unified_orchestrator.pic.projects
    
    project_list = [
        {
            "id": pid,
            "type": p.get('type'),
            "created_at": p.get('created_at'),
            "status": p.get('status')
        }
        for pid, p in projects.items()
    ]
    
    return jsonify({"projects": project_list})

# ═══════════════════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════

DASHBOARD_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creative Intelligence Engine - Dominion Command Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #F8FAFC;
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
            background: rgba(245, 197, 66, 0.1);
            border: 2px solid #F5C542;
            border-radius: 12px;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #F5C542;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            color: #CBD5E1;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .input-section {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 40px;
        }
        
        .input-section h2 {
            color: #F5C542;
            margin-bottom: 20px;
        }
        
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #F8FAFC;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
        }
        
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }
        
        button {
            background: #F5C542;
            color: #0F172A;
            border: none;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #E5B532;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(245, 197, 66, 0.3);
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 25px;
        }
        
        .panel h3 {
            color: #F5C542;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .status-complete { background: #10B981; color: white; }
        .status-in-progress { background: #3B82F6; color: white; }
        .status-pending { background: #6B7280; color: white; }
        
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            color: #CBD5E1;
        }
        
        .metric-value {
            color: #F5C542;
            font-weight: 600;
        }
        
        .projects-list {
            margin-top: 20px;
        }
        
        .project-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .project-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        #loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top: 3px solid #F5C542;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Creative Intelligence Engine</h1>
            <p>Dominion Command Dashboard - The Throne Room of Creative Sovereignty</p>
        </div>
        
        <div class="input-section">
            <h2>📝 Create New Project</h2>
            <textarea id="projectDescription" placeholder="Describe your creative project...

Example: Create a comprehensive video course teaching youth entrepreneurship. Target audience: teenagers and young adults (13-25). Content should be energetic, modern, and inspirational. Include topics: business planning, marketing, finance basics, and digital presence. Brand: CodexDominion (sovereign, empowering, innovative). Output: Multi-platform video series for YouTube, TikTok, and Instagram."></textarea>
            <button onclick="createProject()">🚀 Create Project</button>
        </div>
        
        <div id="loading">
            <div class="spinner"></div>
            <p>Creating project...</p>
        </div>
        
        <div class="input-section">
            <h2>📁 Recent Projects</h2>
            <div id="projectsList" class="projects-list">
                <p style="color: #6B7280;">No projects yet. Create one above to get started!</p>
            </div>
        </div>
        
        <div id="dashboardView" style="display:none;">
            <h2 style="color: #F5C542; margin-bottom: 20px;">Project Dashboard</h2>
            <div class="dashboard" id="dashboardPanels"></div>
        </div>
    </div>
    
    <script>
        async function createProject() {
            const description = document.getElementById('projectDescription').value;
            
            if (!description.trim()) {
                alert('Please enter a project description');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch('/creative/api/project/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ description })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`Project created! ID: ${data.project_id}`);
                    loadProjects();
                    document.getElementById('projectDescription').value = '';
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error creating project: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        async function loadProjects() {
            try {
                const response = await fetch('/creative/api/projects');
                const data = await response.json();
                
                const projectsList = document.getElementById('projectsList');
                
                if (data.projects && data.projects.length > 0) {
                    projectsList.innerHTML = data.projects.map(p => `
                        <div class="project-item" onclick="viewProject('${p.id}')">
                            <strong>${p.type}</strong>
                            <br>
                            <span class="status-badge status-${p.status}">${p.status}</span>
                            <br>
                            <small style="color: #6B7280;">${p.created_at}</small>
                        </div>
                    `).join('');
                } else {
                    projectsList.innerHTML = '<p style="color: #6B7280;">No projects yet.</p>';
                }
            } catch (error) {
                console.error('Error loading projects:', error);
            }
        }
        
        async function viewProject(projectId) {
            try {
                const response = await fetch(`/creative/api/dashboard/${projectId}`);
                const dashboard = await response.json();
                
                const dashboardView = document.getElementById('dashboardView');
                const dashboardPanels = document.getElementById('dashboardPanels');
                
                dashboardPanels.innerHTML = `
                    <div class="panel">
                        <h3>📊 Project Overview</h3>
                        <div class="metric">
                            <span class="metric-label">Status</span>
                            <span class="metric-value">${dashboard.project_overview.status}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Phase</span>
                            <span class="metric-value">${dashboard.project_overview.current_phase}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Progress</span>
                            <span class="metric-value">${(dashboard.project_overview.progress_percentage * 100).toFixed(1)}%</span>
                        </div>
                    </div>
                    
                    <div class="panel">
                        <h3>🏥 Studio Status</h3>
                        <div class="metric">
                            <span class="metric-label">Overall Health</span>
                            <span class="metric-value">${dashboard.studio_status.overall_health}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Graphics Studio</span>
                            <span class="metric-value">${dashboard.studio_status.graphics_studio.status}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Audio Studio</span>
                            <span class="metric-value">${dashboard.studio_status.audio_studio.status}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Video Studio</span>
                            <span class="metric-value">${dashboard.studio_status.video_studio.status}</span>
                        </div>
                    </div>
                    
                    <div class="panel">
                        <h3>🎯 Summary</h3>
                        <div class="metric">
                            <span class="metric-label">Phase</span>
                            <span class="metric-value">${dashboard.summary.phase}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Progress</span>
                            <span class="metric-value">${dashboard.summary.progress}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Next Step</span>
                            <span class="metric-value">${dashboard.summary.next_step}</span>
                        </div>
                    </div>
                `;
                
                dashboardView.style.display = 'block';
                dashboardView.scrollIntoView({ behavior: 'smooth' });
            } catch (error) {
                alert('Error loading dashboard: ' + error.message);
            }
        }
        
        // Load projects on page load
        loadProjects();
    </script>
</body>
</html>
'''

# ═══════════════════════════════════════════════════════════════════════════
# INTEGRATION INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════════════

"""
TO INTEGRATE WITH FLASK_DASHBOARD.PY:

1. Add this import at the top of flask_dashboard.py:
   from creative_engine_routes import creative_engine_bp

2. Register the blueprint after creating the Flask app:
   app.register_blueprint(creative_engine_bp)

3. Access the dashboard at:
   http://localhost:5000/creative/

That's it! The Creative Intelligence Engine is now integrated with your Flask dashboard.
"""
