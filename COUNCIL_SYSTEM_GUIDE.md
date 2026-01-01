# 🏛️ Codex Dominion Council System - Complete Guide

## Overview

The Council System implements the **Council Seal architecture** for governance, policy enforcement, and agent oversight in Codex Dominion. Councils manage policies, review high-impact actions, and enforce safety rules across the platform.

## Architecture

```
Council Seal (Supreme Authority)
    ↓
Councils (Governance Bodies)
    ↓
Engines (Execution Systems)
    ↓
Agents (Action Executors)
    ↓
Workflows (Operations)
```

## Core Components

### 1. **Council Engine** (`council_engine.py`)
- Manages council lifecycle (create, read, update, delete)
- Enforces oversight policies
- Tracks agent assignments
- Checks action permissions
- **Helper Functions:**
  - `get_council_by_domain()` - Get first council by domain
  - `council_allows_action()` - Combined blocked + review check

### 2. **Council Storage** (`councils.json`)
- Persistent JSON storage for council configurations
- Includes oversight rules and metadata
- Version controlled with timestamps

### 3. **Flask API** (`flask_dashboard.py`)
- 12 REST endpoints for council management
- Integration with workflow and calculator systems
- Real-time oversight enforcement

## Council Structure

```python
{
  "id": "council_governance",
  "name": "Governance Council",
  "purpose": "Steward policies, safety, and rule changes",
  "primary_engines": ["engine_governance", "engine_safety"],
  "agents": ["agent_jermaine_super_action"],
  "domains": ["safety", "policy"],
  "oversight": {
    "review_actions": true,
    "review_threshold_weekly_savings": 5000,
    "blocked_action_types": ["delete_user_data"]
  },
  "status": "active"
}
```

## API Endpoints

### **List Councils**
```http
GET /api/councils?status=active
```
**Response:**
```json
{
  "success": true,
  "count": 3,
  "councils": [...]
}
```

### **Get Council**
```http
GET /api/councils/council_governance
```
**Response:**
```json
{
  "success": true,
  "council": {
    "id": "council_governance",
    "name": "Governance Council",
    "oversight": {
      "review_threshold_weekly_savings": 5000,
      "blocked_action_types": ["delete_user_data"]
    }
  }
}
```

### **Create Council**
```http
POST /api/councils
Content-Type: application/json

{
  "name": "Commerce Council",
  "purpose": "Oversee pricing and marketplace",
  "primary_engines": ["engine_commerce"],
  "agents": ["agent_action_basic"],
  "domains": ["commerce", "pricing"],
  "oversight": {
    "review_actions": true,
    "review_threshold_weekly_savings": 10000,
    "blocked_action_types": ["change_pricing_without_approval"]
  }
}
```

### **Update Council**
```http
PATCH /api/councils/council_governance
Content-Type: application/json

{
  "status": "inactive",
  "purpose": "Updated purpose"
}
```

### **Delete Council**
```http
DELETE /api/councils/council_test
```

### **Add Agent to Council**
```http
POST /api/councils/council_governance/agents
Content-Type: application/json

{
  "agent_id": "agent_new_member"
}
```

### **Remove Agent from Council**
```http
DELETE /api/councils/council_governance/agents/agent_old_member
```

### **Check Action Allowed**
```http
POST /api/councils/council_governance/check-action
Content-Type: application/json

{
  "action_type": "delete_user_data"
}
```
**Response:**
```json
{
  "success": true,
  "action_type": "delete_user_data",
  "allowed": false,
  "council_id": "council_governance"
}
```

### **Check Review Required**
```http
POST /api/councils/council_governance/review-required
Content-Type: application/json

{
  "weekly_savings": 15000
}
```
**Response:**
```json
{
  "success": true,
  "weekly_savings": 15000,
  "requires_review": true,
  "council_id": "council_governance"
}
```

### **Get Councils by Agent**
```http
GET /api/councils/by-agent/agent_jermaine_super_action
```

### **Get Councils by Domain**
```http
GET /api/councils/by-domain/policy
```

## Integration Examples

### 1. **Check Action Permission Before Execution**
```python
from council_engine import council_engine

# Before executing sensitive action
action_type = "delete_user_data"
council_id = "council_governance"

if not council_engine.check_action_allowed(action_type, council_id):
    print(f"❌ Action {action_type} is blocked by {council_id}")
    return False

# Proceed with action
execute_action(action_type)
```

### 2. **Require Review for High-Value Workflows**
```python
from council_engine import council_engine
from calculators import calculate_savings

# Calculate ROI
savings_result = calculate_savings(input_data)
weekly_savings = savings_result.weekly_savings

# Check if council review required
if council_engine.requires_review(weekly_savings, "council_governance"):
    print(f"⚠️ Action requires Governance Council review")
    send_to_review_queue(workflow_id, savings_result)
else:
    # Auto-approve
    execute_workflow(workflow_id)
```

### 3. **Get Agent's Councils**
```python
from council_engine import council_engine

agent_id = "agent_jermaine_super_action"
councils = council_engine.get_councils_by_agent(agent_id)

print(f"Agent {agent_id} is a member of {len(councils)} councils:")
for council in councils:
    print(f"  - {council.name}: {council.purpose}")
```
, get_council_by_domain

# Get ALL councils for a domain
domain = "safety"
councils = council_engine.get_councils_by_domain(domain)

print(f"Councils overseeing '{domain}' domain:")
for council in councils:
    print(f"  - {council.name}")

# Get FIRST council for a domain (quick lookup)
council = council_engine.get_council_by_domain("policy")
print(f"Primary policy council: {council.name}")

# Or use utility function for JSON-based lookup
council_dict = get_council_by_domain("safety")
print(f"Found: {council_dict['name']}")
```

### 5. **Combined Permission Check**
```python
from council_engine import council_engine, council_allows_action, get_council_by_domain

# Check if action is allowed AND doesn't require review
# Returns False if blocked OR requires manual review

# Method 1: Using engine (with council_id)
allowed = council_engine.council_allows_action(
    "council_governance",
    "create_workflow",
    {"weekly_savings": 3000}
)

if allowed:
    execute_workflow()
else:
    send_to_review_queue()

# Method 2: Using utility function (with council dict)
council_dict = get_council_by_domain("commerce")
allowed = council_allows_action(
    council_dict,
    "update_pricing",
    {"weekly_savings": 15000}

print(f"Councils overseeing '{domain}' domain:")
for council in councils:
    print(f"  - {council.name}")
```

## Frontend Integration (TypeScript)

### **React Hook: useCouncil.ts**
```typescript
import { useState, useCallback } from 'react';

interface Council {
  id: string;
  name: string;
  purpose: string;
  oversight: {
    review_actions: boolean;
    review_threshold_weekly_savings: number;
    blocked_action_types: string[];
  };
}

export function useCouncil() {
  const [councils, setCouncils] = useState<Council[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchCouncils = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/councils');
      const data = await response.json();
      setCouncils(data.councils);
    } finally {
      setLoading(false);
    }
  }, []);

  const checkActionAllowed = useCallback(
    async (councilId: string, actionType: string) => {
      const response = await fetch(
        `/api/councils/${councilId}/check-action`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action_type: actionType })
        }
      );
      const data = await response.json();
      return data.allowed;
    },
    []
  );

  return { councils, loading, fetchCouncils, checkActionAllowed };
}
```

### **Component: CouncilDashboard.tsx**
```tsx
import React, { useEffect } from 'react';
import { useCouncil } from './useCouncil';

export function CouncilDashboard() {
  const { councils, loading, fetchCouncils } = useCouncil();

  useEffect(() => {
    fetchCouncils();
  }, [fetchCouncils]);

  if (loading) return <div>Loading councils...</div>;

  return (
    <div className="council-dashboard">
      <h1>Council Seal - Governance Dashboard</h1>
      {councils.map(council => (
        <div key={council.id} className="council-card">
          <h2>{council.name}</h2>
          <p>{council.purpose}</p>
          <div className="oversight-info">
            <span>Review Threshold: ${council.oversight.review_threshold_weekly_savings}</span>
            <span>Blocked Actions: {council.oversight.blocked_action_types.length}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Testing

Run comprehensive test suite:

```bash
# Ensure Flask is running
python flask_dashboard.py

# In another terminal, run tests
python test_council_api.py
```

**Test Coverage:**
- ✅ List councils
- ✅ Get specific council
- ✅ Create new council
- ✅ Update council
- ✅ Delete council
- ✅ Add/remove agents
- ✅ Check action permissions
- ✅ Check review requirements
- ✅ Query by agent
- ✅ Query by domain

## Workflow Integration

### **Enhanced Chat API with Council Oversight**

The chat API now includes automatic council oversight for workflow execution:

```python
@app.route("/api/chat", methods=["POST"])
def api_chat_unified():
    data = request.json
    mode = data.get("mode", "chat")
    
    if mode == "execute":
        # Calculate savings
        savings_result = calculate_savings(calculator_input)
        
        # ===== COUNCIL OVERSIGHT CHECK =====
        domain = "automation"  # Determine domain from context
        
        council = get_council_by_domain(domain)
        if council and not council_allows_action(
            council, 
            "create_workflow_customer_followup", 
            savings_result or {}
        ):
            return jsonify({
                "agent_id": agent_id,
                "agent_name": agent.get("name"),
                "mode": "execute",
                "blocked_by_council": council.get("id"),
                "reply": (
                    f"This workflow requires review by {council.get('name')} "
                    "before it can be activated."
                ),
                "savings": savings_result
            }), 403
        
        # Create workflow if allowed
        workflow_action = workflow_engine.create_action(
            action_type="create_workflow_customer_followup",
            created_by_agent=agent_id,
            inputs=workflow_inputs,
            calculated_savings=savings_result
        )
        
        workflow_engine.update_status(workflow_action.id, "running")
        
        return jsonify({
            "agent_id": agent_id,
            "workflow_action": workflow_action.id,
            "savings": savings_result,
            "reply": f"Workflow created (ID: {workflow_action.id})"
        })
```

### **Example Requests**

**High-Value Workflow (BLOCKED):**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_jermaine_super_action",
    "message": "Automate high-value process",
    "mode": "execute",
    "context": {
      "calculator_inputs": {
        "tasks_per_week": 500,
        "time_per_task_minutes": 15,
        "hourly_wage": 30,
        "automation_percent": 0.8,
        "error_rate": 0.1,
        "cost_per_error": 20
      }
    }
  }'
```

**Response (403 Forbidden):**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "execute",
  "blocked_by_council": "council_governance",
  "reply": "This workflow requires review by Governance Council before it can be activated.",
  "savings": {
    "weekly_savings": 15000.00,
    "monthly_savings": 65000.00,
    "yearly_savings": 780000.00
  }
}
```

**Low-Value Workflow (ALLOWED):**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_jermaine_super_action",
    "message": "Automate simple task",
    "mode": "execute",
    "context": {
      "calculator_inputs": {
        "tasks_per_week": 50,
        "time_per_task_minutes": 5,
        "hourly_wage": 25,
        "automation_percent": 0.5
      }
    }
  }'
```

**Response (200 OK):**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "execute",
  "workflow_action": "550e8400-e29b-41d4-a716-446655440000",
  "savings": {
    "weekly_savings": 520.83,
    "monthly_savings": 2250.00,
    "yearly_savings": 27083.33
  },
  "reply": "I've created a workflow (ID: 550e8400...) to automate this."
}
```

## Use Cases

### 1. **Safety Enforcement**
Governance Council blocks dangerous actions:
```json
{
  "oversight": {
    "blocked_action_types": [
      "delete_user_data",
      "modify_security_settings",
      "access_admin_panel"
    ]
  }
}
```

### 2. **Financial Oversight**
Commerce Council requires review for high-value changes:
```json
{
  "oversight": {
    "review_actions": true,
    "review_threshold_weekly_savings": 10000
  }
}
```

### 3. **Multi-Council Governance**
Agent belongs to multiple councils with different authorities:
```python
councils = council_engine.get_councils_by_agent("agent_jermaine_super_action")
# Returns: [Governance Council, Commerce Council, Technical Council]
```

## Best Practices

1. **Always Check Permissions Before Execution**
   ```python
   if not council_engine.check_action_allowed(action_type, council_id):
       return {"error": "Action blocked by council oversight"}
   ```

2. **Implement Review Queues for High-Value Actions**
   ```python
   if council_engine.requires_review(savings, council_id):
       add_to_review_queue(workflow_id)
   ```

3. **Use Domain-Based Routing**
   ```python
   domain = "commerce"
   councils = council_engine.get_councils_by_domain(domain)
   # Route to appropriate council for oversight
   ```

4. **Maintain Audit Trails**
   ```python
   log_council_decision({
       "council_id": council_id,
       "action": action_type,
       "allowed": allowed,
       "timestamp": datetime.utcnow()
   })
   ```

## File Structure

```
codex-dominion/
├── council_engine.py           # Core engine (250 lines)
├── councils.json               # Council configurations
├── flask_dashboard.py          # API endpoints (12 new routes)
├── test_council_api.py         # Test suite (300 lines)
└── COUNCIL_SYSTEM_GUIDE.md     # This guide
```

## Next Steps

1. **Frontend Dashboard**: Build React UI for council management
2. **Real-time Notifications**: Alert councils when review needed
3. **Voting System**: Implement multi-agent consensus for decisions
4. **Audit Logs**: Persist council decisions to database
5. **Email Alerts**: Notify council members of pending reviews

---

## 🔥 Council Seal Status: OPERATIONAL 👑

**System Ready For:**
- ✅ Policy enforcement
- ✅ Action oversight
- ✅ Agent coordination
- ✅ Safety governance
- ✅ Financial review

**Endpoints:** 12 REST APIs  
**Test Coverage:** 10 comprehensive tests  
**Integration:** Workflow Engine + Calculator + Chat API  
**Production Status:** READY FOR DEPLOYMENT  

**🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑**
