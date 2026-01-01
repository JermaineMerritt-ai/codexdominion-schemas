const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

export interface AdvisorRecommendation {
  id: string;
  title: string;
  description: string;
  impact_level: "high" | "medium" | "low";
  confidence_score: number;
  estimated_weekly_savings?: number;
  estimated_monthly_savings?: number;
  automation_complexity?: string;
  expires_at?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface AdvisorRecommendationsResponse {
  recommendations: AdvisorRecommendation[];
  total: number;
}

/**
 * Fetch AI Advisor recommendations
 * GET /api/advisor/recommendations?tenant_id=...&status=...&limit=...
 */
export async function fetchAdvisorRecommendations(
  tenantId: string = "tenant_codexdominion",
  status: string = "pending",
  limit: number = 5
): Promise<AdvisorRecommendationsResponse> {
  try {
    const params = new URLSearchParams({ tenant_id: tenantId, status, limit: limit.toString() });
    const res = await fetch(`${API_BASE}/api/advisor/recommendations?${params}`, { cache: "no-store" });
    
    if (!res.ok) {
      console.warn(`Advisor API returned ${res.status}`);
      return { recommendations: [], total: 0 };
    }
    
    return res.json();
  } catch (err) {
    console.error("Error fetching advisor recommendations:", err);
    return { recommendations: [], total: 0 };
  }
}

/**
 * Refresh AI Advisor recommendations
 * POST /api/advisor/recommendations/refresh
 */
export async function refreshAdvisorRecommendations(
  tenantId: string = "tenant_codexdominion",
  days: number = 30
): Promise<{ success: boolean; recommendations_created: number; message?: string }> {
  try {
    const res = await fetch(`${API_BASE}/api/advisor/recommendations/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tenant_id: tenantId, days }),
    });
    
    if (!res.ok) {
      const text = await res.text();
      console.warn(`Refresh failed: ${res.status} - ${text}`);
      return { success: false, recommendations_created: 0, message: text };
    }
    
    return res.json();
  } catch (err) {
    console.error("Error refreshing recommendations:", err);
    return { success: false, recommendations_created: 0, message: String(err) };
  }
}

/**
 * Dismiss a recommendation
 * POST /api/advisor/recommendations/{id}/dismiss
 */
export async function dismissRecommendation(
  recommendationId: string,
  reason?: string
): Promise<{ success: boolean; message?: string }> {
  try {
    const res = await fetch(`${API_BASE}/api/advisor/recommendations/${recommendationId}/dismiss`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reason }),
    });
    
    if (!res.ok) {
      const text = await res.text();
      return { success: false, message: text };
    }
    
    return res.json();
  } catch (err) {
    console.error("Error dismissing recommendation:", err);
    return { success: false, message: String(err) };
  }
}
