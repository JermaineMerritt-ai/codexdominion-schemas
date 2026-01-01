// ======================================================
// GOVERNANCE CONTROLLER
// API endpoints for civilization governance intelligence
// ======================================================

import { Controller, Get, Post, Param, Body } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { RoleName } from '@prisma/client';

import { CouncilCoordinationService } from './services/council-coordination.service';
import { ApprovalProtocolService } from './services/approval-protocol.service';
import { LeadershipOrchestrationService } from './services/leadership-orchestration.service';
import { RegionalGovernanceService } from './services/regional-governance.service';
import { PrismaService } from '../../prisma/prisma.service';

import {
  EscalateIssueDto,
  SubmitDecisionDto,
  ApproveDto,
  RejectDto,
  AutonomyDto,
  SupportDto,
  ScheduleMeetingDto,
  MinutesDto,
  MilestoneDto,
  MilestoneFiltersDto,
} from './types/governance.types';

@ApiTags('intelligence/governance')
@Controller('intelligence/governance')
export class GovernanceController {
  constructor(
    private councilCoordination: CouncilCoordinationService,
    private approvalProtocol: ApprovalProtocolService,
    private leadershipOrchestration: LeadershipOrchestrationService,
    private regionalGovernance: RegionalGovernanceService,
    private prisma: PrismaService,
  ) {}

  // ======================================================
  // COUNCIL COORDINATION (2 endpoints)
  // ======================================================

  @Get('council/insights/:role')
  @ApiOperation({ summary: 'Get routed insights for leadership role' })
  @ApiResponse({ status: 200, description: 'Insights successfully retrieved' })
  async getCouncilInsights(@Param('role') role: RoleName) {
    // In production, this would fetch insights from intelligence layers
    // and route them to the appropriate leadership level
    return {
      role,
      insights: [],
      message: `Insights for ${role} retrieved`,
    };
  }

  @Post('council/escalate')
  @ApiOperation({ summary: 'Escalate issue up leadership chain' })
  @ApiResponse({ status: 201, description: 'Issue successfully escalated' })
  async escalateIssue(@Body() dto: EscalateIssueDto) {
    await this.councilCoordination.escalateIssue(dto, dto.fromRole, dto.toRole);
    return {
      success: true,
      message: `Issue escalated from ${dto.fromRole} to ${dto.toRole}`,
    };
  }

  // ======================================================
  // APPROVAL PROTOCOLS (4 endpoints)
  // ======================================================

  @Post('approvals/submit')
  @ApiOperation({ summary: 'Submit decision for approval workflow' })
  @ApiResponse({ status: 201, description: 'Decision submitted for approval' })
  async submitApproval(@Body() dto: SubmitDecisionDto) {
    const decisionId = await this.approvalProtocol.submitForApproval(dto);
    return {
      decisionId,
      status: 'PENDING',
      message: 'Decision submitted for approval',
    };
  }

  @Post('approvals/:id/approve')
  @ApiOperation({ summary: 'Approve pending decision' })
  @ApiResponse({ status: 200, description: 'Decision approved' })
  async approveDecision(@Param('id') id: string, @Body() dto: ApproveDto) {
    await this.approvalProtocol.approveDecision(id, dto);
    const status = await this.approvalProtocol.getApprovalStatus(id);
    return {
      decisionId: id,
      status: status.status,
      currentApprovals: status.currentApprovals,
      requiredApprovals: status.requiredApprovals,
      canImplement: status.canImplement,
    };
  }

  @Post('approvals/:id/reject')
  @ApiOperation({ summary: 'Reject pending decision' })
  @ApiResponse({ status: 200, description: 'Decision rejected' })
  async rejectDecision(@Param('id') id: string, @Body() dto: RejectDto) {
    await this.approvalProtocol.rejectDecision(id, dto);
    return {
      decisionId: id,
      status: 'REJECTED',
      reason: dto.reason,
    };
  }

  @Get('approvals/pending')
  @ApiOperation({ summary: 'Get all pending approvals' })
  @ApiResponse({ status: 200, description: 'Pending approvals retrieved' })
  async getPendingApprovals() {
    const decisions = await this.prisma.governanceDecision.findMany({
      where: {
        status: {
          in: ['PENDING', 'UNDER_REVIEW'],
        },
      },
      include: {
        proposer: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
          },
        },
      },
      orderBy: {
        proposedAt: 'desc',
      },
      take: 50,
    });

    return {
      count: decisions.length,
      decisions: decisions.map((d) => ({
        id: d.id,
        type: d.type,
        title: d.title,
        proposedBy: `${d.proposer.firstName} ${d.proposer.lastName}`,
        proposedAt: d.proposedAt,
        status: d.status,
        currentApprovals: d.currentApprovals,
        requiredApprovals: d.requiredApprovals,
      })),
    };
  }

  // ======================================================
  // LEADERSHIP ORCHESTRATION (4 endpoints)
  // ======================================================

  @Get('leadership/readiness/:userId')
  @ApiOperation({ summary: 'Assess leadership readiness for user' })
  @ApiResponse({ status: 200, description: 'Readiness assessment retrieved' })
  async getLeadershipReadiness(@Param('userId') userId: string) {
    const readiness =
      await this.leadershipOrchestration.assessLeadershipReadiness(userId);
    return readiness;
  }

  @Get('leadership/promotions/recommended')
  @ApiOperation({ summary: 'Get recommended promotions' })
  @ApiResponse({ status: 200, description: 'Promotion recommendations retrieved' })
  async getRecommendedPromotions() {
    const readyUsers = await this.prisma.leadershipReadiness.findMany({
      where: {
        isReady: true,
      },
      include: {
        user: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
          },
        },
      },
      orderBy: {
        readinessScore: 'desc',
      },
      take: 20,
    });

    const recommendations = await Promise.all(
      readyUsers.map((r) =>
        this.leadershipOrchestration.recommendPromotion(r.userId),
      ),
    );

    return {
      count: recommendations.length,
      recommendations,
    };
  }

  @Get('leadership/gaps')
  @ApiOperation({ summary: 'Identify leadership gaps across system' })
  @ApiResponse({ status: 200, description: 'Leadership gaps identified' })
  async getLeadershipGaps() {
    const gaps = await this.leadershipOrchestration.identifyLeadershipGaps();
    return {
      count: gaps.length,
      gaps,
    };
  }

  @Post('leadership/succession/:userId/plan')
  @ApiOperation({ summary: 'Plan succession for leadership position' })
  @ApiResponse({ status: 200, description: 'Succession plan created' })
  async planSuccession(@Param('userId') userId: string) {
    const plan = await this.leadershipOrchestration.planSuccession(userId);
    return plan;
  }

  // ======================================================
  // REGIONAL GOVERNANCE (4 endpoints)
  // ======================================================

  @Get('regions/:id/health')
  @ApiOperation({ summary: 'Assess regional health' })
  @ApiResponse({ status: 200, description: 'Regional health assessment retrieved' })
  async getRegionalHealth(@Param('id') id: string) {
    const health = await this.regionalGovernance.assessRegionalHealth(id);
    return health;
  }

  @Get('regions/:id/alignment')
  @ApiOperation({ summary: 'Track regional alignment with Dominion standards' })
  @ApiResponse({ status: 200, description: 'Alignment score retrieved' })
  async getRegionalAlignment(@Param('id') id: string) {
    const alignment =
      await this.regionalGovernance.trackRegionalAlignment(id);
    return alignment;
  }

  @Post('regions/:id/autonomy')
  @ApiOperation({ summary: 'Grant regional autonomy level' })
  @ApiResponse({ status: 200, description: 'Autonomy level updated' })
  async grantAutonomy(@Param('id') id: string, @Body() dto: AutonomyDto) {
    await this.regionalGovernance.grantAutonomy(id, dto);
    return {
      regionId: id,
      autonomyLevel: dto.level,
      message: 'Autonomy level updated',
    };
  }

  @Post('regions/:id/support')
  @ApiOperation({ summary: 'Provide support to region' })
  @ApiResponse({ status: 201, description: 'Support request recorded' })
  async provideSupport(@Param('id') id: string, @Body() dto: SupportDto) {
    await this.regionalGovernance.provideSupport(id, dto);
    return {
      regionId: id,
      supportType: dto.supportType,
      urgency: dto.urgency,
      message: 'Support request recorded',
    };
  }

  // ======================================================
  // MEETINGS & COORDINATION (3 endpoints)
  // ======================================================

  @Post('meetings')
  @ApiOperation({ summary: 'Schedule governance meeting' })
  @ApiResponse({ status: 201, description: 'Meeting scheduled' })
  async scheduleMeeting(@Body() dto: ScheduleMeetingDto) {
    const meeting = await this.prisma.governanceMeeting.create({
      data: {
        type: dto.type as any,
        title: dto.title,
        description: dto.description,
        scheduledAt: dto.scheduledAt,
        duration: dto.duration,
        location: dto.location,
        attendees: dto.attendees as any,
        facilitator: dto.facilitator,
        agenda: dto.agenda as any,
        seasonId: dto.seasonId,
        regionId: dto.regionId,
        status: 'SCHEDULED',
      },
    });

    return {
      meetingId: meeting.id,
      message: 'Meeting scheduled successfully',
    };
  }

  @Get('meetings/upcoming')
  @ApiOperation({ summary: 'Get upcoming governance meetings' })
  @ApiResponse({ status: 200, description: 'Upcoming meetings retrieved' })
  async getUpcomingMeetings() {
    const meetings = await this.prisma.governanceMeeting.findMany({
      where: {
        scheduledAt: {
          gte: new Date(),
        },
        status: 'SCHEDULED',
      },
      orderBy: {
        scheduledAt: 'asc',
      },
      take: 20,
    });

    return {
      count: meetings.length,
      meetings,
    };
  }

  @Post('meetings/:id/minutes')
  @ApiOperation({ summary: 'Record meeting minutes' })
  @ApiResponse({ status: 201, description: 'Minutes recorded' })
  async recordMinutes(@Param('id') id: string, @Body() dto: MinutesDto) {
    const minutes = await this.prisma.meetingMinutes.create({
      data: {
        meetingId: id,
        recordedBy: dto.recordedBy,
        content: dto.content,
        decisions: dto.decisions as any,
        actionItems: dto.actionItems as any,
      },
    });

    // Update meeting status
    await this.prisma.governanceMeeting.update({
      where: { id },
      data: {
        status: 'COMPLETED',
        summary: dto.content.substring(0, 200),
      },
    });

    return {
      minutesId: minutes.id,
      message: 'Minutes recorded successfully',
    };
  }

  // ======================================================
  // CIVILIZATION GOVERNANCE (3 endpoints)
  // ======================================================

  @Get('civilization/milestones')
  @ApiOperation({ summary: 'Get civilization milestones' })
  @ApiResponse({ status: 200, description: 'Milestones retrieved' })
  async getMilestones(@Body() filters?: MilestoneFiltersDto) {
    const milestones = await this.prisma.civilizationMilestone.findMany({
      where: {
        type: filters?.type as any,
        seasonId: filters?.seasonId,
        regionId: filters?.regionId,
        celebrated: filters?.celebrated,
        achievedAt: {
          gte: filters?.startDate,
          lte: filters?.endDate,
        },
      },
      orderBy: {
        achievedAt: 'desc',
      },
      take: 50,
    });

    return {
      count: milestones.length,
      milestones,
    };
  }

  @Post('civilization/milestones')
  @ApiOperation({ summary: 'Record civilization milestone' })
  @ApiResponse({ status: 201, description: 'Milestone recorded' })
  async recordMilestone(@Body() dto: MilestoneDto) {
    const milestone = await this.prisma.civilizationMilestone.create({
      data: {
        type: dto.type as any,
        title: dto.title,
        description: dto.description,
        achievedBy: dto.achievedBy as any,
        impactScore: dto.impactScore,
        significance: dto.significance,
        seasonId: dto.seasonId,
        regionId: dto.regionId,
      },
    });

    return {
      milestoneId: milestone.id,
      message: 'Milestone recorded successfully',
    };
  }

  @Get('civilization/dashboard')
  @ApiOperation({ summary: 'Get civilization governance dashboard' })
  @ApiResponse({ status: 200, description: 'Dashboard data retrieved' })
  async getCivilizationDashboard() {
    // Aggregate governance metrics
    const [
      pendingDecisions,
      approvedDecisions,
      upcomingMeetings,
      readyLeaders,
      leadershipGaps,
      recentMilestones,
    ] = await Promise.all([
      this.prisma.governanceDecision.count({
        where: { status: 'PENDING' },
      }),
      this.prisma.governanceDecision.count({
        where: { status: 'APPROVED' },
      }),
      this.prisma.governanceMeeting.count({
        where: {
          scheduledAt: { gte: new Date() },
          status: 'SCHEDULED',
        },
      }),
      this.prisma.leadershipReadiness.count({
        where: { isReady: true },
      }),
      this.prisma.circle.count({
        where: { captain: undefined },
      }),
      this.prisma.civilizationMilestone.count({
        where: {
          achievedAt: {
            gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          },
        },
      }),
    ]);

    return {
      governance: {
        pendingDecisions,
        approvedDecisions,
        upcomingMeetings,
      },
      leadership: {
        readyForPromotion: readyLeaders,
        criticalGaps: leadershipGaps,
      },
      civilization: {
        milestonesThisMonth: recentMilestones,
      },
      flame: '🔥 Governance Intelligence Operational',
    };
  }
}
