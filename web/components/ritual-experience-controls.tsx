'use client';

import { useEffect, useState } from 'react';
import { getSpatialAudioEngine } from '../lib/spatial-audio-engine';
import {
  RitualPhase,
  EngineHealthStatus,
  RITUAL_PHASE_CONFIG,
  COSMIC_CHOIR_LAYERS,
  calculateHarmonicResonance,
  generateRitualExperienceDescription
} from '../lib/ritual-experience';
import { getAllAudioSources } from '../lib/spatial-audio-design';

export default function RitualExperienceControls() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<RitualPhase>('resonance');
  const [audioEngine] = useState(() => getSpatialAudioEngine());
  const [engineHealth, setEngineHealth] = useState<EngineHealthStatus[]>([]);
  const [showConstellationMap, setShowConstellationMap] = useState(true);
  const [cosmicChoirActive, setCosmicChoirActive] = useState(true);

  // Simulate engine health changes for demonstration
  useEffect(() => {
    if (!isPlaying) return;

    const healthStatuses: EngineHealthStatus[] = [
      { engineId: 'profit-engine', health: 95, status: 'optimal', lastUpdate: new Date().toISOString() },
      { engineId: 'replay-capsule-engine', health: 88, status: 'healthy', lastUpdate: new Date().toISOString() },
      { engineId: 'intelligence-engine', health: 92, status: 'optimal', lastUpdate: new Date().toISOString() },
      { engineId: 'content-engine', health: 78, status: 'healthy', lastUpdate: new Date().toISOString() },
      { engineId: 'commerce-engine', health: 85, status: 'healthy', lastUpdate: new Date().toISOString() },
      { engineId: 'marketing-engine', health: 90, status: 'optimal', lastUpdate: new Date().toISOString() }
    ];

    setEngineHealth(healthStatuses);
    audioEngine.updateAllEngineHealth(healthStatuses);

    // Simulate health fluctuations
    const interval = setInterval(() => {
      const updated = healthStatuses.map(e => ({
        ...e,
        health: Math.max(20, Math.min(100, e.health + (Math.random() - 0.5) * 10)),
        lastUpdate: new Date().toISOString()
      }));
      setEngineHealth(updated);
      audioEngine.updateAllEngineHealth(updated);
    }, 5000);

    return () => clearInterval(interval);
  }, [isPlaying, audioEngine]);

  useEffect(() => {
    return () => {
      audioEngine.stop();
    };
  }, [audioEngine]);

  const handleStart = () => {
    audioEngine.start();
    audioEngine.setRitualPhase(currentPhase);
    setIsPlaying(true);
  };

  const handleStop = () => {
    audioEngine.stop();
    setIsPlaying(false);
  };

  const handlePhaseChange = (phase: RitualPhase) => {
    setCurrentPhase(phase);
    if (isPlaying) {
      audioEngine.setRitualPhase(phase);
    }
  };

  // Calculate harmonic resonance
  const allSources = getAllAudioSources();
  const harmonicResonance = calculateHarmonicResonance(allSources);

  const ritualDescription = generateRitualExperienceDescription({
    phase: currentPhase,
    engineHealthStatuses: engineHealth,
    cosmicChoirActive,
    constellationVisible: showConstellationMap,
    harmonicResonance
  });

  const phaseConfig = RITUAL_PHASE_CONFIG[currentPhase];
  const healthyEngines = engineHealth.filter(e => e.health >= 70).length;

  return (
    <div className="space-y-6 p-6 bg-gradient-to-br from-[#0A0F29] via-[#1A1F3C] to-[#0A0F29] rounded-lg border-2 border-[#FFD700]/40 shadow-2xl">
      {/* Header */}
      <div className="text-center relative">
        <div className="absolute inset-0 bg-[#FFD700]/5 blur-3xl"></div>
        <h2 className="text-3xl font-bold text-[#FFD700] mb-2 relative z-10 animate-pulse">
          🔥 Ritual Experience
        </h2>
        <p className="text-sm text-gray-300 relative z-10">
          Immersive Ceremony · Constellation of Voices · Eternal Resonance
        </p>
      </div>

      {/* Ritual Phase Selector */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-[#FFD700] uppercase tracking-wide">
          🌙 Ritual Phase
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {(Object.keys(RITUAL_PHASE_CONFIG) as RitualPhase[]).map(phase => (
            <button
              key={phase}
              onClick={() => handlePhaseChange(phase)}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                currentPhase === phase
                  ? 'bg-[#FFD700]/20 border-[#FFD700] scale-105'
                  : 'bg-[#1A1F3C] border-[#FFD700]/30 hover:border-[#FFD700]/60'
              }`}
            >
              <div className="font-bold text-white capitalize mb-1">{phase}</div>
              <div className="text-xs text-gray-400">
                {RITUAL_PHASE_CONFIG[phase].description.substring(0, 50)}...
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Playback Controls */}
      <div className="flex gap-3 justify-center">
        <button
          onClick={handleStart}
          disabled={isPlaying}
          className={`px-8 py-4 rounded-lg font-bold text-lg transition-all ${
            isPlaying
              ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-[#FFD700] to-[#FFA500] text-[#0A0F29] hover:scale-110 shadow-lg hover:shadow-[#FFD700]/50'
          }`}
        >
          🔥 Begin Ritual
        </button>
        <button
          onClick={handleStop}
          disabled={!isPlaying}
          className={`px-8 py-4 rounded-lg font-bold text-lg transition-all ${
            !isPlaying
              ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
              : 'bg-red-600 text-white hover:bg-red-700 hover:scale-110 shadow-lg'
          }`}
        >
          ⏹️ End Ritual
        </button>
      </div>

      {/* Constellation Status */}
      {isPlaying && (
        <div className="space-y-4 animate-fade-in">
          {/* Living Constellation */}
          <div className="bg-[#0A0F29] rounded-lg p-6 border-2 border-purple-500/40">
            <h3 className="text-lg font-bold text-purple-400 mb-4 flex items-center gap-2">
              ⭐ Living Constellation
              <span className="text-sm font-normal text-gray-400">
                (Sight & Sound United)
              </span>
            </h3>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-[#FFD700]">
                  {healthyEngines}/{engineHealth.length}
                </div>
                <div className="text-xs text-gray-400">Voices Resonating</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400">
                  {(harmonicResonance.cosmicAlignment * 100).toFixed(0)}%
                </div>
                <div className="text-xs text-gray-400">Cosmic Alignment</div>
              </div>
            </div>

            {/* Directional Awareness */}
            <div className="space-y-2">
              <div className="text-sm font-semibold text-gray-300 mb-2">
                🧭 Directional Awareness:
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {audioEngine.getDirectionalHealthReport().slice(0, 6).map((report, i) => (
                  <div key={i} className="bg-[#1A1F3C] rounded px-3 py-2 text-gray-300 border border-[#FFD700]/20">
                    {report}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Cosmic Choir */}
          <div className="bg-[#0A0F29] rounded-lg p-6 border-2 border-blue-500/40">
            <h3 className="text-lg font-bold text-blue-400 mb-4 flex items-center gap-2">
              🎵 Cosmic Choir
              <label className="ml-auto flex items-center gap-2 text-sm font-normal">
                <input
                  type="checkbox"
                  checked={cosmicChoirActive}
                  onChange={(e) => setCosmicChoirActive(e.target.checked)}
                  className="w-4 h-4"
                />
                Active
              </label>
            </h3>

            {cosmicChoirActive && (
              <div className="space-y-2">
                {COSMIC_CHOIR_LAYERS.map(layer => (
                  <div key={layer.name} className="bg-[#1A1F3C] rounded p-3 border border-blue-500/20">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold text-blue-300">{layer.name}</span>
                      <span className="text-xs text-gray-400 capitalize">{layer.position}</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {layer.sources.length} voices · {layer.blend} blend
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Harmonic Resonance */}
          <div className="bg-[#0A0F29] rounded-lg p-6 border-2 border-green-500/40">
            <h3 className="text-lg font-bold text-green-400 mb-4">
              🌊 Harmonic Resonance
            </h3>

            <div className="space-y-3 text-sm text-gray-300">
              <div className="flex justify-between">
                <span>Fundamental Frequency:</span>
                <span className="font-mono text-green-400">
                  {harmonicResonance.fundamentalFrequency.toFixed(2)} Hz
                </span>
              </div>
              <div className="flex justify-between">
                <span>Dissonance Level:</span>
                <span className="font-mono text-yellow-400">
                  {(harmonicResonance.dissonanceLevel * 100).toFixed(1)}%
                </span>
              </div>
              <div>
                <div className="text-xs text-gray-400 mb-1">Harmonic Series:</div>
                <div className="flex flex-wrap gap-2">
                  {harmonicResonance.harmonicSeries.map((freq, i) => (
                    <span key={i} className="px-2 py-1 bg-green-900/30 text-green-300 rounded text-xs font-mono">
                      {freq.toFixed(0)} Hz
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Ritual Description */}
          <div className="bg-gradient-to-br from-[#1A1F3C] to-[#0A0F29] rounded-lg p-6 border-2 border-[#FFD700]/40">
            <pre className="text-sm text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
              {ritualDescription}
            </pre>
          </div>
        </div>
      )}

      {/* Status Indicator */}
      <div className="text-center">
        <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-full ${
          isPlaying
            ? 'bg-gradient-to-r from-green-900/50 to-blue-900/50 text-green-300 border-2 border-green-400/50 shadow-lg shadow-green-400/20'
            : 'bg-gray-800/30 text-gray-400 border-2 border-gray-600/50'
        }`}>
          <div className={`w-3 h-3 rounded-full ${isPlaying ? 'bg-green-400 animate-pulse' : 'bg-gray-400'}`} />
          <span className="font-medium">
            {isPlaying ? `Ritual Active · ${currentPhase.toUpperCase()} Phase` : 'Ritual Dormant'}
          </span>
        </div>
      </div>

      {/* Immersive Note */}
      <div className="text-center text-xs text-gray-400 italic space-y-1">
        <div>🎧 Best experienced with headphones for full 360° spatial effect</div>
        <div>⭐ Visual constellation map synchronized with soundscape positions</div>
        <div>🔥 Each engine's health radiates from its cosmic position</div>
      </div>
    </div>
  );
}
