/**
 * WebSocket Manager for Multi-Audience Broadcast
 * Handles synchronized replay capsule events and constellation state
 */

export type BroadcastRole = 'sovereign' | 'council' | 'heir' | 'observer';

export interface BroadcastMessage {
  type: 'capsule_sync' | 'constellation_update' | 'playback_control' | 'role_assignment' | 'heartbeat';
  timestamp: string;
  payload: any;
  senderId?: string;
  role?: BroadcastRole;
}

export interface CapsuleSync {
  index: number;
  capsule: {
    id: string;
    timestamp: string;
    engine: string;
    status: 'operational' | 'degraded' | 'failed';
    message: string;
    metadata?: Record<string, any>;
  };
  isPlaying: boolean;
  mode: 'daily' | 'seasonal' | 'epochal' | 'millennial';
}

export interface ConstellationUpdate {
  highlightedEngine: string;
  status: 'operational' | 'degraded' | 'failed';
  nodePositions?: Record<string, { x: number; y: number }>;
}

export interface PlaybackControl {
  action: 'play' | 'pause' | 'seek' | 'reset' | 'fast_forward' | 'rewind';
  targetIndex?: number;
  speed?: number;
}

export class BroadcastWebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private messageHandlers: Map<string, Set<(msg: BroadcastMessage) => void>> = new Map();
  private clientId: string;
  private role: BroadcastRole = 'observer';
  private isConnected = false;
  private wsUrl: string;

  constructor(wsUrl: string, clientId?: string) {
    this.wsUrl = wsUrl;
    this.clientId = clientId || this.generateClientId();
  }

  private generateClientId(): string {
    return `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  connect(role: BroadcastRole = 'observer'): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.role = role;
        this.ws = new WebSocket(`${this.wsUrl}?clientId=${this.clientId}&role=${role}`);

        this.ws.onopen = () => {
          console.log('🔥 Broadcast WebSocket connected as', role);
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.startHeartbeat();
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: BroadcastMessage = JSON.parse(event.data);
            this.handleMessage(message);
          } catch (error) {
            console.error('❌ Failed to parse broadcast message:', error);
          }
        };

        this.ws.onerror = (error) => {
          console.error('❌ Broadcast WebSocket error:', error);
          reject(error);
        };

        this.ws.onclose = () => {
          console.log('🔌 Broadcast WebSocket disconnected');
          this.isConnected = false;
          this.stopHeartbeat();
          this.attemptReconnect();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect(): void {
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    console.log(`🔄 Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    setTimeout(() => {
      this.connect(this.role).catch((error) => {
        console.error('❌ Reconnection failed:', error);
      });
    }, this.reconnectDelay * this.reconnectAttempts);
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      this.send({
        type: 'heartbeat',
        timestamp: new Date().toISOString(),
        payload: { clientId: this.clientId },
      });
    }, 30000); // Every 30 seconds
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  private handleMessage(message: BroadcastMessage): void {
    // Notify specific type handlers
    const handlers = this.messageHandlers.get(message.type);
    if (handlers) {
      handlers.forEach((handler) => handler(message));
    }

    // Notify wildcard handlers
    const wildcardHandlers = this.messageHandlers.get('*');
    if (wildcardHandlers) {
      wildcardHandlers.forEach((handler) => handler(message));
    }
  }

  on(messageType: string, handler: (msg: BroadcastMessage) => void): () => void {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, new Set());
    }
    this.messageHandlers.get(messageType)!.add(handler);

    // Return unsubscribe function
    return () => {
      const handlers = this.messageHandlers.get(messageType);
      if (handlers) {
        handlers.delete(handler);
      }
    };
  }

  send(message: Omit<BroadcastMessage, 'senderId' | 'role'>): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.warn('⚠️ WebSocket not connected, cannot send message');
      return;
    }

    const fullMessage: BroadcastMessage = {
      ...message,
      senderId: this.clientId,
      role: this.role,
    };

    this.ws.send(JSON.stringify(fullMessage));
  }

  // High-level methods for specific broadcast events
  syncCapsule(data: CapsuleSync): void {
    this.send({
      type: 'capsule_sync',
      timestamp: new Date().toISOString(),
      payload: data,
    });
  }

  updateConstellation(data: ConstellationUpdate): void {
    this.send({
      type: 'constellation_update',
      timestamp: new Date().toISOString(),
      payload: data,
    });
  }

  sendPlaybackControl(data: PlaybackControl): void {
    this.send({
      type: 'playback_control',
      timestamp: new Date().toISOString(),
      payload: data,
    });
  }

  getConnectionState(): {
    isConnected: boolean;
    clientId: string;
    role: BroadcastRole;
    reconnectAttempts: number;
  } {
    return {
      isConnected: this.isConnected,
      clientId: this.clientId,
      role: this.role,
      reconnectAttempts: this.reconnectAttempts,
    };
  }
}
