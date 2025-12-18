'use client';

import { useEffect, useState, useRef } from 'react';
import { ConstellationMap } from './constellation-map';
import { FeedbackPanel } from './feedback-panel';
import BroadcastChat from './broadcast-chat';
import { useBroadcastSync } from '../hooks/useBroadcastSync';
import { useReplay } from '../context/ReplayContext';

export interface BroadcastAudienceProps {
  role?: 'council' | 'heir' | 'observer';
  wsUrl?: string;
  showVideo?: boolean;
  userName?: string;
}

export function BroadcastAudience({
  role = 'observer',
  wsUrl = process.env.NEXT_PUBLIC_WS_RELAY_URL || 'wss://codexdominion.app/broadcast',
  showVideo = false,
  userName = 'Council Member',
}: BroadcastAudienceProps) {
  const { index, capsules } = useReplay();
  const { broadcastState, connect, disconnect } = useBroadcastSync({
    wsUrl,
    role,
    autoConnect: true,
  });

  const [isFullscreen, setIsFullscreen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  // Handle fullscreen toggle
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  // Get current capsule
  const currentCapsule = capsules.length > 0 ? capsules[index] : null;

  // Role display names
  const roleNames = {
    council: '👑 Council Member',
    heir: '🔥 Heir',
    observer: '👁️ Observer',
  };

  // Status color mapping
  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'operational':
        return 'text-green-400';
      case 'degraded':
        return 'text-orange-400';
      case 'failed':
        return 'text-red-400';
      default:
        return 'text-gray-400';
    }
  };

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case 'operational':
        return '✅';
      case 'degraded':
        return '⚠️';
      case 'failed':
        return '❌';
      default:
        return '⏳';
    }
  };

  return (
    <div
      className={`bg-[#0A0F29] text-white ${isFullscreen ? 'p-0 h-screen' : 'p-6 min-h-screen'} flex flex-col`}
    >
      {/* Header */}
      <div className={`flex justify-between items-center ${isFullscreen ? 'p-6 pb-4' : 'mb-6'}`}>
        <div>
          <h1 className="text-3xl font-bold text-[#FFD700] mb-2" style={{ fontFamily: 'Cinzel Decorative, serif' }}>
            🔥 Codex Dominion Broadcast
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">{roleNames[role]}</span>
            {broadcastState.isConnected ? (
              <span className="flex items-center gap-2 text-sm text-green-400">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                Connected
              </span>
            ) : (
              <span className="flex items-center gap-2 text-sm text-red-400">
                <span className="w-2 h-2 bg-red-400 rounded-full"></span>
                Disconnected
              </span>
            )}
            <span className="text-sm text-gray-400">
              Capsule: {index + 1} / {capsules.length || 0}
            </span>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={toggleFullscreen}
            className="px-4 py-2 bg-[#1A1F3C] text-[#FFD700] border border-[#FFD700] rounded-lg hover:bg-[#FFD700] hover:text-[#0A0F29] transition-colors"
          >
            {isFullscreen ? '⏹ Exit Fullscreen' : '⛶ Fullscreen'}
          </button>
          {!broadcastState.isConnected && (
            <button
              onClick={connect}
              className="px-4 py-2 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors"
            >
              🔌 Reconnect
            </button>
          )}
        </div>
      </div>

      {/* Connection Warning */}
      {!broadcastState.isConnected && (
        <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 mb-6">
          <p className="text-red-400 font-bold">⚠️ Broadcast Disconnected</p>
          <p className="text-sm text-gray-300 mt-1">
            Unable to connect to sovereign broadcast. Attempting to reconnect...
          </p>
        </div>
      )}

      {/* Current Capsule Display */}
      {currentCapsule ? (
        <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm text-gray-400 mb-2">
                🕰️ {new Date(currentCapsule.timestamp).toLocaleString()}
              </p>
              <p className="text-2xl font-bold">
                <span className="text-[#FFD700]">{currentCapsule.engine}</span>
                <span className="mx-3">—</span>
                <span className={getStatusColor(currentCapsule.status)}>
                  {getStatusIcon(currentCapsule.status)} {currentCapsule.status?.toUpperCase()}
                </span>
              </p>
            </div>
          </div>

          {currentCapsule.event && (
            <div className="bg-[#0A0F29] rounded p-4 mt-4">
              <p className="text-gray-300">{currentCapsule.event}</p>
            </div>
          )}

          {currentCapsule.metadata && Object.keys(currentCapsule.metadata).length > 0 && (
            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-[#FFD700] hover:text-[#FFC700]">
                📋 View Metadata
              </summary>
              <pre className="mt-2 bg-[#0A0F29] rounded p-3 text-xs text-gray-400 overflow-x-auto">
                {JSON.stringify(currentCapsule.metadata, null, 2)}
              </pre>
            </details>
          )}
        </div>
      ) : (
        <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-12 mb-6 text-center">
          <p className="text-gray-400 text-lg">⏳ Waiting for broadcast data...</p>
          <p className="text-sm text-gray-500 mt-2">
            Sovereign has not yet started the ceremonial broadcast.
          </p>
        </div>
      )}

      {/* Video Stream (if enabled) */}
      {showVideo && (
        <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4 mb-6">
          <h2 className="text-xl font-bold text-[#FFD700] mb-3">📹 Live Broadcast Stream</h2>
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full rounded bg-black"
            style={{ maxHeight: '400px' }}
          >
            <track kind="captions" />
          </video>
          <p className="text-sm text-gray-400 mt-2 text-center">
            WebRTC stream from sovereign broadcaster
          </p>
        </div>
      )}

      {/* Constellation Map */}
      <div className={`bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4 flex-1 ${isFullscreen ? 'mb-16' : ''}`}>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xl font-bold text-[#FFD700]">🌌 System Constellation</h2>
          <span className="text-sm text-gray-400">
            {currentCapsule ? `Highlighting: ${currentCapsule.engine}` : 'Awaiting sync...'}
          </span>
        </div>
        {capsules.length > 0 ? (
          <ConstellationMap />
        ) : (
          <div className="w-full h-96 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <p className="text-lg mb-2">🌌</p>
              <p>Constellation map will sync when broadcast begins</p>
            </div>
          </div>
        )}
      </div>

      {/* Council Feedback Panel (Council members only) */}
      {role === 'council' && (
        <div className="mt-6">
          <FeedbackPanel
            userName={userName}
            onFeedbackSent={(feedback) => {
              console.log('Council feedback submitted:', feedback);
              // TODO: Send feedback via WebSocket to sovereign
            }}
          />
        </div>
      )}

      {/* Ceremonial Chat */}
      <div className="mt-6">
        <BroadcastChat userName={userName} userRole={role} />
      </div>

      {/* Status Bar (Fullscreen Only) */}
      {isFullscreen && (
        <div className="fixed bottom-0 left-0 right-0 bg-[#FFD700] text-[#0A0F29] px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="font-bold">🔴 LIVE BROADCAST</span>
            <span className="text-sm opacity-80">
              Codex Dominion • {roleNames[role]} • v2.0.0
            </span>
          </div>
          <div className="flex items-center gap-4">
            {currentCapsule && (
              <span className="text-sm font-bold">
                {currentCapsule.engine} • {currentCapsule.status?.toUpperCase()}
              </span>
            )}
            <span className="text-sm">Press ESC to exit</span>
          </div>
        </div>
      )}

      {/* Role-Based Footer Info */}
      {!isFullscreen && (
        <div className="mt-6 border-t border-[#FFD700]/30 pt-4">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm text-gray-400">Role</p>
              <p className="text-[#FFD700] font-bold">{roleNames[role]}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Client ID</p>
              <p className="text-[#FFD700] font-mono text-xs">
                {broadcastState.clientId || 'Not Connected'}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Last Sync</p>
              <p className="text-[#FFD700] text-sm">
                {broadcastState.lastSync
                  ? new Date(broadcastState.lastSync).toLocaleTimeString()
                  : 'Never'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
