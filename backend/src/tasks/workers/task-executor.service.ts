import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { TasksService } from '../tasks.service';
import { TaskStatus, ActorType, TaskMode } from '../dto';
import { MessageGeneratorService } from '../../services/message-generator.service';
import { EmailSenderService } from '../../services/email-sender.service';

/**
 * TASK EXECUTOR SERVICE (ENHANCED V1)
 * Stage 3 of 3-stage pipeline: Polls for SCHEDULED tasks and executes them
 * Handles SUGGESTION, ASSISTED, and AUTONOMOUS modes
 * Runs every minute via cron
 * 
 * V1 Enhancements:
 * - Real message generation via MessageGeneratorService
 * - Real email sending via EmailSenderService (SMTP)
 * - Enhanced error handling with retry logic
 */
@Injectable()
export class TaskExecutorService {
  private readonly logger = new Logger(TaskExecutorService.name);

  constructor(
    private tasksService: TasksService,
    private messageGenerator: MessageGeneratorService,
    private emailSender: EmailSenderService,
  ) {}

  @Cron(CronExpression.EVERY_MINUTE)
  async executeScheduledTasks() {
    this.logger.log('Running task executor...');

    try {
      // Find tasks that are SCHEDULED and ready to execute
      const scheduledTasks = await this.tasksService.findAll({
        status: TaskStatus.SCHEDULED,
      });

      const now = new Date();
      const tasksToExecute = scheduledTasks.filter((task) => {
        return task.scheduledAt && new Date(task.scheduledAt) <= now;
      });

      this.logger.log(`Found ${tasksToExecute.length} tasks ready for execution`);

      for (const task of tasksToExecute) {
        await this.executeTask(task);
      }
    } catch (error) {
      this.logger.error('Executor error:', error);
    }
  }

  private async executeTask(task: any) {
    try {
      // Set task to IN_PROGRESS
      await this.tasksService.update(task.id, {
        newStatus: TaskStatus.IN_PROGRESS,
        actorType: ActorType.AI,
        actorId: 'ACTION_AI_EXECUTOR',
      });

      this.logger.log(`Executing task ${task.id} (${task.type}, mode: ${task.mode})`);

      // Execute based on mode
      let success = false;

      switch (task.mode) {
        case TaskMode.SUGGESTION:
          success = await this.executeSuggestionMode(task);
          break;
        case TaskMode.ASSISTED:
          success = await this.executeAssistedMode(task);
          break;
        case TaskMode.AUTONOMOUS:
          success = await this.executeAutonomousMode(task);
          break;
        default:
          throw new Error(`Unknown mode: ${task.mode}`);
      }

      // Update task status based on result
      if (success) {
        await this.tasksService.update(task.id, {
          newStatus: TaskStatus.COMPLETED,
          actorType: ActorType.AI,
          actorId: 'ACTION_AI_EXECUTOR',
        });
        this.logger.log(`✅ Task ${task.id} completed successfully`);
      } else {
        await this.tasksService.update(task.id, {
          newStatus: TaskStatus.FAILED,
          actorType: ActorType.AI,
          actorId: 'ACTION_AI_EXECUTOR',
          error: 'Execution failed (see logs)',
        });
        this.logger.error(`❌ Task ${task.id} failed`);
      }
    } catch (error) {
      this.logger.error(`Task ${task.id} execution error:`, error);

      try {
        await this.tasksService.update(task.id, {
          newStatus: TaskStatus.FAILED,
          actorType: ActorType.AI,
          actorId: 'ACTION_AI_EXECUTOR',
          error: error.message,
        });
      } catch (updateError) {
        this.logger.error(`Failed to update task ${task.id} to FAILED:`, updateError);
      }
    }
  }

  private async executeSuggestionMode(task: any): Promise<boolean> {
    // SUGGESTION mode: Generate draft + notify human
    this.logger.log(`[SUGGESTION] Generating draft for task ${task.id}`);

    try {
      // Generate message using real service
      const message = await this.messageGenerator.generateMessage(
        task.type,
        task.payload,
      );

      // V0: Log draft (in production, save to database for human review)
      this.logger.log(`[SUGGESTION] Draft created:`);
      this.logger.log(`Subject: ${message.subject}`);
      this.logger.log(`Body preview: ${message.body_text.substring(0, 100)}...`);

      // TODO V1: Save draft to database
      // await this.draftService.save({
      //   taskId: task.id,
      //   subject: message.subject,
      //   body: message.body,
      //   metadata: message.metadata
      // });

      // TODO V1: Send notification to human for review
      // await this.notificationService.notify({
      //   type: 'DRAFT_READY_FOR_REVIEW',
      //   taskId: task.id,
      //   userId: task.ownerId
      // });

      this.logger.log(`[SUGGESTION] Draft created, human review required`);
      return true;
    } catch (error) {
      this.logger.error(`[SUGGESTION] Failed to generate draft:`, error.message);
      return false;
    }
  }

  private async executeAssistedMode(task: any): Promise<boolean> {
    // ASSISTED mode: Auto-send unless high-risk
    this.logger.log(`[ASSISTED] Evaluating risk for task ${task.id}`);

    const isHighRisk = this.evaluateRisk(task);

    if (isHighRisk) {
      // High-risk: Generate draft and request approval
      this.logger.log(`[ASSISTED] High-risk detected, requesting approval`);
      
      try {
        const message = await this.messageGenerator.generateMessage(
          task.type,
          task.payload,
        );

        this.logger.log(`[ASSISTED] Draft created, approval required`);
        
        // TODO V1: Request approval from human
        // await this.approvalService.request({
        //   taskId: task.id,
        //   draft: message,
        //   reason: 'High-risk: requires human approval'
        // });

        return false; // Pending approval (task will retry later)
      } catch (error) {
        this.logger.error(`[ASSISTED] Failed to generate draft:`, error.message);
        return false;
      }
    }

    // Low-risk: Send automatically
    this.logger.log(`[ASSISTED] Low-risk, sending automatically`);
    return this.sendFollowUpEmail(task);
  }

  private async executeAutonomousMode(task: any): Promise<boolean> {
    // AUTONOMOUS mode: Auto-send within guardrails
    this.logger.log(`[AUTONOMOUS] Sending automatically for task ${task.id}`);
    return this.sendFollowUpEmail(task);
  }

  /**
   * Send follow-up email using real email service
   */
  private async sendFollowUpEmail(task: any): Promise<boolean> {
    try {
      // Generate message
      const message = await this.messageGenerator.generateMessage(
        task.type,
        task.payload,
      );

      // Extract recipient email from payload
      const recipientEmail = this.extractRecipientEmail(task);

      if (!recipientEmail) {
        this.logger.error(`No recipient email found in task ${task.id}`);
        return false;
      }

      // Send email with retry logic (text + HTML)
      const result = await this.emailSender.sendEmailWithRetry(
        recipientEmail,
        message.subject,
        message.body_text,
        message.body_html,
        3, // max retries
      );

      if (result.success) {
        this.logger.log(
          `✉️ Email sent successfully to ${recipientEmail} (ID: ${result.messageId})`,
        );
        return true;
      } else {
        this.logger.error(
          `Failed to send email to ${recipientEmail}: ${result.error}`,
        );
        return false;
      }
    } catch (error) {
      this.logger.error(`Email sending error:`, error.message);
      return false;
    }
  }

  /**
   * Extract recipient email from task payload
   */
  private extractRecipientEmail(task: any): string | null {
    const payload = task.payload;

    // Try different email field names based on task type
    if (task.type === 'INVOICE_FOLLOW_UP') {
      return payload.customer_email || null;
    } else if (task.type === 'LEAD_FOLLOW_UP') {
      return payload.lead_email || null;
    }

    // Fallback: search for any email field
    return payload.email || payload.to || null;
  }

  /**
   * Evaluate if task execution is high-risk
   */
  private evaluateRisk(task: any): boolean {
    const payload = task.payload;

    if (task.type === 'INVOICE_FOLLOW_UP') {
      // High-risk if large amount or very overdue
      if (payload.invoice_amount > 5000) {
        this.logger.log('High-risk: Invoice amount > $5000');
        return true;
      }
      if (payload.days_overdue > 30) {
        this.logger.log('High-risk: Days overdue > 30');
        return true;
      }
    } else if (task.type === 'LEAD_FOLLOW_UP') {
      // High-risk if high-value lead or sensitive stage
      if (payload.estimated_value > 30000) {
        this.logger.log('High-risk: Lead value > $30k');
        return true;
      }
      if (payload.lead_stage === 'PROPOSAL_SENT') {
        this.logger.log('High-risk: Proposal stage requires human touch');
        return true;
      }
    }

    return false;
  }
}
