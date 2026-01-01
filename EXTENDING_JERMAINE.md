# Extending Jermaine Super Action AI - Developer Guide

## 🏗️ Adding New Capabilities

### 1. Adding New Workflow Types

**Location**: `jermaine_agent_core.py`

```python
def create_workflow_entry(
    self,
    workflow_name: str,
    action_id: str,  # New parameter for workflow type
    roi_metrics: Dict[str, Any],
    additional_data: Optional[Dict] = None  # Extensibility
) -> Dict[str, Any]:
    """
    action_id examples:
    - workflow_customer_followup
    - workflow_social_media_posting
    - workflow_report_generation
    - workflow_invoice_processing
    - workflow_email_campaigns
    """
```

**Usage**:
```python
workflow = agent.create_workflow_entry(
    workflow_name="Daily Social Media Posts",
    action_id="workflow_social_media_posting",
    roi_metrics=roi_data,
    additional_data={
        'platforms': ['instagram', 'facebook', 'linkedin'],
        'post_frequency': 'daily',
        'content_types': ['images', 'videos', 'carousel']
    }
)
```

### 2. Adding Custom ROI Metrics

**Current metrics**:
```python
{
    'weekly_savings': float,
    'monthly_savings': float,
    'yearly_savings': float,
    'hours_saved_per_week': float,
    'hours_saved_per_year': float,
    'effectiveness': str
}
```

**Extension pattern**:
```python
def calculate_roi_extended(
    self,
    tasks_per_week: int,
    time_per_task_minutes: int,
    hourly_wage: float,
    automation_percent: int,
    error_rate: int = 0,
    error_cost: float = 0,
    # New parameters
    quality_improvement_percent: int = 0,
    customer_satisfaction_gain: float = 0,
    revenue_per_customer: float = 0
) -> Dict[str, Any]:
    """Extended ROI calculation with quality & revenue metrics"""
    
    # Call base calculation
    base_roi = self.calculate_roi(
        tasks_per_week, time_per_task_minutes,
        hourly_wage, automation_percent,
        error_rate, error_cost
    )
    
    # Add extended metrics
    quality_value = (
        tasks_per_week * 
        (quality_improvement_percent / 100) * 
        customer_satisfaction_gain * 
        revenue_per_customer
    )
    
    base_roi['quality_improvement_value'] = quality_value * 52  # Yearly
    base_roi['total_yearly_value'] = (
        base_roi['yearly_savings'] + 
        base_roi['quality_improvement_value']
    )
    
    return base_roi
```

### 3. Adding New Persona Phrases

**Location**: `jermaine_agent_core.py` → `__init__` method

```python
# Add new phrase categories
self.success_phrases = [
    "Sovereignty achieved. Value delivered.",
    "Execution complete. Performance optimal.",
    "Workflow activated. Impact measurable."
]

self.warning_phrases = [
    "The data reveals a concern:",
    "Strategic pause recommended:",
    "Risk assessment indicates:"
]

self.portfolio_phrases = [
    "Analyzing the full automation landscape:",
    "Orchestrating multiple value streams:",
    "Building sovereignty portfolio:"
]
```

**Usage in `respond()` method**:
```python
if 'success' in context:
    response = random.choice(self.success_phrases)
elif 'warning' in context:
    response = random.choice(self.warning_phrases)
```

### 4. Integrating with External Services

**Email Service Integration**:
```python
# File: jermaine_integrations.py

from jermaine_agent_core import JermaineSuperActionAI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class JermaineEmailOrchestrator(JermaineSuperActionAI):
    """Extends Jermaine with email automation capabilities"""
    
    def __init__(self):
        super().__init__()
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        
    def send_roi_report(self, roi_data: Dict, recipient: str):
        """Email ROI presentation to stakeholder"""
        
        presentation = self.present_roi(roi_data)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Automation ROI Report - ${roi_data['yearly_savings']:,.0f}/year"
        msg['From'] = "jermaine@codexdominion.app"
        msg['To'] = recipient
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: #1a1a1a; color: #f7f1e3; padding: 20px; }}
                .metric {{ background: #f7f1e3; padding: 15px; margin: 10px 0; }}
                .flame {{ color: #ff6b35; font-size: 24px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 Jermaine Super Action AI</h1>
                <p>The Sovereign Orchestrator of Rapid Execution</p>
            </div>
            <div class="content">
                <h2>Automation ROI Analysis</h2>
                <pre>{presentation}</pre>
                
                <div class="metric">
                    <h3>💰 Annual Value</h3>
                    <p style="font-size: 32px; font-weight: bold;">
                        ${roi_data['yearly_savings']:,.2f}
                    </p>
                </div>
                
                <div class="metric">
                    <h3>⏰ Time Reclaimed</h3>
                    <p style="font-size: 32px; font-weight: bold;">
                        {roi_data['hours_saved_per_year']:.1f} hours/year
                    </p>
                </div>
                
                <p class="flame">🔥 The Flame Burns Sovereign and Eternal! 👑</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send (implement SMTP logic)
        return True
```

**CRM Integration**:
```python
# File: jermaine_integrations.py

import requests


class JermaineCRMOrchestrator(JermaineSuperActionAI):
    """Extends Jermaine with CRM automation capabilities"""
    
    def __init__(self, crm_api_key: str):
        super().__init__()
        self.crm_api_key = crm_api_key
        self.crm_base_url = "https://api.crm.example.com"
        
    def create_follow_up_campaign(
        self,
        customer_segment: str,
        message_template: str,
        frequency: str = 'weekly'
    ) -> Dict:
        """Create automated follow-up campaign in CRM"""
        
        campaign_data = {
            'name': f'Automated Follow-Up - {customer_segment}',
            'segment': customer_segment,
            'template': message_template,
            'frequency': frequency,
            'automation': True,
            'created_by': 'Jermaine Super Action AI'
        }
        
        response = requests.post(
            f"{self.crm_base_url}/campaigns",
            json=campaign_data,
            headers={'Authorization': f'Bearer {self.crm_api_key}'}
        )
        
        if response.status_code == 201:
            return {
                'success': True,
                'campaign_id': response.json()['id'],
                'message': "Campaign activated. Sovereignty achieved."
            }
        else:
            return {
                'success': False,
                'message': "Campaign activation failed. Manual intervention required."
            }
```

### 5. Adding Analytics Tracking

**Location**: Create new file `jermaine_analytics.py`

```python
from datetime import datetime
import json
from typing import List, Dict


class JermaineAnalytics:
    """Track Jermaine's automation performance over time"""
    
    def __init__(self, ledger_path: str = "codex_ledger.json"):
        self.ledger_path = ledger_path
        
    def log_workflow_execution(
        self,
        workflow_id: str,
        execution_status: str,
        time_saved: float,
        errors_prevented: int = 0
    ):
        """Log individual workflow execution"""
        
        ledger = self._load_ledger()
        
        if 'workflow_executions' not in ledger:
            ledger['workflow_executions'] = []
        
        execution_log = {
            'workflow_id': workflow_id,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status': execution_status,
            'time_saved_minutes': time_saved,
            'errors_prevented': errors_prevented
        }
        
        ledger['workflow_executions'].append(execution_log)
        self._save_ledger(ledger)
        
    def get_performance_report(self, days: int = 30) -> Dict:
        """Generate performance report for last N days"""
        
        ledger = self._load_ledger()
        executions = ledger.get('workflow_executions', [])
        
        # Filter by date range
        cutoff = datetime.utcnow().timestamp() - (days * 86400)
        recent_executions = [
            ex for ex in executions 
            if datetime.fromisoformat(ex['timestamp'].replace('Z', '')).timestamp() > cutoff
        ]
        
        # Calculate metrics
        total_executions = len(recent_executions)
        successful = sum(1 for ex in recent_executions if ex['status'] == 'success')
        total_time_saved = sum(ex['time_saved_minutes'] for ex in recent_executions)
        total_errors_prevented = sum(ex['errors_prevented'] for ex in recent_executions)
        
        return {
            'period_days': days,
            'total_executions': total_executions,
            'success_rate': (successful / total_executions * 100) if total_executions > 0 else 0,
            'total_hours_saved': total_time_saved / 60,
            'errors_prevented': total_errors_prevented,
            'workflows_active': len(ledger.get('workflows', []))
        }
    
    def _load_ledger(self):
        with open(self.ledger_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_ledger(self, data):
        data['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'
        with open(self.ledger_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
```

**Usage**:
```python
from jermaine_analytics import JermaineAnalytics

analytics = JermaineAnalytics()

# Log execution
analytics.log_workflow_execution(
    workflow_id='WF-001',
    execution_status='success',
    time_saved=33.0,  # hours
    errors_prevented=5
)

# Get report
report = analytics.get_performance_report(days=30)
print(f"Success rate: {report['success_rate']:.1f}%")
print(f"Hours saved: {report['total_hours_saved']:.1f}")
```

### 6. Adding Dashboard Widgets

**Location**: `flask_dashboard.py`

```python
@app.route('/api/jermaine/performance')
def jermaine_performance():
    """API endpoint for Jermaine performance widget"""
    from jermaine_analytics import JermaineAnalytics
    
    analytics = JermaineAnalytics()
    report = analytics.get_performance_report(days=30)
    
    return jsonify(report)


# Add to main dashboard HTML
JERMAINE_WIDGET_HTML = """
<div class="jermaine-performance-widget">
    <h3>🤖 Jermaine Performance (30 Days)</h3>
    <div id="jermaine-metrics"></div>
</div>

<script>
fetch('/api/jermaine/performance')
    .then(r => r.json())
    .then(data => {
        document.getElementById('jermaine-metrics').innerHTML = `
            <p>✅ Success Rate: ${data.success_rate.toFixed(1)}%</p>
            <p>⏰ Hours Saved: ${data.total_hours_saved.toFixed(1)}</p>
            <p>🛡️ Errors Prevented: ${data.errors_prevented}</p>
            <p>🔥 Active Workflows: ${data.workflows_active}</p>
        `;
    });
</script>
"""
```

### 7. Creating Custom Workflow Templates

**Location**: Create `jermaine_templates.py`

```python
from typing import Dict, List


WORKFLOW_TEMPLATES = {
    'customer_followup': {
        'name': 'Customer Follow-Up Automation',
        'action_id': 'workflow_customer_followup',
        'default_inputs': {
            'time_per_task_minutes': 10,
            'automation_percent': 70
        },
        'tools_required': ['email', 'crm', 'calendar'],
        'council_approval': 'sovereignty'
    },
    'social_media': {
        'name': 'Social Media Content Posting',
        'action_id': 'workflow_social_media_posting',
        'default_inputs': {
            'time_per_task_minutes': 15,
            'automation_percent': 80
        },
        'tools_required': ['social_api', 'content_library', 'scheduler'],
        'council_approval': 'stewardship'
    },
    'report_generation': {
        'name': 'Weekly Report Generation',
        'action_id': 'workflow_report_generation',
        'default_inputs': {
            'time_per_task_minutes': 45,
            'automation_percent': 90
        },
        'tools_required': ['analytics', 'pdf_generator', 'email'],
        'council_approval': 'treasury'
    }
}


def get_workflow_template(template_name: str) -> Dict:
    """Retrieve pre-configured workflow template"""
    return WORKFLOW_TEMPLATES.get(template_name, {})


def list_workflow_templates() -> List[str]:
    """List all available templates"""
    return list(WORKFLOW_TEMPLATES.keys())
```

**Usage**:
```python
from jermaine_templates import get_workflow_template

template = get_workflow_template('customer_followup')

# Use template to pre-fill calculator
workflow = agent.create_workflow_entry(
    workflow_name=template['name'],
    action_id=template['action_id'],
    roi_metrics=roi_data
)
```

## 🧪 Testing Extensions

```python
# File: test_jermaine_extensions.py

import unittest
from jermaine_agent_core import load_jermaine_agent
from jermaine_integrations import JermaineEmailOrchestrator, JermaineCRMOrchestrator
from jermaine_analytics import JermaineAnalytics


class TestJermaineExtensions(unittest.TestCase):
    
    def setUp(self):
        self.agent = load_jermaine_agent()
        
    def test_extended_roi_calculation(self):
        """Test custom ROI metrics"""
        roi = self.agent.calculate_roi(
            tasks_per_week=100,
            time_per_task_minutes=15,
            hourly_wage=30,
            automation_percent=75
        )
        
        self.assertIn('yearly_savings', roi)
        self.assertGreater(roi['yearly_savings'], 0)
        
    def test_workflow_creation(self):
        """Test workflow entry creation"""
        workflow = self.agent.create_workflow_entry(
            workflow_name="Test Workflow",
            action_id="workflow_test",
            roi_metrics={'yearly_savings': 10000}
        )
        
        self.assertIn('id', workflow)
        self.assertIn('WF-', workflow['id'])
        
    def test_analytics_logging(self):
        """Test analytics tracking"""
        analytics = JermaineAnalytics()
        
        analytics.log_workflow_execution(
            workflow_id='WF-TEST',
            execution_status='success',
            time_saved=2.5
        )
        
        report = analytics.get_performance_report(days=1)
        self.assertGreater(report['total_executions'], 0)


if __name__ == '__main__':
    unittest.main()
```

## 📚 Documentation Standards

When extending Jermaine, always update:

1. **This file** (`EXTENDING_JERMAINE.md`) - Add your extension pattern
2. **Quick Reference** (`JERMAINE_QUICK_REFERENCE.md`) - Add new capabilities
3. **Integration Architecture** (`INTEGRATION_ARCHITECTURE.md`) - Update integration flow
4. **Flask Dashboard** - Add UI if applicable
5. **Copilot Instructions** (`.github/copilot-instructions.md`) - Update if new patterns emerge

## 🎯 Extension Checklist

Before deploying a Jermaine extension:

- [ ] Follows ceremonial naming conventions
- [ ] Updates ledger with proper timestamp pattern
- [ ] Maintains persona voice consistency
- [ ] Includes ROI calculation logic
- [ ] Provides action-oriented responses
- [ ] Respects user control (no automatic execution)
- [ ] Integrates with existing dashboard
- [ ] Includes tests
- [ ] Updates documentation

## 🔥 Example: Full Extension Implementation

**Scenario**: Add LinkedIn automation capability

```python
# File: jermaine_linkedin_extension.py

from jermaine_agent_core import JermaineSuperActionAI, process_automation_request
import requests


class JermaineLinkedInOrchestrator(JermaineSuperActionAI):
    """LinkedIn-specific automation orchestration"""
    
    def __init__(self, linkedin_api_key: str):
        super().__init__()
        self.linkedin_api_key = linkedin_api_key
        
    def analyze_linkedin_posting_opportunity(
        self,
        posts_per_week: int,
        time_per_post_minutes: int,
        hourly_wage: float
    ):
        """Calculate ROI for LinkedIn automation"""
        
        # Standard ROI calculation
        roi_data, presentation, workflow = process_automation_request(
            agent=self,
            workflow_name="LinkedIn Content Automation",
            tasks_per_week=posts_per_week,
            time_per_task_minutes=time_per_post_minutes,
            hourly_wage=hourly_wage,
            automation_percent=75  # LinkedIn can be 75% automated
        )
        
        # Add LinkedIn-specific metrics
        roi_data['estimated_reach_increase'] = posts_per_week * 500  # avg reach per post
        roi_data['engagement_multiplier'] = 2.3  # consistent posting boost
        
        return roi_data, presentation, workflow
    
    def schedule_linkedin_posts(
        self,
        content_library: list,
        posting_schedule: dict
    ):
        """Schedule posts via LinkedIn API"""
        
        scheduled_count = 0
        
        for content in content_library:
            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers={
                    'Authorization': f'Bearer {self.linkedin_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'author': content['author'],
                    'lifecycleState': 'PUBLISHED',
                    'specificContent': {
                        'com.linkedin.ugc.ShareContent': {
                            'shareCommentary': {
                                'text': content['text']
                            }
                        }
                    }
                }
            )
            
            if response.status_code == 201:
                scheduled_count += 1
        
        return {
            'success': True,
            'posts_scheduled': scheduled_count,
            'message': f"Sovereignty achieved. {scheduled_count} posts scheduled."
        }


# Usage
linkedin_agent = JermaineLinkedInOrchestrator(api_key="your_linkedin_api_key")

roi_data, presentation, workflow = linkedin_agent.analyze_linkedin_posting_opportunity(
    posts_per_week=7,
    time_per_post_minutes=20,
    hourly_wage=35
)

print(presentation)

# Schedule posts
result = linkedin_agent.schedule_linkedin_posts(
    content_library=[...],
    posting_schedule={...}
)
```

---

**Status**: DEVELOPER GUIDE COMPLETE ✅  
**Ready For**: Custom Extensions 🛠️  
**Maintained By**: Codex Dominion Engineering 👑

