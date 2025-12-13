# Audio Studio – Feature Specification

## Goal
Provide a top-tier audio environment to record, upload, enhance, organize, and route audio into video, notebooks, publishing, and products.

---

## Core Capabilities (Phase 1)

### 1. Audio Ingestion

#### Recording
- **Browser-based recording** using Web Audio API / MediaRecorder
- **Microphone selection** (if multiple devices available)
- **Recording controls**: Start, Pause, Resume, Stop
- **Real-time waveform visualization** during recording
- **Recording timer** and file size indicator
- **Format**: WAV (lossless) or MP3 (compressed)

#### Upload
- **Drag-and-drop** file upload interface
- **File browser** selection
- **Supported formats**: WAV, MP3, M4A, FLAC, OGG
- **File validation**: Size limits (max 500MB), format check
- **Upload progress** indicator
- **Batch upload** support (multiple files)

#### Metadata Capture
```typescript
interface AudioSessionMetadata {
  title: string;                    // Required
  description?: string;             // Optional long-form description
  tags: AudioTag[];                 // Multi-select tags
  series?: string;                  // Part of a series/collection
  collection?: string;              // Album/collection name
  category: AudioCategory;          // Primary category
  duration: number;                 // Seconds
  fileSize: number;                 // Bytes
  format: AudioFormat;              // WAV, MP3, M4A, etc.
  sampleRate?: number;              // Hz (44100, 48000, etc.)
  bitrate?: number;                 // kbps
  createdAt: Date;
  updatedAt: Date;
}

type AudioTag =
  | 'devotional'
  | 'kids'
  | 'sermon'
  | 'lesson'
  | 'hymn'
  | 'podcast'
  | 'interview'
  | 'music'
  | 'voiceover'
  | 'narration';

type AudioCategory =
  | 'teaching'
  | 'worship'
  | 'storytelling'
  | 'podcast'
  | 'music'
  | 'production';

type AudioFormat = 'wav' | 'mp3' | 'm4a' | 'flac' | 'ogg';
```

---

### 2. Session Management

#### Sessions List View
**Location**: `/studio/audio`

**Features**:
- **Card/Table toggle** view modes
- **Search** by title, description, tags
- **Filters**:
  - By tag (multi-select)
  - By date range (created, updated)
  - By type (recorded vs uploaded)
  - By category
  - By series/collection
- **Sort options**:
  - Recently created (default)
  - Recently updated
  - Title (A-Z)
  - Duration (shortest/longest)
- **Pagination** or infinite scroll
- **Quick actions** per session:
  - Play preview (inline mini-player)
  - Edit metadata
  - Delete
  - Share link

#### Session Detail View
**Location**: `/studio/audio/:sessionId`

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Audio Studio                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎵 [Audio Player - Full Width]                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ [Play/Pause] ========●===== [00:45 / 03:20]        │  │
│  │ [Volume] [Speed] [Download]                         │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  Waveform Visualization                                     │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ▂▃▅▇▆▅▃▂▃▅▇▆▅▃▂▃▅▇▆▅▃▂▃▅▇▆▅▃▂▃▅▇▆▅▃▂▃▅▇▆▅▃▂▃▅▇▆▅▃  │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Metadata                          │ Actions                │
│ ┌───────────────────────────────┐ │ ┌────────────────────┐ │
│ │ Title: [Morning Devotional]  │ │ │ ⚡ Enhance Audio   │ │
│ │ Description: [textarea]      │ │ │ 📝 Generate Trans  │ │
│ │ Tags: [devotional] [hymn]    │ │ │ 🎬 Send to Video   │ │
│ │ Series: [Daily Devotionals]  │ │ │ 📚 Publish Content │ │
│ │ Category: [Worship]          │ │ │ ⚙️  Add to Workflow │ │
│ │ Duration: 3:20               │ │ │ 🔗 Copy Share Link │ │
│ │ Format: MP3 (320kbps)        │ │ │ 🗑️  Delete Session  │ │
│ │ Created: Dec 12, 2025        │ │ └────────────────────┘ │
│ │ [Save Changes]               │ │                        │
│ └───────────────────────────────┘ │                        │
└─────────────────────────────────────────────────────────────┘
```

**Action Buttons Behavior**:
- **Enhance Audio**: Opens modal → Select enhancements (noise reduction, normalize, EQ) → Process → Show progress
- **Generate Transcript**: Triggers transcription service → Redirects to Notebook Studio with new transcript
- **Send to Video**: Opens modal → Select template or blank → Creates video project with audio pre-loaded
- **Publish Content**: Redirects to Publishing Studio → Auto-fills audio source
- **Add to Workflow**: Opens Automation Studio → Creates new workflow with audio trigger
- **Copy Share Link**: Generates public/private share URL → Copies to clipboard
- **Delete Session**: Confirmation modal → Soft delete (with recovery option)

---

### 3. Basic Processing Hooks

#### Audio Enhancement Pipeline
```typescript
interface AudioProcessingRequest {
  sessionId: string;
  operations: AudioOperation[];
  outputFormat?: AudioFormat;
}

interface AudioOperation {
  type: AudioOperationType;
  params: Record<string, any>;
}

type AudioOperationType =
  | 'noise-reduction'    // Remove background noise
  | 'normalize'          // Normalize volume levels
  | 'eq'                 // Equalization adjustments
  | 'compress'           // Dynamic range compression
  | 'trim'               // Trim silence from start/end
  | 'fade-in'            // Add fade-in effect
  | 'fade-out'           // Add fade-out effect
  | 'pitch-shift'        // Change pitch
  | 'tempo-change'       // Change speed without pitch
  | 'export';            // Export to specific format

// Example usage:
const enhanceRequest: AudioProcessingRequest = {
  sessionId: '123',
  operations: [
    { type: 'noise-reduction', params: { strength: 0.7 } },
    { type: 'normalize', params: { targetLevel: -14 } },
    { type: 'trim', params: { threshold: -40 } },
    { type: 'fade-in', params: { duration: 0.5 } },
    { type: 'fade-out', params: { duration: 1.0 } }
  ],
  outputFormat: 'mp3'
};
```

#### Processing UI Flow
1. **User clicks "Enhance Audio"**
2. **Modal opens** with preset options:
   - Quick Enhance (auto-apply common fixes)
   - Voice Optimize (for speech/podcasts)
   - Music Master (for music content)
   - Custom (manual parameter selection)
3. **User selects preset** or customizes
4. **Preview processing** (optional, on first 30 seconds)
5. **Confirm** → Backend processing starts
6. **Progress indicator** shows processing status
7. **Completion notification** → New version available
8. **Version history** keeps both original and enhanced

---

### 4. Routing to Other Studios

#### Integration Architecture
```typescript
interface StudioRouting {
  sourceStudio: 'audio';
  targetStudio: StudioType;
  action: RoutingAction;
  payload: AudioSessionPayload;
}

type StudioType =
  | 'video'
  | 'notebook'
  | 'publishing'
  | 'automation'
  | 'builder';

interface AudioSessionPayload {
  sessionId: string;
  audioUrl: string;
  metadata: AudioSessionMetadata;
  transcript?: string;       // If already generated
  waveformData?: number[];   // For visualization
}
```

#### Routing Actions

**→ Video Studio**
```typescript
// Route: /studio/video?source=audio&sessionId=123
interface VideoFromAudioAction {
  audioSessionId: string;
  template?: 'lyrics' | 'waveform' | 'minimal' | 'custom';
  options?: {
    addSubtitles: boolean;      // If transcript available
    visualizerStyle: string;    // Waveform visualization type
    backgroundImage?: string;   // Cover art or background
    aspectRatio: '16:9' | '9:16' | '1:1';
  };
}
```

**→ Notebook Studio**
```typescript
// Route: /studio/notebook?action=transcribe&audioId=123
interface NotebookFromAudioAction {
  audioSessionId: string;
  action: 'transcribe' | 'link-asset';
  options?: {
    generateSummary: boolean;
    extractKeyPoints: boolean;
    createTimestamps: boolean;
    speakerDiarization: boolean;  // Identify multiple speakers
  };
}
```

**→ Publishing Studio**
```typescript
// Route: /studio/publishing?source=audio&sessionId=123
interface PublishFromAudioAction {
  audioSessionId: string;
  outputType: 'study-guide' | 'transcript-book' | 'landing-page' | 'email-campaign';
  options?: {
    includeAudioPlayer: boolean;
    generateChapters: boolean;
    addReflectionQuestions: boolean;
  };
}
```

**→ Automation Studio**
```typescript
// Route: /studio/automation?trigger=audio-upload&sessionId=123
interface AutomationFromAudioAction {
  audioSessionId: string;
  workflowType: 'on-upload' | 'on-complete' | 'scheduled';
  actions: AutomationStep[];
}

interface AutomationStep {
  type: 'transcribe' | 'publish' | 'notify' | 'backup' | 'social-share';
  params: Record<string, any>;
}
```

---

### 5. Asset Storage

#### Storage Architecture
```typescript
interface AudioStorage {
  provider: 'azure-blob' | 'aws-s3' | 'cloudflare-r2';
  container: string;
  path: string;
  publicUrl?: string;      // For shareable links
  cdnUrl?: string;         // CDN-accelerated URL
}

interface AudioAsset {
  id: string;              // UUID
  sessionId: string;       // Parent session
  version: number;         // Version number (original = 1)
  storage: AudioStorage;
  metadata: {
    filename: string;
    mimeType: string;
    size: number;          // Bytes
    duration: number;      // Seconds
    checksum: string;      // MD5/SHA256 for integrity
  };
  status: 'uploading' | 'processing' | 'ready' | 'failed';
  createdAt: Date;
}
```

#### Backend API Endpoints
```typescript
// Upload audio file
POST /api/audio/upload
Request: multipart/form-data (file + metadata)
Response: { sessionId, assetId, uploadUrl }

// Get session details
GET /api/audio/sessions/:id
Response: AudioSession with full metadata

// Update session metadata
PATCH /api/audio/sessions/:id
Request: Partial<AudioSessionMetadata>
Response: Updated AudioSession

// List sessions
GET /api/audio/sessions?tags=devotional&limit=20&offset=0
Response: { sessions: AudioSession[], total, hasMore }

// Process audio (enhance, export, etc.)
POST /api/audio/sessions/:id/process
Request: AudioProcessingRequest
Response: { jobId, status, estimatedTime }

// Get processing status
GET /api/audio/sessions/:id/jobs/:jobId
Response: { status, progress, result? }

// Delete session
DELETE /api/audio/sessions/:id
Response: { success: boolean }

// Generate share link
POST /api/audio/sessions/:id/share
Request: { expiresIn?, password? }
Response: { shareUrl, expiresAt }
```

---

## Nice-to-Have (Phase 2)

### Multi-Track Sessions
```typescript
interface MultiTrackSession extends AudioSession {
  tracks: AudioTrack[];
  mixdown?: AudioAsset;  // Final mixed audio
}

interface AudioTrack {
  id: string;
  name: string;          // "Vocals", "Music", "Narration"
  asset: AudioAsset;
  volume: number;        // 0.0 - 1.0
  pan: number;           // -1.0 (left) to 1.0 (right)
  muted: boolean;
  solo: boolean;
  effects: AudioEffect[];
}

interface AudioEffect {
  type: 'reverb' | 'delay' | 'chorus' | 'eq' | 'compressor';
  params: Record<string, number>;
  enabled: boolean;
}
```

**UI**: Simple mixer interface with volume sliders, pan controls, mute/solo buttons per track.

### AI Voice Features
- **Voice Enhancement**: Clarity improvement, de-esser, de-breath
- **AI Narration**: Text-to-speech with custom voices (ElevenLabs, Azure Speech)
- **Voice Cloning**: Train on user's voice for consistent narration
- **Accent/Language**: Convert audio to different accents or languages

### Stem Separation
- **Vocals Isolation**: Extract clean vocal track
- **Music Isolation**: Extract instrumental/music track
- **Ambience**: Extract background sounds
- **Use Case**: Karaoke tracks, remixing, cleaner transcripts

---

## UI Sections

### Audio Studio Home (`/studio/audio`)

**Header**:
- Logo + "Audio Studio"
- Search bar
- Filter toggles (Tags, Date, Type)
- Sort dropdown
- View mode toggle (Cards/Table)

**Main Area**:
```
┌─────────────────────────────────────────────────────────────┐
│ Audio Studio                                 [+ New Session] │
├─────────────────────────────────────────────────────────────┤
│ [🔍 Search...] [🏷️ Tags ▾] [📅 Date ▾] [⚙️ Type ▾]          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Recent Sessions (24)                                        │
│                                                             │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐  │
│ │ 🎵        │ │ 🎵        │ │ 🎵        │ │ 🎵        │  │
│ │ Morning   │ │ Podcast   │ │ Kids      │ │ Sermon    │  │
│ │ Devotion  │ │ EP12      │ │ Story     │ │ Dec 8     │  │
│ │ 3:20      │ │ 45:12     │ │ 8:45      │ │ 32:18     │  │
│ │ [▶] [✏️] │ │ [▶] [✏️] │ │ [▶] [✏️] │ │ [▶] [✏️] │  │
│ └───────────┘ └───────────┘ └───────────┘ └───────────┘  │
│                                                             │
│ [Load More]                                                 │
└─────────────────────────────────────────────────────────────┘
```

**"New Session" Button** → Opens modal:
- Tab 1: **Record** (microphone icon)
- Tab 2: **Upload** (upload icon)

### Session Detail (`/studio/audio/:id`)

See detailed layout in Section 2 above.

**Key Interactions**:
- **Waveform** is clickable for seeking
- **Player controls** are always visible (sticky)
- **Metadata form** has autosave on blur
- **Action buttons** open modals or redirect with context

---

## Technical Stack

### Frontend
- **React 18** + **TypeScript**
- **Next.js** (or Vite if standalone)
- **Tailwind CSS** for styling
- **Wavesurfer.js** or **Peaks.js** for waveform visualization
- **Howler.js** for audio playback
- **React Hook Form** for metadata forms
- **React Query** for data fetching/caching

### Backend
- **Node.js/TypeScript** or **Python/FastAPI**
- **Postgres** for session metadata
- **Azure Blob Storage** (or AWS S3) for audio files
- **Azure Media Services** or **FFmpeg** for processing
- **Azure Speech Services** for transcription (Phase 2)

### APIs & Services
- **Azure Blob Storage SDK** for uploads
- **FFmpeg** (backend) for audio processing
- **Whisper API** or **Azure Speech** for transcription
- **ElevenLabs** or **Azure TTS** for AI voice (Phase 2)

---

## Implementation Phases

### Phase 1: MVP (2-3 weeks)
- [x] Upload audio files with metadata
- [x] Sessions list with search/filter
- [x] Session detail with player
- [x] Basic routing buttons (UI only)
- [x] Azure Blob Storage integration
- [x] Metadata CRUD operations

### Phase 2: Processing (2-3 weeks)
- [ ] Browser-based recording
- [ ] Audio enhancement (noise reduction, normalize)
- [ ] Waveform visualization
- [ ] Transcription integration
- [ ] Actual routing to Video/Notebook/Publishing

### Phase 3: Advanced (3-4 weeks)
- [ ] Multi-track sessions
- [ ] Simple mixer UI
- [ ] AI voice features
- [ ] Stem separation
- [ ] Collaboration (comments, sharing)

---

## Success Metrics

- **Adoption**: 80% of users upload/record at least 1 audio session per week
- **Routing**: 50% of audio sessions are routed to another studio
- **Transcription**: 70% of podcasts/sermons get transcribed
- **Enhancement**: 40% of sessions use audio enhancement
- **Retention**: Audio assets have 95%+ storage reliability

---

## Security & Permissions

- **Audio files** are private by default
- **Share links** can be:
  - Public (anyone with link)
  - Password-protected
  - Time-limited (expires after X days)
- **Role-based access**:
  - Owner: Full CRUD
  - Council: View + Comment
  - Heir: View only (educational content)

---

**Last Updated**: December 12, 2025
**Owner**: CodexDominion Audio Studio Team
**Status**: Ready for Implementation
