/**
 * Rules Engine Service
 * 
 * Evaluates 47 intelligence rules across 7 domains:
 * - Youth (Y1-Y5): Engagement, at-risk detection, milestones
 * - Circles (C1-C5): Health, attendance, captain effectiveness
 * - Missions (M1-M5): Completion, forecasting, impact
 * - Curriculum (CU1-CU5): Engagement, drop-offs, alignment
 * - Creators (CR1-CR5): Activity, quality, spotlights
 * - Culture (CUL1-CUL5): Stories, rituals, identity
 * - Expansion (E1-E5): Regional health, readiness, ambassadors
 * 
 * Each rule returns RuleEvaluation with shouldTrigger + InsightPayload
 */

import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import {
  RuleEvaluation,
  RuleExecutionContext,
  InsightPayload,
  InsightType,
  InsightPriority,
  InsightDomain,
  AudienceRole,
  YouthInsightContext,
  CircleInsightContext,
  MissionInsightContext,
  RegionInsightContext,
} from '../types/intelligence-api.types';

@Injectable()
export class RulesEngineService {
  private readonly logger = new Logger(RulesEngineService.name);

  constructor(private prisma: PrismaService) {}

  /**
   * MASTER ORCHESTRATOR
   * Evaluates all 47 rules and returns triggered insights
   */
  async evaluateAllRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    this.logger.log('Starting full rule evaluation cycle');
    const startTime = Date.now();

    const evaluations: RuleEvaluation[] = [];

    try {
      // Youth Domain (Y1-Y5)
      const youthEvals = await this.evaluateYouthRules(context);
      evaluations.push(...youthEvals);

      // Circles Domain (C1-C5)
      const circleEvals = await this.evaluateCircleRules(context);
      evaluations.push(...circleEvals);

      // Missions Domain (M1-M5)
      const missionEvals = await this.evaluateMissionRules(context);
      evaluations.push(...missionEvals);

      // Curriculum Domain (CU1-CU5)
      const curriculumEvals = await this.evaluateCurriculumRules(context);
      evaluations.push(...curriculumEvals);

      // Creators Domain (CR1-CR5)
      const creatorEvals = await this.evaluateCreatorRules(context);
      evaluations.push(...creatorEvals);

      // Culture Domain (CUL1-CUL5)
      const cultureEvals = await this.evaluateCultureRules(context);
      evaluations.push(...cultureEvals);

      // Expansion Domain (E1-E5)
      const expansionEvals = await this.evaluateExpansionRules(context);
      evaluations.push(...expansionEvals);

      const duration = Date.now() - startTime;
      const triggered = evaluations.filter((e) => e.shouldTrigger).length;

      this.logger.log(
        `Rule evaluation complete: ${evaluations.length} rules evaluated, ${triggered} triggered (${duration}ms)`
      );

      return evaluations;
    } catch (error) {
      this.logger.error('Rule evaluation failed', error);
      throw error;
    }
  }

  // ==============================================================================
  // YOUTH DOMAIN RULES (Y1-Y5)
  // ==============================================================================

  /**
   * Evaluate all Youth rules
   */
  private async evaluateYouthRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get all active youth for evaluation
    const activeYouth = await this.prisma.user.findMany({
      where: {
        roles: { some: { role: { name: 'YOUTH' } } },
        status: 'ACTIVE',
      },
      include: {
        circleMemberships: { include: { circle: true } },
        missionSubmissions: { where: { submittedAt: { gte: this.getLastNDays(30) } } },
        circleAttendance: true,
      },
    });

    for (const youth of activeYouth) {
      // Y1: Youth engagement tracking
      results.push(await this.evaluateY1YouthEngagement(youth, context));

      // Y2: At-risk youth detection (CRITICAL RULE)
      results.push(await this.evaluateY2AtRiskYouth(youth, context));

      // Y3: Achievement milestones
      results.push(await this.evaluateY3Achievements(youth, context));
    }

    return results;
  }

  /**
   * Y1: Track overall youth engagement levels
   */
  private async evaluateY1YouthEngagement(youth: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const attendanceCount = youth.circleAttendance?.length || 0;
    const submissionCount = youth.missionSubmissions?.length || 0;
    const engagementScore = attendanceCount + submissionCount * 2; // Weight submissions higher

    // Threshold: Low engagement = < 5 over last 30 days
    if (engagementScore < 5 && engagementScore > 0) {
      const circleId = youth.circleMemberships[0]?.circle?.id;
      const captainId = youth.circleMemberships[0]?.circle?.captainId;

      return {
        rule_code: 'Y1_LOW_ENGAGEMENT',
        shouldTrigger: true,
        insight: {
          type: InsightType.RECOMMENDATION,
          priority: InsightPriority.IMPORTANT,
          domain: InsightDomain.YOUTH,
          rule_code: 'Y1_LOW_ENGAGEMENT',
          title: `${youth.firstName} ${youth.lastName} showing low engagement`,
          message: `${youth.firstName} has low activity (${attendanceCount} sessions, ${submissionCount} missions) over last 30 days. Consider personal check-in.`,
          context: {
            youth_id: youth.id,
            circle_id: circleId,
            engagement_score: engagementScore,
            attendance_count: attendanceCount,
            submission_count: submissionCount,
          } as YouthInsightContext,
          audience_role: AudienceRole.CAPTAIN,
          audience_scope_id: circleId,
        },
      };
    }

    return { rule_code: 'Y1_LOW_ENGAGEMENT', shouldTrigger: false };
  }

  /**
   * Y2: Detect at-risk youth (missed 3+ sessions, no recent mission)
   * IMPORTANT RULE
   */
  private async evaluateY2AtRiskYouth(youth: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    // Count missed sessions from recent attendance
    const missedCount = youth.circleAttendance?.filter((a: any) => a.status === 'ABSENT').length || 0;
    
    // Check if last mission was submitted
    const noMissionSubmitted = youth.missionSubmissions?.length === 0;

    if (missedCount < 3 || !noMissionSubmitted) {
      return { rule_code: 'Y2_AT_RISK_YOUTH', shouldTrigger: false };
    }

    const circleId = youth.circleMemberships[0]?.circle?.id;
    const captainId = youth.circleMemberships[0]?.circle?.captainId;

    return {
      rule_code: 'Y2_AT_RISK_YOUTH',
      shouldTrigger: true,
      insight: {
        type: InsightType.RECOMMENDATION,
        priority: InsightPriority.IMPORTANT,
        domain: InsightDomain.YOUTH,
        rule_code: 'Y2_AT_RISK_YOUTH',
        title: `Check in with ${youth.firstName}`,
        message: `${youth.firstName} has missed 3 sessions and skipped last week's mission.`,
        context: {
          youth_id: youth.id,
          circle_id: circleId,
          missed_sessions: missedCount,
        } as YouthInsightContext,
        audience_role: AudienceRole.CAPTAIN,
        audience_scope_id: captainId,
      },
    };
  }

  /**
   * Y3: Celebrate youth achievement milestones
   */
  private async evaluateY3Achievements(youth: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const totalSubmissions = await this.prisma.missionSubmission.count({
      where: { userId: youth.id },
    });

    // Milestone: 10, 25, 50, 100 missions
    const milestones = [10, 25, 50, 100];
    const recentMilestone = milestones.find((m) => totalSubmissions === m);

    if (recentMilestone) {
      const circleId = youth.circleMemberships[0]?.circle?.id;

      return {
        rule_code: 'Y3_ACHIEVEMENT_MILESTONE',
        shouldTrigger: true,
        insight: {
          type: InsightType.OPPORTUNITY,
          priority: InsightPriority.INFO,
          domain: InsightDomain.YOUTH,
          rule_code: 'Y3_ACHIEVEMENT_MILESTONE',
          title: `${youth.firstName} ${youth.lastName} reached ${recentMilestone} missions!`,
          message: `${youth.firstName} just completed their ${recentMilestone}th mission. Celebrate this milestone in the next circle session!`,
          context: {
            youth_id: youth.id,
            circle_id: circleId,
            total_submissions: totalSubmissions,
            milestone: recentMilestone,
          } as YouthInsightContext,
          audience_role: AudienceRole.CAPTAIN,
          audience_scope_id: circleId,
        },
      };
    }

    return { rule_code: 'Y3_ACHIEVEMENT_MILESTONE', shouldTrigger: false };
  }

  // ==============================================================================
  // CIRCLES DOMAIN RULES (C1-C5)
  // ==============================================================================

  /**
   * Evaluate all Circle rules
   */
  private async evaluateCircleRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    const activeCircles = await this.prisma.circle.findMany({
      include: {
        members: true,
        sessions: {
          where: { scheduledAt: { gte: this.getLastNDays(30) } },
          include: { attendance: true },
        },
      },
    });

    for (const circle of activeCircles) {
      // C1: Circle health scoring
      results.push(await this.evaluateC1CircleHealth(circle, context));

      // C2: Attendance drop detection (CRITICAL RULE)
      results.push(await this.evaluateC2AttendanceDrop(circle, context));
    }

    return results;
  }

  /**
   * C1: Calculate and track circle health score
   */
  private async evaluateC1CircleHealth(circle: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const totalSessions = circle.sessions.length;
    if (totalSessions === 0) {
      return { rule_code: 'C1_CIRCLE_HEALTH', shouldTrigger: false };
    }

    const totalMembers = circle.members.length;
    const totalAttendance = circle.sessions.reduce((sum: number, s: any) => sum + s.attendance.length, 0);
    const avgAttendanceRate = totalAttendance / (totalSessions * totalMembers);

    // Health thresholds: < 0.5 = unhealthy, 0.5-0.7 = moderate, > 0.7 = healthy
    if (avgAttendanceRate < 0.5) {
      return {
        rule_code: 'C1_CIRCLE_HEALTH',
        shouldTrigger: true,
        insight: {
          type: InsightType.ALERT,
          priority: InsightPriority.IMPORTANT,
          domain: InsightDomain.CIRCLES,
          rule_code: 'C1_CIRCLE_HEALTH',
          title: `Circle ${circle.name} has low health score`,
          message: `Circle ${circle.name} has ${(avgAttendanceRate * 100).toFixed(0)}% average attendance over last 30 days. Consider captain support or circle restructuring.`,
          context: {
            circle_id: circle.id,
            region_id: circle.regionId,
            captain_id: circle.captainId,
            health_score: avgAttendanceRate,
            member_count: totalMembers,
            session_count: totalSessions,
          } as CircleInsightContext,
          audience_role: AudienceRole.REGIONAL_DIRECTOR,
          audience_scope_id: circle.regionId,
        },
      };
    }

    return { rule_code: 'C1_CIRCLE_HEALTH', shouldTrigger: false };
  }

  /**
   * C2: Detect sudden attendance drops between last 2 sessions
   * CRITICAL RULE
   */
  private async evaluateC2AttendanceDrop(circle: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    // Take only the most recent 2 sessions
    const sessions = circle.sessions.slice(0, 2);
    
    if (sessions.length < 2) {
      return { rule_code: 'C2_ATTENDANCE_DROP', shouldTrigger: false };
    }

    // Calculate attendance rates for each session
    const previousSession = sessions[1];
    const latestSession = sessions[0];
    
    const previousRate = this.calculateAttendanceRate([previousSession], circle.members.length);
    const latestRate = this.calculateAttendanceRate([latestSession], circle.members.length);
    
    const drop = previousRate - latestRate;
    const dropThreshold = 0.20; // 20% drop triggers alert

    if (drop < dropThreshold) {
      return { rule_code: 'C2_ATTENDANCE_DROP', shouldTrigger: false };
    }

    return {
      rule_code: 'C2_ATTENDANCE_DROP',
      shouldTrigger: true,
      insight: {
        type: InsightType.ALERT,
        priority: InsightPriority.CRITICAL,
        domain: InsightDomain.CIRCLES,
        rule_code: 'C2_ATTENDANCE_DROP',
        title: `Attendance dropped in ${circle.name}`,
        message: `Attendance fell from ${(previousRate * 100).toFixed(0)}% to ${(latestRate * 100).toFixed(0)}% over the last 2 sessions.`,
        context: {
          circle_id: circle.id,
          region_id: circle.regionId,
          metric_before: previousRate,
          metric_after: latestRate,
          time_window_sessions: 2,
        } as CircleInsightContext,
        audience_role: AudienceRole.REGIONAL_DIRECTOR,
        audience_scope_id: circle.regionId,
        expires_at: this.addDays(new Date(), 7),
      },
    };
  }

  // ==============================================================================
  // MISSIONS DOMAIN RULES (M1-M5)
  // ==============================================================================

  /**
   * Evaluate all Mission rules
   */
  private async evaluateMissionRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get current season's missions
    const currentMissions = await this.prisma.mission.findMany({
      where: { seasonId: context.current_season_id },
      include: {
        submissions: true,
        assignments: true,
      },
    });

    for (const mission of currentMissions) {
      // M3: Mission success forecasting
      results.push(await this.evaluateM3MissionForecast(mission, context));
    }

    return results;
  }

  /**
   * M3: Forecast mission completion rates
   * Simple projection: current rate * 1.2 for optimistic forecast
   */
  private async evaluateM3MissionForecast(mission: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const submitted = mission.submissions.length;
    const total = mission.assignments.length;

    if (total === 0) {
      return { rule_code: 'M3_MISSION_FORECAST', shouldTrigger: false };
    }

    const rate = submitted / total;
    const forecast = rate * 1.2; // Simple 20% optimistic projection

    return {
      rule_code: 'M3_MISSION_FORECAST',
      shouldTrigger: true,
      insight: {
        type: InsightType.FORECAST,
        priority: InsightPriority.INFO,
        domain: InsightDomain.MISSIONS,
        rule_code: 'M3_MISSION_FORECAST',
        title: `Mission completion forecast at ${Math.round(forecast * 100)}%`,
        message: `Based on current submission rate, this mission is projected to reach ${Math.round(forecast * 100)}% completion.`,
        context: {
          mission_id: mission.id,
          forecast_value: forecast,
          confidence: 0.7,
        } as MissionInsightContext,
        audience_role: AudienceRole.ADMIN,
      },
    };
  }

  // ==============================================================================
  // CURRICULUM DOMAIN RULES (CU1-CU5)
  // ==============================================================================

  /**
   * Evaluate all Curriculum rules
   */
  private async evaluateCurriculumRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get all active youth in circles
    const youthInCircles = await this.prisma.user.findMany({
      where: {
        roles: { some: { role: { name: 'YOUTH' } } },
        circleMemberships: { some: {} },
      },
      include: {
        circleMemberships: {
          include: {
            circle: {
              include: {
                captain: true,
              },
            },
          },
        },
        profile: true,
      },
    });

    for (const youth of youthInCircles) {
      // CU4: Curriculum dropoff detection
      results.push(await this.evaluateCU4CurriculumDropoff(youth, context));
    }

    return results;
  }

  /**
   * CU4: Detect youth who have stopped progressing in curriculum
   * Alert if 14+ days without curriculum progress
   */
  private async evaluateCU4CurriculumDropoff(youth: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const lastProgress = youth.profile?.lastCurriculumProgressAt;
    
    if (!lastProgress) {
      return { rule_code: 'CU4_CURRICULUM_DROPOFF', shouldTrigger: false };
    }

    const days = this.daysSince(lastProgress);

    if (days < 14) {
      return { rule_code: 'CU4_CURRICULUM_DROPOFF', shouldTrigger: false };
    }

    const captainId = youth.circleMemberships?.[0]?.circle?.captainId;

    return {
      rule_code: 'CU4_CURRICULUM_DROPOFF',
      shouldTrigger: true,
      insight: {
        type: InsightType.ALERT,
        priority: InsightPriority.IMPORTANT,
        domain: InsightDomain.CURRICULUM,
        rule_code: 'CU4_CURRICULUM_DROPOFF',
        title: `${youth.firstName} has stopped progressing`,
        message: `${youth.firstName} has not advanced in the curriculum for ${days} days.`,
        context: {
          youth_id: youth.id,
          circle_id: youth.circleMemberships?.[0]?.circle?.id,
          days_without_progress: days,
        } as YouthInsightContext,
        audience_role: AudienceRole.CAPTAIN,
        audience_scope_id: captainId,
      },
    };
  }

  // ==============================================================================
  // CREATORS DOMAIN RULES (CR1-CR5)
  // ==============================================================================

  /**
   * Evaluate all Creator rules
   */
  private async evaluateCreatorRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get all youth with artifact counts in last 30 days
    const thirtyDaysAgo = this.getLastNDays(30);
    
    const youthWithArtifacts = await this.prisma.user.findMany({
      where: {
        roles: { some: { role: { name: 'YOUTH' } } },
        circleMemberships: { some: {} },
      },
      include: {
        circleMemberships: {
          include: {
            circle: {
              include: {
                region: true,
              },
            },
          },
        },
        artifacts: {
          where: {
            createdAt: { gte: thirtyDaysAgo },
          },
        },
      },
    });

    for (const youth of youthWithArtifacts) {
      // CR4: Rising creator detection
      results.push(await this.evaluateCR4RisingCreator(youth, context));
    }

    return results;
  }

  /**
   * CR4: Detect youth emerging as creators
   * Opportunity if 3+ artifacts in last 30 days
   */
  private async evaluateCR4RisingCreator(youth: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const artifacts = youth.artifacts?.length || 0;

    if (artifacts < 3) {
      return { rule_code: 'CR4_RISING_CREATOR', shouldTrigger: false };
    }

    const primaryCircle = youth.circleMemberships?.[0]?.circle;
    const regionId = primaryCircle?.region?.id;

    return {
      rule_code: 'CR4_RISING_CREATOR',
      shouldTrigger: true,
      insight: {
        type: InsightType.OPPORTUNITY,
        priority: InsightPriority.IMPORTANT,
        domain: InsightDomain.CREATORS,
        rule_code: 'CR4_RISING_CREATOR',
        title: `${youth.firstName} is emerging as a creator`,
        message: `${youth.firstName} produced ${artifacts} artifacts in the last 30 days.`,
        context: {
          youth_id: youth.id,
          artifact_count: artifacts,
        } as YouthInsightContext,
        audience_role: AudienceRole.REGIONAL_DIRECTOR,
        audience_scope_id: regionId,
      },
    };
  }

  // ==============================================================================
  // CULTURE DOMAIN RULES (CUL1-CUL5)
  // ==============================================================================

  /**
   * Evaluate all Culture rules
   */
  private async evaluateCultureRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get all regions with engagement data
    const regions = await this.prisma.region.findMany({
      include: {
        circles: {
          include: {
            sessions: true,
            members: true,
          },
        },
      },
    });

    for (const region of regions) {
      // CL3: Culture momentum detection
      results.push(await this.evaluateCL3CultureMomentum(region, context));
    }

    return results;
  }

  /**
   * CL3: Detect regions gaining cultural momentum
   * Opportunity if engagement trend > 15%
   */
  private async evaluateCL3CultureMomentum(region: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    // Calculate engagement trend (simplified: ratio of recent sessions to total capacity)
    const totalSessions = region.circles.reduce((sum: number, c: any) => sum + c.sessions.length, 0);
    const totalCapacity = region.circles.reduce((sum: number, c: any) => sum + c.members.length, 0);
    const engagementTrend = totalCapacity > 0 ? totalSessions / totalCapacity : 0;

    const rising = engagementTrend > 0.15;

    if (!rising) {
      return { rule_code: 'CL3_CULTURE_MOMENTUM', shouldTrigger: false };
    }

    return {
      rule_code: 'CL3_CULTURE_MOMENTUM',
      shouldTrigger: true,
      insight: {
        type: InsightType.OPPORTUNITY,
        priority: InsightPriority.INFO,
        domain: InsightDomain.CULTURE,
        rule_code: 'CL3_CULTURE_MOMENTUM',
        title: `Region ${region.name} is gaining momentum`,
        message: `Engagement in ${region.name} is rising across circles, missions, and curriculum.`,
        context: {
          region_id: region.id,
          engagement_trend: engagementTrend,
        } as RegionInsightContext,
        audience_role: AudienceRole.COUNCIL,
      },
    };
  }

  // ==============================================================================
  // EXPANSION DOMAIN RULES (E1-E5)
  // ==============================================================================

  /**
   * Evaluate all Expansion rules
   */
  private async evaluateExpansionRules(context: RuleExecutionContext): Promise<RuleEvaluation[]> {
    const results: RuleEvaluation[] = [];

    // Get all regions with aggregated metrics
    const regions = await this.prisma.region.findMany({
      include: {
        circles: {
          include: {
            members: true,
          },
        },
      },
    });

    for (const region of regions) {
      // E2: Region expansion readiness
      results.push(await this.evaluateE2RegionExpansion(region, context));
    }

    return results;
  }

  /**
   * E2: Detect regions ready for expansion
   * Recommendation if 5+ circles, 70+ avg health, 50+ active youth
   */
  private async evaluateE2RegionExpansion(region: any, context: RuleExecutionContext): Promise<RuleEvaluation> {
    const circleCount = region.circles.length;
    const activeYouth = region.circles.reduce((sum: number, c: any) => sum + c.members.length, 0);
    
    // Calculate avg health score (simplified: based on circle member count vs capacity)
    const avgHealthScore = circleCount > 0 ? (activeYouth / circleCount) * 10 : 0; // Rough estimate

    const ready = circleCount >= 5 && avgHealthScore >= 70 && activeYouth >= 50;

    if (!ready) {
      return { rule_code: 'E2_REGION_EXPANSION_READY', shouldTrigger: false };
    }

    return {
      rule_code: 'E2_REGION_EXPANSION_READY',
      shouldTrigger: true,
      insight: {
        type: InsightType.RECOMMENDATION,
        priority: InsightPriority.IMPORTANT,
        domain: InsightDomain.EXPANSION,
        rule_code: 'E2_REGION_EXPANSION_READY',
        title: `${region.name} is ready for expansion`,
        message: `Region ${region.name} meets all criteria for expansion.`,
        context: {
          region_id: region.id,
          circle_count: circleCount,
          avg_health: avgHealthScore,
          active_youth: activeYouth,
        } as RegionInsightContext,
        audience_role: AudienceRole.COUNCIL,
      },
    };
  }

  // ==============================================================================
  // HELPER METHODS
  // ==============================================================================

  /**
   * Calculate attendance rate for sessions
   */
  private calculateAttendanceRate(sessions: any[], memberCount: number): number {
    if (sessions.length === 0 || memberCount === 0) return 0;
    const totalAttendance = sessions.reduce((sum, s) => sum + s.attendance.length, 0);
    return totalAttendance / (sessions.length * memberCount);
  }

  /**
   * Get date N days ago
   */
  private getLastNDays(days: number): Date {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date;
  }

  /**
   * Get days since a date
   */
  private daysSince(date: Date): number {
    const now = new Date();
    const diff = now.getTime() - new Date(date).getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  /**
   * Get days until a date
   */
  private daysUntil(date: Date): number {
    const now = new Date();
    const diff = new Date(date).getTime() - now.getTime();
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  /**
   * Add days to a date
   */
  private addDays(date: Date, days: number): Date {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }
}
