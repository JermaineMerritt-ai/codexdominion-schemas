# Automation Rules System - Complete Implementation Guide

> **Status:** Backend Complete | UI Specifications Ready | Integration Pending  
> **Last Updated:** December 20, 2025  
> **Components:** Database Models (2), API (13 endpoints), Worker (4 listeners), UI Specs (4 pages)

## 📋 Table of Contents

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [API Reference](#api-reference)
4. [Automation Worker Architecture](#automation-worker-architecture)
5. [UI Specifications](#ui-specifications)
6. [Integration Guide](#integration-guide)
7. [Testing Guide](#testing-guide)
8. [Expected Impact](#expected-impact)

---

## Overview

The Automation Rules System enables self-governing automation across Codex Dominion. Tenants can create rules that automatically trigger workflows, send notifications, generate campaigns, and perform actions based on:

- **Events** (product added, workflow completed, etc.)
- **Schedules** (daily, weekly, monthly, seasonal)
- **Thresholds** (metric crosses value)
- **Behaviors** (customer actions)

### System Architecture

```
Trigger Sources → Automation Worker → Condition Evaluator → Governance Checker → Action Executor → Notifications
     ↓                   ↓                    ↓                      ↓                   ↓               ↓
  Events            Event Listener      evaluate_conditions()   should_auto_approve()  execute_action()  notify_*()
  Schedules         Schedule Listener   
  Thresholds        Threshold Monitor   
  Behaviors         Behavior Tracker    
```

---

## Database Schema

### AutomationRule Model

**Table:** `automation_rules`

#### Core Fields

| Column | Type | Description |
|--------|------|-------------|
| `id` | String (PK) | automation_{uuid} |
| `tenant_id` | String (FK) | Owner tenant |
| `name` | String(255) | Rule name |
| `description` | Text | Rule description |
| `category` | String(100) | marketing, store, product, campaign, customer |
| `enabled` | Boolean | Active status |

#### Trigger Configuration

| Column | Type | Description |
|--------|------|-------------|
| `trigger_type` | Enum(TriggerType) | event, schedule, threshold, behavior |
| `trigger_config` | JSON | Type-specific configuration |

**Trigger Config Examples:**

```json
// EVENT
{
  "event_type": "product_added",
  "source": "store"
}

// SCHEDULE
{
  "pattern": "weekly",
  "day": "monday",
  "time": "09:00",
  "timezone": "UTC"
}

// THRESHOLD
{
  "metric": "product_count",
  "operator": "<",
  "value": 3
}

// BEHAVIOR
{
  "behavior_type": "abandoned_cart",
  "timeframe_hours": 24
}
```

#### Conditions

| Column | Type | Description |
|--------|------|-------------|
| `conditions` | JSON | Array of condition objects (all must pass) |

**Conditions Format:**

```json
[
  {
    "type": "product_count",
    "operator": "<",
    "value": 3
  },
  {
    "type": "store_status",
    "operator": "=",
    "value": "active"
  },
  {
    "type": "date",
    "operator": ">=",
    "value": "2025-12-01"
  }
]
```

**Supported Operators:** `=`, `!=`, `<`, `>`, `<=`, `>=`, `contains`, `not_contains`

#### Action Configuration

| Column | Type | Description |
|--------|------|-------------|
| `action_type` | Enum(ActionType) | What to do when triggered |
| `action_config` | JSON | Action-specific configuration |

**Action Config Examples:**

```json
// START_WORKFLOW
{
  "workflow_type_id": "website_creation",
  "template_id": "basic_site",
  "inputs": {"domain": "example.com"}
}

// SEND_NOTIFICATION
{
  "recipients": ["owner", "collaborators"],
  "message": "Low product count detected",
  "channels": ["email", "push"]
}

// GENERATE_CAMPAIGN
{
  "template_id": "seasonal_promo",
  "channels": ["email", "social"],
  "schedule": "immediate"
}

// ADD_PRODUCT
{
  "template_id": "holiday_product",
  "count": 5,
  "category": "seasonal"
}
```

#### Governance

| Column | Type | Description |
|--------|------|-------------|
| `risk_level` | Enum(RiskLevel) | low, medium, high, critical |
| `requires_approval` | Boolean | Needs council approval |
| `assigned_council_id` | String (FK) | Reviewing council |
| `auto_approval_rules` | JSON | Auto-approval conditions |

**Auto-Approval Rules Format:**

```json
{
  "max_budget": 100,
  "trusted_users_only": true,
  "business_hours_only": false,
  "max_frequency_per_day": 5
}
```

#### Execution Tracking

| Column | Type | Description |
|--------|------|-------------|
| `last_triggered_at` | DateTime | Last trigger time |
| `last_executed_at` | DateTime | Last execution time |
| `execution_count` | Integer | Total executions |
| `success_count` | Integer | Successful executions |
| `failure_count` | Integer | Failed executions |
| `average_execution_time_ms` | Float | Rolling average execution time |

#### Methods

```python
# Evaluate all conditions
automation.evaluate_conditions(context: Dict) -> bool

# Check auto-approval eligibility
automation.should_auto_approve(context: Dict) -> bool

# Record execution stats
automation.record_execution(success: bool, execution_time_ms: float)
```

### AutomationExecution Model

**Table:** `automation_executions`

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer (PK, Auto) | Execution ID |
| `automation_rule_id` | String (FK) | Parent automation |
| `tenant_id` | String (FK) | Owner tenant |
| `triggered_at` | DateTime | Trigger timestamp |
| `trigger_source` | String | event, scheduler, manual |
| `trigger_data` | JSON | Context that triggered execution |
| `conditions_met` | Boolean | All conditions passed |
| `condition_results` | JSON | Detailed condition results |
| `action_started_at` | DateTime | Action start time |
| `action_completed_at` | DateTime | Action completion time |
| `action_result` | JSON | Action execution result |
| `success` | Boolean | Overall success status |
| `error_message` | Text | Error details if failed |
| `execution_time_ms` | Float | Total execution time |
| `required_approval` | Boolean | Needed approval |
| `approved_by_user_id` | String | Approver (if applicable) |
| `approved_at` | DateTime | Approval timestamp |

---

## API Reference

### Base URL: `/api/automations`

### 1. List Automations

```http
GET /api/automations
```

**Query Params:**
- `tenant_id`: Filter by tenant
- `category`: marketing, store, product, campaign, customer
- `trigger_type`: event, schedule, threshold, behavior
- `enabled`: true/false
- `risk_level`: low, medium, high, critical

**Response:**
```json
{
  "automations": [...],
  "count": 10,
  "enabled_count": 8,
  "disabled_count": 2
}
```

### 2. Create Automation

```http
POST /api/automations
```

**Body:**
```json
{
  "tenant_id": "tenant_123",
  "name": "Low Product Alert",
  "description": "Alert when product count drops below 3",
  "category": "product",
  "trigger_type": "threshold",
  "trigger_config": {
    "metric": "product_count",
    "operator": "<",
    "value": 3
  },
  "conditions": [
    {
      "type": "store_status",
      "operator": "=",
      "value": "active"
    }
  ],
  "action_type": "send_notification",
  "action_config": {
    "recipients": ["owner"],
    "message": "Low product count"
  },
  "risk_level": "low",
  "requires_approval": false
}
```

**Response:**
```json
{
  "automation": {...},
  "message": "Automation rule created successfully"
}
```

### 3. Get Automation

```http
GET /api/automations/:id
```

**Response:**
```json
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
```

### 4. Update Automation

```http
PATCH /api/automations/:id
```

**Body:** Partial automation object

### 5. Delete Automation

```http
DELETE /api/automations/:id
```

### 6. Enable Automation

```http
POST /api/automations/:id/enable
```

### 7. Disable Automation

```http
POST /api/automations/:id/disable
```

### 8. Test Conditions

```http
POST /api/automations/:id/test-conditions
```

**Body:**
```json
{
  "context": {
    "product_count": 2,
    "store_status": "active"
  }
}
```

**Response:**
```json
{
  "conditions_met": true,
  "results": [
    {
      "condition": {...},
      "passed": true,
      "actual_value": 2,
      "expected_value": 3
    }
  ],
  "summary": "All 2 conditions passed",
  "would_execute": true
}
```

### 9. Execute Automation

```http
POST /api/automations/:id/execute
```

**Body:**
```json
{
  "context": {...},
  "trigger_source": "manual",
  "bypass_approval": false
}
```

### 10. Get Execution History

```http
GET /api/automations/:id/executions?limit=50&offset=0&success=true
```

### 11. Get Execution Stats

```http
GET /api/automations/:id/stats
```

**Response:**
```json
{
  "total_executions": 100,
  "success_count": 95,
  "failure_count": 5,
  "success_rate": 0.95,
  "avg_execution_time_ms": 523.4,
  "executions_by_day": [...],
  "failure_reasons": [...]
}
```

### 12. Recommend Automations

```http
POST /api/automations/recommend
```

**Body:**
```json
{
  "tenant_id": "tenant_123",
  "context": {
    "product_count": 2,
    "store_performance": "good",
    "recent_campaigns": 0,
    "seasonal_context": "holiday_season"
  }
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "name": "Low Product Alert",
      "description": "...",
      "relevance_score": 0.95,
      "reasoning": "Your product count is low...",
      "suggested_config": {...}
    }
  ],
  "count": 4
}
```

### 13. Get Plain English Summary

```http
GET /api/automations/:id/summary
```

**Response:**
```json
{
  "summary": "When product count drops below 3 in an active store, send a notification to the owner saying 'Low product count'.",
  "trigger_description": "Product count falls below 3",
  "conditions_description": "Store is active",
  "action_description": "Send notification to owner"
}
```

---

## Automation Worker Architecture

### Components

#### 1. Event Listener
- Listens for system events
- Maintains event queue
- Emits events: `product_added`, `workflow_completed`, `store_health_changed`, etc.

#### 2. Schedule Listener
- Checks schedules every minute
- Supports: daily, weekly, monthly, seasonal patterns
- Prevents duplicate triggers within same day

#### 3. Threshold Monitor
- Checks metrics every 5 minutes
- Monitors: `product_count`, `store_traffic`, `conversion_rate`, etc.
- Detects threshold crossings

#### 4. Behavior Tracker
- Checks behaviors every 10 minutes
- Tracks: `abandoned_cart`, `repeat_purchase`, `dormant_customer`, etc.
- Matches customers to behavior patterns

### Execution Pipeline

```
1. Trigger Detected
   ↓
2. Create AutomationExecution log
   ↓
3. Evaluate Conditions (evaluate_conditions)
   ↓ (if all pass)
4. Check Governance (should_auto_approve)
   ↓ (if approved or auto-approved)
5. Execute Action (execute_action)
   ↓
6. Record Results (record_execution)
   ↓
7. Send Notifications
```

### Action Handlers

- `action_start_workflow()` - Starts workflow from template
- `action_send_notification()` - Sends email/push/SMS
- `action_update_product()` - Modifies product data
- `action_generate_campaign()` - Creates marketing campaign
- `action_create_landing_page()` - Generates landing page
- `action_add_product()` - Adds new product
- `action_update_store()` - Updates store settings
- `action_generate_draft()` - Creates workflow draft

### Running the Worker

```bash
# Standalone
python automation_worker.py

# Or integrate into existing worker
from automation_worker import AutomationWorker
worker = AutomationWorker()
worker.start()
```

---

## UI Specifications

### 1. Automation Builder Page

**Route:** `/portal/automations/builder/[id]/page.tsx`

#### Layout: 6 Sections

```typescript
import { AutomationBuilderUI } from "@/components/automation/AutomationBuilderUI";

interface AutomationBuilderPageProps {
  params: { id: string };
}

export default async function AutomationBuilderPage({ params }: AutomationBuilderPageProps) {
  const automationId = params.id === 'new' ? null : params.id;
  const automation = automationId ? await fetchAutomation(automationId) : null;
  
  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <AutomationBuilderUI automation={automation} />
    </div>
  );
}
```

#### Section 1: Automation Info

```typescript
<Card>
  <CardHeader>
    <h2>Automation Details</h2>
  </CardHeader>
  <CardBody>
    <Input 
      label="Name" 
      value={name}
      onChange={setName}
      placeholder="Low Product Alert"
    />
    <Textarea 
      label="Description" 
      value={description}
      onChange={setDescription}
      placeholder="Alert when product count drops below 3"
    />
    <Select 
      label="Category" 
      value={category}
      onChange={setCategory}
      options={["marketing", "store", "product", "campaign", "customer"]}
    />
    <Toggle 
      label="Enabled" 
      value={enabled}
      onChange={setEnabled}
    />
  </CardBody>
</Card>
```

#### Section 2: Trigger Selector

```typescript
<Card>
  <CardHeader>
    <h2>When should this automation trigger?</h2>
  </CardHeader>
  <CardBody>
    <Tabs value={triggerType} onChange={setTriggerType}>
      <Tab value="event">Event</Tab>
      <Tab value="schedule">Schedule</Tab>
      <Tab value="threshold">Threshold</Tab>
      <Tab value="behavior">Behavior</Tab>
    </Tabs>
    
    {triggerType === 'event' && (
      <div className="space-y-4">
        <Select 
          label="Event Type"
          options={[
            "product_added",
            "workflow_completed",
            "store_health_changed",
            "marketing_site_deployed",
            "customer_signup"
          ]}
        />
        <Input label="Source" placeholder="store" />
      </div>
    )}
    
    {triggerType === 'schedule' && (
      <div className="space-y-4">
        <Select 
          label="Pattern"
          options={["daily", "weekly", "monthly", "seasonal"]}
        />
        {pattern === 'weekly' && (
          <Select 
            label="Day"
            options={["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]}
          />
        )}
        <TimeInput label="Time" />
        <Select label="Timezone" options={["UTC", "America/New_York", ...]} />
      </div>
    )}
    
    {triggerType === 'threshold' && (
      <div className="space-y-4">
        <Select 
          label="Metric"
          options={[
            "product_count",
            "store_traffic",
            "conversion_rate",
            "campaign_performance"
          ]}
        />
        <Select 
          label="Operator"
          options={["<", ">", "<=", ">=", "="]}
        />
        <NumberInput label="Value" />
      </div>
    )}
    
    {triggerType === 'behavior' && (
      <div className="space-y-4">
        <Select 
          label="Behavior Type"
          options={[
            "abandoned_cart",
            "product_viewed_not_bought",
            "repeat_purchase",
            "high_value_customer",
            "dormant_customer"
          ]}
        />
        <NumberInput label="Timeframe (hours)" />
      </div>
    )}
  </CardBody>
</Card>
```

#### Section 3: Condition Builder

```typescript
<Card>
  <CardHeader>
    <div className="flex items-center justify-between">
      <h2>Conditions (optional)</h2>
      <Button onClick={addCondition}>
        <Icon name="plus" /> Add Condition
      </Button>
    </div>
  </CardHeader>
  <CardBody>
    {conditions.map((condition, index) => (
      <div key={index} className="flex items-center gap-4 p-4 border rounded-lg">
        <Select 
          label="Type"
          value={condition.type}
          onChange={(val) => updateCondition(index, 'type', val)}
          options={[
            "product_count",
            "store_status",
            "workflow_status",
            "date",
            "customer_behavior"
          ]}
        />
        <Select 
          label="Operator"
          value={condition.operator}
          onChange={(val) => updateCondition(index, 'operator', val)}
          options={["=", "!=", "<", ">", "<=", ">=", "contains", "not_contains"]}
        />
        <Input 
          label="Value"
          value={condition.value}
          onChange={(val) => updateCondition(index, 'value', val)}
        />
        <Button variant="ghost" onClick={() => removeCondition(index)}>
          <Icon name="trash" />
        </Button>
      </div>
    ))}
    
    {conditions.length === 0 && (
      <div className="text-center py-8 text-slate-400">
        No conditions added. Automation will trigger without additional checks.
      </div>
    )}
  </CardBody>
</Card>
```

#### Section 4: Action Selector

```typescript
<Card>
  <CardHeader>
    <h2>What should happen when triggered?</h2>
  </CardHeader>
  <CardBody>
    <Select 
      label="Action Type"
      value={actionType}
      onChange={setActionType}
      options={[
        { value: "start_workflow", label: "Start Workflow" },
        { value: "send_notification", label: "Send Notification" },
        { value: "update_product", label: "Update Product" },
        { value: "generate_campaign", label: "Generate Campaign" },
        { value: "create_landing_page", label: "Create Landing Page" },
        { value: "add_product", label: "Add Product" },
        { value: "update_store", label: "Update Store" },
        { value: "generate_draft", label: "Generate Draft" }
      ]}
    />
    
    {actionType === 'start_workflow' && (
      <div className="space-y-4">
        <Select label="Workflow Type" options={workflowTypes} />
        <Select label="Template" options={templates} />
        <JsonEditor label="Inputs" value={actionConfig.inputs} />
      </div>
    )}
    
    {actionType === 'send_notification' && (
      <div className="space-y-4">
        <MultiSelect 
          label="Recipients"
          options={["owner", "collaborators", "councils"]}
        />
        <Textarea label="Message" />
        <MultiSelect 
          label="Channels"
          options={["email", "push", "sms"]}
        />
      </div>
    )}
    
    {actionType === 'generate_campaign' && (
      <div className="space-y-4">
        <Select label="Template" options={campaignTemplates} />
        <MultiSelect 
          label="Channels"
          options={["email", "social", "ads"]}
        />
      </div>
    )}
    
    {/* ... other action types ... */}
  </CardBody>
</Card>
```

#### Section 5: Governance Settings

```typescript
<Card>
  <CardHeader>
    <h2>Governance & Approval</h2>
  </CardHeader>
  <CardBody>
    <Select 
      label="Risk Level"
      value={riskLevel}
      onChange={setRiskLevel}
      options={[
        { value: "low", label: "Low - Safe for auto-execution" },
        { value: "medium", label: "Medium - Review recommended" },
        { value: "high", label: "High - Requires council approval" },
        { value: "critical", label: "Critical - Always requires approval" }
      ]}
    />
    
    <Toggle 
      label="Requires Approval"
      value={requiresApproval}
      onChange={setRequiresApproval}
    />
    
    {requiresApproval && (
      <Select 
        label="Assigned Council"
        value={assignedCouncilId}
        onChange={setAssignedCouncilId}
        options={councils}
      />
    )}
    
    <Accordion title="Auto-Approval Rules">
      <div className="space-y-4">
        <NumberInput 
          label="Max Budget"
          value={autoApprovalRules.max_budget}
          onChange={(val) => updateAutoApprovalRule('max_budget', val)}
        />
        <Toggle 
          label="Trusted Users Only"
          value={autoApprovalRules.trusted_users_only}
          onChange={(val) => updateAutoApprovalRule('trusted_users_only', val)}
        />
        <Toggle 
          label="Business Hours Only"
          value={autoApprovalRules.business_hours_only}
          onChange={(val) => updateAutoApprovalRule('business_hours_only', val)}
        />
      </div>
    </Accordion>
  </CardBody>
</Card>
```

#### Section 6: Summary Panel

```typescript
<Card className="bg-sovereign-blue/10 border-sovereign-blue">
  <CardHeader>
    <div className="flex items-center gap-2">
      <Icon name="info" className="text-sovereign-blue" />
      <h2>Plain English Summary</h2>
    </div>
  </CardHeader>
  <CardBody>
    <p className="text-lg text-white">
      {generatePlainEnglishSummary(automation)}
    </p>
    
    <div className="mt-4 space-y-2 text-sm text-slate-300">
      <div>
        <strong>Trigger:</strong> {triggerDescription}
      </div>
      {conditions.length > 0 && (
        <div>
          <strong>Conditions:</strong> {conditionsDescription}
        </div>
      )}
      <div>
        <strong>Action:</strong> {actionDescription}
      </div>
    </div>
    
    <div className="mt-6 flex gap-3">
      <Button onClick={testConditions} variant="outline">
        <Icon name="flask" /> Test Conditions
      </Button>
      <Button onClick={saveAutomation} variant="primary">
        <Icon name="save" /> Save Automation
      </Button>
      {automationId && (
        <Button onClick={deleteAutomation} variant="danger">
          <Icon name="trash" /> Delete
        </Button>
      )}
    </div>
  </CardBody>
</Card>
```

### 2. Automation List Page

**Route:** `/portal/automations/page.tsx`

```typescript
export default async function AutomationsPage() {
  const automations = await fetchAutomations();
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Automation Rules</h1>
        <Button href="/portal/automations/builder/new">
          <Icon name="plus" /> Create Automation
        </Button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard icon="zap" label="Total Automations" value={automations.length} />
        <StatCard icon="checkCircle" label="Enabled" value={enabledCount} color="emerald" />
        <StatCard icon="xCircle" label="Disabled" value={disabledCount} color="slate" />
        <StatCard icon="clock" label="Last 24h Executions" value={executions24h} color="blue" />
      </div>
      
      <Tabs>
        <Tab value="all">All ({automations.length})</Tab>
        <Tab value="marketing">Marketing</Tab>
        <Tab value="store">Store</Tab>
        <Tab value="product">Product</Tab>
        <Tab value="campaign">Campaign</Tab>
        <Tab value="customer">Customer</Tab>
      </Tabs>
      
      <div className="space-y-3">
        {automations.map((automation) => (
          <Card key={automation.id}>
            <CardBody>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Toggle 
                    value={automation.enabled}
                    onChange={() => toggleAutomation(automation.id)}
                  />
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {automation.name}
                    </h3>
                    <p className="text-sm text-slate-400">
                      {automation.description}
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant="blue">{automation.category}</Badge>
                      <Badge variant="violet">{automation.trigger_type}</Badge>
                      <Badge 
                        variant={automation.risk_level === 'low' ? 'emerald' : 'gold'}
                      >
                        {automation.risk_level} risk
                      </Badge>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-sm text-slate-400">Success Rate</div>
                    <div className="text-lg font-semibold text-sovereign-emerald">
                      {((automation.success_count / automation.execution_count) * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-slate-400">Executions</div>
                    <div className="text-lg font-semibold text-white">
                      {automation.execution_count}
                    </div>
                  </div>
                  <Button href={`/portal/automations/builder/${automation.id}`} variant="ghost">
                    <Icon name="edit" />
                  </Button>
                </div>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>
    </div>
  );
}
```

### 3. Automation Details Page

**Route:** `/portal/automations/[id]/page.tsx`

```typescript
export default async function AutomationDetailsPage({ params }: { params: { id: string } }) {
  const { automation, stats, recent_executions } = await fetchAutomationDetails(params.id);
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">{automation.name}</h1>
          <p className="text-slate-400">{automation.description}</p>
        </div>
        <div className="flex gap-2">
          <Button href={`/portal/automations/builder/${automation.id}`}>
            <Icon name="edit" /> Edit
          </Button>
          <Button onClick={() => testAutomation(automation.id)} variant="outline">
            <Icon name="flask" /> Test
          </Button>
          {automation.enabled ? (
            <Button onClick={() => disableAutomation(automation.id)} variant="danger">
              <Icon name="pause" /> Disable
            </Button>
          ) : (
            <Button onClick={() => enableAutomation(automation.id)} variant="success">
              <Icon name="play" /> Enable
            </Button>
          )}
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard icon="zap" label="Total Executions" value={stats.total_executions} />
        <StatCard icon="checkCircle" label="Success Rate" value={`${(stats.success_rate * 100).toFixed(1)}%`} color="emerald" />
        <StatCard icon="clock" label="Avg Time" value={`${stats.avg_execution_time_ms.toFixed(0)}ms`} color="blue" />
        <StatCard icon="activity" label="Last 24h" value={stats.last_24h_executions} color="violet" />
      </div>
      
      <Card>
        <CardHeader>
          <h2>Configuration</h2>
        </CardHeader>
        <CardBody>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-sm text-slate-400">Trigger Type</dt>
              <dd className="text-white font-semibold">{automation.trigger_type}</dd>
            </div>
            <div>
              <dt className="text-sm text-slate-400">Action Type</dt>
              <dd className="text-white font-semibold">{automation.action_type}</dd>
            </div>
            <div>
              <dt className="text-sm text-slate-400">Risk Level</dt>
              <dd className="text-white font-semibold">{automation.risk_level}</dd>
            </div>
            <div>
              <dt className="text-sm text-slate-400">Requires Approval</dt>
              <dd className="text-white font-semibold">{automation.requires_approval ? 'Yes' : 'No'}</dd>
            </div>
          </dl>
        </CardBody>
      </Card>
      
      <Card>
        <CardHeader>
          <h2>Execution History</h2>
        </CardHeader>
        <CardBody>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Triggered At</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Conditions</TableHead>
                <TableHead>Success</TableHead>
                <TableHead>Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recent_executions.map((execution) => (
                <TableRow key={execution.id}>
                  <TableCell>{formatDate(execution.triggered_at)}</TableCell>
                  <TableCell>
                    <Badge variant="blue">{execution.trigger_source}</Badge>
                  </TableCell>
                  <TableCell>
                    {execution.conditions_met ? (
                      <Icon name="checkCircle" className="text-sovereign-emerald" />
                    ) : (
                      <Icon name="xCircle" className="text-sovereign-crimson" />
                    )}
                  </TableCell>
                  <TableCell>
                    <StatusBadge status={execution.success ? 'approved' : 'rejected'} />
                  </TableCell>
                  <TableCell className="text-slate-400">
                    {execution.execution_time_ms.toFixed(0)}ms
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
}
```

### 4. Automation Recommendations Modal

```typescript
export function AutomationRecommendationsModal({ tenantId, onClose }: Props) {
  const [recommendations, setRecommendations] = useState([]);
  
  useEffect(() => {
    fetchRecommendations(tenantId).then(setRecommendations);
  }, [tenantId]);
  
  return (
    <Modal onClose={onClose}>
      <ModalHeader>
        <h2>Recommended Automations</h2>
      </ModalHeader>
      <ModalBody>
        <p className="text-slate-400 mb-6">
          Based on your store's performance and context, we recommend these automations:
        </p>
        
        <div className="space-y-4">
          {recommendations.map((rec, index) => (
            <Card key={index} className={rec.relevance_score > 0.9 ? "border-sovereign-gold" : ""}>
              <CardBody>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-semibold text-white">
                        {rec.name}
                      </h3>
                      <div className="text-sm text-sovereign-gold">
                        {(rec.relevance_score * 100).toFixed(0)}% match
                      </div>
                    </div>
                    <p className="text-sm text-slate-400 mb-3">
                      {rec.description}
                    </p>
                    <div className="text-sm text-slate-300 mb-3">
                      <strong>Why:</strong> {rec.reasoning}
                    </div>
                    <Badge variant="blue">{rec.category}</Badge>
                  </div>
                  <Button onClick={() => createFromRecommendation(rec)}>
                    Create
                  </Button>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      </ModalBody>
    </Modal>
  );
}
```

---

## Integration Guide

### Step 1: Run Database Migration

```bash
# Create new tables
python -c "from db import engine; from models import Base; Base.metadata.create_all(bind=engine)"

# Verify tables exist
python -c "from db import SessionLocal; s = SessionLocal(); print('Tables:', s.execute('SHOW TABLES').fetchall())"
```

### Step 2: Register API Routes

**File:** `flask_dashboard.py`

```python
from automation_api import register_automation_routes

# After other route registrations
register_automation_routes(app)
```

Test API:
```bash
curl http://localhost:5000/api/automations
```

### Step 3: Start Automation Worker

```bash
# Terminal 1: Flask Dashboard
python flask_dashboard.py

# Terminal 2: Automation Worker
python automation_worker.py
```

### Step 4: Build UI Components

1. Create `/portal/automations/page.tsx` (automation list)
2. Create `/portal/automations/builder/[id]/page.tsx` (builder UI)
3. Create `/portal/automations/[id]/page.tsx` (details page)
4. Add to navigation menu

### Step 5: Seed Sample Automations

```python
from automation_api import *
from models import *

sample_automations = [
    {
        "tenant_id": "tenant_demo",
        "name": "Low Product Alert",
        "description": "Alert when product count drops below 3",
        "category": "product",
        "trigger_type": "threshold",
        "trigger_config": {"metric": "product_count", "operator": "<", "value": 3},
        "action_type": "send_notification",
        "action_config": {"recipients": ["owner"], "message": "Low product count"},
        "risk_level": "low"
    },
    {
        "tenant_id": "tenant_demo",
        "name": "Weekly Campaign Generator",
        "description": "Create campaigns every Monday",
        "category": "marketing",
        "trigger_type": "schedule",
        "trigger_config": {"pattern": "weekly", "day": "monday", "time": "09:00"},
        "action_type": "generate_campaign",
        "action_config": {"template_id": "weekly_promo", "channels": ["email"]},
        "risk_level": "medium"
    }
]

# Create via API
for automation in sample_automations:
    requests.post('http://localhost:5000/api/automations', json=automation)
```

---

## Testing Guide

### 1. Test Database Models

```python
from models import AutomationRule, TriggerType, ActionType, RiskLevel
from db import SessionLocal

session = SessionLocal()

# Create automation
automation = AutomationRule(
    tenant_id="tenant_test",
    name="Test Automation",
    trigger_type=TriggerType.THRESHOLD,
    trigger_config={"metric": "product_count", "operator": "<", "value": 3},
    conditions=[{"type": "store_status", "operator": "=", "value": "active"}],
    action_type=ActionType.SEND_NOTIFICATION,
    action_config={"recipients": ["owner"]},
    risk_level=RiskLevel.LOW
)

session.add(automation)
session.commit()

# Test evaluate_conditions
context = {"product_count": 2, "store_status": "active"}
assert automation.evaluate_conditions(context) == True

# Test should_auto_approve
assert automation.should_auto_approve({}) == True

session.close()
```

### 2. Test API Endpoints

```bash
# Create automation
curl -X POST http://localhost:5000/api/automations \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "tenant_test",
    "name": "Test Alert",
    "trigger_type": "threshold",
    "trigger_config": {"metric": "product_count", "operator": "<", "value": 3},
    "action_type": "send_notification",
    "action_config": {"recipients": ["owner"]}
  }'

# List automations
curl http://localhost:5000/api/automations?tenant_id=tenant_test

# Test conditions
curl -X POST http://localhost:5000/api/automations/automation_xxx/test-conditions \
  -H "Content-Type: application/json" \
  -d '{"context": {"product_count": 2, "store_status": "active"}}'

# Execute automation
curl -X POST http://localhost:5000/api/automations/automation_xxx/execute \
  -H "Content-Type: application/json" \
  -d '{"context": {"product_count": 2}, "trigger_source": "manual"}'

# Get execution history
curl http://localhost:5000/api/automations/automation_xxx/executions

# Get plain English summary
curl http://localhost:5000/api/automations/automation_xxx/summary
```

### 3. Test Automation Worker

```python
from automation_worker import AutomationWorker

# Start worker
worker = AutomationWorker()

# Emit test event
worker.event_listener.emit_event('product_added', {
    'product_id': 'prod_123',
    'store_id': 'store_456'
})

# Monitor logs
# Should see: "Event emitted: product_added"
# Should see: "Event trigger matched: ..." (if automation exists)

# Test threshold monitor manually
worker.check_thresholds()

# Test schedule listener manually
worker.check_schedules()
```

### 4. Test UI Components

```typescript
// Test automation builder
// Navigate to: /portal/automations/builder/new
// 1. Fill in automation details
// 2. Select trigger type (threshold)
// 3. Add condition (store_status = active)
// 4. Select action (send_notification)
// 5. Verify plain English summary updates
// 6. Click "Test Conditions" button
// 7. Click "Save Automation"
// 8. Verify redirect to automation list

// Test automation list
// Navigate to: /portal/automations
// 1. Verify automations display
// 2. Toggle enable/disable switch
// 3. Verify success rate calculation
// 4. Click edit button
// 5. Verify navigation to builder

// Test automation details
// Navigate to: /portal/automations/automation_xxx
// 1. Verify stats display
// 2. Verify execution history table
// 3. Click "Test" button
// 4. Click "Disable" button
// 5. Verify status updates
```

---

## Expected Impact

### Efficiency Gains

- **80% reduction** in manual workflow creation (automations handle routine tasks)
- **3x increase** in proactive actions (threshold monitors catch issues early)
- **50% faster** response to events (automated triggers vs manual monitoring)

### Business Outcomes

- **95% uptime** for critical automations (low-risk, auto-approved)
- **90% success rate** for automated workflows (tested conditions)
- **5-10 automations per tenant** (average adoption)
- **100+ executions per day** (active tenant)

### User Experience

- **Plain English summaries** make automations understandable to non-technical users
- **Visual condition builder** eliminates need to write code
- **Real-time testing** provides immediate feedback
- **Execution history** builds trust and transparency

### Governance

- **Risk-based approval** ensures safety without slowing low-risk automations
- **Council oversight** maintains human control for high-impact actions
- **Auto-approval rules** balance automation with governance
- **Execution logs** provide complete audit trail

---

## Next Steps

1. ✅ Database models created (AutomationRule, AutomationExecution)
2. ✅ API endpoints implemented (13 endpoints)
3. ✅ Automation worker built (4 trigger listeners)
4. ✅ UI specifications complete (4 pages)
5. ⬜ Run database migration
6. ⬜ Register API routes in flask_dashboard.py
7. ⬜ Build UI components (AutomationBuilderUI, list, details)
8. ⬜ Start automation worker as background process
9. ⬜ Seed 5-10 sample automations
10. ⬜ Test complete lifecycle: create → trigger → execute → verify
11. ⬜ Integrate with workflow_engine for START_WORKFLOW action
12. ⬜ Integrate with notification system for SEND_NOTIFICATION action
13. ⬜ Add automation recommendations to workflow creation flow
14. ⬜ Build automation analytics dashboard
15. ⬜ Document automation patterns and best practices

---

**🔥 The Dominion Automates Itself Sovereign and Eternal!** 👑
