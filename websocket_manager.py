"""
🔥 CODEX DOMINION - WEBSOCKET REAL-TIME UPDATES 🔥
====================================================
WebSocket manager for real-time workflow updates and progress tracking.

Provides live updates for:
- Workflow execution progress
- Asset generation status
- Rendering operations
- Module completion events
- Error notifications

Author: Codex Dominion High Council
Phase: 30 - Creative Intelligence Engine (Option 6)
Last Updated: December 23, 2025
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import json

# Global SocketIO instance (initialized by Flask app)
socketio = None

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages real-time WebSocket communications for the Creative Intelligence Engine.
    
    Event Types:
    - workflow_started: New workflow execution begins
    - workflow_progress: Step completion updates
    - workflow_complete: Workflow execution finished
    - workflow_error: Error occurred during execution
    - rendering_progress: Real-time rendering progress (0-100%)
    - asset_created: New asset generated
    - module_update: Individual module status change
    
    Room Structure:
    - project:{project_id} - Project-specific updates
    - workflow:{workflow_id} - Workflow-specific updates
    - global - System-wide broadcasts
    """
    
    def __init__(self, app: Optional[Flask] = None):
        """Initialize WebSocket Manager"""
        self.logger = logging.getLogger(__name__)
        
        if app:
            self.init_app(app)
        
        self.logger.info("🔥 WebSocket Manager initialized! 👑")
    
    def init_app(self, app: Flask, cors_allowed_origins="*"):
        """
        Initialize Flask-SocketIO with the Flask app.
        
        Args:
            app: Flask application instance
            cors_allowed_origins: CORS origins (use "*" for development)
        """
        global socketio
        
        socketio = SocketIO(
            app,
            cors_allowed_origins=cors_allowed_origins,
            async_mode='threading',  # Use threading for async support (more stable than eventlet)
            logger=True,
            engineio_logger=False
        )
        
        # Register event handlers
        self._register_handlers(socketio)
        
        self.logger.info("✅ Flask-SocketIO initialized with CORS and event handlers")
        
        return socketio
    
    def _register_handlers(self, socketio_instance):
        """Register WebSocket event handlers"""
        
        @socketio_instance.on('connect')
        def handle_connect():
            """Handle client connection"""
            self.logger.info(f"🔌 Client connected")
            emit('connection_status', {
                'status': 'connected',
                'message': '🔥 Connected to Codex Dominion Creative Intelligence Engine! 👑',
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        
        @socketio_instance.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            self.logger.info(f"🔌 Client disconnected")
        
        @socketio_instance.on('join_project')
        def handle_join_project(data):
            """Join a project-specific room for updates"""
            project_id = data.get('project_id')
            if project_id:
                join_room(f"project:{project_id}")
                self.logger.info(f"📡 Client joined project room: {project_id}")
                emit('joined_room', {
                    'room': f"project:{project_id}",
                    'message': f'Subscribed to project updates'
                })
        
        @socketio_instance.on('leave_project')
        def handle_leave_project(data):
            """Leave a project-specific room"""
            project_id = data.get('project_id')
            if project_id:
                leave_room(f"project:{project_id}")
                self.logger.info(f"📡 Client left project room: {project_id}")
                emit('left_room', {
                    'room': f"project:{project_id}",
                    'message': f'Unsubscribed from project updates'
                })
        
        @socketio_instance.on('join_workflow')
        def handle_join_workflow(data):
            """Join a workflow-specific room for execution updates"""
            workflow_id = data.get('workflow_id')
            if workflow_id:
                join_room(f"workflow:{workflow_id}")
                self.logger.info(f"📡 Client joined workflow room: {workflow_id}")
                emit('joined_room', {
                    'room': f"workflow:{workflow_id}",
                    'message': f'Subscribed to workflow updates'
                })
        
        @socketio_instance.on('ping')
        def handle_ping():
            """Health check / keep-alive"""
            emit('pong', {'timestamp': datetime.now(timezone.utc).isoformat()})
    
    # =========================================================================
    # WORKFLOW EVENTS
    # =========================================================================
    
    @staticmethod
    def emit_workflow_started(
        workflow_id: str,
        project_id: str,
        workflow_type: str,
        total_steps: int,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Emit workflow started event.
        
        Args:
            workflow_id: Unique workflow execution ID
            project_id: Associated project ID
            workflow_type: Type of workflow (creative_intelligence, rendering, etc.)
            total_steps: Total number of steps in workflow
            metadata: Additional workflow metadata
        """
        if not socketio:
            return
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'workflow_type': workflow_type,
            'total_steps': total_steps,
            'current_step': 0,
            'status': 'started',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'metadata': metadata or {}
        }
        
        # Emit to workflow room and project room
        socketio.emit('workflow_started', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('workflow_started', event_data, room=f"project:{project_id}")
        socketio.emit('workflow_started', event_data, broadcast=True, namespace='/')
        
        logger.info(f"🚀 Emitted workflow_started: {workflow_id}")
    
    @staticmethod
    def emit_workflow_progress(
        workflow_id: str,
        project_id: str,
        current_step: int,
        total_steps: int,
        step_name: str,
        step_status: str,
        step_result: Optional[Dict[str, Any]] = None,
        progress_percentage: Optional[float] = None
    ):
        """
        Emit workflow progress update.
        
        Args:
            workflow_id: Workflow execution ID
            project_id: Project ID
            current_step: Current step number (1-indexed)
            total_steps: Total steps in workflow
            step_name: Name of current step (PIC, CRE, MMOE, etc.)
            step_status: Status (running, complete, error)
            step_result: Optional result data from step
            progress_percentage: Overall progress (0-100)
        """
        if not socketio:
            return
        
        if progress_percentage is None:
            progress_percentage = (current_step / total_steps) * 100
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'current_step': current_step,
            'total_steps': total_steps,
            'step_name': step_name,
            'step_status': step_status,
            'step_result': step_result,
            'progress_percentage': round(progress_percentage, 2),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('workflow_progress', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('workflow_progress', event_data, room=f"project:{project_id}")
        
        logger.info(f"📊 Emitted workflow_progress: {workflow_id} - {step_name} ({progress_percentage:.1f}%)")
    
    @staticmethod
    def emit_workflow_complete(
        workflow_id: str,
        project_id: str,
        status: str,
        duration_seconds: float,
        results: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ):
        """
        Emit workflow completion event.
        
        Args:
            workflow_id: Workflow execution ID
            project_id: Project ID
            status: Final status (complete, failed, cancelled)
            duration_seconds: Total execution time
            results: Workflow results
            error_message: Error message if failed
        """
        if not socketio:
            return
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'status': status,
            'duration_seconds': duration_seconds,
            'results': results,
            'error_message': error_message,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('workflow_complete', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('workflow_complete', event_data, room=f"project:{project_id}")
        socketio.emit('workflow_complete', event_data, broadcast=True, namespace='/')
        
        status_emoji = "✅" if status == "complete" else "❌"
        logger.info(f"{status_emoji} Emitted workflow_complete: {workflow_id} - {status} ({duration_seconds:.2f}s)")
    
    @staticmethod
    def emit_workflow_error(
        workflow_id: str,
        project_id: str,
        error_type: str,
        error_message: str,
        step_name: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None
    ):
        """
        Emit workflow error event.
        
        Args:
            workflow_id: Workflow execution ID
            project_id: Project ID
            error_type: Type of error (validation, execution, timeout, etc.)
            error_message: Error message
            step_name: Step where error occurred
            error_details: Additional error details
        """
        if not socketio:
            return
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'error_type': error_type,
            'error_message': error_message,
            'step_name': step_name,
            'error_details': error_details,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('workflow_error', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('workflow_error', event_data, room=f"project:{project_id}")
        
        logger.error(f"❌ Emitted workflow_error: {workflow_id} - {error_message}")
    
    # =========================================================================
    # RENDERING EVENTS
    # =========================================================================
    
    @staticmethod
    def emit_rendering_progress(
        workflow_id: str,
        project_id: str,
        asset_id: str,
        asset_name: str,
        asset_type: str,
        progress_percentage: float,
        status: str,
        current_frame: Optional[int] = None,
        total_frames: Optional[int] = None,
        estimated_time_remaining: Optional[float] = None
    ):
        """
        Emit real-time rendering progress.
        
        Args:
            workflow_id: Workflow execution ID
            project_id: Project ID
            asset_id: Asset being rendered
            asset_name: Name of asset
            asset_type: Type of asset (video, audio, image)
            progress_percentage: Rendering progress (0-100)
            status: Status (rendering, encoding, complete)
            current_frame: Current frame (for video)
            total_frames: Total frames (for video)
            estimated_time_remaining: ETA in seconds
        """
        if not socketio:
            return
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'asset_id': asset_id,
            'asset_name': asset_name,
            'asset_type': asset_type,
            'progress_percentage': round(progress_percentage, 2),
            'status': status,
            'current_frame': current_frame,
            'total_frames': total_frames,
            'estimated_time_remaining': estimated_time_remaining,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('rendering_progress', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('rendering_progress', event_data, room=f"project:{project_id}")
        
        logger.debug(f"🎨 Rendering progress: {asset_name} - {progress_percentage:.1f}%")
    
    # =========================================================================
    # ASSET EVENTS
    # =========================================================================
    
    @staticmethod
    def emit_asset_created(
        project_id: str,
        asset_id: str,
        asset_name: str,
        asset_type: str,
        created_by_module: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Emit asset creation event.
        
        Args:
            project_id: Project ID
            asset_id: New asset ID
            asset_name: Asset name
            asset_type: Asset type (video, audio, image, graphics)
            created_by_module: Module that created asset (PIC, CRE, MMOE, etc.)
            metadata: Asset metadata
        """
        if not socketio:
            return
        
        event_data = {
            'project_id': project_id,
            'asset_id': asset_id,
            'asset_name': asset_name,
            'asset_type': asset_type,
            'created_by_module': created_by_module,
            'metadata': metadata or {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('asset_created', event_data, room=f"project:{project_id}")
        
        logger.info(f"📦 Asset created: {asset_name} ({asset_type}) by {created_by_module}")
    
    # =========================================================================
    # MODULE EVENTS
    # =========================================================================
    
    @staticmethod
    def emit_module_update(
        workflow_id: str,
        project_id: str,
        module_name: str,
        status: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Emit individual module status update.
        
        Args:
            workflow_id: Workflow execution ID
            project_id: Project ID
            module_name: Module name (PIC, CRE, MMOE, ADG, CCS, OAE, DASHBOARD)
            status: Status (running, complete, error)
            message: Status message
            data: Additional module data
        """
        if not socketio:
            return
        
        event_data = {
            'workflow_id': workflow_id,
            'project_id': project_id,
            'module_name': module_name,
            'status': status,
            'message': message,
            'data': data or {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('module_update', event_data, room=f"workflow:{workflow_id}")
        socketio.emit('module_update', event_data, room=f"project:{project_id}")
        
        logger.info(f"🔧 Module update: {module_name} - {status}")
    
    # =========================================================================
    # SYSTEM EVENTS
    # =========================================================================
    
    @staticmethod
    def emit_system_notification(
        notification_type: str,
        title: str,
        message: str,
        severity: str = 'info',
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Emit system-wide notification.
        
        Args:
            notification_type: Type (info, warning, error, success)
            title: Notification title
            message: Notification message
            severity: Severity level (info, warning, error, critical)
            metadata: Additional metadata
        """
        if not socketio:
            return
        
        event_data = {
            'notification_type': notification_type,
            'title': title,
            'message': message,
            'severity': severity,
            'metadata': metadata or {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        socketio.emit('system_notification', event_data, broadcast=True, namespace='/')
        
        logger.info(f"📢 System notification: {title}")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_socketio_instance():
    """Get the global SocketIO instance"""
    return socketio


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == '__main__':
    print("🔥 WEBSOCKET MANAGER - STANDALONE TEST 🔥")
    print("=" * 80)
    print("⚠️  This module requires a Flask app to run properly.")
    print("   See creative_intelligence_interfaces.py for integration example.")
    print("\n✅ WebSocket Manager module loaded successfully!")
    print("=" * 80)
