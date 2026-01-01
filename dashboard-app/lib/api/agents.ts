const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

export interface AgentReputation {
  score: number;
  level: string;
  total_actions: number;
  successful_actions: number;
  failed_actions: number;
  success_rate: number;
  total_savings_generated: number;
  avg_savings_per_action: number;
  council_memberships: number;
  votes_cast: number;
  votes_approved: number;
  training_sessions_completed: number;
  improvements_implemented: number;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  rank: number;
  reputation: AgentReputation;
  specializations: string[];
  councils: string[];
  status: string;
  created_at: string;
  last_active: string;
}

export interface ReputationLevel {
  min_score: number;
  color: string;
  icon: string;
}

export interface AgentLeaderboard {
  agents: Agent[];
  reputation_levels: Record<string, ReputationLevel>;
  ranking_weights: Record<string, number>;
}

export async function fetchAgentLeaderboard(): Promise<AgentLeaderboard> {
  const res = await fetch(`${API_BASE}/api/agents/leaderboard`);
  if (!res.ok) throw new Error("Failed to fetch agent leaderboard");
  return res.json();
}

export async function fetchAgentById(id: string): Promise<Agent | null> {
  const res = await fetch(`${API_BASE}/api/agents/${id}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchAgentReputation(id: string): Promise<AgentReputation | null> {
  const res = await fetch(`${API_BASE}/api/agents/${id}/reputation`);
  if (!res.ok) return null;
  return res.json();
}

export interface AgentPerformance {
  agent_id: string;
  name: string;
  total_weekly_savings: number;
  workflows_executed: number;
  approval_rate: number;
  reputation_score: number;
}

/**
 * Fetch agent performance data for analytics
 * GET /api/analytics/agent-performance
 */
export async function fetchAgentPerformance(): Promise<AgentPerformance[]> {
  try {
    const res = await fetch(`${API_BASE}/api/analytics/agent-performance`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch agent performance");
    
    const data = await res.json();
    
    // Flask returns nested object with top_performers.by_savings
    // Transform to flat array format
    if (data.top_performers && Array.isArray(data.top_performers.by_savings)) {
      return data.top_performers.by_savings.map((agent: any) => ({
        agent_id: agent.id || '',
        name: agent.name || 'Unknown Agent',
        total_weekly_savings: agent.total_savings || 0,
        workflows_executed: 0, // Not provided by current endpoint
        approval_rate: 0.95, // Default - not provided by current endpoint
        reputation_score: 0 // Not provided by current endpoint
      }));
    }
    
    return [];
  } catch (err) {
    console.error("Error fetching agent performance:", err);
    return [];
  }
}
