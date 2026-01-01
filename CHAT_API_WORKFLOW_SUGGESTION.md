# Enhanced Chat API - Dynamic Workflow Suggestion

## Overview

The chat API now supports **dynamic workflow type suggestion** based on user natural language requests. Instead of hard-coding workflow types, the agent:

1. Analyzes the user's request
2. Suggests matching workflow types from the catalog
3. Asks the user to choose
4. Gathers required inputs
5. Calculates ROI and creates the workflow

## API Flow

### 1. **SUGGEST Mode** - Agent analyzes request and suggests workflow types

**Request:**
```json
POST /api/chat
{
  "agent_id": "agent_jermaine_super_action",
  "message": "I need to automate follow-up messages to my customers",
  "mode": "suggest"
}
```

**Response:**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "suggest",
  "message": "I need to automate follow-up messages to my customers",
  "suggestions": [
    {
      "id": "customer_followup",
      "name": "Customer Follow-up Automation",
      "description": "Automate weekly follow-up messages to existing customers.",
      "category": "crm",
      "domain": "commerce",
      "relevance_score": 5
    }
  ],
  "reply": "I found 1 workflow type(s) that match your request. Which one would you like to set up?"
}
```

### 2. **CONFIRM Mode** - User selects workflow type, agent requests inputs

**Request:**
```json
POST /api/chat
{
  "agent_id": "agent_jermaine_super_action",
  "message": "Let's use Customer Follow-up Automation",
  "mode": "confirm",
  "context": {
    "workflow_type": "customer_followup"
  }
}
```

**Response:**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "confirm",
  "workflow_type": {
    "id": "customer_followup",
    "name": "Customer Follow-up Automation",
    "description": "Automate weekly follow-up messages to existing customers.",
    "category": "crm",
    "domain": "commerce",
    "required_inputs": [
      "tasks_per_week",
      "time_per_task_minutes",
      "hourly_wage",
      "automation_percent",
      "error_rate",
      "cost_per_error"
    ],
    "default_profile": {
      "value_per_accelerated_task": 0
    }
  },
  "reply": "Great! Let's set up Customer Follow-up Automation. I'll need some information: tasks_per_week, time_per_task_minutes, hourly_wage, automation_percent, error_rate, cost_per_error. You can provide these values and I'll calculate the savings and create the workflow."
}
```

### 3. **EXECUTE Mode** - User provides inputs, agent creates workflow

**Request:**
```json
POST /api/chat
{
  "agent_id": "agent_jermaine_super_action",
  "message": "Create the workflow with these settings",
  "mode": "execute",
  "context": {
    "workflow_type": "customer_followup",
    "calculator_inputs": {
      "tasks_per_week": 50,
      "time_per_task_minutes": 15,
      "hourly_wage": 30,
      "automation_percent": 0.8,
      "error_rate": 0.05,
      "cost_per_error": 20
    },
    "workflow_inputs": {
      "template": "Welcome back! We'd love to hear from you...",
      "frequency": "weekly"
    }
  }
}
```

**Response:**
```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "execute",
  "workflow_action": "77012988-1d88-4c4f-bf58-cecbeb941909",
  "workflow_type": "customer_followup",
  "savings": {
    "weekly_savings": 340.0,
    "monthly_savings": 1472.2,
    "yearly_savings": 17680.0,
    "hours_saved_per_week": 10.0,
    "error_savings_weekly": 40.0,
    "scaling_savings_weekly": 0.0,
    "total_weekly_savings": 340.0
  },
  "reply": "I've created a Customer Follow-up Automation workflow (ID: 77012988-1d88-4c4f-bf58-cecbeb941909). It's now running. I'll track performance and savings."
}
```

## Keyword-Based Matching

The system uses simple keyword matching to suggest workflows. Keywords are mapped for each workflow type:

- **customer_followup**: customer, follow-up, followup, crm, client, retention
- **invoice_reminders**: invoice, payment, reminder, billing, accounts receivable
- **content_scheduler**: content, post, social media, publish, schedule, blog, marketing
- **data_entry_automation**: data entry, input, form, spreadsheet, manual entry
- **report_generation**: report, analytics, dashboard, summary, statistics
- And more...

### Relevance Scoring

- **+1 point** per keyword match
- **+2 points** if category name mentioned
- **+3 points** if workflow name words mentioned

Top 3 matches returned, sorted by score.

## Testing

Run the test script to see the complete flow:

```bash
python test_chat_workflow_suggestion.py
```

This will test:
1. ✅ Full workflow suggestion flow (suggest → confirm → execute)
2. ✅ Multiple suggestions scenario
3. ✅ No match scenario (graceful handling)

## Future Enhancements

The keyword-based matching can be replaced with:

- **ML-based classification** using trained models
- **LLM-based intent detection** for more nuanced understanding
- **Context-aware suggestions** based on user history
- **Multi-turn clarification** for ambiguous requests

## Example User Flows

### Flow 1: Customer Automation
```
👤 "I need to automate follow-up messages"
🤖 Suggests: Customer Follow-up Automation
👤 Chooses workflow
🤖 Requests: tasks_per_week, time_per_task_minutes, etc.
👤 Provides inputs
🤖 Creates workflow with $340/week savings
```

### Flow 2: Content Marketing
```
👤 "Help me schedule social media posts"
🤖 Suggests: Content Publishing Scheduler
👤 Chooses workflow
🤖 Requests: posts_per_week, time_per_post_minutes, etc.
👤 Provides inputs
🤖 Creates workflow with calculated savings
```

### Flow 3: No Match
```
👤 "I want to build a rocket ship"
🤖 "I couldn't identify a specific workflow type..."
```

## Implementation Details

### Location
- **Flask Route**: `flask_dashboard.py` line 8188
- **Suggestion Function**: `flask_dashboard.py` line 8129
- **Workflow Catalog**: `workflow_catalog.py`
- **Test Script**: `test_chat_workflow_suggestion.py`

### Key Functions

1. **suggest_workflow_types(message)** - Analyzes user message and returns top 3 matches
2. **api_chat_unified()** - Main chat endpoint with 4 modes:
   - `chat`: Simple conversation
   - `suggest`: Analyze and suggest workflows
   - `confirm`: Display workflow details and inputs
   - `execute`: Calculate ROI and create workflow

## Status

✅ **FULLY OPERATIONAL**

- Suggestion engine working
- Multi-turn conversation flow implemented
- Test suite passing
- Ready for frontend integration

---

🔥 **The Flame Burns Sovereign and Eternal!** 👑
