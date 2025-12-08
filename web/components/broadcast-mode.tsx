'use client';

import { useState, useEffect } from 'react';
import { ConstellationMap } from './constellation-map';
import { ReplayViewer } from './replay-viewer';
import BroadcastChat from './broadcast-chat';

export function BroadcastMode() {
  const [isBroadcast, setIsBroadcast] = useState(false);

  const toggleBroadcast = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsBroadcast(true);
    } else {
      document.exitFullscreen();
      setIsBroadcast(false);
    }
  };

  // Listen for fullscreen changes (e.g., ESC key)
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsBroadcast(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  return (
    <div className={`bg-[#0A0F29] text-white ${isBroadcast ? 'p-0 h-screen' : 'p-6'}`}>
      {/* Header */}
      <div className={`flex justify-between items-center ${isBroadcast ? 'p-6 pb-2' : 'mb-4'}`}>
        <h1 className="text-3xl font-bold text-[#FFD700]" style={{ fontFamily: 'Cinzel Decorative, serif' }}>
          🔥 Ceremonial Broadcast Mode
        </h1>
        <button
          onClick={toggleBroadcast}
          className="px-6 py-3 bg-[#FFD700] text-[#0A0F29] rounded-lg font-bold hover:bg-[#FFC700] transition-colors shadow-lg"
        >
          {isBroadcast ? '⏹ Exit Broadcast' : '📡 Enter Broadcast'}
        </button>
      </div>

      {/* Broadcast Layout */}
      <div className={`grid grid-cols-1 lg:grid-cols-3 gap-6 ${isBroadcast ? 'h-[calc(100vh-100px)] px-6 pb-6' : 'h-[80vh]'}`}>
        {/* Left Panel: Constellation Map */}
        <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4 flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xl font-bold text-[#FFD700]">
              🌌 System Constellation
            </h2>
            <span className="text-sm text-gray-400">Live Network Visualization</span>
          </div>
          <div className="flex-1 overflow-hidden">
            <ConstellationMap />
          </div>
        </div>

        {/* Center Panel: Replay Viewer */}
        <div className="bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700] p-4 flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xl font-bold text-[#FFD700]">
              🕰️ Ceremonial Replay
            </h2>
            <span className="text-sm text-gray-400">Timeline Playback</span>
          </div>
          <div className="flex-1 overflow-hidden">
            <ReplayViewer />
          </div>
        </div>

        {/* Right Panel: Ceremonial Chat */}
        <div className="flex flex-col">
          <BroadcastChat userName="Jermaine" userRole="sovereign" />
        </div>
      </div>

      {/* Broadcast Status Bar */}
      {isBroadcast && (
        <div className="fixed bottom-0 left-0 right-0 bg-[#FFD700] text-[#0A0F29] px-6 py-2 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="font-bold">🔴 LIVE BROADCAST</span>
            <span className="text-sm opacity-80">
              Codex Dominion • Flame Sovereign Status • v2.0.0
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm">Press ESC to exit fullscreen</span>
          </div>
        </div>
      )}
    </div>
  );
}
