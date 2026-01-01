"""
🔥 CODEX DOMINION - NOTIFICATION DISPATCH WORKER 🔥
====================================================
RQ worker that listens for workflow events and dispatches notifications

This is the "messenger spirit" of the Dominion.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import os

from db import SessionLocal, get_session_context
from models import (
    PortalNotification, NotificationType, Workflow, Tenant, User, 
    UserRole, WorkflowStatus
)
from notification_templates import NotificationTemplates, send_notification_email


class NotificationDispatcher:
    """
    Workflow notification dispatcher
    
    Handles the full lifecycle of notification dispatch:
    1. Determine notification type from event
    2. Render email and portal templates
    3. Send emails to eligible users
    4. Create portal notifications
    """
    
    @staticmethod
    def execute_notification_dispatch(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for notification dispatch
        
        Called by RQ worker when workflow events occur.
        
        Args:
            event: Event dict with keys:
                - workflow_id: str
                - event_type: str (status_change, step_complete, etc.)
                - step: str (optional, for step events)
                - status: str (optional, for status events)
                - metadata: dict (optional)
                
        Returns:
            Result dict with notification count and status
        """
        
        workflow_id = event.get('workflow_id')
        if not workflow_id:
            return {"error": "Missing workflow_id", "success": False}
        
        with get_session_context() as session:
            # Fetch workflow
            workflow = session.query(Workflow).filter_by(id=workflow_id).first()
            if not workflow:
                return {"error": f"Workflow {workflow_id} not found", "success": False}
            
            # Fetch tenant
            tenant = session.query(Tenant).filter_by(id=workflow.tenant_id).first()
            if not tenant:
                return {"error": f"Tenant {workflow.tenant_id} not found", "success": False}
            
            # Fetch eligible users (owners and collaborators)
            users = session.query(User).filter(
                User.tenant_id == tenant.id,
                User.role.in_([UserRole.OWNER, UserRole.COLLABORATOR])
            ).all()
            
            if not users:
                print(f"⚠️ No users to notify for workflow {workflow_id}")
                return {"success": True, "notifications_created": 0}
            
            # Determine notification type
            notification_type = NotificationDispatcher._determine_notification_type(
                event, workflow
            )
            
            if not notification_type:
                print(f"⚠️ Could not determine notification type for event: {event}")
                return {"success": True, "notifications_created": 0}
            
            # Render templates
            notifications_created = 0
            emails_sent = 0
            
            for user in users:
                # Render template
                template_data = NotificationTemplates.render(
                    notification_type=notification_type,
                    workflow=workflow.__dict__,
                    tenant=tenant.__dict__,
                    user=user.__dict__,
                    event=event
                )
                
                subject = template_data['subject']
                body = template_data['body']
                
                # Send email (async in production, sync for now)
                email_sent = False
                if user.email:
                    email_sent = send_notification_email(
                        to_email=user.email,
                        subject=subject,
                        body=body
                    )
                    if email_sent:
                        emails_sent += 1
                
                # Create portal notification
                notification = PortalNotification(
                    id=f"notif_{workflow_id}_{notification_type.value}_{datetime.utcnow().timestamp()}",
                    tenant_id=tenant.id,
                    workflow_id=workflow.id,
                    user_id=user.id,
                    type=notification_type,
                    subject=subject,
                    body=body,
                    step_name=event.get('step_name'),
                    summary=event.get('summary', {}),
                    email_sent=email_sent,
                    email_sent_at=datetime.utcnow() if email_sent else None
                )
                
                session.add(notification)
                notifications_created += 1
            
            session.commit()
            
            print(f"✅ Created {notifications_created} notifications, sent {emails_sent} emails for workflow {workflow_id}")
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "notification_type": notification_type.value,
                "notifications_created": notifications_created,
                "emails_sent": emails_sent
            }
    
    @staticmethod
    def _determine_notification_type(event: Dict[str, Any], 
                                     workflow: Workflow) -> Optional[NotificationType]:
        """
        Determine notification type from event and workflow state
        
        Logic:
        - If event.step == "workflow_started" → WORKFLOW_STARTED
        - If event.status == "completed" and not final step → STEP_COMPLETED
        - If workflow.status == "completed" → WORKFLOW_COMPLETED
        - If workflow.status == "pending_review" → NEEDS_REVIEW
        - If workflow.status == "failed" → WORKFLOW_FAILED
        """
        
        step = event.get('step', '').lower()
        event_status = event.get('status', '').lower()
        workflow_status = workflow.status.value if workflow.status else ''
        
        # Workflow started
        if step == "workflow_started" or (workflow_status == "in_progress" and event.get('is_start')):
            return NotificationType.WORKFLOW_STARTED
        
        # Workflow completed
        if workflow_status == "completed" or step == "workflow_complete":
            return NotificationType.WORKFLOW_COMPLETED
        
        # Workflow needs review
        if workflow_status == "pending_review":
            return NotificationType.NEEDS_REVIEW
        
        # Workflow failed
        if workflow_status == "failed":
            return NotificationType.WORKFLOW_FAILED
        
        # Step completed (intermediate step)
        if event_status == "completed" and step and step != "workflow_complete":
            return NotificationType.STEP_COMPLETED
        
        # Default: None (no notification)
        return None


# ============================================================================
# RQ WORKER TASK
# ============================================================================

def dispatch_workflow_notification(event: Dict[str, Any]):
    """
    RQ task for dispatching workflow notifications
    
    This function is enqueued by the workflow engine when events occur.
    
    Usage:
        from rq import Queue
        queue.enqueue(dispatch_workflow_notification, event)
    """
    try:
        result = NotificationDispatcher.execute_notification_dispatch(event)
        return result
    except Exception as e:
        print(f"❌ Notification dispatch failed: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "success": False}


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def notify_workflow_started(workflow_id: str):
    """Quick helper to notify workflow started"""
    event = {
        "workflow_id": workflow_id,
        "event_type": "status_change",
        "step": "workflow_started",
        "is_start": True
    }
    return dispatch_workflow_notification(event)


def notify_step_completed(workflow_id: str, step_name: str, next_step_name: str):
    """Quick helper to notify step completed"""
    event = {
        "workflow_id": workflow_id,
        "event_type": "step_complete",
        "step_name": step_name,
        "next_step_name": next_step_name,
        "status": "completed"
    }
    return dispatch_workflow_notification(event)


def notify_workflow_completed(workflow_id: str, summary: str = ""):
    """Quick helper to notify workflow completed"""
    event = {
        "workflow_id": workflow_id,
        "event_type": "status_change",
        "step": "workflow_complete",
        "summary": summary
    }
    return dispatch_workflow_notification(event)


def notify_workflow_needs_review(workflow_id: str):
    """Quick helper to notify workflow needs review"""
    event = {
        "workflow_id": workflow_id,
        "event_type": "status_change",
        "status": "pending_review"
    }
    return dispatch_workflow_notification(event)


def notify_workflow_failed(workflow_id: str):
    """Quick helper to notify workflow failed"""
    event = {
        "workflow_id": workflow_id,
        "event_type": "status_change",
        "status": "failed"
    }
    return dispatch_workflow_notification(event)


# ============================================================================
# BATCH NOTIFICATION CLEANUP (Maintenance)
# ============================================================================

def cleanup_old_notifications(days: int = 30) -> int:
    """
    Remove read notifications older than specified days
    
    Keeps database size manageable while preserving recent history.
    
    Args:
        days: Number of days to retain (default: 30)
        
    Returns:
        Number of notifications deleted
    """
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    with get_session_context() as session:
        deleted_count = session.query(PortalNotification).filter(
            PortalNotification.is_read == True,
            PortalNotification.created_at < cutoff_date
        ).delete()
        
        session.commit()
        
        print(f"🧹 Cleaned up {deleted_count} old notifications (older than {days} days)")
        return deleted_count


if __name__ == "__main__":
    # Test notification dispatch
    print("🔥 Testing Notification Dispatcher...")
    
    test_event = {
        "workflow_id": "test_workflow_123",
        "event_type": "status_change",
        "step": "workflow_started",
        "is_start": True
    }
    
    result = dispatch_workflow_notification(test_event)
    print(f"Result: {result}")
