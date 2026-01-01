const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

export interface DashboardOverview {
  capsule_count: number;
  engine_count: number;
  realm_count: number;
  agents_count: number;
  councils_count: number;
  tools_count: number;
}

/**
 * Fetch dashboard overview counts
 * GET /api/dashboard/overview
 */
export async function fetchOverview(): Promise<DashboardOverview> {
  try {
    const res = await fetch(`${API_BASE}/api/dashboard/overview`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch overview");
    return res.json();
  } catch (err) {
    console.error("Error fetching dashboard overview:", err);
    return {
      capsule_count: 0,
      engine_count: 0,
      realm_count: 0,
      agents_count: 0,
      councils_count: 0,
      tools_count: 0,
    };
  }
}
