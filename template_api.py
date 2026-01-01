"""
🔥 CODEX DOMINION - TEMPLATE MANAGEMENT API 🔥
===============================================
Complete Template System with CRUD, Versioning, and Approval Flow

Features:
- Template Editor (create/update templates)
- Template Approval Flow (submit/approve/reject)
- Template Versioning (create versions, deprecate old)
- AI Block Testing (preview AI outputs)
- Template Selection Logic (AI recommendations)
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Blueprint, request, jsonify
from sqlalchemy import desc, or_, and_

from db import SessionLocal
from models import (
    WorkflowTemplate, Council, User, Tenant,
    TemplateStatus
)


# Create Blueprint
template_bp = Blueprint('template', __name__)


def register_template_routes(app):
    """
    Register template routes with Flask app
    
    Usage in flask_dashboard.py:
        from template_api import register_template_routes
        register_template_routes(app)
    """
    app.register_blueprint(template_bp, url_prefix='/api')
    print("✅ Template Management API routes registered")


# ============================================================================
# TEMPLATE CRUD
# ============================================================================

@template_bp.route('/templates', methods=['GET'])
def list_templates():
    """
    List workflow templates
    
    Query params:
    - category: Filter by category
    - status: Filter by status (draft, pending_review, approved, etc.)
    - council_id: Filter by assigned council
    - is_active: Filter by active status (default true)
    - include_deprecated: Include deprecated versions (default false)
    """
    category = request.args.get('category')
    status = request.args.get('status')
    council_id = request.args.get('council_id')
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    include_deprecated = request.args.get('include_deprecated', 'false').lower() == 'true'
    
    session = SessionLocal()
    try:
        query = session.query(WorkflowTemplate)
        
        if is_active:
            query = query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=TemplateStatus[status.upper()])
        if council_id:
            query = query.filter_by(assigned_council_id=council_id)
        if not include_deprecated:
            query = query.filter(WorkflowTemplate.status != TemplateStatus.DEPRECATED)
        
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


@template_bp.route('/templates', methods=['POST'])
def create_template():
    """
    Create a new workflow template
    
    Request body (Template Schema):
    {
        "name": "Launch Black Friday Campaign",
        "description": "Complete campaign for Black Friday",
        "category": "marketing",
        "icon": "campaign",
        "tags": ["seasonal", "campaign", "black-friday"],
        "workflow_type_id": "marketing.seasonal_campaign",
        
        "input_fields": [
            {"key": "store_id", "label": "Store", "type": "select", 
             "required": true, "help_text": "Select your store"},
            {"key": "discount_percent", "label": "Discount %", "type": "number",
             "default": 20, "required": true}
        ],
        
        "ai_blocks": [
            {"id": "email", "name": "Email Sequence",
             "prompt_template": "Create Black Friday email sequence for {{store_name}} with {{discount_percent}}% discount",
             "output_schema": {"type": "array", "items": {"type": "object"}},
             "dependencies": ["store_id", "discount_percent"]}
        ],
        
        "execution_steps": [
            {"order": 1, "action": "generate_campaign", "config": {"type": "email"}},
            {"order": 2, "action": "deploy_landing_page", "dependencies": ["generate_campaign"]}
        ],
        
        "assigned_council_id": "council_media",
        "risk_flags": ["public_facing", "time_sensitive"],
        "auto_approval_rules": {"trusted_users_only": true}
    }
    """
    data = request.json
    
    required = ['name', 'workflow_type_id', 'category', 'created_by_user_id']
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    
    session = SessionLocal()
    try:
        template = WorkflowTemplate(
            id=f"template_{uuid.uuid4().hex[:12]}",
            workflow_type_id=data['workflow_type_id'],
            name=data['name'],
            description=data.get('description'),
            category=data['category'],
            icon=data.get('icon'),
            tags=data.get('tags', []),
            # New schema fields
            input_fields=data.get('input_fields', []),
            ai_blocks=data.get('ai_blocks', []),
            execution_steps=data.get('execution_steps', []),
            assigned_council_id=data.get('assigned_council_id'),
            risk_flags=data.get('risk_flags', []),
            auto_approval_rules=data.get('auto_approval_rules'),
            # Creator
            created_by_user_id=data['created_by_user_id'],
            # Status
            status=TemplateStatus.DRAFT,
            version=1,
            is_active=False
        )
        session.add(template)
        session.commit()
        
        print(f"✅ Created template: {template.id} ({template.name})")
        
        return jsonify({
            "success": True,
            "template": template.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id: str):
    """Get template details including version history"""
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        # Get version history
        versions = []
        if template.parent_template_id:
            # Get all versions
            current = template
            while current.parent_template_id:
                parent = session.query(WorkflowTemplate).filter_by(
                    id=current.parent_template_id
                ).first()
                if parent:
                    versions.insert(0, {
                        "id": parent.id,
                        "version": parent.version,
                        "status": parent.status.value,
                        "created_at": parent.created_at.isoformat()
                    })
                    current = parent
                else:
                    break
        
        versions.append({
            "id": template.id,
            "version": template.version,
            "status": template.status.value,
            "created_at": template.created_at.isoformat()
        })
        
        # Check if there's a newer version
        if template.latest_version_id and template.latest_version_id != template.id:
            newer = session.query(WorkflowTemplate).filter_by(
                id=template.latest_version_id
            ).first()
            if newer:
                versions.append({
                    "id": newer.id,
                    "version": newer.version,
                    "status": newer.status.value,
                    "created_at": newer.created_at.isoformat()
                })
        
        return jsonify({
            "template": template.to_dict(),
            "versions": versions
        }), 200
        
    except Exception as e:
        print(f"❌ Error fetching template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>', methods=['PATCH'])
def update_template(template_id: str):
    """
    Update template (only in DRAFT status)
    
    Can update any field from the template schema
    """
    data = request.json
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        # Only drafts can be edited
        if template.status != TemplateStatus.DRAFT:
            return jsonify({
                "error": f"Cannot edit template in status: {template.status.value}. Create a new version instead."
            }), 400
        
        # Update fields
        updatable = [
            'name', 'description', 'category', 'icon', 'tags',
            'input_fields', 'ai_blocks', 'execution_steps',
            'assigned_council_id', 'risk_flags', 'auto_approval_rules'
        ]
        
        for field in updatable:
            if field in data:
                setattr(template, field, data[field])
        
        template.updated_at = datetime.utcnow()
        session.commit()
        
        print(f"✅ Updated template: {template_id}")
        
        return jsonify({
            "success": True,
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error updating template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id: str):
    """Delete template (soft delete - mark as inactive)"""
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        template.is_active = False
        template.updated_at = datetime.utcnow()
        session.commit()
        
        print(f"✅ Deleted template: {template_id}")
        
        return jsonify({"success": True, "message": "Template deleted"}), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# TEMPLATE APPROVAL FLOW
# ============================================================================

@template_bp.route('/templates/<template_id>/submit', methods=['POST'])
def submit_template_for_approval(template_id: str):
    """
    Submit template for council approval
    
    Request body:
    {
        "council_id": "council_xxx" (optional - uses assigned_council_id if not provided)
    }
    """
    data = request.json or {}
    council_id = data.get('council_id')
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        if template.status != TemplateStatus.DRAFT:
            return jsonify({
                "error": f"Cannot submit template in status: {template.status.value}"
            }), 400
        
        # Use provided council or assigned council
        if council_id:
            template.assigned_council_id = council_id
        elif not template.assigned_council_id:
            return jsonify({"error": "No council assigned to template"}), 400
        
        template.status = TemplateStatus.PENDING_REVIEW
        template.updated_at = datetime.utcnow()
        session.commit()
        
        # TODO: Send notification to council members
        
        print(f"✅ Submitted template {template_id} to {template.assigned_council_id}")
        
        return jsonify({
            "success": True,
            "message": "Template submitted for approval",
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error submitting template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>/approve', methods=['POST'])
def approve_template(template_id: str):
    """
    Approve template (council action)
    
    Request body:
    {
        "council_id": "council_xxx",
        "user_id": "user_xxx",
        "is_pre_approved": false (optional - marks template as instant-run)
    }
    """
    data = request.json
    
    if not data.get('council_id') or not data.get('user_id'):
        return jsonify({"error": "council_id and user_id required"}), 400
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        if template.status != TemplateStatus.PENDING_REVIEW:
            return jsonify({
                "error": f"Cannot approve template in status: {template.status.value}"
            }), 400
        
        # Approve
        template.approve(
            council_id=data['council_id'],
            user_id=data['user_id']
        )
        
        # Set pre-approval flag if specified
        if data.get('is_pre_approved'):
            template.is_pre_approved = True
        
        session.commit()
        
        print(f"✅ Approved template {template_id} (pre-approved: {template.is_pre_approved})")
        
        return jsonify({
            "success": True,
            "message": "Template approved",
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error approving template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>/reject', methods=['POST'])
def reject_template(template_id: str):
    """
    Reject template (council action)
    
    Request body:
    {
        "reason": "Rejection reason"
    }
    """
    data = request.json
    
    if not data.get('reason'):
        return jsonify({"error": "Rejection reason required"}), 400
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        template.reject(reason=data['reason'])
        session.commit()
        
        print(f"✅ Rejected template {template_id}")
        
        return jsonify({
            "success": True,
            "message": "Template rejected",
            "template": template.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error rejecting template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# TEMPLATE VERSIONING
# ============================================================================

@template_bp.route('/templates/<template_id>/create-version', methods=['POST'])
def create_template_version(template_id: str):
    """
    Create a new version of an approved template
    
    The new version starts as DRAFT and must be approved separately.
    Old workflows continue using the old version.
    """
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        if template.status != TemplateStatus.APPROVED:
            return jsonify({
                "error": "Can only create versions from approved templates"
            }), 400
        
        new_version = template.create_new_version(session)
        session.commit()
        
        print(f"✅ Created v{new_version.version} of template {template_id}")
        
        return jsonify({
            "success": True,
            "message": f"Created version {new_version.version}",
            "new_template": new_version.to_dict(),
            "previous_template": template.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating template version: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@template_bp.route('/templates/<template_id>/deprecate', methods=['POST'])
def deprecate_template(template_id: str):
    """Mark template as deprecated (superseded by newer version)"""
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        template.deprecate()
        session.commit()
        
        print(f"✅ Deprecated template {template_id}")
        
        return jsonify({
            "success": True,
            "message": "Template deprecated"
        }), 200
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error deprecating template: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# AI BLOCK TESTING
# ============================================================================

@template_bp.route('/templates/<template_id>/test-ai-block', methods=['POST'])
def test_ai_block(template_id: str):
    """
    Test an AI block with sample inputs
    
    Request body:
    {
        "block_id": "description",
        "inputs": {"product_name": "Wireless Mouse", "price": 29.99}
    }
    
    Returns:
    {
        "preview": "Your generated output here...",
        "tokens_used": 150
    }
    """
    data = request.json
    
    if not data.get('block_id') or not data.get('inputs'):
        return jsonify({"error": "block_id and inputs required"}), 400
    
    session = SessionLocal()
    try:
        template = session.query(WorkflowTemplate).filter_by(id=template_id).first()
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        # Find the AI block
        block = next((b for b in template.ai_blocks if b['id'] == data['block_id']), None)
        if not block:
            return jsonify({"error": f"AI block '{data['block_id']}' not found"}), 404
        
        # Replace variables in prompt template
        prompt = block['prompt_template']
        for key, value in data['inputs'].items():
            prompt = prompt.replace(f"{{{{{key}}}}}", str(value))
        
        # TODO: Call actual AI service (OpenAI, etc.)
        # For now, return mock preview
        preview = f"[AI PREVIEW] Generated content for: {prompt[:100]}..."
        
        return jsonify({
            "success": True,
            "preview": preview,
            "prompt_used": prompt,
            "tokens_used": 150  # Mock value
        }), 200
        
    except Exception as e:
        print(f"❌ Error testing AI block: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# AI TEMPLATE SELECTION LOGIC
# ============================================================================

@template_bp.route('/templates/recommend', methods=['POST'])
def recommend_templates():
    """
    Get AI-recommended templates for a tenant
    
    Request body:
    {
        "tenant_id": "tenant_xxx",
        "context": {
            "store_performance": {...},
            "product_count": 50,
            "recent_workflows": [...]
        }
    }
    
    Returns ranked list of templates with relevance scores
    """
    data = request.json
    
    if not data.get('tenant_id'):
        return jsonify({"error": "tenant_id required"}), 400
    
    tenant_id = data['tenant_id']
    context = data.get('context', {})
    
    session = SessionLocal()
    try:
        # Get all approved templates
        templates = session.query(WorkflowTemplate).filter(
            and_(
                WorkflowTemplate.status == TemplateStatus.APPROVED,
                WorkflowTemplate.is_active == True
            )
        ).all()
        
        # Score and rank templates based on context
        recommendations = []
        for template in templates:
            score = calculate_template_relevance(template, context)
            if score > 0:
                recommendations.append({
                    "template": template.to_dict(),
                    "relevance_score": score,
                    "reasoning": generate_recommendation_reasoning(template, context)
                })
        
        # Sort by relevance
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            "recommendations": recommendations[:10],  # Top 10
            "total_templates_evaluated": len(templates)
        }), 200
        
    except Exception as e:
        print(f"❌ Error recommending templates: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


def calculate_template_relevance(template: WorkflowTemplate, context: Dict) -> float:
    """Calculate relevance score (0-1) for a template given tenant context"""
    score = 0.0
    
    # Store performance factors
    if context.get('low_conversion') and 'conversion' in template.name.lower():
        score += 0.3
    if context.get('low_traffic') and 'seo' in template.name.lower():
        score += 0.3
    
    # Catalog factors
    product_count = context.get('product_count', 0)
    if product_count < 10 and 'product' in template.category.lower():
        score += 0.4
    elif product_count > 100 and 'bundle' in template.name.lower():
        score += 0.2
    
    # Seasonal factors
    if context.get('upcoming_holiday') and 'seasonal' in (template.tags or []):
        score += 0.5
    
    # Usage history (popular templates)
    if template.usage_count > 50:
        score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0


def generate_recommendation_reasoning(template: WorkflowTemplate, context: Dict) -> str:
    """Generate human-readable reasoning for recommendation"""
    reasons = []
    
    if context.get('low_conversion'):
        reasons.append("Your conversion rate is below average")
    if context.get('product_count', 0) < 10:
        reasons.append("You have a small product catalog")
    if context.get('upcoming_holiday'):
        reasons.append(f"{context['upcoming_holiday']} is approaching")
    if template.usage_count > 50:
        reasons.append("This template is popular with other stores")
    
    if reasons:
        return ". ".join(reasons) + "."
    return "This template matches your store's needs."
