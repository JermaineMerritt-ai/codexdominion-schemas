import { fetchOverview } from "@/lib/api/dashboard";
import { fetchAnalyticsSummary, fetchWorkflowMetrics } from "@/lib/api/analytics";
import { fetchAgentPerformance } from "@/lib/api/agents";
import { fetchAdvisorRecommendations } from "@/lib/api/advisor";
import { Icon, Card, CardHeader, CardBody, Avatar, Badge, StatusBadge } from "@/components/ui";
import { RecommendationCard } from "@/components/advisor/RecommendationCard";
import { formatCurrency } from "@/lib/design-system";

export default async function OverviewPage() {
  const [overview, analytics, metrics, agents, advisorData] = await Promise.all([
    fetchOverview(),
    fetchAnalyticsSummary(),
    fetchWorkflowMetrics(),
    fetchAgentPerformance(),
    fetchAdvisorRecommendations("tenant_codexdominion", "pending", 5)
  ]);

  // Defensive checks to ensure arrays
  const safeMetrics = Array.isArray(metrics) ? metrics : [];
  const safeAgents = Array.isArray(agents) ? agents : [];

  const recentWorkflows = safeMetrics.slice(-5).reverse();
  const topAgents = safeAgents
    .slice()
    .sort((a, b) => b.total_weekly_savings - a.total_weekly_savings)
    .slice(0, 3);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Icon name="crown" size={32} className="text-sovereign-gold" />
          <div>
            <h1 className="text-2xl font-bold text-white">
              CODEXDOMINION <span className="text-sovereign-gold">Master Dashboard</span>
            </h1>
            <p className="text-sm text-slate-400">
              Unified command center for engines, agents, councils, workflows, and savings.
            </p>
          </div>
        </div>
        <Badge variant="emerald">
          <Icon name="checkCircle" size={14} className="inline mr-1" />
          All Systems Operational
        </Badge>
      </header>

      <section className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard icon="layers" label="Capsules" value={overview.capsule_count} color="blue" />
        <StatCard icon="brain" label="Engines" value={overview.engine_count} color="violet" />
        <StatCard icon="shield" label="Realms" value={overview.realm_count} color="emerald" />
        <StatCard icon="spark" label="AI Agents" value={overview.agents_count} color="gold" />
        <StatCard icon="users" label="Councils" value={overview.councils_count} color="blue" />
        <StatCard icon="workflow" label="Tools" value={overview.tools_count} color="violet" />
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          icon="checkCircle"
          label="Workflows Completed"
          value={analytics.total_workflows_completed}
          color="emerald"
        />
        <StatCard
          icon="coins"
          label="Est. Weekly Savings"
          value={formatCurrency(analytics.total_estimated_weekly_savings)}
          color="gold"
          highlight
        />
        <StatCard
          icon="chart"
          label="Success Rate"
          value={`${Math.round(analytics.success_rate * 100)}%`}
          color="emerald"
        />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="workflow" className="text-sovereign-blue" />
              <h2 className="text-sm font-semibold text-white">Recent Workflows</h2>
            </div>
          </CardHeader>
          <CardBody>
            {recentWorkflows.length === 0 ? (
              <div className="text-sm text-slate-500">
                No workflows have been executed yet.
              </div>
            ) : (
              <div className="space-y-3">
                {recentWorkflows.map(w => (
                  <div
                    key={w.action_id}
                    className="flex items-center justify-between p-2 rounded-md hover:bg-sovereign-slate transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <Icon name="checkCircle" size={16} className="text-sovereign-emerald" />
                      <div>
                        <div className="font-mono text-xs text-white">{w.action_id}</div>
                        <div className="text-xs text-slate-400">
                          ⚡ {w.duration_seconds.toFixed(1)}s • {w.created_by_agent}
                        </div>
                      </div>
                    </div>
                    <div className="text-sovereign-gold font-semibold">
                      {formatCurrency(w.estimated_weekly_savings)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="crown" className="text-sovereign-gold" />
              <h2 className="text-sm font-semibold text-white">Top Agents by Savings</h2>
            </div>
          </CardHeader>
          <CardBody>
            {topAgents.length === 0 ? (
              <div className="text-sm text-slate-500">
                No agent performance data yet.
              </div>
            ) : (
              <div className="space-y-3">
                {topAgents.map((a, idx) => (
                  <div
                    key={a.agent_id}
                    className="flex items-center gap-3 p-2 rounded-md hover:bg-sovereign-slate transition-colors"
                  >
                    <Avatar domain="commerce" icon="spark" size="sm" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-sovereign-gold font-bold">#{idx + 1}</span>
                        <span className="font-medium text-white">{a.name}</span>
                      </div>
                      <div className="text-xs text-slate-400 font-mono">{a.agent_id}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sovereign-gold font-bold">
                        {formatCurrency(a.total_weekly_savings)}
                      </div>
                      <div className="text-xs text-slate-400">
                        {(a.approval_rate * 100).toFixed(0)}% • ⭐ {a.reputation_score.toFixed(2)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardBody>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="shield" className="text-sovereign-emerald" />
            <h2 className="text-sm font-semibold text-white">Governance Snapshot</h2>
          </div>
        </CardHeader>
        <CardBody>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <p className="text-sm text-slate-300">
                View pending workflows requiring council review and detailed governance activity from the
                Council Review and Council Console sections.
              </p>
            </div>
            <div className="flex gap-2">
              <Badge variant="blue">{analytics.workflows_pending} Pending</Badge>
              <Badge variant="crimson">{analytics.workflows_failed} Failed</Badge>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* AI Advisor Recommendations Section */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Icon name="brain" size={28} className="text-sovereign-violet" />
            <div>
              <h2 className="text-xl font-bold text-white">AI Advisor Recommendations</h2>
              <p className="text-sm text-slate-400">
                Intelligent automation suggestions powered by learning loops
              </p>
            </div>
          </div>
          <Badge variant="violet">
            {advisorData.total} pending
          </Badge>
        </div>

        {advisorData.recommendations.length === 0 ? (
          <Card>
            <CardBody className="text-center py-12">
              <Icon name="info" size={48} className="text-slate-600 mx-auto mb-4 opacity-50" />
              <h3 className="text-lg font-semibold text-white mb-2">No Active Recommendations</h3>
              <p className="text-sm text-slate-400 mb-4">
                AI Advisor is analyzing your workflows. Check back soon for personalized recommendations.
              </p>
              <button className="px-4 py-2 rounded-lg bg-sovereign-violet hover:bg-sovereign-violet/80 text-white font-semibold text-sm transition-colors">
                <Icon name="refresh" size={14} className="inline mr-2" />
                Refresh Analysis
              </button>
            </CardBody>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {advisorData.recommendations.map((rec) => (
              <RecommendationCard
                key={rec.id}
                recommendation={rec}
              />
            ))}
          </div>
        )}

        {advisorData.total > advisorData.recommendations.length && (
          <div className="text-center">
            <a
              href="/dashboard/advisor"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-sovereign-slate hover:bg-sovereign-slate/30 text-slate-300 text-sm transition-colors"
            >
              View All {advisorData.total} Recommendations
              <Icon name="arrowRight" size={14} />
            </a>
          </div>
        )}
      </section>
    </div>
  );
}

interface StatCardProps {
  icon: "layers" | "brain" | "shield" | "spark" | "users" | "workflow" | "coins" | "chart" | "checkCircle";
  label: string;
  value: string | number;
  color: "gold" | "blue" | "emerald" | "violet";
  highlight?: boolean;
}

function StatCard({ icon, label, value, color, highlight = false }: StatCardProps) {
  const colorMap = {
    gold: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    blue: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
    emerald: "text-sovereign-emerald border-sovereign-emerald/30 bg-sovereign-emerald/5",
    violet: "text-sovereign-violet border-sovereign-violet/30 bg-sovereign-violet/5",
  };

  return (
    <Card className={highlight ? "ring-2 ring-sovereign-gold" : ""}>
      <CardBody className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${colorMap[color]}`}>
          <Icon name={icon} size={24} className={colorMap[color].split(" ")[0]} />
        </div>
        <div>
          <div className="text-xs uppercase text-slate-400 font-semibold">{label}</div>
          <div className="text-2xl font-bold text-white mt-0.5">{value}</div>
        </div>
      </CardBody>
    </Card>
  );
}
