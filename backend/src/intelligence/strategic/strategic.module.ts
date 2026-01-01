import { Module } from '@nestjs/common';
import { PrismaService } from '@/prisma/prisma.service';
import { StrategicIntelligenceController } from './strategic.controller';
import { StrategicIntelligenceService } from './services/strategic-intelligence.service';
import { YouthStrategyEngine } from './models/youth-strategy.model';
import { CircleStrategyEngine } from './models/circle-strategy.model';
import { MissionStrategyEngine } from './models/mission-strategy.model';

@Module({
  controllers: [StrategicIntelligenceController],
  providers: [
    PrismaService,
    StrategicIntelligenceService,
    YouthStrategyEngine,
    CircleStrategyEngine,
    MissionStrategyEngine,
  ],
  exports: [StrategicIntelligenceService],
})
export class StrategicModule {}
