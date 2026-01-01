/**
 * Chat API - Workflow Suggestions Integration
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

export interface WorkflowSuggestion {
  id: string;
  name: string;
  description: string;
  category: string;
  domain: string;
  required_inputs?: string[];
}

export interface SuggestWorkflowsResponse {
  message: string;
  suggestions: WorkflowSuggestion[];
}

export interface ChatResponse {
  reply: string;
  workflow_action?: {
    id: string;
    workflow_type: string;
    status: string;
    savings: {
      weekly_savings: number;
      yearly_savings: number;
      hours_saved_per_week: number;
    };
  };
  workflow_type?: {
    id: string;
    name: string;
    description: string;
    required_inputs: string[];
    default_profile: Record<string, any>;
  };
}

/**
 * Get workflow suggestions based on user message
 */
export async function suggestWorkflows(message: string): Promise<SuggestWorkflowsResponse> {
  const res = await fetch(`${API_BASE}/api/workflow-suggestions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  
  if (!res.ok) {
    throw new Error(`Failed to get workflow suggestions: ${res.status}`);
  }
  
  return res.json();
}

/**
 * Send chat message with different modes
 * @param agentId - Agent identifier
 * @param message - User message
 * @param mode - Chat mode: "chat", "suggest", "confirm", "execute"
 * @param context - Optional context (e.g., workflow_type, calculator_inputs)
 */
export async function sendChat(
  agentId: string,
  message: string,
  mode: "chat" | "suggest" | "confirm" | "execute" = "chat",
  context?: Record<string, any>
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      agent_id: agentId,
      message,
      mode,
      context,
    }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }

  return res.json();
}

/**
 * Get workflow type details with required inputs
 */
export async function getWorkflowType(workflowId: string) {
  const res = await fetch(`${API_BASE}/api/workflow-types`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch workflow types: ${res.status}`);
  }

  const types = await res.json();
  return types[workflowId];
}

/**
 * Execute workflow with calculator inputs
 */
export async function executeWorkflow(
  agentId: string,
  workflowType: string,
  calculatorInputs: Record<string, any>
): Promise<ChatResponse> {
  return sendChat(agentId, `Execute ${workflowType} workflow`, "execute", {
    workflow_type: workflowType,
    calculator_inputs: calculatorInputs,
  });
}
