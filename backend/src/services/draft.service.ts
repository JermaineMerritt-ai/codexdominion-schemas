import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface DraftData {
  taskId: string;
  subject: string;
  bodyText: string;
  bodyHtml?: string;
  metadata?: Record<string, any>;
  recipientEmail: string;
  recipientType: string;
}

@Injectable()
export class DraftService {
  private readonly logger = new Logger(DraftService.name);

  constructor(private readonly prisma: PrismaService) {}

  /**
   * Create a new message draft
   */
  async createDraft(data: DraftData): Promise<any> {
    const draft = await this.prisma.messageDraft.create({
      data: {
        taskId: data.taskId,
        subject: data.subject,
        bodyText: data.bodyText,
        bodyHtml: data.bodyHtml || null,
        metadata: data.metadata || {},
        recipientEmail: data.recipientEmail,
        recipientType: data.recipientType,
        status: 'PENDING',
      },
    });

    this.logger.log(
      `Created draft ${draft.id} for task ${data.taskId} (recipient: ${data.recipientEmail})`,
    );

    return draft;
  }

  /**
   * Get draft by task ID
   */
  async getDraftByTaskId(taskId: string): Promise<any | null> {
    return this.prisma.messageDraft.findUnique({
      where: { taskId },
    });
  }

  /**
   * Get draft by ID
   */
  async getDraftById(draftId: string): Promise<any | null> {
    return this.prisma.messageDraft.findUnique({
      where: { id: draftId },
    });
  }

  /**
   * Get all pending drafts
   */
  async getPendingDrafts(): Promise<any[]> {
    return this.prisma.messageDraft.findMany({
      where: { status: 'PENDING' },
      orderBy: { createdAt: 'desc' },
    });
  }

  /**
   * Update draft status
   */
  async updateDraftStatus(
    draftId: string,
    status: 'PENDING' | 'APPROVED' | 'SENT' | 'DISCARDED',
    sentByUserId?: string,
  ): Promise<any> {
    const updateData: any = { status };

    if (status === 'SENT') {
      updateData.sentAt = new Date();
      if (sentByUserId) {
        updateData.sentByUserId = sentByUserId;
      }
    }

    const draft = await this.prisma.messageDraft.update({
      where: { id: draftId },
      data: updateData,
    });

    this.logger.log(`Updated draft ${draftId} status to ${status}`);

    return draft;
  }

  /**
   * Mark draft as sent
   */
  async markDraftSent(draftId: string, sentByUserId?: string): Promise<any> {
    return this.updateDraftStatus(draftId, 'SENT', sentByUserId);
  }

  /**
   * Discard draft
   */
  async discardDraft(draftId: string): Promise<any> {
    return this.updateDraftStatus(draftId, 'DISCARDED');
  }

  /**
   * Delete draft (hard delete)
   */
  async deleteDraft(draftId: string): Promise<void> {
    await this.prisma.messageDraft.delete({
      where: { id: draftId },
    });

    this.logger.log(`Deleted draft ${draftId}`);
  }

  /**
   * Get drafts by recipient email
   */
  async getDraftsByRecipient(recipientEmail: string): Promise<any[]> {
    return this.prisma.messageDraft.findMany({
      where: { recipientEmail },
      orderBy: { createdAt: 'desc' },
    });
  }

  /**
   * Get draft statistics
   */
  async getDraftStats(): Promise<{
    total: number;
    pending: number;
    approved: number;
    sent: number;
    discarded: number;
  }> {
    const [total, pending, approved, sent, discarded] = await Promise.all([
      this.prisma.messageDraft.count(),
      this.prisma.messageDraft.count({ where: { status: 'PENDING' } }),
      this.prisma.messageDraft.count({ where: { status: 'APPROVED' } }),
      this.prisma.messageDraft.count({ where: { status: 'SENT' } }),
      this.prisma.messageDraft.count({ where: { status: 'DISCARDED' } }),
    ]);

    return { total, pending, approved, sent, discarded };
  }
}
