'use client';

import { useState } from 'react';
import { CouncilFeedback, getCouncilFeedbackManager } from '@/lib/feedback/council-feedback';
import { useReplay } from '@/context/ReplayContext';

export interface FeedbackPanelProps {
  userName: string;
  onFeedbackSent?: (feedback: CouncilFeedback) => void;
}

export function FeedbackPanel({ userName, onFeedbackSent }: FeedbackPanelProps) {
  const { index, capsules } = useReplay();
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const currentCapsule = capsules.length > 0 ? capsules[index] : null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!message.trim()) return;

    setIsSubmitting(true);

    const feedback: CouncilFeedback = {
      user: userName,
      role: 'council',
      timestamp: new Date().toISOString(),
      message: message.trim(),
      capsuleId: currentCapsule?.id,
      engine: currentCapsule?.engine,
      metadata: {
        capsuleIndex: index,
        capsuleTimestamp: currentCapsule?.timestamp,
        capsuleStatus: currentCapsule?.status,
      },
    };

    try {
      const manager = getCouncilFeedbackManager();
      const enrichedFeedback = manager.submitFeedback(feedback);

      // Send to broadcast system (if connected)
      if (onFeedbackSent) {
        onFeedbackSent(feedback);
      }

      // Show success state
      setShowSuccess(true);
      setMessage('');

      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4">
      <h3 className="text-lg font-bold text-[#FFD700] mb-3 flex items-center gap-2">
        👑 Council Feedback
      </h3>

      {currentCapsule && (
        <div className="bg-[#0A0F29] rounded p-3 mb-4 text-sm">
          <p className="text-gray-400 mb-1">Providing feedback on:</p>
          <p className="text-[#FFD700]">
            <span className="font-bold">{currentCapsule.engine}</span>
            <span className="mx-2">•</span>
            <span>{currentCapsule.status}</span>
          </p>
          <p className="text-gray-500 text-xs mt-1">
            {new Date(currentCapsule.timestamp).toLocaleString()}
          </p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Share your observations about this event or related historical patterns..."
          className="w-full bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded p-3 text-sm min-h-[100px] focus:border-[#FFD700] focus:outline-none resize-none"
          disabled={isSubmitting}
        />

        <div className="flex items-center justify-between mt-3">
          <span className="text-xs text-gray-500">
            {message.length} / 500 characters
          </span>

          <button
            type="submit"
            disabled={isSubmitting || !message.trim()}
            className="px-4 py-2 bg-[#FFD700] text-[#0A0F29] rounded font-bold hover:bg-[#FFC700] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? '📤 Sending...' : '📝 Submit Feedback'}
          </button>
        </div>
      </form>

      {showSuccess && (
        <div className="mt-3 bg-green-900/30 border border-green-500 rounded p-3 text-sm text-green-400">
          ✅ Feedback submitted successfully! Sovereign will review.
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-[#FFD700]/20">
        <p className="text-xs text-gray-500">
          💡 <span className="font-bold">Tip:</span> Reference historical events (like "last quarter")
          to help identify recurring patterns across rituals.
        </p>
      </div>
    </div>
  );
}
