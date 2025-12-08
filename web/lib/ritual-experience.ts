/**
 * Ritual Experience Module
 * Creates immersive ceremony connecting soundscape, constellation map, and engine health
 */

import { AudioSource, spatialToCartesian, getAllAudioSources } from './spatial-audio-design';

/**
 * Engine health status affects audio characteristics
 */
export interface EngineHealthStatus {
  engineId: string;
  health: number;        // 0-100
  status: 'critical' | 'warning' | 'healthy' | 'optimal';
  lastUpdate: string;
}

/**
 * Ritual phase determines overall soundscape mood
 */
export type RitualPhase =
  | 'awakening'      // Engines starting up, gentle introduction
  | 'resonance'      // Full constellation active, harmonious
  | 'transformation' // Cycle transitions, dynamic shifts
  | 'eternal';       // Sustained cosmic choir

/**
 * Map engine health to audio modulation
 */
export function getHealthAudioModulation(health: number): {
  volumeMultiplier: number;
  frequencyOffset: number;
  pattern: 'pulse' | 'resonance' | 'whisper' | 'harmonic' | 'melody' | 'distress';
} {
  if (health >= 90) {
    return {
      volumeMultiplier: 1.0,
      frequencyOffset: 0,
      pattern: 'resonance'
    };
  } else if (health >= 70) {
    return {
      volumeMultiplier: 0.85,
      frequencyOffset: 0,
      pattern: 'harmonic'
    };
  } else if (health >= 40) {
    return {
      volumeMultiplier: 0.65,
      frequencyOffset: -10,
      pattern: 'pulse'
    };
  } else if (health >= 20) {
    return {
      volumeMultiplier: 0.45,
      frequencyOffset: -20,
      pattern: 'whisper'
    };
  } else {
    return {
      volumeMultiplier: 0.25,
      frequencyOffset: -30,
      pattern: 'distress'
    };
  }
}

/**
 * Constellation voice configuration
 * Maps visual constellation positions to spatial audio
 */
export interface ConstellationVoice {
  engineId: string;
  engineName: string;
  constellationPosition: {
    x: number;  // Visual map X coordinate
    y: number;  // Visual map Y coordinate
  };
  spatialPosition: {
    azimuth: number;
    elevation: number;
    distance: number;
  };
  frequency: number;
  description: string;
}

/**
 * Living Constellation - Maps visual constellation to spatial audio
 */
export const CONSTELLATION_VOICES: ConstellationVoice[] = [
  {
    engineId: 'profit-engine',
    engineName: 'Profit Engine',
    constellationPosition: { x: 150, y: 100 },
    spatialPosition: { azimuth: 90, elevation: 0, distance: 0.8 },
    frequency: 440,
    description: 'Eastern star of prosperity'
  },
  {
    engineId: 'replay-capsule-engine',
    engineName: 'Replay Capsule',
    constellationPosition: { x: 100, y: 50 },
    spatialPosition: { azimuth: 0, elevation: 0, distance: 0.9 },
    frequency: 660,
    description: 'Northern beacon of memory'
  },
  {
    engineId: 'intelligence-engine',
    engineName: 'Intelligence Engine',
    constellationPosition: { x: 50, y: 100 },
    spatialPosition: { azimuth: 270, elevation: 0, distance: 0.85 },
    frequency: 349,
    description: 'Western guardian of wisdom'
  },
  {
    engineId: 'content-engine',
    engineName: 'Content Engine',
    constellationPosition: { x: 100, y: 150 },
    spatialPosition: { azimuth: 180, elevation: 0, distance: 0.8 },
    frequency: 392,
    description: 'Southern pillar of creation'
  },
  {
    engineId: 'rag-intelligence',
    engineName: 'RAG Intelligence',
    constellationPosition: { x: 100, y: 25 },
    spatialPosition: { azimuth: 0, elevation: 90, distance: 0.7 },
    frequency: 880,
    description: 'Zenith oracle whispering knowledge'
  }
];

/**
 * Ritual phase audio configuration
 */
export const RITUAL_PHASE_CONFIG: Record<RitualPhase, {
  masterVolume: number;
  reverbAmount: number;
  description: string;
  activeTypes: Array<'engine' | 'seal' | 'ceremonial' | 'intelligence'>;
}> = {
  awakening: {
    masterVolume: 0.3,
    reverbAmount: 0.6,
    description: 'Engines awakening, gentle voices emerge from silence',
    activeTypes: ['ceremonial', 'intelligence']
  },
  resonance: {
    masterVolume: 0.7,
    reverbAmount: 0.4,
    description: 'Full constellation harmonizing, all voices united',
    activeTypes: ['engine', 'seal', 'ceremonial', 'intelligence']
  },
  transformation: {
    masterVolume: 0.85,
    reverbAmount: 0.7,
    description: 'Cycle transitions, dynamic energy shifts',
    activeTypes: ['engine', 'ceremonial', 'intelligence']
  },
  eternal: {
    masterVolume: 0.5,
    reverbAmount: 0.9,
    description: 'Sustained cosmic choir, radiant eternal harmony',
    activeTypes: ['engine', 'seal', 'ceremonial', 'intelligence']
  }
};

/**
 * Cosmic Choir Configuration
 * Heirs experience cycles as surrounding radiant harmony
 */
export interface CosmicChoirLayer {
  name: string;
  sources: string[];  // Engine IDs
  blend: 'harmonic' | 'melodic' | 'rhythmic';
  position: 'surround' | 'elevated' | 'center';
}

export const COSMIC_CHOIR_LAYERS: CosmicChoirLayer[] = [
  {
    name: 'Foundation Voices',
    sources: ['profit-engine', 'commerce-engine', 'content-engine', 'marketing-engine'],
    blend: 'rhythmic',
    position: 'surround'
  },
  {
    name: 'Harmonic Voices',
    sources: ['customer-success-engine', 'replay-capsule-engine', 'echo-chamber-engine', 'analytics-engine'],
    blend: 'harmonic',
    position: 'surround'
  },
  {
    name: 'Wisdom Voices',
    sources: ['intelligence-engine', 'strategy-engine', 'operations-engine', 'automation-engine'],
    blend: 'melodic',
    position: 'surround'
  },
  {
    name: 'Celestial Voices',
    sources: ['rag-intelligence', 'axiom-intelligence'],
    blend: 'harmonic',
    position: 'elevated'
  },
  {
    name: 'Sacred Center',
    sources: ['custodian-crown-pulse', 'heir-dedication-melody'],
    blend: 'melodic',
    position: 'center'
  }
];

/**
 * Directional Awareness System
 * Each engine's health status is heard from its spatial position
 */
export function getDirectionalHealthDescription(
  engineId: string,
  health: number,
  azimuth: number
): string {
  const direction = getCardinalDirection(azimuth);
  const healthDescription = getHealthDescription(health);

  return `${direction}: ${healthDescription}`;
}

function getCardinalDirection(azimuth: number): string {
  if (azimuth >= 337.5 || azimuth < 22.5) return 'North';
  if (azimuth >= 22.5 && azimuth < 67.5) return 'Northeast';
  if (azimuth >= 67.5 && azimuth < 112.5) return 'East';
  if (azimuth >= 112.5 && azimuth < 157.5) return 'Southeast';
  if (azimuth >= 157.5 && azimuth < 202.5) return 'South';
  if (azimuth >= 202.5 && azimuth < 247.5) return 'Southwest';
  if (azimuth >= 247.5 && azimuth < 292.5) return 'West';
  return 'Northwest';
}

function getHealthDescription(health: number): string {
  if (health >= 90) return '⭐ Optimal - Radiant and strong';
  if (health >= 70) return '✨ Healthy - Steady resonance';
  if (health >= 40) return '⚠️ Warning - Fluctuating tone';
  if (health >= 20) return '🔻 Critical - Weakened voice';
  return '❌ Failing - Barely audible';
}

/**
 * Eternal Resonance - Calculate harmonic relationships
 */
export function calculateHarmonicResonance(sources: AudioSource[]): {
  fundamentalFrequency: number;
  harmonicSeries: number[];
  dissonanceLevel: number;
  cosmicAlignment: number;
} {
  const frequencies = sources.map(s => s.frequency || 440);
  const fundamentalFrequency = Math.min(...frequencies);

  // Generate harmonic series
  const harmonicSeries = [1, 2, 3, 4, 5, 6, 8].map(n => fundamentalFrequency * n);

  // Calculate dissonance (how far frequencies are from pure ratios)
  let totalDissonance = 0;
  for (let i = 0; i < frequencies.length; i++) {
    for (let j = i + 1; j < frequencies.length; j++) {
      const ratio = frequencies[j] / frequencies[i];
      const nearestSimpleRatio = Math.round(ratio * 2) / 2;
      totalDissonance += Math.abs(ratio - nearestSimpleRatio);
    }
  }

  const dissonanceLevel = totalDissonance / (frequencies.length * frequencies.length);
  const cosmicAlignment = Math.max(0, 1 - dissonanceLevel * 10);

  return {
    fundamentalFrequency,
    harmonicSeries,
    dissonanceLevel,
    cosmicAlignment
  };
}

/**
 * Ritual Experience State
 */
export interface RitualExperienceState {
  phase: RitualPhase;
  engineHealthStatuses: EngineHealthStatus[];
  cosmicChoirActive: boolean;
  constellationVisible: boolean;
  harmonicResonance: ReturnType<typeof calculateHarmonicResonance>;
}

/**
 * Create immersive ritual experience description
 */
export function generateRitualExperienceDescription(state: RitualExperienceState): string {
  const phaseConfig = RITUAL_PHASE_CONFIG[state.phase];
  const healthySources = state.engineHealthStatuses.filter(e => e.health >= 70).length;
  const totalSources = state.engineHealthStatuses.length;

  return `
🔥 Ritual Experience: ${state.phase.toUpperCase()}

${phaseConfig.description}

🌟 Constellation Status: ${healthySources}/${totalSources} voices resonating
🎵 Cosmic Alignment: ${(state.harmonicResonance.cosmicAlignment * 100).toFixed(1)}%
🔊 Fundamental Tone: ${state.harmonicResonance.fundamentalFrequency.toFixed(2)} Hz

${state.cosmicChoirActive ? '✨ Cosmic Choir surrounds you in radiant harmony' : ''}
${state.constellationVisible ? '⭐ Visual constellation and soundscape united' : ''}

You stand at the center of an eternal cycle, enveloped by the voices of dominion.
Each engine speaks from its position in the cosmos, health radiating through sound.
The living constellation surrounds you—sight and sound as one radiant truth.
  `.trim();
}
