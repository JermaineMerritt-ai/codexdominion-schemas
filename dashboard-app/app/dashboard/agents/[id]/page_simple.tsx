import { Icon } from "@/components/ui";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Import types from the main page
interface AgentExtended {
  id: string;
  name: string;
  role: string | null;
  personality: string | null;
  mode: string | null;
  avatar_icon: string | null;
  avatar_color: string | null;
  created_at: string;
  domain: string;
  reputation: {
    score: number;
    total_savings: number;
    workflows_executed: number;
    approval_rate: number;
    updated_at: string;
  } | null;
  training: {
    strengths: string[];
    weaknesses: string[];
    restricted_workflow_types: string[];
    last_feedback: string | null;
    updated_at: string;
  } | null;
  engines: string[];
  councils: Array<{
    id: string;
    name: string;
    domain: string | null;
    status: string | null;
  }>;
  status: "active" | "inactive" | "training";
  last_active: string;
}

async function fetchAgentProfile(agentId: string): Promise<AgentExtended> {
  const res = await fetch(`${API_BASE}/api/agents/${agentId}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch agent profile: ${agentId}`);
  }
  return res.json();
}

function formatDate(ts: string | null) {
  if (!ts) return "";
  return new Date(ts).toLocaleString();
}

export default async function AgentProfilePage({ params }: { params: { id: string } }) {
  const profile = await fetchAgentProfile(params.id);

  const rep = profile.reputation;
  const training = profile.training;

  return (
    <div className="space-y-6 max-w-4xl">
      <header className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className="w-12 h-12 rounded-full flex items-center justify-center"
            style={{
              backgroundColor: profile.avatar_color || "#1e293b",
              border: `2px solid ${profile.avatar_color || "#1e293b"}80`
            }}
          >
            {profile.avatar_icon ? (
              <Icon name={profile.avatar_icon as any} size={24} className="text-white" />
            ) : (
              <span className="text-white font-bold text-sm">
                {profile.name
                  .split(" ")
                  .map(p => p[0])
                  .join("")
                  .slice(0, 2)
                  .toUpperCase()}
              </span>
            )}
          </div>
          <div>
            <h1 className="text-2xl font-semibold">{profile.name}</h1>
            <p className="text-sm text-slate-400">
              {profile.role || "AI Agent"} • Mode: {profile.mode || "unspecified"}
            </p>
            {profile.personality && (
              <p className="text-sm text-slate-500 italic mt-1">"{profile.personality}"</p>
            )}
          </div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <ReputationBadge score={rep?.score ?? null} />
          <div className="text-xs text-slate-400 font-mono">{profile.id}</div>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          label="Total savings (weekly)"
          value={`$${(rep?.total_savings || 0).toFixed(2)}`}
        />
        <MetricCard label="Workflows executed" value={rep?.workflows_executed || 0} />
        <MetricCard
          label="Approval rate"
          value={
            rep?.approval_rate != null
              ? `${Math.round(rep.approval_rate * 100)}%`
              : "—"
          }
        />
        <MetricCard
          label="Councils"
          value={profile.councils.length}
        />
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-slate-800 rounded-lg bg-slate-900 p-4">
          <h2 className="text-sm font-semibold text-slate-100 mb-2">
            Strengths
          </h2>
          {training?.strengths && training.strengths.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {training.strengths.map(s => (
                <span
                  key={s}
                  className="px-2 py-1 text-xs rounded-full bg-emerald-900 text-emerald-200"
                >
                  {s}
                </span>
              ))}
            </div>
          ) : (
            <div className="text-sm text-slate-500">No strengths recorded yet.</div>
          )}
        </div>

        <div className="border border-slate-800 rounded-lg bg-slate-900 p-4">
          <h2 className="text-sm font-semibold text-slate-100 mb-2">
            Weaknesses / restrictions
          </h2>
          {training?.weaknesses && training.weaknesses.length > 0 ? (
            <div className="flex flex-wrap gap-2 mb-2">
              {training.weaknesses.map(w => (
                <span
                  key={w}
                  className="px-2 py-1 text-xs rounded-full bg-rose-900 text-rose-200"
                >
                  {w}
                </span>
              ))}
            </div>
          ) : (
            <div className="text-sm text-slate-500 mb-2">No weaknesses recorded yet.</div>
          )}
          {training?.restricted_workflow_types &&
            training.restricted_workflow_types.length > 0 && (
              <div className="mt-1">
                <div className="text-xs text-slate-400 mb-1">
                  Restricted workflows:
                </div>
                <div className="flex flex-wrap gap-2">
                  {training.restricted_workflow_types.map(r => (
                    <span
                      key={r}
                      className="px-2 py-1 text-xs rounded-full bg-slate-800 text-slate-200"
                    >
                      {r}
                    </span>
                  ))}
                </div>
              </div>
            )}
        </div>
      </section>

      <section className="border border-slate-800 rounded-lg bg-slate-900 p-4">
        <h2 className="text-sm font-semibold text-slate-100 mb-2">
          Training & feedback
        </h2>
        <p className="text-sm text-slate-300">
          {training?.last_feedback || "No feedback recorded for this agent yet."}
        </p>
        {profile.councils.length > 0 && (
          <div className="mt-3">
            <div className="text-xs text-slate-400 mb-1">
              Councils this agent participates in:
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.councils.map(c => (
                <span
                  key={c.id}
                  className="px-2 py-1 text-xs rounded-full bg-slate-800 text-slate-200"
                >
                  {c.name} {c.domain && `(${c.domain})`}
                </span>
              ))}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="border border-slate-800 rounded-lg p-4 bg-slate-900">
      <div className="text-xs uppercase text-slate-400">{label}</div>
      <div className="text-xl font-bold mt-1">{value}</div>
    </div>
  );
}

function ReputationBadge({ score }: { score: number | null }) {
  if (score == null) {
    return (
      <div className="px-3 py-1 rounded-full bg-slate-800 text-xs text-slate-200">
        No reputation yet
      </div>
    );
  }
  
  let color = "bg-emerald-900 text-emerald-200";
  if (score < 50) color = "bg-rose-900 text-rose-200";
  else if (score < 75) color = "bg-amber-900 text-amber-200";

  return (
    <div className={`px-3 py-1 rounded-full text-xs font-mono ${color}`}>
      Rep: {Math.round(score)}
    </div>
  );
}

function DecisionPill({ value }: { value: string | null }) {
  const v = (value || "").toLowerCase();
  let cls = "bg-slate-800 text-slate-200";
  if (v === "approved") cls = "bg-emerald-900 text-emerald-200";
  else if (v === "denied" || v === "failed") cls = "bg-rose-900 text-rose-200";
  else if (v === "pending") cls = "bg-amber-900 text-amber-200";

  return (
    <span className={`px-2 py-1 rounded-full text-xs ${cls}`}>
      {value || "—"}
    </span>
  );
}
