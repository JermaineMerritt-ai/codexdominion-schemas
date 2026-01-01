const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.status}`);
  }
  return res.json();
}

export async function fetchOverview() {
  return fetchJSON<{
    capsule_count: number;
    engine_count: number;
    realm_count: number;
    agents_count: number;
    councils_count: number;
    tools_count: number;
    status: string;
  }>("/api/dashboard/overview");
}

export async function fetchCapsules() {
  return fetchJSON<Record<string, any[]>>("/api/capsules");
}

export async function fetchEngines() {
  return fetchJSON<{ engines: any[] }>("/api/intelligence-core");
}

export async function fetchAgents() {
  return fetchJSON<{ agents: any[] }>("/api/agents");
}

export async function fetchCouncils() {
  return fetchJSON<{ councils: any[] }>("/api/councils");
}

export async function fetchTools() {
  return fetchJSON<{ tools: any[]; total_monthly_savings: number; active_tools: number; planned_tools: number }>("/api/tools");
}

export async function fetchCapsule(id: string) {
  return fetchJSON<any>(`/api/capsules/${id}`);
}

export async function fetchEngine(id: string) {
  return fetchJSON<any>(`/api/intelligence-core/${id}`);
}

export async function fetchAgent(id: string) {
  return fetchJSON<any>(`/api/agents/${id}`);
}

export async function fetchCouncil(id: string) {
  return fetchJSON<{
    id: string;
    name: string;
    purpose: string;
    domain: string;
    members: string[];
    primary_engines: string[];
    oversight: any;
    status: string;
  }>(`/api/councils/${id}`);
}

export async function fetchCouncilWorkflows(id: string) {
  const res = await fetch(
    `${BASE_URL}/api/workflows?assigned_council_id=${encodeURIComponent(id)}`,
    { cache: "no-store" }
  );
  if (!res.ok) throw new Error("Failed to fetch council workflows");
  return res.json() as Promise<
    {
      id: string;
      workflow_type_id: string;
      action_type: string;
      created_by_agent: string;
      status: string;
      decision: string;
      estimated_weekly_savings?: number;
      created_at: number;
    }[]
  >;
}

export async function fetchTool(id: string) {
  return fetchJSON<any>(`/api/tools/${id}`);
}

export async function fetchAgentPerformance() {
  const res = await fetch(`${BASE_URL}/api/analytics/agent-performance`, {
    cache: "no-store"
  });
  if (!res.ok) throw new Error("Failed to fetch agent performance");
  return res.json() as Promise<
    {
      agent_id: string;
      name: string;
      total_weekly_savings: number;
      workflows_executed: number;
      approval_rate: number;
      reputation_score: number;
    }[]
  >;
}
