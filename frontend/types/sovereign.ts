/**
 * 👑 SOVEREIGN TYPE DEFINITIONS 🏛️
 * TypeScript models for CodexDominion Sovereign System
 * The Merritt Method™ - Eternal Kingdom Architecture
 */

// ============================================================================
// ENUMS
// ============================================================================

export enum CrownType {
  DEVOTIONAL = 'devotional',
  JOURNAL = 'journal',
  BLUEPRINT = 'blueprint',
  BUNDLE = 'bundle',
}

export enum ScrollEvent {
  CHRISTMAS = 'christmas',
  NEW_YEAR = 'new_year',
  VALENTINE = 'valentine',
  EASTER = 'easter',
  MOTHER_DAY = 'mother_day',
  FATHER_DAY = 'father_day',
  INDEPENDENCE_DAY = 'independence_day',
  LABOR_DAY = 'labor_day',
  BACK_TO_SCHOOL = 'back_to_school',
  HALLOWEEN = 'halloween',
  THANKSGIVING = 'thanksgiving',
  BLACK_FRIDAY = 'black_friday',
  CYBER_MONDAY = 'cyber_monday',
  CUSTOM = 'custom',
}

export enum HymnType {
  DAILY = 'daily',
  SEASONAL = 'seasonal',
  EPOCHAL = 'epochal',
}

export enum CapsuleFormat {
  TEXT = 'text',
  IMAGE = 'image',
  VIDEO = 'video',
  CAROUSEL = 'carousel',
  EMAIL = 'email',
  STORY = 'story',
}

export enum Platform {
  THREADS = 'threads',
  INSTAGRAM = 'instagram',
  YOUTUBE = 'youtube',
  TIKTOK = 'tiktok',
  FACEBOOK = 'facebook',
  TWITTER = 'twitter',
  LINKEDIN = 'linkedin',
}

export enum LedgerType {
  ORDER = 'order',
  REVENUE = 'revenue',
  REFUND = 'refund',
  CUSTOMER = 'customer',
}

export enum ArchiveType {
  REPLAY_CAPSULE = 'replay_capsule',
  HEIRS_DOCUMENTATION = 'heirs_documentation',
  COUNCIL_REPORT = 'council_report',
  EPOCHAL_RECORD = 'epochal_record',
}

// ============================================================================
// INTERFACES
// ============================================================================

/**
 * 👑 Crown (Product/Bundle)
 */
export interface Crown {
  id: string;
  name: string;
  type: CrownType;
  price: number;
  description: string;
  features: string[];
  digital_assets: string[];
  created_at: Date;
  updated_at: Date;
}

/**
 * 📜 Scroll (Campaign Script)
 */
export interface Scroll {
  id: string;
  name: string;
  event: ScrollEvent;
  start_date: Date;
  end_date: Date;
  discount_code: string;
  discount_percentage: number;
  target_crowns: string[]; // Crown IDs
  script_templates: {
    announcement: string;
    daily_reminder: string;
    last_chance: string;
  };
  performance_metrics: {
    impressions: number;
    clicks: number;
    conversions: number;
    revenue: number;
  };
  active: boolean;
}

/**
 * 🎵 Hymn (Broadcast Cycle)
 */
export interface Hymn {
  id: string;
  name: string;
  type: HymnType;
  frequency: 'hourly' | 'daily' | 'weekly' | 'monthly';
  schedule: HymnScheduleItem[];
  active: boolean;
  last_broadcast?: Date;
  next_broadcast?: Date;
}

export interface HymnScheduleItem {
  time: string;
  platforms: Platform[];
  content_type: string;
}

/**
 * 📦 Capsule (Content Unit)
 */
export interface Capsule {
  id: string;
  title: string;
  type: string;
  format: CapsuleFormat;
  content: {
    text: string;
    media_urls: string[];
    cta: string;
    link: string;
  };
  platforms: Platform[];
  hymn_id: string;
  published_at?: Date;
  performance: {
    views: number;
    likes: number;
    comments: number;
    shares: number;
    clicks: number;
  };
}

/**
 * 📊 Ledger Entry (Financial Record)
 */
export interface LedgerEntry {
  id: string;
  ledger_type: LedgerType;
  timestamp: Date;
  crown_id: string;
  customer_id: string;
  amount: number;
  currency: string;
  status: 'pending' | 'completed' | 'refunded';
  payment_method: string;
  metadata: {
    source?: string;
    campaign_id?: string;
    notes?: string;
    [key: string]: any;
  };
}

/**
 * 🏛️ Eternal Archive (Legacy Preservation)
 */
export interface EternalArchive {
  id: string;
  type: ArchiveType;
  period_start: Date;
  period_end: Date;
  contents: {
    capsules: Capsule[];
    scrolls: Scroll[];
    ledger_summary: LedgerSummary;
    hymn_performance: HymnMetrics;
    milestones: Milestone[];
  };
  retention: 'eternal';
  access: {
    heirs: boolean;
    councils: boolean;
    public: boolean;
  };
  created_at: Date;
}

export interface LedgerSummary {
  total_revenue: number;
  total_orders: number;
  average_order_value: number;
}

export interface HymnMetrics {
  total_broadcasts: number;
  total_capsules: number;
  average_engagement: number;
}

export interface Milestone {
  date: string;
  milestone: string;
}

// ============================================================================
// API REQUEST/RESPONSE TYPES
// ============================================================================

/**
 * Request to forge a new Crown
 */
export interface ForgeCrownRequest {
  name: string;
  type: CrownType;
  price: number;
  description: string;
  features: string[];
}

/**
 * Request to unfurl a new Scroll
 */
export interface UnfurlScrollRequest {
  name: string;
  event: ScrollEvent;
  start_date: string;
  end_date: string;
  discount_code: string;
  discount_percentage: number;
  target_crowns: string[];
}

/**
 * Request to compose a new Hymn
 */
export interface ComposeHymnRequest {
  name: string;
  type: HymnType;
  frequency: string;
  schedule: HymnScheduleItem[];
}

/**
 * Request to seal a new Capsule
 */
export interface SealCapsuleRequest {
  title: string;
  type: string;
  format: CapsuleFormat;
  content: {
    text: string;
    media_urls?: string[];
    cta?: string;
    link?: string;
  };
  platforms: Platform[];
  hymn_id: string;
}

/**
 * Request to inscribe a Ledger entry
 */
export interface InscribeLedgerRequest {
  ledger_type: LedgerType;
  crown_id: string;
  customer_id: string;
  amount: number;
  status: string;
  payment_method: string;
  metadata?: Record<string, any>;
}

/**
 * Request to enshrine in Eternal Archive
 */
export interface EnshrineArchiveRequest {
  archive_type: ArchiveType;
  period_start: string;
  period_end: string;
}

/**
 * API Response wrapper
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// ============================================================================
// DASHBOARD STATE TYPES
// ============================================================================

export interface DashboardState {
  crowns: Crown[];
  scrolls: Scroll[];
  hymns: Hymn[];
  capsules: Capsule[];
  ledgers: LedgerEntry[];
  archives: EternalArchive[];
  loading: boolean;
  error: string | null;
}

export interface SovereignMetrics {
  total_revenue: number;
  total_orders: number;
  total_posts: number;
  engagement_rate: number;
  active_scrolls: number;
  active_hymns: number;
  total_archives: number;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

/**
 * Partial Crown for updates
 */
export type CrownUpdate = Partial<Omit<Crown, 'id' | 'created_at'>>;

/**
 * Scroll with computed properties
 */
export type ScrollWithStatus = Scroll & {
  is_active: boolean;
  days_remaining: number;
  performance_summary: string;
};

/**
 * Hymn with next broadcast info
 */
export type HymnWithSchedule = Hymn & {
  upcoming_broadcasts: Date[];
  total_broadcasts_count: number;
};

/**
 * Capsule with engagement metrics
 */
export type CapsuleWithEngagement = Capsule & {
  engagement_rate: number;
  total_engagement: number;
};

/**
 * Archive with file size
 */
export type ArchiveWithMetadata = EternalArchive & {
  file_size_mb: number;
  download_url: string;
};

// ============================================================================
// VALIDATION SCHEMAS (for use with Zod or similar)
// ============================================================================

export const CROWN_TYPES = Object.values(CrownType);
export const SCROLL_EVENTS = Object.values(ScrollEvent);
export const HYMN_TYPES = Object.values(HymnType);
export const CAPSULE_FORMATS = Object.values(CapsuleFormat);
export const PLATFORMS = Object.values(Platform);
export const LEDGER_TYPES = Object.values(LedgerType);
export const ARCHIVE_TYPES = Object.values(ArchiveType);

// ============================================================================
// CONSTANTS
// ============================================================================

export const CURRENCY = 'USD' as const;
export const RETENTION_ETERNAL = 'eternal' as const;

export const SCROLL_EVENT_LABELS: Record<ScrollEvent, string> = {
  [ScrollEvent.CHRISTMAS]: '🎄 Christmas',
  [ScrollEvent.NEW_YEAR]: '🎆 New Year',
  [ScrollEvent.VALENTINE]: '💝 Valentine\'s Day',
  [ScrollEvent.EASTER]: '🐣 Easter',
  [ScrollEvent.MOTHER_DAY]: '👩 Mother\'s Day',
  [ScrollEvent.FATHER_DAY]: '👨 Father\'s Day',
  [ScrollEvent.INDEPENDENCE_DAY]: '🇺🇸 Independence Day',
  [ScrollEvent.LABOR_DAY]: '⚒️ Labor Day',
  [ScrollEvent.BACK_TO_SCHOOL]: '🎒 Back to School',
  [ScrollEvent.HALLOWEEN]: '🎃 Halloween',
  [ScrollEvent.THANKSGIVING]: '🦃 Thanksgiving',
  [ScrollEvent.BLACK_FRIDAY]: '🛍️ Black Friday',
  [ScrollEvent.CYBER_MONDAY]: '💻 Cyber Monday',
  [ScrollEvent.CUSTOM]: '📅 Custom Event',
};

export const PLATFORM_LABELS: Record<Platform, string> = {
  [Platform.THREADS]: 'Threads',
  [Platform.INSTAGRAM]: 'Instagram',
  [Platform.YOUTUBE]: 'YouTube',
  [Platform.TIKTOK]: 'TikTok',
  [Platform.FACEBOOK]: 'Facebook',
  [Platform.TWITTER]: 'Twitter',
  [Platform.LINKEDIN]: 'LinkedIn',
};

export const HYMN_TYPE_LABELS: Record<HymnType, string> = {
  [HymnType.DAILY]: '🔥 Daily Hymn',
  [HymnType.SEASONAL]: '🎄 Seasonal Hymn',
  [HymnType.EPOCHAL]: '🏛️ Epochal Hymn',
};

export const CROWN_TYPE_LABELS: Record<CrownType, string> = {
  [CrownType.DEVOTIONAL]: '📖 Devotional',
  [CrownType.JOURNAL]: '📔 Journal',
  [CrownType.BLUEPRINT]: '📐 Blueprint',
  [CrownType.BUNDLE]: '📦 Bundle',
};
