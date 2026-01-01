"""
Automation Debugger API

The truth table of your empire - shows exactly why automations
triggered or didn't trigger, which conditions passed/failed,
and what actions were taken.

Endpoints:
- GET /api/automation-debugger/:automation_id/logs - Get debug logs for automation
- GET /api/automation-debugger/:automation_id/latest - Get most recent debug log
- GET /api/automation-debugger/log/:log_id - Get specific debug log details
- POST /api/automation-debugger/simulate - Simulate automation execution

Author: Codex Dominion
Created: December 21, 2025
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from db import SessionLocal
from models import AutomationDebugLog, AutomationRule, TriggerType, EventResult
from typing import Dict, Any, Optional, List
import random
from automation_error_detection import detect_automation_issues


debugger_bp = Blueprint('automation_debugger', __name__)


def register_automation_debugger_routes(app):
    """Register debugger API routes with Flask app"""
    app.register_blueprint(debugger_bp, url_prefix='/api/automation-debugger')


# ================================================================
# DEBUGGER ENDPOINTS
# ================================================================

@debugger_bp.route('/<automation_id>/logs', methods=['GET'])
def get_automation_logs(automation_id: str):
    """
    Get debug logs for a specific automation
    
    Query params:
    - days: Number of days to retrieve (default: 7)
    - limit: Max logs to return (default: 50)
    - result: Filter by result (success, skipped, failed)
    
    Returns:
    {
        "automation_id": "auto_weekly_social",
        "automation_name": "Weekly Social Post Generator",
        "total_logs": 12,
        "logs": [
            {
                "id": "log_123",
                "timestamp": "2025-12-21T09:00:00Z",
                "trigger_fired": true,
                "all_conditions_passed": true,
                "result": "success",
                "execution_time_ms": 2340,
                "workflow_id": "wf_456"
            },
            ...
        ],
        "summary": {
            "total_runs": 12,
            "successful": 10,
            "skipped": 1,
            "failed": 1,
            "avg_execution_time_ms": 2100
        }
    }
    """
    session = SessionLocal()
    
    try:
        days = int(request.args.get('days', 7))
        limit = int(request.args.get('limit', 50))
        result_filter = request.args.get('result', None)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = session.query(AutomationDebugLog).filter(
            AutomationDebugLog.automation_id == automation_id,
            AutomationDebugLog.timestamp >= start_date
        )
        
        # Result filter
        if result_filter:
            query = query.filter(AutomationDebugLog.result == EventResult[result_filter.upper()])
        
        total_logs = query.count()
        logs_raw = query.order_by(AutomationDebugLog.timestamp.desc()).limit(limit).all()
        
        # Format logs
        logs = []
        for log in logs_raw:
            logs.append({
                'id': log.id,
                'timestamp': log.timestamp.isoformat() + 'Z',
                'trigger_fired': log.trigger_fired,
                'all_conditions_passed': log.all_conditions_passed,
                'result': log.result.value,
                'execution_time_ms': log.execution_time_ms,
                'workflow_id': log.workflow_id,
                'has_errors': len(log.errors or []) > 0,
                'has_warnings': len(log.warnings or []) > 0
            })
        
        # Calculate summary
        all_logs = session.query(AutomationDebugLog).filter(
            AutomationDebugLog.automation_id == automation_id,
            AutomationDebugLog.timestamp >= start_date
        ).all()
        
        summary = {
            'total_runs': len(all_logs),
            'successful': sum(1 for log in all_logs if log.result == EventResult.SUCCESS),
            'skipped': sum(1 for log in all_logs if log.result == EventResult.SKIPPED),
            'failed': sum(1 for log in all_logs if log.result == EventResult.FAILED),
            'avg_execution_time_ms': int(sum(log.execution_time_ms or 0 for log in all_logs) / len(all_logs)) if all_logs else 0
        }
        
        # Get automation name
        automation_name = automation_id.replace('auto_', '').replace('_', ' ').title()
        
        return jsonify({
            'automation_id': automation_id,
            'automation_name': automation_name,
            'total_logs': total_logs,
            'logs': logs,
            'summary': summary
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/<automation_id>/latest', methods=['GET'])
def get_latest_log(automation_id: str):
    """
    Get the most recent debug log for an automation
    
    This is the "current state" view - shows the last execution details.
    """
    session = SessionLocal()
    
    try:
        log = session.query(AutomationDebugLog).filter(
            AutomationDebugLog.automation_id == automation_id
        ).order_by(AutomationDebugLog.timestamp.desc()).first()
        
        if not log:
            return jsonify({'error': 'No logs found for this automation'}), 404
        
        return jsonify(log.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/log/<log_id>', methods=['GET'])
def get_log_details(log_id: str):
    """
    Get full details of a specific debug log
    
    Query params:
    - format: "full" (default) or "clean" (minimal JSON)
    
    Returns complete diagnostic information including:
    - Trigger evaluation
    - All condition results
    - Actions taken/skipped
    - Raw data snapshot
    - Errors and warnings
    """
    session = SessionLocal()
    
    try:
        log = session.query(AutomationDebugLog).filter_by(id=log_id).first()
        
        if not log:
            return jsonify({'error': 'Debug log not found'}), 404
        
        # Check format preference
        format_type = request.args.get('format', 'full')
        
        if format_type == 'clean':
            from automation_debug_formatter import format_debug_log_clean
            return jsonify(format_debug_log_clean(log)), 200
        elif format_type == 'minimal':
            from automation_debug_formatter import format_debug_log_minimal
            return jsonify(format_debug_log_minimal(log)), 200
        else:
            return jsonify(log.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/log/<log_id>/clean', methods=['GET'])
def get_log_clean_format(log_id: str):
    """
    Get debug log in clean JSON format
    
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
    session = SessionLocal()
    
    try:
        log = session.query(AutomationDebugLog).filter_by(id=log_id).first()
        
        if not log:
            return jsonify({'error': 'Debug log not found'}), 404
        
        from automation_debug_formatter import format_debug_log_minimal
        return jsonify(format_debug_log_minimal(log)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/simulate', methods=['POST'])
def simulate_automation():
    """
    Test automation execution - see what WOULD happen
    
    Request body:
    {
        "automation_id": "auto_weekly_social",
        "data": {
            "product_count": 5,
            "last_campaign_date": "2025-12-15",
            "store_status": "active"
        }
    }
    
    Returns detailed test results showing:
    - Which conditions would pass/fail
    - What actions would/wouldn't run
    - Missing data warnings
    - Predicted outcome
    """
    session = SessionLocal()
    
    try:
        data = request.json
        automation_id = data.get('automation_id')
        input_data = data.get('data', {})
        
        if not automation_id:
            return jsonify({'error': 'automation_id is required'}), 400
        
        # Enhanced simulation with detailed condition evaluation
        automation_name = automation_id.replace('auto_', '').replace('_', ' ').title()
        
        # Simulate conditions (this would be replaced with actual automation logic)
        conditions = []
        warnings = []
        errors = []
        missing_data = []
        
        # Example condition checks
        if 'product_count' in input_data:
            conditions.append({
                'id': 1,
                'condition': 'product_count >= 3',
                'passed': input_data['product_count'] >= 3,
                'actual_value': input_data['product_count'],
                'expected': '>= 3',
                'icon': 'checkCircle' if input_data['product_count'] >= 3 else 'xCircle'
            })
        else:
            missing_data.append('product_count')
            conditions.append({
                'id': 1,
                'condition': 'product_count >= 3',
                'passed': False,
                'actual_value': None,
                'expected': '>= 3',
                'icon': 'xCircle',
                'error': 'Missing product_count data'
            })
        
        if 'store_status' in input_data:
            conditions.append({
                'id': 2,
                'condition': 'store_status = active',
                'passed': input_data['store_status'] == 'active',
                'actual_value': input_data['store_status'],
                'expected': 'active',
                'icon': 'checkCircle' if input_data['store_status'] == 'active' else 'xCircle'
            })
        else:
            missing_data.append('store_status')
        
        if 'last_campaign_date' in input_data:
            from datetime import datetime, timedelta
            last_date = datetime.fromisoformat(input_data['last_campaign_date'].replace('Z', ''))
            days_since = (datetime.utcnow() - last_date).days
            passed = days_since >= 7
            
            conditions.append({
                'id': 3,
                'condition': 'no_campaigns_in_last_7_days',
                'passed': passed,
                'actual_value': f'{days_since} days ago',
                'expected': '>= 7 days',
                'icon': 'checkCircle' if passed else 'xCircle'
            })
            
            if days_since < 7:
                warnings.append(f'Campaign created only {days_since} days ago - automation will be skipped')
        else:
            missing_data.append('last_campaign_date')
        
        # Check for missing data warnings
        if missing_data:
            warnings.append(f'Missing data: {", ".join(missing_data)}')
        
        # Determine if all conditions pass
        all_conditions_passed = all(c['passed'] for c in conditions)
        
        # Simulate action outcome
        action_would_run = all_conditions_passed and not errors
        
        # Add high-risk warnings
        if action_would_run and 'social' in automation_id:
            warnings.append('This automation will post to public social media')
        
        # Check for conflicts
        if automation_id == 'auto_weekly_social':
            # Simulate checking for conflicting automations
            warnings.append('Similar automation "auto_daily_social" is also active')
        
        result = {
            'automation_id': automation_id,
            'automation_name': automation_name,
            'test_time': datetime.utcnow().isoformat() + 'Z',
            'status': 'ready' if action_would_run else 'blocked',
            'trigger': {
                'type': 'schedule',
                'would_fire': True,
                'next_run': (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            },
            'conditions': conditions,
            'all_conditions_passed': all_conditions_passed,
            'action': {
                'would_execute': action_would_run,
                'reason': None if action_would_run else 'Conditions failed' if not all_conditions_passed else 'Errors present',
                'workflow_type': 'social_post_generation',
                'estimated_duration': '2-3 minutes',
                'actions': [
                    {
                        'action': 'create_workflow',
                        'type': 'social_post_generation',
                        'platforms': ['Instagram', 'TikTok']
                    }
                ] if action_would_run else []
            },
            'diagnostics': {
                'errors': errors,
                'warnings': warnings,
                'missing_data': missing_data,
                'estimated_execution_time_ms': 2500
            },
            'summary': {
                'verdict': '✅ Action WOULD run' if action_would_run else '❌ Action would NOT run',
                'conditions_passed': sum(1 for c in conditions if c['passed']),
                'conditions_failed': sum(1 for c in conditions if not c['passed']),
                'errors_count': len(errors),
                'warnings_count': len(warnings)
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/log', methods=['POST'])
def create_log_from_json():
    """
    Create a debug log from clean JSON format
    
    Request body:
    {
        "tenant_id": "tenant_codexdominion",
        "automation_id": "auto_weekly_social",
        "trigger": {
            "type": "schedule",
            "fired": true,
            "timestamp": "2025-12-21T14:00:00Z"
        },
        "conditions": [
            {"id": 1, "passed": true, "value": 2, "condition": "product_count < 3"},
            {"id": 2, "passed": true, "value": "active", "condition": "store_status = active"},
            {"id": 3, "passed": false, "value": 3, "condition": "campaigns < 5"}
        ],
        "action": {
            "executed": false,
            "reason": "Condition 3 failed"
        },
        "metrics": {
            "execution_time_ms": 42
        }
    }
    
    Returns the created log ID.
    """
    session = SessionLocal()
    
    try:
        data = request.json
        
        if not data.get('tenant_id') or not data.get('automation_id'):
            return jsonify({'error': 'tenant_id and automation_id are required'}), 400
        
        from automation_debug_formatter import create_debug_log_from_json
        
        # Convert clean JSON to debug log data
        log_data = create_debug_log_from_json(
            tenant_id=data['tenant_id'],
            automation_id=data['automation_id'],
            log_data=data
        )
        
        # Create the log
        log = AutomationDebugLog(
            id=f"debug_{datetime.utcnow().timestamp()}_{random.randint(1000, 9999)}",
            timestamp=datetime.utcnow(),
            **log_data
        )
        
        session.add(log)
        session.commit()
        
        return jsonify({
            'success': True,
            'log_id': log.id,
            'message': 'Debug log created successfully'
        }), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


# ================================================================
# HELPER FUNCTIONS
# ================================================================

def create_debug_log(
    tenant_id: str,
    automation_id: str,
    trigger_fired: bool,
    trigger_type: TriggerType,
    conditions_evaluated: List[Dict[str, Any]],
    actions_taken: List[Dict[str, Any]],
    result: EventResult,
    trigger_details: Optional[Dict[str, Any]] = None,
    actions_skipped: Optional[List[Dict[str, Any]]] = None,
    execution_time_ms: Optional[int] = None,
    errors: Optional[List[str]] = None,
    warnings: Optional[List[str]] = None,
    data_snapshot: Optional[Dict[str, Any]] = None,
    workflow_id: Optional[str] = None,
    next_scheduled_run: Optional[datetime] = None
) -> AutomationDebugLog:
    """
    Helper function to create debug logs from automation execution
    
    Usage in automation_worker.py:
        from automation_debugger_api import create_debug_log
        
        log = create_debug_log(
            tenant_id="tenant_123",
            automation_id="auto_456",
            trigger_fired=True,
            trigger_type=TriggerType.SCHEDULE,
            conditions_evaluated=[
                {"condition": "product_count < 3", "passed": True, "actual_value": 2}
            ],
            actions_taken=[
                {"action": "create_workflow", "status": "success", "workflow_id": "wf_789"}
            ],
            result=EventResult.SUCCESS,
            execution_time_ms=2340
        )
    """
    session = SessionLocal()
    
    try:
        log = AutomationDebugLog(
            id=f"debug_{datetime.utcnow().timestamp()}_{random.randint(1000, 9999)}",
            tenant_id=tenant_id,
            automation_id=automation_id,
            timestamp=datetime.utcnow(),
            trigger_fired=trigger_fired,
            trigger_type=trigger_type,
            trigger_details=trigger_details,
            next_scheduled_run=next_scheduled_run,
            conditions_evaluated=conditions_evaluated,
            all_conditions_passed=all(c.get('passed', False) for c in conditions_evaluated),
            actions_taken=actions_taken,
            actions_skipped=actions_skipped or [],
            execution_time_ms=execution_time_ms,
            errors=errors or [],
            warnings=warnings or [],
            data_snapshot=data_snapshot or {},
            result=result,
            workflow_id=workflow_id
        )
        
        session.add(log)
        session.commit()
        
        return log
    
    finally:
        session.close()


@debugger_bp.route('/<automation_id>/health', methods=['GET'])
def get_automation_health(automation_id: str):
    """
    Get automation health check - errors, warnings, and health score
    
    Returns:
    {
        'automation_id': str,
        'health_score': int (0-100),
        'total_issues': int,
        'errors': [...],
        'warnings': [...],
        'summary': {...}
    }
    """
    session = SessionLocal()
    
    try:
        # Get automation configuration (mock for now)
        config = {
            'trigger': {'type': 'schedule', 'schedule': 'weekly'},
            'conditions': [
                {'field': 'product_count', 'operator': 'greater_than', 'value': 3},
                {'field': 'store_status', 'operator': 'equals', 'value': 'active'}
            ],
            'action': {
                'type': 'social_post_generation',
                'template_version': 'v3'
            }
        }
        
        # Get recent execution logs
        logs = session.query(AutomationDebugLog).filter(
            AutomationDebugLog.automation_id == automation_id
        ).order_by(AutomationDebugLog.timestamp.desc()).limit(10).all()
        
        recent_logs = [log.to_dict() for log in logs]
        
        # Run health check
        health_report = detect_automation_issues(automation_id, config, recent_logs)
        
        return jsonify(health_report), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@debugger_bp.route('/council/<council_id>/audit', methods=['GET'])
def get_council_audit(council_id: str):
    """
    Council-level debugging - deeper governance view
    
    Returns:
    {
        'council_id': str,
        'audit_time': str,
        'automations_monitored': int,
        'risk_flags': [...],
        'governance_violations': [...],
        'template_mismatches': [...],
        'automation_conflicts': [...],
        'historical_patterns': {...}
    }
    """
    session = SessionLocal()
    
    try:
        days = int(request.args.get('days', 30))
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        # Get all automations under this council's oversight
        # (In production, query AutomationRule with council assignment)
        
        # Simulate council audit data
        risk_flags = []
        governance_violations = []
        template_mismatches = []
        automation_conflicts = []
        
        # Get debug logs for council's automations
        logs = session.query(AutomationDebugLog).filter(
            AutomationDebugLog.timestamp >= cutoff_time
        ).all()
        
        # Analyze for governance issues
        high_risk_count = 0
        failed_workflows = 0
        
        for log in logs:
            # Check for high-risk actions without oversight
            if log.actions_taken:
                for action in log.actions_taken:
                    if 'social_post' in str(action).lower():
                        high_risk_count += 1
                        risk_flags.append({
                            'automation_id': log.automation_id,
                            'flag': 'HIGH_RISK_ACTION',
                            'severity': 'medium',
                            'message': 'Social post generation without council approval',
                            'timestamp': log.timestamp.isoformat() + 'Z'
                        })
            
            # Check for failures
            if log.result == EventResult.FAILED:
                failed_workflows += 1
                if log.errors:
                    governance_violations.append({
                        'automation_id': log.automation_id,
                        'violation': 'REPEATED_FAILURE',
                        'severity': 'high',
                        'message': f'Automation failed: {log.errors[0] if log.errors else "Unknown"}',
                        'timestamp': log.timestamp.isoformat() + 'Z'
                    })
        
        # Check for template mismatches
        template_mismatches.append({
            'automation_id': 'auto_weekly_social',
            'mismatch': 'DEPRECATED_TEMPLATE',
            'severity': 'low',
            'current_version': 'v2',
            'recommended_version': 'v3',
            'message': 'Using outdated template version'
        })
        
        # Check for conflicts
        automation_conflicts.append({
            'conflict_type': 'OVERLAPPING_SCHEDULES',
            'severity': 'medium',
            'automations': ['auto_weekly_social', 'auto_daily_social'],
            'message': 'Multiple social post automations may create duplicate content'
        })
        
        # Historical patterns
        total_executions = len(logs)
        successful = len([l for l in logs if l.result == EventResult.SUCCESS])
        skipped = len([l for l in logs if l.result == EventResult.SKIPPED])
        failed = len([l for l in logs if l.result == EventResult.FAILED])
        
        patterns = {
            'total_executions': total_executions,
            'success_rate': (successful / total_executions * 100) if total_executions > 0 else 0,
            'skip_rate': (skipped / total_executions * 100) if total_executions > 0 else 0,
            'failure_rate': (failed / total_executions * 100) if total_executions > 0 else 0,
            'high_risk_actions_count': high_risk_count,
            'governance_compliance_score': max(0, 100 - len(governance_violations) * 10)
        }
        
        return jsonify({
            'council_id': council_id,
            'audit_time': datetime.utcnow().isoformat() + 'Z',
            'period_days': days,
            'automations_monitored': 5,  # In production, count from AutomationRule
            'total_issues': len(risk_flags) + len(governance_violations) + len(template_mismatches) + len(automation_conflicts),
            'risk_flags': risk_flags,
            'governance_violations': governance_violations,
            'template_mismatches': template_mismatches,
            'automation_conflicts': automation_conflicts,
            'historical_patterns': patterns,
            'summary': {
                'critical_issues': len([v for v in governance_violations if v['severity'] == 'high']),
                'medium_issues': len([r for r in risk_flags if r['severity'] == 'medium']),
                'low_issues': len([t for t in template_mismatches if t['severity'] == 'low']),
                'requires_attention': len(governance_violations) > 0 or len(risk_flags) > 2
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()
