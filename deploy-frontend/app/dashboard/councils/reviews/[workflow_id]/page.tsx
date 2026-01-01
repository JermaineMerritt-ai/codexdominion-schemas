import { notFound } from "next/navigation";

async function fetchIntakeWorkflow(workflowId: string) {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
  const res = await fetch(`${API_BASE}/api/workflows/${workflowId}`, { cache: "no-store" });
  
  if (!res.ok) return null;
  return res.json();
}

async function approveIntake(workflowId: string) {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
  const res = await fetch(`${API_BASE}/api/workflows/${workflowId}/approve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" }
  });
  
  return res.json();
}

export default async function IntakeReviewPage({ params }: { params: { workflow_id: string } }) {
  const { workflow_id } = params;
  const workflow = await fetchIntakeWorkflow(workflow_id);
  
  if (!workflow) {
    notFound();
  }
  
  const inputs = workflow.inputs || {};
  const savings = workflow.calculated_savings || {};
  const summary = savings.intake_summary || "No summary generated";
  const fitScore = savings.fit_score || 0;
  const scoreBreakdown = savings.score_breakdown || {};
  const recommendation = savings.recommendation || "hold";
  
  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Empire Store Ignition Intake Review</h1>
          <p className="text-slate-400">
            Review the prospect's readiness and approve to initiate store creation.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Intake Summary */}
          <div className="lg:col-span-2 space-y-6">
            {/* Intake Summary Card */}
            <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
              <h2 className="text-xl font-bold mb-6 text-emerald-400">Intake Summary</h2>
              
              {/* Brand Overview */}
              <div className="mb-6">
                <h3 className="font-bold mb-3 text-slate-300">Brand Overview</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex">
                    <span className="text-slate-400 w-40">Brand Name:</span>
                    <span className="font-medium">{inputs.brand_name}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Brand Description:</span>
                    <span className="flex-1">{inputs.brand_description}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Primary Products:</span>
                    <span className="flex-1">{inputs.primary_products?.join(", ") || "None"}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Target Audience:</span>
                    <span className="flex-1">{inputs.target_audience}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Target Countries:</span>
                    <span>{inputs.target_countries?.join(", ") || "None"}</span>
                  </div>
                </div>
              </div>

              {/* Founder / Contact */}
              <div className="mb-6">
                <h3 className="font-bold mb-3 text-slate-300">Founder / Contact</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex">
                    <span className="text-slate-400 w-40">Name:</span>
                    <span className="font-medium">{inputs.contact_name}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Email:</span>
                    <span className="font-mono text-emerald-400">{inputs.contact_email}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Current Stage:</span>
                    <span>{inputs.current_stage?.replace(/_/g, " ").toUpperCase()}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Current Platform:</span>
                    <span>{inputs.current_store_platform?.replace(/_/g, " ").toUpperCase()}</span>
                  </div>
                  {inputs.current_store_url && (
                    <div className="flex">
                      <span className="text-slate-400 w-40">Current Store URL:</span>
                      <a href={inputs.current_store_url} target="_blank" className="text-emerald-400 hover:underline">
                        {inputs.current_store_url}
                      </a>
                    </div>
                  )}
                </div>
              </div>

              {/* Goals & Readiness */}
              <div>
                <h3 className="font-bold mb-3 text-slate-300">Goals & Readiness</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex">
                    <span className="text-slate-400 w-40">Revenue Goal:</span>
                    <span className="font-bold text-emerald-400">
                      ${inputs.estimated_monthly_revenue_goal?.toLocaleString()}/month
                    </span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Timeline:</span>
                    <span>{inputs.timeline_readiness?.replace(/_/g, " ").toUpperCase()}</span>
                  </div>
                  <div className="flex">
                    <span className="text-slate-400 w-40">Preferred Platform:</span>
                    <span>{inputs.preferred_platform?.toUpperCase()}</span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-slate-400 mb-1">Biggest Blockers:</span>
                    <span className="text-slate-300 pl-4 border-l-2 border-slate-700">
                      {inputs.biggest_blockers}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* AI Recommendation Card */}
            <div className="border border-emerald-600 bg-emerald-950/20 rounded-lg p-6">
              <h2 className="text-xl font-bold mb-4 text-emerald-400">CodexDominion Recommendation</h2>
              
              <div className="prose prose-invert prose-sm max-w-none mb-6">
                <pre className="whitespace-pre-wrap font-sans text-sm text-slate-200 bg-slate-900/50 p-4 rounded">
                  {summary}
                </pre>
              </div>

              {/* Score Breakdown */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <div className="text-slate-400 mb-1">Brand Clarity</div>
                  <div className="font-bold">{scoreBreakdown.brand_clarity || 0}/3</div>
                </div>
                <div>
                  <div className="text-slate-400 mb-1">Product Clarity</div>
                  <div className="font-bold">{scoreBreakdown.product_clarity || 0}/3</div>
                </div>
                <div>
                  <div className="text-slate-400 mb-1">Revenue Ambition</div>
                  <div className="font-bold">{scoreBreakdown.revenue_ambition || 0}/3</div>
                </div>
                <div>
                  <div className="text-slate-400 mb-1">Timeline Readiness</div>
                  <div className="font-bold">{scoreBreakdown.timeline_readiness || 0}/3</div>
                </div>
                <div>
                  <div className="text-slate-400 mb-1">Platform Fit</div>
                  <div className="font-bold">{scoreBreakdown.platform_fit || 0}/3</div>
                </div>
                <div>
                  <div className="text-slate-400 mb-1">Blocker Severity</div>
                  <div className="font-bold">{scoreBreakdown.blocker_severity || 0}/3</div>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-emerald-700">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm text-slate-400">Total Fit Score</div>
                    <div className="text-3xl font-bold text-emerald-400">{fitScore}/18</div>
                  </div>
                  <div className={`px-4 py-2 rounded font-bold ${
                    recommendation === "approve" 
                      ? "bg-emerald-600 text-white" 
                      : "bg-yellow-600 text-white"
                  }`}>
                    {recommendation.toUpperCase()}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Governance Panel */}
          <div className="space-y-6">
            {/* Governance Info */}
            <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
              <h2 className="text-lg font-bold mb-4 text-emerald-400">Governance</h2>
              
              <div className="space-y-4 text-sm">
                <div>
                  <div className="text-slate-400 mb-1">Council</div>
                  <div className="font-medium">Commerce Council</div>
                </div>
                
                <div>
                  <div className="text-slate-400 mb-1">Workflow ID</div>
                  <div className="font-mono text-xs text-emerald-400">{workflow.id}</div>
                </div>
                
                <div>
                  <div className="text-slate-400 mb-1">Status</div>
                  <div className="font-medium">{workflow.status?.replace(/_/g, " ").toUpperCase()}</div>
                </div>
                
                <div>
                  <div className="text-slate-400 mb-1">Risk Flags</div>
                  <div className="flex flex-wrap gap-1">
                    <span className="px-2 py-1 bg-yellow-600/20 border border-yellow-600 rounded text-xs">
                      Client Fit
                    </span>
                    <span className="px-2 py-1 bg-yellow-600/20 border border-yellow-600 rounded text-xs">
                      Financial Commitment
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <form action={`/api/workflows/${workflow.id}/approve`} method="POST">
                <button
                  type="submit"
                  className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 rounded font-bold"
                >
                  ✅ Approve & Create Store Workflow
                </button>
              </form>
              
              <form action={`/api/workflows/${workflow.id}/decline`} method="POST">
                <button
                  type="submit"
                  className="w-full py-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded font-bold"
                >
                  ❌ Decline Intake
                </button>
              </form>
            </div>

            {/* Workflow Timeline */}
            <div className="border border-slate-800 bg-slate-900 rounded-lg p-6">
              <h2 className="text-lg font-bold mb-4 text-emerald-400">Timeline</h2>
              
              <div className="space-y-3 text-sm">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5"></div>
                  <div className="flex-1">
                    <div className="font-medium">Intake Submitted</div>
                    <div className="text-xs text-slate-400">
                      {new Date(workflow.created_at).toLocaleString()}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5"></div>
                  <div className="flex-1">
                    <div className="font-medium">Worker Scored & Summarized</div>
                    <div className="text-xs text-slate-400">
                      Score: {fitScore}/18
                    </div>
                  </div>
                </div>
                
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-yellow-500 mt-1.5"></div>
                  <div className="flex-1">
                    <div className="font-medium">Assigned to Commerce Council</div>
                    <div className="text-xs text-slate-400">
                      Decision pending
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
