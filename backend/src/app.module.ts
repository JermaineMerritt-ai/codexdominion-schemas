import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { HealthModule } from './health/health.module';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { AnalyticsModule } from './analytics/analytics.module';
import { MissionsModule } from './missions/missions.module';
import { CultureModule } from './culture/culture.module';
import { CirclesModule } from './circles/circles.module';
import { SeasonsModule } from './seasons/seasons.module';
import { CreatorsModule } from './creators/creators.module';
import { RegionsModule } from './regions/regions.module';
import { SchoolsModule } from './schools/schools.module';
import { OutreachModule } from './outreach/outreach.module';
import { EventsModule } from './events/events.module';
import { AlertsModule } from './alerts/alerts.module';
// import { IntelligenceModule } from './intelligence/intelligence.module'; // DISABLED: Replaced by IntelligenceApiModule (V1)
import { StrategicModule } from './intelligence/strategic/strategic.module';
import { GovernanceModule } from './intelligence/governance/governance.module';
import { OrchestrationModule } from './intelligence/orchestration/orchestration.module';
import { IntelligenceApiModule } from './intelligence/api/intelligence-api.module';
import { MarketsModule } from './markets/markets.module';
import { AcademyModule } from './academy/academy.module';
import { UploadsModule } from './uploads/uploads.module';
import { TasksModule } from './tasks/tasks.module';
import { DetectorsModule } from './detectors/detectors.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
    PrismaModule,
    HealthModule,
    AuthModule,
    AnalyticsModule,
    SeasonsModule,
    MissionsModule,
    CultureModule,
    CirclesModule,
    CreatorsModule,
    RegionsModule,
    SchoolsModule,
    OutreachModule,
    EventsModule,
    AlertsModule,
    // IntelligenceModule, // DISABLED: Replaced by IntelligenceApiModule
    StrategicModule,
    GovernanceModule,
    OrchestrationModule,
    IntelligenceApiModule,
    MarketsModule,
    AcademyModule,
    UploadsModule,
    TasksModule,
    DetectorsModule, // ACTION AI: Follow-Up detectors (Invoice + Lead)
  ],
  controllers: [AppController],
  providers: [],
})
export class AppModule {}
