import {
  Controller,
  Get,
  Post,
  Param,
  Query,
  Body,
  UseGuards,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { StrategicIntelligenceService } from './services/strategic-intelligence.service';
import { RecommendationPriority, RecommendationStatus } from '@prisma/client';

@Controller('intelligence/strategic')
@ApiTags('Strategic Intelligence')
@ApiBearerAuth()
export class StrategicIntelligenceController {
  constructor(private strategic: StrategicIntelligenceService) {}

  @Get('youth/:userId/plan')
  @ApiOperation({ summary: 'Get strategic development plan for youth' })
  @ApiResponse({ status: 200, description: 'Strategic plan generated successfully' })
  async getYouthPlan(
    @Param('userId') userId: string,
    @Query('priority') priority?: RecommendationPriority[],
  ) {
    return this.strategic.generateStrategicPlan({
      userId,
      domain: 'YOUTH',
      priority,
    });
  }

  @Get('circles/:circleId/plan')
  @ApiOperation({ summary: 'Get strategic plan for circle' })
  @ApiResponse({ status: 200, description: 'Circle strategic plan generated successfully' })
  async getCirclePlan(
    @Param('circleId') circleId: string,
    @Query('priority') priority?: RecommendationPriority[],
  ) {
    return this.strategic.generateStrategicPlan({
      circleId,
      domain: 'CIRCLES',
      priority,
    });
  }

  @Get('missions/plan')
  @ApiOperation({ summary: 'Get strategic plan for missions' })
  @ApiResponse({ status: 200, description: 'Mission strategic plan generated successfully' })
  async getMissionPlan(
    @Query('regionId') regionId?: string,
    @Query('seasonId') seasonId?: string,
    @Query('priority') priority?: RecommendationPriority[],
  ) {
    return this.strategic.generateStrategicPlan({
      regionId,
      seasonId,
      domain: 'MISSIONS',
      priority,
    });
  }

  @Get('regions/:regionId/plan')
  @ApiOperation({ summary: 'Get strategic expansion plan for region' })
  @ApiResponse({ status: 200, description: 'Regional strategic plan generated successfully' })
  async getRegionalPlan(
    @Param('regionId') regionId: string,
    @Query('priority') priority?: RecommendationPriority[],
  ) {
    return this.strategic.generateStrategicPlan({
      regionId,
      domain: 'REGIONS',
      priority,
    });
  }

  @Get('dashboard')
  @ApiOperation({ summary: 'Get strategic dashboard for current context' })
  @ApiResponse({ status: 200, description: 'Strategic dashboard loaded successfully' })
  async getStrategicDashboard(
    @Query('userId') userId?: string,
    @Query('circleId') circleId?: string,
    @Query('regionId') regionId?: string,
    @Query('priority') priority?: RecommendationPriority[],
  ) {
    return this.strategic.generateStrategicPlan({
      userId,
      circleId,
      regionId,
      priority,
    });
  }

  @Get('recommendations/status/:status')
  @ApiOperation({ summary: 'Get recommendations by status' })
  @ApiResponse({ status: 200, description: 'Recommendations retrieved successfully' })
  async getRecommendationsByStatus(@Param('status') status: string) {
    return this.strategic.getRecommendationsByStatus([status]);
  }

  @Get('recommendations/priority')
  @ApiOperation({ summary: 'Get recommendations by priority' })
  @ApiResponse({ status: 200, description: 'Recommendations retrieved successfully' })
  async getRecommendationsByPriority(@Query('priority') priority: RecommendationPriority[]) {
    return this.strategic.getRecommendationsByPriority(
      Array.isArray(priority) ? priority : [priority],
    );
  }

  @Post('recommendations/:id/review')
  @ApiOperation({ summary: 'Review and approve/reject recommendation' })
  @ApiResponse({ status: 200, description: 'Recommendation reviewed successfully' })
  async reviewRecommendation(
    @Param('id') id: string,
    @Body()
    review: {
      userId: string;
      status: RecommendationStatus;
      notes?: string;
    },
  ) {
    return this.strategic.reviewRecommendation(id, review.userId, review.status, review.notes);
  }

  @Post('recommendations/:id/implement')
  @ApiOperation({ summary: 'Mark recommendation as implemented' })
  @ApiResponse({ status: 200, description: 'Recommendation marked as in progress' })
  async implementRecommendation(@Param('id') id: string) {
    return this.strategic.implementRecommendation(id);
  }

  @Post('recommendations/:id/complete')
  @ApiOperation({ summary: 'Mark recommendation as completed with outcome' })
  @ApiResponse({ status: 200, description: 'Recommendation marked as completed' })
  async completeRecommendation(
    @Param('id') id: string,
    @Body()
    completion: {
      actualOutcome: any;
      variance?: number;
      lessonsLearned?: string;
    },
  ) {
    return this.strategic.completeRecommendation(id, completion);
  }
}
