/**
 * Councils API
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

export interface CouncilOversight {
  review_actions: boolean;
  review_threshold_weekly_savings: number;
  blocked_action_types: string[];
  requires_majority_vote: boolean;
  min_votes: number;
}

export interface Council {
  id: string;
  name: string;
  description?: string;
  domain: string;
  purpose: string;
  members: string[];
  primary_engines: string[];
  oversight: CouncilOversight;
  status: string;
  created_at: string;
  total_votes: number;
  pending_reviews: number;
  // Legacy fields for backward compatibility
  agents?: string[];
  decision_threshold?: number;
  quorum?: number;
  voting_method?: string;
}

export async function fetchCouncils(): Promise<Council[]> {
  const res = await fetch(`${API_BASE}/api/councils`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch councils: ${res.status}`);
  }

  const data = await res.json();
  return data.councils || [];
}

export async function fetchCouncilById(id: string): Promise<Council | null> {
  const res = await fetch(`${API_BASE}/api/councils/${id}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    return null;
  }

  return res.json();
}
