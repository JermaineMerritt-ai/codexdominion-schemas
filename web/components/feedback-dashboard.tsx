'use client';

import { useState, useEffect } from 'react';
import { FeedbackMessage, getCouncilFeedbackManager } from '@/lib/feedback/council-feedback';
import { useSeedFeedback } from '@/hooks/useSeedFeedback';

export function FeedbackDashboard() {
  const [feedbackHistory, setFeedbackHistory] = useState<FeedbackMessage[]>([]);
  const [filter, setFilter] = useState<'all' | 'pending' | 'acknowledged' | 'resolved'>('all');
  const [priorityFilter, setPriorityFilter] = useState<'all' | 'critical' | 'high' | 'medium' | 'low'>('all');

  // Seed sample data on first load
  useSeedFeedback();

  useEffect(() => {
    const manager = getCouncilFeedbackManager();
    const history = manager.getFeedbackHistory();
    setFeedbackHistory(history);

    // Subscribe to new feedback
    manager.onFeedback((newFeedback) => {
      setFeedbackHistory((prev) => [newFeedback, ...prev]);
    });
  }, []);

  const filteredFeedback = feedbackHistory.filter((feedback) => {
    if (filter !== 'all' && feedback.status !== filter) return false;
    if (priorityFilter !== 'all' && feedback.priority !== priorityFilter) return false;
    return true;
  });

  const getPriorityColor = (priority: FeedbackMessage['priority']) => {
    switch (priority) {
      case 'critical':
        return 'bg-red-900/30 border-red-500 text-red-400';
      case 'high':
        return 'bg-orange-900/30 border-orange-500 text-orange-400';
      case 'medium':
        return 'bg-yellow-900/30 border-yellow-500 text-yellow-400';
      case 'low':
        return 'bg-blue-900/30 border-blue-500 text-blue-400';
    }
  };

  const getStatusColor = (status: FeedbackMessage['status']) => {
    switch (status) {
      case 'pending':
        return 'bg-gray-700 text-gray-300';
      case 'acknowledged':
        return 'bg-blue-700 text-blue-200';
      case 'resolved':
        return 'bg-green-700 text-green-200';
    }
  };

  const getStatusIcon = (status: FeedbackMessage['status']) => {
    switch (status) {
      case 'pending':
        return '⏳';
      case 'acknowledged':
        return '👁️';
      case 'resolved':
        return '✅';
    }
  };

  const handleStatusChange = (id: string, newStatus: FeedbackMessage['status']) => {
    const manager = getCouncilFeedbackManager();
    const success = manager.updateFeedbackStatus(id, newStatus);

    if (success) {
      setFeedbackHistory((prev) =>
        prev.map((f) => (f.id === id ? { ...f, status: newStatus } : f))
      );
    }
  };

  const stats = {
    total: feedbackHistory.length,
    pending: feedbackHistory.filter((f) => f.status === 'pending').length,
    acknowledged: feedbackHistory.filter((f) => f.status === 'acknowledged').length,
    resolved: feedbackHistory.filter((f) => f.status === 'resolved').length,
    critical: feedbackHistory.filter((f) => f.priority === 'critical').length,
    high: feedbackHistory.filter((f) => f.priority === 'high').length,
  };

  return (
    <div className="bg-[#0A0F29] text-white p-6 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-[#FFD700] mb-2">
          📝 Council Feedback Dashboard
        </h1>
        <p className="text-gray-400">
          Historical observations and insights from the council
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4 mb-8">
        <div className="bg-[#1A1F3C] border border-[#FFD700]/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-[#FFD700]">{stats.total}</p>
          <p className="text-sm text-gray-400">Total</p>
        </div>
        <div className="bg-[#1A1F3C] border border-gray-500/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-gray-300">{stats.pending}</p>
          <p className="text-sm text-gray-400">Pending</p>
        </div>
        <div className="bg-[#1A1F3C] border border-blue-500/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-blue-400">{stats.acknowledged}</p>
          <p className="text-sm text-gray-400">Acknowledged</p>
        </div>
        <div className="bg-[#1A1F3C] border border-green-500/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-green-400">{stats.resolved}</p>
          <p className="text-sm text-gray-400">Resolved</p>
        </div>
        <div className="bg-[#1A1F3C] border border-red-500/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-red-400">{stats.critical}</p>
          <p className="text-sm text-gray-400">Critical</p>
        </div>
        <div className="bg-[#1A1F3C] border border-orange-500/30 rounded-lg p-4 text-center">
          <p className="text-2xl font-bold text-orange-400">{stats.high}</p>
          <p className="text-sm text-gray-400">High</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 mb-6">
        <div>
          <label className="text-sm text-gray-400 mb-2 block">Status:</label>
          <div className="flex gap-2">
            {['all', 'pending', 'acknowledged', 'resolved'].map((status) => (
              <button
                key={status}
                onClick={() => setFilter(status as typeof filter)}
                className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                  filter === status
                    ? 'bg-[#FFD700] text-[#0A0F29]'
                    : 'bg-[#1A1F3C] text-gray-400 hover:bg-[#2A2F4C]'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-sm text-gray-400 mb-2 block">Priority:</label>
          <div className="flex gap-2">
            {['all', 'critical', 'high', 'medium', 'low'].map((priority) => (
              <button
                key={priority}
                onClick={() => setPriorityFilter(priority as typeof priorityFilter)}
                className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                  priorityFilter === priority
                    ? 'bg-[#FFD700] text-[#0A0F29]'
                    : 'bg-[#1A1F3C] text-gray-400 hover:bg-[#2A2F4C]'
                }`}
              >
                {priority.charAt(0).toUpperCase() + priority.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Feedback List */}
      <div className="space-y-4">
        {filteredFeedback.length === 0 ? (
          <div className="bg-[#1A1F3C] border border-[#FFD700]/30 rounded-lg p-12 text-center">
            <p className="text-gray-400 text-lg">No feedback matches the current filters</p>
          </div>
        ) : (
          filteredFeedback.map((feedback) => (
            <div
              key={feedback.id}
              className={`rounded-lg border-2 p-6 ${getPriorityColor(feedback.priority)}`}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-bold text-lg">👑 {feedback.user}</span>
                    <span className={`px-2 py-1 rounded text-xs font-bold ${getStatusColor(feedback.status)}`}>
                      {getStatusIcon(feedback.status)} {feedback.status.toUpperCase()}
                    </span>
                    <span className="px-2 py-1 rounded text-xs font-bold bg-[#0A0F29]">
                      {feedback.priority.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-400">
                    {new Date(feedback.timestamp).toLocaleString()}
                  </p>
                </div>

                {/* Status Actions (for sovereign) */}
                <div className="flex gap-2">
                  {feedback.status === 'pending' && (
                    <button
                      onClick={() => handleStatusChange(feedback.id, 'acknowledged')}
                      className="px-3 py-1 bg-blue-700 hover:bg-blue-600 text-blue-100 rounded text-sm font-medium transition-colors"
                    >
                      👁️ Acknowledge
                    </button>
                  )}
                  {feedback.status === 'acknowledged' && (
                    <button
                      onClick={() => handleStatusChange(feedback.id, 'resolved')}
                      className="px-3 py-1 bg-green-700 hover:bg-green-600 text-green-100 rounded text-sm font-medium transition-colors"
                    >
                      ✅ Resolve
                    </button>
                  )}
                </div>
              </div>

              {/* Message */}
              <div className="bg-[#0A0F29]/50 rounded p-4 mb-4">
                <p className="text-white leading-relaxed">{feedback.message}</p>
              </div>

              {/* Context */}
              {feedback.engine && (
                <div className="bg-[#0A0F29]/50 rounded p-3 mb-3">
                  <p className="text-sm text-gray-400 mb-1">Related to:</p>
                  <p className="text-[#FFD700] font-bold">
                    {feedback.engine}
                    {feedback.metadata?.capsuleStatus && (
                      <span className="ml-2 text-sm">
                        • {feedback.metadata.capsuleStatus}
                      </span>
                    )}
                  </p>
                  {feedback.metadata?.capsuleTimestamp && (
                    <p className="text-xs text-gray-500 mt-1">
                      Capsule: {new Date(feedback.metadata.capsuleTimestamp).toLocaleString()}
                    </p>
                  )}
                </div>
              )}

              {/* Tags */}
              {feedback.tags && feedback.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {feedback.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-[#0A0F29]/70 rounded text-xs text-gray-300 border border-gray-700"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}

              {/* Footer */}
              <div className="mt-4 pt-4 border-t border-current/20 flex items-center justify-between text-xs text-gray-500">
                <span>ID: {feedback.id}</span>
                {feedback.capsuleId && (
                  <span>Capsule: {feedback.capsuleId}</span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
