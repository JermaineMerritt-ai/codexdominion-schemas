import { Module } from '@nestjs/common';
import { TasksModule } from '../tasks/tasks.module';
import { OverdueInvoiceDetectorService } from './overdue-invoice-detector.service';
import { StaleLeadDetectorService } from './stale-lead-detector.service';

/**
 * Detectors Module
 * 
 * Contains detector services that identify follow-up opportunities
 * and create tasks in the Task Engine.
 * 
 * V0 Detectors:
 * - OverdueInvoiceDetectorService: Detects unpaid invoices past due date
 * - StaleLeadDetectorService: Detects leads with no recent contact
 * 
 * Future detectors:
 * - AbandonedCartDetector
 * - SubscriptionRenewalDetector
 * - CustomerChurnRiskDetector
 * - etc.
 */
@Module({
  imports: [TasksModule], // Import TasksModule to access TasksService
  providers: [OverdueInvoiceDetectorService, StaleLeadDetectorService],
  exports: [OverdueInvoiceDetectorService, StaleLeadDetectorService],
})
export class DetectorsModule {}
