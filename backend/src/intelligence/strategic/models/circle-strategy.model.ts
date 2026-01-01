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
export class CircleStrategyEngine {
  constructor(private prisma: PrismaService) {}

  async generateCircleStrategy(circleId: string): Promise<Partial<StrategicRecommendation>[]> {
    const recommendations: Partial<StrategicRecommendation>[] = [];

    // Get circle data
    const circle = await this.prisma.circle.findUnique({
      where: { id: circleId },
      include: {
        members: {
          include: {
            user: true,
          },
        },
        captain: true,
        sessions: {
          where: {
            scheduledAt: {
              gte: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000), // Last 90 days
            },
          },
          include: {
            attendance: true,
          },
        },
      },
    });

    if (!circle) return recommendations;

    const memberCount = circle.members.length;
    const sessionCount = circle.sessions.length;

    // Calculate health score
    const totalAttendance = circle.sessions.reduce((sum, s) => sum + s.attendance.length, 0);
    const presentCount = circle.sessions.reduce(
      (sum, s) => sum + s.attendance.filter((a) => a.status === 'PRESENT').length,
      0,
    );
    const attendanceRate = totalAttendance > 0 ? (presentCount / totalAttendance) * 100 : 0;

    const healthScore = attendanceRate * 0.7 + (sessionCount >= 8 ? 30 : (sessionCount / 8) * 30);

    // Split Recommendation
    if (memberCount > 18) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Identify co-captain candidate from circle members',
          owner: 'Youth Captain',
          dueWeeks: 2,
        },
        {
          step: 2,
          action: 'Complete co-captain training module',
          owner: 'Co-Captain Candidate',
          dueWeeks: 4,
        },
        {
          step: 3,
          action: 'Plan split logistics (meeting spaces, schedules)',
          owner: 'Regional Director',
          dueWeeks: 6,
        },
        {
          step: 4,
          action: 'Communicate split to circle (celebrate growth)',
          owner: 'Youth Captain',
          dueWeeks: 7,
        },
        {
          step: 5,
          action: 'Execute split at season transition',
          owner: 'Regional Director',
          dueWeeks: 8,
        },
        {
          step: 6,
          action: 'Monitor both circles for 4 weeks post-split',
          owner: 'Regional Director',
          dueWeeks: 12,
        },
      ];

      recommendations.push({
        type: RecommendationType.CIRCLE_STRUCTURE,
        domain: 'CIRCLES',
        priority: RecommendationPriority.HIGH,
        entityId: circleId,
        entityType: 'circle',
        title: `Recommend Split for Circle ${circle.name}`,
        description: `Circle ${circle.name} has reached ${memberCount} members. Optimal circle size is 12-18. Split recommended to maintain intimacy and engagement.`,
        reasoning: `
• Current Members: ${memberCount}
• Optimal Range: 12-18 members
• Health Score: ${healthScore.toFixed(0)}%
• Pattern: Consistent growth exceeding optimal size
        `,
        expectedOutcome: `Circle ${circle.name} splits into 2 healthy circles (10-12 members each), maintains 85%+ health scores, both circles sustain growth.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_season',
        estimatedDuration: 84,
        confidence: 0.85,
        predictionIds: [],
        successMetrics: {
          circleSizeCircle1: { min: 10, max: 14 },
          circleSizeCircle2: { min: 10, max: 14 },
          healthScoreCircle1: 85,
          healthScoreCircle2: 85,
          retentionRate: 90,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    // Collapse Prevention Strategy
    const collapseRisk =
      memberCount < 6 ? 0.4 : 0 +
      (healthScore < 60 ? 0.3 : 0) +
      (attendanceRate < 50 ? 0.3 : 0);

    if (collapseRisk > 0.7) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Regional Director 1-on-1 with captain (diagnose issues)',
          owner: 'Regional Director',
          dueWeeks: 0.5,
        },
        {
          step: 2,
          action: 'Provide captain with Circle Revival Toolkit',
          owner: 'Regional Director',
          dueWeeks: 1,
        },
        {
          step: 3,
          action: 'Co-facilitate next 2 sessions (model best practices)',
          owner: 'Regional Director',
          dueWeeks: 2,
        },
        {
          step: 4,
          action: 'Recruit 2-3 new members from adjacent circles',
          owner: 'Youth Captain',
          dueWeeks: 4,
        },
        {
          step: 5,
          action: 'Run high-engagement mission series',
          owner: 'Youth Captain',
          dueWeeks: 6,
        },
        {
          step: 6,
          action: 'Evaluate circle health — continue or merge',
          owner: 'Regional Director',
          dueWeeks: 8,
        },
      ];

      recommendations.push({
        type: RecommendationType.CIRCLE_STRUCTURE,
        domain: 'CIRCLES',
        priority: RecommendationPriority.CRITICAL,
        entityId: circleId,
        entityType: 'circle',
        title: `Immediate Intervention for Circle ${circle.name}`,
        description: `Circle ${circle.name} shows high collapse risk (${(collapseRisk * 100).toFixed(0)}%). Declining health, low attendance, member attrition require urgent leadership support.`,
        reasoning: `
• Collapse Risk: ${(collapseRisk * 100).toFixed(0)}%
• Health Score: ${healthScore.toFixed(0)}%
• Member Count: ${memberCount} (below threshold)
• Attendance Rate: ${attendanceRate.toFixed(0)}%
• Pattern: Classic circle fragmentation
        `,
        expectedOutcome: `Circle ${circle.name} stabilizes at 8+ members, health score rises to 70%+, captain receives targeted support.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_week',
        estimatedDuration: 56,
        confidence: 0.75,
        predictionIds: [],
        successMetrics: {
          memberCount: { min: 8 },
          healthScore: 70,
          attendanceRate: 75,
          captainConfidence: 7.0,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    // Mentorship Opportunity
    if (
      memberCount >= 12 &&
      memberCount <= 16 &&
      healthScore >= 80 &&
      sessionCount >= 8
    ) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Identify new circle location and initial members',
          owner: 'Regional Director',
          dueWeeks: 2,
        },
        {
          step: 2,
          action: `Assign captain from ${circle.name} as co-facilitator for new circle`,
          owner: 'Regional Director',
          dueWeeks: 3,
        },
        {
          step: 3,
          action: 'Run joint session (both circles) — cultural transmission',
          owner: 'Youth Captain',
          dueWeeks: 4,
        },
        {
          step: 4,
          action: 'Mentor new circle captain for 8 weeks',
          owner: 'Youth Captain',
          dueWeeks: 12,
        },
        {
          step: 5,
          action: 'Celebrate successful launch',
          owner: 'Regional Director',
          dueWeeks: 14,
        },
      ];

      recommendations.push({
        type: RecommendationType.CIRCLE_STRUCTURE,
        domain: 'CIRCLES',
        priority: RecommendationPriority.MEDIUM,
        entityId: circleId,
        entityType: 'circle',
        title: `Circle ${circle.name} Ready to Mentor New Circle`,
        description: `Circle ${circle.name} demonstrates maturity, stability, and strong leadership. Recommend mentoring a newly formed circle to expand regional capacity.`,
        reasoning: `
• Stage: Growth (healthy)
• Members: ${memberCount} (strong base)
• Health Score: ${healthScore.toFixed(0)}%
• Captain Experience: High
• Pattern: Established circle with leadership capacity
        `,
        expectedOutcome: `Circle ${circle.name} mentors new circle for 8 weeks, new circle achieves 70%+ health score, mentorship strengthens both circles.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_season',
        estimatedDuration: 98,
        confidence: 0.8,
        predictionIds: [],
        successMetrics: {
          newCircleHealthScore: 70,
          newCircleMembers: { min: 8, max: 12 },
          mentorCircleHealthScore: 85,
          captainLeadershipScore: 9.0,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    return recommendations;
  }
}
