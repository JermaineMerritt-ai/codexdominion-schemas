/**
 * Codex Dominion Spatial Audio Design System
 * 360° immersive soundscape for engines, seals, and ceremonial elements
 */

export interface SpatialPosition {
  azimuth: number;      // Horizontal angle in degrees (0-360)
  elevation: number;    // Vertical angle in degrees (-90 to 90)
  distance: number;     // Distance from center (0-1, where 1 is max)
  label: string;        // Human-readable position description
}

export interface AudioSource {
  id: string;
  name: string;
  type: 'engine' | 'seal' | 'ceremonial' | 'intelligence';
  position: SpatialPosition;
  frequency?: number;   // Hz - base frequency for tone generation
  pattern?: 'pulse' | 'resonance' | 'whisper' | 'harmonic' | 'melody';
  volume?: number;      // 0-1
}

/**
 * 16 Core Engines + Intelligence Engines
 * Positioned in 360° sound field with spatial characteristics
 */
export const ENGINE_AUDIO_MAP: Record<string, AudioSource> = {
  // East Quadrant (0° - 90°)
  'profit-engine': {
    id: 'profit-engine',
    name: 'Profit Engine',
    type: 'engine',
    position: {
      azimuth: 90,      // Due east
      elevation: 0,
      distance: 0.8,
      label: 'East - Ground Level'
    },
    frequency: 440,     // A4 - Prosperity tone
    pattern: 'resonance',
    volume: 0.7
  },

  'customer-success-engine': {
    id: 'customer-success-engine',
    name: 'Customer Success Engine',
    type: 'engine',
    position: {
      azimuth: 67.5,    // East-northeast
      elevation: 15,
      distance: 0.75,
      label: 'East-Northeast - Elevated'
    },
    frequency: 523,     // C5 - Service harmony
    pattern: 'harmonic',
    volume: 0.65
  },

  'commerce-engine': {
    id: 'commerce-engine',
    name: 'Commerce Engine',
    type: 'engine',
    position: {
      azimuth: 112.5,   // East-southeast
      elevation: -10,
      distance: 0.8,
      label: 'East-Southeast - Slightly Below'
    },
    frequency: 392,     // G4 - Exchange rhythm
    pattern: 'pulse',
    volume: 0.7
  },

  'marketing-engine': {
    id: 'marketing-engine',
    name: 'Marketing Engine',
    type: 'engine',
    position: {
      azimuth: 45,      // Northeast
      elevation: 20,
      distance: 0.85,
      label: 'Northeast - Elevated'
    },
    frequency: 587,     // D5 - Broadcast frequency
    pattern: 'resonance',
    volume: 0.68
  },

  // North Quadrant (270° - 360°/0°)
  'replay-capsule-engine': {
    id: 'replay-capsule-engine',
    name: 'Replay Capsule Engine',
    type: 'engine',
    position: {
      azimuth: 0,       // Due north
      elevation: 0,
      distance: 0.9,
      label: 'North - Ground Level'
    },
    frequency: 660,     // E5 - Memory pulse
    pattern: 'pulse',
    volume: 0.75
  },

  'echo-chamber-engine': {
    id: 'echo-chamber-engine',
    name: 'Echo Chamber Engine',
    type: 'engine',
    position: {
      azimuth: 337.5,   // North-northwest
      elevation: -15,
      distance: 0.85,
      label: 'North-Northwest - Below'
    },
    frequency: 294,     // D4 - Echo resonance
    pattern: 'resonance',
    volume: 0.6
  },

  'oracle-engine': {
    id: 'oracle-engine',
    name: 'Oracle Engine',
    type: 'engine',
    position: {
      azimuth: 22.5,    // North-northeast
      elevation: 30,
      distance: 0.8,
      label: 'North-Northeast - Highly Elevated'
    },
    frequency: 784,     // G5 - Prophecy tone
    pattern: 'harmonic',
    volume: 0.7
  },

  'analytics-engine': {
    id: 'analytics-engine',
    name: 'Analytics Engine',
    type: 'engine',
    position: {
      azimuth: 315,     // Northwest
      elevation: 10,
      distance: 0.75,
      label: 'Northwest - Elevated'
    },
    frequency: 494,     // B4 - Analysis frequency
    pattern: 'pulse',
    volume: 0.65
  },

  // West Quadrant (180° - 270°)
  'intelligence-engine': {
    id: 'intelligence-engine',
    name: 'Intelligence Engine',
    type: 'engine',
    position: {
      azimuth: 270,     // Due west
      elevation: 0,
      distance: 0.8,
      label: 'West - Ground Level'
    },
    frequency: 349,     // F4 - Wisdom tone
    pattern: 'resonance',
    volume: 0.72
  },

  'strategy-engine': {
    id: 'strategy-engine',
    name: 'Strategy Engine',
    type: 'engine',
    position: {
      azimuth: 247.5,   // West-southwest
      elevation: 15,
      distance: 0.85,
      label: 'West-Southwest - Elevated'
    },
    frequency: 440,     // A4 - Planning harmony
    pattern: 'harmonic',
    volume: 0.68
  },

  'operations-engine': {
    id: 'operations-engine',
    name: 'Operations Engine',
    type: 'engine',
    position: {
      azimuth: 292.5,   // West-northwest
      elevation: -5,
      distance: 0.75,
      label: 'West-Northwest - Slightly Below'
    },
    frequency: 330,     // E4 - Operations rhythm
    pattern: 'pulse',
    volume: 0.7
  },

  'automation-engine': {
    id: 'automation-engine',
    name: 'Automation Engine',
    type: 'engine',
    position: {
      azimuth: 225,     // Southwest
      elevation: 0,
      distance: 0.8,
      label: 'Southwest - Ground Level'
    },
    frequency: 523,     // C5 - Automation pulse
    pattern: 'pulse',
    volume: 0.65
  },

  // South Quadrant (90° - 180°)
  'content-engine': {
    id: 'content-engine',
    name: 'Content Engine',
    type: 'engine',
    position: {
      azimuth: 180,     // Due south
      elevation: 0,
      distance: 0.85,
      label: 'South - Ground Level'
    },
    frequency: 392,     // G4 - Creation tone
    pattern: 'harmonic',
    volume: 0.7
  },

  'social-engine': {
    id: 'social-engine',
    name: 'Social Engine',
    type: 'engine',
    position: {
      azimuth: 157.5,   // South-southeast
      elevation: 10,
      distance: 0.75,
      label: 'South-Southeast - Elevated'
    },
    frequency: 587,     // D5 - Community frequency
    pattern: 'resonance',
    volume: 0.68
  },

  'innovation-engine': {
    id: 'innovation-engine',
    name: 'Innovation Engine',
    type: 'engine',
    position: {
      azimuth: 202.5,   // South-southwest
      elevation: 20,
      distance: 0.8,
      label: 'South-Southwest - Elevated'
    },
    frequency: 660,     // E5 - Innovation spark
    pattern: 'pulse',
    volume: 0.72
  },

  'growth-engine': {
    id: 'growth-engine',
    name: 'Growth Engine',
    type: 'engine',
    position: {
      azimuth: 135,     // Southeast
      elevation: 5,
      distance: 0.85,
      label: 'Southeast - Slightly Elevated'
    },
    frequency: 494,     // B4 - Expansion tone
    pattern: 'resonance',
    volume: 0.7
  },

  // Intelligence Engines (Above)
  'rag-intelligence': {
    id: 'rag-intelligence',
    name: 'RAG Intelligence',
    type: 'intelligence',
    position: {
      azimuth: 0,       // Directly above
      elevation: 90,
      distance: 0.6,
      label: 'Zenith - Above Center'
    },
    frequency: 880,     // A5 - Knowledge whisper
    pattern: 'whisper',
    volume: 0.5
  },

  'axiom-intelligence': {
    id: 'axiom-intelligence',
    name: 'Axiom Intelligence',
    type: 'intelligence',
    position: {
      azimuth: 180,     // Behind and above
      elevation: 75,
      distance: 0.65,
      label: 'High Southern - Above Rear'
    },
    frequency: 784,     // G5 - Truth resonance
    pattern: 'whisper',
    volume: 0.52
  }
};

/**
 * Ceremonial Audio Elements
 * Center channel and surround positions for seals and dedication
 */
export const CEREMONIAL_AUDIO: Record<string, AudioSource> = {
  'custodian-crown-pulse': {
    id: 'custodian-crown-pulse',
    name: 'Custodian Crown Heartbeat',
    type: 'ceremonial',
    position: {
      azimuth: 0,
      elevation: 0,
      distance: 0,      // Center channel
      label: 'Center - Sovereign Anchor'
    },
    frequency: 261.63,  // C4 - Middle C, steady foundation
    pattern: 'pulse',
    volume: 0.8
  },

  'heir-dedication-melody': {
    id: 'heir-dedication-melody',
    name: 'Heir Dedication Melody',
    type: 'ceremonial',
    position: {
      azimuth: 180,     // Behind listener
      elevation: 45,    // Above and behind
      distance: 0.5,
      label: 'Rear Elevated - Enveloping'
    },
    frequency: 523.25,  // C5 - Octave above foundation
    pattern: 'melody',
    volume: 0.6
  }
};

/**
 * Council Seal Harmonics
 * Orbiting surround channels with harmonic frequencies
 */
export const COUNCIL_SEAL_AUDIO: AudioSource[] = [
  {
    id: 'council-seal-1',
    name: 'Elena Rodriguez Seal',
    type: 'seal',
    position: {
      azimuth: 45,
      elevation: 10,
      distance: 0.7,
      label: 'Northeast Surround'
    },
    frequency: 329.63,  // E4 - First harmony
    pattern: 'harmonic',
    volume: 0.55
  },
  {
    id: 'council-seal-2',
    name: 'Marcus Chen Seal',
    type: 'seal',
    position: {
      azimuth: 135,
      elevation: 10,
      distance: 0.7,
      label: 'Southeast Surround'
    },
    frequency: 392.00,  // G4 - Second harmony
    pattern: 'harmonic',
    volume: 0.55
  },
  {
    id: 'council-seal-3',
    name: 'Aisha Patel Seal',
    type: 'seal',
    position: {
      azimuth: 225,
      elevation: 10,
      distance: 0.7,
      label: 'Southwest Surround'
    },
    frequency: 440.00,  // A4 - Third harmony
    pattern: 'harmonic',
    volume: 0.55
  },
  {
    id: 'council-seal-4',
    name: 'Dmitri Volkov Seal',
    type: 'seal',
    position: {
      azimuth: 315,
      elevation: 10,
      distance: 0.7,
      label: 'Northwest Surround'
    },
    frequency: 493.88,  // B4 - Fourth harmony
    pattern: 'harmonic',
    volume: 0.55
  },
  {
    id: 'council-seal-5',
    name: 'Sofia Ramirez Seal',
    type: 'seal',
    position: {
      azimuth: 180,
      elevation: 20,
      distance: 0.65,
      label: 'Rear Elevated'
    },
    frequency: 523.25,  // C5 - Fifth harmony (octave)
    pattern: 'harmonic',
    volume: 0.58
  }
];

/**
 * Complete Spatial Audio Scene
 * All sources combined for immersive experience
 */
export const COMPLETE_AUDIO_SCENE = {
  engines: ENGINE_AUDIO_MAP,
  ceremonial: CEREMONIAL_AUDIO,
  councilSeals: COUNCIL_SEAL_AUDIO
};

/**
 * Utility: Get audio source by engine name
 */
export function getEngineAudioSource(engineName: string): AudioSource | undefined {
  const normalizedName = engineName.toLowerCase().replace(/\s+/g, '-');
  return ENGINE_AUDIO_MAP[normalizedName];
}

/**
 * Utility: Calculate 3D position from spatial coordinates
 * Returns [x, y, z] for Web Audio API positioning
 */
export function spatialToCartesian(position: SpatialPosition): [number, number, number] {
  const azimuthRad = (position.azimuth * Math.PI) / 180;
  const elevationRad = (position.elevation * Math.PI) / 180;
  const distance = position.distance;

  const x = distance * Math.cos(elevationRad) * Math.sin(azimuthRad);
  const y = distance * Math.sin(elevationRad);
  const z = -distance * Math.cos(elevationRad) * Math.cos(azimuthRad);

  return [x, y, z];
}

/**
 * Utility: Get all active audio sources
 */
export function getAllAudioSources(): AudioSource[] {
  return [
    ...Object.values(ENGINE_AUDIO_MAP),
    ...Object.values(CEREMONIAL_AUDIO),
    ...COUNCIL_SEAL_AUDIO
  ];
}

/**
 * Utility: Filter sources by type
 */
export function getSourcesByType(
  type: 'engine' | 'seal' | 'ceremonial' | 'intelligence'
): AudioSource[] {
  return getAllAudioSources().filter(source => source.type === type);
}

/**
 * Spatial Audio Scene Metadata
 */
export const SCENE_METADATA = {
  totalSources: getAllAudioSources().length,
  engineCount: Object.keys(ENGINE_AUDIO_MAP).length,
  sealCount: COUNCIL_SEAL_AUDIO.length,
  ceremonialCount: Object.keys(CEREMONIAL_AUDIO).length,

  description: `
    Codex Dominion Spatial Audio Experience:
    - 16 Core Engines + 2 Intelligence Engines positioned in 360° field
    - Custodian Crown Pulse anchors center channel (C4 at 261.63 Hz)
    - 5 Council Seals emit harmonics in surround configuration
    - Heir Dedication Melody envelops from above and behind (C5 at 523.25 Hz)
    - RAG Intelligence whispers from zenith (A5 at 880 Hz)
    - Complete immersive soundscape for ceremonial exports
  `.trim(),

  frequencyRange: {
    lowest: 261.63,   // C4 - Custodian pulse
    highest: 880,     // A5 - RAG whisper
    span: '2.5 octaves'
  },

  spatialCoverage: '360° horizontal × 180° vertical (full sphere)'
};
