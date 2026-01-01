"use client";

import { useState } from "react";
import { Icon, Card, CardHeader, CardBody, Badge, StatusBadge, Avatar } from "@/components/ui";
import { formatCurrency } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Draft schema from database
interface WorkflowDraft {
  id: string;
  tenant_id: string;
  created_by_user_id: string;
  workflow_type_id: string;
  name: string;
  purpose: string | null;
  inputs: Record<string, any> | null;
  preview_data: Record<string, any> | null;
  expected_outputs: string[] | null;
  estimated_duration_minutes: number | null;
  required_approvals: string[] | null;
  dependencies: string[] | null;
  status: "editing" | "pending_review" | "approved" | "rejected" | "converted" | "discarded";
  assigned_council_id: string | null;
  reviewed_by_user_id: string | null;
  review_comment: string | null;
  created_from_template_id: string | null;
  created_from_proposal_id: string | null;
  converted_to_workflow_id: string | null;
  created_at: string;
  updated_at: string;
  last_edited_at: string | null;
  reviewed_at: string | null;
  converted_at: string | null;
}

interface Template {
  id: string;
  name: string;
  description: string;
  is_pre_approved: boolean;
  usage_count: number;
}

interface Proposal {
  id: string;
  title: string;
  description: string;
  confidence_score: number;
  priority: string;
  expected_impact: Record<string, any> | null;
}

async function fetchDraft(draftId: string): Promise<{
  draft: WorkflowDraft | null;
  template: Template | null;
  proposal: Proposal | null;
}> {
  try {
    const res = await fetch(`${API_BASE}/api/drafts/${draftId}`, { cache: "no-store" });
    if (!res.ok) return { draft: null, template: null, proposal: null };
    return res.json();
  } catch (err) {
    console.error("Error fetching draft:", err);
    return { draft: null, template: null, proposal: null };
  }
}

function formatDate(ts: string) {
  return new Date(ts).toLocaleString();
}

function getStatusColor(status: string): "gold" | "blue" | "emerald" | "violet" | "crimson" | "slate" {
  const map: Record<string, any> = {
    editing: "blue",
    pending_review: "violet",
    approved: "emerald",
    rejected: "crimson",
    converted: "gold",
    discarded: "slate"
  };
  return map[status] || "slate";
}

export default async function DraftPage({ params }: { params: { id: string } }) {
  const draftId = params.id;
  const { draft, template, proposal } = await fetchDraft(draftId);

  if (!draft) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="clipboard" size={48} className="text-slate-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Draft Not Found</h2>
          <p className="text-slate-400">The draft "{draftId}" does not exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header Section */}
      <header className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-white">{draft.name}</h1>
              <Badge variant={getStatusColor(draft.status)}>
                <Icon name="workflow" size={12} className="inline mr-1" />
                {draft.status.replace(/_/g, " ")}
              </Badge>
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-400">
              <div className="flex items-center gap-1">
                <Icon name="users" size={14} />
                <span>Created by {draft.created_by_user_id}</span>
              </div>
              <span>•</span>
              <div className="flex items-center gap-1">
                <Icon name="clock" size={14} />
                <span>Last edited {draft.last_edited_at ? formatDate(draft.last_edited_at) : "never"}</span>
              </div>
              {draft.converted_to_workflow_id && (
                <>
                  <span>•</span>
                  <div className="flex items-center gap-1">
                    <Icon name="checkCircle" size={14} className="text-sovereign-emerald" />
                    <a 
                      href={`/portal/workflows/${draft.converted_to_workflow_id}`}
                      className="text-sovereign-emerald hover:underline"
                    >
                      View Workflow
                    </a>
                  </div>
                </>
              )}
            </div>
          </div>
          <DraftActionButtons draft={draft} />
        </div>

        {/* Source info (template or proposal) */}
        {(template || proposal) && (
          <div className="flex gap-2">
            {template && (
              <Badge variant="blue">
                <Icon name="clipboard" size={12} className="inline mr-1" />
                From Template: {template.name}
                {template.is_pre_approved && (
                  <span className="ml-1 text-sovereign-gold">✓ Pre-Approved</span>
                )}
              </Badge>
            )}
            {proposal && (
              <Badge variant="violet">
                <Icon name="brain" size={12} className="inline mr-1" />
                From AI Proposal (Confidence: {Math.round(proposal.confidence_score * 100)}%)
              </Badge>
            )}
          </div>
        )}
      </header>

      {/* Summary Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Icon name="info" className="text-sovereign-blue" />
            <h2 className="text-lg font-semibold text-white">Draft Summary</h2>
          </div>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Purpose</h3>
              <p className="text-sm text-white">{draft.purpose || "No purpose defined"}</p>
            </div>

            <div>
              <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Expected Outputs</h3>
              {draft.expected_outputs && draft.expected_outputs.length > 0 ? (
                <ul className="space-y-1">
                  {draft.expected_outputs.map((output, idx) => (
                    <li key={idx} className="text-sm text-white flex items-start gap-2">
                      <Icon name="checkCircle" size={14} className="text-sovereign-emerald mt-0.5" />
                      <span>{output}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-slate-400">Not specified</p>
              )}
            </div>

            <div>
              <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Estimated Time</h3>
              <div className="flex items-center gap-2">
                <Icon name="clock" size={20} className="text-sovereign-violet" />
                <span className="text-lg font-semibold text-white">
                  {draft.estimated_duration_minutes ? `${draft.estimated_duration_minutes} min` : "Unknown"}
                </span>
              </div>
            </div>

            {draft.required_approvals && draft.required_approvals.length > 0 && (
              <div>
                <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Required Approvals</h3>
                <div className="flex flex-wrap gap-2">
                  {draft.required_approvals.map((approval) => (
                    <Badge key={approval} variant="violet" size="sm">
                      {approval}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {draft.dependencies && draft.dependencies.length > 0 && (
              <div>
                <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Dependencies</h3>
                <ul className="space-y-1">
                  {draft.dependencies.map((dep, idx) => (
                    <li key={idx} className="text-sm text-white flex items-center gap-2">
                      <Icon name="workflow" size={12} className="text-slate-500" />
                      <span>{dep}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {draft.assigned_council_id && (
              <div>
                <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Assigned Council</h3>
                <Badge variant="emerald">
                  <Icon name="shield" size={12} className="inline mr-1" />
                  {draft.assigned_council_id}
                </Badge>
              </div>
            )}
          </div>
        </CardBody>
      </Card>

      {/* Inputs Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="edit" className="text-sovereign-violet" />
              <h2 className="text-lg font-semibold text-white">Workflow Inputs</h2>
            </div>
            {draft.status === "editing" && (
              <Badge variant="blue">Editable</Badge>
            )}
          </div>
        </CardHeader>
        <CardBody>
          {draft.status === "editing" ? (
            <DraftInputsEditor draft={draft} />
          ) : (
            <DraftInputsDisplay draft={draft} />
          )}
        </CardBody>
      </Card>

      {/* Preview Panel */}
      {draft.preview_data && Object.keys(draft.preview_data).length > 0 && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="eye" className="text-sovereign-gold" />
              <h2 className="text-lg font-semibold text-white">Live Preview</h2>
            </div>
          </CardHeader>
          <CardBody>
            <DraftPreview draft={draft} />
          </CardBody>
        </Card>
      )}

      {/* Review Section (if pending or completed review) */}
      {(draft.status === "pending_review" || draft.reviewed_at) && (
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Icon name="shield" className="text-sovereign-emerald" />
              <h2 className="text-lg font-semibold text-white">Council Review</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              {draft.reviewed_at && (
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-400">Reviewed By:</span>{" "}
                    <span className="text-white font-semibold">{draft.reviewed_by_user_id || "Unknown"}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Reviewed At:</span>{" "}
                    <span className="text-white">{formatDate(draft.reviewed_at)}</span>
                  </div>
                </div>
              )}

              {draft.review_comment && (
                <div>
                  <h3 className="text-xs uppercase text-slate-400 font-semibold mb-2">Review Comment</h3>
                  <div className="p-3 rounded-lg bg-sovereign-slate border border-sovereign-slate">
                    <p className="text-sm text-white whitespace-pre-wrap">{draft.review_comment}</p>
                  </div>
                </div>
              )}

              {draft.status === "pending_review" && (
                <div className="text-center py-4">
                  <Icon name="clock" size={48} className="text-sovereign-violet mx-auto mb-3 opacity-50" />
                  <p className="text-sm text-slate-400">
                    Awaiting council review...
                  </p>
                </div>
              )}
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
}

// ============================================================================
// CLIENT COMPONENTS (Interactive sections)
// ============================================================================

function DraftActionButtons({ draft }: { draft: WorkflowDraft }) {
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    setLoading(true);
    try {
      // Save logic will be implemented with form data
      alert("Save functionality to be implemented with form state");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!confirm("Submit this draft for council review?")) return;
    
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/drafts/${draft.id}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      
      if (res.ok) {
        alert("Draft submitted for review!");
        window.location.reload();
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      alert(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const handleConvert = async () => {
    if (!confirm("Convert this draft to a workflow? This will execute the workflow.")) return;
    
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/drafts/${draft.id}/convert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ auto_execute: true })
      });
      
      if (res.ok) {
        const data = await res.json();
        alert("Draft converted to workflow!");
        window.location.href = `/portal/workflows/${data.workflow_id}`;
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      alert(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDiscard = async () => {
    if (!confirm("Discard this draft? This action cannot be undone.")) return;
    
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/drafts/${draft.id}`, { method: "DELETE" });
      
      if (res.ok) {
        alert("Draft discarded!");
        window.location.href = "/portal/workflows/drafts";
      } else {
        const error = await res.json();
        alert(`Error: ${error.error}`);
      }
    } catch (err) {
      alert(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex gap-2">
      {draft.status === "editing" && (
        <>
          <button
            onClick={handleSave}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-sovereign-blue hover:bg-blue-600 text-white font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            <Icon name="save" size={16} />
            Save Draft
          </button>
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-sovereign-violet hover:bg-purple-600 text-white font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            <Icon name="upload" size={16} />
            Submit for Review
          </button>
        </>
      )}

      {draft.status === "approved" && !draft.converted_to_workflow_id && (
        <button
          onClick={handleConvert}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-sovereign-emerald hover:bg-emerald-600 text-white font-semibold flex items-center gap-2 disabled:opacity-50"
        >
          <Icon name="play" size={16} />
          Run Workflow
        </button>
      )}

      {draft.status !== "converted" && draft.status !== "discarded" && (
        <button
          onClick={handleDiscard}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-slate-600 hover:bg-slate-700 text-white font-semibold flex items-center gap-2 disabled:opacity-50"
        >
          <Icon name="trash" size={16} />
          Discard
        </button>
      )}
    </div>
  );
}

function DraftInputsEditor({ draft }: { draft: WorkflowDraft }) {
  const [inputs, setInputs] = useState(draft.inputs || {});

  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-400 mb-4">
        Edit the workflow inputs below. Changes are saved automatically.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(inputs).map(([key, value]) => (
          <div key={key} className="space-y-2">
            <label className="block text-sm font-semibold text-white">
              {key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
            </label>
            
            {typeof value === "object" && value !== null ? (
              <textarea
                value={JSON.stringify(value, null, 2)}
                onChange={(e) => {
                  try {
                    const parsed = JSON.parse(e.target.value);
                    setInputs({ ...inputs, [key]: parsed });
                  } catch {}
                }}
                className="w-full px-3 py-2 rounded-lg bg-sovereign-slate border border-sovereign-slate text-white font-mono text-xs"
                rows={4}
              />
            ) : typeof value === "boolean" ? (
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={value}
                  onChange={(e) => setInputs({ ...inputs, [key]: e.target.checked })}
                  className="w-4 h-4"
                />
                <span className="text-sm text-slate-300">Enabled</span>
              </label>
            ) : typeof value === "number" ? (
              <input
                type="number"
                value={value}
                onChange={(e) => setInputs({ ...inputs, [key]: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 rounded-lg bg-sovereign-slate border border-sovereign-slate text-white"
              />
            ) : (
              <input
                type="text"
                value={String(value)}
                onChange={(e) => setInputs({ ...inputs, [key]: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-sovereign-slate border border-sovereign-slate text-white"
              />
            )}
          </div>
        ))}
      </div>

      <div className="pt-4 border-t border-sovereign-slate">
        <button
          onClick={async () => {
            const res = await fetch(`${API_BASE}/api/drafts/${draft.id}`, {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ inputs })
            });
            if (res.ok) {
              alert("Inputs saved!");
            }
          }}
          className="px-4 py-2 rounded-lg bg-sovereign-blue hover:bg-blue-600 text-white font-semibold"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
}

function DraftInputsDisplay({ draft }: { draft: WorkflowDraft }) {
  const inputs = draft.inputs || {};

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(inputs).length === 0 ? (
        <p className="text-sm text-slate-400 col-span-2">No inputs defined</p>
      ) : (
        Object.entries(inputs).map(([key, value]) => (
          <div key={key} className="space-y-1">
            <h3 className="text-xs uppercase text-slate-400 font-semibold">
              {key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
            </h3>
            <div className="p-3 rounded-lg bg-sovereign-slate border border-sovereign-slate">
              {typeof value === "object" && value !== null ? (
                <pre className="text-xs text-white font-mono overflow-x-auto">
                  {JSON.stringify(value, null, 2)}
                </pre>
              ) : (
                <p className="text-sm text-white">{String(value)}</p>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

function DraftPreview({ draft }: { draft: WorkflowDraft }) {
  const preview = draft.preview_data || {};

  return (
    <div className="space-y-4">
      <p className="text-sm text-slate-400 mb-4">
        This is a preview of what will be generated when the workflow runs.
      </p>

      {Object.keys(preview).length === 0 ? (
        <div className="text-center py-8">
          <Icon name="eye" size={48} className="text-slate-600 mx-auto mb-3 opacity-50" />
          <p className="text-sm text-slate-400">
            No preview available. Submit the draft for review to generate a preview.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {Object.entries(preview).map(([key, value]) => (
            <div key={key}>
              <h3 className="text-sm font-semibold text-white mb-2">
                {key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </h3>
              <div className="p-4 rounded-lg bg-sovereign-slate border border-sovereign-slate">
                {typeof value === "object" && value !== null ? (
                  <pre className="text-xs text-white font-mono overflow-x-auto whitespace-pre-wrap">
                    {JSON.stringify(value, null, 2)}
                  </pre>
                ) : (
                  <p className="text-sm text-white whitespace-pre-wrap">{String(value)}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
