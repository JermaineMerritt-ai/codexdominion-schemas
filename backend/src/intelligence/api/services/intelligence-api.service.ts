/**
 * Intelligence API Service
 * 
 * Core business logic for Intelligence API v1:
 * - generateInsights(): Batch job that runs rules engine and creates/updates Insight records
 * - getInsightFeed(): Returns role-scoped, prioritized intelligence feed
 * - Type-specific getters: getAlerts(), getRecommendations(), getForecasts(), getOpportunities()
 * - updateInsightStatus(): Manages insight lifecycle (ACTIVE → ACKNOWLEDGED → RESOLVED → DISMISSED)
 * 
 * This service makes CodexDominion "talk back to leadership" with actionable intelligence.
 */

import { Injectable, Logger, NotFoundException, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { RulesEngineService } from './rules-engine.service';
import {
  GetFeedDto,
  UpdateInsightStatusDto,
  InsightFeedResponse,
  InsightDetail,
  AuthUserContext,
  RoleScopedFilter,
  BatchGenerationResult,
  RuleExecutionContext,
  InsightType,
  InsightStatus,
  InsightDomain,
  AudienceRole,
} from '../types/intelligence-api.types';
import { Prisma, Insight } from '@prisma/client';
import { runDailyIntelligenceJob } from '../../orchestration/daily-intelligence-job';

@Injectable()
export class IntelligenceApiService {
  private readonly logger = new Logger(IntelligenceApiService.name);

  constructor(
    private prisma: PrismaService,
    private rulesEngine: RulesEngineService
  ) {}

  // ==============================================================================
  // BATCH INSIGHT GENERATION (Scheduled Job)
  // ==============================================================================

  /**
   * Generate insights by evaluating all 47 rules
   * Called by cron job (daily or hourly)
   * 
   * HIGH-LEVEL FLOW:
   * 1. Collect data - Load youth, circles, regions, missions, curriculum with needed relations
   * 2. Run evaluators - For each domain, run its rules (Y1-Y7, C1-C7, etc.)
   * 3. Upsert insights - Use (rule_code + context keys) as natural identity to avoid duplicates
   * 4. Expire/resolve stale insights - If condition no longer true, auto-resolve/dismiss
   * 
   * Returns:
   * - Number of rules evaluated
   * - Number of insights created/updated
   * - Execution time
   */
  async generateInsights(): Promise<BatchGenerationResult> {
    this.logger.log('🔥 Starting batch insight generation');
    const startTime = Date.now();

    try {
      // Run the daily intelligence job orchestrator
      // This calls all 7 domain evaluators: Circle, Youth, Mission, Curriculum, Culture, Creator, Expansion
      const results = await runDailyIntelligenceJob(this.prisma);

      const executionTime = Date.now() - startTime;

      this.logger.log(
        `🔥 Batch complete: ${results.total} insights generated across all domains (${executionTime}ms)`
      );

      return {
        total_evaluated: results.circles + results.youth + results.missions + results.curriculum + results.culture + results.creators + results.expansion,
        total_triggered: results.total,
        insights_created: 0, // Individual domain evaluators handle persistence
        insights_updated: 0, // Individual domain evaluators handle persistence
        insights_expired: 0, // TODO: Implement stale insight resolution after batch
        execution_time_ms: executionTime,
        errors: [],
      };
    } catch (error) {
      this.logger.error('❌ Batch insight generation failed', error);
      throw error;
    }
  }

  /**
   * Upsert insight with duplicate detection
   * Uses (rule_code + context keys) as natural identity
   * 
   * Natural key strategy:
   * - For Youth rules: rule_code + user_id
   * - For Circle rules: rule_code + circle_id
   * - For Region rules: rule_code + region_id
   * - For Mission rules: rule_code + mission_id
   */
  private async upsertInsight(insightPayload: any): Promise<'created' | 'updated'> {
    // Extract natural key from context
    const naturalKey = this.extractNaturalKey(insightPayload.rule_code, insightPayload.context);

    // Build WHERE clause for duplicate detection
    const whereClause: Prisma.InsightWhereInput = {
      rule_code: insightPayload.rule_code,
      status: { in: [InsightStatus.ACTIVE, InsightStatus.ACKNOWLEDGED] },
    };

    // Add context-based filters (natural key)
    if (naturalKey.user_id) {
      whereClause.context = {
        path: ['user_id'],
        equals: naturalKey.user_id,
      } as any;
    } else if (naturalKey.circle_id) {
      whereClause.context = {
        path: ['circle_id'],
        equals: naturalKey.circle_id,
      } as any;
    } else if (naturalKey.region_id) {
      whereClause.context = {
        path: ['region_id'],
        equals: naturalKey.region_id,
      } as any;
    } else if (naturalKey.mission_id) {
      whereClause.context = {
        path: ['mission_id'],
        equals: naturalKey.mission_id,
      } as any;
    }

    // Check for existing insight
    const existingInsight = await this.prisma.insight.findFirst({
      where: whereClause,
    });

    if (existingInsight) {
      // Update existing insight (refresh message, context, timestamp)
      await this.prisma.insight.update({
        where: { id: existingInsight.id },
        data: {
          title: insightPayload.title,
          message: insightPayload.message,
          context: insightPayload.context as any,
          priority: insightPayload.priority, // Priority may change
          updated_at: new Date(),
        },
      });
      return 'updated';
    } else {
      // Create new insight
      await this.prisma.insight.create({
        data: {
          type: insightPayload.type,
          priority: insightPayload.priority,
          domain: insightPayload.domain,
          rule_code: insightPayload.rule_code,
          title: insightPayload.title,
          message: insightPayload.message,
          context: insightPayload.context as any,
          audience_role: insightPayload.audience_role,
          audience_scope_id: insightPayload.audience_scope_id,
          expires_at: insightPayload.expires_at,
        },
      });
      return 'created';
    }
  }

  /**
   * Extract natural key from context based on rule domain
   */
  private extractNaturalKey(ruleCode: string, context: any): {
    user_id?: string;
    circle_id?: string;
    region_id?: string;
    mission_id?: string;
  } {
    // Youth domain rules (Y1-Y7): user_id
    if (ruleCode.startsWith('Y')) {
      return { user_id: context.user_id || context.youth_id };
    }

    // Circle domain rules (C1-C7): circle_id
    if (ruleCode.startsWith('C')) {
      return { circle_id: context.circle_id };
    }

    // Culture/Expansion domain rules (CUL1-CUL7, E1-E7): region_id
    if (ruleCode.startsWith('CUL') || ruleCode.startsWith('E')) {
      return { region_id: context.region_id };
    }

    // Mission domain rules (M1-M7): mission_id
    if (ruleCode.startsWith('M')) {
      return { mission_id: context.mission_id };
    }

    // Curriculum/Creator domain rules (CU1-CU7, CR1-CR7): user_id
    if (ruleCode.startsWith('CU') || ruleCode.startsWith('CR')) {
      return { user_id: context.user_id || context.youth_id };
    }

    // Fallback: use user_id if available
    return { user_id: context.user_id || context.youth_id };
  }

  /**
   * Resolve stale insights (conditions no longer true)
   * 
   * Strategy: If a rule did NOT trigger this cycle, but an ACTIVE insight exists for it,
   * assume the condition resolved itself → mark as RESOLVED
   */
  private async resolveStaleInsights(evaluations: any[]): Promise<number> {
    const triggeredRuleCodes = new Set(
      evaluations.filter((e) => e.shouldTrigger).map((e) => e.rule_code)
    );

    const allRuleCodes = evaluations.map((e) => e.rule_code);
    const nonTriggeredRuleCodes = allRuleCodes.filter((code) => !triggeredRuleCodes.has(code));

    if (nonTriggeredRuleCodes.length === 0) {
      return 0;
    }

    // Auto-resolve insights for rules that didn't trigger
    const result = await this.prisma.insight.updateMany({
      where: {
        rule_code: { in: nonTriggeredRuleCodes },
        status: { in: [InsightStatus.ACTIVE, InsightStatus.ACKNOWLEDGED] },
        updated_at: { lt: new Date(Date.now() - 24 * 60 * 60 * 1000) }, // Only if not updated in last 24h
      },
      data: {
        status: InsightStatus.RESOLVED,
        updated_at: new Date(),
      },
    });

    if (result.count > 0) {
      this.logger.log(`✅ Auto-resolved ${result.count} stale insights (conditions no longer true)`);
    }

    return result.count;
  }

  /**
   * Expire insights past their expiration date
   */
  private async expireOldInsights(): Promise<number> {
    const result = await this.prisma.insight.updateMany({
      where: {
        expires_at: { lt: new Date() },
        status: { in: [InsightStatus.ACTIVE, InsightStatus.ACKNOWLEDGED] },
      },
      data: {
        status: InsightStatus.DISMISSED,
      },
    });

    return result.count;
  }

  // ==============================================================================
  // INTELLIGENCE FEED (Role-Scoped)
  // ==============================================================================

  /**
   * Get intelligence feed for authenticated user
   * Automatically filters by role + scope
   * Returns prioritized mix of alerts, recommendations, forecasts, opportunities
   */
  async getInsightFeed(filters: GetFeedDto, user: AuthUserContext): Promise<InsightFeedResponse> {
    const { type, domain, status = InsightStatus.ACTIVE, limit = 50, offset = 0 } = filters;

    // Build role-scoped WHERE clause
    const whereClause = this.buildRoleScopedQuery(user);

    // Add filters
    if (type) {
      whereClause.type = type;
    }
    if (domain) {
      whereClause.domain = domain;
    }
    whereClause.status = status;

    // Query insights
    const [insights, total] = await Promise.all([
      this.prisma.insight.findMany({
        where: whereClause,
        orderBy: [
          { priority: 'asc' }, // CRITICAL first
          { created_at: 'desc' },
        ],
        take: limit,
        skip: offset,
      }),
      this.prisma.insight.count({ where: whereClause }),
    ]);

    return {
      insights,
      total,
      has_more: offset + insights.length < total,
    };
  }

  /**
   * Get alerts only (type = ALERT)
   */
  async getAlerts(filters: GetFeedDto, user: AuthUserContext): Promise<InsightFeedResponse> {
    return this.getInsightFeed({ ...filters, type: InsightType.ALERT }, user);
  }

  /**
   * Get recommendations only (type = RECOMMENDATION)
   */
  async getRecommendations(filters: GetFeedDto, user: AuthUserContext): Promise<InsightFeedResponse> {
    return this.getInsightFeed({ ...filters, type: InsightType.RECOMMENDATION }, user);
  }

  /**
   * Get forecasts only (type = FORECAST)
   */
  async getForecasts(filters: GetFeedDto, user: AuthUserContext): Promise<InsightFeedResponse> {
    return this.getInsightFeed({ ...filters, type: InsightType.FORECAST }, user);
  }

  /**
   * Get opportunities only (type = OPPORTUNITY)
   */
  async getOpportunities(filters: GetFeedDto, user: AuthUserContext): Promise<InsightFeedResponse> {
    return this.getInsightFeed({ ...filters, type: InsightType.OPPORTUNITY }, user);
  }

  /**
   * Get single insight by ID (with auth check)
   */
  async getInsightById(id: string, user: AuthUserContext): Promise<InsightDetail> {
    const insight = await this.prisma.insight.findUnique({
      where: { id },
      include: {
        events: {
          orderBy: { created_at: 'desc' },
        },
      },
    });

    if (!insight) {
      throw new NotFoundException(`Insight ${id} not found`);
    }

    // Verify user has access to this insight
    if (!this.canAccessInsight(insight, user)) {
      throw new ForbiddenException('You do not have permission to view this insight');
    }

    return insight;
  }

  // ==============================================================================
  // INSIGHT LIFECYCLE MANAGEMENT
  // ==============================================================================

  /**
   * Update insight status (ACKNOWLEDGED, RESOLVED, DISMISSED)
   * Records action in InsightEvent audit trail
   */
  async updateInsightStatus(
    id: string,
    dto: UpdateInsightStatusDto,
    user: AuthUserContext
  ): Promise<InsightDetail> {
    // Get insight and verify access
    const insight = await this.getInsightById(id, user);

    // Update status
    const updated = await this.prisma.insight.update({
      where: { id },
      data: {
        status: dto.status,
        updated_at: new Date(),
      },
      include: {
        events: {
          orderBy: { created_at: 'desc' },
        },
      },
    });

    // Record action in audit trail
    await this.prisma.insightEvent.create({
      data: {
        insight_id: id,
        user_id: user.user_id,
        action: dto.status,
      },
    });

    this.logger.log(`Insight ${id} status updated to ${dto.status} by user ${user.user_id}`);

    return updated;
  }

  // ==============================================================================
  // ROLE-BASED FILTERING LOGIC
  // ==============================================================================

  /**
   * Build Prisma WHERE clause based on user role + scope
   * 
   * Rules:
   * - ADMIN / COUNCIL: See everything (all regions, all domains)
   * - REGIONAL_DIRECTOR: See their region only (CIRCLES, YOUTH, MISSIONS, CULTURE)
   * - AMBASSADOR: See EXPANSION domain for their outreach scope
   * - CAPTAIN: See their circle only (YOUTH, CIRCLES, MISSIONS)
   * - YOUTH: See personal insights only (future)
   */
  private buildRoleScopedQuery(user: AuthUserContext): Prisma.InsightWhereInput {
    const where: Prisma.InsightWhereInput = {};

    // ADMIN / COUNCIL: See everything
    if (user.roles.includes('ADMIN') || user.roles.includes('COUNCIL')) {
      return where; // No filters
    }

    // REGIONAL_DIRECTOR: Their region only
    if (user.roles.includes('REGIONAL_DIRECTOR') && user.region_id) {
      where.OR = [
        {
          audience_role: AudienceRole.REGIONAL_DIRECTOR,
          audience_scope_id: user.region_id,
        },
        {
          audience_role: AudienceRole.ADMIN, // Also see global insights
          audience_scope_id: null,
        },
      ];
      return where;
    }

    // AMBASSADOR: Expansion domain only
    if (user.roles.includes('AMBASSADOR')) {
      where.OR = [
        {
          audience_role: AudienceRole.AMBASSADOR,
          domain: InsightDomain.EXPANSION,
        },
        {
          audience_role: AudienceRole.ADMIN,
          audience_scope_id: null,
        },
      ];
      return where;
    }

    // CAPTAIN: Their circle only
    if (user.roles.includes('CAPTAIN') && user.circle_id) {
      where.OR = [
        {
          audience_role: AudienceRole.CAPTAIN,
          audience_scope_id: user.circle_id,
        },
        {
          audience_role: AudienceRole.ADMIN,
          audience_scope_id: null,
        },
      ];
      return where;
    }

    // YOUTH: Personal insights only (future)
    if (user.roles.includes('YOUTH')) {
      where.OR = [
        {
          audience_role: AudienceRole.YOUTH,
          audience_scope_id: user.user_id,
        },
      ];
      return where;
    }

    // Default: No access
    return { id: 'none' };
  }

  /**
   * Check if user can access specific insight
   */
  private canAccessInsight(insight: Insight, user: AuthUserContext): boolean {
    // ADMIN / COUNCIL: Access to everything
    if (user.roles.includes('ADMIN') || user.roles.includes('COUNCIL')) {
      return true;
    }

    // Check role + scope match
    if (insight.audience_role === AudienceRole.REGIONAL_DIRECTOR) {
      return user.roles.includes('REGIONAL_DIRECTOR') && user.region_id === insight.audience_scope_id;
    }

    if (insight.audience_role === AudienceRole.CAPTAIN) {
      return user.roles.includes('CAPTAIN') && user.circle_id === insight.audience_scope_id;
    }

    if (insight.audience_role === AudienceRole.AMBASSADOR) {
      return user.roles.includes('AMBASSADOR') && insight.domain === InsightDomain.EXPANSION;
    }

    if (insight.audience_role === AudienceRole.YOUTH) {
      return user.roles.includes('YOUTH') && user.user_id === insight.audience_scope_id;
    }

    // Global insights (audience_scope_id = null)
    if (insight.audience_scope_id === null) {
      return true;
    }

    return false;
  }

  // ==============================================================================
  // HELPER METHODS
  // ==============================================================================

  /**
   * Get current week number (simple implementation)
   */
  private getCurrentWeek(): number {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now.getTime() - start.getTime();
    return Math.floor(diff / (7 * 24 * 60 * 60 * 1000)) + 1;
  }
}
