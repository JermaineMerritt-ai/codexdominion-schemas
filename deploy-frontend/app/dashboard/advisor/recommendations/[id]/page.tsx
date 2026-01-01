import { Icon, Card, CardHeader, CardBody, Badge, StatusBadge } from "@/components/ui";
import { formatCurrency } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

interface Recommendation {
  id: string;
  title: string;
  description: string;
  impact_level: "high" | "medium" | "low";
  confidence_score: number;
  estimated_weekly_savings?: number;
  estimated_monthly_savings?: number;
  estimated_yearly_savings?: number;
  automation_complexity?: string;
  reasoning?: string;
  proposed_workflow?: {
    type: string;
    triggers: string[];
    actions: string[];
    conditions?: string[];
  };
  signals_analyzed?: {
    workflows_analyzed?: number;
    patterns_detected?: number;
    automation_opportunities?: number;
  };
  learning_loop_data?: {
    similar_recommendations_count?: number;
    average_acceptance_rate?: number;
    impact_accuracy?: number;
  };
  expires_at?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

async function fetchRecommendation(id: string): Promise<Recommendation | null> {
  try {
    const res = await fetch(`${API_BASE}/api/advisor/recommendations/${id}`, { 
      cache: "no-store" 
    });
    if (!res.ok) return null;
    return res.json();
  } catch (err) {
    console.error("Error fetching recommendation:", err);
    return null;
  }
}

export default async function ReviewRecommendationPage({ params }: { params: { id: string } }) {
  const recommendation = await fetchRecommendation(params.id);

  if (!recommendation) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="alert" size={48} className="text-slate-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Recommendation Not Found</h2>
          <p className="text-slate-400">This recommendation may have been dismissed or expired.</p>
          <a 
            href="/dashboard/overview"
            className="inline-flex items-center gap-2 mt-4 px-4 py-2 rounded-lg bg-sovereign-gold hover:bg-sovereign-gold/80 text-sovereign-obsidian font-semibold text-sm transition-colors"
          >
            <Icon name="arrowRight" size={14} />
            Back to Dashboard
          </a>
        </div>
      </div>
    );
  }

  const impactColors = {
    high: "text-sovereign-crimson border-sovereign-crimson/30 bg-sovereign-crimson/5",
    medium: "text-sovereign-gold border-sovereign-gold/30 bg-sovereign-gold/5",
    low: "text-sovereign-blue border-sovereign-blue/30 bg-sovereign-blue/5",
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <header className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <a 
              href="/dashboard/overview"
              className="text-slate-400 hover:text-white transition-colors"
            >
              <Icon name="arrowRight" size={16} className="rotate-180" />
            </a>
            <Badge variant="violet">AI Advisor</Badge>
            <Badge variant={recommendation.impact_level === "high" ? "crimson" : recommendation.impact_level === "medium" ? "gold" : "blue"}>
              {recommendation.impact_level.toUpperCase()} IMPACT
            </Badge>
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">
            {recommendation.title}
          </h1>
          <p className="text-sm text-slate-400">
            Generated {new Date(recommendation.created_at).toLocaleString()} • 
            {recommendation.confidence_score}% confidence
          </p>
        </div>
        <StatusBadge status={recommendation.status} />
      </header>

      {/* Impact Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {recommendation.estimated_weekly_savings && (
          <Card className="ring-2 ring-sovereign-gold/30">
            <CardBody>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-sovereign-gold/10 border border-sovereign-gold/30">
                  <Icon name="coins" size={24} className="text-sovereign-gold" />
                </div>
                <div>
                  <div className="text-xs text-slate-400 mb-1">Weekly Savings</div>
                  <div className="text-2xl font-bold text-sovereign-gold">
                    {formatCurrency(recommendation.estimated_weekly_savings)}
                  </div>
                </div>
              </div>
            </CardBody>
          </Card>
        )}
        {recommendation.estimated_monthly_savings && (
          <Card>
            <CardBody>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-sovereign-emerald/10 border border-sovereign-emerald/30">
                  <Icon name="chart" size={24} className="text-sovereign-emerald" />
                </div>
                <div>
                  <div className="text-xs text-slate-400 mb-1">Monthly Savings</div>
                  <div className="text-2xl font-bold text-white">
                    {formatCurrency(recommendation.estimated_monthly_savings)}
                  </div>
                </div>
              </div>
            </CardBody>
          </Card>
        )}
        <Card>
          <CardBody>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-sovereign-violet/10 border border-sovereign-violet/30">
                <Icon name="brain" size={24} className="text-sovereign-violet" />
              </div>
              <div>
                <div className="text-xs text-slate-400 mb-1">Confidence</div>
                <div className="text-2xl font-bold text-white">{recommendation.confidence_score}%</div>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Description & Reasoning */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="info" className="text-sovereign-blue" />
            <h2 className="text-lg font-semibold text-white">Recommendation Details</h2>
          </div>
        </CardHeader>
        <CardBody className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Description</h3>
            <p className="text-sm text-slate-400">{recommendation.description}</p>
          </div>
          {recommendation.reasoning && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-2">AI Reasoning</h3>
              <p className="text-sm text-slate-400">{recommendation.reasoning}</p>
            </div>
          )}
          {recommendation.automation_complexity && (
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Icon name="settings" size={14} />
              <span>Implementation complexity: <strong className="text-white">{recommendation.automation_complexity}</strong></span>
            </div>
          )}
        </CardBody>
      </Card>

      {/* Proposed Workflow */}
      {recommendation.proposed_workflow && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="workflow" className="text-sovereign-violet" />
              <h2 className="text-lg font-semibold text-white">Proposed Automation Workflow</h2>
            </div>
          </CardHeader>
          <CardBody className="space-y-4">
            <div>
              <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">Workflow Type</h3>
              <Badge variant="violet">{recommendation.proposed_workflow.type}</Badge>
            </div>
            <div>
              <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">Triggers</h3>
              <div className="flex flex-wrap gap-2">
                {recommendation.proposed_workflow.triggers.map((trigger, idx) => (
                  <Badge key={idx} variant="blue">
                    <Icon name="zap" size={10} className="inline mr-1" />
                    {trigger}
                  </Badge>
                ))}
              </div>
            </div>
            {recommendation.proposed_workflow.conditions && recommendation.proposed_workflow.conditions.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">Conditions</h3>
                <div className="space-y-1">
                  {recommendation.proposed_workflow.conditions.map((condition, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                      <Icon name="checkCircle" size={14} className="text-sovereign-emerald mt-0.5" />
                      <span>{condition}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div>
              <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">Actions</h3>
              <div className="space-y-1">
                {recommendation.proposed_workflow.actions.map((action, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-sm text-slate-300">
                    <Icon name="activity" size={14} className="text-sovereign-gold mt-0.5" />
                    <span>{action}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Signals Analyzed */}
      {recommendation.signals_analyzed && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="chart" className="text-sovereign-emerald" />
              <h2 className="text-lg font-semibold text-white">Analysis Data</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-3 gap-4 text-center">
              {recommendation.signals_analyzed.workflows_analyzed !== undefined && (
                <div>
                  <div className="text-2xl font-bold text-white mb-1">
                    {recommendation.signals_analyzed.workflows_analyzed}
                  </div>
                  <div className="text-xs text-slate-400">Workflows Analyzed</div>
                </div>
              )}
              {recommendation.signals_analyzed.patterns_detected !== undefined && (
                <div>
                  <div className="text-2xl font-bold text-white mb-1">
                    {recommendation.signals_analyzed.patterns_detected}
                  </div>
                  <div className="text-xs text-slate-400">Patterns Detected</div>
                </div>
              )}
              {recommendation.signals_analyzed.automation_opportunities !== undefined && (
                <div>
                  <div className="text-2xl font-bold text-sovereign-gold mb-1">
                    {recommendation.signals_analyzed.automation_opportunities}
                  </div>
                  <div className="text-xs text-slate-400">Opportunities Found</div>
                </div>
              )}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Learning Loop Stats */}
      {recommendation.learning_loop_data && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="brain" className="text-sovereign-violet" />
              <h2 className="text-lg font-semibold text-white">Learning Loop Insights</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-3 gap-4">
              {recommendation.learning_loop_data.similar_recommendations_count !== undefined && (
                <div>
                  <div className="text-xs text-slate-400 mb-1">Similar Recommendations</div>
                  <div className="text-xl font-bold text-white">
                    {recommendation.learning_loop_data.similar_recommendations_count}
                  </div>
                </div>
              )}
              {recommendation.learning_loop_data.average_acceptance_rate !== undefined && (
                <div>
                  <div className="text-xs text-slate-400 mb-1">Average Acceptance</div>
                  <div className="text-xl font-bold text-sovereign-emerald">
                    {(recommendation.learning_loop_data.average_acceptance_rate * 100).toFixed(0)}%
                  </div>
                </div>
              )}
              {recommendation.learning_loop_data.impact_accuracy !== undefined && (
                <div>
                  <div className="text-xs text-slate-400 mb-1">Impact Accuracy</div>
                  <div className="text-xl font-bold text-sovereign-gold">
                    {(recommendation.learning_loop_data.impact_accuracy * 100).toFixed(0)}%
                  </div>
                </div>
              )}
            </div>
          </CardBody>
        </Card>
      )}

      {/* Action Buttons */}
      <Card>
        <CardBody>
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => {/* TODO: Implement accept workflow */}}
              className="flex-1 px-6 py-3 rounded-lg bg-sovereign-emerald hover:bg-sovereign-emerald/80 text-white font-semibold transition-colors flex items-center justify-center gap-2"
            >
              <Icon name="checkCircle" size={16} />
              Accept & Create Workflow
            </button>
            <button
              onClick={() => {/* TODO: Implement request changes */}}
              className="flex-1 px-6 py-3 rounded-lg border-2 border-sovereign-gold hover:bg-sovereign-gold/10 text-sovereign-gold font-semibold transition-colors flex items-center justify-center gap-2"
            >
              <Icon name="edit" size={16} />
              Request Changes
            </button>
            <button
              onClick={() => {/* TODO: Implement dismiss */}}
              className="px-6 py-3 rounded-lg border border-sovereign-slate hover:bg-sovereign-slate/30 text-slate-300 font-semibold transition-colors flex items-center justify-center gap-2"
            >
              <Icon name="xCircle" size={16} />
              Dismiss
            </button>
          </div>
          <p className="text-xs text-slate-500 text-center mt-3">
            {recommendation.expires_at && (
              <>Expires {new Date(recommendation.expires_at).toLocaleString()} • </>
            )}
            Recommendation ID: {recommendation.id}
          </p>
        </CardBody>
      </Card>
    </div>
  );
}
