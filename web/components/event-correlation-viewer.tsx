'use client';

import { useState, useEffect } from 'react';
import { UnifiedEvent, EventCorrelation, getUnifiedEventManager } from '@/lib/events/unified-event-manager';

interface EventCorrelationViewerProps {
  capsuleId: string;
  windowMinutes?: number;
}

export function EventCorrelationViewer({ capsuleId, windowMinutes = 10 }: EventCorrelationViewerProps) {
  const [correlation, setCorrelation] = useState<EventCorrelation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCorrelation();
  }, [capsuleId, windowMinutes]);

  const loadCorrelation = () => {
    setLoading(true);
    const manager = getUnifiedEventManager();
    const result = manager.correlateCapsuleEvents(capsuleId, windowMinutes);
    setCorrelation(result);
    setLoading(false);
  };

  const getEventTypeIcon = (type: string) => {
    switch (type) {
      case 'annotation':
        return '📋';
      case 'chat':
        return '💬';
      case 'feedback':
        return '📝';
      case 'capsule':
        return '⚙️';
      default:
        return '📊';
    }
  };

  const getEventTypeColor = (type: string) => {
    switch (type) {
      case 'annotation':
        return 'bg-blue-900/30 border-blue-500';
      case 'chat':
        return 'bg-purple-900/30 border-purple-500';
      case 'feedback':
        return 'bg-orange-900/30 border-orange-500';
      case 'capsule':
        return 'bg-green-900/30 border-green-500';
      default:
        return 'bg-gray-900/30 border-gray-500';
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'sovereign':
        return '👑';
      case 'council':
        return '🎓';
      case 'heir':
        return '🌟';
      case 'custodian':
        return '🔑';
      case 'observer':
        return '👁️';
      default:
        return '💬';
    }
  };

  if (loading) {
    return (
      <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6">
        <p className="text-gray-400 text-center">Loading event correlation...</p>
      </div>
    );
  }

  if (!correlation || correlation.events.length === 0) {
    return (
      <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6">
        <h3 className="text-xl font-bold text-[#FFD700] mb-2">🔗 Event Correlation</h3>
        <p className="text-gray-400 text-center py-4">No correlated events found for this capsule.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-[#FFD700]">🔗 Event Correlation Analysis</h3>
        <span className="text-sm text-gray-400">{correlation.events.length} events</span>
      </div>

      {/* Time Window */}
      <div className="bg-[#0A0F29] rounded p-3 mb-4 border border-[#FFD700]/20">
        <p className="text-xs text-gray-500 mb-1">Time Window:</p>
        <p className="text-sm text-white">{correlation.timeWindow}</p>
      </div>

      {/* Detected Patterns */}
      {correlation.patterns.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-bold text-[#FFD700] mb-2">🔍 Detected Patterns:</h4>
          <div className="space-y-2">
            {correlation.patterns.map((pattern, idx) => (
              <div key={idx} className="bg-[#0A0F29] rounded p-2 border-l-4 border-[#FFD700]">
                <p className="text-sm text-white">{pattern}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Event Timeline */}
      <div>
        <h4 className="text-sm font-bold text-[#FFD700] mb-3">📅 Event Timeline:</h4>
        <div className="space-y-3">
          {correlation.events
            .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
            .map((event) => (
              <div
                key={event.id}
                className={`rounded-lg p-4 border ${getEventTypeColor(event.type)}`}
              >
                {/* Event Header */}
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{getEventTypeIcon(event.type)}</span>
                    <span className="text-xs font-bold text-[#FFD700] uppercase">{event.type}</span>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(event.timestamp).toLocaleTimeString()}
                  </span>
                </div>

                {/* User Info */}
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-lg">{getRoleIcon(event.role)}</span>
                  <span className="font-bold text-white text-sm">{event.user}</span>
                  <span className="text-xs text-gray-400">({event.role})</span>
                </div>

                {/* Engine Badge */}
                {event.engine && (
                  <div className="mb-2">
                    <span className="px-2 py-1 bg-[#0A0F29] rounded text-xs text-[#FFD700] border border-[#FFD700]/30">
                      {event.engine}
                    </span>
                  </div>
                )}

                {/* Content */}
                <p className="text-white text-sm leading-relaxed mb-2">{event.content}</p>

                {/* Tags */}
                {event.tags && event.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {event.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 bg-[#0A0F29] rounded text-xs text-gray-300 border border-gray-600"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}

                {/* Metadata */}
                {event.metadata && Object.keys(event.metadata).length > 0 && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-xs text-gray-400 hover:text-[#FFD700]">
                      View Metadata
                    </summary>
                    <pre className="mt-2 bg-black/30 rounded p-2 text-xs text-gray-400 overflow-x-auto">
                      {JSON.stringify(event.metadata, null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
