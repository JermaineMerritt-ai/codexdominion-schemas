# Multi-Audience Broadcast Architecture
**Codex Dominion • Flame Sovereign Status • v2.0.0**

---

## 🔥 Sovereign Proclamation

The Ceremonial Broadcast System enables synchronized multi-audience viewing of Codex Dominion's sovereign flame heartbeat. Councils, heirs, and observers witness engine status changes, constellation highlights, and replay capsule events in perfect harmony.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SOVEREIGN BROADCASTER                         │
│  (Controls playback, shares screen/video, sends sync events)    │
└─────────────┬───────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       RELAY SERVER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  WebSocket   │  │   WebRTC     │  │   Redis      │          │
│  │  Signaling   │  │   Relay      │  │   PubSub     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  • Role-based access control (sovereign/council/heir/observer)  │
│  • Capsule sync event broadcasting                              │
│  • Constellation state synchronization                          │
│  • Playback control relay                                       │
└─────────────┬───────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PARTICIPANT VIEWERS                           │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐   │
│  │  Council  │  │  Council  │  │   Heir    │  │ Observer  │   │
│  │  Member   │  │  Member   │  │           │  │           │   │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📡 Communication Layers

### 1. WebSocket Layer (Control Plane)
**Purpose:** Real-time synchronization of replay state and constellation updates

**Message Types:**
```typescript
interface BroadcastMessage {
  type: 'capsule_sync' | 'constellation_update' | 'playback_control' | 'role_assignment' | 'heartbeat';
  timestamp: string;
  payload: any;
  senderId: string;
  role: 'sovereign' | 'council' | 'heir' | 'observer';
}
```

**Events:**
- **capsule_sync**: Broadcasts current replay capsule index, status, and mode
- **constellation_update**: Highlights current engine node with status color
- **playback_control**: Play, pause, seek, reset, fast-forward, rewind commands
- **role_assignment**: Server assigns role based on authentication
- **heartbeat**: Keep-alive ping every 30 seconds

**Connection Flow:**
```
Client → ws://relay.codexdominion.com?clientId={id}&role={role}
Server → Authenticates role via JWT token
Server → Broadcasts role_assignment message
Client → Subscribes to capsule_sync, constellation_update, playback_control
Sovereign → Sends sync events on every index/status change
Viewers → Receive and apply state updates automatically
```

### 2. WebRTC Layer (Media Plane)
**Purpose:** Low-latency video/screen sharing for ceremonial broadcast view

**Components:**
- **RTCPeerConnection**: Handles peer-to-peer media streaming
- **RTCDataChannel**: Supplementary data sync (backup for WebSocket)
- **STUN/TURN Servers**: NAT traversal for firewall penetration

**Broadcaster Flow:**
```javascript
1. navigator.mediaDevices.getDisplayMedia() → Capture broadcast screen
2. RTCPeerConnection.addTrack() → Add video/audio tracks
3. createOffer() → Generate SDP offer
4. WebSocket → Send offer to relay server
5. Relay → Forwards offer to all connected viewers
```

**Viewer Flow:**
```javascript
1. WebSocket → Receive offer from broadcaster via relay
2. createAnswer() → Generate SDP answer
3. WebSocket → Send answer back to broadcaster
4. RTCPeerConnection.ontrack → Receive remote stream
5. <video ref={remoteStreamRef} autoPlay /> → Display broadcast
```

**ICE Candidate Exchange:**
```
Broadcaster → Finds ICE candidates → WebSocket → Relay → Viewers
Viewers → Find ICE candidates → WebSocket → Relay → Broadcaster
Both sides add candidates via addIceCandidate()
```

### 3. Relay Server Architecture

**Technology Stack:**
- **Node.js + ws**: WebSocket server for signaling
- **Redis**: PubSub for horizontal scaling across relay instances
- **JWT Authentication**: Role-based access control
- **Rate Limiting**: Prevent abuse (10 messages/sec per client)

**Role Permissions:**
```
Sovereign:
  - Send capsule_sync, constellation_update, playback_control
  - Initiate WebRTC broadcast
  - Control replay timeline
  - Disconnect any participant

Council:
  - Receive all sync events
  - View WebRTC stream
  - Send feedback messages (optional)
  - Cannot control playback

Heir:
  - Receive all sync events
  - View WebRTC stream
  - Read-only access

Observer:
  - Receive capsule_sync only (limited)
  - No WebRTC access
  - Rate-limited updates (1 every 5 seconds)
```

**Server Endpoints:**
```
WebSocket: ws://relay.codexdominion.com
  Query Params: ?clientId={id}&role={role}&token={jwt}

REST API: https://relay.codexdominion.com/api
  POST /broadcast/start → Sovereign initiates broadcast
  POST /broadcast/stop → Sovereign ends broadcast
  GET /broadcast/participants → List active viewers
  POST /broadcast/kick/{clientId} → Remove participant
  GET /broadcast/stats → Connection metrics
```

---

## 🎯 Implementation Components

### Frontend (Next.js + React)

**Created Files:**
1. **`web/lib/broadcast/websocket-manager.ts`**
   - BroadcastWebSocketManager class
   - Message type definitions
   - Reconnection logic with exponential backoff
   - Heartbeat keep-alive (30s interval)
   - Role-based message filtering

2. **`web/lib/broadcast/webrtc-manager.ts`**
   - BroadcastWebRTCManager class
   - Broadcaster initialization with screen capture
   - Viewer connection with remote stream handling
   - Data channel for backup sync
   - ICE candidate handling

3. **`web/hooks/useBroadcastSync.ts`**
   - React hook integrating WebSocket + ReplayContext
   - Auto-sync index, capsules, isPlaying, mode
   - Sovereign broadcasts state changes
   - Viewers receive and apply updates
   - Connection state management

4. **`web/components/broadcast-mode.tsx`**
   - Fullscreen ceremonial view
   - ConstellationMap + ReplayViewer side-by-side
   - Live status bar with participant count
   - Enter/exit broadcast toggle

**Integration Example:**
```tsx
// pages/broadcast/page.tsx
import { BroadcastMode } from '@/components/broadcast-mode';
import { useBroadcastSync } from '@/hooks/useBroadcastSync';

export default function BroadcastPage() {
  const { broadcastState, connect, disconnect } = useBroadcastSync({
    wsUrl: process.env.NEXT_PUBLIC_WS_RELAY_URL!,
    role: 'sovereign', // or 'council', 'heir', 'observer'
    autoConnect: true,
  });

  return (
    <div>
      <div className="text-white">
        Status: {broadcastState.isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        | Participants: {broadcastState.participantCount}
      </div>
      <BroadcastMode />
    </div>
  );
}
```

### Backend (Relay Server)

**Required Implementation:**
```typescript
// server/relay-server.ts
import WebSocket from 'ws';
import { createClient } from 'redis';
import jwt from 'jsonwebtoken';

const wss = new WebSocket.Server({ port: 8080 });
const redis = createClient();
await redis.connect();

wss.on('connection', async (ws, req) => {
  const url = new URL(req.url!, 'ws://localhost');
  const token = url.searchParams.get('token');
  const role = url.searchParams.get('role');

  // Authenticate
  const decoded = jwt.verify(token, process.env.JWT_SECRET);

  // Subscribe to Redis channel
  const subscriber = redis.duplicate();
  await subscriber.connect();
  await subscriber.subscribe('broadcast-sync', (message) => {
    ws.send(message);
  });

  ws.on('message', async (data) => {
    const msg = JSON.parse(data.toString());

    // Role-based filtering
    if (role === 'sovereign') {
      // Broadcast to all via Redis
      await redis.publish('broadcast-sync', JSON.stringify(msg));
    } else if (['council', 'heir'].includes(role)) {
      // Councils/heirs can send feedback (optional)
      if (msg.type === 'feedback') {
        await redis.publish('broadcast-feedback', JSON.stringify(msg));
      }
    }
    // Observers cannot send messages
  });
});
```

---

## 🔐 Security Considerations

1. **Authentication:**
   - JWT tokens with role claims
   - Expire after broadcast session ends
   - Refresh mechanism for long broadcasts

2. **Rate Limiting:**
   - 10 messages/second per client
   - 100 connection attempts/hour per IP
   - Sovereign exempt from limits

3. **Encryption:**
   - WSS (WebSocket Secure) with TLS 1.3
   - DTLS for WebRTC data channels
   - End-to-end encryption for sensitive metadata

4. **Access Control:**
   - Role verification on every message
   - Sovereign can kick participants
   - IP whitelist for council members

---

## 📊 Monitoring & Observability

**Metrics to Track:**
- Active WebSocket connections (by role)
- WebRTC stream quality (bitrate, packet loss, jitter)
- Message latency (time from sovereign send to viewer receive)
- Reconnection attempts per client
- CPU/memory usage on relay server

**Grafana Dashboards:**
- Real-time participant count
- Capsule sync frequency
- Constellation update lag
- Role distribution (sovereign: 1, councils: X, heirs: Y, observers: Z)

**Alerts:**
- Sovereign disconnected → Pause broadcast, notify all
- Relay server CPU > 80% → Scale horizontally
- Message queue depth > 1000 → Backpressure warning
- Participant count drops suddenly → Investigate network issue

---

## 🚀 Deployment Checklist

### Phase 1: Local Testing
- [x] WebSocket manager implemented
- [x] WebRTC manager implemented
- [x] useBroadcastSync hook created
- [x] BroadcastMode component integrated
- [ ] Test with 2 browser windows (sovereign + viewer)
- [ ] Verify capsule sync lag < 100ms
- [ ] Test constellation highlighting

### Phase 2: Relay Server
- [ ] Deploy Node.js WebSocket server to Azure
- [ ] Configure Redis for PubSub
- [ ] Implement JWT authentication
- [ ] Add rate limiting middleware
- [ ] Set up STUN/TURN servers
- [ ] Load test with 50 concurrent viewers

### Phase 3: Production
- [ ] Enable WSS with SSL certificate
- [ ] Deploy to IONOS frontend (Next.js static)
- [ ] Point WebSocket to Azure relay URL
- [ ] Configure CORS for WebRTC signaling
- [ ] Set up Grafana monitoring
- [ ] Create runbook for incident response

### Phase 4: Optimization
- [ ] Implement Redis Cluster for multi-region
- [ ] Add CDN caching for static assets
- [ ] Optimize WebRTC codec (VP9 vs H.264)
- [ ] Implement adaptive bitrate for slow connections
- [ ] Add reconnection with state recovery

---

## 🎬 Ceremonial Broadcast Rituals

**Daily Stand-Up:**
- Sovereign shares engine health dashboard
- Councils view constellation map
- Review degraded services (orange nodes)
- Discuss recovery plans

**Weekly Review:**
- Sovereign plays full week replay (epochal mode)
- Highlight critical incidents
- Celebrate uptime milestones
- Constellations pulse with success metrics

**Quarterly Showcase:**
- Sovereign presents to all heirs
- Fullscreen broadcast mode
- Live commentary with voice narration
- Q&A session via chat overlay

---

## 📚 API Reference

### WebSocket Messages

**Capsule Sync (Sovereign → All):**
```json
{
  "type": "capsule_sync",
  "timestamp": "2025-12-07T05:39:00Z",
  "senderId": "sovereign_001",
  "role": "sovereign",
  "payload": {
    "index": 12,
    "capsule": {
      "id": "cap_1234",
      "timestamp": "2025-12-07T05:39:00Z",
      "engine": "Commerce Engine",
      "status": "degraded",
      "message": "High API latency detected",
      "metadata": { "latency_ms": 850 }
    },
    "isPlaying": true,
    "mode": "daily"
  }
}
```

**Playback Control (Sovereign → All):**
```json
{
  "type": "playback_control",
  "timestamp": "2025-12-07T06:00:00Z",
  "senderId": "sovereign_001",
  "role": "sovereign",
  "payload": {
    "action": "pause"
  }
}
```

**Constellation Update (Sovereign → All):**
```json
{
  "type": "constellation_update",
  "timestamp": "2025-12-07T05:39:00Z",
  "senderId": "sovereign_001",
  "role": "sovereign",
  "payload": {
    "highlightedEngine": "Commerce Engine",
    "status": "degraded",
    "nodePositions": {
      "Commerce Engine": { "x": 300, "y": 200 }
    }
  }
}
```

---

## 🔮 Future Enhancements

1. **Multi-Sovereign Mode:**
   - Multiple broadcasters in round-robin
   - Council voting for active sovereign
   - Smooth handoff without disconnect

2. **Recording & Playback:**
   - Save broadcast sessions to Azure Blob
   - Replay past ceremonies on-demand
   - Searchable archive by engine/status

3. **Interactive Polls:**
   - Sovereign asks questions during broadcast
   - Councils vote in real-time
   - Results displayed on constellation map

4. **AI Commentary:**
   - Jermaine Super Action AI narrates events
   - Explains status changes in ceremonial language
   - Text-to-speech for accessibility

5. **Spatial Audio:**
   - Different engines emit unique tones
   - Degraded services sound alarm chimes
   - Operational engines hum harmoniously

---

## 🛡️ Flame Sovereign Seal

**Authored by:** Codex Dominion Engineering Council
**Approved by:** Jermaine Merritt, Sovereign Architect
**Status:** 🔥 **SEALED AND ETERNAL**
**Version:** 2.0.0
**Last Updated:** 2025-12-07T06:15:00Z

---

**All systems operational. All audiences synchronized. The flame burns eternal across all realms.**

🔥 **CODEX DOMINION • ALIVE • IMMORTAL** 🔥
