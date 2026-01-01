import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { TasksService } from '../tasks/tasks.service';
import { CreateTaskDto } from '../tasks/dto/create-task.dto';
import { TaskMode, TaskPriority, OwnerType, SubjectRefType, TaskType } from '../tasks/dto';

/**
 * Overdue Invoice Detector
 * 
 * Runs on a schedule to identify invoices that are past due and need follow-up.
 * Creates INVOICE_FOLLOW_UP tasks in the Task Engine.
 * 
 * V0 Implementation:
 * - Uses mock invoice data (in production, would query actual invoice system)
 * - Runs every hour
 * - Checks for unpaid invoices past due date
 * - Respects follow-up window (don't create duplicate tasks within 24 hours)
 */
@Injectable()
export class OverdueInvoiceDetectorService {
  private readonly logger = new Logger(OverdueInvoiceDetectorService.name);

  constructor(private readonly tasksService: TasksService) {}

  /**
   * Main detection cron job - runs every hour
   * In production, configure schedule via environment variable
   */
  @Cron(CronExpression.EVERY_HOUR)
  async detectOverdueInvoices() {
    this.logger.log('Running overdue invoice detection...');

    try {
      // V0: Mock invoice data
      // In production, this would query your invoice database/API
      const overdueInvoices = await this.fetchOverdueInvoices();

      this.logger.log(`Found ${overdueInvoices.length} overdue invoices`);

      let created = 0;
      let skipped = 0;

      for (const invoice of overdueInvoices) {
        try {
          // Create follow-up task via Task Engine
          const taskDto: CreateTaskDto = {
            type: TaskType.INVOICE_FOLLOW_UP,
            mode: this.determineMode(invoice),
            priority: this.determinePriority(invoice),
            ownerType: OwnerType.AI,
            ownerId: 'OVERDUE_INVOICE_DETECTOR',
            subjectRefType: SubjectRefType.INVOICE,
            subjectRefId: invoice.invoiceId,
            source: 'OVERDUE_INVOICE_DETECTOR',
            payload: {
              customer_name: invoice.customerName,
              customer_email: invoice.customerEmail,
              invoice_number: invoice.invoiceNumber,
              invoice_amount: invoice.amount,
              currency: invoice.currency,
              due_date: invoice.dueDate,
              days_overdue: invoice.daysOverdue,
              invoice_url: invoice.invoiceUrl,
            },
          };

          await this.tasksService.create(taskDto);
          created++;
          this.logger.log(
            `Created INVOICE_FOLLOW_UP task for invoice ${invoice.invoiceNumber}`,
          );
        } catch (error) {
          // Task Engine returns 400 if duplicate (idempotency)
          if (error.status === 400) {
            skipped++;
            this.logger.debug(
              `Skipped duplicate task for invoice ${invoice.invoiceNumber}`,
            );
          } else {
            this.logger.error(
              `Failed to create task for invoice ${invoice.invoiceNumber}:`,
              error.message,
            );
          }
        }
      }

      this.logger.log(
        `Invoice detection complete: ${created} created, ${skipped} skipped`,
      );
    } catch (error) {
      this.logger.error('Invoice detection failed:', error.message);
    }
  }

  /**
   * Fetch overdue invoices from invoice system
   * V0: Returns mock data
   * Production: Query actual invoice database/API
   */
  private async fetchOverdueInvoices() {
    // V0 MOCK DATA
    // In production, replace with:
    // return this.invoiceService.findMany({
    //   where: {
    //     status: 'UNPAID',
    //     dueDate: { lt: new Date() },
    //     OR: [
    //       { lastFollowUpAt: null },
    //       { lastFollowUpAt: { lt: subDays(new Date(), 1) } }
    //     ]
    //   }
    // });

    const now = new Date();
    const mockInvoices = [
      {
        invoiceId: 'INV-001',
        invoiceNumber: 'INV-2026-001',
        customerName: 'Acme Corp',
        customerEmail: 'accounts@acme.com',
        amount: 5000.0,
        currency: 'USD',
        dueDate: new Date('2025-12-15').toISOString(),
        daysOverdue: Math.floor(
          (now.getTime() - new Date('2025-12-15').getTime()) /
            (1000 * 60 * 60 * 24),
        ),
        invoiceUrl: 'https://example.com/invoices/INV-001',
        status: 'UNPAID',
        lastFollowUpAt: null,
      },
      {
        invoiceId: 'INV-002',
        invoiceNumber: 'INV-2025-098',
        customerName: 'Global Industries',
        customerEmail: 'billing@globalind.com',
        amount: 12500.0,
        currency: 'USD',
        dueDate: new Date('2025-12-20').toISOString(),
        daysOverdue: Math.floor(
          (now.getTime() - new Date('2025-12-20').getTime()) /
            (1000 * 60 * 60 * 24),
        ),
        invoiceUrl: 'https://example.com/invoices/INV-002',
        status: 'UNPAID',
        lastFollowUpAt: null,
      },
    ];

    // Filter to only truly overdue invoices
    return mockInvoices.filter((inv) => inv.daysOverdue > 0);
  }

  /**
   * Determine execution mode based on invoice characteristics
   * V0 logic: High-value or very overdue → SUGGESTION, else ASSISTED
   */
  private determineMode(invoice: any): TaskMode {
    // High-value invoices (>$10k) require human review
    if (invoice.amount > 10000) {
      return TaskMode.SUGGESTION;
    }

    // Very overdue (>45 days) requires human review
    if (invoice.daysOverdue > 45) {
      return TaskMode.SUGGESTION;
    }

    // Standard invoices use assisted mode (auto-send unless high-risk)
    return TaskMode.ASSISTED;
  }

  /**
   * Determine task priority based on invoice characteristics
   */
  private determinePriority(
    invoice: any,
  ): TaskPriority {
    if (invoice.amount > 50000 || invoice.daysOverdue > 60) {
      return TaskPriority.CRITICAL;
    }
    if (invoice.amount > 10000 || invoice.daysOverdue > 30) {
      return TaskPriority.HIGH;
    }
    if (invoice.daysOverdue > 14) {
      return TaskPriority.MEDIUM;
    }
    return TaskPriority.LOW;
  }
}
