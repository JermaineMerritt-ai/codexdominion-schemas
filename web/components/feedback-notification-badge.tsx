'use client';

import { useState, useEffect } from 'react';
import { getCouncilFeedbackManager } from '@/lib/feedback/council-feedback';
import Link from 'next/link';

export function FeedbackNotificationBadge() {
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const manager = getCouncilFeedbackManager();

    const updateCount = () => {
      const history = manager.getFeedbackHistory();
      const pending = history.filter((f) => f.status === 'pending').length;
      setPendingCount(pending);
    };

    updateCount();

    // Subscribe to new feedback
    manager.onFeedback(() => {
      updateCount();
    });

    // Check every 30 seconds for updates
    const interval = setInterval(updateCount, 30000);

    return () => clearInterval(interval);
  }, []);

  if (pendingCount === 0) {
    return null;
  }

  return (
    <Link
      href="/feedback"
      className="fixed bottom-6 right-6 bg-[#FFD700] text-[#0A0F29] rounded-full shadow-2xl hover:bg-[#FFC700] transition-all transform hover:scale-110 z-50"
    >
      <div className="relative p-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">📝</span>
          <div className="flex flex-col">
            <span className="text-xs font-bold">Council Feedback</span>
            <span className="text-xs opacity-80">{pendingCount} pending</span>
          </div>
        </div>

        {/* Pulse animation */}
        <span className="absolute top-0 right-0 flex h-4 w-4">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-4 w-4 bg-red-500 items-center justify-center text-white text-xs font-bold">
            {pendingCount}
          </span>
        </span>
      </div>
    </Link>
  );
}
