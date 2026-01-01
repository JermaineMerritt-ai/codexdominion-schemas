import { IntelligenceItem } from '../intelligence.types';
import { IntelligenceRuleContext } from './rule-definitions';

/**
 * ===================================================================
 * CIRCLE INTELLIGENCE DOMAIN (C1-C7)
 * First complete intelligence domain with health scoring
 * ===================================================================
 */

/**
 * Helper to create properly formatted IntelligenceItem
 */
function createItem(
  ruleId: string,
  item: Omit<IntelligenceItem, 'ruleId' | 'timestamp'>
): IntelligenceItem {
  return {
    ...item,
    ruleId,
    timestamp: new Date().toISOString(),
  };
}

/**
 * C1 - Circle Health Score (Foundational Metric)
 * Computes 0-100 health score for each circle based on:
 * - Attendance rate (40%)
 * - Mission completion rate (40%)
 * - Session consistency (20%)
 */
export async function evaluateCircleHealthScore(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  // Get all circles in scope with 30 days of data
  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      members: true,
      sessions: {
        where: {
          scheduledAt: {
            gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          },
        },
        include: {
          attendance: true,
        },
      },
    },
  });

  for (const circle of circles) {
    const memberCount = circle.members.length;
    if (memberCount === 0 || circle.sessions.length === 0) continue;

    // 1. Attendance rate (40%)
    const totalSlots = circle.sessions.length * memberCount;
    const totalAttendance = circle.sessions.reduce(
      (sum, session) => sum + session.attendance.filter((a) => a.status === 'PRESENT').length,
      0
    );
    const attendanceRate = totalSlots > 0 ? (totalAttendance / totalSlots) * 100 : 0;

    // 2. Mission completion rate (40%)
    const submissions = await ctx.prisma.missionSubmission.findMany({
      where: {
        userId: { in: circle.members.map((m) => m.userId) },
        submittedAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
    });
    const missionCompletionRate = memberCount > 0 ? (submissions.length / memberCount) * 100 : 0;

    // 3. Session consistency (20%)
    const weeksInPeriod = 4;
    const sessionsPerWeek = circle.sessions.length / weeksInPeriod;
    const sessionConsistency = Math.min(sessionsPerWeek * 25, 100);

    const healthScore = Math.round(
      attendanceRate * 0.4 + missionCompletionRate * 0.4 + sessionConsistency * 0.2
    );

    const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;

    results.push(createItem('C1', {
      type: 'recommendation',
      domain: 'circles',
      message: `Circle ${circle.name} health score: ${healthScore}/100 (Attendance: ${Math.round(attendanceRate)}%, Missions: ${Math.round(missionCompletionRate)}%, Consistency: ${Math.round(sessionConsistency)}%)`,
      severity: healthScore < 50 ? 'high' : healthScore < 70 ? 'medium' : 'low',
      audience: ['captain', 'director', 'admin'],
      metadata: {
        circleId: circle.id,
        circleName: circle.name,
        healthScore,
        attendanceRate: Math.round(attendanceRate),
        missionCompletionRate: Math.round(missionCompletionRate),
        sessionConsistency: Math.round(sessionConsistency),
        captainName,
      },
    }));
  }

  return results;
}

/**
 * C2 - Attendance Drop Alert
 * Triggers when attendance drops >20% between consecutive sessions
 * Formula: drop = previousAvg - latestAvg
 *          if drop > 0.2 → alert
 */
export async function evaluateAttendanceDropAlert(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      members: true,
      sessions: {
        orderBy: { scheduledAt: 'desc' },
        take: 2,
        include: {
          attendance: true,
        },
      },
    },
  });

  for (const circle of circles) {
    if (circle.sessions.length < 2 || circle.members.length === 0) continue;

    const [latestSession, previousSession] = circle.sessions;
    const memberCount = circle.members.length;

    const latestAttendance = latestSession.attendance.filter((a) => a.status === 'PRESENT').length;
    const previousAttendance = previousSession.attendance.filter((a) => a.status === 'PRESENT').length;

    // Calculate averages (as decimals, not percentages)
    const latestAvg = latestAttendance / memberCount;
    const previousAvg = previousAttendance / memberCount;

    // drop = previousAvg - latestAvg
    const drop = previousAvg - latestAvg;

    // if drop > 0.2 → alert
    if (drop > 0.2) {
      const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;
      results.push(createItem('C2', {
        type: 'alert',
        domain: 'circles',
        message: `Circle ${circle.name} attendance dropped ${Math.round(drop * 100)}% over the last two sessions (from ${Math.round(previousAvg * 100)}% to ${Math.round(latestAvg * 100)}%).`,
        severity: 'high',
        audience: ['captain', 'director'],
        metadata: {
          circleId: circle.id,
          circleName: circle.name,
          drop: Math.round(drop * 1000) / 1000, // 3 decimal places
          dropPercentage: Math.round(drop * 100),
          previousAvg: Math.round(previousAvg * 1000) / 1000,
          latestAvg: Math.round(latestAvg * 1000) / 1000,
          previousRate: Math.round(previousAvg * 100),
          latestRate: Math.round(latestAvg * 100),
          captainName,
        },
      }));
    }
  }

  return results;
}

/**
 * C3 - Circle Growth Forecast
 * Calculates growth rate and forecasts next 30 days of membership growth
 * Formula: growthRate = (newMembersLast30Days / totalMembers)
 *          forecast = growthRate * 30-day projection
 */
export async function evaluateCircleGrowthForecast(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      _count: {
        select: {
          members: true,
        },
      },
    },
  });

  for (const circle of circles) {
    const totalMembers = circle._count.members;
    if (totalMembers === 0) continue;

    // Count new members in last 30 days at database level
    const newMembersLast30Days = await ctx.prisma.circleMember.count({
      where: {
        circleId: circle.id,
        joinedAt: { gte: thirtyDaysAgo },
      },
    });

    // Calculate growth rate
    const growthRate = totalMembers > 0 ? (newMembersLast30Days / totalMembers) : 0;

    // Forecast next 30 days (expected new members)
    const forecast = Math.round(growthRate * totalMembers);

    // Projected total in 30 days
    const projectedTotal = totalMembers + forecast;

    const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;

    // Determine severity and message based on growth patterns
    let severity: 'low' | 'medium' | 'high';
    let message: string;
    let type: 'recommendation' | 'opportunity' | 'alert';

    if (growthRate >= 0.2) {
      // High growth (20%+)
      severity = 'low';
      type = 'opportunity';
      message = `Circle ${circle.name} is experiencing high growth! Added ${newMembersLast30Days} members (${Math.round(growthRate * 100)}% growth). Forecast: ${forecast} more in next 30 days.`;
    } else if (growthRate >= 0.1) {
      // Moderate growth (10-19%)
      severity = 'low';
      type = 'recommendation';
      message = `Circle ${circle.name} showing steady growth. Added ${newMembersLast30Days} members (${Math.round(growthRate * 100)}% growth). Forecast: ${forecast} more in next 30 days.`;
    } else if (growthRate > 0) {
      // Low growth (1-9%)
      severity = 'medium';
      type = 'recommendation';
      message = `Circle ${circle.name} has slow growth. Only ${newMembersLast30Days} new members (${Math.round(growthRate * 100)}% growth). Consider outreach initiatives.`;
    } else {
      // No growth
      severity = 'high';
      type = 'alert';
      message = `Circle ${circle.name} has no new members in 30 days. Growth stagnant. Captain support needed.`;
    }

    results.push(createItem('C3', {
      type,
      domain: 'circles',
      message,
      severity,
      audience: ['captain', 'director', 'admin'],
      metadata: {
        circleId: circle.id,
        circleName: circle.name,
        totalMembers,
        newMembersLast30Days,
        growthRate: Math.round(growthRate * 100), // Percentage
        forecast,
        projectedTotal,
        captainName,
      },
    }));
  }

  return results;
}

/**
 * C4 - Captain Support Recommendation
 * Recommends director check-in when circle health < 50
 */
export async function evaluateCaptainSupportRecommendation(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          id: true,
          firstName: true,
          lastName: true,
        },
      },
      members: true,
      sessions: {
        where: {
          scheduledAt: {
            gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          },
        },
        include: {
          attendance: true,
        },
      },
    },
  });

  for (const circle of circles) {
    const memberCount = circle.members.length;
    if (memberCount === 0 || circle.sessions.length === 0) continue;

    // Compute simplified health score
    const totalSlots = circle.sessions.length * memberCount;
    const totalAttendance = circle.sessions.reduce(
      (sum, session) => sum + session.attendance.filter((a) => a.status === 'PRESENT').length,
      0
    );
    const attendanceRate = totalSlots > 0 ? (totalAttendance / totalSlots) * 100 : 0;

    const submissions = await ctx.prisma.missionSubmission.findMany({
      where: {
        userId: { in: circle.members.map((m) => m.userId) },
        submittedAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
    });
    const missionCompletionRate = memberCount > 0 ? (submissions.length / memberCount) * 100 : 0;

    const weeksInPeriod = 4;
    const sessionsPerWeek = circle.sessions.length / weeksInPeriod;
    const sessionConsistency = Math.min(sessionsPerWeek * 25, 100);

    const healthScore = Math.round(
      attendanceRate * 0.4 + missionCompletionRate * 0.4 + sessionConsistency * 0.2
    );

    if (healthScore < 50) {
      const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;
      results.push(createItem('C4', {
        type: 'recommendation',
        domain: 'circles',
        message: `Recommend a check-in with Captain ${captainName} — Circle ${circle.name} needs support (health score: ${healthScore}/100).`,
        severity: 'high',
        audience: ['director'],
        metadata: {
          circleId: circle.id,
          circleName: circle.name,
          captainId: circle.captain.id,
          captainName,
          healthScore,
        },
      }));
    }
  }

  return results;
}

/**
 * C5 - Circle Cohesion Signal
 * Detects high attendance (>70%) + low mission completion (<30%)
 */
export async function evaluateCircleCohesionSignal(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      members: true,
      sessions: {
        where: {
          scheduledAt: {
            gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          },
        },
        include: {
          attendance: true,
        },
      },
    },
  });

  for (const circle of circles) {
    const memberCount = circle.members.length;
    if (memberCount === 0 || circle.sessions.length === 0) continue;

    // Attendance rate
    const totalSlots = circle.sessions.length * memberCount;
    const totalAttendance = circle.sessions.reduce(
      (sum, session) => sum + session.attendance.filter((a) => a.status === 'PRESENT').length,
      0
    );
    const attendanceRate = totalSlots > 0 ? (totalAttendance / totalSlots) * 100 : 0;

    // Mission completion rate
    const submissions = await ctx.prisma.missionSubmission.findMany({
      where: {
        userId: { in: circle.members.map((m) => m.userId) },
        submittedAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
    });
    const missionCompletionRate = memberCount > 0 ? (submissions.length / memberCount) * 100 : 0;

    // High attendance + low missions = cohesion but low execution
    if (attendanceRate > 70 && missionCompletionRate < 30) {
      const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;
      results.push(createItem('C5', {
        type: 'recommendation',
        domain: 'circles',
        message: `Circle ${circle.name} shows strong cohesion but low execution (${Math.round(attendanceRate)}% attendance, ${Math.round(missionCompletionRate)}% mission completion).`,
        severity: 'medium',
        audience: ['captain', 'director'],
        metadata: {
          circleId: circle.id,
          circleName: circle.name,
          attendanceRate: Math.round(attendanceRate),
          missionCompletionRate: Math.round(missionCompletionRate),
          captainName,
        },
      }));
    }
  }

  return results;
}

/**
 * C6 - Circle Split Recommendation
 * Recommends splitting when circle > 20 members
 */
export async function evaluateCircleSplitRecommendation(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      _count: {
        select: { members: true },
      },
    },
  });

  for (const circle of circles) {
    const memberCount = circle._count.members;

    if (memberCount > 20) {
      const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;
      results.push(createItem('C6', {
        type: 'recommendation',
        domain: 'circles',
        message: `Circle ${circle.name} is large enough to split into two circles (${memberCount} members).`,
        severity: 'medium',
        audience: ['director', 'admin'],
        metadata: {
          circleId: circle.id,
          circleName: circle.name,
          memberCount,
          captainName,
        },
      }));
    }
  }

  return results;
}

/**
 * C7 - Circle Spotlight Recommendation
 * Recognizes circles with health score > 90 for 4+ weeks
 */
export async function evaluateCircleSpotlightRecommendation(
  ctx: IntelligenceRuleContext,
  options: { regionId?: string; userId?: string; roles?: string[] }
): Promise<IntelligenceItem[]> {
  const results: IntelligenceItem[] = [];

  const circles = await ctx.prisma.circle.findMany({
    where: {
      regionId: options.regionId || undefined,
    },
    include: {
      captain: {
        select: {
          firstName: true,
          lastName: true,
        },
      },
      members: true,
      sessions: {
        where: {
          scheduledAt: {
            gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          },
        },
        include: {
          attendance: true,
        },
      },
    },
  });

  for (const circle of circles) {
    const memberCount = circle.members.length;
    if (memberCount === 0 || circle.sessions.length < 4) continue;

    // Compute health score
    const totalSlots = circle.sessions.length * memberCount;
    const totalAttendance = circle.sessions.reduce(
      (sum, session) => sum + session.attendance.filter((a) => a.status === 'PRESENT').length,
      0
    );
    const attendanceRate = totalSlots > 0 ? (totalAttendance / totalSlots) * 100 : 0;

    const submissions = await ctx.prisma.missionSubmission.findMany({
      where: {
        userId: { in: circle.members.map((m) => m.userId) },
        submittedAt: {
          gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        },
      },
    });
    const missionCompletionRate = memberCount > 0 ? (submissions.length / memberCount) * 100 : 0;

    const weeksInPeriod = 4;
    const sessionsPerWeek = circle.sessions.length / weeksInPeriod;
    const sessionConsistency = Math.min(sessionsPerWeek * 25, 100);

    const healthScore = Math.round(
      attendanceRate * 0.4 + missionCompletionRate * 0.4 + sessionConsistency * 0.2
    );

    if (healthScore > 90) {
      const captainName = `${circle.captain.firstName} ${circle.captain.lastName}`;
      results.push(createItem('C7', {
        type: 'opportunity',
        domain: 'circles',
        message: `Circle ${circle.name} is eligible for regional spotlight (health score: ${healthScore}/100 for 4 weeks).`,
        severity: 'low',
        audience: ['director', 'admin'],
        metadata: {
          circleId: circle.id,
          circleName: circle.name,
          healthScore,
          captainName,
        },
      }));
    }
  }

  return results;
}
