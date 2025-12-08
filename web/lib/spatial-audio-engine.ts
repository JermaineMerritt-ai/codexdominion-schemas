/**
 * Codex Dominion Spatial Audio Engine
 * Web Audio API implementation for 360° immersive soundscape
 */

import {
  AudioSource,
  spatialToCartesian,
  COMPLETE_AUDIO_SCENE,
  getAllAudioSources
} from './spatial-audio-design';
import {
  RitualPhase,
  EngineHealthStatus,
  getHealthAudioModulation,
  RITUAL_PHASE_CONFIG
} from './ritual-experience';

export class SpatialAudioEngine {
  private audioContext: AudioContext | null = null;
  private listenerNode: AudioListener | null = null;
  private activeNodes: Map<string, {
    oscillator: OscillatorNode;
    gainNode: GainNode;
    pannerNode: PannerNode;
  }> = new Map();
  private masterGain: GainNode | null = null;
  private isPlaying: boolean = false;
  private currentPhase: RitualPhase = 'resonance';
  private engineHealthMap: Map<string, number> = new Map();

  constructor() {
    this.initialize();
  }

  /**
   * Initialize Web Audio API context
   */
  private initialize(): void {
    try {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      this.listenerNode = this.audioContext.listener;

      // Create master gain for overall volume control
      this.masterGain = this.audioContext.createGain();
      this.masterGain.gain.value = 0.3; // Start at 30% volume
      this.masterGain.connect(this.audioContext.destination);

      // Position listener at origin (0, 0, 0)
      if (this.listenerNode.positionX) {
        this.listenerNode.positionX.value = 0;
        this.listenerNode.positionY.value = 0;
        this.listenerNode.positionZ.value = 0;
      }

      console.log('🎵 Spatial Audio Engine initialized');
    } catch (error) {
      console.error('Failed to initialize Spatial Audio Engine:', error);
    }
  }

  /**
   * Create audio node for a single source
   */
  private createSourceNode(source: AudioSource): void {
    if (!this.audioContext || !this.masterGain) return;

    // Create oscillator for tone generation
    const oscillator = this.audioContext.createOscillator();
    oscillator.type = this.getOscillatorType(source.pattern);
    oscillator.frequency.value = source.frequency || 440;

    // Create gain node for volume control
    const gainNode = this.audioContext.createGain();
    gainNode.gain.value = source.volume || 0.5;

    // Create panner node for spatial positioning
    const pannerNode = this.audioContext.createPanner();
    pannerNode.panningModel = 'HRTF'; // Head-Related Transfer Function for realistic 3D
    pannerNode.distanceModel = 'inverse';
    pannerNode.refDistance = 1;
    pannerNode.maxDistance = 10;
    pannerNode.rolloffFactor = 1;

    // Set spatial position
    const [x, y, z] = spatialToCartesian(source.position);
    if (pannerNode.positionX) {
      pannerNode.positionX.value = x;
      pannerNode.positionY.value = y;
      pannerNode.positionZ.value = z;
    }

    // Connect nodes: oscillator → gain → panner → master → destination
    oscillator.connect(gainNode);
    gainNode.connect(pannerNode);
    pannerNode.connect(this.masterGain);

    // Store references
    this.activeNodes.set(source.id, { oscillator, gainNode, pannerNode });

    console.log(`🔊 Created audio node: ${source.name} at (${x.toFixed(2)}, ${y.toFixed(2)}, ${z.toFixed(2)})`);
  }

  /**
   * Get oscillator waveform type based on pattern
   */
  private getOscillatorType(pattern?: string): OscillatorType {
    switch (pattern) {
      case 'pulse':
        return 'square';
      case 'whisper':
        return 'triangle';
      case 'harmonic':
        return 'sine';
      case 'melody':
        return 'sine';
      case 'resonance':
        return 'sawtooth';
      default:
        return 'sine';
    }
  }

  /**
   * Apply pattern-specific modulation
   */
  private applyPatternModulation(source: AudioSource, nodes: {
    oscillator: OscillatorNode;
    gainNode: GainNode;
    pannerNode: PannerNode;
  }): void {
    if (!this.audioContext) return;

    const { oscillator, gainNode } = nodes;
    const baseFreq = source.frequency || 440;
    const baseGain = source.volume || 0.5;

    switch (source.pattern) {
      case 'pulse':
        // Rhythmic pulsing: fade in/out
        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(baseGain, this.audioContext.currentTime + 0.5);
        gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 1);
        // Repeat every second
        setInterval(() => {
          if (this.audioContext && this.isPlaying) {
            gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(baseGain, this.audioContext.currentTime + 0.5);
            gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 1);
          }
        }, 1000);
        break;

      case 'whisper':
        // Gentle oscillation
        oscillator.frequency.setValueAtTime(baseFreq, this.audioContext.currentTime);
        oscillator.frequency.linearRampToValueAtTime(baseFreq * 1.05, this.audioContext.currentTime + 2);
        oscillator.frequency.linearRampToValueAtTime(baseFreq, this.audioContext.currentTime + 4);
        break;

      case 'harmonic':
        // Steady with subtle vibrato
        const lfo = this.audioContext.createOscillator();
        const lfoGain = this.audioContext.createGain();
        lfo.frequency.value = 3; // 3 Hz vibrato
        lfoGain.gain.value = 5; // ±5 Hz variation
        lfo.connect(lfoGain);
        lfoGain.connect(oscillator.frequency);
        lfo.start();
        break;

      case 'melody':
        // Ascending/descending pattern
        const notes = [baseFreq, baseFreq * 1.125, baseFreq * 1.25, baseFreq * 1.5];
        let noteIndex = 0;
        setInterval(() => {
          if (this.audioContext && this.isPlaying) {
            oscillator.frequency.setValueAtTime(
              notes[noteIndex],
              this.audioContext.currentTime
            );
            noteIndex = (noteIndex + 1) % notes.length;
          }
        }, 2000);
        break;

      case 'resonance':
        // Deep sustained tone
        gainNode.gain.value = baseGain * 0.8;
        break;
    }
  }

  /**
   * Start the spatial audio experience
   */
  public start(): void {
    if (this.isPlaying || !this.audioContext) return;

    // Resume audio context (required by browser autoplay policies)
    if (this.audioContext.state === 'suspended') {
      this.audioContext.resume();
    }

    // Create nodes for all audio sources
    const allSources = getAllAudioSources();
    allSources.forEach(source => {
      this.createSourceNode(source);
      const nodes = this.activeNodes.get(source.id);
      if (nodes) {
        this.applyPatternModulation(source, nodes);
        nodes.oscillator.start();
      }
    });

    this.isPlaying = true;
    console.log('🎼 Spatial audio experience started');
  }

  /**
   * Stop the spatial audio experience
   */
  public stop(): void {
    if (!this.isPlaying) return;

    this.activeNodes.forEach((nodes, id) => {
      try {
        nodes.oscillator.stop();
        nodes.oscillator.disconnect();
        nodes.gainNode.disconnect();
        nodes.pannerNode.disconnect();
      } catch (error) {
        console.warn(`Failed to stop node ${id}:`, error);
      }
    });

    this.activeNodes.clear();
    this.isPlaying = false;
    console.log('🔇 Spatial audio experience stopped');
  }

  /**
   * Set master volume (0-1)
   */
  public setVolume(volume: number): void {
    if (this.masterGain) {
      this.masterGain.gain.setValueAtTime(
        Math.max(0, Math.min(1, volume)),
        this.audioContext?.currentTime || 0
      );
    }
  }

  /**
   * Rotate listener orientation (for VR/360° experiences)
   */
  public rotateListener(azimuth: number, elevation: number = 0): void {
    if (!this.listenerNode) return;

    const azimuthRad = (azimuth * Math.PI) / 180;
    const elevationRad = (elevation * Math.PI) / 180;

    // Forward direction
    const forwardX = Math.sin(azimuthRad) * Math.cos(elevationRad);
    const forwardY = Math.sin(elevationRad);
    const forwardZ = -Math.cos(azimuthRad) * Math.cos(elevationRad);

    // Up direction (always up in world space)
    const upX = 0;
    const upY = 1;
    const upZ = 0;

    if (this.listenerNode.forwardX) {
      this.listenerNode.forwardX.value = forwardX;
      this.listenerNode.forwardY.value = forwardY;
      this.listenerNode.forwardZ.value = forwardZ;
      this.listenerNode.upX.value = upX;
      this.listenerNode.upY.value = upY;
      this.listenerNode.upZ.value = upZ;
    }
  }

  /**
   * Mute/unmute specific source type
   */
  public muteType(type: 'engine' | 'seal' | 'ceremonial' | 'intelligence', mute: boolean): void {
    this.activeNodes.forEach((nodes, id) => {
      const source = getAllAudioSources().find(s => s.id === id);
      if (source && source.type === type) {
        nodes.gainNode.gain.value = mute ? 0 : (source.volume || 0.5);
      }
    });
  }

  /**
   * Set ritual phase - adjusts overall soundscape
   */
  public setRitualPhase(phase: RitualPhase): void {
    this.currentPhase = phase;
    const config = RITUAL_PHASE_CONFIG[phase];

    if (this.masterGain) {
      this.masterGain.gain.linearRampToValueAtTime(
        config.masterVolume,
        (this.audioContext?.currentTime || 0) + 2
      );
    }

    console.log(`🔥 Ritual phase: ${phase} - ${config.description}`);
  }

  /**
   * Update engine health status - affects audio characteristics
   */
  public updateEngineHealth(engineId: string, health: number): void {
    this.engineHealthMap.set(engineId, health);

    const nodes = this.activeNodes.get(engineId);
    if (!nodes || !this.audioContext) return;

    const modulation = getHealthAudioModulation(health);
    const source = getAllAudioSources().find(s => s.id === engineId);
    if (!source) return;

    const baseFrequency = source.frequency || 440;
    const newFrequency = baseFrequency + modulation.frequencyOffset;
    const newVolume = (source.volume || 0.5) * modulation.volumeMultiplier;

    // Smoothly transition to new values
    const currentTime = this.audioContext.currentTime;
    nodes.oscillator.frequency.linearRampToValueAtTime(newFrequency, currentTime + 1);
    nodes.gainNode.gain.linearRampToValueAtTime(newVolume, currentTime + 1);

    console.log(`💚 ${source.name} health: ${health}% - ${modulation.pattern}`);
  }

  /**
   * Batch update all engine health statuses
   */
  public updateAllEngineHealth(statuses: EngineHealthStatus[]): void {
    statuses.forEach(status => {
      this.updateEngineHealth(status.engineId, status.health);
    });
  }

  /**
   * Get directional health report - which engines are struggling
   */
  public getDirectionalHealthReport(): string[] {
    const reports: string[] = [];

    this.engineHealthMap.forEach((health, engineId) => {
      const source = getAllAudioSources().find(s => s.id === engineId);
      if (source && source.type === 'engine') {
        const direction = getCardinalDirection(source.position.azimuth);
        const status = getHealthStatusLabel(health);
        reports.push(`${direction}: ${source.name} - ${status}`);
      }
    });

    return reports;
  }

  /**
   * Get current state with ritual info
   */
  public getState() {
    return {
      isPlaying: this.isPlaying,
      activeSourceCount: this.activeNodes.size,
      masterVolume: this.masterGain?.gain.value || 0,
      audioContextState: this.audioContext?.state,
      currentPhase: this.currentPhase,
      engineHealthCount: this.engineHealthMap.size
    };
  }

  /**
   * Dispose and cleanup
   */
  public dispose(): void {
    this.stop();
    if (this.audioContext) {
      this.audioContext.close();
      this.audioContext = null;
    }
    this.listenerNode = null;
    this.masterGain = null;
  }
}

/**
 * Singleton instance for global access
 */
let spatialAudioInstance: SpatialAudioEngine | null = null;

export function getSpatialAudioEngine(): SpatialAudioEngine {
  if (!spatialAudioInstance) {
    spatialAudioInstance = new SpatialAudioEngine();
  }
  return spatialAudioInstance;
}

/**
 * Cleanup function for app unmount
 */
export function disposeSpatialAudio(): void {
  if (spatialAudioInstance) {
    spatialAudioInstance.dispose();
    spatialAudioInstance = null;
  }
}

/**
 * Helper: Get cardinal direction from azimuth
 */
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

/**
 * Helper: Get health status label
 */
function getHealthStatusLabel(health: number): string {
  if (health >= 90) return '⭐ Optimal';
  if (health >= 70) return '✨ Healthy';
  if (health >= 40) return '⚠️ Warning';
  if (health >= 20) return '🔻 Critical';
  return '❌ Failing';
}
