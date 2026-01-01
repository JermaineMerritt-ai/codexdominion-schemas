# CodexDominion Governance Specification v1.0

**Last Updated:** December 19, 2025  
**Status:** Production  
**Audience:** Developers, Partners, System Integrators

---

## 1. System Overview

### 1.1. Architecture

CodexDominion is a sovereign automation and governance network composed of:

- **36 Councils** — Domain-focused governance bodies (e.g., Governance, Commerce, Media, Youth, Creator, Research, Security, Education, etc.)
- **300+ AI Agents** — Action AIs/avatars that execute tasks, design workflows, and interact with users
- **12 Core Engines** — Foundational intelligence engines (Identity, Governance, Safety, Commerce, Workflow, Recommendation, AI, Knowledge, Community, Media, Culture, Analytics)
- **Workflow Engine** — Executes and tracks automation workflows
- **Savings Calculator** — Estimates financial and time savings for each automation
- **Reputation System** — Scores AI agents based on performance, savings, and governance approval
- **Voting & Oversight** — Councils review and vote on high-impact or sensitive workflows

The system is accessed through the **CODEXDOMINION MASTER DASHBOARD ULTIMATE**, built on:
- **Backend:** Flask (Python) on port 5000
- **Frontend:** Next.js 14 (App Router) on port 3000

---

## 2. Core Entities

### 2.1. Council

Councils are governance bodies that oversee specific domains and vote on workflows within their jurisdiction.

#### Schema

```typescript
interface Council {
  id: string;                        // e.g., "council_governance"
  name: string;                      // Human-readable name
  purpose: string;                   // What this council stewards
  domain: string;                    // Primary domain (governance, commerce, media, youth)
  members: string[];                 // Array of agent IDs
  primary_engines: string[];         // List of engine IDs
  oversight: OversightRules;         // Governance rules
  status: "active" | "paused";
}

interface OversightRules {
  review_actions: boolean;                     // Must review workflows in domain?
  review_threshold_weekly_savings: number;     // Savings threshold for review
  blocked_action_types: string[];              // Always block these action types
  requires_majority_vote: boolean;             // Multiple members must vote?
  min_votes: number;                           // Minimum votes for binding decision
}
```

#### Example

```json
{
  "id": "council_governance",
  "name": "Governance Council",
  "purpose": "Oversees policy, compliance, and strategic decisions",
  "domain": "governance",
  "members": [
    "agent_jermaine_super_action",
    "agent_governance_advisor"
  ],
  "primary_engines": [
    "governance_engine",
    "identity_engine"
  ],
  "oversight": {
    "review_actions": true,
    "review_threshold_weekly_savings": 1000,
    "blocked_action_types": ["policy_change"],
    "requires_majority_vote": true,
    "min_votes": 2
  },
  "status": "active"
}
```

---

### 2.2. Agent

AI agents execute workflows, interact with users, and participate in council governance.

#### Schema

```typescript
interface Agent {
  id: string;
  name: string;
  role: string;                       // Concise description
  personality: string;                // Tone/behavior
  mode: "research" | "execution" | "hybrid";
  primary_engines: string[];
  secondary_engines: string[];
  domains: string[];                  // Primary operating domains
  capabilities: string[];             // e.g., "create_workflows", "summarize_docs"
  ui: AvatarSettings;
  reputation: ReputationMetrics;
  training: TrainingData;
}

interface AvatarSettings {
  color: string;
  icon: string;
  emoji: string;
}

interface ReputationMetrics {
  score: number;                      // 0-1 decimal
  total_savings: number;              // Cumulative estimated weekly savings
  workflows_executed: number;         // Count
  approval_rate: number;              // Ratio of approved workflows (0-1)
}

interface TrainingData {
  strengths: string[];                // Domains or workflow tags they excel in
  weaknesses: string[];               // Areas to avoid
  restricted_workflow_types: string[]; // Workflow IDs they cannot trigger
  last_feedback: string;              // Latest high-level feedback
}
```

#### Example

```json
{
  "id": "agent_treasury_guardian",
  "name": "Treasury Guardian",
  "role": "Financial Oversight",
  "personality": "Professional, detail-oriented, risk-averse",
  "mode": "execution",
  "primary_engines": ["commerce_engine", "governance_engine"],
  "secondary_engines": ["analytics_engine"],
  "domains": ["commerce", "finance"],
  "capabilities": [
    "create_workflows",
    "calculate_savings",
    "monitor_transactions"
  ],
  "ui": {
    "color": "#10b981",
    "icon": "shield",
    "emoji": "🛡️"
  },
  "reputation": {
    "score": 0.66,
    "total_savings": 289300,
    "workflows_executed": 634,
    "approval_rate": 0.959
  },
  "training": {
    "strengths": [
      "commerce_automation",
      "customer_followup",
      "payment_processing"
    ],
    "weaknesses": [
      "governance_policy",
      "strategic_planning"
    ],
    "restricted_workflow_types": [
      "policy_change",
      "governance_review"
    ],
    "last_feedback": "Great at follow-ups, avoid governance-critical workflows."
  }
}
```

---

### 2.3. WorkflowAction

Represents a single automation workflow instance tracked by the system.

#### Schema

```typescript
interface WorkflowAction {
  id: string;
  action_type: string;                    // e.g., "create_workflow_customer_followup"
  workflow_type_id: string;               // From catalog (e.g., "customer_followup")
  created_by_agent: string;               // Agent ID
  inputs: Record<string, any>;            // Raw inputs for execution
  calculated_savings: SavingsBreakdown;   // Output of savings calculator
  status: ActionStatus;
  created_at: number;                     // Unix timestamp
  updated_at: number;                     // Unix timestamp
  assigned_council_id: string | null;     // Council responsible for review
  decision: DecisionStatus;
  votes: Vote[];
}

type ActionStatus = "pending" | "running" | "completed" | "failed";
type DecisionStatus = "pending" | "approved" | "denied";

interface SavingsBreakdown {
  weekly: number;
  monthly: number;
  annual: number;
  time_saved_hours: number;
  error_reduction_savings: number;
  acceleration_value: number;
}

interface Vote {
  member_id: string;                      // Agent ID
  vote: "approve" | "deny";
  reason: string;
  timestamp: number;                      // Unix timestamp
}
```

#### Example

```json
{
  "id": "wf_abc123",
  "action_type": "create_workflow_customer_followup",
  "workflow_type_id": "customer_followup",
  "created_by_agent": "agent_treasury_guardian",
  "inputs": {
    "frequency": 200,
    "time_per_task": 10,
    "hourly_cost": 25
  },
  "calculated_savings": {
    "weekly": 2916.67,
    "monthly": 12500,
    "annual": 150000,
    "time_saved_hours": 116.67,
    "error_reduction_savings": 300,
    "acceleration_value": 0
  },
  "status": "pending",
  "created_at": 1734624000,
  "updated_at": 1734624000,
  "assigned_council_id": "council_commerce",
  "decision": "pending",
  "votes": []
}
```

---

## 3. Governance Logic

### 3.1. Workflow Creation Flow

```
User → Agent Chat → mode="execute" → Workflow Engine
  ↓
1. Workflow Type Selection (from catalog)
2. Savings Calculation
3. Domain Determination
4. Council Assignment
5. Governance Check
  ↓
Automatic Execution OR Pending Review
```

### 3.2. Council Assignment

```python
domain = workflow_type.get("domain")  # e.g., "commerce"
council = get_council_by_domain(domain)
action.assigned_council_id = council.id
```

### 3.3. Governance Decision Matrix

| Condition | Action |
|-----------|--------|
| Workflow type in `blocked_action_types` | Auto-deny |
| `review_actions = true` OR savings > `review_threshold_weekly_savings` | Pending review |
| Agent has workflow type in `restricted_workflow_types` | Auto-deny |
| None of the above | Auto-run |

#### Pseudocode

```python
def should_require_review(workflow_action, agent, council):
    # Check blocked types
    if workflow_action.action_type in council.oversight.blocked_action_types:
        return "denied"
    
    # Check agent restrictions
    if workflow_action.workflow_type_id in agent.training.restricted_workflow_types:
        return "denied"
    
    # Check review requirements
    if council.oversight.review_actions:
        return "pending"
    
    if workflow_action.calculated_savings.weekly > council.oversight.review_threshold_weekly_savings:
        return "pending"
    
    # Auto-approve
    return "approved"
```

### 3.4. Council Voting

#### Vote Submission

```http
POST /api/workflows/<action_id>/vote
Content-Type: application/json

{
  "member_id": "agent_jermaine_super_action",
  "vote": "approve",
  "reason": "High ROI with low risk. Approved."
}
```

#### Decision Evaluation

```python
def evaluate_council_decision(council, action):
    votes = action.votes
    approve_votes = sum(1 for v in votes if v.vote == "approve")
    deny_votes = sum(1 for v in votes if v.vote == "deny")
    total_votes = len(votes)
    
    # Check minimum votes
    if total_votes < council.oversight.min_votes:
        return "pending"
    
    # Check majority requirement
    if council.oversight.requires_majority_vote:
        if approve_votes > deny_votes:
            return "approved"
        elif deny_votes >= approve_votes:
            return "denied"
    
    return "pending"
```

#### Status Updates

```python
if decision == "approved":
    action.decision = "approved"
    workflow_engine.update_status(action.id, "running")
elif decision == "denied":
    action.decision = "denied"
    workflow_engine.update_status(action.id, "failed")
```

### 3.5. Reputation Updates

#### On Workflow Completion

```python
# Success case
agent.reputation.workflows_executed += 1
agent.reputation.total_savings += action.calculated_savings.weekly
agent.reputation.approval_rate = (successful / total)

# Calculate new reputation score
R = 0.5 * S + 0.3 * A + 0.2 * V
# S = Savings normalized to $500k max
# A = Approval rate (0-1)
# V = Volume normalized to 1,500 actions max
```

#### On Workflow Denial

```python
# Add to training data
agent.training.weaknesses.append(action.workflow_type_id)
agent.training.last_feedback = f"Workflow {action.id} denied by {council.name}"

# Optionally decrease reputation
agent.reputation.approval_rate = (successful / total)
```

---

## 4. Key API Contracts

### 4.1. Chat & Execution

#### POST `/api/chat`

Execute workflows via conversational interface.

**Request:**
```json
{
  "message": "Create customer follow-up automation",
  "agent_id": "agent_treasury_guardian",
  "mode": "execute",
  "context": {}
}
```

**Response:**
```json
{
  "response": "I've created a customer follow-up workflow...",
  "workflow_id": "wf_abc123",
  "savings": {
    "weekly": 2916.67,
    "monthly": 12500,
    "annual": 150000
  },
  "status": "pending"
}
```

---

### 4.2. Workflow Management

#### GET `/api/workflow-types`

List all available workflow types from catalog.

**Response:**
```json
{
  "workflow_types": [
    {
      "id": "customer_followup",
      "name": "Customer Follow-up",
      "domain": "commerce",
      "inputs": [...],
      "estimated_savings": {...}
    }
  ]
}
```

#### GET `/api/workflows`

List all workflow actions.

**Response:**
```json
{
  "workflows": [
    {
      "id": "wf_abc123",
      "action_type": "create_workflow_customer_followup",
      "status": "pending",
      "created_by_agent": "agent_treasury_guardian",
      "assigned_council_id": "council_commerce",
      "decision": "pending"
    }
  ]
}
```

#### GET `/api/workflows/<action_id>`

Get single workflow details.

**Response:**
```json
{
  "id": "wf_abc123",
  "action_type": "create_workflow_customer_followup",
  "calculated_savings": {...},
  "status": "pending",
  "votes": [],
  "decision": "pending"
}
```

#### GET `/api/workflows/metrics`

Get workflow metrics and statistics.

**Response:**
```json
{
  "total": 1247,
  "pending": 23,
  "running": 45,
  "completed": 1167,
  "failed": 12,
  "total_savings": {
    "weekly": 487650,
    "monthly": 2092800,
    "annual": 25113600
  }
}
```

#### POST `/api/workflows/<action_id>/vote`

Submit council vote on workflow.

**Request:**
```json
{
  "member_id": "agent_jermaine_super_action",
  "vote": "approve",
  "reason": "High ROI with low risk."
}
```

**Response:**
```json
{
  "action_id": "wf_abc123",
  "votes": [
    {
      "member_id": "agent_jermaine_super_action",
      "vote": "approve",
      "reason": "High ROI with low risk.",
      "timestamp": 1734624000
    }
  ],
  "decision": "approved"
}
```

---

### 4.3. Analytics

#### GET `/api/analytics/summary`

Global system metrics.

**Response:**
```json
{
  "total_workflows": 1247,
  "total_agents": 36,
  "total_councils": 36,
  "total_savings": {
    "weekly": 1970000,
    "monthly": 8450000,
    "annual": 101400000
  },
  "success_rate": 0.954
}
```

#### GET `/api/analytics/agent-performance`

Per-agent performance metrics.

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_jermaine_super_action",
      "name": "Jermaine Super Action",
      "workflows_executed": 1247,
      "total_savings": 487650,
      "success_rate": 0.953,
      "reputation_score": 0.94
    }
  ],
  "total_agents": 36,
  "avg_success_rate": 0.954
}
```

---

### 4.4. Councils

#### GET `/api/councils`

List all councils.

**Response:**
```json
{
  "councils": [
    {
      "id": "council_governance",
      "name": "Governance Council",
      "domain": "governance",
      "members": [...],
      "status": "active"
    }
  ],
  "total": 36
}
```

#### GET `/api/councils/<council_id>`

Get single council details.

**Response:**
```json
{
  "id": "council_governance",
  "name": "Governance Council",
  "purpose": "Oversees policy, compliance, and strategic decisions",
  "domain": "governance",
  "members": [
    "agent_jermaine_super_action",
    "agent_governance_advisor"
  ],
  "primary_engines": ["governance_engine"],
  "oversight": {
    "review_actions": true,
    "review_threshold_weekly_savings": 1000,
    "blocked_action_types": ["policy_change"],
    "requires_majority_vote": true,
    "min_votes": 2
  },
  "status": "active"
}
```

#### GET `/api/workflows/pending-review`

Get workflows awaiting council review.

**Query Parameters:**
- `council_id` (optional): Filter by council

**Response:**
```json
{
  "reviews": [
    {
      "id": "wf_abc123",
      "action_type": "create_workflow_customer_followup",
      "created_by_agent": "agent_treasury_guardian",
      "assigned_council_id": "council_commerce",
      "calculated_savings": {...},
      "decision": "pending",
      "votes": []
    }
  ],
  "total": 23
}
```

---

### 4.5. Agents

#### GET `/api/agents/leaderboard`

Get ranked list of agents by reputation.

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_jermaine_super_action",
      "name": "Jermaine Super Action",
      "rank": 1,
      "reputation": {
        "score": 0.94,
        "total_savings": 487650,
        "workflows_executed": 1247,
        "approval_rate": 0.953
      }
    }
  ],
  "total_agents": 36
}
```

#### GET `/api/agents/<agent_id>`

Get single agent details.

**Response:**
```json
{
  "id": "agent_treasury_guardian",
  "name": "Treasury Guardian",
  "role": "Financial Oversight",
  "reputation": {
    "score": 0.66,
    "total_savings": 289300,
    "workflows_executed": 634,
    "approval_rate": 0.959
  },
  "training": {
    "strengths": ["commerce_automation"],
    "weaknesses": ["governance_policy"],
    "restricted_workflow_types": ["policy_change"],
    "last_feedback": "Great at follow-ups, avoid governance-critical workflows."
  }
}
```

#### GET `/api/agents/<agent_id>/reputation`

Get agent reputation metrics only.

**Response:**
```json
{
  "score": 0.66,
  "total_savings": 289300,
  "workflows_executed": 634,
  "approval_rate": 0.959
}
```

---

## 5. Council Console Layout

### 5.1. Route

```
app/dashboard/councils/[id]/page.tsx
```

### 5.2. Page Structure

#### Top Section: Council Identity

```tsx
<div className="council-header">
  <div className="council-title">
    <h1>{council.name}</h1>
    <Badge>{council.domain}</Badge>
    <StatusChip status={council.status} />
  </div>
  
  <p className="council-purpose">{council.purpose}</p>
  
  <div className="council-engines">
    {council.primary_engines.map(engine => (
      <EngineBadge key={engine} engineId={engine} />
    ))}
  </div>
  
  <div className="council-members">
    {council.members.map(memberId => (
      <AgentAvatar key={memberId} agentId={memberId} />
    ))}
  </div>
</div>
```

#### Metrics Row

```tsx
<div className="metrics-row">
  <MetricCard
    label="Workflows Reviewed"
    value={metrics.total_reviewed}
  />
  <MetricCard
    label="Total Approved Savings"
    value={formatCurrency(metrics.total_savings)}
    suffix="/ week"
  />
  <MetricCard
    label="Approval Rate"
    value={formatPercent(metrics.approval_rate)}
  />
  <MetricCard
    label="Avg Review Time"
    value={formatDuration(metrics.avg_review_time)}
  />
</div>
```

#### Tabbed Content

```tsx
<Tabs defaultValue="overview">
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="pending">
      Pending Review
      {pendingCount > 0 && <Badge>{pendingCount}</Badge>}
    </TabsTrigger>
    <TabsTrigger value="history">History</TabsTrigger>
    <TabsTrigger value="members">Members</TabsTrigger>
  </TabsList>
  
  <TabsContent value="overview">
    <MetricsCharts councilId={council.id} />
  </TabsContent>
  
  <TabsContent value="pending">
    <PendingReviewTable councilId={council.id} />
  </TabsContent>
  
  <TabsContent value="history">
    <DecisionHistory councilId={council.id} />
  </TabsContent>
  
  <TabsContent value="members">
    <MemberList members={council.members} />
  </TabsContent>
</Tabs>
```

### 5.3. Pending Review Table

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Workflow ID</TableHead>
      <TableHead>Type</TableHead>
      <TableHead>Created By</TableHead>
      <TableHead>Weekly Savings</TableHead>
      <TableHead>Votes</TableHead>
      <TableHead>Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {pendingWorkflows.map(workflow => (
      <TableRow key={workflow.id}>
        <TableCell>
          <WorkflowId id={workflow.id} />
        </TableCell>
        <TableCell>
          <WorkflowTypeBadge type={workflow.workflow_type_id} />
        </TableCell>
        <TableCell>
          <AgentChip agentId={workflow.created_by_agent} />
        </TableCell>
        <TableCell>
          {formatCurrency(workflow.calculated_savings.weekly)}
        </TableCell>
        <TableCell>
          <VoteStatus votes={workflow.votes} />
        </TableCell>
        <TableCell>
          <Button onClick={() => openVoteModal(workflow)}>
            Vote
          </Button>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### 5.4. Vote Modal

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Vote on Workflow</DialogTitle>
    </DialogHeader>
    
    <div className="workflow-summary">
      <WorkflowDetails workflow={selectedWorkflow} />
      <SavingsBreakdown savings={selectedWorkflow.calculated_savings} />
    </div>
    
    <div className="vote-form">
      <RadioGroup value={vote} onValueChange={setVote}>
        <div className="radio-item">
          <RadioGroupItem value="approve" id="approve" />
          <Label htmlFor="approve">Approve</Label>
        </div>
        <div className="radio-item">
          <RadioGroupItem value="deny" id="deny" />
          <Label htmlFor="deny">Deny</Label>
        </div>
      </RadioGroup>
      
      <Textarea
        placeholder="Reason for vote..."
        value={reason}
        onChange={(e) => setReason(e.target.value)}
      />
    </div>
    
    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Cancel
      </Button>
      <Button onClick={submitVote}>
        Submit Vote
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## 6. Implementation Checklist

### Backend (Flask)

- [x] `WorkflowAction` dataclass with council fields
- [x] `get_action_raw()` method in workflow_engine
- [x] `/api/workflows/<id>/vote` endpoint
- [x] `find_council_by_id()` helper
- [x] `evaluate_council_decision()` logic
- [x] Council data loading from `councils.json`
- [x] Agent training data in `agent_reputation.json`
- [x] Reputation calculation (R = 0.5*S + 0.3*A + 0.2*V)

### Frontend (Next.js)

- [ ] `app/dashboard/councils/[id]/page.tsx`
- [ ] Council identity section
- [ ] Metrics row with 4 cards
- [ ] Tabbed interface (Overview, Pending, History, Members)
- [ ] Pending Review table
- [ ] Vote modal component
- [ ] API integration hooks
- [ ] Real-time updates (polling or websockets)

### Data Files

- [x] `councils.json` with oversight rules
- [x] `agent_reputation.json` with training data
- [x] `workflow_catalog.json` with workflow types

---

## 7. Security & Permissions

### Role-Based Access

```typescript
enum Permission {
  VIEW_COUNCILS = "councils.view",
  VOTE_WORKFLOWS = "workflows.vote",
  MANAGE_COUNCILS = "councils.manage",
  VIEW_AGENTS = "agents.view",
  MANAGE_AGENTS = "agents.manage"
}

interface User {
  id: string;
  role: "admin" | "council_member" | "viewer";
  permissions: Permission[];
  council_memberships: string[];  // Council IDs
}
```

### Authorization Checks

```python
def can_vote_on_workflow(user, workflow_action):
    # Must be council member
    if workflow_action.assigned_council_id not in user.council_memberships:
        return False
    
    # Must have vote permission
    if Permission.VOTE_WORKFLOWS not in user.permissions:
        return False
    
    return True
```

---

## 8. Future Enhancements

### 8.1. Advanced Voting Rules

- **Weighted votes:** Senior council members have higher vote weight
- **Delegation:** Members can delegate votes to other agents
- **Quorum requirements:** Minimum % of members must vote
- **Time limits:** Auto-deny after X hours without quorum

### 8.2. Learning & Optimization

- **Auto-routing:** ML model learns which councils approve which workflow types
- **Risk scoring:** Predict likelihood of approval before submission
- **Agent training:** Automated feedback loops update agent training data
- **Council rebalancing:** Suggest member additions/removals based on workload

### 8.3. Audit & Compliance

- **Immutable audit log:** Blockchain or append-only log for all decisions
- **Compliance reports:** Automated regulatory reporting
- **External integrations:** Webhook notifications to external systems
- **Appeal process:** Ability to appeal denied workflows

---

## 9. Glossary

- **Council:** Governance body overseeing a specific domain
- **Agent:** AI entity that executes workflows and participates in governance
- **Workflow Action:** Single instance of an automation workflow
- **Decision:** Governance outcome (pending/approved/denied)
- **Reputation:** Quantified agent performance score (0-1)
- **Oversight:** Governance rules for a council
- **Domain:** Functional area (governance, commerce, media, etc.)
- **Engine:** Core intelligence subsystem
- **Training:** Agent-specific performance data and restrictions

---

## 10. Support & Contact

- **Documentation:** https://docs.codexdominion.app
- **API Reference:** https://api.codexdominion.app/docs
- **Discord:** https://discord.gg/codexdominion
- **Email:** support@codexdominion.app
- **GitHub:** https://github.com/codexdominion

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**

