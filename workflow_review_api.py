"""
🔥 CODEX DOMINION - WORKFLOW REVIEW & APPROVAL API 🔥
======================================================
REST API endpoints for workflow review, approval, and comment system

Implements the Council Seal governance architecture with human-in-the-loop decision making.

Endpoints:
- GET /api/workflows/:id/review - Get full review data
- POST /api/workflows/:id/approve - Approve workflow
- POST /api/workflows/:id/request-changes - Request changes
- POST /api/workflows/:id/resubmit - Resubmit after changes
- GET /api/workflows/:id/comments - Get comments
- POST /api/workflows/:id/comments - Add comment
- PATCH /api/workflows/:id/comments/:commentId/resolve - Resolve comment thread
- GET /api/workflows/:id/timeline - Get timeline events

Governance Features:
- Council member voting (if requires_majority_vote)
- Comment threads with markdown support
- Timeline event tracking
- Notification triggers on state changes
- Artifact display for review
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from db import SessionLocal, get_session_context
from models import (
    Workflow, WorkflowComment, WorkflowTimelineEvent, WorkflowArtifact,
    User, Council, CouncilMember, PortalNotification,
    WorkflowStatus, WorkflowDecision, CommentType, NotificationType
)
from notification_worker import (
    notify_workflow_completed,
    notify_needs_review
)


# Create Blueprint
workflow_review_bp = Blueprint('workflow_review', __name__)


def register_workflow_review_routes(app):
    """
    Register workflow review routes with Flask app
    
    Usage in flask_dashboard.py:
        from workflow_review_api import register_workflow_review_routes
        register_workflow_review_routes(app)
    """
    app.register_blueprint(workflow_review_bp, url_prefix='/api/workflows')
    print("✅ Workflow Review API routes registered")


# ============================================================================
# REVIEW DATA RETRIEVAL
# ============================================================================

@workflow_review_bp.route('/<workflow_id>/review', methods=['GET'])
def get_workflow_review(workflow_id: str):
    """
    Get complete workflow review data
    
    Returns:
    - Workflow details
    - Summary and AI analysis
    - Artifacts (launch posts, landing page, products, etc.)
    - Council information
    - Timeline events
    - Comments
    - Approval status
    """
    session = SessionLocal()
    try:
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404
        
        # Get council details
        council_data = None
        if workflow.assigned_council_id:
            council = session.query(Council).filter_by(id=workflow.assigned_council_id).first()
            if council:
                members = session.query(CouncilMember).filter_by(
                    council_id=council.id,
                    is_active=True
                ).all()
                council_data = {
                    "id": council.id,
                    "name": council.name,
                    "description": council.description,
                    "requires_majority_vote": council.config.get("oversight", {}).get("requires_majority_vote", False),
                    "min_votes": council.config.get("oversight", {}).get("min_votes", 1),
                    "members": [m.to_dict() for m in members]
                }
        
        # Get artifacts
        artifacts = session.query(WorkflowArtifact).filter_by(workflow_id=workflow_id).all()
        
        # Get timeline events
        timeline = session.query(WorkflowTimelineEvent).filter_by(
            workflow_id=workflow_id
        ).order_by(WorkflowTimelineEvent.created_at.desc()).all()
        
        # Get comments with threading
        comments = session.query(WorkflowComment).filter_by(
            workflow_id=workflow_id,
            parent_id=None  # Top-level comments only
        ).order_by(WorkflowComment.created_at.desc()).all()
        
        # Get creator details
        creator_name = "Unknown Agent"
        if workflow.creator:
            creator_name = workflow.creator.display_name or workflow.creator.name
        
        # Get reviewer details
        reviewer_data = None
        if workflow.reviewed_by_user_id:
            reviewer = session.query(User).filter_by(id=workflow.reviewed_by_user_id).first()
            if reviewer:
                reviewer_data = {
                    "id": reviewer.id,
                    "name": reviewer.name,
                    "email": reviewer.email,
                    "reviewed_at": workflow.reviewed_at.isoformat() if workflow.reviewed_at else None
                }
        
        return jsonify({
            "workflow": {
                "id": workflow.id,
                "workflow_type_id": workflow.workflow_type_id,
                "tenant_id": workflow.tenant_id,
                "status": workflow.status.value,
                "decision_status": workflow.decision_status.value if workflow.decision_status else "pending",
                "created_by": creator_name,
                "summary": workflow.summary,
                "inputs": workflow.inputs,
                "outputs": workflow.outputs,
                "calculated_savings": workflow.calculated_savings,
                "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
                "review_comment": workflow.review_comment,
                "resubmission_count": workflow.resubmission_count
            },
            "council": council_data,
            "artifacts": [a.to_dict() for a in artifacts],
            "timeline": [t.to_dict() for t in timeline],
            "comments": [c.to_dict() for c in comments],
            "reviewer": reviewer_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching workflow review: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# APPROVAL ACTIONS
# ============================================================================

@workflow_review_bp.route('/<workflow_id>/approve', methods=['POST'])
def approve_workflow(workflow_id: str):
    """
    Approve a workflow
    
    Request body:
    {
        "user_id": "user_xxx",
        "comment": "Optional approval comment",
        "suggested_edits": "Optional suggestions"
    }
    
    Actions:
    - Update workflow status to approved
    - Record timeline event
    - Send notifications to customer and team
    - Trigger next workflow if chained
    """
    data = request.json
    user_id = data.get('user_id')
    comment = data.get('comment', '')
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    session = SessionLocal()
    try:
        # Get workflow
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404
        
        # Get user
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update workflow
        workflow.status = WorkflowStatus.COMPLETED
        workflow.decision_status = WorkflowDecision.APPROVED
        workflow.reviewed_by_user_id = user_id
        workflow.reviewed_at = datetime.utcnow()
        workflow.review_comment = comment
        workflow.completed_at = datetime.utcnow()
        
        # Create timeline event
        timeline_event = WorkflowTimelineEvent(
            id=f"timeline_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            user_id=user_id,
            event_type="approved",
            title=f"Workflow approved by {user.name}",
            description=comment if comment else None,
            metadata={"decision": "approved"}
        )
        session.add(timeline_event)
        
        # Create system comment if comment provided
        if comment:
            system_comment = WorkflowComment(
                id=f"comment_{uuid.uuid4().hex[:12]}",
                workflow_id=workflow_id,
                user_id=user_id,
                comment_type=CommentType.REVIEWER,
                content=f"**Approved**: {comment}"
            )
            session.add(system_comment)
        
        session.commit()
        
        # Send notification (workflow completed)
        notify_workflow_completed(
            workflow_id=workflow_id,
            step_name="review_completed",
            summary={"decision": "approved", "comment": comment}
        )
        
        return jsonify({
            "success": True,
            "message": "Workflow approved successfully",
            "workflow": workflow.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error approving workflow: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@workflow_review_bp.route('/<workflow_id>/request-changes', methods=['POST'])
def request_changes(workflow_id: str):
    """
    Request changes to a workflow
    
    Request body:
    {
        "user_id": "user_xxx",
        "comment": "Required explanation of needed changes",
        "suggested_edits": "Optional specific suggestions",
        "risk_notes": "Optional internal risk assessment"
    }
    
    Actions:
    - Update workflow status to changes_requested
    - Record timeline event
    - Send notifications to customer
    - Pause workflow execution
    """
    data = request.json
    user_id = data.get('user_id')
    comment = data.get('comment', '')
    suggested_edits = data.get('suggested_edits', '')
    risk_notes = data.get('risk_notes', '')
    
    if not user_id or not comment:
        return jsonify({"error": "user_id and comment required"}), 400
    
    session = SessionLocal()
    try:
        # Get workflow
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404
        
        # Get user
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update workflow
        workflow.status = WorkflowStatus.PENDING_REVIEW  # Keep in review state
        workflow.decision_status = WorkflowDecision.NEEDS_REVISION
        workflow.reviewed_by_user_id = user_id
        workflow.reviewed_at = datetime.utcnow()
        workflow.review_comment = comment
        
        # Create timeline event
        timeline_event = WorkflowTimelineEvent(
            id=f"timeline_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            user_id=user_id,
            event_type="changes_requested",
            title=f"Changes requested by {user.name}",
            description=comment,
            metadata={
                "suggested_edits": suggested_edits,
                "risk_notes": risk_notes
            }
        )
        session.add(timeline_event)
        
        # Create reviewer comment
        comment_content = f"**Changes Requested**\n\n{comment}"
        if suggested_edits:
            comment_content += f"\n\n**Suggested Edits:**\n{suggested_edits}"
        
        reviewer_comment = WorkflowComment(
            id=f"comment_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            user_id=user_id,
            comment_type=CommentType.REVIEWER,
            content=comment_content
        )
        session.add(reviewer_comment)
        
        session.commit()
        
        # Send notification (needs review with changes)
        notify_needs_review(
            workflow_id=workflow_id,
            summary={"decision": "changes_requested", "comment": comment}
        )
        
        return jsonify({
            "success": True,
            "message": "Changes requested successfully",
            "workflow": workflow.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error requesting changes: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@workflow_review_bp.route('/<workflow_id>/resubmit', methods=['POST'])
def resubmit_workflow(workflow_id: str):
    """
    Resubmit workflow after making changes
    
    Request body:
    {
        "user_id": "user_xxx",
        "comment": "Optional description of changes made"
    }
    
    Actions:
    - Update workflow status back to pending_review
    - Increment resubmission_count
    - Record timeline event
    - Send notifications to reviewers
    """
    data = request.json
    user_id = data.get('user_id')
    comment = data.get('comment', '')
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    session = SessionLocal()
    try:
        # Get workflow
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404
        
        # Get user
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Update workflow
        workflow.status = WorkflowStatus.PENDING_REVIEW
        workflow.decision_status = WorkflowDecision.PENDING
        workflow.resubmission_count += 1
        
        # Create timeline event
        timeline_event = WorkflowTimelineEvent(
            id=f"timeline_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            user_id=user_id,
            event_type="resubmitted",
            title=f"Workflow resubmitted by {user.name}",
            description=comment if comment else "Workflow updated and resubmitted for review",
            metadata={"resubmission_count": workflow.resubmission_count}
        )
        session.add(timeline_event)
        
        # Create customer comment if provided
        if comment:
            customer_comment = WorkflowComment(
                id=f"comment_{uuid.uuid4().hex[:12]}",
                workflow_id=workflow_id,
                user_id=user_id,
                comment_type=CommentType.CUSTOMER,
                content=f"**Resubmitted for Review**\n\n{comment}"
            )
            session.add(customer_comment)
        
        session.commit()
        
        # Send notification (back to needs review)
        notify_needs_review(
            workflow_id=workflow_id,
            summary={"event": "resubmitted", "comment": comment}
        )
        
        return jsonify({
            "success": True,
            "message": "Workflow resubmitted successfully",
            "workflow": workflow.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error resubmitting workflow: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# COMMENT SYSTEM
# ============================================================================

@workflow_review_bp.route('/<workflow_id>/comments', methods=['GET'])
def get_comments(workflow_id: str):
    """
    Get all comments for a workflow
    
    Query params:
    - filter: all | reviewer | customer | system
    """
    filter_type = request.args.get('filter', 'all')
    
    session = SessionLocal()
    try:
        query = session.query(WorkflowComment).filter_by(
            workflow_id=workflow_id,
            parent_id=None  # Top-level only
        )
        
        # Apply filter
        if filter_type == 'reviewer':
            query = query.filter_by(comment_type=CommentType.REVIEWER)
        elif filter_type == 'customer':
            query = query.filter_by(comment_type=CommentType.CUSTOMER)
        elif filter_type == 'system':
            query = query.filter_by(comment_type=CommentType.SYSTEM)
        
        comments = query.order_by(WorkflowComment.created_at.desc()).all()
        
        return jsonify({
            "comments": [c.to_dict() for c in comments],
            "total": len(comments)
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching comments: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@workflow_review_bp.route('/<workflow_id>/comments', methods=['POST'])
def add_comment(workflow_id: str):
    """
    Add a comment to a workflow
    
    Request body:
    {
        "user_id": "user_xxx",
        "content": "Comment text (markdown supported)",
        "parent_id": "comment_xxx" (optional, for replies),
        "comment_type": "reviewer" | "customer" | "system"
    }
    """
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content', '').strip()
    parent_id = data.get('parent_id')
    comment_type = data.get('comment_type', 'customer')
    
    if not user_id or not content:
        return jsonify({"error": "user_id and content required"}), 400
    
    session = SessionLocal()
    try:
        # Verify workflow exists
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404
        
        # Verify user exists
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Create comment
        comment = WorkflowComment(
            id=f"comment_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            user_id=user_id,
            parent_id=parent_id,
            comment_type=CommentType[comment_type.upper()],
            content=content
        )
        session.add(comment)
        
        # Create timeline event for top-level comments
        if not parent_id:
            timeline_event = WorkflowTimelineEvent(
                id=f"timeline_{uuid.uuid4().hex[:12]}",
                workflow_id=workflow_id,
                user_id=user_id,
                event_type="comment_added",
                title=f"Comment by {user.name}",
                description=content[:100] + "..." if len(content) > 100 else content
            )
            session.add(timeline_event)
        
        session.commit()
        
        return jsonify({
            "success": True,
            "comment": comment.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding comment: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@workflow_review_bp.route('/<workflow_id>/comments/<comment_id>/resolve', methods=['PATCH'])
def resolve_comment(workflow_id: str, comment_id: str):
    """
    Resolve a comment thread
    
    Request body:
    {
        "user_id": "user_xxx"
    }
    """
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    session = SessionLocal()
    try:
        comment = session.query(WorkflowComment).filter_by(
            id=comment_id,
            workflow_id=workflow_id
        ).first()
        
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Mark as resolved
        comment.is_resolved = True
        comment.resolved_by_user_id = user_id
        comment.resolved_at = datetime.utcnow()
        
        session.commit()
        
        return jsonify({
            "success": True,
            "comment": comment.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error resolving comment: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# TIMELINE
# ============================================================================

@workflow_review_bp.route('/<workflow_id>/timeline', methods=['GET'])
def get_timeline(workflow_id: str):
    """
    Get workflow timeline events
    """
    session = SessionLocal()
    try:
        events = session.query(WorkflowTimelineEvent).filter_by(
            workflow_id=workflow_id
        ).order_by(WorkflowTimelineEvent.created_at.desc()).all()
        
        return jsonify({
            "events": [e.to_dict() for e in events],
            "total": len(events)
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching timeline: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
