/**
 * Intelligence API Controller
 * 
 * REST API for CodexDominion 47 Intelligence System
 * 
 * Endpoints:
 * - GET /intelligence/feed - Main intelligence feed (role-scoped, prioritized)
 * - GET /intelligence/alerts - Alerts only
 * - GET /intelligence/recommendations - Recommendations only
 * - GET /intelligence/forecasts - Forecasts only
 * - GET /intelligence/opportunities - Opportunities only
 * - GET /intelligence/insights/:id - Single insight detail
 * - PATCH /intelligence/insights/:id - Update insight status
 * 
 * All endpoints require JWT authentication and automatically filter by user role + scope.
 */

import {
  Controller,
  Get,
  Post,
  Patch,
  Param,
  Query,
  Body,
  UseGuards,
  Request,
  HttpCode,
  HttpStatus,
  ForbiddenException,
} from '@nestjs/common';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiQuery,
  ApiParam,
} from '@nestjs/swagger';
import { IntelligenceApiService } from './services/intelligence-api.service';
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';
import {
  GetFeedDto,
  UpdateInsightStatusDto,
  InsightFeedResponse,
  InsightDetail,
  AuthUserContext,
  InsightType,
  InsightDomain,
  InsightStatus,
} from './types/intelligence-api.types';

@ApiTags('Intelligence API')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('intelligence')
export class IntelligenceApiController {
  constructor(private readonly intelligenceService: IntelligenceApiService) {}

  /**
   * GET /intelligence/feed
   * Main intelligence feed - role-scoped, prioritized mix of all insight types
   */
  @Get('feed')
  @ApiOperation({
    summary: 'Get intelligence feed',
    description:
      'Returns role-scoped, prioritized intelligence feed. Automatically filters by user role + scope. ' +
      'Admin/Council see everything, Regional Directors see their region, Captains see their circle.',
  })
  @ApiQuery({ name: 'type', enum: InsightType, required: false, description: 'Filter by insight type' })
  @ApiQuery({ name: 'domain', enum: InsightDomain, required: false, description: 'Filter by domain' })
  @ApiQuery({ name: 'status', enum: InsightStatus, required: false, description: 'Filter by status (default: ACTIVE)' })
  @ApiQuery({ name: 'limit', type: Number, required: false, description: 'Max results (default: 50)' })
  @ApiQuery({ name: 'offset', type: Number, required: false, description: 'Pagination offset (default: 0)' })
  @ApiResponse({
    status: 200,
    description: 'Intelligence feed retrieved successfully',
  })
  async getInsightFeed(@Query() filters: GetFeedDto, @Request() req): Promise<InsightFeedResponse> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getInsightFeed(filters, user);
  }

  /**
   * GET /intelligence/alerts
   * Alerts only (type = ALERT)
   */
  @Get('alerts')
  @ApiOperation({
    summary: 'Get alerts',
    description: 'Returns urgent issues requiring immediate attention. Filtered to type=ALERT.',
  })
  @ApiQuery({ name: 'domain', enum: InsightDomain, required: false, description: 'Filter by domain' })
  @ApiQuery({ name: 'status', enum: InsightStatus, required: false, description: 'Filter by status (default: ACTIVE)' })
  @ApiQuery({ name: 'limit', type: Number, required: false, description: 'Max results (default: 50)' })
  @ApiQuery({ name: 'offset', type: Number, required: false, description: 'Pagination offset (default: 0)' })
  @ApiResponse({
    status: 200,
    description: 'Alerts retrieved successfully',
  })
  async getAlerts(@Query() filters: GetFeedDto, @Request() req): Promise<InsightFeedResponse> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getAlerts(filters, user);
  }

  /**
   * GET /intelligence/recommendations
   * Recommendations only (type = RECOMMENDATION)
   */
  @Get('recommendations')
  @ApiOperation({
    summary: 'Get recommendations',
    description: 'Returns actionable suggestions for improvement. Filtered to type=RECOMMENDATION.',
  })
  @ApiQuery({ name: 'domain', enum: InsightDomain, required: false, description: 'Filter by domain' })
  @ApiQuery({ name: 'status', enum: InsightStatus, required: false, description: 'Filter by status (default: ACTIVE)' })
  @ApiQuery({ name: 'limit', type: Number, required: false, description: 'Max results (default: 50)' })
  @ApiQuery({ name: 'offset', type: Number, required: false, description: 'Pagination offset (default: 0)' })
  @ApiResponse({
    status: 200,
    description: 'Recommendations retrieved successfully',
  })
  async getRecommendations(@Query() filters: GetFeedDto, @Request() req): Promise<InsightFeedResponse> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getRecommendations(filters, user);
  }

  /**
   * GET /intelligence/forecasts
   * Forecasts only (type = FORECAST)
   */
  @Get('forecasts')
  @ApiOperation({
    summary: 'Get forecasts',
    description: 'Returns future-facing projections for planning. Filtered to type=FORECAST.',
  })
  @ApiQuery({ name: 'domain', enum: InsightDomain, required: false, description: 'Filter by domain' })
  @ApiQuery({ name: 'status', enum: InsightStatus, required: false, description: 'Filter by status (default: ACTIVE)' })
  @ApiQuery({ name: 'limit', type: Number, required: false, description: 'Max results (default: 50)' })
  @ApiQuery({ name: 'offset', type: Number, required: false, description: 'Pagination offset (default: 0)' })
  @ApiResponse({
    status: 200,
    description: 'Forecasts retrieved successfully',
  })
  async getForecasts(@Query() filters: GetFeedDto, @Request() req): Promise<InsightFeedResponse> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getForecasts(filters, user);
  }

  /**
   * GET /intelligence/opportunities
   * Opportunities only (type = OPPORTUNITY)
   */
  @Get('opportunities')
  @ApiOperation({
    summary: 'Get opportunities',
    description: 'Returns positive signals to celebrate/leverage. Filtered to type=OPPORTUNITY.',
  })
  @ApiQuery({ name: 'domain', enum: InsightDomain, required: false, description: 'Filter by domain' })
  @ApiQuery({ name: 'status', enum: InsightStatus, required: false, description: 'Filter by status (default: ACTIVE)' })
  @ApiQuery({ name: 'limit', type: Number, required: false, description: 'Max results (default: 50)' })
  @ApiQuery({ name: 'offset', type: Number, required: false, description: 'Pagination offset (default: 0)' })
  @ApiResponse({
    status: 200,
    description: 'Opportunities retrieved successfully',
  })
  async getOpportunities(@Query() filters: GetFeedDto, @Request() req): Promise<InsightFeedResponse> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getOpportunities(filters, user);
  }

  /**
   * GET /intelligence/insights/:id
   * Get single insight detail with full context and audit trail
   */
  @Get('insights/:id')
  @ApiOperation({
    summary: 'Get insight by ID',
    description: 'Returns full insight detail including events audit trail. Requires user to have access to this insight.',
  })
  @ApiParam({ name: 'id', type: String, description: 'Insight UUID' })
  @ApiResponse({
    status: 200,
    description: 'Insight retrieved successfully',
  })
  @ApiResponse({
    status: 404,
    description: 'Insight not found',
  })
  @ApiResponse({
    status: 403,
    description: 'User does not have permission to view this insight',
  })
  async getInsightById(@Param('id') id: string, @Request() req): Promise<InsightDetail> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.getInsightById(id, user);
  }

  /**
   * PATCH /intelligence/insights/:id
   * Update insight status (ACKNOWLEDGED, RESOLVED, DISMISSED)
   * Records action in InsightEvent audit trail
   */
  @Patch('insights/:id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: 'Update insight status',
    description:
      'Updates insight lifecycle status. Valid transitions: ' +
      'ACTIVE → ACKNOWLEDGED → RESOLVED, or ACTIVE → DISMISSED. ' +
      'Action is recorded in audit trail with user_id and timestamp.',
  })
  @ApiParam({ name: 'id', type: String, description: 'Insight UUID' })
  @ApiResponse({
    status: 200,
    description: 'Insight status updated successfully',
  })
  @ApiResponse({
    status: 404,
    description: 'Insight not found',
  })
  @ApiResponse({
    status: 403,
    description: 'User does not have permission to update this insight',
  })
  async updateInsightStatus(
    @Param('id') id: string,
    @Body() dto: UpdateInsightStatusDto,
    @Request() req
  ): Promise<InsightDetail> {
    const user: AuthUserContext = this.extractUserContext(req);
    return this.intelligenceService.updateInsightStatus(id, dto, user);
  }

  /**
   * POST /intelligence/generate
   * Manually trigger batch insight generation (for testing/admin use)
   * Runs all 47 rules and upserts insights
   */
  @Post('generate')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({
    summary: 'Generate insights (manual trigger)',
    description:
      '🔥 Manually triggers batch insight generation. Runs all 47 intelligence rules, ' +
      'upserts insights (avoiding duplicates), and expires/resolves stale insights. ' +
      'Normally runs automatically via scheduled job. Returns batch execution statistics.',
  })
  @ApiResponse({
    status: 200,
    description: 'Batch generation completed successfully',
    schema: {
      example: {
        total_evaluated: 47,
        total_triggered: 12,
        insights_created: 8,
        insights_updated: 4,
        insights_expired: 2,
        execution_time_ms: 3521,
        errors: [],
      },
    },
  })
  async generateInsights(@Request() req) {
    const user: AuthUserContext = this.extractUserContext(req);

    // Only ADMIN/COUNCIL can manually trigger
    if (!user.roles.includes('ADMIN') && !user.roles.includes('COUNCIL')) {
      throw new ForbiddenException('Only ADMIN or COUNCIL can trigger batch generation');
    }

    return this.intelligenceService.generateInsights();
  }

  // ==============================================================================
  // HELPER METHODS
  // ==============================================================================

  /**
   * Extract user context from JWT request
   * Maps JWT payload to AuthUserContext interface
   */
  private extractUserContext(req: any): AuthUserContext {
    const jwtUser = req.user; // Injected by JwtAuthGuard

    return {
      user_id: jwtUser.sub || jwtUser.userId,
      email: jwtUser.email,
      roles: jwtUser.roles || [],
      region_id: jwtUser.region_id,
      circle_id: jwtUser.circle_id,
    };
  }
}
