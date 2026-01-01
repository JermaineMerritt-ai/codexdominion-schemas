// ======================================================
// COUNCIL COORDINATION SERVICE
// Routes insights and manages escalations across leadership hierarchy
// ======================================================

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import { RoleName } from '@prisma/client';
import { DecisionFlow, EscalateIssueDto } from '../types/governance.types';

@Injectable()
export class CouncilCoordinationService {
  constructor(private prisma: PrismaService) {}

  /**
   * Route insight to appropriate leadership level
   * Insights flow downward from Council → Directors → Ambassadors → Captains → Youth
   */
  async routeInsight(insight: any, targetRole: RoleName): Promise<void> {
    // Leadership hierarchy (top to bottom)
    const hierarchy: RoleName[] = [
      RoleName.ADMIN,
      RoleName.COUNCIL,
      RoleName.REGIONAL_DIRECTOR,
      RoleName.AMBASSADOR,
      RoleName.YOUTH_CAPTAIN,
      RoleName.YOUTH,
    ];

    const targetIndex = hierarchy.indexOf(targetRole);
    if (targetIndex === -1) {
      throw new Error(`Invalid target role: ${targetRole}`);
    }

    // Get all users with target role
    const targetUsers = await this.prisma.user.findMany({
      where: {
        roles: {
          some: {
            role: {
              name: targetRole,
            },
          },
        },
      },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
      },
    });

    // In production, this would:
    // 1. Send notifications to target users
    // 2. Create governance tasks
    // 3. Log routing in audit trail
    
    console.log(
      `✅ Routed insight to ${targetUsers.length} ${targetRole} users`,
    );
  }

  /**
   * Escalate issue up the leadership chain
   * Issues flow upward: Youth → Captains → Ambassadors → Directors → Council → Admin
   */
  async escalateIssue(
    issue: EscalateIssueDto,
    fromRole: RoleName,
    toRole: RoleName,
  ): Promise<void> {
    const hierarchy: RoleName[] = [
      RoleName.YOUTH,
      RoleName.YOUTH_CAPTAIN,
      RoleName.AMBASSADOR,
      RoleName.REGIONAL_DIRECTOR,
      RoleName.COUNCIL,
      RoleName.ADMIN,
    ];

    const fromIndex = hierarchy.indexOf(fromRole);
    const toIndex = hierarchy.indexOf(toRole);

    // Validate escalation path (must go upward)
    if (toIndex <= fromIndex) {
      throw new Error(
        `Invalid escalation: ${fromRole} → ${toRole}. Must escalate upward.`,
      );
    }

    // Create governance decision for escalation
    const decision = await this.prisma.governanceDecision.create({
      data: {
        type: 'POLICY_CHANGE', // Or specific escalation type
        domain: 'escalation',
        title: issue.issueType,
        description: issue.description,
        reasoning: `Escalated from ${fromRole} to ${toRole} due to ${issue.priority} priority`,
        proposedBy: issue.entityId || 'system',
        status: 'PENDING',
        requiredApprovals: 1,
        approvers: [],
        entityId: issue.entityId,
        entityType: issue.entityType,
      },
    });

    // Record escalation in history
    await this.prisma.decisionHistory.create({
      data: {
        decisionId: decision.id,
        action: 'PROPOSED',
        actorId: issue.entityId || 'system',
        notes: `Escalated from ${fromRole} to ${toRole}`,
        metadata: issue as any,
      },
    });

    console.log(`🚨 Escalated issue ${decision.id} from ${fromRole} to ${toRole}`);
  }

  /**
   * Collect feedback from a leadership tier
   */
  async collectFeedback(fromRole: RoleName): Promise<any[]> {
    // Get all decisions where this role has participated
    const decisions = await this.prisma.governanceDecision.findMany({
      where: {
        proposer: {
          roles: {
            some: {
              role: {
                name: fromRole,
              },
            },
          },
        },
        status: 'IMPLEMENTED',
      },
      include: {
        proposer: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
          },
        },
        history: {
          orderBy: {
            timestamp: 'desc',
          },
          take: 1,
        },
      },
      take: 20,
      orderBy: {
        implementedAt: 'desc',
      },
    });

    return decisions.map((d) => ({
      decisionId: d.id,
      title: d.title,
      proposer: `${d.proposer.firstName} ${d.proposer.lastName}`,
      implementedAt: d.implementedAt,
      feedback: d.history[0]?.notes || 'No feedback yet',
    }));
  }

  /**
   * Track decision flow through governance layers
   */
  async trackDecisionFlow(decisionId: string): Promise<DecisionFlow> {
    const decision = await this.prisma.governanceDecision.findUnique({
      where: { id: decisionId },
      include: {
        proposer: {
          include: {
            roles: {
              include: {
                role: true,
              },
            },
          },
        },
        history: {
          orderBy: {
            timestamp: 'asc',
          },
          include: {
            actor: {
              include: {
                roles: {
                  include: {
                    role: true,
                  },
                },
              },
            },
          },
        },
      },
    });

    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    const proposedRole = decision.proposer.roles[0]?.role.name || RoleName.YOUTH;
    const approvers = (decision.approvers as any[]) || [];

    const daysInReview = Math.floor(
      (new Date().getTime() - decision.proposedAt.getTime()) /
        (1000 * 60 * 60 * 24),
    );

    return {
      decisionId: decision.id,
      proposedBy: `${decision.proposer.firstName} ${decision.proposer.lastName}`,
      proposedRole,
      currentLevel: this.getCurrentLevel(approvers),
      approvalPath: approvers.map((a: any, index: number) => ({
        order: index + 1,
        role: a.role,
        userId: a.userId,
        status: a.status,
        timestamp: a.timestamp ? new Date(a.timestamp) : undefined,
        notes: a.notes,
      })),
      status: decision.status,
      daysInReview,
    };
  }

  private getCurrentLevel(approvers: any[]): RoleName {
    if (!approvers || approvers.length === 0) return RoleName.YOUTH_CAPTAIN;

    const lastApprover = approvers[approvers.length - 1];
    return lastApprover.role || RoleName.YOUTH_CAPTAIN;
  }
}
