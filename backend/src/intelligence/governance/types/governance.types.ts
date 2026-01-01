// ======================================================
// GOVERNANCE LAYER - TYPE DEFINITIONS
// Civilization Era Intelligence (Layer 7)
// ======================================================

import { RoleName } from '@prisma/client';

// Council Coordination Types
export interface DecisionFlow {
  decisionId: string;
  proposedBy: string;
  proposedRole: RoleName;
  currentLevel: RoleName;
  approvalPath: ApprovalStep[];
  status: string;
  daysInReview: number;
}

export interface ApprovalStep {
  order: number;
  role: RoleName;
  userId?: string;
  status: 'pending' | 'approved' | 'rejected';
  timestamp?: Date;
  notes?: string;
}

export interface EscalateIssueDto {
  issueType: string;
  description: string;
  fromRole: RoleName;
  toRole: RoleName;
  entityId?: string;
  entityType?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

// Approval Protocol Types
export interface ApprovalStatus {
  decisionId: string;
  status: string;
  currentApprovals: number;
  requiredApprovals: number;
  approvers: ApprovalStep[];
  canImplement: boolean;
  nextApprover?: RoleName;
}

export interface SubmitDecisionDto {
  type: string;
  domain: string;
  title: string;
  description: string;
  reasoning: string;
  proposedBy: string;
  entityId?: string;
  entityType?: string;
  seasonId?: string;
  regionId?: string;
  requiredApprovals?: number;
  impactScore?: number;
  impactDescription?: string;
}

export interface ApproveDto {
  approverId: string;
  notes?: string;
}

export interface RejectDto {
  approverId: string;
  reason: string;
}

// Leadership Orchestration Types
export interface PromotionRecommendation {
  userId: string;
  currentRole: RoleName;
  targetRole: RoleName;
  readinessScore: number;
  strengths: string[];
  growthAreas: string[];
  recommendedActions: string[];
  timeToReadiness: number; // days
  isReadyNow: boolean;
}

export interface SuccessionPlan {
  currentLeaderId: string;
  currentRole: RoleName;
  successors: SuccessorCandidate[];
  riskLevel: 'low' | 'medium' | 'high';
  recommendedTimeline: string;
  developmentPlan: string[];
}

export interface SuccessorCandidate {
  userId: string;
  readinessScore: number;
  strengths: string[];
  developmentNeeds: string[];
  estimatedReadiness: string; // e.g., "3 months", "ready now"
}

export interface LeadershipGap {
  gapType: string; // "missing_director", "missing_captain", "understaffed"
  regionId?: string;
  circleId?: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  recommendedActions: string[];
  potentialCandidates: string[]; // User IDs
}

// Regional Governance Types
export interface RegionalHealth {
  regionId: string;
  regionName: string;
  healthScore: number;
  autonomyLevel: string;
  metrics: {
    circleCount: number;
    youthCount: number;
    missionCompletion: number;
    attendanceRate: number;
    leadershipDepth: number;
  };
  strengths: string[];
  concerns: string[];
  recommendations: string[];
  needsSupport: boolean;
  supportAreas: string[];
}

export interface AlignmentScore {
  regionId: string;
  overall: number;
  dimensions: {
    culturalAlignment: number;
    missionAlignment: number;
    leadershipAlignment: number;
    operationalAlignment: number;
  };
  gaps: string[];
  recommendations: string[];
}

export interface AutonomyDto {
  level: 'SUPERVISED' | 'SEMI_AUTONOMOUS' | 'AUTONOMOUS';
  reason: string;
  effectiveDate?: Date;
}

export interface SupportDto {
  supportType: string; // "leadership", "curriculum", "operational", "financial"
  description: string;
  urgency: 'low' | 'medium' | 'high';
  requestedBy?: string;
}

// Meeting Types
export interface ScheduleMeetingDto {
  type: string;
  title: string;
  description?: string;
  scheduledAt: Date;
  duration: number; // minutes
  location?: string;
  attendees: MeetingAttendee[];
  facilitator?: string;
  agenda: AgendaItem[];
  seasonId?: string;
  regionId?: string;
}

export interface MeetingAttendee {
  userId: string;
  role: RoleName;
  status: 'confirmed' | 'declined' | 'pending';
}

export interface AgendaItem {
  order: number;
  topic: string;
  duration: number; // minutes
  presenter?: string;
  notes?: string;
}

export interface MinutesDto {
  meetingId: string;
  recordedBy: string;
  content: string; // Markdown
  decisions: string[]; // Decision IDs
  actionItems: ActionItem[];
}

export interface ActionItem {
  description: string;
  assignedTo?: string;
  dueDate?: Date;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in_progress' | 'completed';
}

// Civilization Milestone Types
export interface MilestoneDto {
  type: string;
  title: string;
  description: string;
  achievedBy: Contributor[];
  impactScore: number;
  significance: string;
  seasonId?: string;
  regionId?: string;
}

export interface Contributor {
  userId: string;
  contribution: string;
}

export interface MilestoneFiltersDto {
  type?: string;
  seasonId?: string;
  regionId?: string;
  celebrated?: boolean;
  startDate?: Date;
  endDate?: Date;
}
