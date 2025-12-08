'use client';

import { useEffect, useState } from 'react';
import { UnifiedEvent, getUnifiedEventManager } from '@/lib/events/unified-event-manager';
import { useSeedUnifiedEvents } from '@/hooks/useSeedUnifiedEvents';

interface Filters {
  type: 'all' | 'annotation' | 'chat' | 'feedback' | 'capsule';
  engine: string;
  role: string;
  cycle: string;
}

export default function AnnotationArchive() {
  useSeedUnifiedEvents();

  const [annotations, setAnnotations] = useState<UnifiedEvent[]>([]);
  const [filters, setFilters] = useState<Filters>({
    type: 'all',
    engine: '',
    role: '',
    cycle: '',
  });
  const [searchQuery, setSearchQuery] = useState('');

  // All 18 engines
  const engines = [
    'Commerce Engine',
    'Profit Engine',
    'RAG Intelligence Engine',
    'Axiom Intelligence Engine',
    'Marketing Engine',
    'Distribution Engine',
    'Video Studio',
    'Avatar System',
    'Content Studio',
    'Analytics Engine',
    'Automation Engine',
    'Email Engine',
    'Social Media Engine',
    'SEO Engine',
    'Customer Support Engine',
    'Billing Engine',
    'Inventory Engine',
    'Reporting Engine',
  ];

  useEffect(() => {
    loadAnnotations();

    // Refresh every 10 seconds
    const interval = setInterval(loadAnnotations, 10000);
    return () => clearInterval(interval);
  }, [filters, searchQuery]);

  const loadAnnotations = () => {
    const manager = getUnifiedEventManager();
    let results: UnifiedEvent[];

    // Start with search or all events
    if (searchQuery.trim()) {
      results = manager.searchEvents(searchQuery);
    } else if (filters.type === 'all') {
      results = manager.getAllEvents();
    } else {
      results = manager.getEventsByType(filters.type);
    }

    // Apply engine filter
    if (filters.engine) {
      results = results.filter((a) => a.engine === filters.engine);
    }

    // Apply role filter
    if (filters.role) {
      results = results.filter((a) => a.role === filters.role);
    }

    // Apply cycle filter (time-based)
    if (filters.cycle) {
      const now = new Date().getTime();
      results = results.filter((a) => {
        const eventTime = new Date(a.timestamp).getTime();
        const hoursDiff = (now - eventTime) / (1000 * 60 * 60);

        switch (filters.cycle) {
          case 'daily':
            return hoursDiff <= 24;
          case 'seasonal':
            return hoursDiff <= 24 * 7; // 7 days
          case 'epochal':
            return hoursDiff <= 24 * 30; // 30 days
          case 'millennial':
            return hoursDiff <= 24 * 90; // 90 days
          default:
            return true;
        }
      });
    }

    setAnnotations(results);
  };

  const getEventIcon = (type: string) => {
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
        return '🕰️';
    }
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'annotation':
        return 'text-blue-400';
      case 'chat':
        return 'text-purple-400';
      case 'feedback':
        return 'text-orange-400';
      case 'capsule':
        return 'text-green-400';
      default:
        return 'text-gray-400';
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

  return (
    <div className="bg-[#1A1F3C] p-6 rounded-lg border-2 border-[#FFD700]">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-[#FFD700]">📚 Annotation Archive</h2>
        <span className="text-sm text-gray-400">{annotations.length} events</span>
      </div>

      {/* Search Bar */}
      <div className="mb-4">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search annotations, chat, feedback..."
          className="w-full px-4 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
        />
      </div>

      {/* Filter Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
        {/* Type Filter */}
        <div>
          <label className="block text-xs text-gray-400 mb-1">Event Type</label>
          <select
            value={filters.type}
            onChange={(e) => setFilters((f) => ({ ...f, type: e.target.value as Filters['type'] }))}
            className="w-full px-3 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
          >
            <option value="all">All Types</option>
            <option value="annotation">📋 Annotation</option>
            <option value="chat">💬 Chat</option>
            <option value="feedback">📝 Feedback</option>
            <option value="capsule">⚙️ Capsule</option>
          </select>
        </div>

        {/* Engine Filter */}
        <div>
          <label className="block text-xs text-gray-400 mb-1">Engine</label>
          <select
            value={filters.engine}
            onChange={(e) => setFilters((f) => ({ ...f, engine: e.target.value }))}
            className="w-full px-3 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
          >
            <option value="">All Engines</option>
            {engines.map((engine) => (
              <option key={engine} value={engine}>
                {engine}
              </option>
            ))}
          </select>
        </div>

        {/* Role Filter */}
        <div>
          <label className="block text-xs text-gray-400 mb-1">Role</label>
          <select
            value={filters.role}
            onChange={(e) => setFilters((f) => ({ ...f, role: e.target.value }))}
            className="w-full px-3 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
          >
            <option value="">All Roles</option>
            <option value="sovereign">👑 Sovereign</option>
            <option value="custodian">🔑 Custodian</option>
            <option value="council">🎓 Council</option>
            <option value="heir">🌟 Heir</option>
            <option value="observer">👁️ Observer</option>
          </select>
        </div>

        {/* Cycle Filter */}
        <div>
          <label className="block text-xs text-gray-400 mb-1">Time Cycle</label>
          <select
            value={filters.cycle}
            onChange={(e) => setFilters((f) => ({ ...f, cycle: e.target.value }))}
            className="w-full px-3 py-2 bg-[#0A0F29] text-white border border-[#FFD700]/30 rounded focus:border-[#FFD700] focus:outline-none"
          >
            <option value="">All Time</option>
            <option value="daily">📅 Daily (24h)</option>
            <option value="seasonal">🌙 Seasonal (7d)</option>
            <option value="epochal">⏳ Epochal (30d)</option>
            <option value="millennial">🌌 Millennial (90d)</option>
          </select>
        </div>
      </div>

      {/* Active Filters Display */}
      {(filters.type !== 'all' || filters.engine || filters.role || filters.cycle || searchQuery) && (
        <div className="mb-4 flex flex-wrap gap-2">
          <span className="text-xs text-gray-400">Active filters:</span>
          {filters.type !== 'all' && (
            <span className="px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded text-xs">
              Type: {filters.type}
            </span>
          )}
          {filters.engine && (
            <span className="px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded text-xs">
              Engine: {filters.engine}
            </span>
          )}
          {filters.role && (
            <span className="px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded text-xs">
              Role: {filters.role}
            </span>
          )}
          {filters.cycle && (
            <span className="px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded text-xs">
              Cycle: {filters.cycle}
            </span>
          )}
          {searchQuery && (
            <span className="px-2 py-1 bg-[#FFD700]/20 text-[#FFD700] rounded text-xs">
              Search: "{searchQuery}"
            </span>
          )}
          <button
            onClick={() => {
              setFilters({ type: 'all', engine: '', role: '', cycle: '' });
              setSearchQuery('');
            }}
            className="px-2 py-1 bg-red-900/30 text-red-400 rounded text-xs hover:bg-red-900/50 transition-colors"
          >
            Clear All
          </button>
        </div>
      )}

      {/* Annotations List */}
      <ul className="space-y-3 max-h-[500px] overflow-y-auto custom-scrollbar pr-2">
        {annotations.length === 0 ? (
          <li className="text-center py-8 text-gray-400">
            <p className="text-2xl mb-2">📚</p>
            <p>No events found</p>
          </li>
        ) : (
          annotations.map((a) => (
            <li
              key={a.id}
              className="bg-[#0A0F29] p-4 rounded-lg border border-[#FFD700]/20 hover:border-[#FFD700]/50 transition-colors"
            >
              <div className="flex items-start gap-3">
                {/* Event Icon */}
                <span className="text-2xl flex-shrink-0">{getEventIcon(a.type)}</span>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  {/* Timestamp and Type */}
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className="text-xs text-gray-500">
                      {new Date(a.timestamp).toLocaleString()}
                    </span>
                    <span className={`text-xs font-bold uppercase ${getEventColor(a.type)}`}>
                      {a.type}
                    </span>
                  </div>

                  {/* User Info */}
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{getRoleIcon(a.role)}</span>
                    <span className="text-[#FFD700] font-bold text-sm">{a.user}</span>
                    <span className="text-xs text-gray-400">({a.role})</span>
                  </div>

                  {/* Engine Badge */}
                  {a.engine && (
                    <div className="mb-2">
                      <span className="px-2 py-1 bg-[#1A1F3C] rounded text-xs text-[#FFD700] border border-[#FFD700]/30">
                        {a.engine}
                      </span>
                    </div>
                  )}

                  {/* Note/Content */}
                  <p className="text-white text-sm leading-relaxed mb-2">
                    <em>{a.content}</em>
                  </p>

                  {/* Tags */}
                  {a.tags && a.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {a.tags.map((tag) => (
                        <span
                          key={tag}
                          className="px-2 py-0.5 bg-[#1A1F3C] rounded text-xs text-gray-300 border border-gray-600"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Capsule Link */}
                  {a.capsuleId && (
                    <div className="mt-2 text-xs text-gray-500">
                      📦 Capsule: <span className="font-mono text-gray-400">{a.capsuleId}</span>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))
        )}
      </ul>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #0A0F29;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #FFD700;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #FFA500;
        }
      `}</style>
    </div>
  );
}
