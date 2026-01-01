"use client";

import { useEffect, useState } from "react";
import { Icon } from "@/components/ui";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";

// Mock tenant/user IDs - replace with actual auth context
const TENANT_ID = "tenant_default";
const USER_ID = "user_default";

interface Notification {
  id: string;
  type: string;
  subject: string;
  body: string;
  is_read: boolean;
  created_at: string;
  workflow: {
    id: string;
  };
}

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

export function NotificationDropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUnreadCount();
    
    // Poll for unread count every 30 seconds
    const interval = setInterval(fetchUnreadCount, 30000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isOpen) {
      fetchNotifications();
    }
  }, [isOpen]);

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

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        tenant_id: TENANT_ID,
        user_id: USER_ID,
        limit: "5",
      });

      const res = await fetch(`${API_BASE}/api/notifications?${params}`, {
        cache: "no-store",
      });

      if (res.ok) {
        const data = await res.json();
        setNotifications(data.notifications || []);
      }
    } catch (error) {
      console.error("Error fetching notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (ts: string) => {
    const date = new Date(ts);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="relative">
      {/* Notification Bell Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-lg hover:bg-sovereign-slate transition-colors"
      >
        <Icon name="bell" size={20} className="text-slate-300" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-sovereign-blue text-white text-xs font-bold flex items-center justify-center">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          ></div>

          {/* Dropdown Content */}
          <div className="absolute right-0 mt-2 w-96 rounded-lg border border-sovereign-slate bg-sovereign-obsidian shadow-xl z-50">
            {/* Header */}
            <div className="px-4 py-3 border-b border-sovereign-slate flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white">Notifications</h3>
              <Link
                href="/portal/notifications"
                className="text-xs text-sovereign-blue hover:text-sovereign-gold transition-colors"
                onClick={() => setIsOpen(false)}
              >
                View all
              </Link>
            </div>

            {/* Content */}
            <div className="max-h-96 overflow-y-auto">
              {loading ? (
                <div className="px-4 py-8 text-center">
                  <div className="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-sovereign-gold"></div>
                </div>
              ) : notifications.length === 0 ? (
                <div className="px-4 py-8 text-center">
                  <Icon
                    name="checkCircle"
                    size={32}
                    className="text-slate-600 mx-auto mb-2 opacity-50"
                  />
                  <p className="text-sm text-slate-400">No notifications</p>
                </div>
              ) : (
                <div className="divide-y divide-sovereign-slate">
                  {notifications.map((notification) => (
                    <Link
                      key={notification.id}
                      href={`/portal/workflows/${notification.workflow.id}`}
                      className={`block px-4 py-3 hover:bg-sovereign-slate/30 transition-colors ${
                        !notification.is_read ? "bg-sovereign-slate/10" : ""
                      }`}
                      onClick={() => setIsOpen(false)}
                    >
                      <div className="flex items-start gap-3">
                        {/* Icon */}
                        <div
                          className={`mt-0.5 ${
                            COLOR_MAP[notification.type] || "text-slate-400"
                          }`}
                        >
                          <Icon
                            name={(ICON_MAP[notification.type] as any) || "info"}
                            size={16}
                          />
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between gap-2">
                            <h4
                              className={`text-xs font-semibold ${
                                !notification.is_read
                                  ? "text-white"
                                  : "text-slate-300"
                              }`}
                            >
                              {notification.subject}
                            </h4>
                            {!notification.is_read && (
                              <div className="w-2 h-2 rounded-full bg-sovereign-blue mt-1"></div>
                            )}
                          </div>
                          <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                            {notification.body.split("\n\n")[0]}
                          </p>
                          <span className="text-xs text-slate-500 mt-1 block">
                            {formatTimestamp(notification.created_at)}
                          </span>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            {notifications.length > 0 && (
              <div className="px-4 py-2 border-t border-sovereign-slate">
                <Link
                  href="/portal/notifications"
                  className="block text-center text-xs text-sovereign-blue hover:text-sovereign-gold transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  View all notifications →
                </Link>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
