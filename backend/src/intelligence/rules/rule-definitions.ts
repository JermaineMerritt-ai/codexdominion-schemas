import { IntelligenceItem } from '../intelligence.types';
import { PrismaClient } from '@prisma/client';
import {
  evaluateCircleHealthScore,
  evaluateAttendanceDropAlert,
  evaluateCircleGrowthForecast,
  evaluateCaptainSupportRecommendation,
  evaluateCircleCohesionSignal,
  evaluateCircleSplitRecommendation,
  evaluateCircleSpotlightRecommendation,
} from './circle-rules';

export type RuleTrigger = 'weekly' | 'daily' | 'on_demand';

export interface IntelligenceRuleContext {
  prisma: PrismaClient;
  // add more shared services later if needed
}

export type RuleEvaluator = (
  ctx: IntelligenceRuleContext,
  options?: { regionId?: string; userId?: string; roles?: string[] }
) => Promise<IntelligenceItem[]>;

export interface IntelligenceRuleDefinition {
  id: string;               // e.g., 'Y2'
  name: string;             // e.g., 'At-Risk Youth Detection'
  trigger: RuleTrigger;
  domain: string;
  evaluator: RuleEvaluator;
}

// ---------- Example helpers ----------

const nowIso = () => new Date().toISOString();

// Example utility: compute average attendance for a session
function averageAttendance(
  attendanceRecords: { status: string }[]
): number {
  if (!attendanceRecords || attendanceRecords.length === 0) return 0;
  const presentCount = attendanceRecords.filter(
    (a) => a.status.toLowerCase() === 'present'
  ).length;
  return presentCount / attendanceRecords.length;
}

// ---------- Example rule evaluators ----------

// Y2 — At-Risk Youth Detection
const evaluateY2: RuleEvaluator = async (ctx) => {
  const { prisma } = ctx;

  // Example: last 3 weeks of data
  const threeWeeksAgo = new Date();
  threeWeeksAgo.setDate(threeWeeksAgo.getDate() - 21);

  const youths = await prisma.user.findMany({
    where: {
      roles: {
        some: {
          role: {
            name: 'YOUTH',
          },
        },
      },
    },
    include: {
      circleAttendance: {
        where: { 
          session: { 
            scheduledAt: { gte: threeWeeksAgo } 
          } 
        },
      },
      missionSubmissions: {
        where: { submittedAt: { gte: threeWeeksAgo } },
      },
      profile: true,
    },
  });

  const items: IntelligenceItem[] = [];

  for (const y of youths) {
    const attendanceCount =
      y.circleAttendance?.filter(
        (a: any) => a.status.toLowerCase() === 'present'
      ).length ?? 0;
    const submissionCount = y.missionSubmissions?.length ?? 0;

    // Very simple rule: no attendance & no submissions in last 3 weeks
    if (attendanceCount === 0 && submissionCount === 0) {
      const firstName = y.firstName || y.email.split('@')[0];
      const lastName = y.lastName || '';
      items.push({
        type: 'alert',
        domain: 'youth',
        ruleId: 'Y2',
        message: `${firstName} ${lastName} is at risk (no attendance or submissions in 3 weeks).`.trim(),
        severity: 'high',
        audience: ['captain', 'director'],
        timestamp: nowIso(),
        metadata: { userId: y.id },
      });
    }
  }

  return items;
};

// C2 — Circle Attendance Drop Alert
const evaluateC2: RuleEvaluator = async (ctx, options) => {
  const { prisma } = ctx;

  const circles = await prisma.circle.findMany({
    where: options?.regionId ? { regionId: options.regionId } : {},
    include: {
      sessions: {
        orderBy: { scheduledAt: 'desc' },
        take: 2,
        include: { attendance: true },
      },
    },
  });

  const items: IntelligenceItem[] = [];

  for (const circle of circles) {
    const [latest, previous] = circle.sessions;

    if (!latest || !previous) continue;

    const latestAvg = averageAttendance(latest.attendance);
    const previousAvg = averageAttendance(previous.attendance);

    const drop = previousAvg - latestAvg;

    if (drop > 0.2) {
      items.push({
        type: 'alert',
        domain: 'circles',
        ruleId: 'C2',
        message: `Circle "${circle.name}" attendance dropped by ${Math.round(
          drop * 100
        )}% over the last two sessions.`,
        severity: 'medium',
        audience: ['captain', 'director'],
        timestamp: nowIso(),
        metadata: { circleId: circle.id },
      });
    }
  }

  return items;
};

// M3 — Mission Success Forecast (simple example)
const evaluateM3: RuleEvaluator = async (ctx, options) => {
  const { prisma } = ctx;

  const missions = await prisma.mission.findMany({
    where: {},  // Remove regionId filter for now as it's not in Mission model
    include: { 
      submissions: true,
      assignments: true,
    },
  });

  const items: IntelligenceItem[] = [];

  for (const mission of missions) {
    const totalAssigned = mission.assignments?.length ?? 0;
    if (totalAssigned === 0) continue;

    const submissions = mission.submissions ?? [];
    const submittedCount = submissions.length;

    const completionRate = submittedCount / totalAssigned;

    if (completionRate >= 0.8) {
      items.push({
        type: 'forecast',
        domain: 'missions',
        ruleId: 'M3',
        message: `Mission "${mission.title}" is on track for high completion (~${Math.round(
          completionRate * 100
        )}%).`,
        audience: ['admin', 'director'],
        timestamp: nowIso(),
        metadata: { missionId: mission.id },
      });
    }
  }

  return items;
};

// ---------- Rule registry ----------

export const IntelligenceRules: IntelligenceRuleDefinition[] = [
  // ===================================================================
  // YOUTH DOMAIN (Y*)
  // ===================================================================
  {
    id: 'Y2',
    name: 'At-Risk Youth Detection',
    trigger: 'weekly',
    domain: 'youth',
    evaluator: evaluateY2,
  },

  // ===================================================================
  // CIRCLES DOMAIN (C1-C7) - FIRST COMPLETE DOMAIN
  // ===================================================================
  {
    id: 'C1',
    name: 'Circle Health Score',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCircleHealthScore,
  },
  {
    id: 'C2',
    name: 'Attendance Drop Alert',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateAttendanceDropAlert,
  },
  {
    id: 'C3',
    name: 'Circle Growth Forecast',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCircleGrowthForecast,
  },
  {
    id: 'C4',
    name: 'Captain Support Recommendation',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCaptainSupportRecommendation,
  },
  {
    id: 'C5',
    name: 'Circle Cohesion Signal',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCircleCohesionSignal,
  },
  {
    id: 'C6',
    name: 'Circle Split Recommendation',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCircleSplitRecommendation,
  },
  {
    id: 'C7',
    name: 'Circle Spotlight Recommendation',
    trigger: 'weekly',
    domain: 'circles',
    evaluator: evaluateCircleSpotlightRecommendation,
  },

  // ===================================================================
  // MISSIONS DOMAIN (M*)
  // ===================================================================
  {
    id: 'M3',
    name: 'Mission Success Forecast',
    trigger: 'weekly',
    domain: 'missions',
    evaluator: evaluateM3,
  },

  // TODO: add Y1, Y3–Y7, M1, M2, M4–M7, CU*, CL*, CR*, E*
];
