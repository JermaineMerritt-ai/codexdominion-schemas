import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { TasksService } from '../tasks/tasks.service';
import { CreateTaskDto } from '../tasks/dto/create-task.dto';
import { TaskMode, TaskPriority, OwnerType, SubjectRefType, TaskType } from '../tasks/dto';

/**
 * Stale Lead Detector
 * 
 * Runs on a schedule to identify leads that haven't been contacted recently
 * and need follow-up. Creates LEAD_FOLLOW_UP tasks in the Task Engine.
 * 
 * V0 Implementation:
 * - Uses mock lead data (in production, would query actual CRM system)
 * - Runs every 6 hours
 * - Checks for open leads with no recent contact
 * - Respects follow-up window (don't create duplicate tasks within 24 hours)
 */
@Injectable()
export class StaleLeadDetectorService {
  private readonly logger = new Logger(StaleLeadDetectorService.name);

  // Configuration (in production, load from environment/config service)
  private readonly STALE_THRESHOLD_DAYS = 7; // Lead is stale after 7 days of no contact

  constructor(private readonly tasksService: TasksService) {}

  /**
   * Main detection cron job - runs every 6 hours
   * In production, configure schedule via environment variable
   */
  @Cron(CronExpression.EVERY_6_HOURS)
  async detectStaleLeads() {
    this.logger.log('Running stale lead detection...');

    try {
      // V0: Mock lead data
      // In production, this would query your CRM database/API
      const staleLeads = await this.fetchStaleLeads();

      this.logger.log(`Found ${staleLeads.length} stale leads`);

      let created = 0;
      let skipped = 0;

      for (const lead of staleLeads) {
        try {
          // Create follow-up task via Task Engine
          const taskDto: CreateTaskDto = {
            type: TaskType.LEAD_FOLLOW_UP,
            mode: this.determineMode(lead),
            priority: this.determinePriority(lead),
            ownerType: OwnerType.AI,
            ownerId: 'STALE_LEAD_DETECTOR',
            subjectRefType: SubjectRefType.LEAD,
            subjectRefId: lead.leadId,
            source: 'STALE_LEAD_DETECTOR',
            payload: {
              lead_name: lead.name,
              lead_email: lead.email,
              lead_phone: lead.phone,
              company: lead.company,
              lead_source: lead.source,
              lead_stage: lead.stage,
              last_contact_at: lead.lastContactAt,
              days_since_contact: lead.daysSinceContact,
              estimated_value: lead.estimatedValue,
              notes: lead.notes,
            },
          };

          await this.tasksService.create(taskDto);
          created++;
          this.logger.log(
            `Created LEAD_FOLLOW_UP task for lead ${lead.name}`,
          );
        } catch (error) {
          // Task Engine returns 400 if duplicate (idempotency)
          if (error.status === 400) {
            skipped++;
            this.logger.debug(
              `Skipped duplicate task for lead ${lead.name}`,
            );
          } else {
            this.logger.error(
              `Failed to create task for lead ${lead.name}:`,
              error.message,
            );
          }
        }
      }

      this.logger.log(
        `Lead detection complete: ${created} created, ${skipped} skipped`,
      );
    } catch (error) {
      this.logger.error('Lead detection failed:', error.message);
    }
  }

  /**
   * Fetch stale leads from CRM system
   * V0: Returns mock data
   * Production: Query actual CRM database/API
   */
  private async fetchStaleLeads() {
    // V0 MOCK DATA
    // In production, replace with:
    // return this.crmService.findMany({
    //   where: {
    //     status: 'OPEN',
    //     lastContactAt: { lt: subDays(new Date(), this.STALE_THRESHOLD_DAYS) }
    //   }
    // });

    const now = new Date();
    const staleThreshold = new Date(
      now.getTime() - this.STALE_THRESHOLD_DAYS * 24 * 60 * 60 * 1000,
    );

    const mockLeads = [
      {
        leadId: 'LEAD-001',
        name: 'John Smith',
        email: 'john.smith@techstartup.com',
        phone: '+1-555-0123',
        company: 'Tech Startup Inc',
        source: 'Website Form',
        stage: 'QUALIFIED',
        lastContactAt: new Date('2025-12-20').toISOString(),
        daysSinceContact: Math.floor(
          (now.getTime() - new Date('2025-12-20').getTime()) /
            (1000 * 60 * 60 * 24),
        ),
        estimatedValue: 25000,
        notes: 'Interested in enterprise plan, waiting for budget approval',
        status: 'OPEN',
      },
      {
        leadId: 'LEAD-002',
        name: 'Sarah Johnson',
        email: 'sarah.j@consulting.com',
        phone: '+1-555-0456',
        company: 'Consulting Pros LLC',
        source: 'Referral',
        stage: 'CONTACTED',
        lastContactAt: new Date('2025-12-15').toISOString(),
        daysSinceContact: Math.floor(
          (now.getTime() - new Date('2025-12-15').getTime()) /
            (1000 * 60 * 60 * 24),
        ),
        estimatedValue: 15000,
        notes: 'Initial discovery call completed, needs follow-up demo',
        status: 'OPEN',
      },
      {
        leadId: 'LEAD-003',
        name: 'Michael Chen',
        email: 'm.chen@ecommerce.com',
        phone: '+1-555-0789',
        company: 'E-Commerce Solutions',
        source: 'LinkedIn',
        stage: 'PROPOSAL_SENT',
        lastContactAt: new Date('2025-12-18').toISOString(),
        daysSinceContact: Math.floor(
          (now.getTime() - new Date('2025-12-18').getTime()) /
            (1000 * 60 * 60 * 24),
        ),
        estimatedValue: 40000,
        notes: 'Proposal sent, awaiting response from decision maker',
        status: 'OPEN',
      },
    ];

    // Filter to only truly stale leads
    return mockLeads.filter(
      (lead) =>
        new Date(lead.lastContactAt) < staleThreshold && lead.status === 'OPEN',
    );
  }

  /**
   * Determine execution mode based on lead characteristics
   * V0 logic: High-value leads → SUGGESTION, else ASSISTED
   */
  private determineMode(lead: any): TaskMode {
    // High-value leads (>$30k) require human review
    if (lead.estimatedValue > 30000) {
      return TaskMode.SUGGESTION;
    }

    // Proposal stage requires human touch
    if (lead.stage === 'PROPOSAL_SENT') {
      return TaskMode.SUGGESTION;
    }

    // Standard leads use assisted mode (auto-send unless high-risk)
    return TaskMode.ASSISTED;
  }

  /**
   * Determine task priority based on lead characteristics
   */
  private determinePriority(
    lead: any,
  ): TaskPriority {
    if (lead.estimatedValue > 50000 || lead.daysSinceContact > 21) {
      return TaskPriority.CRITICAL;
    }
    if (lead.estimatedValue > 20000 || lead.daysSinceContact > 14) {
      return TaskPriority.HIGH;
    }
    if (lead.daysSinceContact > 10) {
      return TaskPriority.MEDIUM;
    }
    return TaskPriority.LOW;
  }
}
