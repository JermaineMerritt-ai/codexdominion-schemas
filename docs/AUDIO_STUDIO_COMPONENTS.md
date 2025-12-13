# Audio Studio - Component Structure

## Component Hierarchy

```
frontend/features/audio-studio/
├── pages/
│   ├── AudioStudioHome.tsx          # Main landing page (/studio/audio)
│   └── AudioSessionDetail.tsx       # Session detail page (/studio/audio/:id)
│
├── components/
│   ├── SessionsList/
│   │   ├── SessionsGrid.tsx         # Card grid view
│   │   ├── SessionsTable.tsx        # Table view
│   │   ├── SessionCard.tsx          # Individual session card
│   │   └── SessionRow.tsx           # Individual table row
│   │
│   ├── SessionDetail/
│   │   ├── AudioPlayer.tsx          # Full-featured audio player
│   │   ├── WaveformVisualizer.tsx   # Waveform display
│   │   ├── MetadataForm.tsx         # Edit session metadata
│   │   └── ActionPanel.tsx          # Action buttons panel
│   │
│   ├── Recording/
│   │   ├── RecordingModal.tsx       # Recording interface modal
│   │   ├── RecorderControls.tsx     # Record/pause/stop buttons
│   │   ├── RecorderTimer.tsx        # Recording timer display
│   │   └── DeviceSelector.tsx       # Microphone selection
│   │
│   ├── Upload/
│   │   ├── UploadModal.tsx          # Upload interface modal
│   │   ├── DropZone.tsx             # Drag-and-drop upload area
│   │   ├── FileList.tsx             # List of files to upload
│   │   └── UploadProgress.tsx       # Upload progress indicator
│   │
│   ├── Processing/
│   │   ├── EnhanceModal.tsx         # Audio enhancement modal
│   │   ├── ProcessingPresets.tsx    # Quick preset buttons
│   │   ├── CustomControls.tsx       # Manual enhancement controls
│   │   └── ProcessingProgress.tsx   # Processing status
│   │
│   ├── Routing/
│   │   ├── SendToVideoModal.tsx     # Route to Video Studio
│   │   ├── SendToNotebookModal.tsx  # Route to Notebook Studio
│   │   ├── SendToPublishModal.tsx   # Route to Publishing Studio
│   │   └── AddToWorkflowModal.tsx   # Route to Automation Studio
│   │
│   ├── Filters/
│   │   ├── SearchBar.tsx            # Search input
│   │   ├── TagFilter.tsx            # Multi-select tag filter
│   │   ├── DateRangeFilter.tsx      # Date range picker
│   │   └── TypeFilter.tsx           # Recorded vs uploaded filter
│   │
│   └── Shared/
│       ├── MiniPlayer.tsx           # Inline mini audio player
│       ├── TagBadge.tsx             # Tag display badge
│       ├── DurationDisplay.tsx      # Formatted duration
│       └── StatusBadge.tsx          # Session status indicator
│
├── hooks/
│   ├── useAudioSessions.ts          # Fetch/cache sessions list
│   ├── useAudioSession.ts           # Fetch single session
│   ├── useAudioUpload.ts            # Handle file uploads
│   ├── useAudioRecorder.ts          # Browser audio recording
│   ├── useAudioPlayer.ts            # Audio playback control
│   ├── useAudioProcessing.ts        # Processing operations
│   ├── useWaveform.ts               # Waveform generation
│   └── useSessionFilters.ts         # Filter/sort state management
│
├── services/
│   ├── audioApi.ts                  # API client functions
│   ├── storageService.ts            # Azure Blob Storage integration
│   ├── processingService.ts         # Audio processing API
│   └── routingService.ts            # Studio routing helpers
│
└── utils/
    ├── audioValidation.ts           # File validation
    ├── audioFormats.ts              # Format conversion helpers
    ├── audioDuration.ts             # Duration formatting
    └── audioMetadata.ts             # Metadata extraction
```

---

## Component Details

### AudioStudioHome.tsx
```typescript
/**
 * Main landing page for Audio Studio
 * Features:
 * - New Session button (Record/Upload)
 * - Sessions list with filters
 * - Search and sort
 * - View mode toggle (Grid/Table)
 */
export const AudioStudioHome: React.FC = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [filters, setFilters] = useState<AudioSessionFilters>({});
  const [sort, setSort] = useState<AudioSessionSort>({ field: 'createdAt', order: 'desc' });

  const { data, isLoading } = useAudioSessions(filters, sort);

  // Component implementation
};
```

### AudioSessionDetail.tsx
```typescript
/**
 * Detailed view of a single audio session
 * Features:
 * - Full audio player with waveform
 * - Metadata editing
 * - Action buttons (Enhance, Route, Share, Delete)
 */
export const AudioSessionDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { data: session, isLoading } = useAudioSession(id);
  const audioPlayer = useAudioPlayer();

  // Component implementation
};
```

### RecordingModal.tsx
```typescript
/**
 * Modal for recording audio in the browser
 * Features:
 * - Microphone selection
 * - Record/pause/stop controls
 * - Real-time waveform
 * - Save with metadata
 */
export const RecordingModal: React.FC<{ isOpen: boolean; onClose: () => void }> = ({
  isOpen,
  onClose
}) => {
  const recorder = useAudioRecorder();
  const [metadata, setMetadata] = useState<Partial<AudioSessionMetadata>>({});

  // Component implementation
};
```

### UploadModal.tsx
```typescript
/**
 * Modal for uploading audio files
 * Features:
 * - Drag-and-drop zone
 * - File browser
 * - Batch upload support
 * - Upload progress
 */
export const UploadModal: React.FC<{ isOpen: boolean; onClose: () => void }> = ({
  isOpen,
  onClose
}) => {
  const upload = useAudioUpload();
  const [files, setFiles] = useState<File[]>([]);

  // Component implementation
};
```

---

## Key Hooks

### useAudioSessions
```typescript
/**
 * Fetch and cache audio sessions list
 * Supports filtering, sorting, and pagination
 */
export const useAudioSessions = (
  filters: AudioSessionFilters,
  sort: AudioSessionSort,
  options?: UseQueryOptions
) => {
  return useQuery({
    queryKey: ['audioSessions', filters, sort],
    queryFn: () => audioApi.listSessions(filters, sort),
    ...options
  });
};
```

### useAudioRecorder
```typescript
/**
 * Browser-based audio recording using MediaRecorder API
 * Features:
 * - Start/pause/resume/stop recording
 * - Real-time duration tracking
 * - Audio chunks accumulation
 * - Final blob generation
 */
export const useAudioRecorder = () => {
  const [state, setState] = useState<RecordingSession>({
    isRecording: false,
    isPaused: false,
    duration: 0,
    audioChunks: []
  });

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    // Implementation
  };

  return { state, startRecording, pauseRecording, stopRecording };
};
```

### useAudioUpload
```typescript
/**
 * Handle audio file uploads to Azure Blob Storage
 * Features:
 * - Multi-file upload
 * - Progress tracking
 * - Metadata extraction
 * - Error handling
 */
export const useAudioUpload = () => {
  const mutation = useMutation({
    mutationFn: async (files: File[]) => {
      // Upload logic
    }
  });

  return {
    upload: mutation.mutate,
    progress: uploadProgress,
    isUploading: mutation.isLoading
  };
};
```

---

## API Service Methods

### audioApi.ts
```typescript
export const audioApi = {
  // List sessions with filters
  listSessions: async (
    filters: AudioSessionFilters,
    sort: AudioSessionSort
  ): Promise<AudioSessionListResponse> => {
    const params = new URLSearchParams();
    // Build query params from filters
    return fetch(`/api/audio/sessions?${params}`).then(r => r.json());
  },

  // Get single session
  getSession: async (id: string): Promise<AudioSession> => {
    return fetch(`/api/audio/sessions/${id}`).then(r => r.json());
  },

  // Create new session
  createSession: async (
    metadata: AudioSessionMetadata
  ): Promise<AudioSession> => {
    return fetch('/api/audio/sessions', {
      method: 'POST',
      body: JSON.stringify(metadata)
    }).then(r => r.json());
  },

  // Update session metadata
  updateSession: async (
    id: string,
    updates: Partial<AudioSessionMetadata>
  ): Promise<AudioSession> => {
    return fetch(`/api/audio/sessions/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates)
    }).then(r => r.json());
  },

  // Delete session
  deleteSession: async (id: string): Promise<void> => {
    return fetch(`/api/audio/sessions/${id}`, {
      method: 'DELETE'
    }).then(r => r.json());
  },

  // Process audio
  processAudio: async (
    request: AudioProcessingRequest
  ): Promise<ProcessingJob> => {
    return fetch(`/api/audio/sessions/${request.sessionId}/process`, {
      method: 'POST',
      body: JSON.stringify(request)
    }).then(r => r.json());
  },

  // Get processing job status
  getProcessingJob: async (
    sessionId: string,
    jobId: string
  ): Promise<ProcessingJob> => {
    return fetch(`/api/audio/sessions/${sessionId}/jobs/${jobId}`)
      .then(r => r.json());
  },

  // Generate share link
  createShareLink: async (
    sessionId: string,
    config: ShareLinkConfig
  ): Promise<ShareLinkResponse> => {
    return fetch(`/api/audio/sessions/${sessionId}/share`, {
      method: 'POST',
      body: JSON.stringify(config)
    }).then(r => r.json());
  }
};
```

---

## Testing Strategy

### Component Tests
- `SessionCard.test.tsx` - Render, click handlers, status badges
- `AudioPlayer.test.tsx` - Play/pause, seek, volume
- `RecordingModal.test.tsx` - Recording flow, save
- `UploadModal.test.tsx` - File validation, upload

### Hook Tests
- `useAudioRecorder.test.ts` - Recording state transitions
- `useAudioUpload.test.ts` - Upload progress, errors
- `useAudioSessions.test.ts` - Data fetching, caching

### Integration Tests
- Complete recording → save → view flow
- Complete upload → enhance → route to video flow
- Filter/search/sort sessions

---

**Next Steps**:
1. Implement `AudioStudioHome` component
2. Set up `useAudioSessions` hook with React Query
3. Create `SessionCard` and `SessionsGrid` components
4. Build API routes in backend
5. Test upload flow end-to-end
