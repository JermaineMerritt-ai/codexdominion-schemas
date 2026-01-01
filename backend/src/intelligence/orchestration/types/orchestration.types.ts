// =============================================================================
// ORCHESTRATION LAYER - Type Definitions
// =============================================================================
// The Dominion's heartbeat - synchronizes cycles, coordinates engines

import { EngineName, EngineStatus, CycleType, CycleStatus, CycleScope, LinkType, ActionType, ActionStatus, CivilizationEventType, EventStatus } from '@prisma/client';

// =============================================================================
// ENGINE SYNCHRONIZATION
// =============================================================================

export interface EngineHealthReport {
  engineName: EngineName;
  status: EngineStatus;
  health: number; // 0-1
  lastHeartbeat: Date;
  metrics: Record<string, any>;
  issues: EngineIssue[];
  dependencies: DependencyStatus[];
}

export interface EngineIssue {
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  detectedAt: Date;
  suggestedAction?: string;
}

export interface DependencyStatus {
  dependsOn: EngineName;
  status: 'HEALTHY' | 'DEGRADED' | 'BLOCKED';
  lastSync: Date;
}

export interface EngineConflict {
  engine1: EngineName;
  engine2: EngineName;
  conflictType: string;
  description: string;
  resolution: string;
  priority: number; // 1-10
}

export interface EngineSequence {
  engines: EngineName[];
  sequenceType: string;
  estimatedDuration: number; // minutes
  steps: SequenceStep[];
}

export interface SequenceStep {
  step: number;
  engine: EngineName;
  action: string;
  duration: number; // minutes
  dependencies: number[]; // step numbers
}

// =============================================================================
// SEASONAL ORCHESTRATION
// =============================================================================

export interface SeasonalAlignment {
  seasonId: string;
  seasonName: string;
  overallScore: number; // 0-1
  curriculum: AlignmentDimension;
  missions: AlignmentDimension;
  creators: AlignmentDimension;
  exchange: AlignmentDimension;
  intelligence: AlignmentDimension;
  transitionStatus: 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED';
  transitionProgress: number; // 0-1
}

export interface AlignmentDimension {
  aligned: boolean;
  score: number; // 0-1
  issues: string[];
  recommendations: string[];
}

export interface SeasonTransitionPlan {
  fromSeasonId: string;
  toSeasonId: string;
  startDate: Date;
  targetCompletionDate: Date;
  steps: TransitionStep[];
  blockers: string[];
  readiness: number; // 0-1
}

export interface TransitionStep {
  step: number;
  name: string;
  engine: EngineName;
  action: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  estimatedDuration: number; // minutes
  actualDuration?: number;
}

// =============================================================================
// REGIONAL ORCHESTRATION
// =============================================================================

export interface RegionalCoordination {
  regionId: string;
  regionName: string;
  syncedWithGlobal: boolean;
  autonomyLevel: number; // 0-1
  coordinationScore: number; // 0-1
  customizations: RegionalCustomization;
  nextSync: Date;
  issues: string[];
}

export interface RegionalCustomization {
  culturalThemes: string[];
  languagePreferences: string[];
  customRituals: string[];
  cycleTiming: {
    missionCycleStart: Date;
    curriculumCycleStart: Date;
    creatorCycleStart: Date;
  };
}

export interface RegionalSyncResult {
  regionId: string;
  syncedAt: Date;
  success: boolean;
  itemsSynced: number;
  conflicts: RegionalConflict[];
  nextSyncDate: Date;
}

export interface RegionalConflict {
  type: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
  resolution: string;
}

// =============================================================================
// MISSION-CURRICULUM ALIGNMENT
// =============================================================================

export interface MissionCurriculumAlignment {
  missionId: string;
  missionTitle: string;
  linkedModules: ModuleLink[];
  alignmentScore: number; // 0-1
  prerequisitesMet: boolean;
  readiness: number; // 0-1
  recommendations: string[];
}

export interface ModuleLink {
  moduleId: string;
  moduleTitle: string;
  linkType: LinkType;
  alignmentScore: number; // 0-1
  required: boolean;
  completionRequired: number; // 0-1
}

export interface PrerequisiteCheck {
  missionId: string;
  userId: string;
  allPrerequisitesMet: boolean;
  missingPrerequisites: MissingPrerequisite[];
  readiness: number; // 0-1
  estimatedTimeToReady: number; // days
}

export interface MissingPrerequisite {
  moduleId: string;
  moduleTitle: string;
  completion: number; // 0-1
  estimatedTimeToComplete: number; // hours
}

// =============================================================================
// CREATOR-SEASON ORCHESTRATION
// =============================================================================

export interface CreatorSeasonSync {
  seasonId: string;
  seasonName: string;
  activeChallenges: SeasonalChallenge[];
  alignmentScore: number; // 0-1
  participation: number; // count
  submissionCount: number;
  qualityScore: number; // 0-1
}

export interface SeasonalChallenge {
  challengeId: string;
  title: string;
  seasonalTheme: string;
  themeScore: number; // 0-1
  launchDate: Date;
  endDate: Date;
  peakDate?: Date;
  linkedMissions: string[];
  linkedCurriculum: string[];
  participation: number;
  submissions: number;
}

export interface CreativeRenaissance {
  seasonId: string;
  startDate: Date;
  endDate: Date;
  themes: string[];
  targetChallenges: number;
  targetParticipation: number;
  targetSubmissions: number;
  events: RenaissanceEvent[];
}

export interface RenaissanceEvent {
  type: 'LAUNCH' | 'SPOTLIGHT' | 'SHOWCASE' | 'AWARDS';
  date: Date;
  description: string;
  participants: number;
}

// =============================================================================
// INTELLIGENCE-LEADERSHIP ORCHESTRATION
// =============================================================================

export interface IntelligenceTrigger {
  insightType: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  sourceEngine: EngineName;
  detectedAt: Date;
  actionType: ActionType;
  targetRole: string;
  targetUserId?: string;
  actionDescription: string;
  priority: number; // 1-10
  estimatedImpact: number; // 0-1
}

export interface ActionExecution {
  actionId: string;
  status: ActionStatus;
  assignedTo: string[];
  startedAt?: Date;
  completedAt?: Date;
  executedBy?: string;
  outcome?: string;
  impactScore?: number; // 0-1
}

export interface ActionImpact {
  actionId: string;
  actionType: ActionType;
  executedAt: Date;
  impactScore: number; // 0-1
  beforeMetrics: Record<string, number>;
  afterMetrics: Record<string, number>;
  improvement: number; // percentage
}

// =============================================================================
// EXCHANGE ORCHESTRATION
// =============================================================================

export interface ExchangeSync {
  entityType: string;
  entityId: string;
  exchangeLessonId?: string;
  financialTool?: string;
  alignmentTheme: string;
  integrationScore: number; // 0-1
  youthEngaged: number;
  toolsUsed: number;
  lessonsCompleted: number;
}

export interface FinancialCoherence {
  seasonId: string;
  overallCoherence: number; // 0-1
  missionIntegration: number; // 0-1
  curriculumIntegration: number; // 0-1
  creatorIntegration: number; // 0-1
  youthEngagement: number; // 0-1
  recommendations: string[];
}

// =============================================================================
// CIVILIZATION-WIDE ORCHESTRATION
// =============================================================================

export interface CivilizationPulse {
  timestamp: Date;
  overallHealth: number; // 0-1
  engineHealth: Record<EngineName, number>; // 0-1 each
  seasonalAlignment: number; // 0-1
  regionalCoordination: number; // 0-1
  culturalVitality: number; // 0-1
  activeYouth: number;
  activeCreators: number;
  activeChallenges: number;
  upcomingEvents: number;
  criticalIssues: string[];
}

export interface EpochTransition {
  name: string;
  type: 'SEASONAL' | 'CULTURAL' | 'LEADERSHIP' | 'EXPANSION';
  startDate: Date;
  endDate: Date;
  scope: CycleScope;
  involvedRegions: string[];
  coordinationPlan: TransitionStep[];
  readiness: number; // 0-1
  blockers: string[];
}

export interface CulturalRitual {
  name: string;
  type: CivilizationEventType;
  scheduledAt: Date;
  duration: number; // minutes
  scope: CycleScope;
  regionId?: string;
  ritualSteps: RitualStep[];
  expectedParticipants: number;
  culturalImpact: number; // 0-1 expected
}

export interface RitualStep {
  order: number;
  name: string;
  description: string;
  duration: number; // minutes
  participants: string[]; // role names
}

// =============================================================================
// DTOs - Request/Response Objects
// =============================================================================

export interface SyncAllEnginesDto {
  forceSync?: boolean;
  specificEngines?: EngineName[];
}

export interface TransitionSeasonDto {
  toSeasonId: string;
  startDate: Date;
  dryRun?: boolean;
}

export interface LinkMissionCurriculumDto {
  missionId: string;
  moduleId: string;
  linkType: LinkType;
  moduleRequired: boolean;
  moduleCompletion?: number; // 0-1
}

export interface LaunchSeasonalChallengeDto {
  challengeId: string;
  seasonId: string;
  launchDate: Date;
  endDate: Date;
  peakDate?: Date;
  linkedMissions?: string[];
  linkedCurriculum?: string[];
}

export interface TriggerActionDto {
  insightType: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  sourceEngine: EngineName;
  actionType: ActionType;
  targetRole: string;
  targetUserId?: string;
  actionDescription: string;
  priority: number; // 1-10
  sourceData: Record<string, any>;
}

export interface IntegrateExchangeDto {
  entityType: string;
  entityId: string;
  exchangeLessonId?: string;
  financialTool?: string;
  alignmentTheme: string;
}

export interface OrchestrateCivilizationEventDto {
  name: string;
  type: CivilizationEventType;
  scheduledAt: Date;
  duration: number; // minutes
  scope: CycleScope;
  regionId?: string;
  involvedEngines: EngineName[];
  ritualSteps: RitualStep[];
  expectedParticipants: number;
}

export interface CustomizeRegionalOrchestrationDto {
  regionId: string;
  culturalThemes?: string[];
  languagePreferences?: string[];
  customRituals?: string[];
  missionCycleStart?: Date;
  curriculumCycleStart?: Date;
  creatorCycleStart?: Date;
  autonomyLevel?: number; // 0-1
}

export interface ValidatePrerequisitesDto {
  missionId: string;
  userId: string;
}

export interface TrackAlignmentDto {
  seasonId: string;
  regionId?: string;
}

export interface MeasureImpactDto {
  actionId: string;
  beforeMetrics: Record<string, number>;
  afterMetrics: Record<string, number>;
}
