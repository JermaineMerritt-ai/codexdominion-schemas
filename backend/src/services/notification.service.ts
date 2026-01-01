import { Injectable, Logger } from '@nestjs/common';

export enum NotificationType {
  DRAFT_READY = 'DRAFT_READY',
  APPROVAL_REQUIRED = 'APPROVAL_REQUIRED',
  FOLLOW_UP_SENT = 'FOLLOW_UP_SENT',
  GUARDRAIL_BLOCKED = 'GUARDRAIL_BLOCKED',
}

export interface NotificationPayload {
  type: NotificationType;
  taskId: string;
  subject: string;
  message: string;
  metadata?: Record<string, any>;
}

@Injectable()
export class NotificationService {
  private readonly logger = new Logger(NotificationService.name);

  /**
   * Notify human user (V0: console logs, V1+: real notifications)
   */
  async notify(payload: NotificationPayload): Promise<void> {
    // V0 Implementation: Console logging
    this.logger.log('='.repeat(60));
    this.logger.log(`🔔 NOTIFICATION: ${payload.type}`);
    this.logger.log(`Task ID: ${payload.taskId}`);
    this.logger.log(`Subject: ${payload.subject}`);
    this.logger.log(`Message: ${payload.message}`);
    if (payload.metadata) {
      this.logger.log(
        `Metadata: ${JSON.stringify(payload.metadata, null, 2)}`,
      );
    }
    this.logger.log('='.repeat(60));

    // TODO V1: Implement real notification channels
    // - Email notification to assigned human
    // - Push notification to mobile app
    // - Slack/Discord webhook
    // - Dashboard alert/bell icon
    // - SMS for critical notifications
  }

  /**
   * Notify that a draft is ready for review
   */
  async notifyDraftReady(
    taskId: string,
    draftId: string,
    recipientEmail: string,
    subject: string,
  ): Promise<void> {
    await this.notify({
      type: NotificationType.DRAFT_READY,
      taskId,
      subject: 'Follow-up Draft Ready',
      message: `A follow-up email draft is ready for your review.`,
      metadata: {
        draftId,
        recipientEmail,
        emailSubject: subject,
        actionRequired: 'Review and send the draft from the dashboard',
      },
    });
  }

  /**
   * Notify that approval is required for high-risk action
   */
  async notifyApprovalRequired(
    taskId: string,
    reason: string,
    metadata?: Record<string, any>,
  ): Promise<void> {
    await this.notify({
      type: NotificationType.APPROVAL_REQUIRED,
      taskId,
      subject: 'Approval Required for Follow-up',
      message: `High-risk follow-up requires your approval: ${reason}`,
      metadata: {
        ...metadata,
        actionRequired: 'Review and approve/reject from the dashboard',
      },
    });
  }

  /**
   * Notify that a follow-up email was sent automatically
   */
  async notifyFollowUpSent(
    taskId: string,
    recipientEmail: string,
    subject: string,
    mode: string,
  ): Promise<void> {
    await this.notify({
      type: NotificationType.FOLLOW_UP_SENT,
      taskId,
      subject: 'Follow-up Email Sent',
      message: `Follow-up email sent automatically (${mode} mode).`,
      metadata: {
        recipientEmail,
        emailSubject: subject,
        mode,
      },
    });
  }

  /**
   * Notify that a follow-up was blocked by guardrails
   */
  async notifyGuardrailBlocked(
    taskId: string,
    reason: string,
    metadata?: Record<string, any>,
  ): Promise<void> {
    await this.notify({
      type: NotificationType.GUARDRAIL_BLOCKED,
      taskId,
      subject: 'Follow-up Blocked by Guardrails',
      message: `Follow-up attempt blocked: ${reason}`,
      metadata: {
        ...metadata,
        actionRequired: 'Review the task and update guardrail settings if needed',
      },
    });
  }
}
