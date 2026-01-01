// ======================================================
// LEADERSHIP ORCHESTRATION SERVICE
// Assesses leadership readiness and plans succession
// ======================================================

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { RoleName } from '@prisma/client';
import {
  PromotionRecommendation,
  SuccessionPlan,
  SuccessorCandidate,
  LeadershipGap,
} from '../types/governance.types';

@Injectable()
export class LeadershipOrchestrationService {
  constructor(private prisma: PrismaService) {}

  /**
   * Assess leadership readiness for a user
   */
  async assessLeadershipReadiness(userId: string): Promise<any> {
    const user = await this.prisma.user.findUnique({
      where: { id: userId },
      include: {
        roles: {
          include: {
            role: true,
          },
        },
        missionAssignments: {
          include: {
            submissions: true,
          },
        },
        circleAttendance: true,
        leadershipReadiness: true,
      },
    });

    if (!user) {
      throw new Error(`User ${userId} not found`);
    }

    const currentRole = user.roles[0]?.role.name || RoleName.YOUTH;
    const targetRole = this.getNextRole(currentRole);

    // Calculate readiness factors
    const attendance = this.calculateAttendance(user.circleAttendance);
    const missionCompletion = this.calculateMissionCompletion(
      user.missionAssignments,
    );
    const leadershipSignals = this.calculateLeadershipSignals(user);
    const mentorshipHours = 0; // Would be calculated from mentorship tracking

    const readinessScore =
      attendance * 0.25 +
      missionCompletion * 0.25 +
      leadershipSignals * 0.25 +
      Math.min(mentorshipHours / 20, 1) * 0.25;

    const isReady = readinessScore * 100 >= 80;
    const timeToReadiness = isReady
      ? 0
      : Math.ceil((80 - readinessScore * 100) / 2); // 2 points per day estimate

    // Create or update readiness record
    const readiness = await this.prisma.leadershipReadiness.upsert({
      where: { userId },
      update: {
        currentRole,
        targetRole,
        readinessScore: readinessScore * 100,
        attendance: attendance * 100,
        missionCompletion: missionCompletion * 100,
        leadershipSignals: leadershipSignals * 100,
        mentorshipHours,
        isReady,
        timeToReadiness,
        lastAssessment: new Date(),
        nextAssessment: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
      },
      create: {
        userId,
        currentRole,
        targetRole,
        readinessScore: readinessScore * 100,
        attendance: attendance * 100,
        missionCompletion: missionCompletion * 100,
        leadershipSignals: leadershipSignals * 100,
        mentorshipHours,
        isReady,
        timeToReadiness,
      },
    });

    console.log(
      `📊 Leadership readiness assessed for ${user.firstName}: ${(readinessScore * 100).toFixed(1)}%`,
    );

    return readiness;
  }

  /**
   * Recommend users for promotion
   */
  async recommendPromotion(userId: string): Promise<PromotionRecommendation> {
    const readiness = await this.prisma.leadershipReadiness.findUnique({
      where: { userId },
      include: {
        user: true,
        assessments: {
          orderBy: {
            timestamp: 'desc',
          },
          take: 3,
        },
      },
    });

    if (!readiness) {
      throw new Error(`Leadership readiness not found for user ${userId}`);
    }

    const strengths: string[] = [];
    const growthAreas: string[] = [];

    if (readiness.attendance >= 80) strengths.push('Consistent attendance');
    else growthAreas.push('Improve attendance consistency');

    if (readiness.missionCompletion >= 80)
      strengths.push('Strong mission completion');
    else growthAreas.push('Complete more missions');

    if (readiness.leadershipSignals >= 80)
      strengths.push('Demonstrates leadership initiative');
    else growthAreas.push('Take more leadership initiative');

    if (readiness.mentorshipHours >= 20) strengths.push('Active mentor');
    else growthAreas.push('Engage in mentorship opportunities');

    const recommendedActions: string[] = [];
    if (!readiness.isReady) {
      if (readiness.attendance < 80)
        recommendedActions.push('Attend next 4 circle sessions');
      if (readiness.missionCompletion < 80)
        recommendedActions.push('Complete 3 additional missions');
      if (readiness.leadershipSignals < 80)
        recommendedActions.push('Lead 1 circle discussion or project');
      if (readiness.mentorshipHours < 20)
        recommendedActions.push('Mentor 2 younger youth members');
    }

    return {
      userId: readiness.userId,
      currentRole: readiness.currentRole,
      targetRole: readiness.targetRole,
      readinessScore: readiness.readinessScore,
      strengths,
      growthAreas,
      recommendedActions,
      timeToReadiness: readiness.timeToReadiness || 0,
      isReadyNow: readiness.isReady,
    };
  }

  /**
   * Plan succession for a leadership position
   */
  async planSuccession(currentLeaderId: string): Promise<SuccessionPlan> {
    const leader = await this.prisma.user.findUnique({
      where: { id: currentLeaderId },
      include: {
        roles: {
          include: {
            role: true,
          },
        },
        circlesLed: {
          include: {
            members: {
              include: {
                user: {
                  include: {
                    leadershipReadiness: true,
                  },
                },
              },
            },
          },
        },
        regionDirected: {
          include: {
            circles: {
              include: {
                members: {
                  include: {
                    user: {
                      include: {
                        leadershipReadiness: true,
                      },
                    },
                  },
                },
              },
            },
          },
        },
      },
    });

    if (!leader) {
      throw new Error(`Leader ${currentLeaderId} not found`);
    }

    const currentRole = leader.roles[0]?.role.name || RoleName.YOUTH_CAPTAIN;

    // Get all potential successors
    const candidates: SuccessorCandidate[] = [];

    // For circle captains, look at circle members
    if (currentRole === RoleName.YOUTH_CAPTAIN && leader.circlesLed.length > 0) {
      const circle = leader.circlesLed[0];
      for (const member of circle.members) {
        if (member.user.leadershipReadiness?.isReady) {
          candidates.push(this.toSuccessorCandidate(member.user));
        }
      }
    }

    // For regional directors, look at captains in region
    if (currentRole === RoleName.REGIONAL_DIRECTOR && leader.regionDirected.length > 0) {
      const region = leader.regionDirected[0];
      for (const circle of region.circles) {
        for (const member of circle.members) {
          if (member.user.leadershipReadiness?.targetRole === RoleName.REGIONAL_DIRECTOR) {
            candidates.push(this.toSuccessorCandidate(member.user));
          }
        }
      }
    }

    // Sort by readiness score
    candidates.sort((a, b) => b.readinessScore - a.readinessScore);

    const topCandidates = candidates.slice(0, 3);
    const riskLevel =
      topCandidates.length === 0
        ? 'high'
        : topCandidates[0].readinessScore >= 80
          ? 'low'
          : 'medium';

    return {
      currentLeaderId,
      currentRole,
      successors: topCandidates,
      riskLevel,
      recommendedTimeline: this.getSuccessionTimeline(topCandidates),
      developmentPlan: this.getDevelopmentPlan(topCandidates),
    };
  }

  /**
   * Identify leadership gaps across the system
   */
  async identifyLeadershipGaps(regionId?: string): Promise<LeadershipGap[]> {
    const gaps: LeadershipGap[] = [];

    // Find circles without captains
    const circlesWithoutCaptains = await this.prisma.circle.findMany({
      where: {
        regionId: regionId || undefined,
        captain: undefined,
      },
      include: {
        region: true,
        members: {
          include: {
            user: {
              include: {
                leadershipReadiness: true,
              },
            },
          },
        },
      },
    });

    for (const circle of circlesWithoutCaptains) {
      const potentials = circle.members
        .filter((m) => m.user.leadershipReadiness?.isReady)
        .map((m) => m.userId);

      gaps.push({
        gapType: 'missing_captain',
        circleId: circle.id,
        regionId: circle.regionId || undefined,
        severity: potentials.length > 0 ? 'medium' : 'high',
        description: `Circle ${circle.name} has no captain`,
        recommendedActions: potentials.length > 0
          ? ['Promote one of the ready members to captain']
          : ['Recruit external captain', 'Develop current members'],
        potentialCandidates: potentials,
      });
    }

    // Find regions without directors
    const regionsWithoutDirectors = await this.prisma.region.findMany({
      where: {
        id: regionId || undefined,
        director: undefined,
      },
    });

    for (const region of regionsWithoutDirectors) {
      gaps.push({
        gapType: 'missing_director',
        regionId: region.id,
        severity: 'critical',
        description: `Region ${region.name} has no director`,
        recommendedActions: [
          'Recruit experienced regional director',
          'Promote ambassador with strong track record',
          'Assign interim director from council',
        ],
        potentialCandidates: [],
      });
    }

    console.log(`🔍 Identified ${gaps.length} leadership gaps`);
    return gaps;
  }

  // Helper methods
  private calculateAttendance(attendance: any[]): number {
    if (attendance.length === 0) return 0;
    const present = attendance.filter((a) => a.status === 'PRESENT').length;
    return present / attendance.length;
  }

  private calculateMissionCompletion(assignments: any[]): number {
    if (assignments.length === 0) return 0;
    const completed = assignments.filter(
      (a) => a.submissions.length > 0 && a.submissions[0].status === 'APPROVED',
    ).length;
    return completed / assignments.length;
  }

  private calculateLeadershipSignals(user: any): number {
    // In production, this would analyze:
    // - Circle facilitation history
    // - Mentorship engagement
    // - Initiative taking
    // - Problem solving
    // - Collaboration quality
    return 0.75; // Placeholder
  }

  private getNextRole(currentRole: RoleName): RoleName {
    const progression: Record<RoleName, RoleName> = {
      [RoleName.YOUTH]: RoleName.YOUTH_CAPTAIN,
      [RoleName.YOUTH_CAPTAIN]: RoleName.AMBASSADOR,
      [RoleName.AMBASSADOR]: RoleName.REGIONAL_DIRECTOR,
      [RoleName.REGIONAL_DIRECTOR]: RoleName.COUNCIL,
      [RoleName.COUNCIL]: RoleName.ADMIN,
      [RoleName.ADMIN]: RoleName.ADMIN,
      [RoleName.CREATOR]: RoleName.EDUCATOR,
      [RoleName.EDUCATOR]: RoleName.COUNCIL,
    };

    return progression[currentRole] || currentRole;
  }

  private toSuccessorCandidate(user: any): SuccessorCandidate {
    const readiness = user.leadershipReadiness;
    return {
      userId: user.id,
      readinessScore: readiness?.readinessScore || 0,
      strengths: readiness?.readinessScore >= 80 ? ['Ready for leadership'] : [],
      developmentNeeds: readiness?.readinessScore < 80
        ? ['Continue building leadership skills']
        : [],
      estimatedReadiness: readiness?.isReady
        ? 'ready now'
        : `${readiness?.timeToReadiness || 30} days`,
    };
  }

  private getSuccessionTimeline(candidates: SuccessorCandidate[]): string {
    if (candidates.length === 0) return 'No successors identified - urgent recruitment needed';
    if (candidates[0].readinessScore >= 80) return 'Successor ready for immediate transition';
    return `${candidates[0].estimatedReadiness} - active development in progress`;
  }

  private getDevelopmentPlan(candidates: SuccessorCandidate[]): string[] {
    if (candidates.length === 0) {
      return [
        'Recruit external candidates',
        'Fast-track promising members',
        'Implement emergency succession protocol',
      ];
    }

    return [
      `Continue developing top ${candidates.length} candidates`,
      'Provide leadership shadowing opportunities',
      'Assign increasing responsibility',
      'Conduct monthly readiness assessments',
    ];
  }
}
