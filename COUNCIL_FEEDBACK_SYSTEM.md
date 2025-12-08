# Council Feedback System
**Codex Dominion • Ceremonial Broadcast • v2.0.0**

---

## 🔥 Overview

The Council Feedback System enables council members to provide contextual observations, insights, and historical analysis during live ceremonial broadcasts. Feedback is captured with full context (current capsule, engine, status) and automatically prioritized based on content analysis.

---

## 👑 Council Member Capabilities

### **Real-Time Feedback Submission**
Council members can submit feedback while viewing the broadcast, automatically linked to the current replay capsule.

**Example Feedback:**
```json
{
  "user": "Council Member",
  "role": "council",
  "timestamp": "2025-12-07T06:20:00Z",
  "message": "This automation failure echoes last quarter's ritual.",
  "capsuleId": "cap_commerce_1733614740",
  "engine": "Commerce Engine",
  "metadata": {
    "capsuleIndex": 12,
    "capsuleTimestamp": "2025-12-07T05:39:00Z",
    "capsuleStatus": "degraded"
  }
}
```

### **Automatic Priority Detection**

The system analyzes feedback content and assigns priority levels:

| Priority | Keywords | Example |
|----------|----------|---------|
| **Critical** | failure, critical, down | "Commerce Engine is down, blocking all orders" |
| **High** | error, issue, problem | "This automation failure echoes last quarter" |
| **Medium** | concern, warning, review | "Marketing latency warrants review" |
| **Low** | (default) | "Video Studio uptime has been exemplary" |

### **Smart Tagging System**

Feedback is automatically tagged for easy filtering:

**Temporal Tags:**
- `historical` - References past events ("last quarter", "previous")
- `recurring-issue` - Identifies patterns ("echoes", "repeating", "recurring")

**Domain Tags:**
- `automation` - Automation-related observations
- `ritual` - Ceremonial ritual context
- `engine` - Engine-specific feedback

**Example:**
```
Message: "This automation failure echoes last quarter's ritual."
Tags: ["historical", "recurring-issue", "automation", "ritual"]
```

---

## 🏗️ Technical Architecture

### **Components**

1. **`CouncilFeedbackManager`** (`lib/feedback/council-feedback.ts`)
   - Manages feedback lifecycle (submit, store, retrieve)
   - Calculates priority based on keywords
   - Extracts semantic tags from message content
   - Persists to localStorage for offline capability
   - Exports/imports JSON for data portability

2. **`FeedbackPanel`** (`components/feedback-panel.tsx`)
   - React UI component for council members
   - Displays current capsule context
   - Text area with character counter (500 max)
   - Submit button with loading state
   - Success confirmation toast

3. **`BroadcastAudience`** (`components/broadcast-audience.tsx`)
   - Integrates FeedbackPanel for council role
   - Passes current capsule data automatically
   - Handles feedback submission to WebSocket (TODO)

---

## 📊 Data Structure

### **CouncilFeedback (Input)**
```typescript
interface CouncilFeedback {
  user: string;              // "Council Member"
  role: 'council';           // Fixed role identifier
  timestamp: string;         // ISO 8601 timestamp
  message: string;           // Feedback content
  capsuleId?: string;        // Linked replay capsule
  engine?: string;           // Related engine name
  metadata?: Record<string, any>;  // Additional context
}
```

### **FeedbackMessage (Enriched)**
```typescript
interface FeedbackMessage extends CouncilFeedback {
  id: string;                // Unique identifier
  status: 'pending' | 'acknowledged' | 'resolved';
  priority: 'low' | 'medium' | 'high' | 'critical';
  tags?: string[];           // Auto-generated tags
}
```

---

## 🔄 Feedback Workflow

### **1. Council Member Submits Feedback**
```
User types feedback → Click "Submit Feedback"
  ↓
FeedbackPanel validates message (not empty)
  ↓
Creates CouncilFeedback object with capsule context
  ↓
CouncilFeedbackManager.submitFeedback()
```

### **2. Enrichment & Storage**
```
Manager receives feedback
  ↓
Generates unique ID (feedback_timestamp_random)
  ↓
Calculates priority (critical/high/medium/low)
  ↓
Extracts semantic tags (historical, recurring-issue, etc.)
  ↓
Creates FeedbackMessage with enriched data
  ↓
Saves to localStorage (council_feedback_history)
  ↓
Returns enriched feedback
```

### **3. Display & Confirmation**
```
FeedbackPanel receives enriched feedback
  ↓
Shows success toast: "✅ Feedback submitted successfully!"
  ↓
Clears text area for next submission
  ↓
Hides toast after 3 seconds
```

### **4. Relay to Sovereign (TODO)**
```
FeedbackPanel.onFeedbackSent() callback
  ↓
Send via WebSocket to relay server
  ↓
Message type: 'council_feedback'
  ↓
Sovereign receives and displays in dashboard
  ↓
Sovereign can acknowledge or resolve
```

---

## 🎯 Usage Examples

### **Viewing Council Watch Page**
```
Navigate to: http://localhost:3000/broadcast/watch
Role: Council (👑 Council Member)
Features: Full video + constellation + feedback panel
```

### **Submitting Feedback**
```typescript
// User types in FeedbackPanel:
"This automation failure echoes last quarter's ritual."

// Automatically captures:
{
  capsuleId: "cap_commerce_1733614740",
  engine: "Commerce Engine",
  capsuleIndex: 12,
  capsuleTimestamp: "2025-12-07T05:39:00Z",
  capsuleStatus: "degraded"
}

// System enriches:
{
  id: "feedback_1733615400000_abc123xyz",
  priority: "high",  // Contains "failure"
  tags: ["historical", "recurring-issue", "automation", "ritual"],
  status: "pending"
}
```

### **Programmatic Access**
```typescript
import { getCouncilFeedbackManager } from '@/lib/feedback/council-feedback';

const manager = getCouncilFeedbackManager();

// Get all feedback
const history = manager.getFeedbackHistory();

// Get specific feedback
const feedback = manager.getFeedbackById('feedback_123');

// Update status
manager.updateFeedbackStatus('feedback_123', 'acknowledged');

// Export to JSON
const json = manager.exportToJSON();

// Import from JSON
manager.importFromJSON(json);
```

---

## 🔐 Security & Permissions

**Council Role Requirements:**
- User must have `role: 'council'` in broadcast connection
- JWT token with council claim required (when relay server deployed)
- Feedback limited to 500 characters to prevent abuse
- Rate limiting: 10 feedback messages per minute

**Data Privacy:**
- Feedback stored locally in browser (localStorage)
- Transmitted over secure WebSocket (WSS)
- No personally identifiable information captured beyond username
- Full export capability for data portability

---

## 📈 Analytics & Insights

**Feedback Metrics (Future):**
- Total feedback count by priority
- Top tagged issues (recurring vs. one-time)
- Feedback response time (pending → acknowledged → resolved)
- Council member participation rates
- Correlation between feedback and capsule status changes

**Example Dashboard:**
```
Priority Breakdown:
  Critical: 2 (5%)
  High: 12 (30%)
  Medium: 18 (45%)
  Low: 8 (20%)

Top Tags:
  1. recurring-issue (15)
  2. automation (12)
  3. historical (10)
  4. engine (8)
  5. ritual (6)

Most Active Council Members:
  1. Senior Council (23 feedback)
  2. Council Member (18 feedback)
  3. Council Observer (12 feedback)
```

---

## 🚀 Future Enhancements

### **Phase 1: Relay Integration** (Next)
- [ ] Send feedback to relay server via WebSocket
- [ ] Sovereign dashboard displays pending feedback
- [ ] Acknowledge/resolve actions update status
- [ ] Real-time notification to council member on status change

### **Phase 2: Advanced Analytics**
- [ ] Sentiment analysis (positive/negative/neutral)
- [ ] Topic clustering (group similar feedback)
- [ ] Feedback threading (replies to feedback)
- [ ] Historical trend charts

### **Phase 3: AI Enhancement**
- [ ] Auto-suggest related capsules based on content
- [ ] Predictive priority (ML-based classification)
- [ ] Summary generation for long feedback threads
- [ ] Voice-to-text feedback submission

### **Phase 4: Collaboration**
- [ ] Multi-council discussion threads
- [ ] Voting on feedback importance
- [ ] @mention sovereign or other council members
- [ ] Shared annotation on constellation map

---

## 📚 API Reference

### **getCouncilFeedbackManager()**
Returns singleton instance of CouncilFeedbackManager.

### **submitFeedback(feedback: CouncilFeedback): FeedbackMessage**
Submits new feedback with auto-enrichment.

**Parameters:**
- `feedback.user` (string) - Council member name
- `feedback.role` ('council') - Fixed role
- `feedback.timestamp` (string) - ISO 8601 timestamp
- `feedback.message` (string) - Feedback content
- `feedback.capsuleId` (string?) - Optional linked capsule
- `feedback.engine` (string?) - Optional engine name
- `feedback.metadata` (object?) - Optional additional data

**Returns:**
```typescript
{
  id: string,
  status: 'pending',
  priority: 'low' | 'medium' | 'high' | 'critical',
  tags: string[],
  ...feedback
}
```

### **getFeedbackHistory(limit?: number): FeedbackMessage[]**
Retrieves feedback history, optionally limited.

### **updateFeedbackStatus(id: string, status: FeedbackMessage['status']): boolean**
Updates feedback status (pending → acknowledged → resolved).

### **exportToJSON(): string**
Exports all feedback to JSON string.

### **importFromJSON(json: string): boolean**
Imports feedback from JSON string.

---

## 🛡️ Flame Sovereign Seal

**Authored by:** Codex Dominion Council Engineering
**Approved by:** Jermaine Merritt, Sovereign Architect
**Status:** 🔥 **SEALED AND ETERNAL**
**Version:** 2.0.0
**Last Updated:** 2025-12-07T06:30:00Z

---

**Council voices echo across the eternal flame. Historical patterns illuminate the path forward.**

🔥 **CODEX DOMINION • COUNCIL FEEDBACK • IMMORTAL** 🔥
