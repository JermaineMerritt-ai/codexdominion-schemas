"use client";

import { useState } from "react";
import { Icon, Badge, Avatar } from "@/components/ui";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

interface Comment {
  id: string;
  workflow_id: string;
  user_id: string;
  parent_id: string | null;
  comment_type: "reviewer" | "customer" | "system";
  content: string;
  is_resolved: boolean;
  resolved_by_user_id: string | null;
  resolved_at: string | null;
  created_at: string;
  updated_at: string;
  user: {
    id: string;
    name: string;
    email: string;
    role: string;
  };
  reply_count: number;
}

interface WorkflowCommentThreadProps {
  workflowId: string;
  comments: Comment[];
  onRefresh: () => void;
}

export default function WorkflowCommentThread({
  workflowId,
  comments,
  onRefresh,
}: WorkflowCommentThreadProps) {
  const [newComment, setNewComment] = useState("");
  const [filter, setFilter] = useState<"all" | "reviewer" | "customer" | "system">("all");
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [replyContent, setReplyContent] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAddComment() {
    if (!newComment.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/workflows/${workflowId}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_current", // TODO: Get from auth context
          content: newComment,
          comment_type: "customer", // TODO: Detect based on user role
        }),
      });

      if (!res.ok) throw new Error("Failed to add comment");

      setNewComment("");
      onRefresh();
    } catch (err) {
      console.error("Error adding comment:", err);
      alert("Failed to add comment");
    } finally {
      setLoading(false);
    }
  }

  async function handleAddReply(parentId: string) {
    if (!replyContent.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/workflows/${workflowId}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_current", // TODO: Get from auth context
          content: replyContent,
          parent_id: parentId,
          comment_type: "customer",
        }),
      });

      if (!res.ok) throw new Error("Failed to add reply");

      setReplyContent("");
      setReplyingTo(null);
      onRefresh();
    } catch (err) {
      console.error("Error adding reply:", err);
      alert("Failed to add reply");
    } finally {
      setLoading(false);
    }
  }

  async function handleResolve(commentId: string) {
    if (!confirm("Mark this comment thread as resolved?")) return;

    setLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/api/workflows/${workflowId}/comments/${commentId}/resolve`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "user_current", // TODO: Get from auth context
          }),
        }
      );

      if (!res.ok) throw new Error("Failed to resolve comment");

      onRefresh();
    } catch (err) {
      console.error("Error resolving comment:", err);
      alert("Failed to resolve comment");
    } finally {
      setLoading(false);
    }
  }

  const filteredComments =
    filter === "all"
      ? comments
      : comments.filter((c) => c.comment_type === filter);

  const commentTypeColors = {
    reviewer: "text-sovereign-blue",
    customer: "text-sovereign-emerald",
    system: "text-slate-400",
  };

  const commentTypeIcons = {
    reviewer: "shield",
    customer: "users",
    system: "info",
  };

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex items-center gap-2 flex-wrap">
        {["all", "reviewer", "customer", "system"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f as typeof filter)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? "bg-sovereign-gold text-sovereign-obsidian"
                : "bg-sovereign-slate text-slate-400 hover:text-white"
            }`}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Add Comment */}
      <div className="space-y-2">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment... (Markdown supported)"
          className="w-full px-3 py-2 bg-sovereign-obsidian border border-sovereign-slate rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-sovereign-gold resize-none"
          rows={3}
        />
        <button
          onClick={handleAddComment}
          disabled={loading || !newComment.trim()}
          className="px-4 py-2 bg-sovereign-gold hover:bg-gold-600 text-sovereign-obsidian font-semibold rounded-lg text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Posting..." : "Add Comment"}
        </button>
      </div>

      {/* Comments List */}
      <div className="space-y-4">
        {filteredComments.length === 0 ? (
          <div className="text-center py-8">
            <Icon name="comment" size={36} className="text-slate-600 mx-auto mb-2 opacity-50" />
            <p className="text-sm text-slate-500">No comments yet</p>
          </div>
        ) : (
          filteredComments.map((comment) => (
            <div
              key={comment.id}
              className={`p-4 rounded-lg border ${
                comment.is_resolved
                  ? "bg-sovereign-slate/50 border-sovereign-slate opacity-60"
                  : "bg-sovereign-slate border-sovereign-slate"
              }`}
            >
              {/* Comment Header */}
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Avatar domain="default" icon={commentTypeIcons[comment.comment_type] as any} size="sm" />
                  <div>
                    <div className="text-sm font-semibold text-white">
                      {comment.user.name}
                    </div>
                    <div className="text-xs text-slate-500">
                      {new Date(comment.created_at).toLocaleString()}
                    </div>
                  </div>
                  <Badge
                    variant={
                      comment.comment_type === "reviewer"
                        ? "blue"
                        : comment.comment_type === "customer"
                        ? "emerald"
                        : "default"
                    }
                  >
                    {comment.comment_type}
                  </Badge>
                </div>

                {comment.is_resolved && (
                  <Badge variant="emerald">
                    <Icon name="checkCircle" size={10} className="inline mr-1" />
                    Resolved
                  </Badge>
                )}
              </div>

              {/* Comment Content (supports markdown) */}
              <div
                className="text-sm text-slate-300 whitespace-pre-wrap prose prose-invert prose-sm max-w-none"
                dangerouslySetInnerHTML={{
                  __html: renderMarkdown(comment.content),
                }}
              />

              {/* Comment Actions */}
              {!comment.is_resolved && (
                <div className="flex items-center gap-3 mt-3 pt-3 border-t border-sovereign-slate">
                  <button
                    onClick={() => setReplyingTo(comment.id)}
                    className="text-xs text-slate-400 hover:text-sovereign-gold transition-colors"
                  >
                    Reply
                  </button>
                  <button
                    onClick={() => handleResolve(comment.id)}
                    disabled={loading}
                    className="text-xs text-slate-400 hover:text-sovereign-emerald transition-colors disabled:opacity-50"
                  >
                    Resolve
                  </button>
                  {comment.reply_count > 0 && (
                    <span className="text-xs text-slate-500">
                      {comment.reply_count} {comment.reply_count === 1 ? "reply" : "replies"}
                    </span>
                  )}
                </div>
              )}

              {/* Reply Box */}
              {replyingTo === comment.id && (
                <div className="mt-3 pl-4 border-l-2 border-sovereign-gold space-y-2">
                  <textarea
                    value={replyContent}
                    onChange={(e) => setReplyContent(e.target.value)}
                    placeholder="Write a reply..."
                    className="w-full px-3 py-2 bg-sovereign-obsidian border border-sovereign-slate rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-sovereign-gold resize-none"
                    rows={2}
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleAddReply(comment.id)}
                      disabled={loading || !replyContent.trim()}
                      className="px-3 py-1 bg-sovereign-gold hover:bg-gold-600 text-sovereign-obsidian font-semibold rounded text-xs transition-colors disabled:opacity-50"
                    >
                      Reply
                    </button>
                    <button
                      onClick={() => {
                        setReplyingTo(null);
                        setReplyContent("");
                      }}
                      className="px-3 py-1 bg-sovereign-slate hover:bg-slate-700 text-white rounded text-xs transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

/**
 * Simple markdown renderer
 * Supports: **bold**, *italic*, `code`, [links](url)
 */
function renderMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") // Bold
    .replace(/\*(.*?)\*/g, "<em>$1</em>") // Italic
    .replace(/`(.*?)`/g, "<code>$1</code>") // Code
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener" class="text-sovereign-gold hover:underline">$1</a>') // Links
    .replace(/\n/g, "<br>"); // Line breaks
}
