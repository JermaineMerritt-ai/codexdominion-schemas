// Strategic Intelligence Type Definitions

import {
  RecommendationType,
  RecommendationPriority,
  RecommendationStatus,
  AlertDomain,
} from '@prisma/client';

export interface ActionItem {
  step: number;
  action: string;
  owner: string;
  dueWeeks: number;
}

export interface SuccessMetrics {
  [key: string]: any;
}

export interface StrategicContext {
  userId?: string;
  circleId?: string;
  regionId?: string;
  seasonId?: string;
  domain?: AlertDomain;
  priority?: RecommendationPriority[];
}

export interface RecommendationSummary {
  total: number;
  byPriority: Record<RecommendationPriority, number>;
  byDomain: Record<AlertDomain, number>;
  estimatedImplementationDays: number;
}

export interface YouthTrajectoryData {
  trend: 'rising' | 'stable' | 'declining';
  confidence: number;
  forecasts: {
    leadershipReadiness: number;
    burnoutRisk: number;
    creatorPotential: number;
    atRiskProbability: number;
  };
}

export interface CircleLifecycleData {
  stage: 'growth' | 'stable' | 'decline' | 'collapse';
  confidence: number;
  forecasts: {
    memberCount: number;
    healthScore: number;
    collapseRisk: number;
    splitRecommended: boolean;
    growthVelocity: number;
  };
}

export interface MissionPredictionData {
  predictedCompletionRate: number;
  difficulty: 'easy' | 'medium' | 'hard' | 'extreme';
  predictedDropOffPoints: number[];
  confidence: number;
}
