"""
Automation Timeline API

Endpoints for tracking and displaying automation execution history.
Every automation firing creates an AutomationEvent record that appears in the timeline.

Author: Codex Dominion
Created: December 20, 2025
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from db import SessionLocal
from models import AutomationEvent, AutomationRule, Workflow, TriggerType, EventResult
from typing import Dict, Any, Optional, List


timeline_bp = Blueprint('automation_timeline', __name__)


def register_automation_timeline_routes(app):
    """Register timeline API routes with Flask app"""
    app.register_blueprint(timeline_bp, url_prefix='/api/automation-timeline')


# ================================================================
# TIMELINE ENDPOINTS
# ================================================================

@timeline_bp.route('/tenant/<tenant_id>', methods=['GET'])
def get_tenant_timeline(tenant_id: str):
    """
    Get automation timeline for tenant with filters
    
    Query params:
    - category: Filter by automation category (Store, Marketing, Website, Customer Behavior, Analytics)
    - result: Filter by result (success, skipped, failed)
    - days: Number of days to show (default: 30)
    - limit: Max events to return (default: 100)
    - offset: Pagination offset (default: 0)
    
    Returns:
    {
        "events": [...],
        "total_count": 150,
        "filters": {
            "category": "Store",
            "result": "success",
            "days": 30
        },
        "stats": {
            "total_events": 150,
            "success": 120,
            "skipped": 20,
            "failed": 10,
            "by_category": {
                "Store": 40,
                "Marketing": 60,
                ...
            }
        }
    }
    """
    session = SessionLocal()
    
    try:
        # Parse filters
        category = request.args.get('category', None)
        result_filter = request.args.get('result', None)
        days = int(request.args.get('days', 30))
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        # Base query
        query = session.query(AutomationEvent).filter(
            AutomationEvent.tenant_id == tenant_id
        )
        
        # Date filter
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(AutomationEvent.timestamp >= start_date)
        
        # Category filter - get from event metadata
        # Note: Category filtering now done post-query since we removed AutomationRule dependency
        
        # Result filter
        if result_filter and result_filter != 'All':
            if result_filter == 'Errors':
                query = query.filter(AutomationEvent.result == EventResult.FAILED)
            else:
                query = query.filter(AutomationEvent.result == EventResult[result_filter.upper()])
        
        # Get total count
        total_count = query.count()
        
        # Paginate
        events_raw = query.order_by(AutomationEvent.timestamp.desc()).limit(limit).offset(offset).all()
        
        # Format events - use only AutomationEvent data
        events = []
        for event in events_raw:
            # Extract category from metadata or automation_id
            metadata = event.event_metadata or {}
            category_from_id = 'Unknown'
            if 'social' in event.automation_id:
                category_from_id = 'Marketing'
            elif 'cart' in event.automation_id or 'email' in event.automation_id:
                category_from_id = 'Store'
            elif 'seo' in event.automation_id or 'homepage' in event.automation_id or 'landing' in event.automation_id:
                category_from_id = 'Website'
            elif 'behavior' in event.automation_id:
                category_from_id = 'Customer Behavior'
            elif 'report' in event.automation_id or 'analytics' in event.automation_id:
                category_from_id = 'Analytics'
            
            automation_category = metadata.get('category', category_from_id)
            
            # Get automation name from ID
            automation_name = event.automation_id.replace('auto_', '').replace('_', ' ').title()
            
            events.append({
                'id': event.id,
                'automation_id': event.automation_id,
                'automation_name': automation_name,
                'automation_category': automation_category,
                'trigger_type': event.trigger_type.value,
                'timestamp': event.timestamp.isoformat() + 'Z',
                'result': event.result.value,
                'message': event.message,
                'workflow': {
                    'id': event.workflow_id,
                    'status': 'completed'
                } if event.workflow_id else None,
                'metadata': metadata
            })
        
        # Calculate stats
        all_events = session.query(AutomationEvent).filter(
            AutomationEvent.tenant_id == tenant_id,
            AutomationEvent.timestamp >= start_date
        ).all()
        
        stats = {
            'total_events': len(all_events),
            'success': sum(1 for e in all_events if e.result == EventResult.SUCCESS),
            'skipped': sum(1 for e in all_events if e.result == EventResult.SKIPPED),
            'failed': sum(1 for e in all_events if e.result == EventResult.FAILED),
            'by_category': {}
        }
        
        # Count by category - extract from metadata or automation_id
        category_counts = {}
        for event in all_events:
            metadata = event.event_metadata or {}
            category_from_id = 'Unknown'
            if 'social' in event.automation_id:
                category_from_id = 'Marketing'
            elif 'cart' in event.automation_id or 'email' in event.automation_id:
                category_from_id = 'Store'
            elif 'seo' in event.automation_id or 'homepage' in event.automation_id or 'landing' in event.automation_id:
                category_from_id = 'Website'
            elif 'behavior' in event.automation_id:
                category_from_id = 'Customer Behavior'
            elif 'report' in event.automation_id or 'analytics' in event.automation_id:
                category_from_id = 'Analytics'
            
            cat = metadata.get('category', category_from_id)
            category_counts[cat] = category_counts.get(cat, 0) + 1
        stats['by_category'] = category_counts
        
        return jsonify({
            'events': events,
            'total_count': total_count,
            'filters': {
                'category': category,
                'result': result_filter,
                'days': days
            },
            'stats': stats
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@timeline_bp.route('/event/<event_id>', methods=['GET'])
def get_event_details(event_id: str):
    """
    Get detailed information about a specific automation event
    
    Returns:
    {
        "event": {
            "id": "...",
            "automation_id": "...",
            "automation_name": "Weekly Social Post Generator",
            "automation_category": "Marketing",
            "trigger_type": "schedule",
            "timestamp": "2025-12-20T09:00:00Z",
            "result": "success",
            "message": "Generated 5 posts for Instagram and TikTok",
            "workflow": {...},
            "metadata": {...}
        },
        "automation": {
            "id": "...",
            "name": "...",
            "description": "...",
            "enabled": true
        }
    }
    """
    session = SessionLocal()
    
    try:
        event = session.query(AutomationEvent).filter_by(id=event_id).first()
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        # Extract category from metadata or automation_id
        metadata = event.event_metadata or {}
        category_from_id = 'Unknown'
        if 'social' in event.automation_id:
            category_from_id = 'Marketing'
        elif 'cart' in event.automation_id or 'email' in event.automation_id:
            category_from_id = 'Store'
        elif 'seo' in event.automation_id or 'homepage' in event.automation_id or 'landing' in event.automation_id:
            category_from_id = 'Website'
        elif 'behavior' in event.automation_id:
            category_from_id = 'Customer Behavior'
        elif 'report' in event.automation_id or 'analytics' in event.automation_id:
            category_from_id = 'Analytics'
        
        automation_category = metadata.get('category', category_from_id)
        automation_name = event.automation_id.replace('auto_', '').replace('_', ' ').title()
        
        return jsonify({
            'event': {
                'id': event.id,
                'automation_id': event.automation_id,
                'automation_name': automation_name,
                'automation_category': automation_category,
                'trigger_type': event.trigger_type.value,
                'timestamp': event.timestamp.isoformat() + 'Z',
                'result': event.result.value,
                'message': event.message,
                'workflow': {
                    'id': event.workflow_id,
                    'status': 'completed'
                } if event.workflow_id else None,
                'metadata': metadata
            },
            'automation': {
                'id': event.automation_id,
                'name': automation_name,
                'description': f"{automation_category} automation",
                'enabled': True,
                'category': automation_category
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@timeline_bp.route('/stats/<tenant_id>', methods=['GET'])
def get_timeline_stats(tenant_id: str):
    """
    Get aggregate statistics for automation timeline
    
    Query params:
    - days: Number of days to analyze (default: 30)
    
    Returns:
    {
        "total_events": 150,
        "success_rate": 0.80,
        "most_active_automation": "Weekly Social Post Generator",
        "recent_failures": [...],
        "activity_by_day": [...],
        "category_breakdown": {...}
    }
    """
    session = SessionLocal()
    
    try:
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)
        
        events = session.query(AutomationEvent).filter(
            AutomationEvent.tenant_id == tenant_id,
            AutomationEvent.timestamp >= start_date
        ).all()
        
        if not events:
            return jsonify({
                'total_events': 0,
                'success_rate': 0.0,
                'most_active_automation': None,
                'recent_failures': [],
                'activity_by_day': [],
                'category_breakdown': {}
            }), 200
        
        # Calculate success rate
        success_count = sum(1 for e in events if e.result == EventResult.SUCCESS)
        success_rate = success_count / len(events) if events else 0.0
        
        # Find most active automation
        automation_counts = {}
        for event in events:
            automation_counts[event.automation_id] = automation_counts.get(event.automation_id, 0) + 1
        
        most_active_id = max(automation_counts, key=automation_counts.get) if automation_counts else None
        most_active_automation = None
        if most_active_id:
            most_active_automation = most_active_id.replace('auto_', '').replace('_', ' ').title()
        
        # Recent failures
        recent_failures = []
        failed_events = [e for e in events if e.result == EventResult.FAILED]
        for event in sorted(failed_events, key=lambda e: e.timestamp, reverse=True)[:5]:
            automation_name = event.automation_id.replace('auto_', '').replace('_', ' ').title()
            recent_failures.append({
                'id': event.id,
                'automation_name': automation_name,
                'timestamp': event.timestamp.isoformat() + 'Z',
                'message': event.message
            })
        
        # Activity by day
        activity_by_day = {}
        for event in events:
            day_key = event.timestamp.strftime('%Y-%m-%d')
            activity_by_day[day_key] = activity_by_day.get(day_key, 0) + 1
        
        activity_list = [
            {'date': day, 'count': count}
            for day, count in sorted(activity_by_day.items())
        ]
        
        # Category breakdown - extract from metadata
        category_breakdown = {}
        for event in events:
            metadata = event.event_metadata or {}
            category_from_id = 'Unknown'
            if 'social' in event.automation_id:
                category_from_id = 'Marketing'
            elif 'cart' in event.automation_id or 'email' in event.automation_id:
                category_from_id = 'Store'
            elif 'seo' in event.automation_id or 'homepage' in event.automation_id or 'landing' in event.automation_id:
                category_from_id = 'Website'
            elif 'behavior' in event.automation_id:
                category_from_id = 'Customer Behavior'
            elif 'report' in event.automation_id or 'analytics' in event.automation_id:
                category_from_id = 'Analytics'
            
            cat = metadata.get('category', category_from_id)
            category_breakdown[cat] = category_breakdown.get(cat, 0) + 1
        
        return jsonify({
            'total_events': len(events),
            'success_rate': round(success_rate, 2),
            'most_active_automation': most_active_automation,
            'recent_failures': recent_failures,
            'activity_by_day': activity_list,
            'category_breakdown': category_breakdown
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


# ================================================================
# HELPER FUNCTIONS
# ================================================================

def create_automation_event(
    tenant_id: str,
    automation_id: str,
    trigger_type: TriggerType,
    result: EventResult,
    message: str,
    workflow_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> AutomationEvent:
    """
    Helper function to create automation events
    
    Usage in automation_worker.py:
        from automation_timeline_api import create_automation_event
        from models import EventResult
        
        event = create_automation_event(
            tenant_id="tenant_123",
            automation_id="auto_456",
            trigger_type=TriggerType.SCHEDULE,
            result=EventResult.SUCCESS,
            message="Generated 5 posts for Instagram",
            workflow_id="workflow_789",
            metadata={"platforms": ["Instagram", "TikTok"], "post_count": 5}
        )
    
    Args:
        tenant_id: The tenant who owns this automation
        automation_id: The automation rule that fired
        trigger_type: Type of trigger (event, schedule, threshold, behavior)
        result: Outcome (success, skipped, failed)
        message: Human-readable summary of what happened
        workflow_id: Optional workflow created by this automation
        metadata: Optional JSON metadata with additional details
    
    Returns:
        The created AutomationEvent instance
    """
    session = SessionLocal()
    
    try:
        event = AutomationEvent(
            tenant_id=tenant_id,
            automation_id=automation_id,
            trigger_type=trigger_type,
            timestamp=datetime.utcnow(),
            result=result,
            message=message,
            workflow_id=workflow_id,
            event_metadata=metadata or {}
        )
        
        session.add(event)
        session.commit()
        
        return event
    
    except Exception as e:
        session.rollback()
        print(f"Error creating automation event: {str(e)}")
        raise
    
    finally:
        session.close()


def format_timeline_entry(event: AutomationEvent, automation: AutomationRule, workflow: Optional[Workflow] = None) -> Dict[str, Any]:
    """
    Format an automation event for timeline display
    
    Returns:
    {
        "id": "...",
        "icon": "checkCircle",
        "icon_color": "emerald",
        "automation_name": "Weekly Social Post Generator",
        "trigger_label": "Schedule",
        "timestamp": "2025-12-20T09:00:00Z",
        "timestamp_label": "Monday at 9:00 AM",
        "result": "success",
        "result_label": "Fired",
        "message": "Generated 5 posts for Instagram and TikTok",
        "workflow_link": "/portal/workflows/workflow_789",
        "has_workflow": true
    }
    """
    # Icon and color based on result
    icon_map = {
        EventResult.SUCCESS: ('checkCircle', 'emerald'),
        EventResult.SKIPPED: ('info', 'blue'),
        EventResult.FAILED: ('xCircle', 'crimson')
    }
    icon, icon_color = icon_map.get(event.result, ('info', 'slate'))
    
    # Result label
    result_labels = {
        EventResult.SUCCESS: 'Fired',
        EventResult.SKIPPED: 'Skipped',
        EventResult.FAILED: 'Failed'
    }
    result_label = result_labels.get(event.result, 'Unknown')
    
    # Trigger label
    trigger_labels = {
        TriggerType.EVENT: 'Event',
        TriggerType.SCHEDULE: 'Schedule',
        TriggerType.THRESHOLD: 'Threshold',
        TriggerType.BEHAVIOR: 'Behavior'
    }
    trigger_label = trigger_labels.get(event.trigger_type, 'Unknown')
    
    # Format timestamp
    timestamp_label = event.timestamp.strftime('%A at %I:%M %p')
    
    return {
        'id': event.id,
        'icon': icon,
        'icon_color': icon_color,
        'automation_name': automation.name,
        'automation_category': automation.category,
        'trigger_label': trigger_label,
        'timestamp': event.timestamp.isoformat() + 'Z',
        'timestamp_label': timestamp_label,
        'result': event.result.value,
        'result_label': result_label,
        'message': event.message,
        'workflow_link': f'/portal/workflows/{workflow.id}' if workflow else None,
        'has_workflow': workflow is not None,
        'metadata': event.event_metadata or {}
    }


# Export helper function for use in other modules
__all__ = ['register_automation_timeline_routes', 'create_automation_event', 'format_timeline_entry']
