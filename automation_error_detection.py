"""
Codex Dominion - Automation Error & Warning Detection System

Surfaces issues before they become problems:
- Missing data
- Invalid configuration
- Dormant automations
- Conflicting rules
- High-risk actions
- Governance violations

The Dominion protects the tenant.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


class IssueType(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AutomationIssue:
    """Represents an issue detected in automation configuration or execution"""
    
    def __init__(
        self,
        issue_type: IssueType,
        severity: IssueSeverity,
        code: str,
        message: str,
        automation_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        remediation: Optional[str] = None
    ):
        self.issue_type = issue_type
        self.severity = severity
        self.code = code
        self.message = message
        self.automation_id = automation_id
        self.details = details or {}
        self.remediation = remediation
        self.detected_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'issue_type': self.issue_type.value,
            'severity': self.severity.value,
            'code': self.code,
            'message': self.message,
            'automation_id': self.automation_id,
            'details': self.details,
            'remediation': self.remediation,
            'detected_at': self.detected_at.isoformat() + 'Z'
        }


class AutomationErrorDetector:
    """Detects errors and warnings in automation configuration and execution"""
    
    def __init__(self, session=None):
        self.session = session
        self.issues: List[AutomationIssue] = []
    
    def check_automation(
        self,
        automation_id: str,
        config: Dict[str, Any],
        recent_logs: List[Dict[str, Any]] = None
    ) -> List[AutomationIssue]:
        """
        Run all checks on an automation
        Returns list of detected issues
        """
        self.issues = []
        
        # Configuration checks
        self._check_missing_data(automation_id, config)
        self._check_invalid_config(automation_id, config)
        self._check_deprecated_templates(automation_id, config)
        
        # Execution history checks
        if recent_logs:
            self._check_dormant_automation(automation_id, recent_logs)
            self._check_repeated_failures(automation_id, recent_logs)
            self._check_performance_issues(automation_id, recent_logs)
        
        # Risk checks
        self._check_high_risk_actions(automation_id, config)
        self._check_conflicting_automations(automation_id, config)
        
        return self.issues
    
    def _check_missing_data(self, automation_id: str, config: Dict[str, Any]):
        """Check for missing or incomplete configuration data"""
        required_fields = ['trigger', 'conditions', 'action']
        
        for field in required_fields:
            if field not in config or not config[field]:
                self.issues.append(AutomationIssue(
                    issue_type=IssueType.ERROR,
                    severity=IssueSeverity.CRITICAL,
                    code='MISSING_CONFIG',
                    message=f'Missing required field: {field}',
                    automation_id=automation_id,
                    details={'missing_field': field},
                    remediation=f'Add {field} configuration to automation'
                ))
        
        # Check for missing condition values
        if 'conditions' in config:
            for idx, condition in enumerate(config.get('conditions', [])):
                if 'field' not in condition:
                    self.issues.append(AutomationIssue(
                        issue_type=IssueType.ERROR,
                        severity=IssueSeverity.HIGH,
                        code='MISSING_CONDITION_FIELD',
                        message=f'Condition {idx + 1} missing field specification',
                        automation_id=automation_id,
                        details={'condition_index': idx},
                        remediation='Specify which field this condition should evaluate'
                    ))
    
    def _check_invalid_config(self, automation_id: str, config: Dict[str, Any]):
        """Check for invalid configuration values"""
        # Check trigger schedule
        if config.get('trigger', {}).get('type') == 'schedule':
            schedule = config['trigger'].get('schedule')
            if not schedule:
                self.issues.append(AutomationIssue(
                    issue_type=IssueType.ERROR,
                    severity=IssueSeverity.HIGH,
                    code='INVALID_SCHEDULE',
                    message='Schedule trigger missing schedule configuration',
                    automation_id=automation_id,
                    remediation='Add schedule (e.g., "weekly", "daily", "0 9 * * *")'
                ))
        
        # Check condition operators
        valid_operators = ['equals', 'not_equals', 'greater_than', 'less_than', 'contains']
        if 'conditions' in config:
            for idx, condition in enumerate(config.get('conditions', [])):
                operator = condition.get('operator')
                if operator and operator not in valid_operators:
                    self.issues.append(AutomationIssue(
                        issue_type=IssueType.ERROR,
                        severity=IssueSeverity.MEDIUM,
                        code='INVALID_OPERATOR',
                        message=f'Condition {idx + 1} uses invalid operator: {operator}',
                        automation_id=automation_id,
                        details={'condition_index': idx, 'invalid_operator': operator},
                        remediation=f'Use one of: {", ".join(valid_operators)}'
                    ))
    
    def _check_deprecated_templates(self, automation_id: str, config: Dict[str, Any]):
        """Check for deprecated template versions"""
        action_type = config.get('action', {}).get('type')
        template_version = config.get('action', {}).get('template_version')
        
        deprecated_templates = {
            'social_post_generation': ['v1', 'v2'],  # v3+ is current
            'product_bundling': ['v1'],  # v2+ is current
        }
        
        if action_type in deprecated_templates:
            if template_version in deprecated_templates[action_type]:
                self.issues.append(AutomationIssue(
                    issue_type=IssueType.WARNING,
                    severity=IssueSeverity.MEDIUM,
                    code='DEPRECATED_TEMPLATE',
                    message=f'Using deprecated template version: {template_version}',
                    automation_id=automation_id,
                    details={
                        'action_type': action_type,
                        'current_version': template_version,
                        'recommended_version': 'v3'
                    },
                    remediation='Update to latest template version for improved features'
                ))
    
    def _check_dormant_automation(self, automation_id: str, recent_logs: List[Dict[str, Any]]):
        """Check if automation hasn't fired in a long time"""
        if not recent_logs:
            self.issues.append(AutomationIssue(
                issue_type=IssueType.WARNING,
                severity=IssueSeverity.LOW,
                code='DORMANT_AUTOMATION',
                message='Automation has no execution history',
                automation_id=automation_id,
                details={'days_since_last_run': None},
                remediation='Verify automation is configured correctly and trigger conditions are reachable'
            ))
            return
        
        # Get most recent execution
        latest_log = max(recent_logs, key=lambda x: x.get('timestamp', ''))
        latest_time = datetime.fromisoformat(latest_log['timestamp'].replace('Z', ''))
        days_since = (datetime.utcnow() - latest_time).days
        
        if days_since > 30:
            self.issues.append(AutomationIssue(
                issue_type=IssueType.WARNING,
                severity=IssueSeverity.MEDIUM,
                code='DORMANT_AUTOMATION',
                message=f'Automation hasn\'t fired in {days_since} days',
                automation_id=automation_id,
                details={'days_since_last_run': days_since, 'last_run': latest_log['timestamp']},
                remediation='Review trigger conditions or disable if no longer needed'
            ))
    
    def _check_repeated_failures(self, automation_id: str, recent_logs: List[Dict[str, Any]]):
        """Check for repeated failures indicating systemic issues"""
        if len(recent_logs) < 3:
            return
        
        # Get last 5 executions
        sorted_logs = sorted(recent_logs, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
        failed_logs = [log for log in sorted_logs if log.get('result') == 'failed']
        
        failure_rate = len(failed_logs) / len(sorted_logs)
        
        if failure_rate >= 0.6:  # 60% failure rate
            self.issues.append(AutomationIssue(
                issue_type=IssueType.ERROR,
                severity=IssueSeverity.HIGH,
                code='HIGH_FAILURE_RATE',
                message=f'Automation failing {int(failure_rate * 100)}% of the time',
                automation_id=automation_id,
                details={
                    'failure_rate': failure_rate,
                    'recent_executions': len(sorted_logs),
                    'failed_executions': len(failed_logs),
                    'common_errors': self._extract_common_errors(failed_logs)
                },
                remediation='Review error logs and fix underlying issues'
            ))
    
    def _check_performance_issues(self, automation_id: str, recent_logs: List[Dict[str, Any]]):
        """Check for performance degradation"""
        execution_times = [
            log.get('execution_time_ms', 0) 
            for log in recent_logs 
            if log.get('execution_time_ms')
        ]
        
        if not execution_times:
            return
        
        avg_time = sum(execution_times) / len(execution_times)
        
        # Warn if average execution time exceeds 10 seconds
        if avg_time > 10000:
            self.issues.append(AutomationIssue(
                issue_type=IssueType.WARNING,
                severity=IssueSeverity.LOW,
                code='SLOW_EXECUTION',
                message=f'Average execution time is {avg_time / 1000:.1f} seconds',
                automation_id=automation_id,
                details={
                    'avg_execution_ms': avg_time,
                    'max_execution_ms': max(execution_times),
                    'min_execution_ms': min(execution_times)
                },
                remediation='Optimize automation logic or break into smaller workflows'
            ))
    
    def _check_high_risk_actions(self, automation_id: str, config: Dict[str, Any]):
        """Flag high-risk actions that need careful monitoring"""
        high_risk_actions = [
            'social_post_generation',
            'email_campaign',
            'price_update',
            'inventory_deletion'
        ]
        
        action_type = config.get('action', {}).get('type')
        
        if action_type in high_risk_actions:
            self.issues.append(AutomationIssue(
                issue_type=IssueType.INFO,
                severity=IssueSeverity.MEDIUM,
                code='HIGH_RISK_ACTION',
                message=f'This automation performs high-risk action: {action_type}',
                automation_id=automation_id,
                details={'action_type': action_type},
                remediation='Ensure proper testing and monitoring. Consider adding council oversight.'
            ))
    
    def _check_conflicting_automations(self, automation_id: str, config: Dict[str, Any]):
        """Check for automations that might conflict with each other"""
        # This would query the database for similar automations
        # For now, we'll simulate based on action type
        
        action_type = config.get('action', {}).get('type')
        
        # Simulated conflicts (in production, query database)
        potential_conflicts = {
            'social_post_generation': ['auto_daily_social', 'auto_weekly_social'],
            'price_update': ['auto_sale_pricing', 'auto_dynamic_pricing']
        }
        
        if action_type in potential_conflicts:
            conflicts = [aid for aid in potential_conflicts[action_type] if aid != automation_id]
            if conflicts:
                self.issues.append(AutomationIssue(
                    issue_type=IssueType.WARNING,
                    severity=IssueSeverity.MEDIUM,
                    code='POTENTIAL_CONFLICT',
                    message=f'Similar automations detected: {", ".join(conflicts)}',
                    automation_id=automation_id,
                    details={
                        'action_type': action_type,
                        'conflicting_automations': conflicts
                    },
                    remediation='Review automation logic to ensure they don\'t interfere with each other'
                ))
    
    def _extract_common_errors(self, failed_logs: List[Dict[str, Any]]) -> List[str]:
        """Extract most common error messages"""
        errors = []
        for log in failed_logs:
            if log.get('errors'):
                errors.extend(log['errors'])
        
        # Return unique errors
        return list(set(errors))[:3]  # Top 3


def detect_automation_issues(
    automation_id: str,
    config: Dict[str, Any],
    recent_logs: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main entry point for error detection
    
    Returns:
    {
        'automation_id': str,
        'checked_at': str,
        'total_issues': int,
        'errors': [...],
        'warnings': [...],
        'info': [...]
    }
    """
    detector = AutomationErrorDetector()
    issues = detector.check_automation(automation_id, config, recent_logs)
    
    errors = [i.to_dict() for i in issues if i.issue_type == IssueType.ERROR]
    warnings = [i.to_dict() for i in issues if i.issue_type == IssueType.WARNING]
    info = [i.to_dict() for i in issues if i.issue_type == IssueType.INFO]
    
    return {
        'automation_id': automation_id,
        'checked_at': datetime.utcnow().isoformat() + 'Z',
        'total_issues': len(issues),
        'health_score': calculate_health_score(errors, warnings, info),
        'errors': errors,
        'warnings': warnings,
        'info': info,
        'summary': {
            'critical_count': len([e for e in errors if e['severity'] == 'critical']),
            'high_count': len([i for i in issues if i.severity == IssueSeverity.HIGH]),
            'medium_count': len([i for i in issues if i.severity == IssueSeverity.MEDIUM]),
            'low_count': len([i for i in issues if i.severity == IssueSeverity.LOW])
        }
    }


def calculate_health_score(errors: List[Dict], warnings: List[Dict], info: List[Dict]) -> int:
    """
    Calculate automation health score (0-100)
    100 = perfect, 0 = critical issues
    """
    score = 100
    
    # Deduct points for issues
    for error in errors:
        severity = error['severity']
        if severity == 'critical':
            score -= 25
        elif severity == 'high':
            score -= 15
        elif severity == 'medium':
            score -= 10
        else:
            score -= 5
    
    for warning in warnings:
        severity = warning['severity']
        if severity == 'high':
            score -= 10
        elif severity == 'medium':
            score -= 5
        else:
            score -= 2
    
    return max(0, score)  # Don't go below 0
