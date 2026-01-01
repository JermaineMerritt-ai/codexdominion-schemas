import { Injectable } from '@nestjs/common';
import { PrismaService } from '@/prisma/prisma.service';
import {
  StrategicRecommendation,
  RecommendationType,
  RecommendationPriority,
  RecommendationStatus,
} from '@prisma/client';
import { ActionItem } from '../types/strategic.types';

@Injectable()
export class MissionStrategyEngine {
  constructor(private prisma: PrismaService) {}

  async generateMissionStrategy(
    regionId?: string,
    seasonId?: string,
  ): Promise<Partial<StrategicRecommendation>[]> {
    const recommendations: Partial<StrategicRecommendation>[] = [];

    // Get missions with submission data
    const missions = await this.prisma.mission.findMany({
      where: {
        ...(seasonId && { seasonId }),
      },
      include: {
        assignments: {
          include: {
            submissions: true,
          },
        },
      },
    });

    for (const mission of missions) {
      const totalAssignments = mission.assignments.length;
      if (totalAssignments < 10) continue; // Need sufficient data

      const completedSubmissions = mission.assignments.filter(
        (a) => a.submissions?.some((s) => s.status === 'APPROVED'),
      ).length;

      const completionRate =
        totalAssignments > 0 ? completedSubmissions / totalAssignments : 0;

      // Categorize difficulty
      let difficulty: 'easy' | 'medium' | 'hard' | 'extreme';
      if (completionRate > 0.75) difficulty = 'easy';
      else if (completionRate > 0.55) difficulty = 'medium';
      else if (completionRate > 0.35) difficulty = 'hard';
      else difficulty = 'extreme';

      // Emphasize High-Performing Missions
      if (difficulty === 'easy' && completionRate > 0.8) {
        const actionItems: ActionItem[] = [
          {
            step: 1,
            action: 'Feature mission in regional curriculum guide',
            owner: 'Regional Director',
            dueWeeks: 2,
          },
          {
            step: 2,
            action: 'Create mission showcase (youth testimonials)',
            owner: 'Creator Circle',
            dueWeeks: 4,
          },
          {
            step: 3,
            action: 'Train captains on best practices for this mission',
            owner: 'Regional Director',
            dueWeeks: 6,
          },
          {
            step: 4,
            action: 'Introduce mission early in season',
            owner: 'Youth Captain',
            dueWeeks: 8,
          },
        ];

        recommendations.push({
          type: RecommendationType.MISSION_EMPHASIS,
          domain: 'MISSIONS',
          priority: RecommendationPriority.MEDIUM,
          entityId: mission.id,
          entityType: 'mission',
          regionId,
          seasonId,
          title: `Emphasize Mission "${mission.title}" Next Season`,
          description: `Mission "${mission.title}" shows exceptional completion rates (${(completionRate * 100).toFixed(0)}%). High engagement, strong learning outcomes, and youth enthusiasm make this a signature mission.`,
          reasoning: `
• Completion Rate: ${(completionRate * 100).toFixed(0)}%
• Difficulty: ${difficulty}
• Total Assignments: ${totalAssignments}
• Pattern: Consistent success across circles
          `,
          expectedOutcome: `Mission "${mission.title}" becomes regional signature mission, completion rate remains 80%+, featured in onboarding.`,
          actionItems: actionItems as any,
          timeHorizon: 'next_season',
          estimatedDuration: 56,
          confidence: 0.85,
          predictionIds: [],
          successMetrics: {
            completionRate: 80,
            youthSatisfaction: 8.5,
            captainConfidence: 8.0,
          } as any,
          status: RecommendationStatus.GENERATED,
        });
      }

      // Retire Low-Performing Missions
      if (difficulty === 'extreme' && completionRate < 0.3) {
        const actionItems: ActionItem[] = [
          {
            step: 1,
            action: 'Gather youth/captain feedback on mission pain points',
            owner: 'Regional Director',
            dueWeeks: 2,
          },
          {
            step: 2,
            action: 'Decide: retire, simplify, or split into 2 missions',
            owner: 'Council',
            dueWeeks: 4,
          },
          {
            step: 3,
            action: 'If redesign: create new version with pilot test',
            owner: 'Curriculum Team',
            dueWeeks: 8,
          },
          {
            step: 4,
            action: 'If retire: announce to regions with replacement suggestion',
            owner: 'Council',
            dueWeeks: 4,
          },
        ];

        recommendations.push({
          type: RecommendationType.MISSION_EMPHASIS,
          domain: 'MISSIONS',
          priority: RecommendationPriority.HIGH,
          entityId: mission.id,
          entityType: 'mission',
          regionId,
          seasonId,
          title: `Retire or Redesign Mission "${mission.title}"`,
          description: `Mission "${mission.title}" shows low completion (${(completionRate * 100).toFixed(0)}%) and high difficulty. Youth report confusion and frustration. Recommend retirement or major redesign.`,
          reasoning: `
• Completion Rate: ${(completionRate * 100).toFixed(0)}%
• Difficulty: ${difficulty}
• Total Attempts: ${totalAssignments}
• Pattern: Consistent struggle across circles
          `,
          expectedOutcome: `Mission either removed from rotation or redesigned with 50%+ completion rate improvement.`,
          actionItems: actionItems as any,
          timeHorizon: 'next_season',
          estimatedDuration: 56,
          confidence: 0.8,
          predictionIds: [],
          successMetrics: {
            missionRetiredOrRedesigned: true,
            replacementCompletionRate: 60,
          } as any,
          status: RecommendationStatus.GENERATED,
        });
      }

      // Medium Difficulty - Monitor
      if (difficulty === 'medium' && completionRate >= 0.55 && completionRate <= 0.7) {
        recommendations.push({
          type: RecommendationType.MISSION_EMPHASIS,
          domain: 'MISSIONS',
          priority: RecommendationPriority.LOW,
          entityId: mission.id,
          entityType: 'mission',
          regionId,
          seasonId,
          title: `Monitor Mission "${mission.title}"`,
          description: `Mission "${mission.title}" shows moderate performance (${(completionRate * 100).toFixed(0)}% completion). Consider minor adjustments to improve success rate.`,
          reasoning: `
• Completion Rate: ${(completionRate * 100).toFixed(0)}%
• Difficulty: ${difficulty}
• Opportunity for improvement with minor tweaks
          `,
          expectedOutcome: `Mission completion rate improves to 70%+ with small adjustments.`,
          actionItems: [
            {
              step: 1,
              action: 'Review youth feedback for friction points',
              owner: 'Regional Director',
              dueWeeks: 2,
            },
            {
              step: 2,
              action: 'Simplify 1-2 steps or provide clearer guidance',
              owner: 'Curriculum Team',
              dueWeeks: 4,
            },
          ] as any,
          timeHorizon: 'next_season',
          estimatedDuration: 28,
          confidence: 0.7,
          predictionIds: [],
          successMetrics: {
            completionRate: 70,
          } as any,
          status: RecommendationStatus.GENERATED,
        });
      }
    }

    return recommendations;
  }
}
