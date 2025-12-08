'use client';

import { useEffect, useState } from 'react';
import { getSpatialAudioEngine } from '@/lib/spatial-audio-engine';
import { SCENE_METADATA, getSourcesByType } from '@/lib/spatial-audio-design';

export default function SpatialAudioControls() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(30);
  const [mutedTypes, setMutedTypes] = useState<Set<string>>(new Set());
  const [audioEngine] = useState(() => getSpatialAudioEngine());

  useEffect(() => {
    return () => {
      audioEngine.stop();
    };
  }, [audioEngine]);

  const handlePlay = () => {
    if (!isPlaying) {
      audioEngine.start();
      setIsPlaying(true);
    }
  };

  const handleStop = () => {
    audioEngine.stop();
    setIsPlaying(false);
  };

  const handleVolumeChange = (value: number) => {
    setVolume(value);
    audioEngine.setVolume(value / 100);
  };

  const toggleMuteType = (type: 'engine' | 'seal' | 'ceremonial' | 'intelligence') => {
    const newMuted = new Set(mutedTypes);
    if (newMuted.has(type)) {
      newMuted.delete(type);
      audioEngine.muteType(type, false);
    } else {
      newMuted.add(type);
      audioEngine.muteType(type, true);
    }
    setMutedTypes(newMuted);
  };

  return (
    <div className="space-y-6 p-6 bg-[#1A1F3C] rounded-lg border-2 border-[#FFD700]/30">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#FFD700] mb-2">
          🎵 Spatial Audio Experience
        </h2>
        <p className="text-sm text-gray-400">
          360° Immersive Soundscape for Codex Dominion
        </p>
      </div>

      {/* Scene Info */}
      <div className="grid grid-cols-2 gap-4 p-4 bg-[#0A0F29] rounded border border-[#FFD700]/20">
        <div className="text-center">
          <div className="text-2xl font-bold text-[#FFD700]">
            {SCENE_METADATA.totalSources}
          </div>
          <div className="text-xs text-gray-400">Total Sources</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-[#FFD700]">
            {SCENE_METADATA.engineCount}
          </div>
          <div className="text-xs text-gray-400">Engines</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-[#FFD700]">
            {SCENE_METADATA.sealCount}
          </div>
          <div className="text-xs text-gray-400">Council Seals</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-[#FFD700]">
            360°
          </div>
          <div className="text-xs text-gray-400">Coverage</div>
        </div>
      </div>

      {/* Playback Controls */}
      <div className="space-y-4">
        <div className="flex gap-3 justify-center">
          <button
            onClick={handlePlay}
            disabled={isPlaying}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              isPlaying
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-[#FFD700] text-[#0A0F29] hover:bg-[#FFC700] hover:scale-105'
            }`}
          >
            ▶️ Start Experience
          </button>
          <button
            onClick={handleStop}
            disabled={!isPlaying}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              !isPlaying
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-red-600 text-white hover:bg-red-700 hover:scale-105'
            }`}
          >
            ⏹️ Stop
          </button>
        </div>

        {/* Volume Slider */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <label className="text-sm font-medium text-gray-300">
              🔊 Master Volume
            </label>
            <span className="text-sm text-[#FFD700] font-mono">
              {volume}%
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value={volume}
            onChange={(e) => handleVolumeChange(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-[#FFD700]"
          />
        </div>
      </div>

      {/* Source Type Mute Controls */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-gray-300 uppercase tracking-wide">
          Layer Controls
        </h3>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => toggleMuteType('engine')}
            className={`p-3 rounded-lg border-2 transition-all ${
              mutedTypes.has('engine')
                ? 'bg-gray-700 border-gray-600 text-gray-400'
                : 'bg-[#0A0F29] border-[#FFD700]/30 text-[#FFD700] hover:border-[#FFD700]'
            }`}
          >
            <div className="text-lg mb-1">⚙️</div>
            <div className="text-xs font-medium">Engines ({SCENE_METADATA.engineCount})</div>
          </button>
          <button
            onClick={() => toggleMuteType('seal')}
            className={`p-3 rounded-lg border-2 transition-all ${
              mutedTypes.has('seal')
                ? 'bg-gray-700 border-gray-600 text-gray-400'
                : 'bg-[#0A0F29] border-purple-500/30 text-purple-400 hover:border-purple-500'
            }`}
          >
            <div className="text-lg mb-1">🛰️</div>
            <div className="text-xs font-medium">Council Seals ({SCENE_METADATA.sealCount})</div>
          </button>
          <button
            onClick={() => toggleMuteType('ceremonial')}
            className={`p-3 rounded-lg border-2 transition-all ${
              mutedTypes.has('ceremonial')
                ? 'bg-gray-700 border-gray-600 text-gray-400'
                : 'bg-[#0A0F29] border-red-500/30 text-red-400 hover:border-red-500'
            }`}
          >
            <div className="text-lg mb-1">👑</div>
            <div className="text-xs font-medium">Ceremonial ({SCENE_METADATA.ceremonialCount})</div>
          </button>
          <button
            onClick={() => toggleMuteType('intelligence')}
            className={`p-3 rounded-lg border-2 transition-all ${
              mutedTypes.has('intelligence')
                ? 'bg-gray-700 border-gray-600 text-gray-400'
                : 'bg-[#0A0F29] border-blue-500/30 text-blue-400 hover:border-blue-500'
            }`}
          >
            <div className="text-lg mb-1">🧠</div>
            <div className="text-xs font-medium">Intelligence (2)</div>
          </button>
        </div>
      </div>

      {/* Key Elements Description */}
      <div className="p-4 bg-[#0A0F29] rounded border border-[#FFD700]/20 space-y-2">
        <h4 className="text-sm font-bold text-[#FFD700] mb-3">Key Elements:</h4>
        <div className="space-y-2 text-xs text-gray-300">
          <div>
            <span className="font-semibold text-[#FFD700]">👑 Custodian Crown Pulse:</span>
            <span className="ml-2">Center channel at C4 (261.63 Hz) - Steady heartbeat anchor</span>
          </div>
          <div>
            <span className="font-semibold text-purple-400">🛰️ Council Harmonics:</span>
            <span className="ml-2">5 seals orbiting in surround configuration (E4-C5 range)</span>
          </div>
          <div>
            <span className="font-semibold text-red-400">🦅 Heir Dedication:</span>
            <span className="ml-2">Behind & above at C5 (523.25 Hz) - Enveloping melody</span>
          </div>
          <div>
            <span className="font-semibold text-blue-400">🧠 RAG Intelligence:</span>
            <span className="ml-2">Zenith position at A5 (880 Hz) - Knowledge whisper</span>
          </div>
          <div>
            <span className="font-semibold text-yellow-400">⚙️ 16 Engines:</span>
            <span className="ml-2">360° distributed (Profit East, Replay North, etc.)</span>
          </div>
        </div>
      </div>

      {/* Status Indicator */}
      <div className="text-center">
        <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full ${
          isPlaying
            ? 'bg-green-900/30 text-green-400 border border-green-500/50'
            : 'bg-gray-800/30 text-gray-400 border border-gray-600/50'
        }`}>
          <div className={`w-2 h-2 rounded-full ${isPlaying ? 'bg-green-400 animate-pulse' : 'bg-gray-400'}`} />
          <span className="text-xs font-medium">
            {isPlaying ? 'Spatial Audio Active' : 'Spatial Audio Inactive'}
          </span>
        </div>
      </div>

      {/* Warning */}
      <div className="text-xs text-center text-gray-500 italic">
        🎧 Best experienced with headphones for full 3D spatial effect
      </div>
    </div>
  );
}
