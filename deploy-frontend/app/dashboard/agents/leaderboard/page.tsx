import { fetchAgentPerformance } from "@/lib/api";

export default async function AgentLeaderboardPage() {
  const agents = await fetchAgentPerformance();
  const sorted = agents.slice().sort(
    (a, b) => b.total_weekly_savings - a.total_weekly_savings
  );

  return (
    <div className="space-y-6 max-w-4xl">
      <h1 className="text-2xl font-semibold">Agent Leaderboard</h1>
      <p className="text-sm text-slate-400">
        Ranked by estimated weekly savings, with reputation and approval rates.
      </p>

      <div className="border border-slate-800 rounded-lg bg-slate-900">
        {sorted.length === 0 ? (
          <div className="p-4 text-sm text-slate-500">
            No agent performance data yet. Execute some workflows to populate this leaderboard.
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-slate-950 text-xs text-slate-400">
              <tr className="text-left">
                <th className="px-3 py-2">Rank</th>
                <th className="px-3 py-2">Agent</th>
                <th className="px-3 py-2">Weekly savings</th>
                <th className="px-3 py-2">Workflows</th>
                <th className="px-3 py-2">Approval rate</th>
                <th className="px-3 py-2">Reputation</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((a, idx) => (
                <tr key={a.agent_id} className="border-t border-slate-800">
                  <td className="px-3 py-2 text-xs text-slate-400">
                    #{idx + 1}
                  </td>
                  <td className="px-3 py-2">
                    <div className="font-medium">{a.name}</div>
                    <div className="text-xs text-slate-500 font-mono">
                      {a.agent_id}
                    </div>
                  </td>
                  <td className="px-3 py-2">
                    ${a.total_weekly_savings.toLocaleString()}
                  </td>
                  <td className="px-3 py-2">{a.workflows_executed}</td>
                  <td className="px-3 py-2">
                    {(a.approval_rate * 100).toFixed(0)}%
                  </td>
                  <td className="px-3 py-2">
                    <span className="px-2 py-1 rounded-full bg-slate-800 text-xs">
                      {a.reputation_score.toFixed(2)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
