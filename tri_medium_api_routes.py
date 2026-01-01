"""
🔥 CODEX DOMINION - TRI-MEDIUM FLASK API ROUTES 🔥
====================================================
RESTful API endpoints for Tri-Medium Integration Layer

Provides comprehensive HTTP API for:
- Creating and managing integrated projects
- Executing cross-medium workflows
- Real-time status monitoring
- Asset management and retrieval
- System health checks

Integration with Flask Master Dashboard (flask_dashboard.py)

API Endpoints:
    POST   /api/tri-medium/projects              - Create project
    GET    /api/tri-medium/projects              - List projects
    GET    /api/tri-medium/projects/<id>         - Get project details
    POST   /api/tri-medium/projects/<id>/execute - Execute project
    DELETE /api/tri-medium/projects/<id>         - Delete project
    GET    /api/tri-medium/status                - System status
    GET    /api/tri-medium/health                - Health check

Author: Codex Dominion High Council
Last Updated: December 23, 2025
"""

from flask import Blueprint, request, jsonify, send_file
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from tri_medium_integration_core import (
    get_tri_medium_core,
    IntegrationMode,
    ProjectPriority,
    MediumType
)

# Create Flask Blueprint
tri_medium_bp = Blueprint('tri_medium', __name__, url_prefix='/api/tri-medium')

# Configure logging
logger = logging.getLogger(__name__)


def validate_mediums(mediums: List[str]) -> bool:
    """Validate that provided mediums are valid"""
    valid_mediums = {"graphics", "audio", "video"}
    return all(m.lower() in valid_mediums for m in mediums)


def validate_mode(mode: str) -> bool:
    """Validate integration mode"""
    valid_modes = {"sequential", "parallel", "adaptive", "custom"}
    return mode.lower() in valid_modes


def validate_priority(priority: str) -> bool:
    """Validate project priority"""
    valid_priorities = {"urgent", "high", "medium", "low"}
    return priority.lower() in valid_priorities


@tri_medium_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        200: System is healthy
        500: System has issues
    
    Example:
        GET /api/tri-medium/health
        
        Response:
        {
            "status": "healthy",
            "timestamp": "2025-12-23T10:30:00.000000Z",
            "version": "1.0.0"
        }
    """
    try:
        core = get_tri_medium_core()
        system_status = core.get_system_status()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "mediums_available": {
                "graphics": system_status["mediums"]["graphics"]["available"],
                "audio": system_status["mediums"]["audio"]["available"],
                "video": system_status["mediums"]["video"]["available"]
            }
        }), 200
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 500


@tri_medium_bp.route('/status', methods=['GET'])
def get_system_status():
    """
    Get comprehensive system status
    
    Returns:
        System health metrics across all mediums
    
    Example:
        GET /api/tri-medium/status
        
        Response:
        {
            "mediums": {...},
            "total_active_projects": 5,
            "integration_components": {...}
        }
    """
    try:
        core = get_tri_medium_core()
        status = core.get_system_status()
        
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"❌ Failed to get system status: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/projects', methods=['POST'])
def create_project():
    """
    Create a new integrated project
    
    Request Body:
        {
            "name": "Project Name",
            "mediums": ["graphics", "audio", "video"],
            "mode": "parallel",  # sequential, parallel, adaptive, custom
            "priority": "high",  # urgent, high, medium, low
            "metadata": {...}    # Optional
        }
    
    Returns:
        201: Project created successfully
        400: Invalid request
    
    Example:
        POST /api/tri-medium/projects
        Content-Type: application/json
        
        {
            "name": "Marketing Campaign Q1",
            "mediums": ["graphics", "video"],
            "mode": "parallel",
            "priority": "high"
        }
        
        Response:
        {
            "project_id": "tri_medium_abc123def456",
            "name": "Marketing Campaign Q1",
            "status": "created",
            "mediums": ["graphics", "video"]
        }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'mediums' not in data:
            return jsonify({"error": "Missing required fields: name, mediums"}), 400
        
        name = data['name']
        mediums = data['mediums']
        mode = data.get('mode', 'sequential')
        priority = data.get('priority', 'medium')
        metadata = data.get('metadata', {})
        
        # Validate inputs
        if not validate_mediums(mediums):
            return jsonify({"error": "Invalid mediums. Must be: graphics, audio, or video"}), 400
        
        if not validate_mode(mode):
            return jsonify({"error": "Invalid mode. Must be: sequential, parallel, adaptive, or custom"}), 400
        
        if not validate_priority(priority):
            return jsonify({"error": "Invalid priority. Must be: urgent, high, medium, or low"}), 400
        
        # Create project
        core = get_tri_medium_core()
        project_id = core.create_integrated_project(
            name=name,
            mediums=mediums,
            mode=IntegrationMode(mode.upper()),
            priority=ProjectPriority(priority.upper()),
            metadata=metadata
        )
        
        project = core.get_project_status(project_id)
        
        logger.info(f"🔥 Created project {project_id}: {name}")
        
        return jsonify({
            "project_id": project_id,
            "name": name,
            "status": project["status"],
            "mediums": project["mediums"],
            "created_at": project["created_at"]
        }), 201
        
    except Exception as e:
        logger.error(f"❌ Failed to create project: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/projects', methods=['GET'])
def list_projects():
    """
    List all projects with optional filtering
    
    Query Parameters:
        status: Filter by status (created, executing, completed, partial)
        medium: Filter by medium (graphics, audio, video)
    
    Returns:
        List of projects
    
    Example:
        GET /api/tri-medium/projects?status=executing&medium=graphics
        
        Response:
        {
            "projects": [...],
            "count": 5,
            "timestamp": "2025-12-23T10:30:00.000000Z"
        }
    """
    try:
        core = get_tri_medium_core()
        
        # Get filter parameters
        status_filter = request.args.get('status')
        medium_filter = request.args.get('medium')
        
        # Validate filters
        if medium_filter and not validate_mediums([medium_filter]):
            return jsonify({"error": "Invalid medium filter"}), 400
        
        # Get projects
        projects = core.list_projects(
            status_filter=status_filter,
            medium_filter=medium_filter
        )
        
        return jsonify({
            "projects": projects,
            "count": len(projects),
            "filters": {
                "status": status_filter,
                "medium": medium_filter
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Failed to list projects: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id: str):
    """
    Get detailed project information
    
    Args:
        project_id: Project identifier
    
    Returns:
        Complete project details
    
    Example:
        GET /api/tri-medium/projects/tri_medium_abc123def456
        
        Response:
        {
            "id": "tri_medium_abc123def456",
            "name": "Marketing Campaign Q1",
            "status": "executing",
            "mediums": ["graphics", "video"],
            "completion_percentage": 45,
            ...
        }
    """
    try:
        core = get_tri_medium_core()
        project = core.get_project_status(project_id)
        
        return jsonify(project), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"❌ Failed to get project {project_id}: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/projects/<project_id>/execute', methods=['POST'])
def execute_project(project_id: str):
    """
    Execute a project across all specified mediums
    
    Args:
        project_id: Project identifier
    
    Returns:
        Execution results for each medium
    
    Example:
        POST /api/tri-medium/projects/tri_medium_abc123def456/execute
        
        Response:
        {
            "project_id": "tri_medium_abc123def456",
            "status": "executing",
            "results": {
                "graphics": {"status": "completed", ...},
                "video": {"status": "completed", ...}
            }
        }
    """
    try:
        core = get_tri_medium_core()
        
        # Execute project
        results = core.execute_project(project_id)
        
        # Get updated status
        project = core.get_project_status(project_id)
        
        logger.info(f"🚀 Executed project {project_id}")
        
        return jsonify({
            "project_id": project_id,
            "status": project["status"],
            "completion_percentage": project["completion_percentage"],
            "results": results,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"❌ Failed to execute project {project_id}: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id: str):
    """
    Delete a project
    
    Args:
        project_id: Project identifier
    
    Returns:
        Deletion confirmation
    
    Example:
        DELETE /api/tri-medium/projects/tri_medium_abc123def456
        
        Response:
        {
            "message": "Project deleted successfully",
            "project_id": "tri_medium_abc123def456"
        }
    """
    try:
        core = get_tri_medium_core()
        
        # Check if project exists
        if project_id not in core.active_projects:
            return jsonify({"error": "Project not found"}), 404
        
        # Move to history and remove from active
        project = core.active_projects[project_id]
        core.project_history.append(project)
        del core.active_projects[project_id]
        core._save_state()
        
        logger.info(f"🗑️ Deleted project {project_id}")
        
        return jsonify({
            "message": "Project deleted successfully",
            "project_id": project_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Failed to delete project {project_id}: {e}")
        return jsonify({"error": str(e)}), 500


@tri_medium_bp.route('/mediums', methods=['GET'])
def get_available_mediums():
    """
    Get list of available mediums and their capabilities
    
    Returns:
        Available mediums with status
    
    Example:
        GET /api/tri-medium/mediums
        
        Response:
        {
            "mediums": {
                "graphics": {"available": true, "clusters": [...]},
                "audio": {"available": true, "services": [...]},
                "video": {"available": false}
            }
        }
    """
    try:
        core = get_tri_medium_core()
        system_status = core.get_system_status()
        
        return jsonify({
            "mediums": system_status["mediums"],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Failed to get mediums: {e}")
        return jsonify({"error": str(e)}), 500


# Error handlers
@tri_medium_bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@tri_medium_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found", "message": str(error)}), 404


@tri_medium_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


def register_tri_medium_routes(app):
    """
    Register Tri-Medium API routes with Flask app
    
    Usage in flask_dashboard.py:
        from tri_medium_api_routes import register_tri_medium_routes
        register_tri_medium_routes(app)
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(tri_medium_bp)
    logger.info("✅ Registered Tri-Medium API routes at /api/tri-medium")


if __name__ == "__main__":
    # Standalone testing
    from flask import Flask
    
    app = Flask(__name__)
    register_tri_medium_routes(app)
    
    print("\n🔥 Tri-Medium API Routes registered!")
    print("\nAvailable endpoints:")
    print("  POST   /api/tri-medium/projects")
    print("  GET    /api/tri-medium/projects")
    print("  GET    /api/tri-medium/projects/<id>")
    print("  POST   /api/tri-medium/projects/<id>/execute")
    print("  DELETE /api/tri-medium/projects/<id>")
    print("  GET    /api/tri-medium/status")
    print("  GET    /api/tri-medium/health")
    print("  GET    /api/tri-medium/mediums")
    
    print("\n🔥 Ready to integrate with Flask Master Dashboard! 👑")
