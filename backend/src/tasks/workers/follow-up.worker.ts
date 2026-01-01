import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { TasksService } from '../tasks.service';
import { Task } from '@prisma/client';

// TODO: Replace with actual email service
interface EmailService {
  sendEmail(options: {
    to: string;
    subject: string;
    textBody: string;
    htmlBody?: string;
  }): Promise<void>;
}

@Injectable()
export class FollowUpWorker {
  constructor(
    private readonly prisma: PrismaService,
    private readonly tasksService: TasksService,
    // private readonly emailService: EmailService, // TODO: inject actual email service
  ) {}

  // Run on interval (e.g. cron or Bull queue)
  async processScheduledTasks() {
    const tasks = await this.prisma.task.findMany({
      where: {
        status: 'SCHEDULED',
        type: { in: ['INVOICE_FOLLOW_UP', 'LEAD_FOLLOW_UP'] },
        scheduledAt: { lte: new Date() },
      },
      take: 50,
    });

    for (const task of tasks) {
      await this.handleTask(task);
    }
  }

  private async handleTask(task: Task) {
    // 1. Move to IN_PROGRESS
    await this.tasksService.updateTaskStatus(task.id, {
      newStatus: 'IN_PROGRESS',
      actorType: 'SYSTEM',
      actorId: 'FOLLOW_UP_WORKER',
    });

    try {
      // 2. Guardrails check (rate limit, status, etc.)
      const allowed = await this.checkGuardrails(task);
      if (!allowed) {
        await this.tasksService.updateTaskStatus(task.id, {
          newStatus: 'CANCELLED',
          actorType: 'SYSTEM',
          actorId: 'FOLLOW_UP_WORKER',
          error: 'Guardrails prevented execution',
        });
        return;
      }

      // 3. Generate message
      const { subject, bodyText, bodyHtml } = await this.generateMessage(task);

      // 4. Apply mode behavior
      if (task.mode === 'SUGGESTION') {
        await this.saveDraft(task, subject, bodyText, bodyHtml);
      } else {
        // TODO: Uncomment when emailService is injected
        // await this.emailService.sendEmail({
        //   to: this.getRecipientEmail(task),
        //   subject,
        //   textBody: bodyText,
        //   htmlBody: bodyHtml,
        // });
        console.log(`[FollowUpWorker] Would send email to ${this.getRecipientEmail(task)}`);
      }

      // 5. Mark completed
      await this.tasksService.updateTaskStatus(task.id, {
        newStatus: 'COMPLETED',
        actorType: 'AI',
        actorId: 'FOLLOW_UP_WORKER',
      });
    } catch (e: any) {
      await this.tasksService.updateTaskStatus(task.id, {
        newStatus: 'FAILED',
        actorType: 'AI',
        actorId: 'FOLLOW_UP_WORKER',
        error: e?.message ?? 'Unknown error',
      });
    }
  }

  private async checkGuardrails(task: Task): Promise<boolean> {
    // TODO: implement rate limits, max follow-ups, etc.
    return true;
  }

  private async generateMessage(task: Task): Promise<{
    subject: string;
    bodyText: string;
    bodyHtml?: string;
  }> {
    if (task.type === 'INVOICE_FOLLOW_UP') {
      const p = task.payload as any;
      const subject = `Following up on invoice ${p.invoice_number}`;
      const bodyText = `Hi ${p.customer_name}, ...`; // plug Action AI generation here
      return { subject, bodyText };
    }

    if (task.type === 'LEAD_FOLLOW_UP') {
      const p = task.payload as any;
      const subject = `Quick check-in`;
      const bodyText = `Hi ${p.lead_name}, ...`;
      return { subject, bodyText };
    }

    throw new Error('Unsupported task type');
  }

  private getRecipientEmail(task: Task): string {
    const p = task.payload as any;
    return p.customer_email || p.lead_email;
  }

  private async saveDraft(
    task: Task,
    subject: string,
    bodyText: string,
    bodyHtml?: string,
  ) {
    // Could be a message_drafts table or attachment to task.payload
    await this.prisma.task.update({
      where: { id: task.id },
      data: {
        payload: {
          ...task.payload,
          draft: { subject, bodyText, bodyHtml },
        },
      },
    });
  }
}
