// ======================================================
// APPROVAL PROTOCOL SERVICE
// Manages approval workflows for governance decisions
// ======================================================

import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../../prisma/prisma.service';
import {
  ApprovalStatus,
  SubmitDecisionDto,
  ApproveDto,
  RejectDto,
} from '../types/governance.types';
import { DecisionType, DecisionStatus } from '@prisma/client';

@Injectable()
export class ApprovalProtocolService {
  constructor(private prisma: PrismaService) {}

  /**
   * Submit decision for approval workflow
   */
  async submitForApproval(dto: SubmitDecisionDto): Promise<string> {
    // Get approval workflow for this entity type
    const workflow = await this.prisma.approvalWorkflow.findFirst({
      where: {
        entityType: dto.entityType || dto.domain,
        isActive: true,
      },
    });

    const requiredApprovals = dto.requiredApprovals || (workflow?.steps ? (workflow.steps as any[]).filter((s: any) => s.required).length : 1);

    const decision = await this.prisma.governanceDecision.create({
      data: {
        type: dto.type as DecisionType,
        domain: dto.domain,
        title: dto.title,
        description: dto.description,
        reasoning: dto.reasoning,
        proposedBy: dto.proposedBy,
        status: DecisionStatus.PENDING,
        requiredApprovals,
        currentApprovals: 0,
        entityId: dto.entityId,
        entityType: dto.entityType,
        seasonId: dto.seasonId,
        regionId: dto.regionId,
        impactScore: dto.impactScore,
        impactDescription: dto.impactDescription,
        approvers: workflow?.steps || [],
      },
    });

    // Record in history
    await this.prisma.decisionHistory.create({
      data: {
        decisionId: decision.id,
        action: 'PROPOSED',
        actorId: dto.proposedBy,
        notes: 'Decision submitted for approval',
      },
    });

    console.log(`📋 Decision ${decision.id} submitted for approval (requires ${requiredApprovals} approvals)`);
    return decision.id;
  }

  /**
   * Approve a pending decision
   */
  async approveDecision(
    decisionId: string,
    dto: ApproveDto,
  ): Promise<void> {
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
      },
    });

    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    if (decision.status !== DecisionStatus.PENDING && decision.status !== DecisionStatus.UNDER_REVIEW) {
      throw new Error(
        `Decision ${decisionId} is ${decision.status} and cannot be approved`,
      );
    }

    // Get approver's role
    const approver = await this.prisma.user.findUnique({
      where: { id: dto.approverId },
      include: {
        roles: {
          include: {
            role: true,
          },
        },
      },
    });

    if (!approver) {
      throw new Error(`Approver ${dto.approverId} not found`);
    }

    const approverRole = approver.roles[0]?.role.name;

    // Update approvers list
    const approvers = (decision.approvers as any[]) || [];
    approvers.push({
      userId: dto.approverId,
      role: approverRole,
      status: 'approved',
      timestamp: new Date().toISOString(),
      notes: dto.notes,
    });

    const currentApprovals = decision.currentApprovals + 1;
    const isApproved = currentApprovals >= decision.requiredApprovals;

    // Update decision
    await this.prisma.governanceDecision.update({
      where: { id: decisionId },
      data: {
        approvers: approvers as any,
        currentApprovals,
        status: isApproved ? DecisionStatus.APPROVED : DecisionStatus.UNDER_REVIEW,
        approvedAt: isApproved ? new Date() : undefined,
        approvedBy: isApproved ? dto.approverId : undefined,
      },
    });

    // Record in history
    await this.prisma.decisionHistory.create({
      data: {
        decisionId,
        action: 'APPROVED',
        actorId: dto.approverId,
        notes: dto.notes || `Approved by ${approverRole}`,
      },
    });

    console.log(
      `✅ Decision ${decisionId} approved by ${approverRole} (${currentApprovals}/${decision.requiredApprovals})`,
    );
  }

  /**
   * Reject a pending decision
   */
  async rejectDecision(
    decisionId: string,
    dto: RejectDto,
  ): Promise<void> {
    const decision = await this.prisma.governanceDecision.findUnique({
      where: { id: decisionId },
    });

    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    if (decision.status !== DecisionStatus.PENDING && decision.status !== DecisionStatus.UNDER_REVIEW) {
      throw new Error(
        `Decision ${decisionId} is ${decision.status} and cannot be rejected`,
      );
    }

    await this.prisma.governanceDecision.update({
      where: { id: decisionId },
      data: {
        status: DecisionStatus.REJECTED,
        rejectedAt: new Date(),
        rejectedBy: dto.approverId,
      },
    });

    await this.prisma.decisionHistory.create({
      data: {
        decisionId,
        action: 'REJECTED',
        actorId: dto.approverId,
        notes: dto.reason,
      },
    });

    console.log(`❌ Decision ${decisionId} rejected: ${dto.reason}`);
  }

  /**
   * Get approval status for decision
   */
  async getApprovalStatus(decisionId: string): Promise<ApprovalStatus> {
    const decision = await this.prisma.governanceDecision.findUnique({
      where: { id: decisionId },
    });

    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    const approvers = (decision.approvers as any[]) || [];
    const canImplement =
      decision.status === DecisionStatus.APPROVED &&
      decision.currentApprovals >= decision.requiredApprovals;

    return {
      decisionId: decision.id,
      status: decision.status,
      currentApprovals: decision.currentApprovals,
      requiredApprovals: decision.requiredApprovals,
      approvers: approvers.map((a: any, index: number) => ({
        order: index + 1,
        role: a.role,
        userId: a.userId,
        status: a.status,
        timestamp: a.timestamp ? new Date(a.timestamp) : undefined,
        notes: a.notes,
      })),
      canImplement,
      nextApprover: this.getNextApprover(approvers, decision.requiredApprovals),
    };
  }

  /**
   * Mark decision as implemented
   */
  async implementDecision(decisionId: string): Promise<void> {
    const decision = await this.prisma.governanceDecision.findUnique({
      where: { id: decisionId },
    });

    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    if (decision.status !== DecisionStatus.APPROVED) {
      throw new Error(
        `Decision ${decisionId} is ${decision.status} and cannot be implemented`,
      );
    }

    await this.prisma.governanceDecision.update({
      where: { id: decisionId },
      data: {
        status: DecisionStatus.IMPLEMENTED,
        implementedAt: new Date(),
      },
    });

    await this.prisma.decisionHistory.create({
      data: {
        decisionId,
        action: 'IMPLEMENTED',
        actorId: decision.approvedBy || decision.proposedBy,
        notes: 'Decision successfully implemented',
      },
    });

    console.log(`🎯 Decision ${decisionId} marked as implemented`);
  }

  private getNextApprover(approvers: any[], required: number): any {
    if (approvers.length >= required) return undefined;
    
    // In production, this would look up the workflow and determine next approver role
    return undefined;
  }
}
