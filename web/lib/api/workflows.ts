/**
 * Workflow API Client
 * Functions for interacting with workflow catalog and metrics endpoints
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

/**
 * Fetch all available workflow types from the catalog
 */
export async function fetchWorkflowTypes() {
  const res = await fetch(`${BASE_URL}/api/workflow-types`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch workflow types");
  return res.json();
}

/**
 * Fetch workflow metrics (counts, status distribution, total savings)
 */
export async function fetchWorkflowMetrics() {
  const res = await fetch(`${BASE_URL}/api/workflows/metrics`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch workflow metrics");
  return res.json();
}

/**
 * Fetch a specific workflow type by ID
 */
export async function fetchWorkflowType(workflowTypeId: string) {
  const res = await fetch(`${BASE_URL}/api/workflows/types/${workflowTypeId}`, { 
    cache: "no-store" 
  });
  if (!res.ok) throw new Error(`Failed to fetch workflow type: ${workflowTypeId}`);
  return res.json();
}

/**
 * Fetch all workflows (actions)
 */
export async function fetchWorkflows() {
  const res = await fetch(`${BASE_URL}/api/workflows`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch workflows");
  return res.json();
}

/**
 * Fetch a specific workflow by ID
 */
export async function fetchWorkflow(workflowId: string) {
  const res = await fetch(`${BASE_URL}/api/workflows/${workflowId}`, { 
    cache: "no-store" 
  });
  if (!res.ok) throw new Error(`Failed to fetch workflow: ${workflowId}`);
  return res.json();
}

/**
 * TypeScript Interfaces
 */

export interface WorkflowType {
  id: string;
  name: string;
  description: string;
  category: string;
  domain: string;
  required_inputs: string[];
}

export interface WorkflowMetrics {
  total_actions: number;
  status_counts: {
    pending: number;
    running: number;
    completed: number;
    failed: number;
  };
  total_savings: {
    weekly: number;
    monthly: number;
    yearly: number;
  };
  actions_by_type: Record<string, number>;
}

export interface WorkflowAction {
  id: string;
  action_type: string;
  created_by_agent: string;
  inputs: Record<string, any>;
  calculated_savings: {
    weekly_savings: number;
    monthly_savings: number;
    yearly_savings: number;
    hours_saved_per_week: number;
    error_savings_weekly: number;
    scaling_savings_weekly: number;
    total_weekly_savings: number;
  };
  status: "pending" | "running" | "completed" | "failed";
  created_at: number;
  updated_at: number;
}
