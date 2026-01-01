import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

interface GuardrailConfig {
  maxFollowUps: number;
  minSpacingDays: number;
}

interface GuardrailResult {
  allowed: boolean;
  reason?: string;
  metadata?: {
    followUpCount?: number;
    lastFollowUpAt?: Date;
    daysSinceLastFollowUp?: number;
  };
}

@Injectable()
export class GuardrailsService {
  private readonly logger = new Logger(GuardrailsService.name);

  // Guardrail configurations per subject type
  private readonly configs: Record<string, GuardrailConfig> = {
    INVOICE: {
      maxFollowUps: 3,
      minSpacingDays: 3,
    },
    LEAD: {
      maxFollowUps: 5,
      minSpacingDays: 2,
    },
  };

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Check if follow-up is allowed based on guardrails
   */
  async checkFollowUpAllowed(
    subjectRefType: string,
    subjectRefId: string,
    payload: any,
  ): Promise<GuardrailResult> {
    const config = this.configs[subjectRefType];
    if (!config) {
      return {
        allowed: false,
        reason: `Unknown subject type: ${subjectRefType}`,
      };
    }

    // Check 1: Max follow-ups limit
    const followUpCount = await this.getFollowUpCount(
      subjectRefType,
      subjectRefId,
    );
    if (followUpCount >= config.maxFollowUps) {
      this.logger.warn(
        `Max follow-ups reached for ${subjectRefType} ${subjectRefId}: ${followUpCount}/${config.maxFollowUps}`,
      );
      return {
        allowed: false,
        reason: `Max follow-ups (${config.maxFollowUps}) reached`,
        metadata: { followUpCount },
      };
    }

    // Check 2: Min spacing between follow-ups
    const lastFollowUp = await this.getLastFollowUpDate(
      subjectRefType,
      subjectRefId,
    );
    if (lastFollowUp) {
      const daysSince = this.getDaysBetween(lastFollowUp, new Date());
      if (daysSince < config.minSpacingDays) {
        this.logger.warn(
          `Minimum spacing not met for ${subjectRefType} ${subjectRefId}: ${daysSince} days < ${config.minSpacingDays} days`,
        );
        return {
          allowed: false,
          reason: `Minimum spacing (${config.minSpacingDays} days) not met`,
          metadata: { lastFollowUpAt: lastFollowUp, daysSinceLastFollowUp: daysSince },
        };
      }
    }

    // Check 3: Subject-specific flags
    if (subjectRefType === 'INVOICE') {
      // Check invoice-specific conditions
      const invoiceCheck = this.checkInvoiceGuardrails(payload);
      if (!invoiceCheck.allowed) {
        return invoiceCheck;
      }
    }

    if (subjectRefType === 'LEAD') {
      // Check lead-specific conditions
      const leadCheck = this.checkLeadGuardrails(payload);
      if (!leadCheck.allowed) {
        return leadCheck;
      }
    }

    // All checks passed
    return {
      allowed: true,
      metadata: { followUpCount, lastFollowUpAt: lastFollowUp || undefined },
    };
  }

  /**
   * Check invoice-specific guardrails
   */
  private checkInvoiceGuardrails(payload: any): GuardrailResult {
    // Check if invoice status changed from UNPAID
    if (payload.invoice_status && payload.invoice_status !== 'UNPAID') {
      return {
        allowed: false,
        reason: `Invoice status is no longer UNPAID: ${payload.invoice_status}`,
      };
    }

    // Check "do not contact" flag
    if (payload.do_not_contact === true) {
      return {
        allowed: false,
        reason: 'Customer marked as "do not contact"',
      };
    }

    return { allowed: true };
  }

  /**
   * Check lead-specific guardrails
   */
  private checkLeadGuardrails(payload: any): GuardrailResult {
    // Check if lead is closed or unqualified
    const disallowedStatuses = ['CLOSED', 'UNQUALIFIED'];
    if (payload.lead_stage && disallowedStatuses.includes(payload.lead_stage)) {
      return {
        allowed: false,
        reason: `Lead status is ${payload.lead_stage}`,
      };
    }

    // Check if lead unsubscribed
    if (payload.unsubscribed === true) {
      return {
        allowed: false,
        reason: 'Lead has unsubscribed',
      };
    }

    return { allowed: true };
  }

  /**
   * Get total follow-up count for a subject
   */
  private async getFollowUpCount(
    subjectRefType: string,
    subjectRefId: string,
  ): Promise<number> {
    const count = await this.prisma.followUpHistory.count({
      where: {
        subjectRefType,
        subjectRefId,
      },
    });
    return count;
  }

  /**
   * Get last follow-up date for a subject
   */
  private async getLastFollowUpDate(
    subjectRefType: string,
    subjectRefId: string,
  ): Promise<Date | null> {
    const lastFollowUp = await this.prisma.followUpHistory.findFirst({
      where: {
        subjectRefType,
        subjectRefId,
      },
      orderBy: {
        attemptedAt: 'desc',
      },
      select: {
        attemptedAt: true,
      },
    });

    return lastFollowUp ? lastFollowUp.attemptedAt : null;
  }

  /**
   * Record a follow-up attempt in history
   */
  async recordFollowUpAttempt(
    subjectRefType: string,
    subjectRefId: string,
    taskId: string,
    emailSent: boolean,
  ): Promise<void> {
    const followUpCount = await this.getFollowUpCount(
      subjectRefType,
      subjectRefId,
    );

    await this.prisma.followUpHistory.create({
      data: {
        subjectRefType,
        subjectRefId,
        taskId,
        attemptNumber: followUpCount + 1,
        emailSent,
        emailSentAt: emailSent ? new Date() : null,
      },
    });

    this.logger.log(
      `Recorded follow-up attempt #${followUpCount + 1} for ${subjectRefType} ${subjectRefId} (emailSent: ${emailSent})`,
    );
  }

  /**
   * Calculate days between two dates
   */
  private getDaysBetween(date1: Date, date2: Date): number {
    const msPerDay = 1000 * 60 * 60 * 24;
    const diff = Math.abs(date2.getTime() - date1.getTime());
    return Math.floor(diff / msPerDay);
  }
}
