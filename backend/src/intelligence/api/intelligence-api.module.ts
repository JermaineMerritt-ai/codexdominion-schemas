/**
 * Intelligence API Module
 * 
 * NestJS module configuration for Intelligence API V1
 * 
 * Provides:
 * - RulesEngineService: Evaluates 47 intelligence rules
 * - IntelligenceApiService: Business logic for insight generation and retrieval
 * - IntelligenceSchedulerService: Automated batch job scheduler (daily at 6 AM, optional hourly)
 * - IntelligenceApiController: 8 REST endpoints (including manual /generate trigger)
 * 
 * Depends on:
 * - PrismaModule: Database access
 * - AuthModule: JWT authentication
 * - ScheduleModule: Cron job scheduling
 */

import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { PrismaModule } from '../../prisma/prisma.module';
import { IntelligenceApiController } from './intelligence-api.controller';
import { IntelligenceApiService } from './services/intelligence-api.service';
import { RulesEngineService } from './services/rules-engine.service';
import { IntelligenceSchedulerService } from './services/intelligence-scheduler.service';

@Module({
  imports: [
    PrismaModule,
    ScheduleModule.forRoot(), // Enable cron jobs
  ],
  controllers: [IntelligenceApiController],
  providers: [
    IntelligenceApiService,
    RulesEngineService,
    IntelligenceSchedulerService, // Scheduled batch jobs
  ],
  exports: [IntelligenceApiService, RulesEngineService], // Export for use in other modules
})
export class IntelligenceApiModule {}
