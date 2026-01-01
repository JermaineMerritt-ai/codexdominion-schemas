"""
Automation Rules API

RESTful API for managing automation rules that trigger workflows, notifications,
and actions based on events, schedules, thresholds, or customer behavior.

Endpoints:
- CRUD operations (5)
- Enable/disable automation (2)
- Test conditions (1)
- Execute automation (1)
- Get execution history (1)
- Get execution stats (1)
- Recommend automations (1)
- Get plain English summary (1)

Integration:
    from automation_api import register_automation_routes
    register_automation_routes(app)
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import desc, func
from db import SessionLocal
from models import (
    AutomationRule, AutomationExecution, Tenant, Council, WorkflowTemplate,
    TriggerType, ActionType, RiskLevel
)
import json

automation_bp = Blueprint('automation', __name__, url_prefix='/api/automations')


# ============================================================================
# CRUD OPERATIONS
# ============================================================================

@automation_bp.route('', methods=['GET'])
def list_automations():
    """
    List automation rules with filtering.
    
    Query params:
    - tenant_id: Filter by tenant
    - category: Filter by category (marketing, store, product, campaign, customer)
    - trigger_type: Filter by trigger type (event, schedule, threshold, behavior)
    - enabled: Filter by enabled status (true/false)
    - risk_level: Filter by risk level (low, medium, high, critical)
    
    Returns:
    {
      "automations": [...],
      "count": 10,
      "enabled_count": 8,
      "disabled_count": 2
    }
    """
    session = SessionLocal()
    try:
        query = session.query(AutomationRule)
        
        # Filters
        tenant_id = request.args.get('tenant_id')
        if tenant_id:
            query = query.filter(AutomationRule.tenant_id == tenant_id)
        
        category = request.args.get('category')
        if category:
            query = query.filter(AutomationRule.category == category)
        
        trigger_type = request.args.get('trigger_type')
        if trigger_type:
            query = query.filter(AutomationRule.trigger_type == TriggerType(trigger_type))
        
        enabled = request.args.get('enabled')
        if enabled is not None:
            enabled_bool = enabled.lower() == 'true'
            query = query.filter(AutomationRule.enabled == enabled_bool)
        
        risk_level = request.args.get('risk_level')
        if risk_level:
            query = query.filter(AutomationRule.risk_level == RiskLevel(risk_level))
        
        # Order by most recently created
        query = query.order_by(desc(AutomationRule.created_at))
        
        automations = query.all()
        
        # Calculate stats
        enabled_count = sum(1 for a in automations if a.enabled)
        disabled_count = len(automations) - enabled_count
        
        return jsonify({
            "automations": [a.to_dict() for a in automations],
            "count": len(automations),
            "enabled_count": enabled_count,
            "disabled_count": disabled_count
        }), 200
        
    finally:
        session.close()


@automation_bp.route('', methods=['POST'])
def create_automation():
    """
    Create a new automation rule.
    
    Body:
    {
      "tenant_id": "tenant_123",
      "name": "Low Product Alert",
      "description": "Alert when product count drops below 3",
      "category": "product",
      "trigger_type": "threshold",
      "trigger_config": {"metric": "product_count", "operator": "<", "value": 3},
      "conditions": [
        {"type": "store_status", "operator": "=", "value": "active"}
      ],
      "action_type": "send_notification",
      "action_config": {"recipients": ["owner"], "message": "Low product count"},
      "risk_level": "low",
      "requires_approval": false,
      "assigned_council_id": "council_ops",
      "auto_approval_rules": {"max_budget": 100}
    }
    
    Returns:
    {
      "automation": {...},
      "message": "Automation rule created successfully"
    }
    """
    session = SessionLocal()
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['tenant_id', 'name', 'trigger_type', 'trigger_config', 'action_type', 'action_config']
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate enums
        try:
            trigger_type = TriggerType(data['trigger_type'])
            action_type = ActionType(data['action_type'])
            risk_level = RiskLevel(data.get('risk_level', 'low'))
        except ValueError as e:
            return jsonify({"error": f"Invalid enum value: {str(e)}"}), 400
        
        # Create automation
        automation = AutomationRule(
            tenant_id=data['tenant_id'],
            name=data['name'],
            description=data.get('description'),
            category=data.get('category'),
            enabled=data.get('enabled', True),
            trigger_type=trigger_type,
            trigger_config=data['trigger_config'],
            conditions=data.get('conditions', []),
            action_type=action_type,
            action_config=data['action_config'],
            risk_level=risk_level,
            requires_approval=data.get('requires_approval', False),
            assigned_council_id=data.get('assigned_council_id'),
            auto_approval_rules=data.get('auto_approval_rules', {}),
            created_by_user_id=data.get('created_by_user_id')
        )
        
        session.add(automation)
        session.commit()
        session.refresh(automation)
        
        return jsonify({
            "automation": automation.to_dict(),
            "message": "Automation rule created successfully"
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@automation_bp.route('/<automation_id>', methods=['GET'])
def get_automation(automation_id):
    """
    Get a specific automation rule with execution stats.
    
    Returns:
    {
      "automation": {...},
      "stats": {
        "total_executions": 100,
        "success_rate": 0.95,
        "avg_execution_time_ms": 523.4,
        "last_24h_executions": 12
      },
      "recent_executions": [...]
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        # Calculate success rate
        success_rate = 0.0
        if automation.execution_count > 0:
            success_rate = automation.success_count / automation.execution_count
        
        # Get last 24h executions
        last_24h = datetime.utcnow() - timedelta(hours=24)
        last_24h_count = session.query(AutomationExecution).filter(
            AutomationExecution.automation_rule_id == automation_id,
            AutomationExecution.triggered_at >= last_24h
        ).count()
        
        # Get recent executions (last 10)
        recent_executions = session.query(AutomationExecution).filter(
            AutomationExecution.automation_rule_id == automation_id
        ).order_by(desc(AutomationExecution.triggered_at)).limit(10).all()
        
        return jsonify({
            "automation": automation.to_dict(),
            "stats": {
                "total_executions": automation.execution_count,
                "success_rate": success_rate,
                "avg_execution_time_ms": automation.average_execution_time_ms,
                "last_24h_executions": last_24h_count
            },
            "recent_executions": [e.to_dict() for e in recent_executions]
        }), 200
        
    finally:
        session.close()


@automation_bp.route('/<automation_id>', methods=['PATCH'])
def update_automation(automation_id):
    """
    Update an automation rule.
    Only updateable fields: name, description, category, trigger_config, conditions, action_config, risk_level, auto_approval_rules
    
    Body: Partial automation object
    
    Returns:
    {
      "automation": {...},
      "message": "Automation rule updated successfully"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        data = request.get_json()
        
        # Updateable fields
        updateable = ['name', 'description', 'category', 'trigger_config', 'conditions', 
                     'action_config', 'risk_level', 'requires_approval', 'assigned_council_id', 
                     'auto_approval_rules']
        
        for field in updateable:
            if field in data:
                if field == 'risk_level':
                    setattr(automation, field, RiskLevel(data[field]))
                else:
                    setattr(automation, field, data[field])
        
        automation.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(automation)
        
        return jsonify({
            "automation": automation.to_dict(),
            "message": "Automation rule updated successfully"
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@automation_bp.route('/<automation_id>', methods=['DELETE'])
def delete_automation(automation_id):
    """
    Delete an automation rule and all its execution logs.
    
    Returns:
    {
      "message": "Automation rule deleted successfully"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        session.delete(automation)
        session.commit()
        
        return jsonify({
            "message": "Automation rule deleted successfully"
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# ENABLE/DISABLE OPERATIONS
# ============================================================================

@automation_bp.route('/<automation_id>/enable', methods=['POST'])
def enable_automation(automation_id):
    """
    Enable an automation rule.
    
    Returns:
    {
      "automation": {...},
      "message": "Automation rule enabled"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        automation.enabled = True
        automation.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(automation)
        
        return jsonify({
            "automation": automation.to_dict(),
            "message": "Automation rule enabled"
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@automation_bp.route('/<automation_id>/disable', methods=['POST'])
def disable_automation(automation_id):
    """
    Disable an automation rule.
    
    Returns:
    {
      "automation": {...},
      "message": "Automation rule disabled"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        automation.enabled = False
        automation.updated_at = datetime.utcnow()
        
        session.commit()
        session.refresh(automation)
        
        return jsonify({
            "automation": automation.to_dict(),
            "message": "Automation rule disabled"
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# TESTING OPERATIONS
# ============================================================================

@automation_bp.route('/<automation_id>/test-conditions', methods=['POST'])
def test_conditions(automation_id):
    """
    Test automation conditions against provided context without executing.
    
    Body:
    {
      "context": {
        "product_count": 2,
        "store_status": "active",
        "workflow_status": "completed"
      }
    }
    
    Returns:
    {
      "conditions_met": true,
      "results": [
        {"condition": {...}, "passed": true, "actual_value": 2, "expected_value": 3}
      ],
      "summary": "All 2 conditions passed",
      "would_execute": true
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        data = request.get_json()
        context = data.get('context', {})
        
        # Test each condition individually
        results = []
        all_passed = True
        
        for condition in automation.conditions:
            condition_type = condition.get("type")
            operator = condition.get("operator")
            expected_value = condition.get("value")
            actual_value = context.get(condition_type)
            
            # Evaluate condition
            passed = False
            if actual_value is not None:
                if operator == "=":
                    passed = actual_value == expected_value
                elif operator == "!=":
                    passed = actual_value != expected_value
                elif operator == "<":
                    passed = actual_value < expected_value
                elif operator == ">":
                    passed = actual_value > expected_value
                elif operator == "<=":
                    passed = actual_value <= expected_value
                elif operator == ">=":
                    passed = actual_value >= expected_value
                elif operator == "contains":
                    passed = expected_value in str(actual_value)
                elif operator == "not_contains":
                    passed = expected_value not in str(actual_value)
            
            results.append({
                "condition": condition,
                "passed": passed,
                "actual_value": actual_value,
                "expected_value": expected_value,
                "missing_context": actual_value is None
            })
            
            if not passed:
                all_passed = False
        
        # Overall result
        conditions_met = automation.evaluate_conditions(context)
        
        # Check if would auto-approve
        would_auto_approve = automation.should_auto_approve(context)
        
        return jsonify({
            "conditions_met": conditions_met,
            "results": results,
            "summary": f"{'All' if all_passed else 'Some'} {len(results)} condition(s) {'passed' if all_passed else 'failed'}",
            "would_execute": conditions_met and (would_auto_approve or not automation.requires_approval),
            "requires_approval": automation.requires_approval and not would_auto_approve
        }), 200
        
    finally:
        session.close()


# ============================================================================
# EXECUTION OPERATIONS
# ============================================================================

@automation_bp.route('/<automation_id>/execute', methods=['POST'])
def execute_automation(automation_id):
    """
    Manually execute an automation rule.
    
    Body:
    {
      "context": {...},
      "trigger_source": "manual",
      "bypass_approval": false
    }
    
    Returns:
    {
      "execution": {...},
      "message": "Automation executed successfully"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        if not automation.enabled:
            return jsonify({"error": "Automation is disabled"}), 400
        
        data = request.get_json()
        context = data.get('context', {})
        trigger_source = data.get('trigger_source', 'manual')
        bypass_approval = data.get('bypass_approval', False)
        
        # Create execution log
        execution = AutomationExecution(
            automation_rule_id=automation.id,
            tenant_id=automation.tenant_id,
            trigger_source=trigger_source,
            trigger_data=context
        )
        
        start_time = datetime.utcnow()
        
        # Evaluate conditions
        conditions_met = automation.evaluate_conditions(context)
        execution.conditions_met = conditions_met
        
        if not conditions_met:
            execution.success = False
            execution.error_message = "Conditions not met"
            session.add(execution)
            session.commit()
            
            return jsonify({
                "execution": execution.to_dict(),
                "message": "Conditions not met, automation not executed"
            }), 200
        
        # Check approval requirements
        if automation.requires_approval and not bypass_approval:
            can_auto_approve = automation.should_auto_approve(context)
            if not can_auto_approve:
                execution.required_approval = True
                execution.success = False
                execution.error_message = "Requires council approval"
                session.add(execution)
                session.commit()
                
                return jsonify({
                    "execution": execution.to_dict(),
                    "message": "Requires council approval before execution"
                }), 200
        
        # Execute action (placeholder - would integrate with actual action handlers)
        execution.action_started_at = datetime.utcnow()
        
        try:
            # TODO: Integrate with actual action handlers
            action_result = {
                "action_type": automation.action_type.value,
                "status": "simulated",
                "message": "Action execution would happen here"
            }
            
            execution.action_result = action_result
            execution.action_completed_at = datetime.utcnow()
            execution.success = True
            
        except Exception as action_error:
            execution.error_message = str(action_error)
            execution.success = False
        
        # Calculate execution time
        end_time = datetime.utcnow()
        execution.execution_time_ms = (end_time - start_time).total_seconds() * 1000
        
        # Update automation stats
        automation.last_triggered_at = start_time
        automation.record_execution(execution.success, execution.execution_time_ms)
        
        session.add(execution)
        session.commit()
        session.refresh(execution)
        
        return jsonify({
            "execution": execution.to_dict(),
            "message": "Automation executed successfully" if execution.success else "Automation execution failed"
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@automation_bp.route('/<automation_id>/executions', methods=['GET'])
def get_execution_history(automation_id):
    """
    Get execution history for an automation rule.
    
    Query params:
    - limit: Max number of results (default 50)
    - offset: Skip N results (default 0)
    - success: Filter by success status (true/false)
    
    Returns:
    {
      "executions": [...],
      "count": 100,
      "has_more": true
    }
    """
    session = SessionLocal()
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        query = session.query(AutomationExecution).filter(
            AutomationExecution.automation_rule_id == automation_id
        )
        
        # Filter by success
        success = request.args.get('success')
        if success is not None:
            success_bool = success.lower() == 'true'
            query = query.filter(AutomationExecution.success == success_bool)
        
        # Get total count
        total_count = query.count()
        
        # Get paginated results
        executions = query.order_by(desc(AutomationExecution.triggered_at)).limit(limit).offset(offset).all()
        
        return jsonify({
            "executions": [e.to_dict() for e in executions],
            "count": total_count,
            "has_more": (offset + len(executions)) < total_count
        }), 200
        
    finally:
        session.close()


@automation_bp.route('/<automation_id>/stats', methods=['GET'])
def get_execution_stats(automation_id):
    """
    Get detailed execution statistics for an automation rule.
    
    Returns:
    {
      "total_executions": 100,
      "success_count": 95,
      "failure_count": 5,
      "success_rate": 0.95,
      "avg_execution_time_ms": 523.4,
      "executions_by_day": [...],
      "failure_reasons": [...]
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        # Get executions from last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        executions = session.query(AutomationExecution).filter(
            AutomationExecution.automation_rule_id == automation_id,
            AutomationExecution.triggered_at >= thirty_days_ago
        ).all()
        
        # Group by day
        executions_by_day = {}
        for execution in executions:
            day = execution.triggered_at.date().isoformat()
            if day not in executions_by_day:
                executions_by_day[day] = {"total": 0, "success": 0, "failure": 0}
            executions_by_day[day]["total"] += 1
            if execution.success:
                executions_by_day[day]["success"] += 1
            else:
                executions_by_day[day]["failure"] += 1
        
        # Get failure reasons
        failure_reasons = {}
        for execution in executions:
            if not execution.success and execution.error_message:
                reason = execution.error_message
                failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        # Calculate success rate
        success_rate = 0.0
        if automation.execution_count > 0:
            success_rate = automation.success_count / automation.execution_count
        
        return jsonify({
            "total_executions": automation.execution_count,
            "success_count": automation.success_count,
            "failure_count": automation.failure_count,
            "success_rate": success_rate,
            "avg_execution_time_ms": automation.average_execution_time_ms,
            "executions_by_day": [
                {"date": day, **stats} for day, stats in sorted(executions_by_day.items())
            ],
            "failure_reasons": [
                {"reason": reason, "count": count} for reason, count in sorted(failure_reasons.items(), key=lambda x: x[1], reverse=True)
            ]
        }), 200
        
    finally:
        session.close()


# ============================================================================
# AI RECOMMENDATION OPERATIONS
# ============================================================================

@automation_bp.route('/recommend', methods=['POST'])
def recommend_automations():
    """
    Get AI-recommended automation rules for a tenant based on their context.
    
    Body:
    {
      "tenant_id": "tenant_123",
      "context": {
        "product_count": 2,
        "store_performance": "good",
        "recent_campaigns": 0,
        "customer_engagement": "low",
        "seasonal_context": "holiday_season"
      }
    }
    
    Returns:
    {
      "recommendations": [
        {
          "name": "Low Product Alert",
          "description": "...",
          "relevance_score": 0.95,
          "reasoning": "Your product count is low...",
          "suggested_config": {...}
        }
      ]
    }
    """
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    context = data.get('context', {})
    
    recommendations = []
    
    # Recommendation 1: Low Product Count
    if context.get('product_count', 0) < 5:
        recommendations.append({
            "name": "Low Product Alert",
            "description": "Get notified when product count drops below threshold",
            "category": "product",
            "relevance_score": 0.95,
            "reasoning": f"Your product count ({context.get('product_count')}) is low. This automation will alert you to maintain inventory.",
            "suggested_config": {
                "trigger_type": "threshold",
                "trigger_config": {"metric": "product_count", "operator": "<", "value": 3},
                "action_type": "send_notification",
                "action_config": {"recipients": ["owner"], "message": "Product inventory is low"},
                "risk_level": "low"
            }
        })
    
    # Recommendation 2: Campaign Generation
    if context.get('recent_campaigns', 0) == 0:
        recommendations.append({
            "name": "Weekly Campaign Generator",
            "description": "Automatically create marketing campaigns every week",
            "category": "marketing",
            "relevance_score": 0.88,
            "reasoning": "You haven't run any recent campaigns. Regular marketing keeps customers engaged.",
            "suggested_config": {
                "trigger_type": "schedule",
                "trigger_config": {"pattern": "weekly", "day": "monday", "time": "09:00"},
                "action_type": "generate_campaign",
                "action_config": {"template_id": "weekly_promo", "channels": ["email", "social"]},
                "risk_level": "medium"
            }
        })
    
    # Recommendation 3: Seasonal Automation
    if context.get('seasonal_context') == 'holiday_season':
        recommendations.append({
            "name": "Holiday Product Launch",
            "description": "Automatically add seasonal products during holidays",
            "category": "product",
            "relevance_score": 0.82,
            "reasoning": "It's holiday season. Automated seasonal product launches can boost sales.",
            "suggested_config": {
                "trigger_type": "event",
                "trigger_config": {"event_type": "season_start", "season": "holiday"},
                "action_type": "add_product",
                "action_config": {"template_id": "holiday_product", "count": 5},
                "risk_level": "medium"
            }
        })
    
    # Recommendation 4: Low Engagement Recovery
    if context.get('customer_engagement') == 'low':
        recommendations.append({
            "name": "Re-engagement Campaign",
            "description": "Automatically reach out to inactive customers",
            "category": "customer",
            "relevance_score": 0.79,
            "reasoning": "Customer engagement is low. Automated re-engagement can win back customers.",
            "suggested_config": {
                "trigger_type": "behavior",
                "trigger_config": {"behavior_type": "inactive", "days": 30},
                "action_type": "send_notification",
                "action_config": {"template_id": "winback_email", "offer": "10% discount"},
                "risk_level": "low"
            }
        })
    
    # Sort by relevance score
    recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return jsonify({
        "recommendations": recommendations,
        "count": len(recommendations)
    }), 200


@automation_bp.route('/<automation_id>/summary', methods=['GET'])
def get_plain_english_summary(automation_id):
    """
    Get a plain English summary of what an automation does.
    
    Returns:
    {
      "summary": "When product count drops below 3 in an active store, send a notification to the owner saying 'Low product count'.",
      "trigger_description": "Product count falls below 3",
      "conditions_description": "Store is active",
      "action_description": "Send notification to owner"
    }
    """
    session = SessionLocal()
    try:
        automation = session.query(AutomationRule).filter_by(id=automation_id).first()
        
        if not automation:
            return jsonify({"error": "Automation rule not found"}), 404
        
        # Build trigger description
        trigger_desc = ""
        if automation.trigger_type == TriggerType.EVENT:
            event_type = automation.trigger_config.get('event_type', 'an event')
            trigger_desc = f"{event_type.replace('_', ' ')} occurs"
        elif automation.trigger_type == TriggerType.SCHEDULE:
            pattern = automation.trigger_config.get('pattern', 'scheduled time')
            trigger_desc = f"{pattern} schedule"
        elif automation.trigger_type == TriggerType.THRESHOLD:
            metric = automation.trigger_config.get('metric', 'metric')
            operator = automation.trigger_config.get('operator', '=')
            value = automation.trigger_config.get('value', 0)
            trigger_desc = f"{metric.replace('_', ' ')} {operator} {value}"
        elif automation.trigger_type == TriggerType.BEHAVIOR:
            behavior = automation.trigger_config.get('behavior_type', 'behavior')
            trigger_desc = f"customer {behavior.replace('_', ' ')}"
        
        # Build conditions description
        conditions_desc = ""
        if automation.conditions:
            condition_parts = []
            for cond in automation.conditions:
                cond_type = cond.get('type', 'condition').replace('_', ' ')
                operator = cond.get('operator', '=')
                value = cond.get('value', '')
                condition_parts.append(f"{cond_type} {operator} {value}")
            conditions_desc = " and ".join(condition_parts)
        
        # Build action description
        action_desc = ""
        if automation.action_type == ActionType.START_WORKFLOW:
            workflow_type = automation.action_config.get('workflow_type_id', 'workflow')
            action_desc = f"start {workflow_type.replace('_', ' ')} workflow"
        elif automation.action_type == ActionType.SEND_NOTIFICATION:
            recipients = automation.action_config.get('recipients', ['users'])
            message = automation.action_config.get('message', 'notification')
            action_desc = f"send notification to {', '.join(recipients)}: '{message}'"
        elif automation.action_type == ActionType.GENERATE_CAMPAIGN:
            channels = automation.action_config.get('channels', ['channels'])
            action_desc = f"generate campaign on {', '.join(channels)}"
        elif automation.action_type == ActionType.ADD_PRODUCT:
            count = automation.action_config.get('count', 1)
            action_desc = f"add {count} new product(s)"
        else:
            action_desc = f"{automation.action_type.value.replace('_', ' ')}"
        
        # Build full summary
        summary = f"When {trigger_desc}"
        if conditions_desc:
            summary += f" and {conditions_desc}"
        summary += f", {action_desc}."
        
        return jsonify({
            "summary": summary,
            "trigger_description": trigger_desc,
            "conditions_description": conditions_desc or "No additional conditions",
            "action_description": action_desc
        }), 200
        
    finally:
        session.close()


# ============================================================================
# REGISTRATION
# ============================================================================

def register_automation_routes(app):
    """Register automation blueprint with Flask app"""
    app.register_blueprint(automation_bp)
    print("✓ Automation Rules API registered at /api/automations")
