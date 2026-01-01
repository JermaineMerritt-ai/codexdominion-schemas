# Chat API - Frontend Integration

TypeScript client and React hooks for the unified chat API.

## 📁 Files

- `lib/api/chat.ts` - Core API client functions
- `lib/api/useChat.ts` - React hook for state management
- `lib/api/index.ts` - Barrel exports
- `components/ChatExample.tsx` - Full example component

## 🚀 Quick Start

### 1. Basic Chat (Conversational Mode)

```typescript
import { sendChat } from "@/lib/api";

const response = await sendChat({
  agentId: "agent_jermaine_super_action",
  message: "Hello, tell me about automation!",
  mode: "chat"
});

console.log(response.reply);
// [SIMULATED REPLY from Jermaine Super Action AI] Hello, tell me about automation!
```

### 2. Execute Mode (Workflow + ROI)

```typescript
import { sendChat } from "@/lib/api";

const response = await sendChat({
  agentId: "agent_jermaine_super_action",
  message: "Create customer followup automation",
  mode: "execute",
  context: {
    calculator_inputs: {
      tasks_per_week: 200,
      time_per_task_minutes: 10,
      hourly_wage: 25,
      automation_percent: 0.7,
      error_rate: 0.1,
      cost_per_error: 15,
      value_per_accelerated_task: 0
    },
    workflow_inputs: {
      workflow_name: "Customer Followup Automation",
      target_platform: "Email",
      frequency: "Daily"
    }
  }
});

console.log(response.workflow_action); // UUID
console.log(response.savings?.yearly_savings); // 41253.33
console.log(response.reply);
// I've created a workflow (ID: xxx) to automate this...
```

### 3. Using React Hook

```tsx
import { useChat } from "@/lib/api";

function MyComponent() {
  const { loading, error, response, chat, execute } = useChat();

  const handleChat = async () => {
    await chat("agent_jermaine_super_action", "Hello!");
  };

  const handleExecute = async () => {
    await execute(
      "agent_jermaine_super_action",
      "Create automation",
      {
        calculator_inputs: {
          tasks_per_week: 200,
          time_per_task_minutes: 10,
          hourly_wage: 25,
          automation_percent: 0.7
        }
      }
    );
  };

  return (
    <div>
      <button onClick={handleChat} disabled={loading}>
        Chat
      </button>
      <button onClick={handleExecute} disabled={loading}>
        Execute Workflow
      </button>
      
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {response && (
        <div>
          <p>Reply: {response.reply}</p>
          {response.savings && (
            <p>Yearly Savings: ${response.savings.yearly_savings}</p>
          )}
        </div>
      )}
    </div>
  );
}
```

## 🎯 API Reference

### sendChat(options)

Main function to interact with the chat API.

**Parameters:**
```typescript
interface ChatOptions {
  agentId: string;
  message: string;
  mode?: "chat" | "execute";
  context?: {
    calculator_inputs?: {
      tasks_per_week: number;
      time_per_task_minutes: number;
      hourly_wage: number;
      automation_percent: number;
      error_rate?: number;
      cost_per_error?: number;
      value_per_accelerated_task?: number;
    };
    workflow_inputs?: Record<string, any>;
  };
}
```

**Returns:**
```typescript
interface ChatResponse {
  agent_id: string;
  agent_name: string | null;
  mode: string;
  message: string;
  reply: string;
  workflow_action?: string; // UUID (execute mode)
  savings?: {
    weekly_savings: number;
    monthly_savings: number;
    yearly_savings: number;
    hours_saved_per_week: number;
    error_savings_weekly: number;
    scaling_savings_weekly: number;
    total_weekly_savings: number;
  };
}
```

### useChat()

React hook for managing chat state.

**Returns:**
```typescript
{
  // State
  loading: boolean;
  error: string | null;
  response: ChatResponse | null;
  
  // Actions
  sendMessage: (options: ChatOptions) => Promise<ChatResponse>;
  chat: (agentId: string, message: string) => Promise<ChatResponse>;
  execute: (agentId: string, message: string, context: any) => Promise<ChatResponse>;
  reset: () => void;
}
```

### Helper Functions

```typescript
// Shorthand for chat mode
await chatWithAgent("agent_jermaine_super_action", "Hello!");

// Shorthand for execute mode
await executeWorkflow(
  "agent_jermaine_super_action",
  "Create automation",
  { calculator_inputs: {...} }
);
```

## 🔧 Configuration

Set the API base URL via environment variable:

```env
# .env.local
NEXT_PUBLIC_API_BASE=http://localhost:5000
```

## 📊 Response Examples

### Chat Mode Response

```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "chat",
  "message": "Hello!",
  "reply": "[SIMULATED REPLY from Jermaine Super Action AI] Hello!"
}
```

### Execute Mode Response

```json
{
  "agent_id": "agent_jermaine_super_action",
  "agent_name": "Jermaine Super Action AI",
  "mode": "execute",
  "message": "Create automation",
  "workflow_action": "86fc68be-f227-4ea6-be46-d491e59dba10",
  "reply": "I've created a workflow (ID: 86fc68be-f227-4ea6-be46-d491e59dba10) to automate this. It's now running. I'll track performance and savings.",
  "savings": {
    "weekly_savings": 793.33,
    "monthly_savings": 3435.13,
    "yearly_savings": 41253.33,
    "hours_saved_per_week": 23.33,
    "error_savings_weekly": 210.0,
    "scaling_savings_weekly": 0.0,
    "total_weekly_savings": 793.33
  }
}
```

## 🧪 Testing

Run the example component:

```bash
# Start backend
python flask_dashboard.py

# In another terminal, start frontend
cd frontend
npm run dev
```

Visit: http://localhost:3000/chat-example

## 🔗 Backend Integration

This client connects to:
- **Endpoint:** `POST /api/chat`
- **Backend File:** `flask_dashboard.py` (line ~8095)
- **Dependencies:** 
  - Calculator module (`calculators.py`)
  - Workflow engine (`workflow_engine.py`)

## 🎨 UI Component

See `components/ChatExample.tsx` for a complete working example with:
- Message input
- Calculator parameter controls
- Chat/Execute mode buttons
- Loading states
- Error handling
- Response display with savings breakdown

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**
