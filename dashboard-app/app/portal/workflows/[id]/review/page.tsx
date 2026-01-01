"use client";

import { useState, useEffect } from "react";
import {
  Icon,
  Card,
  CardHeader,
  CardBody,
  Badge,
  StatusBadge,
  Avatar,
} from "@/components/ui";
import { formatCurrency } from "@/lib/design-system";
import WorkflowCommentThread from "@/components/WorkflowCommentThread";
import WorkflowArtifacts from "@/components/WorkflowArtifacts";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

interface WorkflowReviewData {
  workflow: {
    id: string;
    workflow_type_id: string;
    tenant_id: string;
    status: string;
    decision_status: string;
    created_by: string;
    summary: string;
    inputs: Record<string, any>;
    outputs: Record<string, any>;
    calculated_savings: { weekly?: number; monthly?: number; yearly?: number };
    created_at: string;
    review_comment?: string;
    resubmission_count: number;
  };
  council: {
    id: string;
    name: string;
    description: string;
    requires_majority_vote: boolean;
    min_votes: number;
    members: any[];
  } | null;
  artifacts: any[];
  timeline: any[];
  comments: any[];
  reviewer: {
    id: string;
    name: string;
    email: string;
    reviewed_at: string;
  } | null;
}

export default function WorkflowReviewPage({
  params,
}: {
  params: { id: string };
}) {
  const [data, setData] = useState<WorkflowReviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [comment, setComment] = useState("");
  const [suggestedEdits, setSuggestedEdits] = useState("");

  useEffect(() => {
    fetchReviewData();
  }, [params.id]);

  async function fetchReviewData() {
    try {
      const res = await fetch(`${API_BASE}/api/workflows/${params.id}/review`, {
        cache: "no-store",
      });
      if (!res.ok) throw new Error("Failed to fetch review data");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Error fetching review data:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleApprove() {
    if (!confirm("Are you sure you want to approve this workflow?")) return;

    setActionLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/workflows/${params.id}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_current", // TODO: Get from auth context
          comment: comment,
        }),
      });

      if (!res.ok) throw new Error("Failed to approve workflow");

      // Refresh data
      await fetchReviewData();
      setComment("");
      alert("✅ Workflow approved successfully!");
    } catch (err) {
      console.error("Error approving workflow:", err);
      alert("❌ Failed to approve workflow");
    } finally {
      setActionLoading(false);
    }
  }

  async function handleRequestChanges() {
    if (!comment.trim()) {
      alert("Please provide a comment explaining the needed changes");
      return;
    }

    setActionLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/api/workflows/${params.id}/request-changes`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "user_current", // TODO: Get from auth context
            comment: comment,
            suggested_edits: suggestedEdits,
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to request changes");

      // Refresh data
      await fetchReviewData();
      setComment("");
      setSuggestedEdits("");
      alert("✅ Changes requested successfully!");
    } catch (err) {
      console.error("Error requesting changes:", err);
      alert("❌ Failed to request changes");
    } finally {
      setActionLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="workflow" size={48} className="text-slate-600 animate-pulse mx-auto mb-4" />
          <p className="text-slate-400">Loading workflow review...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Icon name="xCircle" size={48} className="text-crimson-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Workflow Not Found</h2>
          <p className="text-slate-400">The workflow could not be loaded.</p>
        </div>
      </div>
    );
  }

  const { workflow, council, artifacts, timeline, comments, reviewer } = data;
  const isPending = workflow.decision_status === "pending";
  const isApproved = workflow.decision_status === "approved";
  const needsRevision = workflow.decision_status === "needs_revision";

  return (
    <div className="space-y-6 max-w-6xl">
      {/* Header */}
      <header className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-white">
                {workflow.workflow_type_id.replace(/_/g, " ")}
              </h1>
              <StatusBadge status={workflow.decision_status} />
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-400">
              <span className="flex items-center gap-1">
                <Icon name="users" size={14} />
                Created by {workflow.created_by}
              </span>
              <span>•</span>
              <span>{new Date(workflow.created_at).toLocaleDateString()}</span>
              {workflow.tenant_id && (
                <>
                  <span>•</span>
                  <span className="font-mono text-xs">{workflow.tenant_id}</span>
                </>
              )}
            </div>
          </div>

          {council && (
            <div className="text-right">
              <div className="text-sm text-slate-400 mb-1">Assigned Council</div>
              <Badge variant="blue">
                <Icon name="shield" size={12} className="inline mr-1" />
                {council.name}
              </Badge>
            </div>
          )}
        </div>

        {workflow.resubmission_count > 0 && (
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-violet-500/10 border border-violet-500/30">
            <Icon name="refresh" size={16} className="text-violet-400" />
            <span className="text-sm text-violet-300">
              Resubmitted {workflow.resubmission_count} time{workflow.resubmission_count !== 1 ? "s" : ""}
            </span>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Summary + Artifacts + Timeline */}
        <div className="lg:col-span-2 space-y-6">
          {/* Summary Panel */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Icon name="info" className="text-sovereign-blue" />
                <h2 className="text-lg font-semibold text-white">Summary</h2>
              </div>
            </CardHeader>
            <CardBody>
              <p className="text-slate-300 whitespace-pre-wrap">
                {workflow.summary || "No summary provided"}
              </p>

              {workflow.calculated_savings && (
                <div className="mt-4 pt-4 border-t border-sovereign-slate">
                  <h3 className="text-sm font-semibold text-slate-400 uppercase mb-2">
                    Estimated Savings
                  </h3>
                  <div className="grid grid-cols-3 gap-4">
                    {workflow.calculated_savings.weekly && (
                      <div>
                        <div className="text-xs text-slate-500">Weekly</div>
                        <div className="text-lg font-bold text-sovereign-gold">
                          {formatCurrency(workflow.calculated_savings.weekly)}
                        </div>
                      </div>
                    )}
                    {workflow.calculated_savings.monthly && (
                      <div>
                        <div className="text-xs text-slate-500">Monthly</div>
                        <div className="text-lg font-bold text-sovereign-gold">
                          {formatCurrency(workflow.calculated_savings.monthly)}
                        </div>
                      </div>
                    )}
                    {workflow.calculated_savings.yearly && (
                      <div>
                        <div className="text-xs text-slate-500">Yearly</div>
                        <div className="text-lg font-bold text-sovereign-gold">
                          {formatCurrency(workflow.calculated_savings.yearly)}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </CardBody>
          </Card>

          {/* Artifacts Panel */}
          {artifacts.length > 0 && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Icon name="file" className="text-sovereign-emerald" />
                  <h2 className="text-lg font-semibold text-white">Artifacts</h2>
                </div>
              </CardHeader>
              <CardBody>
                <WorkflowArtifacts
                  artifacts={artifacts}
                  workflowType={workflow.workflow_type_id}
                  outputs={workflow.outputs}
                />
              </CardBody>
            </Card>
          )}

          {/* Timeline */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Icon name="clock" className="text-slate-400" />
                <h2 className="text-lg font-semibold text-white">Timeline</h2>
              </div>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {timeline.length === 0 ? (
                  <p className="text-sm text-slate-500">No timeline events yet</p>
                ) : (
                  timeline.map((event) => (
                    <div key={event.id} className="flex gap-3">
                      <div className="w-2 h-2 rounded-full bg-sovereign-blue mt-2 flex-shrink-0"></div>
                      <div className="flex-1">
                        <div className="text-sm font-semibold text-white">
                          {event.title}
                        </div>
                        {event.description && (
                          <div className="text-xs text-slate-400 mt-1">
                            {event.description}
                          </div>
                        )}
                        <div className="text-xs text-slate-500 mt-1">
                          {new Date(event.created_at).toLocaleString()}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardBody>
          </Card>
        </div>

        {/* Right Column: Decision Panel + Comments */}
        <div className="space-y-6">
          {/* Decision Panel */}
          {isPending && (
            <Card className="border-2 border-sovereign-gold">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Icon name="checkCircle" className="text-sovereign-gold" />
                  <h2 className="text-lg font-semibold text-white">Make Decision</h2>
                </div>
              </CardHeader>
              <CardBody className="space-y-4">
                {/* Comment Box */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-2">
                    Comment
                  </label>
                  <textarea
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    className="w-full px-3 py-2 bg-sovereign-obsidian border border-sovereign-slate rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-sovereign-gold resize-none"
                    rows={4}
                    placeholder="Add your review comment here..."
                  />
                </div>

                {/* Suggested Edits (optional) */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-2">
                    Suggested Edits (Optional)
                  </label>
                  <textarea
                    value={suggestedEdits}
                    onChange={(e) => setSuggestedEdits(e.target.value)}
                    className="w-full px-3 py-2 bg-sovereign-obsidian border border-sovereign-slate rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-sovereign-gold resize-none"
                    rows={3}
                    placeholder="Specific suggestions for improvement..."
                  />
                </div>

                {/* Action Buttons */}
                <div className="space-y-3 pt-2">
                  <button
                    onClick={handleApprove}
                    disabled={actionLoading}
                    className="w-full px-4 py-3 bg-sovereign-emerald hover:bg-emerald-600 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <Icon name="checkCircle" size={18} />
                    {actionLoading ? "Processing..." : "✅ Approve"}
                  </button>

                  <button
                    onClick={handleRequestChanges}
                    disabled={actionLoading}
                    className="w-full px-4 py-3 bg-crimson-500 hover:bg-crimson-600 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <Icon name="xCircle" size={18} />
                    {actionLoading ? "Processing..." : "❌ Request Changes"}
                  </button>
                </div>
              </CardBody>
            </Card>
          )}

          {/* Decision Result (if already decided) */}
          {!isPending && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Icon
                    name={isApproved ? "checkCircle" : "xCircle"}
                    className={isApproved ? "text-sovereign-emerald" : "text-crimson-500"}
                  />
                  <h2 className="text-lg font-semibold text-white">Decision</h2>
                </div>
              </CardHeader>
              <CardBody>
                <div className="space-y-3">
                  <StatusBadge status={workflow.decision_status} />
                  {reviewer && (
                    <div className="text-sm text-slate-400">
                      <div className="flex items-center gap-2 mb-1">
                        <Avatar domain="default" icon="users" size="sm" />
                        <span>{reviewer.name}</span>
                      </div>
                      <div className="text-xs">
                        {new Date(reviewer.reviewed_at).toLocaleString()}
                      </div>
                    </div>
                  )}
                  {workflow.review_comment && (
                    <div className="mt-3 pt-3 border-t border-sovereign-slate">
                      <div className="text-sm text-slate-300 whitespace-pre-wrap">
                        {workflow.review_comment}
                      </div>
                    </div>
                  )}
                </div>
              </CardBody>
            </Card>
          )}

          {/* Council Info */}
          {council && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Icon name="shield" className="text-sovereign-blue" />
                  <h2 className="text-lg font-semibold text-white">
                    {council.name}
                  </h2>
                </div>
              </CardHeader>
              <CardBody className="space-y-3">
                <p className="text-sm text-slate-400">{council.description}</p>
                <div className="pt-2 border-t border-sovereign-slate">
                  <div className="text-xs text-slate-500 uppercase mb-2">
                    Council Members
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {council.members.map((member) => (
                      <Badge key={member.id} variant="blue">
                        {member.name}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardBody>
            </Card>
          )}

          {/* Comments */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Icon name="comment" className="text-sovereign-violet" />
                <h2 className="text-lg font-semibold text-white">Comments</h2>
              </div>
            </CardHeader>
            <CardBody>
              <WorkflowCommentThread
                workflowId={workflow.id}
                comments={comments}
                onRefresh={fetchReviewData}
              />
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  );
}
