"use client";

import { useEffect, useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  Badge,
  Icon,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableCell,
  TableHead,
} from "@/components/ui";
import { styles } from "@/lib/design-system";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Mock tenant/user IDs - replace with actual auth context
const TENANT_ID = "tenant_default";
const USER_ID = "user_default";

interface Notification {
  id: string;
  type: string;
  subject: string;
  body: string;
  step_name?: string;
  is_read: boolean;
  created_at: string;
  workflow: {
    id: string;
    workflow_type_id: string;
    status: string;
  };
}

type FilterType = "all" | "workflows" | "reviews" | "completed" | "errors";

const FILTER_LABELS: Record<FilterType, string> = {
  all: "All",
  workflows: "Workflows",
  reviews: "Reviews Needed",
  completed: "Completed",
  errors: "Errors",
};

const NOTIFICATION_TYPE_MAP: Record<string, FilterType> = {
  workflow_started: "workflows",
  step_completed: "workflows",
  workflow_completed: "completed",
  needs_review: "reviews",
  workflow_failed: "errors",
};

const ICON_MAP: Record<string, string> = {
  workflow_started: "play",
  step_completed: "checkCircle",
  workflow_completed: "checkCircle",
  needs_review: "alertCircle",
  workflow_failed: "xCircle",
};

const COLOR_MAP: Record<string, string> = {
  workflow_started: "text-sovereign-blue",
  step_completed: "text-sovereign-emerald",
  workflow_completed: "text-sovereign-gold",
  needs_review: "text-sovereign-violet",
  workflow_failed: "text-red-500",
};

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filter, setFilter] = useState<FilterType>("all");
  const [loading, setLoading] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    fetchNotifications();
    fetchUnreadCount();
  }, [filter]);

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        tenant_id: TENANT_ID,
        user_id: USER_ID,
        limit: "50",
      });

      // Add filter-specific params
      if (filter !== "all") {
        if (filter === "reviews") {
          params.append("type", "needs_review");
        } else if (filter === "completed") {
          params.append("type", "workflow_completed");
        } else if (filter === "errors") {
          params.append("type", "workflow_failed");
        } else if (filter === "workflows") {
          // Show workflow_started and step_completed
          params.append("type", "workflow_started");
        }
      }

      const res = await fetch(`${API_BASE}/api/notifications?${params}`, {
        cache: "no-store",
      });

      if (!res.ok) {
        throw new Error("Failed to fetch notifications");
      }

      const data = await res.json();
      setNotifications(data.notifications || []);
    } catch (error) {
      console.error("Error fetching notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnreadCount = async () => {
    try {
      const params = new URLSearchParams({
        tenant_id: TENANT_ID,
        user_id: USER_ID,
      });

      const res = await fetch(`${API_BASE}/api/notifications/unread-count?${params}`);
      if (res.ok) {
        const data = await res.json();
        setUnreadCount(data.unread_count || 0);
      }
    } catch (error) {
      console.error("Error fetching unread count:", error);
    }
  };

  const markAsRead = async (notificationId: string) => {
    try {
      const res = await fetch(
        `${API_BASE}/api/notifications/${notificationId}/mark-read`,
        {
          method: "POST",
        }
      );

      if (res.ok) {
        // Update local state
        setNotifications((prev) =>
          prev.map((n) =>
            n.id === notificationId ? { ...n, is_read: true } : n
          )
        );
        setUnreadCount((prev) => Math.max(0, prev - 1));
      }
    } catch (error) {
      console.error("Error marking notification as read:", error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/notifications/mark-all-read`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tenant_id: TENANT_ID,
          user_id: USER_ID,
        }),
      });

      if (res.ok) {
        // Refresh notifications
        fetchNotifications();
        setUnreadCount(0);
      }
    } catch (error) {
      console.error("Error marking all as read:", error);
    }
  };

  const filteredNotifications =
    filter === "all"
      ? notifications
      : notifications.filter(
          (n) => NOTIFICATION_TYPE_MAP[n.type] === filter
        );

  const formatTimestamp = (ts: string) => {
    const date = new Date(ts);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Notifications</h1>
          {unreadCount > 0 && (
            <p className="text-sm text-slate-400 mt-1">
              {unreadCount} unread notification{unreadCount !== 1 ? "s" : ""}
            </p>
          )}
        </div>
        {unreadCount > 0 && (
          <button
            onClick={markAllAsRead}
            className="px-4 py-2 rounded-lg bg-sovereign-slate border border-sovereign-blue text-sovereign-blue hover:bg-sovereign-blue hover:text-white transition-colors text-sm font-medium"
          >
            Mark all as read
          </button>
        )}
      </div>

      {/* Filters */}
      <Card>
        <CardBody>
          <div className="flex flex-wrap gap-2">
            {(Object.keys(FILTER_LABELS) as FilterType[]).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  filter === f
                    ? "bg-sovereign-blue text-white"
                    : "bg-sovereign-slate border border-sovereign-slate text-slate-300 hover:border-sovereign-blue"
                }`}
              >
                {FILTER_LABELS[f]}
              </button>
            ))}
          </div>
        </CardBody>
      </Card>

      {/* Notifications List */}
      <Card>
        <CardBody>
          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-sovereign-gold"></div>
              <p className="text-slate-400 mt-4">Loading notifications...</p>
            </div>
          ) : filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <Icon
                name="checkCircle"
                size={48}
                className="text-slate-600 mx-auto mb-3 opacity-50"
              />
              <p className="text-slate-400">No notifications to display.</p>
            </div>
          ) : (
            <div className="space-y-0 divide-y divide-sovereign-slate">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`px-4 py-4 hover:bg-sovereign-slate/30 transition-colors cursor-pointer ${
                    !notification.is_read ? "bg-sovereign-slate/10" : ""
                  }`}
                  onClick={() => {
                    if (!notification.is_read) {
                      markAsRead(notification.id);
                    }
                  }}
                >
                  <div className="flex items-start gap-4">
                    {/* Icon */}
                    <div
                      className={`mt-1 ${
                        COLOR_MAP[notification.type] || "text-slate-400"
                      }`}
                    >
                      <Icon
                        name={
                          (ICON_MAP[notification.type] as any) || "info"
                        }
                        size={24}
                      />
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <h3
                            className={`text-sm font-semibold ${
                              !notification.is_read
                                ? "text-white"
                                : "text-slate-300"
                            }`}
                          >
                            {notification.subject}
                          </h3>
                          <p className="text-sm text-slate-400 mt-1 whitespace-pre-wrap">
                            {notification.body.split("\n\n")[0]}
                          </p>
                        </div>
                        <div className="flex items-center gap-2">
                          {!notification.is_read && (
                            <div className="w-2 h-2 rounded-full bg-sovereign-blue"></div>
                          )}
                          <span className="text-xs text-slate-500 whitespace-nowrap">
                            {formatTimestamp(notification.created_at)}
                          </span>
                        </div>
                      </div>

                      {/* Action */}
                      <a
                        href={`/portal/workflows/${notification.workflow.id}`}
                        className="inline-flex items-center gap-1 text-xs text-sovereign-blue hover:text-sovereign-gold mt-2 transition-colors"
                        onClick={(e) => e.stopPropagation()}
                      >
                        View workflow
                        <Icon name="arrowRight" size={12} />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
