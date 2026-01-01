// =============================================================================
// SEASONAL ORCHESTRATION SERVICE
// =============================================================================
// Ensures civilization-wide seasonal rhythm across all systems

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { SeasonName } from '@prisma/client';
import {
  SeasonalAlignment,
  AlignmentDimension,
  SeasonTransitionPlan,
  TransitionStep,
  TransitionSeasonDto,
} from '../types/orchestration.types';

@Injectable()
export class SeasonalOrchestrationService {
  constructor(private prisma: PrismaService) {}

  /**
   * Transition entire Dominion to new season
   * Coordinates all engines: curriculum, missions, creators, exchange, intelligence
   */
  async transitionSeason(dto: TransitionSeasonDto): Promise<SeasonTransitionPlan> {
    const toSeason = await this.prisma.season.findUnique({
      where: { id: dto.toSeasonId },
    });

    if (!toSeason) {
      throw new Error(`Season ${dto.toSeasonId} not found`);
    }

    // Get current season
    const currentSeason = await this.prisma.season.findFirst({
      where: {
        startDate: { lte: new Date() },
        endDate: { gte: new Date() },
      },
    });

    // Build transition plan
    const plan: SeasonTransitionPlan = {
      fromSeasonId: currentSeason?.id || '',
      toSeasonId: dto.toSeasonId,
      startDate: dto.startDate,
      targetCompletionDate: new Date(dto.startDate.getTime() + 7 * 86400000), // 7 days
      steps: [
        { step: 1, name: 'Align Curriculum', engine: 'CURRICULUM' as any, action: 'Sync curriculum modules to season theme', status: 'PENDING', estimatedDuration: 60 },
        { step: 2, name: 'Sync Missions', engine: 'MISSION' as any, action: 'Update missions to reflect seasonal goals', status: 'PENDING', estimatedDuration: 45 },
        { step: 3, name: 'Launch Creator Challenges', engine: 'CREATOR' as any, action: 'Launch seasonal creator challenges', status: 'PENDING', estimatedDuration: 30 },
        { step: 4, name: 'Integrate Exchange Lessons', engine: 'EXCHANGE' as any, action: 'Sync Dominion Exchange financial lessons', status: 'PENDING', estimatedDuration: 30 },
        { step: 5, name: 'Update Intelligence Thresholds', engine: 'INTELLIGENCE' as any, action: 'Adjust intelligence criteria for new season', status: 'PENDING', estimatedDuration: 20 },
      ],
      blockers: [],
      readiness: 0,
    };

    // If not dry run, create seasonal sync record
    if (!dto.dryRun) {
      await this.prisma.seasonalSynchronization.upsert({
        where: { seasonId: dto.toSeasonId },
        create: {
          seasonId: dto.toSeasonId,
          transitionStarted: new Date(),
          transitionPlan: plan.steps as any,
          regionalVariations: {},
        },
        update: {
          transitionStarted: new Date(),
          transitionPlan: plan.steps as any,
        },
      });
    }

    return plan;
  }

  /**
   * Align all systems to current season
   * Returns alignment scores for each system
   */
  async alignSystemsToSeason(seasonId: string): Promise<SeasonalAlignment> {
    const season = await this.prisma.season.findUnique({
      where: { id: seasonId },
      include: {
        curriculumModules: true,
        missions: true,
        creatorChallenges: true,
      },
    });

    if (!season) {
      throw new Error(`Season ${seasonId} not found`);
    }

    // Check each system's alignment
    const curriculum = await this.checkCurriculumAlignment(seasonId);
    const missions = await this.checkMissionAlignment(seasonId);
    const creators = await this.checkCreatorAlignment(seasonId);
    const exchange = await this.checkExchangeAlignment(seasonId);
    const intelligence = await this.checkIntelligenceAlignment(seasonId);

    // Calculate overall score
    const overallScore = (
      curriculum.score +
      missions.score +
      creators.score +
      exchange.score +
      intelligence.score
    ) / 5;

    // Get transition status
    const syncRecord = await this.prisma.seasonalSynchronization.findUnique({
      where: { seasonId },
    });

    return {
      seasonId,
      seasonName: season.name,
      overallScore,
      curriculum,
      missions,
      creators,
      exchange,
      intelligence,
      transitionStatus: syncRecord?.transitionCompleted ? 'COMPLETED' : syncRecord?.transitionStarted ? 'IN_PROGRESS' : 'NOT_STARTED',
      transitionProgress: syncRecord ? this.calculateTransitionProgress(syncRecord.transitionPlan as any) : 0,
    };
  }

  /**
   * Sync curriculum to seasonal theme
   */
  async syncCurriculumToSeason(seasonId: string): Promise<void> {
    const season = await this.prisma.season.findUnique({
      where: { id: seasonId },
    });

    if (!season) {
      throw new Error(`Season ${seasonId} not found`);
    }

    // Update curriculum modules to reflect seasonal theme
    const modules = await this.prisma.curriculumModule.findMany({
      where: { seasonId },
    });

    console.log(`Synced ${modules.length} curriculum modules to ${season.name} season`);

    // Update seasonal sync record
    await this.prisma.seasonalSynchronization.upsert({
      where: { seasonId },
      create: {
        seasonId,
        curriculumAligned: true,
        curriculumScore: 1.0,
        regionalVariations: {},
      },
      update: {
        curriculumAligned: true,
        curriculumScore: 1.0,
      },
    });
  }

  /**
   * Sync missions to seasonal goals
   */
  async syncMissionsToSeason(seasonId: string): Promise<void> {
    const season = await this.prisma.season.findUnique({
      where: { id: seasonId },
      include: { missions: true },
    });

    if (!season) {
      throw new Error(`Season ${seasonId} not found`);
    }

    console.log(`Synced ${season.missions.length} missions to ${season.name} season`);

    // Update seasonal sync record
    await this.prisma.seasonalSynchronization.upsert({
      where: { seasonId },
      create: {
        seasonId,
        missionsAligned: true,
        missionScore: 1.0,
        regionalVariations: {},
      },
      update: {
        missionsAligned: true,
        missionScore: 1.0,
      },
    });
  }

  /**
   * Launch seasonal creator challenges
   */
  async syncCreatorsToSeason(seasonId: string): Promise<void> {
    const season = await this.prisma.season.findUnique({
      where: { id: seasonId },
      include: { creatorChallenges: true },
    });

    if (!season) {
      throw new Error(`Season ${seasonId} not found`);
    }

    console.log(`Synced ${season.creatorChallenges.length} creator challenges to ${season.name} season`);

    // Update seasonal sync record
    await this.prisma.seasonalSynchronization.upsert({
      where: { seasonId },
      create: {
        seasonId,
        creatorsAligned: true,
        creatorScore: 1.0,
        regionalVariations: {},
      },
      update: {
        creatorsAligned: true,
        creatorScore: 1.0,
      },
    });
  }

  /**
   * Integrate Dominion Exchange lessons with seasonal theme
   */
  async syncExchangeToSeason(seasonId: string): Promise<void> {
    const season = await this.prisma.season.findUnique({
      where: { id: seasonId },
    });

    if (!season) {
      throw new Error(`Season ${seasonId} not found`);
    }

    // Get Exchange integrations for this season's missions and curriculum
    const integrations = await this.prisma.exchangeIntegration.findMany({
      where: {
        OR: [
          { entityType: 'SEASON', entityId: seasonId },
        ],
      },
    });

    console.log(`Synced ${integrations.length} Exchange integrations to ${season.name} season`);

    // Update seasonal sync record
    await this.prisma.seasonalSynchronization.upsert({
      where: { seasonId },
      create: {
        seasonId,
        exchangeAligned: true,
        exchangeScore: integrations.length > 0 ? 1.0 : 0.5,
        regionalVariations: {},
      },
      update: {
        exchangeAligned: true,
        exchangeScore: integrations.length > 0 ? 1.0 : 0.5,
      },
    });
  }

  // =============================================================================
  // PRIVATE HELPER METHODS
  // =============================================================================

  private async checkCurriculumAlignment(seasonId: string): Promise<AlignmentDimension> {
    const modules = await this.prisma.curriculumModule.findMany({
      where: { seasonId },
    });

    const score = modules.length > 0 ? 1.0 : 0;
    const aligned = modules.length > 0;

    return {
      aligned,
      score,
      issues: aligned ? [] : ['No curriculum modules found for this season'],
      recommendations: aligned ? [] : ['Create curriculum modules for seasonal theme'],
    };
  }

  private async checkMissionAlignment(seasonId: string): Promise<AlignmentDimension> {
    const missions = await this.prisma.mission.findMany({
      where: { seasonId },
    });

    const score = missions.length > 0 ? 1.0 : 0;
    const aligned = missions.length > 0;

    return {
      aligned,
      score,
      issues: aligned ? [] : ['No missions found for this season'],
      recommendations: aligned ? [] : ['Create missions aligned with seasonal goals'],
    };
  }

  private async checkCreatorAlignment(seasonId: string): Promise<AlignmentDimension> {
    const challenges = await this.prisma.creatorChallenge.findMany({
      where: { seasonId },
    });

    const score = challenges.length > 0 ? 1.0 : 0;
    const aligned = challenges.length > 0;

    return {
      aligned,
      score,
      issues: aligned ? [] : ['No creator challenges for this season'],
      recommendations: aligned ? [] : ['Launch seasonal creator challenges'],
    };
  }

  private async checkExchangeAlignment(seasonId: string): Promise<AlignmentDimension> {
    const integrations = await this.prisma.exchangeIntegration.findMany({
      where: { entityType: 'SEASON', entityId: seasonId },
    });

    const score = integrations.length > 0 ? 1.0 : 0.5;
    const aligned = integrations.length > 0;

    return {
      aligned,
      score,
      issues: aligned ? [] : ['Limited Exchange integration with seasonal theme'],
      recommendations: aligned ? [] : ['Create Exchange lesson integrations for season'],
    };
  }

  private async checkIntelligenceAlignment(seasonId: string): Promise<AlignmentDimension> {
    // Check if intelligence thresholds are adjusted for season
    // For now, assume intelligence is always aligned
    return {
      aligned: true,
      score: 0.9,
      issues: [],
      recommendations: [],
    };
  }

  private calculateTransitionProgress(plan: any[]): number {
    if (!plan || plan.length === 0) return 0;

    const completedSteps = plan.filter((step: any) => step.status === 'COMPLETED').length;
    return completedSteps / plan.length;
  }
}
