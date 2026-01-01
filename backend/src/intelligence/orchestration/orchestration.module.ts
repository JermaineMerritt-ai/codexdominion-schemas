// =============================================================================
// ORCHESTRATION MODULE
// =============================================================================
// The Dominion's heartbeat - wires all 8 orchestration services

import { Module } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { OrchestrationController } from './orchestration.controller';
import { EngineSynchronizationService } from './services/engine-synchronization.service';
import { SeasonalOrchestrationService } from './services/seasonal-orchestration.service';
import {
  RegionalOrchestrationService,
  MissionCurriculumService,
  CreatorOrchestrationService,
  IntelligenceActionService,
  ExchangeOrchestrationService,
  CivilizationOrchestrationService,
} from './services/consolidated-orchestration.services';

@Module({
  controllers: [OrchestrationController],
  providers: [
    PrismaService,
    EngineSynchronizationService,
    SeasonalOrchestrationService,
    RegionalOrchestrationService,
    MissionCurriculumService,
    CreatorOrchestrationService,
    IntelligenceActionService,
    ExchangeOrchestrationService,
    CivilizationOrchestrationService,
  ],
  exports: [
    EngineSynchronizationService,
    SeasonalOrchestrationService,
    RegionalOrchestrationService,
    MissionCurriculumService,
    CreatorOrchestrationService,
    IntelligenceActionService,
    ExchangeOrchestrationService,
    CivilizationOrchestrationService,
  ],
})
export class OrchestrationModule {}
