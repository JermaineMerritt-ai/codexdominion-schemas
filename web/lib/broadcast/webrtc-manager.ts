/**
 * WebRTC Manager for Multi-Audience Broadcast
 * Handles low-latency video + data sync for sovereign broadcast streams
 */

export interface RTCConnectionConfig {
  iceServers: RTCIceServer[];
  iceTransportPolicy?: RTCIceTransportPolicy;
  bundlePolicy?: RTCBundlePolicy;
}

export interface BroadcastStream {
  id: string;
  stream: MediaStream;
  role: 'broadcaster' | 'viewer';
  timestamp: string;
}

export class BroadcastWebRTCManager {
  private peerConnection: RTCPeerConnection | null = null;
  private localStream: MediaStream | null = null;
  private remoteStream: MediaStream | null = null;
  private dataChannel: RTCDataChannel | null = null;
  private config: RTCConnectionConfig;
  private onRemoteStreamCallback?: (stream: MediaStream) => void;
  private onDataChannelMessageCallback?: (data: any) => void;
  private role: 'broadcaster' | 'viewer';

  constructor(
    config?: Partial<RTCConnectionConfig>,
    role: 'broadcaster' | 'viewer' = 'viewer'
  ) {
    this.role = role;
    this.config = {
      iceServers: config?.iceServers || [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' },
      ],
      iceTransportPolicy: config?.iceTransportPolicy || 'all',
      bundlePolicy: config?.bundlePolicy || 'balanced',
    };
  }

  async initializeBroadcaster(constraints?: MediaStreamConstraints): Promise<MediaStream> {
    if (this.role !== 'broadcaster') {
      throw new Error('Cannot initialize broadcaster in viewer mode');
    }

    try {
      // Get local media stream (screen + audio for ceremonial broadcast)
      this.localStream = await navigator.mediaDevices.getDisplayMedia(
        constraints || {
          video: {
            width: { ideal: 1920 },
            height: { ideal: 1080 },
            frameRate: { ideal: 30 },
          },
          audio: true,
        }
      );

      console.log('🎥 Broadcaster stream initialized');
      return this.localStream;
    } catch (error) {
      console.error('❌ Failed to get broadcaster stream:', error);
      throw error;
    }
  }

  async createPeerConnection(): Promise<void> {
    this.peerConnection = new RTCPeerConnection(this.config);

    // Handle ICE candidates
    this.peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        console.log('🧊 ICE candidate:', event.candidate);
        // Send to signaling server
        this.sendToSignalingServer({
          type: 'ice-candidate',
          candidate: event.candidate,
        });
      }
    };

    // Handle connection state changes
    this.peerConnection.onconnectionstatechange = () => {
      console.log('🔗 Connection state:', this.peerConnection?.connectionState);
    };

    // Handle ICE connection state
    this.peerConnection.oniceconnectionstatechange = () => {
      console.log('🧊 ICE connection state:', this.peerConnection?.iceConnectionState);
    };

    // For viewers: handle remote stream
    if (this.role === 'viewer') {
      this.peerConnection.ontrack = (event) => {
        console.log('🎬 Remote stream received');
        this.remoteStream = event.streams[0];
        if (this.onRemoteStreamCallback) {
          this.onRemoteStreamCallback(this.remoteStream);
        }
      };
    }

    // For broadcasters: add local tracks
    if (this.role === 'broadcaster' && this.localStream) {
      this.localStream.getTracks().forEach((track) => {
        this.peerConnection!.addTrack(track, this.localStream!);
      });
    }

    // Create data channel for synchronized replay data
    if (this.role === 'broadcaster') {
      this.dataChannel = this.peerConnection.createDataChannel('broadcast-sync', {
        ordered: true,
      });
      this.setupDataChannel();
    } else {
      // Viewer: wait for data channel from broadcaster
      this.peerConnection.ondatachannel = (event) => {
        this.dataChannel = event.channel;
        this.setupDataChannel();
      };
    }
  }

  private setupDataChannel(): void {
    if (!this.dataChannel) return;

    this.dataChannel.onopen = () => {
      console.log('📡 Data channel opened');
    };

    this.dataChannel.onclose = () => {
      console.log('📴 Data channel closed');
    };

    this.dataChannel.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨 Data channel message:', data);
        if (this.onDataChannelMessageCallback) {
          this.onDataChannelMessageCallback(data);
        }
      } catch (error) {
        console.error('❌ Failed to parse data channel message:', error);
      }
    };
  }

  async createOffer(): Promise<RTCSessionDescriptionInit> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    const offer = await this.peerConnection.createOffer();
    await this.peerConnection.setLocalDescription(offer);
    return offer;
  }

  async createAnswer(): Promise<RTCSessionDescriptionInit> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    const answer = await this.peerConnection.createAnswer();
    await this.peerConnection.setLocalDescription(answer);
    return answer;
  }

  async handleOffer(offer: RTCSessionDescriptionInit): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    await this.peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
  }

  async handleAnswer(answer: RTCSessionDescriptionInit): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    await this.peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
  }

  async addIceCandidate(candidate: RTCIceCandidateInit): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    await this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
  }

  sendData(data: any): void {
    if (!this.dataChannel || this.dataChannel.readyState !== 'open') {
      console.warn('⚠️ Data channel not open, cannot send data');
      return;
    }

    this.dataChannel.send(JSON.stringify(data));
  }

  onRemoteStream(callback: (stream: MediaStream) => void): void {
    this.onRemoteStreamCallback = callback;
  }

  onDataChannelMessage(callback: (data: any) => void): void {
    this.onDataChannelMessageCallback = callback;
  }

  private sendToSignalingServer(message: any): void {
    // This should be implemented to communicate with your WebSocket signaling server
    console.log('📤 Sending to signaling server:', message);
  }

  getLocalStream(): MediaStream | null {
    return this.localStream;
  }

  getRemoteStream(): MediaStream | null {
    return this.remoteStream;
  }

  getConnectionStats(): Promise<RTCStatsReport> | null {
    return this.peerConnection?.getStats() || null;
  }

  close(): void {
    // Close data channel
    if (this.dataChannel) {
      this.dataChannel.close();
      this.dataChannel = null;
    }

    // Stop local stream tracks
    if (this.localStream) {
      this.localStream.getTracks().forEach((track) => track.stop());
      this.localStream = null;
    }

    // Close peer connection
    if (this.peerConnection) {
      this.peerConnection.close();
      this.peerConnection = null;
    }

    this.remoteStream = null;
    console.log('🔌 WebRTC connection closed');
  }
}
