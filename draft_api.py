"""
🔥 CODEX DOMINION - WORKFLOW DRAFT API 🔥
==========================================
REST API endpoints for workflow drafts, templates, and AI proposals

Draft Mode enables users to:
- Create workflow proposals before execution
- Edit and preview workflows
- Submit for council review
- Convert approved drafts to workflows
- Use pre-approved templates
- Accept AI-generated proposals

Endpoints:
- GET /api/drafts - List drafts (with filters)
- POST /api/drafts - Create new draft
- GET /api/drafts/:id - Get draft details
- PATCH /api/drafts/:id - Update draft
- DELETE /api/drafts/:id - Discard draft
- POST /api/drafts/:id/submit - Submit for review
- POST /api/drafts/:id/convert - Convert to workflow (after approval)
- GET /api/templates - List templates
- GET /api/templates/:id - Get template details
- POST /api/templates/:id/use - Create draft from template
- GET /api/proposals - List AI proposals
- POST /api/proposals/:id/accept - Accept proposal (creates draft)
- POST /api/proposals/:id/dismiss - Dismiss proposal
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from flask import Blueprint, request, jsonify
from sqlalchemy import desc, or_

from db import SessionLocal
from models import (
    WorkflowDraft, WorkflowTemplate, AIWorkflowProposal,
    Workflow, User, Council, Tenant,
    DraftStatus, ProposalStatus, WorkflowStatus, WorkflowDecision
)
from notification_worker import notify_needs_review, notify_workflow_started


# Create Blueprint
draft_bp = Blueprint('draft', __name__)


def register_draft_routes(app):
    """
    Register draft routes with Flask app
    
    Usage in flask_dashboard.py:
        from draft_api import register_draft_routes
        register_draft_routes(app)
    """
    app.register_blueprint(draft_bp, url_prefix='/api')
    print("✅ Draft Mode API routes registered")


# ============================================================================
# DRAFT CRUD
# ============================================================================

@draft_bp.route('/drafts', methods=['GET'])
def list_drafts():
    """
    List workflow drafts
    
    Query params:
    - tenant_id: Filter by tenant
    - status: Filter by status (editing, pending_review, approved, etc.)
    - user_id: Filter by creator
    - limit: Max results (default 50)
    - offset: Pagination offset
    """
    tenant_id = request.args.get('tenant_id')
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    session = SessionLocal()
    try:
        query = session.query(WorkflowDraft)
        
        if tenant_id:
            query = query.filter_by(tenant_id=tenant_id)
        if status:
            query = query.filter_by(status=DraftStatus[status.upper()])
        if user_id:
            query = query.filter_by(created_by_user_id=user_id)
        
        # Exclude converted and discarded by default
        query = query.filter(
            WorkflowDraft.status.notin_([DraftStatus.CONVERTED, DraftStatus.DISCARDED])
        )
        
        total = query.count()
        drafts = query.order_by(desc(WorkflowDraft.updated_at)).limit(limit).offset(offset).all()
        
        return jsonify({
            "drafts": [d.to_dict() for d in drafts],
            "total": total,
            "limit": limit,
            "offset": offset
        }), 200
        
    except Exception as e:
        print(f"❌ Error listing drafts: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/drafts', methods=['POST'])
def create_draft():
    """
    Create a new workflow draft
    
    Request body:
    {
        "tenant_id": "tenant_xxx",
        "created_by_user_id": "user_xxx",
        "workflow_type_id": "social.generate_launch_campaign_for_store",
        "name": "Holiday Campaign",
        "purpose": "Launch holiday products",
        "inputs": {...},
        "from_template_id": "template_xxx" (optional)
    }
    """
    data = request.json
    
    required = ['tenant_id', 'created_by_user_id', 'workflow_type_id', 'name']
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    
    session = SessionLocal()
    try:
        draft = WorkflowDraft(
            id=f"draft_{uuid.uuid4().hex[:12]}",
            tenant_id=data['tenant_id'],
            created_by_user_id=data['created_by_user_id'],
            workflow_type_id=data['workflow_type_id'],
            name=data['name'],
            purpose=data.get('purpose'),
            inputs=data.get('inputs', {}),
            preview_data=data.get('preview_data', {}),
            expected_outputs=data.get('expected_outputs'),
            estimated_duration_minutes=data.get('estimated_duration_minutes'),
            required_approvals=data.get('required_approvals'),
            dependencies=data.get('dependencies'),
            created_from_template_id=data.get('from_template_id'),
            status=DraftStatus.EDITING
        )
        session.add(draft)
        session.commit()
        
        print(f"✅ Created draft: {draft.id} ({draft.name})")
        
        return jsonify({
            "success": True,
            "draft": draft.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/drafts/<draft_id>', methods=['GET'])
def get_draft(draft_id: str):
    """Get draft details"""
    session = SessionLocal()
    try:
        draft = session.query(WorkflowDraft).filter_by(id=draft_id).first()
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        
        # Get template info if created from template
        template_data = None
        if draft.created_from_template_id:
            template = session.query(WorkflowTemplate).filter_by(
                id=draft.created_from_template_id
            ).first()
            if template:
                template_data = template.to_dict()
        
        # Get proposal info if created from proposal
        proposal_data = None
        if draft.created_from_proposal_id:
            proposal = session.query(AIWorkflowProposal).filter_by(
                id=draft.created_from_proposal_id
            ).first()
            if proposal:
                proposal_data = proposal.to_dict()
        
        return jsonify({
            "draft": draft.to_dict(),
            "template": template_data,
            "proposal": proposal_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/drafts/<draft_id>', methods=['PATCH'])
def update_draft(draft_id: str):
    """
    Update draft fields
    
    Request body:
    {
        "name": "Updated name" (optional),
        "purpose": "Updated purpose" (optional),
        "inputs": {...} (optional),
        "preview_data": {...} (optional)
    }
    """
    data = request.json
    
    session = SessionLocal()
    try:
        draft = session.query(WorkflowDraft).filter_by(id=draft_id).first()
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        
        # Only allow edits if status is EDITING
        if draft.status != DraftStatus.EDITING:
            return jsonify({
                "error": f"Cannot edit draft in status: {draft.status.value}"
            }), 400
        
        # Update fields
        if 'name' in data:
            draft.name = data['name']
        if 'purpose' in data:
            draft.purpose = data['purpose']
        if 'inputs' in data:
            draft.inputs = data['inputs']
        if 'preview_data' in data:
            draft.preview_data = data['preview_data']
        
        draft.last_edited_at = datetime.utcnow()
        draft.updated_at = datetime.utcnow()
        
        session.commit()
        
        print(f"✅ Updated draft: {draft_id}")
        
        return jsonify({
            "success": True,
            "draft": draft.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error updating draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/drafts/<draft_id>', methods=['DELETE'])
def discard_draft(draft_id: str):
    """Discard draft (soft delete - sets status to DISCARDED)"""
    session = SessionLocal()
    try:
        draft = session.query(WorkflowDraft).filter_by(id=draft_id).first()
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        
        draft.status = DraftStatus.DISCARDED
        draft.updated_at = datetime.utcnow()
        session.commit()
        
        print(f"✅ Discarded draft: {draft_id}")
        
        return jsonify({"success": True, "message": "Draft discarded"}), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error discarding draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# DRAFT WORKFLOW (Submit, Approve, Convert)
# ============================================================================

@draft_bp.route('/drafts/<draft_id>/submit', methods=['POST'])
def submit_draft_for_review(draft_id: str):
    """
    Submit draft for council review
    
    Request body:
    {
        "council_id": "council_xxx" (optional - auto-routes if not provided)
    }
    """
    data = request.json or {}
    council_id = data.get('council_id')
    
    session = SessionLocal()
    try:
        draft = session.query(WorkflowDraft).filter_by(id=draft_id).first()
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        
        if draft.status != DraftStatus.EDITING:
            return jsonify({
                "error": f"Cannot submit draft in status: {draft.status.value}"
            }), 400
        
        # Auto-route to council if not specified
        if not council_id:
            from workflow_engine import get_council_for_workflow_type
            council_id = get_council_for_workflow_type(draft.workflow_type_id)
        
        # Update draft
        draft.status = DraftStatus.PENDING_REVIEW
        draft.assigned_council_id = council_id
        draft.updated_at = datetime.utcnow()
        
        session.commit()
        
        # Send notification
        if council_id:
            try:
                notify_needs_review(
                    workflow_id=draft_id,
                    summary={
                        "type": "draft_submission",
                        "draft_name": draft.name,
                        "council_id": council_id
                    }
                )
            except Exception as e:
                print(f"⚠️ Notification failed: {e}")
        
        print(f"✅ Submitted draft {draft_id} to {council_id or 'auto-routing'}")
        
        return jsonify({
            "success": True,
            "message": "Draft submitted for review",
            "draft": draft.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error submitting draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/drafts/<draft_id>/convert', methods=['POST'])
def convert_draft_to_workflow(draft_id: str):
    """
    Convert approved draft to actual workflow
    
    This creates a Workflow record and enqueues execution.
    Only works for drafts with status APPROVED or if from pre-approved template.
    
    Request body:
    {
        "auto_execute": true (optional, default true)
    }
    """
    data = request.json or {}
    auto_execute = data.get('auto_execute', True)
    
    session = SessionLocal()
    try:
        draft = session.query(WorkflowDraft).filter_by(id=draft_id).first()
        if not draft:
            return jsonify({"error": "Draft not found"}), 404
        
        # Check if conversion is allowed
        can_convert = (
            draft.status == DraftStatus.APPROVED or
            (draft.created_from_template_id and draft.template and draft.template.is_pre_approved)
        )
        
        if not can_convert:
            return jsonify({
                "error": f"Draft must be approved before conversion (current status: {draft.status.value})"
            }), 400
        
        if draft.status == DraftStatus.CONVERTED:
            return jsonify({
                "error": "Draft already converted",
                "workflow_id": draft.converted_to_workflow_id
            }), 400
        
        # Create workflow
        from workflow_engine import workflow_engine
        
        workflow_id = workflow_engine.create_workflow(
            workflow_type_id=draft.workflow_type_id,
            created_by_agent="draft_converter",  # Special agent ID
            inputs=draft.inputs or {},
            calculated_savings=draft.inputs.get('calculated_savings', {}),
            assigned_council_id=draft.assigned_council_id,
            auto_execute=auto_execute,
            auto_route_councils=False  # Already routed in draft
        )
        
        # Update draft
        draft.status = DraftStatus.CONVERTED
        draft.converted_to_workflow_id = workflow_id
        draft.converted_at = datetime.utcnow()
        draft.updated_at = datetime.utcnow()
        
        session.commit()
        
        print(f"✅ Converted draft {draft_id} to workflow {workflow_id}")
        
        return jsonify({
            "success": True,
            "message": "Draft converted to workflow",
            "workflow_id": workflow_id,
            "draft": draft.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error converting draft: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# TEMPLATES
# ============================================================================

@draft_bp.route('/templates', methods=['GET'])
def list_templates():
    """
    List workflow templates
    
    Query params:
    - category: Filter by category
    - workflow_type_id: Filter by workflow type
    - is_active: Filter by active status (default true)
    """
    category = request.args.get('category')
    workflow_type_id = request.args.get('workflow_type_id')
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    session = SessionLocal()
    try:
        query = session.query(WorkflowTemplate)
        
        if is_active:
            query = query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        if workflow_type_id:
            query = query.filter_by(workflow_type_id=workflow_type_id)
        
        templates = query.order_by(desc(WorkflowTemplate.usage_count)).all()
        
        return jsonify({
            "templates": [t.to_dict() for t in templates],
            "total": len(templates)
        }), 200
        
    except Exception as e:
        print(f"❌ Error listing templates: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id: str):
    """Get template details"""
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        return jsonify({"template": template.to_dict()}), 200
        
    except Exception as e:
        print(f"❌ Error fetching template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/templates/<template_id>/use', methods=['POST'])
def use_template(template_id: str):
    """
    Create a draft from a template
    
    Request body:
    {
        "tenant_id": "tenant_xxx",
        "user_id": "user_xxx",
        "name": "Optional custom name" (uses template name if not provided),
        "custom_inputs": {...} (optional overrides for default inputs)
    }
    """
    data = request.json
    
    if not data.get('tenant_id') or not data.get('user_id'):
        return jsonify({"error": "tenant_id and user_id required"}), 400
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        if not template.is_active:
            return jsonify({"error": "Template is inactive"}), 400
        
        # Merge default inputs with custom inputs
        inputs = dict(template.default_inputs or {})
        if data.get('custom_inputs'):
            inputs.update(data['custom_inputs'])
        
        # Create draft
        draft = WorkflowDraft(
            id=f"draft_{uuid.uuid4().hex[:12]}",
            tenant_id=data['tenant_id'],
            created_by_user_id=data['user_id'],
            workflow_type_id=template.workflow_type_id,
            name=data.get('name', template.name),
            purpose=template.description,
            inputs=inputs,
            expected_outputs=template.approved_structure,
            created_from_template_id=template_id,
            status=DraftStatus.EDITING
        )
        session.add(draft)
        
        # Update template usage
        template.increment_usage()
        
        session.commit()
        
        print(f"✅ Created draft from template {template_id}: {draft.id}")
        
        return jsonify({
            "success": True,
            "draft": draft.to_dict(),
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error using template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# AI PROPOSALS
# ============================================================================

@draft_bp.route('/proposals', methods=['GET'])
def list_proposals():
    """
    List AI workflow proposals
    
    Query params:
    - tenant_id: Filter by tenant (required)
    - status: Filter by status (default: pending)
    - priority: Filter by priority
    """
    tenant_id = request.args.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id required"}), 400
    
    status = request.args.get('status', 'pending')
    priority = request.args.get('priority')
    
    session = SessionLocal()
    try:
        query = session.query(AIWorkflowProposal).filter_by(tenant_id=tenant_id)
        
        if status:
            query = query.filter_by(status=ProposalStatus[status.upper()])
        if priority:
            query = query.filter_by(priority=priority)
        
        # Filter out expired proposals
        query = query.filter(
            or_(
                AIWorkflowProposal.expires_at.is_(None),
                AIWorkflowProposal.expires_at > datetime.utcnow()
            )
        )
        
        proposals = query.order_by(desc(AIWorkflowProposal.created_at)).all()
        
        return jsonify({
            "proposals": [p.to_dict() for p in proposals],
            "total": len(proposals)
        }), 200
        
    except Exception as e:
        print(f"❌ Error listing proposals: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/proposals/<proposal_id>/accept', methods=['POST'])
def accept_proposal(proposal_id: str):
    """
    Accept AI proposal and create draft
    
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
        proposal = session.query(AIWorkflowProposal).filter_by(id=proposal_id).first()
        if not proposal:
            return jsonify({"error": "Proposal not found"}), 404
        
        if proposal.status != ProposalStatus.PENDING:
            return jsonify({
                "error": f"Proposal already {proposal.status.value}"
            }), 400
        
        # Create draft from proposal
        draft = WorkflowDraft(
            id=f"draft_{uuid.uuid4().hex[:12]}",
            tenant_id=proposal.tenant_id,
            created_by_user_id=user_id,
            workflow_type_id=proposal.workflow_type_id,
            name=proposal.title,
            purpose=proposal.description,
            inputs=proposal.suggested_inputs or {},
            created_from_proposal_id=proposal_id,
            status=DraftStatus.EDITING
        )
        session.add(draft)
        
        # Update proposal
        proposal.status = ProposalStatus.ACCEPTED
        proposal.acted_on_at = datetime.utcnow()
        proposal.created_draft_id = draft.id
        
        session.commit()
        
        print(f"✅ Accepted proposal {proposal_id}, created draft {draft.id}")
        
        return jsonify({
            "success": True,
            "draft": draft.to_dict(),
            "proposal": proposal.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error accepting proposal: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@draft_bp.route('/proposals/<proposal_id>/dismiss', methods=['POST'])
def dismiss_proposal(proposal_id: str):
    """Dismiss AI proposal"""
    session = SessionLocal()
    try:
        proposal = session.query(AIWorkflowProposal).filter_by(id=proposal_id).first()
        if not proposal:
            return jsonify({"error": "Proposal not found"}), 404
        
        proposal.status = ProposalStatus.DISMISSED
        proposal.acted_on_at = datetime.utcnow()
        session.commit()
        
        print(f"✅ Dismissed proposal {proposal_id}")
        
        return jsonify({"success": True, "message": "Proposal dismissed"}), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error dismissing proposal: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
