# Workflow Engine Integration Guide

## 🔥 Codex Dominion Workflow Engine

The Workflow Engine is an action tracking system that integrates with the Calculator module to create, track, and execute automation workflows with ROI metrics.

## Architecture

```
Calculator Module (calculators.py)
    ↓ Computes ROI
Workflow Engine (workflow_engine.py)
    ↓ Tracks Actions
Flask API (flask_dashboard.py)
    ↓ Exposes Endpoints
Jermaine Agent / External Systems
```

## Core Components

### 1. WorkflowAction (Dataclass)
```python
@dataclass
class WorkflowAction:
    id: str                           # UUID
    action_type: str                  # e.g., "customer_followup"
    created_by_agent: str             # e.g., "jermaine_super_action_ai"
    inputs: Dict[str, Any]            # Original calculation inputs
    calculated_savings: Dict[str, Any] # ROI metrics from calculator
    status: ActionStatus              # pending → running → completed/failed
    created_at: float                 # Unix timestamp
    updated_at: float                 # Unix timestamp
```

### 2. WorkflowEngine (Singleton)
- **create_action()**: Create new workflow with inputs and savings
- **update_status()**: Change action status (pending/running/completed/failed)
- **get_action()**: Retrieve action details by ID
- **list_actions()**: Get all actions

## API Endpoints

### List/Create Actions
```http
GET  /api/workflows/actions
POST /api/workflows/actions
```

**GET Response:**
```json
{
  "success": true,
  "count": 1,
  "actions": {
    "3e66f15a-4740-42a6-a5ae-3174ac4b989f": {
      "id": "3e66f15a-4740-42a6-a5ae-3174ac4b989f",
      "action_type": "customer_followup",
      "created_by_agent": "jermaine_super_action_ai",
      "status": "completed",
      "inputs": {...},
      "calculated_savings": {...}
    }
  }
}
```

**POST Request:**
```json
{
  "action_type": "customer_followup",
  "created_by_agent": "jermaine_super_action_ai",
  "inputs": {
    "tasks_per_week": 200,
    "time_per_task_minutes": 10,
    "hourly_wage": 25,
    "automation_percent": 0.7
  },
  "calculated_savings": {
    "weekly_savings": 793.33,
    "yearly_savings": 41253.33,
    "effectiveness": "STELLAR"
  }
}
```

**POST Response (201 Created):**
```json
{
  "success": true,
  "action_id": "3e66f15a-4740-42a6-a5ae-3174ac4b989f",
  "status": "pending",
  "created_at": 1703001234.567
}
```

### Get/Update Action
```http
GET   /api/workflows/actions/<action_id>
PATCH /api/workflows/actions/<action_id>
```

**PATCH Request:**
```json
{
  "status": "running"  // or "completed", "failed"
}
```

### Execute Action
```http
POST /api/workflows/actions/<action_id>/execute
```
Changes status from "pending" → "running"

## Complete Workflow Example

### 1. Calculate Savings
```python
# Using Calculator API
import requests

calc_response = requests.post("http://localhost:5000/api/calculators/savings", json={
    "tasks_per_week": 200,
    "time_per_task_minutes": 10,
    "hourly_wage": 25,
    "automation_percent": 0.7,
    "error_rate": 0.1,
    "cost_per_error": 15,
    "value_per_accelerated_task": 0
})

savings = calc_response.json()
# {
#   "weekly_savings": 793.33,
#   "yearly_savings": 41253.33,
#   "effectiveness": "STELLAR",
#   ...
# }
```

### 2. Create Workflow Action
```python
# Create action with calculated savings
workflow_response = requests.post("http://localhost:5000/api/workflows/actions", json={
    "action_type": "customer_followup",
    "created_by_agent": "jermaine_super_action_ai",
    "inputs": {
        "tasks_per_week": 200,
        "time_per_task_minutes": 10,
        "hourly_wage": 25,
        "automation_percent": 0.7
    },
    "calculated_savings": savings
})

action_id = workflow_response.json()["action_id"]
# "3e66f15a-4740-42a6-a5ae-3174ac4b989f"
```

### 3. Execute Action
```python
# Start execution
requests.post(f"http://localhost:5000/api/workflows/actions/{action_id}/execute")
# Status changes: pending → running
```

### 4. Update Status
```python
# Mark as completed
requests.patch(
    f"http://localhost:5000/api/workflows/actions/{action_id}",
    json={"status": "completed"}
)
```

### 5. Retrieve Action
```python
# Get details
response = requests.get(f"http://localhost:5000/api/workflows/actions/{action_id}")
action = response.json()["action"]

print(f"Action: {action['action_type']}")
print(f"Status: {action['status']}")
print(f"Yearly Savings: ${action['calculated_savings']['yearly_savings']:,.2f}")
# Action: customer_followup
# Status: completed
# Yearly Savings: $41,253.33
```

## Integration with Jermaine Agent

Update `jermaine_agent_core.py` to use the workflow engine:

```python
import requests

class JermaineSuperActionAI:
    def __init__(self):
        self.api_base = "http://localhost:5000"
    
    def create_workflow_with_savings(self, workflow_data):
        """Calculate savings and create workflow action"""
        # 1. Calculate ROI
        savings_response = requests.post(
            f"{self.api_base}/api/calculators/savings",
            json={
                "tasks_per_week": workflow_data["tasks_per_week"],
                "time_per_task_minutes": workflow_data["time_per_task_minutes"],
                "hourly_wage": workflow_data["hourly_wage"],
                "automation_percent": workflow_data["automation_percent"],
                "error_rate": workflow_data.get("error_rate", 0.1),
                "cost_per_error": workflow_data.get("cost_per_error", 15),
                "value_per_accelerated_task": workflow_data.get("value_per_accelerated_task", 0)
            }
        )
        savings = savings_response.json()
        
        # 2. Create workflow action
        action_response = requests.post(
            f"{self.api_base}/api/workflows/actions",
            json={
                "action_type": workflow_data["action_type"],
                "created_by_agent": "jermaine_super_action_ai",
                "inputs": workflow_data,
                "calculated_savings": savings
            }
        )
        
        return action_response.json()
```

## Status Lifecycle

```
pending → running → completed
                 ↘ failed
```

- **pending**: Action created, awaiting execution
- **running**: Execution in progress
- **completed**: Successfully finished
- **failed**: Execution error

## Testing

Run the test suite:

```bash
# Start Flask server
$env:FLASK_APP = "flask_dashboard.py"
.\.venv\Scripts\python.exe -m flask run --host=0.0.0.0 --port=5000 --no-reload

# In another terminal
.\.venv\Scripts\python.exe test_workflow_engine.py
```

Expected output:
```
✅ Action created: 3e66f15a-4740-42a6-a5ae-3174ac4b989f
✅ Action retrieved
✅ Action execution started
✅ Action completed
✅ Retrieved 1 action(s)
✅ All workflow engine tests passed!
```

## API Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/workflows/actions` | GET | List all actions |
| `/api/workflows/actions` | POST | Create new action |
| `/api/workflows/actions/<id>` | GET | Get action details |
| `/api/workflows/actions/<id>` | PATCH | Update action status |
| `/api/workflows/actions/<id>/execute` | POST | Start execution |

## Data Flow

```
User Input (Tasks, Time, Wage)
    ↓
Calculator Module (calculators.py)
    ↓ Computes ROI
Savings Result ($41,253.33/year, STELLAR)
    ↓
Workflow Engine (workflow_engine.py)
    ↓ Creates Action
Tracked Workflow (pending → running → completed)
    ↓
Flask API Endpoints
    ↓ Exposes to
External Systems / Jermaine Agent
```

## Future Enhancements

1. **Persistence**: Save actions to `codex_ledger.json`
2. **Notifications**: Alert on status changes
3. **Scheduling**: Execute actions at specific times
4. **History**: Track action execution history
5. **Analytics**: Dashboard for workflow ROI metrics
6. **Webhooks**: Trigger external systems on completion

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**

**System Status**: Workflow Engine OPERATIONAL ✅
**Last Updated**: December 19, 2025
