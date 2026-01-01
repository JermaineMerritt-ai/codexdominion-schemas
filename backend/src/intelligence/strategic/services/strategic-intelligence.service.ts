import { Injectable } from '@nestjs/common';
import { PrismaService } from '@/prisma/prisma.service';
import {
  StrategicRecommendation,
  RecommendationPriority,
  AlertDomain,
} from '@prisma/client';
import { YouthStrategyEngine } from '../models/youth-strategy.model';
import { CircleStrategyEngine } from '../models/circle-strategy.model';
import { MissionStrategyEngine } from '../models/mission-strategy.model';
import { StrategicContext, RecommendationSummary } from '../types/strategic.types';

@Injectable()
export class StrategicIntelligenceService {
  constructor(
    private prisma: PrismaService,
    private youthStrategy: YouthStrategyEngine,
    private circleStrategy: CircleStrategyEngine,
    private missionStrategy: MissionStrategyEngine,
  ) {}

  async generateStrategicPlan(context: StrategicContext): Promise<{
    recommendations: StrategicRecommendation[];
    summary: RecommendationSummary;
  }> {
    const recommendations: Partial<StrategicRecommendation>[] = [];

    // Youth strategies
    if (context.userId && (!context.domain || context.domain === 'YOUTH')) {
      const youthRecs = await this.youthStrategy.generateYouthStrategy(context.userId);
      recommendations.push(...youthRecs);
    }

    // Circle strategies
    if (context.circleId && (!context.domain || context.domain === 'CIRCLES')) {
      const circleRecs = await this.circleStrategy.generateCircleStrategy(context.circleId);
      recommendations.push(...circleRecs);
    }

    // Mission strategies
    if (!context.domain || context.domain === 'MISSIONS') {
      const missionRecs = await this.missionStrategy.generateMissionStrategy(
        context.regionId,
        context.seasonId,
      );
      recommendations.push(...missionRecs);
    }

    // Filter by priority if specified
    let filteredRecs = recommendations;
    if (context.priority?.length) {
      filteredRecs = recommendations.filter((r) => r.priority && context.priority!.includes(r.priority));
    }

    // Save to database
    const savedRecommendations = await Promise.all(
      filteredRecs.map(async (rec) => {
        return this.prisma.strategicRecommendation.create({
          data: {
            type: rec.type!,
            domain: rec.domain!,
            priority: rec.priority!,
            status: rec.status || 'GENERATED',
            entityId: rec.entityId,
            entityType: rec.entityType,
            regionId: rec.regionId,
            seasonId: rec.seasonId,
            title: rec.title || 'Untitled Recommendation',
            description: rec.description || '',
            reasoning: rec.reasoning || '',
            expectedOutcome: rec.expectedOutcome || '',
            actionItems: (rec.actionItems as any) || [],
            timeHorizon: rec.timeHorizon || 'MEDIUM',
            estimatedDuration: rec.estimatedDuration || 0,
            predictionIds: rec.predictionIds || [],
            memoryPatterns: (rec.memoryPatterns as any) || null,
            confidence: rec.confidence || 0.5,
            successMetrics: (rec.successMetrics as any) || {},
          },
        });
      }),
    );

    // Generate summary
    const summary: RecommendationSummary = {
      total: savedRecommendations.length,
      byPriority: this.countByField(savedRecommendations, 'priority'),
      byDomain: this.countByField(savedRecommendations, 'domain'),
      estimatedImplementationDays: savedRecommendations.reduce(
        (sum, r) => sum + (r.estimatedDuration || 0),
        0,
      ),
    };

    return { recommendations: savedRecommendations, summary };
  }

  async getRecommendationsByStatus(status: string[]): Promise<StrategicRecommendation[]> {
    return this.prisma.strategicRecommendation.findMany({
      where: {
        status: {
          in: status as any,
        },
      },
      include: {
        region: true,
        season: true,
      },
      orderBy: {
        generatedAt: 'desc',
      },
    });
  }

  async getRecommendationsByPriority(
    priority: RecommendationPriority[],
  ): Promise<StrategicRecommendation[]> {
    return this.prisma.strategicRecommendation.findMany({
      where: {
        priority: {
          in: priority,
        },
      },
      include: {
        region: true,
        season: true,
      },
      orderBy: [{ priority: 'asc' }, { generatedAt: 'desc' }],
    });
  }

  async reviewRecommendation(
    id: string,
    userId: string,
    status: string,
    notes?: string,
  ): Promise<StrategicRecommendation> {
    const recommendation = await this.prisma.strategicRecommendation.update({
      where: { id },
      data: {
        status: status as any,
        reviewedAt: new Date(),
        reviewedBy: userId,
      },
    });

    // Record in history
    await this.prisma.strategyHistory.create({
      data: {
        recommendationId: id,
        statusChange: `Status changed to ${status}`,
        lessonsLearned: notes,
      },
    });

    return recommendation;
  }

  async implementRecommendation(id: string): Promise<StrategicRecommendation> {
    const recommendation = await this.prisma.strategicRecommendation.update({
      where: { id },
      data: {
        status: 'IN_PROGRESS',
        implementedAt: new Date(),
      },
    });

    await this.prisma.strategyHistory.create({
      data: {
        recommendationId: id,
        statusChange: 'Implementation started',
      },
    });

    return recommendation;
  }

  async completeRecommendation(
    id: string,
    completion: {
      actualOutcome: any;
      variance?: number;
      lessonsLearned?: string;
    },
  ): Promise<StrategicRecommendation> {
    const recommendation = await this.prisma.strategicRecommendation.update({
      where: { id },
      data: {
        status: 'COMPLETED',
        completedAt: new Date(),
      },
    });

    await this.prisma.strategyHistory.create({
      data: {
        recommendationId: id,
        statusChange: 'COMPLETED',
        actualOutcome: completion.actualOutcome,
        variance: completion.variance,
        lessonsLearned: completion.lessonsLearned,
      },
    });

    return recommendation;
  }

  private countByField<T extends Record<string, any>>(
    items: T[],
    field: keyof T,
  ): Record<string, number> {
    return items.reduce((acc, item) => {
      const key = String(item[field]);
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
  }
}
