/**
 * Intelligence API V1 Type Definitions
 * 
 * Types for the 47-rule intelligence system that generates:
 * - Alerts (urgent issues)
 * - Recommendations (actionable suggestions)
 * - Forecasts (future projections)
 * - Opportunities (positive signals)
 * 
 * Powers role-scoped intelligence feeds in Empire Dashboard.
 */

import { 
  InsightType, 
  InsightPriority, 
  InsightDomain, 
  AudienceRole, 
  InsightStatus,
  Insight as PrismaInsight,
  InsightEvent as PrismaInsightEvent
} from '@prisma/client';

// ==============================================================================
// CORE INSIGHT TYPES
// ==============================================================================

/**
 * Full Insight with all metadata
 * Returned by GET /insights/:id
 */
export interface InsightDetail extends PrismaInsight {
  events?: InsightEvent[];  // Optional audit trail
}

/**
 * Insight Event (audit trail)
 * Tracks leadership actions on insights
 */
export interface InsightEvent extends PrismaInsightEvent {}

/**
 * Insight context payload structure
 * JSON field contains entity references
 */
export interface InsightContext {
  // Entity references
  user_id?: string;
  circle_id?: string;
  region_id?: string;
  mission_id?: string;
  curriculum_id?: string;
  creator_id?: string;
  
  // Metrics for rules
  metric_before?: number;
  metric_after?: number;
  time_window_weeks?: number;
  forecast_value?: number;
  confidence?: number;
  threshold?: number;
  
  // Additional metadata
  [key: string]: any;
}

// ==============================================================================
// RULE ENGINE TYPES
// ==============================================================================

/**
 * Rule Evaluation Result
 * Returned by each rule evaluation method
 */
export interface RuleEvaluation {
  rule_code: string;            // e.g., Y2_AT_RISK_YOUTH
  shouldTrigger: boolean;       // Did rule conditions pass?
  insight?: InsightPayload;     // Insight to create if triggered
}

/**
 * Insight creation payload (before DB insert)
 */
export type InsightPayload = {
  type: "ALERT" | "RECOMMENDATION" | "FORECAST" | "OPPORTUNITY"
  priority: "CRITICAL" | "IMPORTANT" | "INFO"
  domain: "YOUTH" | "CIRCLES" | "MISSIONS" | "CURRICULUM" | "CULTURE" | "CREATORS" | "EXPANSION"
  rule_code: string
  title: string
  message: string
  context: Record<string, any>
  audience_role: "ADMIN" | "COUNCIL" | "REGIONAL_DIRECTOR" | "AMBASSADOR" | "CAPTAIN" | "YOUTH"
  audience_scope_id?: string | null
  expires_at?: Date | null
}

/**
 * Evaluator function type
 * Takes input data and returns an InsightPayload if conditions are met, null otherwise
 */
export type Evaluator<TInput> = (input: TInput) => InsightPayload | null

/**
 * Rule configuration metadata
 * Can be extended for dynamic rule tuning
 */
export interface RuleConfig {
  rule_code: string;
  enabled: boolean;
  thresholds?: Record<string, number>;
  schedule?: string;  // Cron schedule for batch evaluation
}

/**
 * Rule execution context
 * Data available to all rules during evaluation
 */
export interface RuleExecutionContext {
  current_season_id?: string;
  current_week?: number;
  evaluation_timestamp: Date;
  
  // Cached analytics for performance
  active_youth_count?: number;
  active_circles_count?: number;
  active_regions_count?: number;
}

// ==============================================================================
// API REQUEST/RESPONSE TYPES
// ==============================================================================

/**
 * Query parameters for GET /intelligence/feed
 */
export interface GetFeedDto {
  type?: InsightType;       // Filter by type
  domain?: InsightDomain;   // Filter by domain
  status?: InsightStatus;   // Filter by status (default: ACTIVE)
  limit?: number;           // Max results (default: 50)
  offset?: number;          // Pagination offset
}

/**
 * Update insight status (PATCH /insights/:id)
 */
export interface UpdateInsightStatusDto {
  status: InsightStatus;    // New status: ACKNOWLEDGED, RESOLVED, DISMISSED
}

/**
 * Intelligence feed response
 * Array of insights with metadata
 */
export interface InsightFeedResponse {
  insights: PrismaInsight[];
  total: number;
  has_more: boolean;
}

/**
 * Insight summary for dashboard cards
 */
export interface InsightSummary {
  total_active: number;
  by_priority: {
    critical: number;
    important: number;
    info: number;
  };
  by_type: {
    alerts: number;
    recommendations: number;
    forecasts: number;
    opportunities: number;
  };
  by_domain: Record<InsightDomain, number>;
}

// ==============================================================================
// ROLE-BASED FILTERING TYPES
// ==============================================================================

/**
 * User context for role-based filtering
 * Extracted from JWT token
 */
export interface AuthUserContext {
  user_id: string;
  email: string;
  roles: string[];  // e.g., ['REGIONAL_DIRECTOR', 'AMBASSADOR']
  
  // Scope identifiers (if applicable)
  region_id?: string;   // For REGIONAL_DIRECTOR
  circle_id?: string;   // For CAPTAIN
}

/**
 * Prisma WHERE clause for role-scoped queries
 */
export interface RoleScopedFilter {
  AND?: any[];
  OR?: any[];
  audience_role?: AudienceRole | { in: AudienceRole[] };
  audience_scope_id?: string | { in: string[] };
  status?: InsightStatus;
  expires_at?: { gt: Date } | null;
}

// ==============================================================================
// ANALYTICS & REPORTING TYPES
// ==============================================================================

/**
 * Leadership responsiveness metrics
 * How quickly insights are acknowledged/resolved
 */
export interface LeadershipResponsivenessReport {
  avg_time_to_acknowledge_hours: number;
  avg_time_to_resolve_days: number;
  total_active_insights: number;
  total_resolved_insights: number;
  dismissal_rate: number;  // % of insights dismissed
}

/**
 * Rule effectiveness metrics
 * Which rules generate most value
 */
export interface RuleEffectivenessReport {
  rule_code: string;
  total_triggered: number;
  avg_resolution_days: number;
  dismissal_rate: number;
  impact_score: number;  // Custom metric
}

// ==============================================================================
// BATCH JOB TYPES
// ==============================================================================

/**
 * Batch insight generation result
 * Returned by intelligence-api.service.generateInsights()
 */
export interface BatchGenerationResult {
  total_evaluated: number;        // Total rules evaluated
  total_triggered: number;        // Rules that passed conditions
  insights_created: number;       // New insights inserted
  insights_updated: number;       // Existing insights updated
  insights_expired: number;       // Insights marked expired
  execution_time_ms: number;
  errors: string[];
}

/**
 * Scheduled job configuration
 * For cron/scheduler setup
 */
export interface IntelligenceJobConfig {
  schedule: string;               // Cron expression (e.g., '0 6 * * *')
  enabled: boolean;
  concurrent_execution: boolean;  // Allow overlapping jobs?
  timeout_minutes: number;
}

// ==============================================================================
// DOMAIN-SPECIFIC TYPES (for rule clarity)
// ==============================================================================

/**
 * Youth-specific insight context
 */
export interface YouthInsightContext extends InsightContext {
  youth_id: string;
  circle_id?: string;
  missed_sessions?: number;
  last_submission_date?: string;
  engagement_score?: number;
}

/**
 * Circle-specific insight context
 */
export interface CircleInsightContext extends InsightContext {
  circle_id: string;
  region_id?: string;
  captain_id?: string;
  attendance_rate?: number;
  member_count?: number;
  health_score?: number;
}

/**
 * Mission-specific insight context
 */
export interface MissionInsightContext extends InsightContext {
  mission_id: string;
  completion_rate?: number;
  submission_count?: number;
  difficulty_score?: number;
  forecast_completion_rate?: number;
}

/**
 * Region-specific insight context
 * Used by Culture and Expansion domain rules
 */
export interface RegionInsightContext extends InsightContext {
  region_id: string;
  region_name?: string;
  director_id?: string;
  director_name?: string;
  
  // Region-specific metrics
  circles_count?: number;
  active_youth_count?: number;
  total_youth_count?: number;
  health_score?: number;
  engagement_rate?: number;
  engagement_trend?: number;  // Change over time_window_weeks
  expansion_ready?: boolean;
}

// ==============================================================================
// HELPER TYPES
// ==============================================================================

/**
 * Pagination metadata
 */
export interface PaginationMeta {
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

/**
 * Standard API response wrapper
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  meta?: PaginationMeta;
}

// ==============================================================================
// EXPORTS
// ==============================================================================

export {
  InsightType,
  InsightPriority,
  InsightDomain,
  AudienceRole,
  InsightStatus,
  PrismaInsight,
  PrismaInsightEvent
};
