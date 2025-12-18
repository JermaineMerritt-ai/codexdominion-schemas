/**
 * React Hook for Broadcast Synchronization
 * Integrates WebSocket + WebRTC with ReplayContext for multi-audience sync
 */

import { useEffect, useRef, useState } from 'react';
import { useReplay } from '../context/ReplayContext';
import {
  BroadcastWebSocketManager,
  BroadcastRole,
  BroadcastMessage,
  CapsuleSync,
  ConstellationUpdate,
  PlaybackControl,
} from '@/lib/broadcast/websocket-manager';

export interface BroadcastConfig {
  wsUrl: string;
  role: BroadcastRole;
  clientId?: string;
  autoConnect?: boolean;
}

export interface BroadcastState {
  isConnected: boolean;
  connectionState: string;
  clientId: string;
  role: BroadcastRole;
  participantCount: number;
  lastSync: string | null;
}

export function useBroadcastSync(config: BroadcastConfig) {
  const { index, setIndex, capsules, setCapsules, isPlaying, setIsPlaying, mode, setMode } =
    useReplay();

  const wsManagerRef = useRef<BroadcastWebSocketManager | null>(null);
  const [broadcastState, setBroadcastState] = useState<BroadcastState>({
    isConnected: false,
    connectionState: 'disconnected',
    clientId: '',
    role: config.role,
    participantCount: 0,
    lastSync: null,
  });

  const isSovereignRef = useRef(config.role === 'sovereign');

  // Initialize WebSocket connection
  useEffect(() => {
    const manager = new BroadcastWebSocketManager(config.wsUrl, config.clientId);
    wsManagerRef.current = manager;

    if (config.autoConnect !== false) {
      manager.connect(config.role).then(() => {
        const state = manager.getConnectionState();
        setBroadcastState((prev) => ({
          ...prev,
          isConnected: state.isConnected,
          connectionState: 'connected',
          clientId: state.clientId,
        }));
      });
    }

    // Subscribe to capsule sync messages
    const unsubCapsuleSync = manager.on('capsule_sync', (msg: BroadcastMessage) => {
      if (isSovereignRef.current) return; // Sovereign doesn't receive sync, only sends

      const payload = msg.payload as CapsuleSync;
      console.log('🕰️ Received capsule sync:', payload);

      // Update replay state
      setIndex(payload.index);
      setIsPlaying(payload.isPlaying);
      setMode(payload.mode);

      // Optionally update capsules if payload includes new data
      if (payload.capsule) {
        const existing = capsules.find((c) => c.id === payload.capsule.id);
        if (!existing) {
          setCapsules([...capsules, payload.capsule]);
        }
      }

      setBroadcastState((prev) => ({
        ...prev,
        lastSync: new Date().toISOString(),
      }));
    });

    // Subscribe to constellation updates
    const unsubConstellation = manager.on('constellation_update', (msg: BroadcastMessage) => {
      const payload = msg.payload as ConstellationUpdate;
      console.log('🌌 Received constellation update:', payload);
      // Constellation updates are handled by ConstellationMap component
    });

    // Subscribe to playback controls
    const unsubPlayback = manager.on('playback_control', (msg: BroadcastMessage) => {
      if (isSovereignRef.current) return; // Sovereign controls, doesn't receive

      const payload = msg.payload as PlaybackControl;
      console.log('⏯️ Received playback control:', payload);

      switch (payload.action) {
        case 'play':
          setIsPlaying(true);
          break;
        case 'pause':
          setIsPlaying(false);
          break;
        case 'seek':
          if (payload.targetIndex !== undefined) {
            setIndex(payload.targetIndex);
          }
          break;
        case 'reset':
          setIndex(0);
          setIsPlaying(false);
          break;
        case 'fast_forward':
          setIndex((prev: number) => Math.min(prev + 5, capsules.length - 1));
          break;
        case 'rewind':
          setIndex((prev: number) => Math.max(prev - 5, 0));
          break;
      }
    });

    // Cleanup on unmount
    return () => {
      unsubCapsuleSync();
      unsubConstellation();
      unsubPlayback();
      manager.disconnect();
    };
  }, [config.wsUrl, config.clientId, config.role, config.autoConnect]);

  // Sovereign: Broadcast state changes to all participants
  useEffect(() => {
    if (!isSovereignRef.current || !wsManagerRef.current) return;
    if (!broadcastState.isConnected) return;
    if (capsules.length === 0) return;

    const currentCapsule = capsules[index];
    if (!currentCapsule) return;

    // Broadcast capsule sync
    wsManagerRef.current.syncCapsule({
      index,
      capsule: {
        ...currentCapsule,
        status: (currentCapsule.status as 'operational' | 'degraded' | 'failed') || 'operational',
        message: currentCapsule.event || '',
      },
      isPlaying,
      mode,
    });

    // Broadcast constellation update
    wsManagerRef.current.updateConstellation({
      highlightedEngine: currentCapsule.engine,
      status: (currentCapsule.status as 'operational' | 'degraded' | 'failed') || 'operational',
    });

    console.log('📡 Sovereign broadcast sync:', { index, engine: currentCapsule.engine });
  }, [index, isPlaying, mode, capsules, broadcastState.isConnected]);

  // Sovereign: Broadcast playback controls
  const broadcastPlaybackControl = (action: PlaybackControl['action'], targetIndex?: number) => {
    if (!isSovereignRef.current || !wsManagerRef.current) return;

    wsManagerRef.current.sendPlaybackControl({
      action,
      targetIndex,
    });
  };

  const connect = async () => {
    if (!wsManagerRef.current) return;
    await wsManagerRef.current.connect(config.role);
    const state = wsManagerRef.current.getConnectionState();
    setBroadcastState((prev) => ({
      ...prev,
      isConnected: state.isConnected,
      connectionState: 'connected',
      clientId: state.clientId,
    }));
  };

  const disconnect = () => {
    if (!wsManagerRef.current) return;
    wsManagerRef.current.disconnect();
    setBroadcastState((prev) => ({
      ...prev,
      isConnected: false,
      connectionState: 'disconnected',
    }));
  };

  return {
    broadcastState,
    connect,
    disconnect,
    broadcastPlaybackControl,
    isSovereign: isSovereignRef.current,
  };
}
