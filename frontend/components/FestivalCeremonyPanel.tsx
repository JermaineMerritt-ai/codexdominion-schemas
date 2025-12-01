import React, { useState, useEffect } from 'react';

interface CeremonialCycle {
  cycle_id: string;
  timestamp: string;
  ceremony_type: string;
  kind: 'proclamation' | 'silence' | 'blessing';
  message: string;
  proclamation?: string;
  rite: string;
  flame_status: string;
  recorded_by: string;
  sacred_checksum: string;
}

interface CeremonialResponse {
  status: string;
  total_ceremonies: number;
  last_ceremony?: string;
  last_updated?: string;
  cycles: CeremonialCycle[];
  metadata: {
    filtered_count: number;
    total_count: number;
    ceremonial_kinds: string[];
    ceremonial_stats: Record<string, number>;
    flame_status: string;
  };
}

interface FestivalCeremonyPanelProps {
  kind?: 'proclamation' | 'silence' | 'blessing';
}

export default function FestivalCeremonyPanel({ kind }: FestivalCeremonyPanelProps) {
  const [ceremonialData, setCeremonialData] = useState<CeremonialResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCeremonialData = async () => {
      setLoading(true);
      setError(null);

      try {
        const params = new URLSearchParams();
        if (kind) {
          params.append('kind', kind);
        }

        const response = await fetch(`/api/ceremony?${params.toString()}`);

        if (!response.ok) {
          throw new Error(`Failed to fetch ceremonial data: ${response.statusText}`);
        }

        const data: CeremonialResponse = await response.json();
        setCeremonialData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchCeremonialData();
  }, [kind]);
  const getCeremonialIcon = (kind: string): string => {
    switch (kind) {
      case 'proclamation':
        return '📢';
      case 'silence':
        return '🤫';
      case 'blessing':
        return '🙏';
      default:
        return '🕯️';
    }
  };

  const getCeremonialColor = (kind: string): string => {
    switch (kind) {
      case 'proclamation':
        return 'text-orange-700 bg-orange-100 border-orange-300';
      case 'silence':
        return 'text-slate-700 bg-slate-100 border-slate-300';
      case 'blessing':
        return 'text-emerald-700 bg-emerald-100 border-emerald-300';
      default:
        return 'text-indigo-700 bg-indigo-100 border-indigo-300';
    }
  };

  const getCeremonialBgClass = (kind: string): string => {
    switch (kind) {
      case 'proclamation':
        return 'bg-orange-50 border-l-orange-400';
      case 'silence':
        return 'bg-slate-50 border-l-slate-400';
      case 'blessing':
        return 'bg-emerald-50 border-l-emerald-400';
      default:
        return 'bg-indigo-50 border-l-indigo-400';
    }
  };

  if (loading) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading ceremonial inscriptions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-800 font-medium">Error loading ceremonial data</p>
        <p className="text-red-600 text-sm mt-2">{error}</p>
      </div>
    );
  }

  // Get cycles from fetched data
  const ceremonialCycles = ceremonialData?.cycles || [];

  if (!ceremonialCycles || ceremonialCycles.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <span className="mr-2">{kind ? getCeremonialIcon(kind) : '🕯️'}</span>
          {kind ? `Sacred ${kind.charAt(0).toUpperCase() + kind.slice(1)}s` : 'Festival Ceremony'}
        </h2>
        <div className="text-center py-8">
          <div className="text-gray-400 text-4xl mb-4">🕯️</div>
          <p className="text-gray-600 italic">
            {kind
              ? `No ${kind}s have been inscribed yet. The sacred altar awaits your first ${kind}.`
              : 'No ceremonial inscriptions yet. The sacred altar awaits your first ceremony.'}
          </p>
          <div className="mt-4 text-sm text-gray-500">
            <p>Sacred ceremonies available:</p>
            <div className="flex justify-center space-x-4 mt-2">
              <span>📢 Proclamations</span>
              <span>🤫 Silences</span>
              <span>🙏 Blessings</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-800 flex items-center">
          <span className="mr-2">{kind ? getCeremonialIcon(kind) : '🕯️'}</span>
          {kind ? `Sacred ${kind.charAt(0).toUpperCase() + kind.slice(1)}s` : 'Sacred Ceremonies'}
          <span className="ml-2 text-sm font-normal text-gray-500">
            ({ceremonialCycles.length} {kind ? kind + 's' : 'inscriptions'})
          </span>
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          Sacred proclamations, silences, and blessings inscribed in the eternal bulletin
        </p>
      </div>

      <div className="p-4">
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {ceremonialCycles.map((cycle, index) => (
            <div
              key={cycle.cycle_id || index}
              className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow duration-200"
            >
              {/* Header with ceremony kind and timestamp */}
              <div className="flex items-start justify-between p-4 border-b border-gray-100">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getCeremonialIcon(cycle.kind)}</span>
                  <div>
                    <span
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getCeremonialColor(cycle.kind)}`}
                    >
                      {cycle.kind.toUpperCase()}
                    </span>
                    <p className="text-xs text-gray-500 mt-1">{cycle.cycle_id}</p>
                  </div>
                </div>

                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {new Date(cycle.timestamp).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-500">{cycle.rite}</p>
                </div>
              </div>

              {/* Ceremonial message */}
              <div className={`p-4 border-l-4 ${getCeremonialBgClass(cycle.kind)}`}>
                <div className="flex items-start space-x-3">
                  <div className="flex-1">
                    <p className="text-gray-800 font-medium text-base leading-relaxed">
                      {cycle.message}
                    </p>

                    {/* Show formatted proclamation if available */}
                    {cycle.proclamation && cycle.proclamation !== cycle.message && (
                      <details className="mt-3">
                        <summary className="text-sm text-gray-600 cursor-pointer hover:text-gray-800">
                          View Sacred Formatting
                        </summary>
                        <div className="mt-2 p-3 bg-white bg-opacity-50 rounded border text-sm text-gray-700 whitespace-pre-line">
                          {cycle.proclamation}
                        </div>
                      </details>
                    )}
                  </div>
                </div>
              </div>

              {/* Footer with metadata */}
              <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>
                    Flame:{' '}
                    <span className="font-mono">{cycle.flame_status?.replace('_', ' ')}</span>
                  </span>
                  <span>
                    Checksum:{' '}
                    <span className="font-mono">{cycle.sacred_checksum?.substring(0, 8)}...</span>
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer with ceremonial stats */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 rounded-b-lg">
        <div className="flex items-center justify-center space-x-6 text-xs text-gray-600">
          {(() => {
            const counts = ceremonialCycles.reduce(
              (acc, cycle) => {
                acc[cycle.kind] = (acc[cycle.kind] || 0) + 1;
                return acc;
              },
              {} as Record<string, number>
            );

            return (
              <>
                {counts.proclamation && (
                  <span className="flex items-center">
                    📢 <strong className="ml-1">{counts.proclamation}</strong> Proclamations
                  </span>
                )}
                {counts.silence && (
                  <span className="flex items-center">
                    🤫 <strong className="ml-1">{counts.silence}</strong> Silences
                  </span>
                )}
                {counts.blessing && (
                  <span className="flex items-center">
                    🙏 <strong className="ml-1">{counts.blessing}</strong> Blessings
                  </span>
                )}
              </>
            );
          })()}
        </div>
        <p className="text-xs text-gray-500 text-center mt-2">
          🕯️ Sacred ceremonies preserved in the eternal bulletin
        </p>
      </div>
    </div>
  );
}
