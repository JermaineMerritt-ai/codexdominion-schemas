/**
 * Chat API Client
 * 
 * Unified interface for conversational and workflow execution modes
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

async function postJSON<T>(path: string, body: any): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    throw new Error(`Failed POST ${path}: ${res.status}`);
  }
  return res.json();
}

export interface ChatResponse {
  agent_id: string;
  agent_name: string | null;
  mode: string;
  message: string;
  reply: string;
  workflow_action?: string;
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

export interface ChatOptions {
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

/**
 * Send a message to an AI agent
 * 
 * @param options - Chat configuration
 * @returns Promise with agent response and optional workflow data
 * 
 * @example
 * // Conversational mode
 * const response = await sendChat({
 *   agentId: "agent_jermaine_super_action",
 *   message: "Hello!",
 *   mode: "chat"
 * });
 * 
 * @example
 * // Execute mode with ROI calculation
 * const response = await sendChat({
 *   agentId: "agent_jermaine_super_action",
 *   message: "Create customer followup automation",
 *   mode: "execute",
 *   context: {
 *     calculator_inputs: {
 *       tasks_per_week: 200,
 *       time_per_task_minutes: 10,
 *       hourly_wage: 25,
 *       automation_percent: 0.7
 *     },
 *     workflow_inputs: {
 *       workflow_name: "Customer Followup",
 *       target_platform: "Email"
 *     }
 *   }
 * });
 * console.log(response.savings?.yearly_savings); // 41253.33
 * console.log(response.workflow_action); // UUID
 */
export async function sendChat(options: ChatOptions): Promise<ChatResponse> {
  return postJSON<ChatResponse>("/api/chat", {
    agent_id: options.agentId,
    message: options.message,
    mode: options.mode || "chat",
    context: options.context || {}
  });
}

/**
 * Send a chat message (shorthand for mode='chat')
 */
export async function chatWithAgent(
  agentId: string,
  message: string
): Promise<ChatResponse> {
  return sendChat({ agentId, message, mode: "chat" });
}

/**
 * Execute a workflow with ROI calculation (shorthand for mode='execute')
 */
export async function executeWorkflow(
  agentId: string,
  message: string,
  context: ChatOptions["context"]
): Promise<ChatResponse> {
  return sendChat({ agentId, message, mode: "execute", context });
}
