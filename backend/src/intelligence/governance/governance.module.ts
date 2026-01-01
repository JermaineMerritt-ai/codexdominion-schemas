// ======================================================
// GOVERNANCE MODULE
// Wires all governance services and controller
// ======================================================

import { Module } from '@nestjs/common';
import { GovernanceController } from './governance.controller';
import { CouncilCoordinationService } from './services/council-coordination.service';
import { ApprovalProtocolService } from './services/approval-protocol.service';
import { LeadershipOrchestrationService } from './services/leadership-orchestration.service';
import { RegionalGovernanceService } from './services/regional-governance.service';
import { PrismaService } from '../../prisma/prisma.service';

@Module({
  controllers: [GovernanceController],
  providers: [
    PrismaService,
    CouncilCoordinationService,
    ApprovalProtocolService,
    LeadershipOrchestrationService,
    RegionalGovernanceService,
  ],
  exports: [
    CouncilCoordinationService,
    ApprovalProtocolService,
    LeadershipOrchestrationService,
    RegionalGovernanceService,
  ],
})
export class GovernanceModule {}
