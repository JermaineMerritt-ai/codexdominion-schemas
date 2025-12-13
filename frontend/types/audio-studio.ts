// Audio Studio - TypeScript Type Definitions
// Location: frontend/types/audio-studio.ts

/**
 * Core audio session metadata structure
 */
export interface AudioSessionMetadata {
  title: string;
  description?: string;
  tags: AudioTag[];
  series?: string;
  collection?: string;
  category: AudioCategory;
  duration: number;          // Seconds
  fileSize: number;          // Bytes
  format: AudioFormat;
  sampleRate?: number;       // Hz (44100, 48000, etc.)
  bitrate?: number;          // kbps
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Audio session tag types
 */
export type AudioTag =
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

/**
 * Audio session category types
 */
export type AudioCategory =
  | 'teaching'
  | 'worship'
  | 'storytelling'
  | 'podcast'
  | 'music'
  | 'production';

/**
 * Supported audio formats
 */
export type AudioFormat = 'wav' | 'mp3' | 'm4a' | 'flac' | 'ogg';

/**
 * Complete audio session with asset and metadata
 */
export interface AudioSession {
  id: string;
  userId: string;
  metadata: AudioSessionMetadata;
  assets: AudioAsset[];
  currentVersion: number;
  status: SessionStatus;
  shareUrl?: string;
  transcriptId?: string;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Session status types
 */
export type SessionStatus =
  | 'draft'           // Initial creation
  | 'uploading'       // File upload in progress
  | 'processing'      // Audio processing in progress
  | 'ready'           // Ready to use
  | 'failed'          // Processing failed
  | 'archived';       // Soft deleted

/**
 * Audio asset storage information
 */
export interface AudioAsset {
  id: string;
  sessionId: string;
  version: number;
  storage: AudioStorage;
  metadata: AssetMetadata;
  status: AssetStatus;
  createdAt: Date;
}

/**
 * Storage backend configuration
 */
export interface AudioStorage {
  provider: 'azure-blob' | 'aws-s3' | 'cloudflare-r2';
  container: string;
  path: string;
  publicUrl?: string;
  cdnUrl?: string;
}

/**
 * Asset-level metadata
 */
export interface AssetMetadata {
  filename: string;
  mimeType: string;
  size: number;
  duration: number;
  checksum: string;
}

/**
 * Asset processing status
 */
export type AssetStatus =
  | 'uploading'
  | 'processing'
  | 'ready'
  | 'failed';

/**
 * Audio processing request structure
 */
export interface AudioProcessingRequest {
  sessionId: string;
  operations: AudioOperation[];
  outputFormat?: AudioFormat;
}

/**
 * Individual audio processing operation
 */
export interface AudioOperation {
  type: AudioOperationType;
  params: Record<string, any>;
}

/**
 * Available audio processing operations
 */
export type AudioOperationType =
  | 'noise-reduction'
  | 'normalize'
  | 'eq'
  | 'compress'
  | 'trim'
  | 'fade-in'
  | 'fade-out'
  | 'pitch-shift'
  | 'tempo-change'
  | 'export';

/**
 * Studio routing configuration
 */
export interface StudioRouting {
  sourceStudio: 'audio';
  targetStudio: StudioType;
  action: RoutingAction;
  payload: AudioSessionPayload;
}

/**
 * Available target studios
 */
export type StudioType =
  | 'video'
  | 'notebook'
  | 'publishing'
  | 'automation'
  | 'builder';

/**
 * Routing action types
 */
export type RoutingAction = string; // Specific to each studio

/**
 * Payload when routing audio to another studio
 */
export interface AudioSessionPayload {
  sessionId: string;
  audioUrl: string;
  metadata: AudioSessionMetadata;
  transcript?: string;
  waveformData?: number[];
}

/**
 * Video creation from audio
 */
export interface VideoFromAudioAction {
  audioSessionId: string;
  template?: 'lyrics' | 'waveform' | 'minimal' | 'custom';
  options?: {
    addSubtitles: boolean;
    visualizerStyle: string;
    backgroundImage?: string;
    aspectRatio: '16:9' | '9:16' | '1:1';
  };
}

/**
 * Notebook creation from audio
 */
export interface NotebookFromAudioAction {
  audioSessionId: string;
  action: 'transcribe' | 'link-asset';
  options?: {
    generateSummary: boolean;
    extractKeyPoints: boolean;
    createTimestamps: boolean;
    speakerDiarization: boolean;
  };
}

/**
 * Publishing from audio
 */
export interface PublishFromAudioAction {
  audioSessionId: string;
  outputType: 'study-guide' | 'transcript-book' | 'landing-page' | 'email-campaign';
  options?: {
    includeAudioPlayer: boolean;
    generateChapters: boolean;
    addReflectionQuestions: boolean;
  };
}

/**
 * Automation workflow from audio
 */
export interface AutomationFromAudioAction {
  audioSessionId: string;
  workflowType: 'on-upload' | 'on-complete' | 'scheduled';
  actions: AutomationStep[];
}

/**
 * Automation workflow step
 */
export interface AutomationStep {
  type: 'transcribe' | 'publish' | 'notify' | 'backup' | 'social-share';
  params: Record<string, any>;
}

/**
 * Multi-track session (Phase 2)
 */
export interface MultiTrackSession extends AudioSession {
  tracks: AudioTrack[];
  mixdown?: AudioAsset;
}

/**
 * Individual audio track in multi-track session
 */
export interface AudioTrack {
  id: string;
  name: string;
  asset: AudioAsset;
  volume: number;        // 0.0 - 1.0
  pan: number;           // -1.0 (left) to 1.0 (right)
  muted: boolean;
  solo: boolean;
  effects: AudioEffect[];
}

/**
 * Audio effect configuration
 */
export interface AudioEffect {
  type: 'reverb' | 'delay' | 'chorus' | 'eq' | 'compressor';
  params: Record<string, number>;
  enabled: boolean;
}

/**
 * Session list filters
 */
export interface AudioSessionFilters {
  tags?: AudioTag[];
  category?: AudioCategory;
  dateRange?: {
    start: Date;
    end: Date;
  };
  type?: 'recorded' | 'uploaded';
  series?: string;
  collection?: string;
  search?: string;
}

/**
 * Session list sort options
 */
export interface AudioSessionSort {
  field: 'createdAt' | 'updatedAt' | 'title' | 'duration';
  order: 'asc' | 'desc';
}

/**
 * Paginated session list response
 */
export interface AudioSessionListResponse {
  sessions: AudioSession[];
  total: number;
  hasMore: boolean;
  nextOffset?: number;
}

/**
 * Share link configuration
 */
export interface ShareLinkConfig {
  expiresIn?: number;    // Seconds
  password?: string;
  allowDownload?: boolean;
  allowComments?: boolean;
}

/**
 * Share link response
 */
export interface ShareLinkResponse {
  shareUrl: string;
  expiresAt?: Date;
  token: string;
}

/**
 * Processing job status
 */
export interface ProcessingJob {
  id: string;
  sessionId: string;
  type: 'enhance' | 'transcode' | 'split-stems';
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress: number;      // 0-100
  estimatedTime?: number; // Seconds
  result?: {
    assetId?: string;
    error?: string;
  };
  createdAt: Date;
  completedAt?: Date;
}

/**
 * Waveform data for visualization
 */
export interface WaveformData {
  sessionId: string;
  peaks: number[];       // Normalized amplitude values
  duration: number;
  sampleRate: number;
}

/**
 * Recording session state
 */
export interface RecordingSession {
  isRecording: boolean;
  isPaused: boolean;
  duration: number;
  mediaRecorder?: MediaRecorder;
  audioChunks: Blob[];
}
