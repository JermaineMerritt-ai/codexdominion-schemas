"""
Automation Library API

REST API for browsing and enabling pre-built automation templates.

Endpoints:
- List templates by category (1)
- Get template details (1)
- Enable template (create automation from template) (1)
- Get AI suggestions for tenant (1)
- Get tenant's enabled automations from library (1)

Integration:
    from automation_library_api import register_automation_library_routes
    register_automation_library_routes(app)
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import desc, func
from db import SessionLocal
from models import (
    AutomationTemplate, AutomationRule, Tenant,
    TriggerType, ActionType, RiskLevel
)

library_bp = Blueprint('automation_library', __name__, url_prefix='/api/automation-library')


# ============================================================================
# LIBRARY BROWSING
# ============================================================================

@library_bp.route('/templates', methods=['GET'])
def list_templates():
    """
    List automation templates from the library.
    
    Query params:
    - category: Filter by category (Store, Marketing, Website, Customer Behavior, Analytics)
    - featured: Show only featured templates (true/false)
    - active: Show only active templates (default: true)
    
    Returns:
    {
      "templates": [...],
      "categories": ["Store", "Marketing", "Website", "Customer Behavior", "Analytics"],
      "count": 20
    }
    """
    session = SessionLocal()
    try:
        query = session.query(AutomationTemplate)
        
        # Filter by active status (default true)
        active = request.args.get('active', 'true')
        if active.lower() == 'true':
            query = query.filter(AutomationTemplate.active == True)
        
        # Filter by category
        category = request.args.get('category')
        if category:
            query = query.filter(AutomationTemplate.category == category)
        
        # Filter by featured
        featured = request.args.get('featured')
        if featured and featured.lower() == 'true':
            query = query.filter(AutomationTemplate.featured == True)
        
        # Order by popularity and featured status
        query = query.order_by(
            desc(AutomationTemplate.featured),
            desc(AutomationTemplate.popularity_score)
        )
        
        templates = query.all()
        
        # Get all unique categories
        all_categories = session.query(AutomationTemplate.category).distinct().all()
        categories = [cat[0] for cat in all_categories]
        
        return jsonify({
            "templates": [t.to_dict() for t in templates],
            "categories": categories,
            "count": len(templates)
        }), 200
        
    finally:
        session.close()


@library_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """
    Get detailed information about a specific template.
    
    Returns:
    {
      "template": {...},
      "usage_count": 150,
      "avg_success_rate": 0.95,
      "estimated_value": "2 hours/week saved"
    }
    """
    session = SessionLocal()
    try:
        template = session.query(AutomationTemplate).filter_by(id=template_id).first()
        
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        # Count how many automations were created from this template
        # (This would need a template_id field in AutomationRule to track properly)
        usage_count = 0  # Placeholder
        
        # Calculate estimated value based on template type
        estimated_value = None
        if template.avg_value_generated:
            estimated_value = f"${template.avg_value_generated:.0f}/month"
        elif template.category == "Store":
            estimated_value = "2-5 hours/week saved"
        elif template.category == "Marketing":
            estimated_value = "3-8 hours/week saved"
        elif template.category == "Customer Behavior":
            estimated_value = "10-20% conversion increase"
        
        return jsonify({
            "template": template.to_dict(),
            "usage_count": usage_count,
            "avg_success_rate": template.success_rate or 0.90,
            "estimated_value": estimated_value
        }), 200
        
    finally:
        session.close()


# ============================================================================
# TEMPLATE ENABLEMENT
# ============================================================================

@library_bp.route('/templates/<template_id>/enable', methods=['POST'])
def enable_template(template_id):
    """
    Enable a template by creating an automation from it.
    
    Body:
    {
      "tenant_id": "tenant_123",
      "config": {
        "platforms": ["Instagram", "TikTok"],
        "tone": "Bold",
        "post_count": 5
      },
      "created_by_user_id": "user_456",
      "submit_for_approval": false
    }
    
    Returns:
    {
      "automation": {...},
      "message": "Automation enabled successfully" | "Submitted for council approval"
    }
    """
    session = SessionLocal()
    try:
        template = session.query(AutomationTemplate).filter_by(id=template_id).first()
        
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        if not template.active:
            return jsonify({"error": "Template is not active"}), 400
        
        data = request.get_json()
        tenant_id = data.get('tenant_id')
        user_config = data.get('config', {})
        created_by_user_id = data.get('created_by_user_id')
        submit_for_approval = data.get('submit_for_approval', False)
        
        if not tenant_id:
            return jsonify({"error": "tenant_id is required"}), 400
        
        # Validate configuration against schema
        validation_errors = validate_config(template.config_schema, user_config)
        if validation_errors:
            return jsonify({"error": "Configuration validation failed", "details": validation_errors}), 400
        
        # Create automation from template
        automation = template.create_automation_from_template(
            tenant_id=tenant_id,
            user_config=user_config,
            created_by_user_id=created_by_user_id
        )
        
        # If requires approval and submit_for_approval is True, disable initially
        if template.requires_approval and submit_for_approval:
            automation.enabled = False
            message = "Automation submitted for council approval"
        else:
            message = "Automation enabled successfully"
        
        session.add(automation)
        session.commit()
        session.refresh(automation)
        
        # Update template popularity
        template.popularity_score = (template.popularity_score or 0) + 1
        session.commit()
        
        return jsonify({
            "automation": automation.to_dict(),
            "message": message
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@library_bp.route('/templates/<template_id>/configure', methods=['POST'])
def preview_configuration(template_id):
    """
    Preview what an automation will look like with the provided configuration.
    Does not create the automation.
    
    Body:
    {
      "config": {
        "platforms": ["Instagram"],
        "tone": "Bold"
      }
    }
    
    Returns:
    {
      "preview": {
        "name": "...",
        "trigger_config": {...},
        "action_config": {...},
        "summary": "When ... occurs, ..."
      }
    }
    """
    session = SessionLocal()
    try:
        template = session.query(AutomationTemplate).filter_by(id=template_id).first()
        
        if not template:
            return jsonify({"error": "Template not found"}), 404
        
        data = request.get_json()
        user_config = data.get('config', {})
        
        # Merge configs
        trigger_config = template.default_trigger_config.copy()
        action_config = template.default_action_config.copy()
        
        for field in template.config_schema:
            key = field.get('key')
            if key in user_config:
                target = field.get('target', 'action_config')
                if target == 'trigger_config':
                    trigger_config[key] = user_config[key]
                else:
                    action_config[key] = user_config[key]
        
        # Generate plain English summary
        summary = generate_summary(
            template.trigger_type,
            trigger_config,
            template.action_type,
            action_config
        )
        
        return jsonify({
            "preview": {
                "name": template.name,
                "trigger_config": trigger_config,
                "action_config": action_config,
                "conditions": template.default_conditions,
                "summary": summary
            }
        }), 200
        
    finally:
        session.close()


# ============================================================================
# AI SUGGESTIONS
# ============================================================================

@library_bp.route('/suggestions', methods=['POST'])
def get_ai_suggestions():
    """
    Get AI-suggested automation templates for a tenant based on their context.
    
    Body:
    {
      "tenant_id": "tenant_123",
      "context": {
        "product_count": 2,
        "recent_campaigns": 0,
        "store_age_days": 45,
        "traffic_trend": "declining"
      }
    }
    
    Returns:
    {
      "suggestions": [
        {
          "template": {...},
          "relevance_score": 0.95,
          "message": "Your product catalog is low. Enable auto-generation?",
          "estimated_impact": "Save 2-5 hours/week"
        }
      ]
    }
    """
    session = SessionLocal()
    try:
        data = request.get_json()
        tenant_id = data.get('tenant_id')
        context = data.get('context', {})
        
        if not tenant_id:
            return jsonify({"error": "tenant_id is required"}), 400
        
        # Find templates that should be suggested
        templates = session.query(AutomationTemplate).filter(
            AutomationTemplate.active == True,
            AutomationTemplate.ai_enhanced == True
        ).all()
        
        suggestions = []
        
        for template in templates:
            if template.should_suggest_to_tenant(context):
                # Calculate relevance score based on context match
                relevance_score = calculate_relevance(template, context)
                
                # Get suggestion message from template
                message = template.ai_suggestion_rules.get('suggestion_message', 
                    f"Consider enabling {template.name}")
                
                # Estimate impact
                estimated_impact = None
                if template.avg_value_generated:
                    estimated_impact = f"${template.avg_value_generated:.0f}/month"
                elif template.category == "Store":
                    estimated_impact = "Save 2-5 hours/week"
                elif template.category == "Marketing":
                    estimated_impact = "Increase engagement 15-30%"
                
                suggestions.append({
                    "template": template.to_dict(),
                    "relevance_score": relevance_score,
                    "message": message,
                    "estimated_impact": estimated_impact
                })
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            "suggestions": suggestions[:5],  # Top 5 suggestions
            "count": len(suggestions)
        }), 200
        
    finally:
        session.close()


@library_bp.route('/tenant/<tenant_id>/enabled', methods=['GET'])
def get_tenant_enabled_automations(tenant_id):
    """
    Get all automations enabled by this tenant from the library.
    
    Returns:
    {
      "automations": [...],
      "count": 5,
      "categories_used": ["Store", "Marketing"]
    }
    """
    session = SessionLocal()
    try:
        # Get all automations for this tenant
        automations = session.query(AutomationRule).filter(
            AutomationRule.tenant_id == tenant_id
        ).order_by(desc(AutomationRule.created_at)).all()
        
        # Get unique categories
        categories_used = list(set([a.category for a in automations if a.category]))
        
        return jsonify({
            "automations": [a.to_dict() for a in automations],
            "count": len(automations),
            "categories_used": categories_used
        }), 200
        
    finally:
        session.close()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_config(config_schema, user_config):
    """
    Validate user configuration against schema.
    
    Args:
        config_schema: List of field definitions
        user_config: User-provided configuration
    
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    for field in config_schema:
        key = field.get('key')
        required = field.get('required', False)
        field_type = field.get('type')
        
        # Check required fields
        if required and key not in user_config:
            errors.append(f"Missing required field: {key}")
            continue
        
        if key not in user_config:
            continue
        
        value = user_config[key]
        
        # Type validation
        if field_type == 'number' and not isinstance(value, (int, float)):
            errors.append(f"{key} must be a number")
        elif field_type == 'select' and value not in field.get('options', []):
            errors.append(f"{key} must be one of: {', '.join(field.get('options', []))}")
        elif field_type == 'multiselect':
            if not isinstance(value, list):
                errors.append(f"{key} must be a list")
            else:
                options = field.get('options', [])
                invalid = [v for v in value if v not in options]
                if invalid:
                    errors.append(f"{key} contains invalid values: {', '.join(invalid)}")
    
    return errors


def generate_summary(trigger_type, trigger_config, action_type, action_config):
    """
    Generate plain English summary of automation.
    
    Args:
        trigger_type: TriggerType enum
        trigger_config: Trigger configuration
        action_type: ActionType enum
        action_config: Action configuration
    
    Returns:
        Plain English summary string
    """
    # Trigger description
    trigger_desc = ""
    if trigger_type == TriggerType.EVENT:
        event_type = trigger_config.get('event_type', 'an event')
        trigger_desc = f"{event_type.replace('_', ' ')} occurs"
    elif trigger_type == TriggerType.SCHEDULE:
        pattern = trigger_config.get('pattern', 'scheduled time')
        day = trigger_config.get('day', '')
        time = trigger_config.get('time', '')
        if pattern == 'weekly' and day:
            trigger_desc = f"every {day} at {time}"
        elif pattern == 'daily' and time:
            trigger_desc = f"every day at {time}"
        else:
            trigger_desc = f"on {pattern} schedule"
    elif trigger_type == TriggerType.THRESHOLD:
        metric = trigger_config.get('metric', 'metric')
        operator = trigger_config.get('operator', '=')
        value = trigger_config.get('value', 0)
        trigger_desc = f"{metric.replace('_', ' ')} {operator} {value}"
    elif trigger_type == TriggerType.BEHAVIOR:
        behavior = trigger_config.get('behavior_type', 'behavior')
        trigger_desc = f"customer {behavior.replace('_', ' ')}"
    
    # Action description
    action_desc = ""
    if action_type == ActionType.START_WORKFLOW:
        workflow_type = action_config.get('workflow_type_id', 'workflow')
        action_desc = f"start {workflow_type.replace('_', ' ')} workflow"
    elif action_type == ActionType.SEND_NOTIFICATION:
        recipients = action_config.get('recipients', ['users'])
        action_desc = f"send notification to {', '.join(recipients)}"
    elif action_type == ActionType.GENERATE_CAMPAIGN:
        channels = action_config.get('channels', ['channels'])
        action_desc = f"generate campaign on {', '.join(channels)}"
    elif action_type == ActionType.ADD_PRODUCT:
        count = action_config.get('count', 1)
        action_desc = f"add {count} new product(s)"
    else:
        action_desc = f"{action_type.value.replace('_', ' ')}"
    
    return f"When {trigger_desc}, {action_desc}."


def calculate_relevance(template, context):
    """
    Calculate relevance score for a template suggestion.
    
    Args:
        template: AutomationTemplate
        context: Tenant context
    
    Returns:
        Relevance score (0.0 to 1.0)
    """
    score = 0.5  # Base score
    
    suggest_when = template.ai_suggestion_rules.get('suggest_when', {})
    
    # Check how many conditions match
    total_conditions = len(suggest_when)
    matched_conditions = 0
    
    for metric, rule in suggest_when.items():
        operator = rule.get('operator')
        threshold = rule.get('value')
        actual_value = context.get(metric)
        
        if actual_value is None:
            continue
        
        # Check if condition matches
        if operator == '<' and actual_value < threshold:
            matched_conditions += 1
        elif operator == '>' and actual_value > threshold:
            matched_conditions += 1
        elif operator == '=' and actual_value == threshold:
            matched_conditions += 1
    
    # Calculate score based on match percentage
    if total_conditions > 0:
        match_percentage = matched_conditions / total_conditions
        score = 0.5 + (match_percentage * 0.5)
    
    # Boost score based on template popularity and success rate
    if template.popularity_score:
        score += (min(template.popularity_score, 100) / 100) * 0.1
    
    if template.success_rate:
        score += template.success_rate * 0.1
    
    return min(score, 1.0)


# ============================================================================
# REGISTRATION
# ============================================================================

def register_automation_library_routes(app):
    """Register automation library blueprint with Flask app"""
    app.register_blueprint(library_bp)
    print("✓ Automation Library API registered at /api/automation-library")
