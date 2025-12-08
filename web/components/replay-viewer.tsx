'use client';

import { useEffect, useState } from 'react';
import { CapsuleAnnotationPanel } from './capsule-annotation-panel';

interface ReplayCapsule {
  id: string;
  timestamp: string;
  engine: string;
  status: string;
  event?: string;
  metadata?: Record<string, any>;
}

type ReplayMode = 'daily' | 'seasonal' | 'epochal' | 'millennial';

export function ReplayViewer() {
  const [capsules, setCapsules] = useState<ReplayCapsule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [index, setIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [mode, setMode] = useState<ReplayMode>('daily');

  useEffect(() => {
    const fetchCapsules = async () => {
      try {
        setLoading(true);
        const res = await fetch(`/api/replaycapsules?mode=${mode}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setCapsules(data);
        setIndex(0); // Reset to start when mode changes
        setIsPlaying(false);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch replay capsules:', err);
        setError('Failed to load replay capsules');
      } finally {
        setLoading(false);
      }
    };

    fetchCapsules();
  }, [mode]);

  // Playback loop
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isPlaying && index < capsules.length - 1) {
      timer = setInterval(() => {
        setIndex((i) => i + 1);
      }, 1500); // advance every 1.5s
    } else if (isPlaying && index >= capsules.length - 1) {
      setIsPlaying(false); // Stop at end
    }
    return () => clearInterval(timer);
  }, [isPlaying, index, capsules.length]);

  // Playback controls
  const play = () => setIsPlaying(true);
  const pause = () => setIsPlaying(false);
  const reset = () => {
    setIndex(0);
    setIsPlaying(false);
  };
  const fastForward = () => setIndex((i) => Math.min(i + 5, capsules.length - 1));
  const rewind = () => setIndex((i) => Math.max(i - 5, 0));

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

  const getStatusDotColor = (status: string) => {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('operational') || statusLower.includes('success')) {
      return 'bg-green-500';
    }
    if (statusLower.includes('degraded') || statusLower.includes('warning')) {
      return 'bg-orange-500';
    }
    if (statusLower.includes('failed') || statusLower.includes('error') || statusLower.includes('down')) {
      return 'bg-red-500';
    }
    return 'bg-gray-500';
  };

  const getModeIcon = (m: ReplayMode) => {
    const icons = {
      daily: '📅',
      seasonal: '🍂',
      epochal: '⏳',
      millennial: '🌌',
    };
    return icons[m];
  };

  const getModeDescription = (m: ReplayMode) => {
    const descriptions = {
      daily: 'Last 24 hours',
      seasonal: 'Last 3 months',
      epochal: 'Last year',
      millennial: 'All time',
    };
    return descriptions[m];
  };

  return (
    <div className="bg-[#1A1F3C] p-6 rounded-lg border border-[#FFD700] shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-[#FFD700] flex items-center">
          <span className="mr-2">🎭</span>
          Ceremonial Replay Viewer
        </h2>
        <span className="text-xs text-gray-400">
          {capsules.length} capsules • {getModeDescription(mode)}
        </span>
      </div>

      {/* Mode Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        {(['daily', 'seasonal', 'epochal', 'millennial'] as ReplayMode[]).map((m) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className={`
              px-4 py-2 rounded-lg font-semibold transition-all flex items-center space-x-2
              ${mode === m
                ? 'bg-[#FFD700] text-black shadow-lg scale-105'
                : 'bg-[#0A0F29] text-gray-300 hover:bg-[#FFD700] hover:text-black'
              }
            `}
          >
            <span>{getModeIcon(m)}</span>
            <span>{m.charAt(0).toUpperCase() + m.slice(1)}</span>
          </button>
        ))}
      </div>

      {loading && capsules.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <span className="text-3xl">⏳</span>
          <p className="mt-2">Loading ceremonial replays...</p>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-900/30 border border-red-500 rounded-lg text-red-400 mb-4">
          ⚠️ {error}
        </div>
      )}

      {!loading && capsules.length === 0 && !error && (
        <div className="text-center py-12 text-gray-400">
          <span className="text-3xl">📜</span>
          <p className="mt-2">No ceremonial events recorded yet</p>
          <p className="text-xs mt-1">Events will appear as engines generate capsules</p>
        </div>
      )}

      {capsules.length > 0 && (
        <>
          {/* Current Capsule Display */}
          <div className="mb-6 p-6 bg-[#0A0F29] rounded-lg border border-[#FFD700]">
            <p className="text-xs text-gray-400 mb-2">
              🕰️ {new Date(capsules[index].timestamp).toLocaleString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
              })}
            </p>
            <div className="flex items-center space-x-3 mb-3">
              <span className={`w-4 h-4 rounded-full ${getStatusDotColor(capsules[index].status)} animate-pulse`}></span>
              <span className="text-2xl font-bold text-[#FFD700]">{capsules[index].engine}</span>
              <span className="text-gray-500">—</span>
              <span className={`text-xl font-semibold ${getStatusColor(capsules[index].status)}`}>
                {capsules[index].status}
              </span>
            </div>
            {capsules[index].event && (
              <p className="text-base text-gray-300">📝 {capsules[index].event}</p>
            )}
            {capsules[index].metadata && (
              <details className="mt-3">
                <summary className="text-sm text-[#FFD700] cursor-pointer hover:underline">
                  View metadata
                </summary>
                <pre className="mt-2 text-xs text-gray-300 bg-black/40 p-3 rounded overflow-x-auto border border-[#FFD700]/30">
                  {JSON.stringify(capsules[index].metadata, null, 2)}
                </pre>
              </details>
            )}
          </div>

          {/* Playback Controls */}
          <div className="flex items-center space-x-3 mb-4">
            <button
              onClick={reset}
              className="px-4 py-2 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] transition-all flex items-center space-x-2"
            >
              <span>⏮</span>
              <span>Reset</span>
            </button>
            <button
              onClick={rewind}
              disabled={index === 0}
              className="px-4 py-2 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              ⏪ -5
            </button>
            {!isPlaying ? (
              <button
                onClick={play}
                disabled={index >= capsules.length - 1}
                className="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center space-x-2"
              >
                <span>▶</span>
                <span>Play</span>
              </button>
            ) : (
              <button
                onClick={pause}
                className="px-6 py-2 bg-orange-600 text-white font-semibold rounded-lg hover:bg-orange-500 transition-all flex items-center space-x-2"
              >
                <span>⏸</span>
                <span>Pause</span>
              </button>
            )}
            <button
              onClick={fastForward}
              disabled={index >= capsules.length - 1}
              className="px-4 py-2 bg-[#FFD700] text-black font-semibold rounded-lg hover:bg-[#FFA500] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              ⏩ +5
            </button>
            <div className="flex-1"></div>
            <span className="text-sm text-gray-400 font-mono">
              {index + 1} / {capsules.length}
            </span>
          </div>

          {/* Timeline Progress Bar */}
          <div className="mb-6">
            <div className="w-full bg-gray-700 h-3 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-[#FFD700] to-[#FFA500] h-3 rounded-full transition-all duration-300"
                style={{ width: `${((index + 1) / capsules.length) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Timeline List */}
          <div className="space-y-2 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
            {capsules.map((capsule, idx) => (
              <div
                key={capsule.id || idx}
                onClick={() => {
                  setIndex(idx);
                  setIsPlaying(false);
                }}
                className={`flex items-center space-x-3 p-3 rounded-lg cursor-pointer transition-all ${
                  idx === index
                    ? 'bg-[#FFD700]/20 border-2 border-[#FFD700]'
                    : 'bg-[#0A0F29] border border-gray-700 hover:border-[#FFD700]'
                }`}
              >
                <div className={`w-2 h-2 rounded-full ${getStatusDotColor(capsule.status)}`}></div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-400">
                      {new Date(capsule.timestamp).toLocaleTimeString()}
                    </span>
                    <span className="text-sm font-medium text-[#FFD700] truncate">
                      {capsule.engine}
                    </span>
                    <span className={`text-xs ${getStatusColor(capsule.status)}`}>
                      {capsule.status}
                    </span>
                  </div>
                </div>
                {idx === index && (
                  <span className="text-[#FFD700]">▶</span>
                )}
              </div>
            ))}
          </div>
        </>
      )}

      {/* Capsule Annotation Panel */}
      {!loading && !error && capsules.length > 0 && (
        <div className="mt-6">
          <CapsuleAnnotationPanel
            capsuleId={capsules[index].id}
            engine={capsules[index].engine}
          />
        </div>
      )}

      <style>{`
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
