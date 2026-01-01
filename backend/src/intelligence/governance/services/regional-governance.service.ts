// ======================================================
// REGIONAL GOVERNANCE SERVICE
// Manages regional autonomy and alignment
// ======================================================

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import {
  RegionalHealth,
  AlignmentScore,
  AutonomyDto,
  SupportDto,
} from '../types/governance.types';

@Injectable()
export class RegionalGovernanceService {
  constructor(private prisma: PrismaService) {}

  /**
   * Assess overall regional health
   */
  async assessRegionalHealth(regionId: string): Promise<RegionalHealth> {
    const region = await this.prisma.region.findUnique({
      where: { id: regionId },
      include: {
        circles: {
          include: {
            members: true,
            sessions: {
              include: {
                attendance: true,
              },
            },
            missionAssignments: {
              include: {
                submissions: true,
              },
            },
          },
        },
        governance: true,
        director: true,
      },
    });

    if (!region) {
      throw new Error(`Region ${regionId} not found`);
    }

    // Calculate metrics
    const circleCount = region.circles.length;
    const youthCount = region.circles.reduce(
      (sum, c) => sum + c.members.length,
      0,
    );

    // Mission completion rate
    const totalMissions = region.circles.reduce(
      (sum, c) => sum + c.missionAssignments.length,
      0,
    );
    const completedMissions = region.circles.reduce(
      (sum, c) =>
        sum +
        c.missionAssignments.filter(
          (a) =>
            a.submissions.length > 0 && a.submissions[0].status === 'APPROVED',
        ).length,
      0,
    );
    const missionCompletion =
      totalMissions > 0 ? (completedMissions / totalMissions) * 100 : 0;

    // Attendance rate
    const totalAttendance = region.circles.reduce(
      (sum, c) => sum + c.sessions.reduce((s, sess) => s + sess.attendance.length, 0),
      0,
    );
    const presentAttendance = region.circles.reduce(
      (sum, c) =>
        sum +
        c.sessions.reduce(
          (s, sess) =>
            s + sess.attendance.filter((a) => a.status === 'PRESENT').length,
          0,
        ),
      0,
    );
    const attendanceRate =
      totalAttendance > 0 ? (presentAttendance / totalAttendance) * 100 : 0;

    // Leadership depth (percentage of roles filled)
    const leadershipDepth = region.director ? 100 : 0;

    // Calculate health score (weighted average)
    const healthScore =
      circleCount * 0.1 * 10 + // 10 circles = 10 points
      youthCount * 0.05 + // 20 youth = 10 points (up to 50)
      missionCompletion * 0.4 + // 40% weight
      attendanceRate * 0.3 + // 30% weight
      leadershipDepth * 0.2; // 20% weight

    // Identify strengths and concerns
    const strengths: string[] = [];
    const concerns: string[] = [];
    const recommendations: string[] = [];

    if (circleCount >= 5) strengths.push('Strong circle network');
    else concerns.push('Limited circle coverage');

    if (youthCount >= 30) strengths.push('Healthy youth participation');
    else concerns.push('Low youth enrollment');

    if (missionCompletion >= 70) strengths.push('High mission completion');
    else {
      concerns.push('Low mission completion');
      recommendations.push('Review mission difficulty and support');
    }

    if (attendanceRate >= 75) strengths.push('Consistent attendance');
    else {
      concerns.push('Attendance challenges');
      recommendations.push('Improve engagement strategies');
    }

    if (!region.director) {
      concerns.push('No regional director');
      recommendations.push('Appoint regional director urgently');
    }

    // Determine autonomy level
    const autonomyLevel =
      healthScore >= 80
        ? 'AUTONOMOUS'
        : healthScore >= 60
          ? 'SEMI_AUTONOMOUS'
          : 'SUPERVISED';

    // Update or create governance record
    await this.prisma.regionalGovernance.upsert({
      where: { regionId },
      update: {
        healthScore,
        autonomyLevel,
        circleCount,
        youthCount,
        missionCompletion,
        needsSupport: healthScore < 60,
        supportAreas: concerns,
        lastReview: new Date(),
        nextReview: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000), // 90 days
      },
      create: {
        regionId,
        healthScore,
        autonomyLevel,
        circleCount,
        youthCount,
        missionCompletion,
        needsSupport: healthScore < 60,
        supportAreas: concerns,
      },
    });

    console.log(
      `🏛️ Regional health assessed: ${region.name} - ${healthScore.toFixed(1)}% (${autonomyLevel})`,
    );

    return {
      regionId,
      regionName: region.name,
      healthScore,
      autonomyLevel,
      metrics: {
        circleCount,
        youthCount,
        missionCompletion,
        attendanceRate,
        leadershipDepth,
      },
      strengths,
      concerns,
      recommendations,
      needsSupport: healthScore < 60,
      supportAreas: concerns,
    };
  }

  /**
   * Grant regional autonomy level
   */
  async grantAutonomy(regionId: string, dto: AutonomyDto): Promise<void> {
    const region = await this.prisma.region.findUnique({
      where: { id: regionId },
      include: {
        governance: true,
      },
    });

    if (!region) {
      throw new Error(`Region ${regionId} not found`);
    }

    // Validate autonomy level against health score
    if (dto.level === 'AUTONOMOUS' && region.governance && region.governance.healthScore < 80) {
      throw new Error(
        `Region health score (${region.governance.healthScore}) too low for AUTONOMOUS status (requires 80+)`,
      );
    }

    if (dto.level === 'SEMI_AUTONOMOUS' && region.governance && region.governance.healthScore < 60) {
      throw new Error(
        `Region health score (${region.governance.healthScore}) too low for SEMI_AUTONOMOUS status (requires 60+)`,
      );
    }

    await this.prisma.regionalGovernance.update({
      where: { regionId },
      data: {
        autonomyLevel: dto.level,
        lastReview: new Date(),
      },
    });

    console.log(`🎖️ Region ${region.name} autonomy set to ${dto.level}: ${dto.reason}`);
  }

  /**
   * Provide support to region
   */
  async provideSupport(regionId: string, dto: SupportDto): Promise<void> {
    const region = await this.prisma.region.findUnique({
      where: { id: regionId },
      include: {
        governance: true,
      },
    });

    if (!region) {
      throw new Error(`Region ${regionId} not found`);
    }

    const supportAreas = region.governance?.supportAreas as string[] || [];
    if (!supportAreas.includes(dto.supportType)) {
      supportAreas.push(dto.supportType);
    }

    await this.prisma.regionalGovernance.update({
      where: { regionId },
      data: {
        needsSupport: true,
        supportAreas,
        escalations: (region.governance?.escalations || 0) + 1,
      },
    });

    // In production, this would:
    // 1. Create support ticket
    // 2. Assign support team
    // 3. Schedule intervention
    // 4. Track resolution

    console.log(
      `🚨 Support request for ${region.name}: ${dto.supportType} (${dto.urgency} priority)`,
    );
  }

  /**
   * Track regional alignment with Dominion standards
   */
  async trackRegionalAlignment(regionId: string): Promise<AlignmentScore> {
    const region = await this.prisma.region.findUnique({
      where: { id: regionId },
      include: {
        circles: {
          include: {
            sessions: true,
            missionAssignments: {
              include: {
                submissions: true,
                mission: true,
              },
            },
          },
        },
        culturalStories: true,
      },
    });

    if (!region) {
      throw new Error(`Region ${regionId} not found`);
    }

    // Cultural alignment (using cultural stories as proxy)
    const culturalAlignment =
      region.culturalStories.length >= 4 ? 100 : region.culturalStories.length * 25;

    // Mission alignment (completion rate)
    const totalMissions = region.circles.reduce(
      (sum, c) => sum + c.missionAssignments.length,
      0,
    );
    const alignedMissions = region.circles.reduce(
      (sum, c) =>
        sum +
        c.missionAssignments.filter((a) => {
          // Check if mission is from current season
          return a.mission && a.submissions.length > 0;
        }).length,
      0,
    );
    const missionAlignment =
      totalMissions > 0 ? (alignedMissions / totalMissions) * 100 : 0;

    // Leadership alignment (director present)
    const leadershipAlignment = region.directorId ? 100 : 0;

    // Operational alignment (regular sessions)
    const totalSessions = region.circles.reduce(
      (sum, c) => sum + c.sessions.length,
      0,
    );
    const operationalAlignment = totalSessions >= 12 ? 100 : (totalSessions / 12) * 100;

    // Overall alignment
    const overall =
      (culturalAlignment +
        missionAlignment +
        leadershipAlignment +
        operationalAlignment) /
      4;

    const gaps: string[] = [];
    if (culturalAlignment < 75) gaps.push('Increase cultural content engagement');
    if (missionAlignment < 75) gaps.push('Improve mission participation');
    if (leadershipAlignment < 75) gaps.push('Establish regional director');
    if (operationalAlignment < 75) gaps.push('Increase session frequency');

    const recommendations: string[] = [];
    if (overall < 75) {
      recommendations.push('Schedule alignment workshop with council');
      recommendations.push('Review and adopt Dominion best practices');
      recommendations.push('Increase cultural ceremony participation');
    }

    console.log(
      `📐 Regional alignment: ${region.name} - ${overall.toFixed(1)}% aligned`,
    );

    return {
      regionId,
      overall,
      dimensions: {
        culturalAlignment,
        missionAlignment,
        leadershipAlignment,
        operationalAlignment,
      },
      gaps,
      recommendations,
    };
  }
}
