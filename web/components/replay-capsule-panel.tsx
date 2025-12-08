'use client';

import { useEffect, useState } from 'react';

interface ReplayCapsule {
  id: string;
  timestamp: string;
  engine: string;
  status: string;
  event: string;
  metadata?: Record<string, any>;
}

export function ReplayCapsulePanel() {
  const [capsules, setCapsules] = useState<ReplayCapsule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCapsules = async () => {
      try {
        setLoading(true);
        const res = await fetch('/api/replaycapsules');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setCapsules(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch replay capsules:', err);
        setError('Failed to load capsules');
      } finally {
        setLoading(false);
      }
    };

    fetchCapsules();
    const interval = setInterval(fetchCapsules, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const formatTimestamp = (timestamp: string) => {
    try {
      return new Date(timestamp).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return timestamp;
    }
  };

  const getStatusColor = (status: string) => {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('operational') || statusLower.includes('success')) {
      return 'text-green-400';
    }
    if (statusLower.includes('degraded') || statusLower.includes('warning')) {
      return 'text-orange-400';
    }
    if (statusLower.includes('failed') || statusLower.includes('error') || statusLower.includes('down')) {
      return 'text-red-400';
    }
    return 'text-gray-400';
  };

  return (
    <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-[#FFD700] flex items-center">
          <span className="mr-2">🕰️</span>
          Replay Capsule Archive
        </h2>
        <span className="text-xs text-gray-400">
          {capsules.length} capsules
        </span>
      </div>

      {loading && capsules.length === 0 && (
        <div className="text-center py-8 text-gray-400">
          <span className="text-2xl">⏳</span>
          <p className="mt-2">Loading capsules...</p>
        </div>
      )}

      {error && (
        <div className="p-3 bg-red-900/30 border border-red-500 rounded-lg text-red-400 text-sm">
          ⚠️ {error}
        </div>
      )}

      {!loading && capsules.length === 0 && !error && (
        <div className="text-center py-8 text-gray-400">
          <span className="text-2xl">📦</span>
          <p className="mt-2">No capsules archived yet</p>
        </div>
      )}

      {capsules.length > 0 && (
        <ul className="space-y-2 text-sm max-h-96 overflow-y-auto custom-scrollbar">
          {capsules.map((capsule, idx) => (
            <li
              key={capsule.id || idx}
              className="p-3 bg-[#0A0F29] rounded-lg border border-gray-700 hover:border-[#FFD700] transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-gray-400 text-xs">
                      {formatTimestamp(capsule.timestamp)}
                    </span>
                    <span className="px-2 py-0.5 bg-blue-900/50 rounded text-blue-300 text-xs">
                      {capsule.engine}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`font-medium ${getStatusColor(capsule.status)}`}>
                      {capsule.status}
                    </span>
                    {capsule.event && (
                      <span className="text-gray-400">• {capsule.event}</span>
                    )}
                  </div>
                  {capsule.metadata && Object.keys(capsule.metadata).length > 0 && (
                    <details className="mt-2">
                      <summary className="text-xs text-[#FFD700] cursor-pointer hover:underline">
                        View metadata
                      </summary>
                      <pre className="mt-1 text-xs text-gray-400 bg-black/30 p-2 rounded overflow-x-auto">
                        {JSON.stringify(capsule.metadata, null, 2)}
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #0A0F29;
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #FFD700;
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #FFA500;
        }
      `}</style>
    </div>
  );
}
