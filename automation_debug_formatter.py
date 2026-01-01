"""
Automation Debug Log Formatter

Converts raw debug logs into clean, standardized JSON format
for API responses and external integrations.
"""

from typing import Dict, Any, List
from datetime import datetime
from models import AutomationDebugLog


def format_debug_log_clean(log: AutomationDebugLog) -> Dict[str, Any]:
    """
    Convert AutomationDebugLog to clean JSON format
    
    Returns:
    {
        "trigger": {
            "type": "schedule",
            "fired": true,
            "timestamp": "2025-12-21T14:00:00Z"
        },
        "conditions": [
            {"id": 1, "passed": true, "value": 2},
            {"id": 2, "passed": true, "value": "active"},
            {"id": 3, "passed": false, "value": 3}
        ],
        "action": {
            "executed": false,
            "reason": "Condition 3 failed"
        },
        "metrics": {
            "execution_time_ms": 42
        }
    }
    """
    # Format conditions
    conditions = []
    for idx, condition in enumerate(log.conditions_evaluated or [], start=1):
        conditions.append({
            "id": idx,
            "condition": condition.get("condition", ""),
            "passed": condition.get("passed", False),
            "value": condition.get("actual_value"),
            "expected": condition.get("expected")
        })
    
    # Determine action status
    action_executed = len(log.actions_taken or []) > 0
    action_reason = None
    
    if not action_executed:
        if not log.trigger_fired:
            action_reason = "Trigger did not fire"
        elif not log.all_conditions_passed:
            failed_conditions = [
                c.get("condition") 
                for c in (log.conditions_evaluated or []) 
                if not c.get("passed", False)
            ]
            action_reason = f"Conditions failed: {', '.join(failed_conditions)}"
        elif log.errors:
            action_reason = log.errors[0] if log.errors else "Unknown error"
        else:
            action_reason = "Skipped"
    
    # Build clean format
    return {
        "trigger": {
            "type": log.trigger_type.value,
            "fired": log.trigger_fired,
            "timestamp": log.timestamp.isoformat() + 'Z',
            "details": log.trigger_details or {}
        },
        "conditions": conditions,
        "action": {
            "executed": action_executed,
            "reason": action_reason,
            "actions_taken": log.actions_taken or [],
            "workflow_id": log.workflow_id
        },
        "metrics": {
            "execution_time_ms": log.execution_time_ms or 0,
            "errors": log.errors or [],
            "warnings": log.warnings or []
        },
        "result": log.result.value,
        "automation_id": log.automation_id,
        "log_id": log.id
    }


def format_debug_log_minimal(log: AutomationDebugLog) -> Dict[str, Any]:
    """
    Ultra-minimal format for quick analysis
    
    Returns:
    {
        "trigger": {"type": "schedule", "fired": true, "timestamp": "..."},
        "conditions": [
            {"id": 1, "passed": true, "value": 2},
            {"id": 2, "passed": true, "value": "active"},
            {"id": 3, "passed": false, "value": 3}
        ],
        "action": {"executed": false, "reason": "Condition 3 failed"},
        "metrics": {"execution_time_ms": 42}
    }
    """
    conditions = []
    for idx, condition in enumerate(log.conditions_evaluated or [], start=1):
        conditions.append({
            "id": idx,
            "passed": condition.get("passed", False),
            "value": condition.get("actual_value")
        })
    
    action_executed = len(log.actions_taken or []) > 0
    action_reason = None
    
    if not action_executed:
        if not log.trigger_fired:
            action_reason = "Trigger did not fire"
        elif not log.all_conditions_passed:
            failed_ids = [
                idx + 1 
                for idx, c in enumerate(log.conditions_evaluated or []) 
                if not c.get("passed", False)
            ]
            action_reason = f"Condition {', '.join(map(str, failed_ids))} failed"
        else:
            action_reason = "Skipped"
    
    return {
        "trigger": {
            "type": log.trigger_type.value,
            "fired": log.trigger_fired,
            "timestamp": log.timestamp.isoformat() + 'Z'
        },
        "conditions": conditions,
        "action": {
            "executed": action_executed,
            "reason": action_reason
        },
        "metrics": {
            "execution_time_ms": log.execution_time_ms or 0
        }
    }


def create_debug_log_from_json(
    tenant_id: str,
    automation_id: str,
    log_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a debug log from clean JSON format
    
    Input format:
    {
        "trigger": {"type": "schedule", "fired": true, "timestamp": "..."},
        "conditions": [
            {"id": 1, "passed": true, "value": 2, "condition": "product_count < 3"},
            ...
        ],
        "action": {"executed": false, "reason": "..."},
        "metrics": {"execution_time_ms": 42}
    }
    
    Returns: Data ready for AutomationDebugLog creation
    """
    from models import TriggerType, EventResult
    
    # Parse trigger
    trigger_data = log_data.get("trigger", {})
    trigger_type = TriggerType[trigger_data.get("type", "schedule").upper()]
    trigger_fired = trigger_data.get("fired", False)
    
    # Parse conditions
    conditions_raw = log_data.get("conditions", [])
    conditions_evaluated = []
    for cond in conditions_raw:
        conditions_evaluated.append({
            "condition": cond.get("condition", f"Condition {cond.get('id')}"),
            "passed": cond.get("passed", False),
            "actual_value": cond.get("value"),
            "expected": cond.get("expected")
        })
    
    all_conditions_passed = all(c["passed"] for c in conditions_evaluated)
    
    # Parse action
    action_data = log_data.get("action", {})
    action_executed = action_data.get("executed", False)
    
    actions_taken = []
    actions_skipped = []
    
    if action_executed:
        actions_taken = action_data.get("actions_taken", [])
    else:
        actions_skipped = [{
            "action": "automation_execution",
            "reason": action_data.get("reason", "Unknown")
        }]
    
    # Determine result
    if action_executed:
        result = EventResult.SUCCESS
    elif not trigger_fired:
        result = EventResult.SKIPPED
    elif not all_conditions_passed:
        result = EventResult.SKIPPED
    else:
        result = EventResult.FAILED
    
    # Parse metrics
    metrics = log_data.get("metrics", {})
    
    return {
        "tenant_id": tenant_id,
        "automation_id": automation_id,
        "trigger_fired": trigger_fired,
        "trigger_type": trigger_type,
        "trigger_details": trigger_data.get("details", {}),
        "conditions_evaluated": conditions_evaluated,
        "all_conditions_passed": all_conditions_passed,
        "actions_taken": actions_taken,
        "actions_skipped": actions_skipped,
        "execution_time_ms": metrics.get("execution_time_ms", 0),
        "errors": metrics.get("errors", []),
        "warnings": metrics.get("warnings", []),
        "data_snapshot": log_data.get("data_snapshot", {}),
        "result": result,
        "workflow_id": action_data.get("workflow_id")
    }
