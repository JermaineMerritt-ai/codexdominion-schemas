/**
 * Workflow API client
 * Connects to Flask backend at Azure Container Apps
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

export interface Workflow {
  id: string;
  workflow_type_id: string | null;
  action_type: string | null;
  created_by_agent: string | null;
  inputs: Record<string, any> | null;
  calculated_savings: {
    weekly?: number;
    monthly?: number;
    yearly?: number;
  } | null;
  status: string | null;
  assigned_council_id: string | null;
  created_at: string;
}

export async function fetchWorkflow(id: string): Promise<Workflow | null> {
  try {
    const response = await fetch(`${API_BASE}/api/workflows/${id}`, {
      cache: "no-store",
    });
    
    if (!response.ok) {
      return null;
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching workflow:", error);
    return null;
  }
}

export async function fetchWorkflows(): Promise<Workflow[]> {
  try {
    const response = await fetch(`${API_BASE}/api/workflows`, {
      cache: "no-store",
    });
    
    if (!response.ok) {
      return [];
    }
    
    return await response.json();
  } catch (error) {
    console.error("Error fetching workflows:", error);
    return [];
  }
}
