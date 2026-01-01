// =============================================================================
// ORCHESTRATION CONTROLLER
// =============================================================================
// API endpoints for the Dominion's heartbeat - 40+ endpoints across 8 domains

import { Controller, Get, Post, Patch, Body, Param, Query, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';
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

@Controller('intelligence/orchestration')
@ApiTags('Orchestration Intelligence')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
export class OrchestrationController {
  constructor(
    private engineSync: EngineSynchronizationService,
    private seasonal: SeasonalOrchestrationService,
    private regional: RegionalOrchestrationService,
    private missionCurriculum: MissionCurriculumService,
    private creator: CreatorOrchestrationService,
    private intelligenceAction: IntelligenceActionService,
    private exchange: ExchangeOrchestrationService,
    private civilization: CivilizationOrchestrationService,
  ) {}

  // =============================================================================
  // ENGINE SYNCHRONIZATION (5 endpoints)
  // =============================================================================

  @Post('engines/sync')
  @ApiOperation({ summary: 'Synchronize all engines' })
  @ApiResponse({ status: 200, description: 'Engines synchronized' })
  async syncAllEngines(@Body() dto: { forceSync?: boolean; specificEngines?: any[] }) {
    return await this.engineSync.syncAllEngines(dto);
  }

  @Get('engines/:engineName/health')
  @ApiOperation({ summary: 'Check engine health' })
  async checkEngineHealth(@Param('engineName') engineName: any) {
    return await this.engineSync.checkEngineHealth(engineName);
  }

  @Post('engines/resolve-conflicts')
  @ApiOperation({ summary: 'Resolve engine conflicts' })
  async resolveEngineConflicts() {
    return await this.engineSync.resolveEngineConflicts();
  }

  @Get('engines/sequence/:type')
  @ApiOperation({ summary: 'Get orchestration sequence' })
  async getEngineSequence(@Param('type') type: string) {
    return await this.engineSync.orchestrateEngineSequence(type);
  }

  @Get('engines/status')
  @ApiOperation({ summary: 'Get all engine statuses' })
  async getAllEngineStatuses() {
    const engines = ['CIRCLE', 'YOUTH', 'MISSION', 'CURRICULUM', 'CREATOR', 'EXCHANGE', 'INTELLIGENCE', 'GOVERNANCE', 'ORCHESTRATION'];
    const healthReports = await Promise.all(
      engines.map(async (name) => await this.engineSync.checkEngineHealth(name as any))
    );
    return healthReports;
  }

  // =============================================================================
  // SEASONAL ORCHESTRATION (6 endpoints)
  // =============================================================================

  @Post('seasons/transition')
  @ApiOperation({ summary: 'Transition to new season' })
  async transitionSeason(@Body() dto: { toSeasonId: string; startDate: Date; dryRun?: boolean }) {
    return await this.seasonal.transitionSeason(dto);
  }

  @Get('seasons/:seasonId/alignment')
  @ApiOperation({ summary: 'Check seasonal alignment' })
  async getSeasonalAlignment(@Param('seasonId') seasonId: string) {
    return await this.seasonal.alignSystemsToSeason(seasonId);
  }

  @Post('seasons/:seasonId/sync/curriculum')
  @ApiOperation({ summary: 'Sync curriculum to season' })
  async syncCurriculumToSeason(@Param('seasonId') seasonId: string) {
    await this.seasonal.syncCurriculumToSeason(seasonId);
    return { seasonId, synced: true, component: 'curriculum' };
  }

  @Post('seasons/:seasonId/sync/missions')
  @ApiOperation({ summary: 'Sync missions to season' })
  async syncMissionsToSeason(@Param('seasonId') seasonId: string) {
    await this.seasonal.syncMissionsToSeason(seasonId);
    return { seasonId, synced: true, component: 'missions' };
  }

  @Post('seasons/:seasonId/sync/creators')
  @ApiOperation({ summary: 'Sync creators to season' })
  async syncCreatorsToSeason(@Param('seasonId') seasonId: string) {
    await this.seasonal.syncCreatorsToSeason(seasonId);
    return { seasonId, synced: true, component: 'creators' };
  }

  @Post('seasons/:seasonId/sync/exchange')
  @ApiOperation({ summary: 'Sync Exchange to season' })
  async syncExchangeToSeason(@Param('seasonId') seasonId: string) {
    await this.seasonal.syncExchangeToSeason(seasonId);
    return { seasonId, synced: true, component: 'exchange' };
  }

  // =============================================================================
  // REGIONAL ORCHESTRATION (4 endpoints)
  // =============================================================================

  @Post('regions/:regionId/sync')
  @ApiOperation({ summary: 'Sync regional cycles' })
  async syncRegionalCycles(@Param('regionId') regionId: string) {
    return await this.regional.syncRegionalCycles(regionId);
  }

  @Post('regions/:regionId/customize')
  @ApiOperation({ summary: 'Customize regional orchestration' })
  async customizeRegionalOrchestration(
    @Param('regionId') regionId: string,
    @Body() customization: any
  ) {
    return await this.regional.customizeRegionalOrchestration(regionId, customization);
  }

  @Get('regions/:regionId/alignment')
  @ApiOperation({ summary: 'Track regional alignment' })
  async trackRegionalAlignment(@Param('regionId') regionId: string) {
    return await this.regional.trackRegionalAlignment(regionId);
  }

  @Get('regions/:regionId/events')
  @ApiOperation({ summary: 'Get coordinated regional events' })
  async getRegionalEvents(@Param('regionId') regionId: string) {
    return await this.regional.coordinateRegionalEvents(regionId);
  }

  // =============================================================================
  // MISSION-CURRICULUM ALIGNMENT (4 endpoints)
  // =============================================================================

  @Post('mission-curriculum/link')
  @ApiOperation({ summary: 'Link mission to curriculum' })
  async linkMissionToCurriculum(@Body() dto: any) {
    return await this.missionCurriculum.linkMissionToCurriculum(dto);
  }

  @Get('missions/:missionId/prerequisites/:userId')
  @ApiOperation({ summary: 'Validate mission prerequisites' })
  async validateMissionPrerequisites(
    @Param('missionId') missionId: string,
    @Param('userId') userId: string
  ) {
    return await this.missionCurriculum.validateMissionPrerequisites(missionId, userId);
  }

  @Get('missions/recommend/:userId/:seasonId')
  @ApiOperation({ summary: 'Recommend next mission' })
  async recommendNextMission(
    @Param('userId') userId: string,
    @Param('seasonId') seasonId: string
  ) {
    return await this.missionCurriculum.recommendNextMission(userId, seasonId);
  }

  @Get('seasons/:seasonId/curriculum-mission-alignment')
  @ApiOperation({ summary: 'Track curriculum-mission alignment' })
  async trackCurriculumMissionAlignment(@Param('seasonId') seasonId: string) {
    return await this.missionCurriculum.trackCurriculumMissionAlignment(seasonId);
  }

  // =============================================================================
  // CREATOR ORCHESTRATION (4 endpoints)
  // =============================================================================

  @Post('creators/seasons/:seasonId/sync')
  @ApiOperation({ summary: 'Sync creator challenges' })
  async syncCreatorChallenges(@Param('seasonId') seasonId: string) {
    return await this.creator.syncCreatorChallenges(seasonId);
  }

  @Post('creators/challenges/launch')
  @ApiOperation({ summary: 'Launch seasonal challenge' })
  async launchSeasonalChallenge(@Body() dto: any) {
    return await this.creator.launchSeasonalChallenge(dto);
  }

  @Get('creators/spotlight/:seasonId')
  @ApiOperation({ summary: 'Get spotlight creators' })
  async spotlightCreators(@Param('seasonId') seasonId: string, @Query('limit') limit?: number) {
    return await this.creator.spotlightCreators(seasonId, limit ? parseInt(limit.toString()) : 10);
  }

  @Post('creators/renaissance/:seasonId')
  @ApiOperation({ summary: 'Orchestrate creative renaissance' })
  async orchestrateCreativeRenaissance(@Param('seasonId') seasonId: string) {
    return await this.creator.orchestrateCreativeRenaissance(seasonId);
  }

  // =============================================================================
  // INTELLIGENCE-LEADERSHIP COORDINATION (4 endpoints)
  // =============================================================================

  @Post('intelligence/actions/trigger')
  @ApiOperation({ summary: 'Trigger action from insight' })
  async triggerActionFromInsight(@Body() dto: any) {
    return await this.intelligenceAction.triggerActionFromInsight(dto);
  }

  @Post('intelligence/actions/:actionId/route')
  @ApiOperation({ summary: 'Route intelligence to leadership' })
  async routeIntelligenceToLeadership(
    @Param('actionId') actionId: string,
    @Body() body: { routedTo: string[] }
  ) {
    return await this.intelligenceAction.routeIntelligenceToLeadership(actionId, body.routedTo);
  }

  @Get('intelligence/actions/:actionId/execution')
  @ApiOperation({ summary: 'Track action execution' })
  async trackActionExecution(@Param('actionId') actionId: string) {
    return await this.intelligenceAction.trackActionExecution(actionId);
  }

  @Post('intelligence/actions/:actionId/measure-impact')
  @ApiOperation({ summary: 'Measure action impact' })
  async measureActionImpact(@Param('actionId') actionId: string, @Body() dto: any) {
    return await this.intelligenceAction.measureActionImpact({ actionId, ...dto });
  }

  // =============================================================================
  // EXCHANGE ORCHESTRATION (4 endpoints)
  // =============================================================================

  @Post('exchange/seasons/:seasonId/sync')
  @ApiOperation({ summary: 'Sync Exchange lessons' })
  async syncExchangeLessons(@Param('seasonId') seasonId: string) {
    return await this.exchange.syncExchangeLessons(seasonId);
  }

  @Post('exchange/align-tools')
  @ApiOperation({ summary: 'Align financial tools' })
  async alignFinancialTools(@Body() body: { entityType: string; entityId: string }) {
    return await this.exchange.alignFinancialTools(body.entityType, body.entityId);
  }

  @Post('exchange/missions/:missionId/integrate')
  @ApiOperation({ summary: 'Integrate Exchange with missions' })
  async integrateExchangeWithMissions(
    @Param('missionId') missionId: string,
    @Body() body: { exchangeLessonId: string }
  ) {
    return await this.exchange.integrateExchangeWithMissions(missionId, body.exchangeLessonId);
  }

  @Get('exchange/seasons/:seasonId/coherence')
  @ApiOperation({ summary: 'Track financial coherence' })
  async trackFinancialCoherence(@Param('seasonId') seasonId: string) {
    return await this.exchange.trackFinancialCoherence(seasonId);
  }

  // =============================================================================
  // CIVILIZATION-WIDE ORCHESTRATION (5 endpoints)
  // =============================================================================

  @Post('civilization/events')
  @ApiOperation({ summary: 'Orchestrate civilization event' })
  async orchestrateCivilizationEvent(@Body() dto: any) {
    return await this.civilization.orchestrateCivilizationEvent(dto);
  }

  @Get('civilization/pulse')
  @ApiOperation({ summary: 'Track civilization pulse' })
  async trackCivilizationPulse() {
    return await this.civilization.trackCivilizationPulse();
  }

  @Post('civilization/epoch-transition')
  @ApiOperation({ summary: 'Coordinate epoch transition' })
  async coordinateEpochTransition(@Body() dto: any) {
    return await this.civilization.coordinateEpochTransition(
      dto.name,
      dto.type,
      new Date(dto.startDate),
      new Date(dto.endDate)
    );
  }

  @Get('civilization/rituals/:seasonId')
  @ApiOperation({ summary: 'Sync cultural rituals' })
  async syncCulturalRituals(@Param('seasonId') seasonId: string) {
    return await this.civilization.syncCulturalRituals(seasonId);
  }

  @Get('civilization/dashboard')
  @ApiOperation({ summary: 'Civilization orchestration dashboard' })
  async getCivilizationDashboard() {
    const pulse = await this.civilization.trackCivilizationPulse();
    const engines = await this.getAllEngineStatuses();

    return {
      pulse,
      engines: engines.map(e => ({ engine: e.engineName, health: e.health, status: e.status })),
      summary: {
        overallHealth: pulse.overallHealth,
        criticalIssues: pulse.criticalIssues.length,
        activeYouth: pulse.activeYouth,
        activeCreators: pulse.activeCreators,
        upcomingEvents: pulse.upcomingEvents,
      },
    };
  }
}
