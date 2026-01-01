/**
 * Circle Domain Evaluators
 * 
 * Type-safe evaluator functions for Circle intelligence rules (C1-C7).
 * Each evaluator takes CircleWithRelations and returns InsightPayload or null.
 */

import { Circle, CircleMember, CircleSession, CircleAttendance, User } from '@prisma/client';
import { Evaluator, InsightPayload } from '../api/types/intelligence-api.types';

/**
 * Circle with all required relations for rule evaluation
 */
export type CircleWithRelations = Circle & {
  captain: User;
  members: CircleMember[];
  sessions: (CircleSession & {
    attendance: CircleAttendance[];
  })[];
};

/**
 * C2 - Attendance Drop
 * Detects circles with declining attendance rates
 */
function evaluateC2_AttendanceDrop(circle: CircleWithRelations): InsightPayload | null {
  // TODO: Implement attendance drop detection logic
  // Compare last 2 weeks vs previous 2 weeks
  // Trigger if drop > 20%
  return null;
}

/**
 * Array of all Circle domain evaluators
 * Add new evaluators here as C1, C3-C7 are implemented
 */
export const circleEvaluators: Array<Evaluator<CircleWithRelations>> = [
  evaluateC2_AttendanceDrop,
  // C1 - Circle Health Score
  // C3 - Captain Effectiveness
  // C4 - Circle Growth
  // C5 - Circle Stagnation
  // C6 - Session Quality
  // C7 - Member Retention
];

/**
 * Evaluate all Circle rules for a given circle
 * Returns array of triggered insights
 */
export function evaluateCircleRules(circle: CircleWithRelations): InsightPayload[] {
  return circleEvaluators
    .map(evaluator => evaluator(circle))
    .filter((insight): insight is InsightPayload => insight !== null);
}

/**
 * Build a unique fingerprint for an insight
 * Used for deduplication - same rule + same context = same fingerprint
 * 
 * @example
 * ```typescript
 * const fingerprint = buildInsightFingerprint(payload);
 * // => "C2_ATTENDANCE_DROP|circle_id:abc123"
 * ```
 */
export function buildInsightFingerprint(payload: InsightPayload): string {
  const keys = ["circle_id", "youth_id", "region_id", "mission_id"];
  const parts = keys
    .filter(k => payload.context[k] !== undefined)
    .map(k => `${k}:${payload.context[k]}`);

  return [payload.rule_code, ...parts].join("|");
}

/**
 * Persist insights to database with deduplication
 * Updates existing ACTIVE insights or creates new ones
 * 
 * @example
 * ```typescript
 * await persistInsights(prisma, insights);
 * ```
 */
export async function persistInsights(prisma: any, payloads: InsightPayload[]): Promise<void> {
  for (const payload of payloads) {
    const fingerprint = buildInsightFingerprint(payload);

    const existing = await prisma.insight.findFirst({
      where: {
        fingerprint,
        status: "ACTIVE"
      }
    });

    if (!existing) {
      await prisma.insight.create({
        data: {
          ...payload,
          context: payload.context,
          fingerprint,
          status: "ACTIVE"
        }
      });
    } else {
      await prisma.insight.update({
        where: { id: existing.id },
        data: {
          title: payload.title,
          message: payload.message,
          context: payload.context,
          priority: payload.priority,
          updated_at: new Date()
        }
      });
    }
  }
}

/**
 * Run Circle Intelligence batch job
 * Fetches all circles with relations, evaluates rules, and persists insights
 * 
 * @example
 * ```typescript
 * await runCircleIntelligence(prisma);
 * ```
 */
export async function runCircleIntelligence(prisma: any): Promise<InsightPayload[]> {
  const circles = await prisma.circle.findMany({
    include: {
      captain: true,
      members: true,
      sessions: {
        include: { attendance: true },
        orderBy: { scheduledAt: 'desc' }
      },
      region: true,
    }
  });

  const insights: InsightPayload[] = [];

  for (const circle of circles) {
    for (const evaluator of circleEvaluators) {
      const result = evaluator(circle);
      if (result) insights.push(result);
    }
  }

  return insights;
}
