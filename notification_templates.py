"""
🔥 CODEX DOMINION - NOTIFICATION TEMPLATES 🔥
==============================================
Email and portal notification template rendering

Provides warm, clear, concise messaging for workflow lifecycle events.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from models import NotificationType


class NotificationTemplates:
    """
    Template renderer for workflow notifications
    
    Renders email and portal notifications with dynamic content
    based on workflow state and events.
    """
    
    BASE_PORTAL_URL = "https://codexdominion.app/portal"
    
    @classmethod
    def render(cls, 
               notification_type: NotificationType,
               workflow: Dict[str, Any],
               tenant: Dict[str, Any],
               user: Dict[str, Any],
               event: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Render notification template
        
        Args:
            notification_type: Type of notification
            workflow: Workflow data dict
            tenant: Tenant data dict
            user: User data dict
            event: Optional event data (for step_completed)
            
        Returns:
            Dict with 'subject' and 'body' keys
        """
        
        # Common template variables
        workflow_name = workflow.get('workflow_type_id', 'workflow').replace('_', ' ').title()
        user_name = user.get('name', 'there').split()[0]  # First name only
        workflow_id = workflow.get('id')
        portal_link = f"{cls.BASE_PORTAL_URL}/workflows/{workflow_id}"
        
        # Route to appropriate template
        if notification_type == NotificationType.WORKFLOW_STARTED:
            return cls._workflow_started(workflow_name, user_name, portal_link)
        
        elif notification_type == NotificationType.STEP_COMPLETED:
            step_name = event.get('step_name', 'Step') if event else 'Step'
            next_step = event.get('next_step_name', 'Next step') if event else 'Next step'
            return cls._step_completed(step_name, next_step, portal_link)
        
        elif notification_type == NotificationType.WORKFLOW_COMPLETED:
            summary = workflow.get('summary', 'Workflow completed successfully.')
            return cls._workflow_completed(workflow_name, summary, portal_link)
        
        elif notification_type == NotificationType.NEEDS_REVIEW:
            return cls._needs_review(workflow_name, user_name, portal_link)
        
        elif notification_type == NotificationType.WORKFLOW_FAILED:
            return cls._workflow_failed(workflow_name, portal_link)
        
        else:
            # Fallback generic notification
            return {
                "subject": f"Update: {workflow_name}",
                "body": f"Your {workflow_name} has been updated.\n\nView details:\n{portal_link}"
            }
    
    @staticmethod
    def _workflow_started(workflow_name: str, user_name: str, portal_link: str) -> Dict[str, str]:
        """Template: Workflow Started"""
        return {
            "subject": f"Your {workflow_name} has started",
            "body": f"""Hi {user_name},

Your {workflow_name} is now in progress.

We'll notify you as each step completes.

You can follow along here:
{portal_link}"""
        }
    
    @staticmethod
    def _step_completed(step_name: str, next_step: str, portal_link: str) -> Dict[str, str]:
        """Template: Step Completed"""
        return {
            "subject": f"{step_name} completed",
            "body": f"""Good news — {step_name} is complete.

Next up:
{next_step}

View progress:
{portal_link}"""
        }
    
    @staticmethod
    def _workflow_completed(workflow_name: str, summary: str, portal_link: str) -> Dict[str, str]:
        """Template: Workflow Completed"""
        return {
            "subject": f"Your {workflow_name} is complete",
            "body": f"""Your {workflow_name} has finished successfully.

Highlights:
{summary}

You can review everything here:
{portal_link}"""
        }
    
    @staticmethod
    def _needs_review(workflow_name: str, user_name: str, portal_link: str) -> Dict[str, str]:
        """Template: Workflow Needs Review"""
        return {
            "subject": f"Your review is needed: {workflow_name}",
            "body": f"""Hi {user_name},

Your {workflow_name} is ready for your review.

Please approve or request changes:
{portal_link}"""
        }
    
    @staticmethod
    def _workflow_failed(workflow_name: str, portal_link: str) -> Dict[str, str]:
        """Template: Workflow Failed"""
        return {
            "subject": f"We hit a snag in {workflow_name}",
            "body": f"""Something unexpected happened during {workflow_name}.

Our system has logged the issue and will attempt recovery.

You can check details here:
{portal_link}"""
        }
    
    @classmethod
    def render_portal_short(cls, 
                           notification_type: NotificationType,
                           workflow_name: str,
                           step_name: Optional[str] = None) -> str:
        """
        Render short notification for portal dropdown
        
        Returns concise single-line message for notification list.
        """
        
        if notification_type == NotificationType.WORKFLOW_STARTED:
            return f"Your {workflow_name} has started"
        
        elif notification_type == NotificationType.STEP_COMPLETED:
            return f"{step_name or 'Step'} completed"
        
        elif notification_type == NotificationType.WORKFLOW_COMPLETED:
            return f"Your {workflow_name} is complete"
        
        elif notification_type == NotificationType.NEEDS_REVIEW:
            return f"Review needed: {workflow_name}"
        
        elif notification_type == NotificationType.WORKFLOW_FAILED:
            return f"Issue in {workflow_name}"
        
        else:
            return f"Update: {workflow_name}"


# ============================================================================
# EMAIL SENDER UTILITY
# ============================================================================

def send_notification_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send notification email via SMTP
    
    Uses environment variables for SMTP configuration:
    - SMTP_HOST
    - SMTP_PORT
    - SMTP_USER
    - SMTP_PASS
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (plain text)
        
    Returns:
        True if sent successfully, False otherwise
    """
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    try:
        # SMTP configuration from environment
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        
        if not smtp_user or not smtp_pass:
            print("⚠️ SMTP credentials not configured - skipping email")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Plain text body
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        print(f"✅ Email sent to {to_email}: {subject}")
        return True
        
    except Exception as e:
        print(f"⚠️ Failed to send email to {to_email}: {e}")
        return False


# ============================================================================
# NOTIFICATION ICONS
# ============================================================================

NOTIFICATION_ICONS = {
    NotificationType.WORKFLOW_STARTED: "play",
    NotificationType.STEP_COMPLETED: "checkCircle",
    NotificationType.WORKFLOW_COMPLETED: "checkCircle",
    NotificationType.NEEDS_REVIEW: "alertCircle",
    NotificationType.WORKFLOW_FAILED: "xCircle"
}


def get_notification_icon(notification_type: NotificationType) -> str:
    """Get icon name for notification type"""
    return NOTIFICATION_ICONS.get(notification_type, "info")
