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
export class YouthStrategyEngine {
  constructor(private prisma: PrismaService) {}

  async generateYouthStrategy(userId: string): Promise<Partial<StrategicRecommendation>[]> {
    const recommendations: Partial<StrategicRecommendation>[] = [];

    // Get user data
    const user = await this.prisma.user.findUnique({
      where: { id: userId },
      include: {
        profile: true,
        roles: { include: { role: true } },
        circleMemberships: {
          include: {
            circle: true,
          },
        },
        missionAssignments: {
          include: {
            submissions: true,
          },
        },
        circleAttendance: {
          include: {
            session: true,
          },
          where: {
            session: {
              scheduledAt: {
                gte: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000), // Last 90 days
              },
            },
          },
        },
      },
    });

    if (!user) return recommendations;

    // Calculate metrics
    const totalAttendance = user.circleAttendance.length;
    const presentCount = user.circleAttendance.filter((a) => a.status === 'PRESENT').length;
    const attendanceRate = totalAttendance > 0 ? (presentCount / totalAttendance) * 100 : 0;

    const totalMissions = user.missionAssignments.length;
    const completedMissions = user.missionAssignments.filter(
      (a) => a.submissions?.some((s) => s.status === 'APPROVED'),
    ).length;
    const missionCompletionRate =
      totalMissions > 0 ? (completedMissions / totalMissions) * 100 : 0;

    // Calculate leadership readiness score (simplified)
    const leadershipReadiness =
      (attendanceRate / 100) * 0.4 + (missionCompletionRate / 100) * 0.4 + 0.2;

    // Leadership Track Recommendation
    if (leadershipReadiness > 0.75 && attendanceRate > 80 && completedMissions >= 5) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Assign to captain mentorship program',
          owner: 'Regional Director',
          dueWeeks: 2,
        },
        {
          step: 2,
          action: 'Complete Leadership Module series',
          owner: 'Youth',
          dueWeeks: 6,
        },
        {
          step: 3,
          action: 'Shadow current captain for 4 sessions',
          owner: 'Youth Captain',
          dueWeeks: 8,
        },
        {
          step: 4,
          action: 'Lead 2 trial sessions with feedback',
          owner: 'Youth',
          dueWeeks: 10,
        },
        {
          step: 5,
          action: 'Formal captain appointment',
          owner: 'Council',
          dueWeeks: 12,
        },
      ];

      recommendations.push({
        type: RecommendationType.YOUTH_PATH,
        domain: 'YOUTH',
        priority: RecommendationPriority.HIGH,
        entityId: userId,
        entityType: 'youth',
        title: `Recommend ${user.firstName} ${user.lastName} for Leadership Path`,
        description: `${user.firstName} shows strong leadership signals (${(leadershipReadiness * 100).toFixed(0)}% readiness). Consistent attendance (${attendanceRate.toFixed(0)}%), mission completion (${missionCompletionRate.toFixed(0)}%), and emerging leadership behaviors indicate readiness for captain training next season.`,
        reasoning: `
• Attendance Rate: ${attendanceRate.toFixed(0)}%
• Missions Completed: ${completedMissions}/${totalMissions}
• Leadership Readiness Score: ${(leadershipReadiness * 100).toFixed(0)}%
• Pattern: High engagement + consistent presence + peer influence
        `,
        expectedOutcome: `${user.firstName} transitions to Youth Captain within 1-2 seasons, mentors 3-5 youth, leads weekly sessions with 85%+ attendance.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_season',
        estimatedDuration: 84, // ~12 weeks
        confidence: 0.85,
        predictionIds: [],
        successMetrics: {
          captainAppointment: true,
          sessionAttendance: 85,
          youthMentored: 3,
          leadershipScore: 8.0,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    // Creator Track Recommendation
    const artifacts = await this.prisma.artifact.count({
      where: { creatorId: userId },
    });

    if (artifacts >= 3 && missionCompletionRate > 60) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Enroll in Creator Foundations module',
          owner: 'Youth',
          dueWeeks: 2,
        },
        {
          step: 2,
          action: 'Complete first Creator Challenge',
          owner: 'Youth',
          dueWeeks: 6,
        },
        {
          step: 3,
          action: 'Join Creator Circle sessions (2x/month)',
          owner: 'Youth',
          dueWeeks: 8,
        },
        {
          step: 4,
          action: 'Build initial portfolio',
          owner: 'Youth',
          dueWeeks: 12,
        },
      ];

      recommendations.push({
        type: RecommendationType.YOUTH_PATH,
        domain: 'YOUTH',
        priority: RecommendationPriority.MEDIUM,
        entityId: userId,
        entityType: 'youth',
        title: `Recommend ${user.firstName} ${user.lastName} for Creator Path`,
        description: `${user.firstName} demonstrates strong creative capacity (${artifacts} artifacts submitted). Pattern recognition, artifact submissions, and mission progress suggest alignment with Creator Track.`,
        reasoning: `
• Artifacts Submitted: ${artifacts}
• Mission Completion: ${missionCompletionRate.toFixed(0)}%
• Collaboration Readiness: Strong
        `,
        expectedOutcome: `${user.firstName} completes 5+ creator challenges, builds portfolio, transitions to Creator Circle within 2 seasons.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_season',
        estimatedDuration: 84,
        confidence: 0.75,
        predictionIds: [],
        successMetrics: {
          challengesCompleted: 5,
          portfolioSize: 10,
          creatorCircleMembership: true,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    // Burnout Prevention Strategy
    const recentAttendance = user.circleAttendance
      .filter((a) => {
        const date = new Date(a.session.scheduledAt);
        const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
        return date >= thirtyDaysAgo;
      })
      .sort((a, b) => new Date(b.session.scheduledAt).getTime() - new Date(a.session.scheduledAt).getTime());

    const recentAttendanceRate =
      recentAttendance.length > 0
        ? (recentAttendance.filter((a) => a.status === 'PRESENT').length / recentAttendance.length) * 100
        : 0;

    const showsBurnoutPattern =
      attendanceRate > 70 && // Was previously engaged
      recentAttendanceRate < 50 && // Now declining
      recentAttendance.length >= 4; // Enough data points

    if (showsBurnoutPattern) {
      const actionItems: ActionItem[] = [
        {
          step: 1,
          action: 'Captain 1-on-1 check-in within 48 hours',
          owner: 'Youth Captain',
          dueWeeks: 0.25,
        },
        {
          step: 2,
          action: 'Reduce mission load by 50% for 4 weeks',
          owner: 'Youth Captain',
          dueWeeks: 1,
        },
        {
          step: 3,
          action: 'Offer low-pressure circle role (observer/contributor)',
          owner: 'Youth Captain',
          dueWeeks: 2,
        },
        {
          step: 4,
          action: 'Weekly check-ins for 1 month',
          owner: 'Youth Captain',
          dueWeeks: 4,
        },
      ];

      recommendations.push({
        type: RecommendationType.YOUTH_PATH,
        domain: 'YOUTH',
        priority: RecommendationPriority.CRITICAL,
        entityId: userId,
        entityType: 'youth',
        title: `Burnout Prevention for ${user.firstName} ${user.lastName}`,
        description: `${user.firstName} shows early burnout patterns. High previous engagement (${attendanceRate.toFixed(0)}%) followed by rapid decline (${recentAttendanceRate.toFixed(0)}% in last 30 days) requires immediate supportive intervention.`,
        reasoning: `
• Historical Attendance: ${attendanceRate.toFixed(0)}%
• Recent Attendance (30 days): ${recentAttendanceRate.toFixed(0)}%
• Pattern: Sharp decline from high baseline
• Classic burnout trajectory detected
        `,
        expectedOutcome: `${user.firstName} stabilizes engagement, returns to 70%+ attendance, expresses renewed purpose.`,
        actionItems: actionItems as any,
        timeHorizon: 'next_week',
        estimatedDuration: 28,
        confidence: 0.8,
        predictionIds: [],
        successMetrics: {
          attendanceRate: 70,
          engagementScore: 6.0,
          missionCompletion: 50,
        } as any,
        status: RecommendationStatus.GENERATED,
      });
    }

    return recommendations;
  }
}
