const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

export interface AnalyticsSummary {
  total_workflows_completed: number;
  total_estimated_weekly_savings: number;
  total_estimated_yearly_savings: number;
  average_workflow_duration_seconds: number;
  workflows_pending: number;
  workflows_failed: number;
}

export interface WorkflowMetric {
  action_id: string;
  workflow_type: string;
  created_by_agent: string;
  status: string;
  estimated_weekly_savings: number;
  duration_seconds: number;
  created_at: number;
}

/**
 * Fetch analytics summary
 * GET /api/analytics/summary
 */
export async function fetchAnalyticsSummary(): Promise<AnalyticsSummary> {
  try {
    const res = await fetch(`${API_BASE}/api/analytics/summary`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch analytics summary");
    return res.json();
  } catch (err) {
    console.error("Error fetching analytics summary:", err);
    return {
      total_workflows_completed: 0,
      total_estimated_weekly_savings: 0,
      total_estimated_yearly_savings: 0,
      average_workflow_duration_seconds: 0,
      workflows_pending: 0,
      workflows_failed: 0,
    };
  }
}

/**
 * Fetch workflow metrics
 * GET /api/workflows/metrics
 */
export async function fetchWorkflowMetrics(): Promise<WorkflowMetric[]> {
  try {
    const res = await fetch(`${API_BASE}/api/workflows/metrics`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch workflow metrics");
    return res.json();
  } catch (err) {
    console.error("Error fetching workflow metrics:", err);
    return [];
  }
}
