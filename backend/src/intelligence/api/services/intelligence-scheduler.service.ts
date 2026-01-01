/**
 * Intelligence Scheduler Service
 * 
 * Automated batch job scheduler for Intelligence API V1
 * 
 * Runs insight generation on configurable schedules:
 * - Daily at 6:00 AM (primary job)
 * - Hourly during business hours (optional)
 * - On-demand via API endpoint
 * 
 * Uses @nestjs/schedule for cron jobs
 */

import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { IntelligenceApiService } from './intelligence-api.service';

@Injectable()
export class IntelligenceSchedulerService {
  private readonly logger = new Logger(IntelligenceSchedulerService.name);

  constructor(private intelligenceService: IntelligenceApiService) {}

  /**
   * Daily batch job - Runs at 6:00 AM every day
   * Primary insight generation cycle
   */
  @Cron('0 6 * * *', {
    name: 'daily-intelligence-generation',
    timeZone: 'America/New_York', // Adjust to your timezone
  })
  async handleDailyInsightGeneration() {
    this.logger.log('🔥 Starting daily intelligence generation (6:00 AM)');

    try {
      const result = await this.intelligenceService.generateInsights();

      this.logger.log(
        `✅ Daily generation complete: ${result.insights_created} created, ` +
          `${result.insights_updated} updated, ${result.insights_expired} expired ` +
          `(${result.execution_time_ms}ms)`
      );

      // Log errors if any
      if (result.errors.length > 0) {
        this.logger.warn(`⚠️ ${result.errors.length} errors during generation:`, result.errors);
      }
    } catch (error) {
      this.logger.error('❌ Daily intelligence generation failed', error);
    }
  }

  /**
   * Hourly batch job - Runs every hour during business hours (8 AM - 8 PM)
   * Optional: Provides more real-time intelligence updates
   * 
   * Uncomment @Cron decorator to enable
   */
  // @Cron('0 8-20 * * *', {
  //   name: 'hourly-intelligence-generation',
  //   timeZone: 'America/New_York',
  // })
  async handleHourlyInsightGeneration() {
    this.logger.log('🔥 Starting hourly intelligence generation (business hours)');

    try {
      const result = await this.intelligenceService.generateInsights();

      this.logger.log(
        `✅ Hourly generation complete: ${result.insights_created} created, ` +
          `${result.insights_updated} updated (${result.execution_time_ms}ms)`
      );
    } catch (error) {
      this.logger.error('❌ Hourly intelligence generation failed', error);
    }
  }

  /**
   * Cleanup job - Runs at midnight every day
   * Removes old RESOLVED/DISMISSED insights (older than 90 days)
   */
  @Cron('0 0 * * *', {
    name: 'intelligence-cleanup',
    timeZone: 'America/New_York',
  })
  async handleInsightCleanup() {
    this.logger.log('🧹 Starting insight cleanup (midnight)');

    try {
      const ninetyDaysAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);

      const result = await this.intelligenceService['prisma'].insight.deleteMany({
        where: {
          status: { in: ['RESOLVED', 'DISMISSED'] },
          updated_at: { lt: ninetyDaysAgo },
        },
      });

      this.logger.log(`✅ Cleanup complete: ${result.count} old insights deleted`);
    } catch (error) {
      this.logger.error('❌ Insight cleanup failed', error);
    }
  }

  /**
   * Manual trigger (called by API endpoint or admin console)
   */
  async triggerManualGeneration(): Promise<any> {
    this.logger.log('🔥 Manual intelligence generation triggered');
    return this.intelligenceService.generateInsights();
  }
}
