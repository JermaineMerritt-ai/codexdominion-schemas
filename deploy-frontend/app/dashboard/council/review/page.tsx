"use client";

import { useState, useEffect } from "react";
import { Search, Filter, CheckCircle, XCircle, Clock, TrendingUp } from "lucide-react";

interface WorkflowReview {
  id: string;
  workflow_type: string;
  workflow_name: string;
  agent_id: string;
  agent_name: string;
  domain: string;
  assigned_council_id: string;
  council_name: string;
  estimated_weekly_savings: number;
  created_at: string;
  decision: "pending" | "approved" | "denied";
  votes: Array<{
    id: number; // workflow_votes.id (SERIAL)
    workflow_id: string; // References workflows.id
    member_id: string; // References agents.id
    member_name: string; // From agent JOIN
    vote: string; // TEXT in database (typically "approve" | "deny")
    reason: string; // TEXT
    timestamp: string; // TIMESTAMP
  }>;
  inputs?: Record<string, any>;
  savings_breakdown?: {
    weekly: number;
    monthly: number;
    yearly: number;
    hours_saved: number;
  };
}

export default function CouncilReviewPage() {
  const [reviews, setReviews] = useState<WorkflowReview[]>([]);
  const [filteredReviews, setFilteredReviews] = useState<WorkflowReview[]>([]);
  const [selectedCouncil, setSelectedCouncil] = useState<string>("all");
  const [selectedStatus, setSelectedStatus] = useState<string>("pending");
  const [selectedDomain, setSelectedDomain] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedReview, setSelectedReview] = useState<WorkflowReview | null>(null);
  const [loading, setLoading] = useState(false);

  const councils = [
    "all",
    "governance",
    "treasury",
    "commerce",
    "media",
    "security",
    "operations",
  ];
  const domains = ["all", "finance", "operations", "marketing", "security", "governance"];

  useEffect(() => {
    fetchReviews();
  }, []);

  useEffect(() => {
    filterReviews();
  }, [reviews, selectedCouncil, selectedStatus, selectedDomain, searchTerm]);

  async function fetchReviews() {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/workflows/pending-review");
      if (res.ok) {
        const data = await res.json();
        setReviews(data.reviews || []);
      }
    } catch (err) {
      console.error("Failed to fetch reviews:", err);
    } finally {
      setLoading(false);
    }
  }

  function filterReviews() {
    let filtered = reviews;

    if (selectedCouncil !== "all") {
      filtered = filtered.filter((r) => r.assigned_council_id === selectedCouncil);
    }

    if (selectedStatus !== "all") {
      filtered = filtered.filter((r) => r.decision === selectedStatus);
    }

    if (selectedDomain !== "all") {
      filtered = filtered.filter((r) => r.domain === selectedDomain);
    }

    if (searchTerm) {
      filtered = filtered.filter(
        (r) =>
          r.workflow_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          r.agent_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          r.id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredReviews(filtered);
  }

  async function handleVote(reviewId: string, vote: "approve" | "deny", reason: string) {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/api/workflows/${reviewId}/vote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          member_id: "current_user_id", // Replace with actual user ID
          vote,
          reason,
        }),
      });

      if (res.ok) {
        await fetchReviews();
        setSelectedReview(null);
      }
    } catch (err) {
      console.error("Failed to submit vote:", err);
    } finally {
      setLoading(false);
    }
  }

  function getStatusIcon(decision: string) {
    switch (decision) {
      case "approved":
        return <CheckCircle className="text-green-500" size={18} />;
      case "denied":
        return <XCircle className="text-red-500" size={18} />;
      default:
        return <Clock className="text-yellow-500" size={18} />;
    }
  }

  function getStatusBadge(decision: string) {
    const colors = {
      pending: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
      approved: "bg-green-500/20 text-green-400 border-green-500/30",
      denied: "bg-red-500/20 text-red-400 border-red-500/30",
    };
    return colors[decision as keyof typeof colors] || colors.pending;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Council Review</h1>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <Clock size={16} />
          <span>{filteredReviews.length} workflows pending review</span>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Council</label>
            <select
              value={selectedCouncil}
              onChange={(e) => setSelectedCouncil(e.target.value)}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm"
            >
              {councils.map((council) => (
                <option key={council} value={council}>
                  {council === "all" ? "All Councils" : council.replace("_", " ")}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Status</label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm"
            >
              <option value="all">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="denied">Denied</option>
            </select>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Domain</label>
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm"
            >
              {domains.map((domain) => (
                <option key={domain} value={domain}>
                  {domain === "all" ? "All Domains" : domain}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Search</label>
            <div className="relative">
              <Search
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                size={16}
              />
              <input
                type="text"
                placeholder="Workflow ID, agent..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Review List */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-800/50 border-b border-slate-700">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Workflow ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Type
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Agent
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Council
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Savings
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Status
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-slate-400">
                  Created
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-slate-400">
                    Loading reviews...
                  </td>
                </tr>
              ) : filteredReviews.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-slate-400">
                    No workflows to review
                  </td>
                </tr>
              ) : (
                filteredReviews.map((review) => (
                  <tr
                    key={review.id}
                    onClick={() => setSelectedReview(review)}
                    className="hover:bg-slate-800/50 cursor-pointer transition-colors"
                  >
                    <td className="px-4 py-3 text-sm font-mono text-blue-400">
                      {review.id.substring(0, 8)}
                    </td>
                    <td className="px-4 py-3 text-sm">{review.workflow_name}</td>
                    <td className="px-4 py-3 text-sm">{review.agent_name}</td>
                    <td className="px-4 py-3 text-sm text-slate-400">
                      {review.council_name}
                    </td>
                    <td className="px-4 py-3 text-sm font-semibold text-emerald-400">
                      ${review.estimated_weekly_savings.toLocaleString()}/wk
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs border ${getStatusBadge(
                          review.decision
                        )}`}
                      >
                        {getStatusIcon(review.decision)}
                        {review.decision}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-400">
                      {new Date(review.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detail Drawer */}
      {selectedReview && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Workflow Review Details</h2>
              <button
                onClick={() => setSelectedReview(null)}
                className="text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-6">
              {/* Overview */}
              <div>
                <h3 className="text-sm font-medium text-slate-400 mb-2">Overview</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-400">Workflow ID:</span>
                    <span className="ml-2 font-mono text-blue-400">{selectedReview.id}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Type:</span>
                    <span className="ml-2">{selectedReview.workflow_name}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Agent:</span>
                    <span className="ml-2">{selectedReview.agent_name}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Council:</span>
                    <span className="ml-2">{selectedReview.council_name}</span>
                  </div>
                </div>
              </div>

              {/* Savings Breakdown */}
              {selectedReview.savings_breakdown && (
                <div>
                  <h3 className="text-sm font-medium text-slate-400 mb-2">
                    Savings Breakdown
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="bg-slate-800 rounded p-3">
                      <div className="text-xs text-slate-400">Weekly</div>
                      <div className="text-lg font-semibold text-emerald-400">
                        ${selectedReview.savings_breakdown.weekly.toLocaleString()}
                      </div>
                    </div>
                    <div className="bg-slate-800 rounded p-3">
                      <div className="text-xs text-slate-400">Monthly</div>
                      <div className="text-lg font-semibold text-emerald-400">
                        ${selectedReview.savings_breakdown.monthly.toLocaleString()}
                      </div>
                    </div>
                    <div className="bg-slate-800 rounded p-3">
                      <div className="text-xs text-slate-400">Yearly</div>
                      <div className="text-lg font-semibold text-emerald-400">
                        ${selectedReview.savings_breakdown.yearly.toLocaleString()}
                      </div>
                    </div>
                    <div className="bg-slate-800 rounded p-3">
                      <div className="text-xs text-slate-400">Hours Saved</div>
                      <div className="text-lg font-semibold">
                        {selectedReview.savings_breakdown.hours_saved}h
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Vote History */}
              <div>
                <h3 className="text-sm font-medium text-slate-400 mb-2">Vote History</h3>
                {selectedReview.votes.length === 0 ? (
                  <p className="text-sm text-slate-500">No votes yet</p>
                ) : (
                  <div className="space-y-2">
                    {selectedReview.votes.map((vote, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-800 rounded p-3 flex items-start gap-3"
                      >
                        {vote.vote === "approve" ? (
                          <CheckCircle className="text-green-500 mt-0.5" size={18} />
                        ) : (
                          <XCircle className="text-red-500 mt-0.5" size={18} />
                        )}
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium">{vote.member_name}</span>
                            <span className="text-xs text-slate-400">
                              {new Date(vote.timestamp).toLocaleString()}
                            </span>
                          </div>
                          <p className="text-sm text-slate-400">{vote.reason}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              {selectedReview.decision === "pending" && (
                <div className="flex gap-3 pt-4 border-t border-slate-700">
                  <button
                    onClick={() =>
                      handleVote(
                        selectedReview.id,
                        "approve",
                        "Approved - meets council standards"
                      )
                    }
                    disabled={loading}
                    className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-500 rounded font-medium disabled:opacity-50"
                  >
                    Approve Workflow
                  </button>
                  <button
                    onClick={() =>
                      handleVote(
                        selectedReview.id,
                        "deny",
                        "Denied - requires further review"
                      )
                    }
                    disabled={loading}
                    className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-500 rounded font-medium disabled:opacity-50"
                  >
                    Deny Workflow
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
