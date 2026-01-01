import {
  Controller,
  Get,
  Query,
  Req,
  UseGuards,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { IntelligenceService } from './intelligence.service';
import { IntelligenceQueryDto } from './dto/intelligence-query.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { Request } from 'express';

interface RequestWithUser extends Request {
  user: {
    id: string;
    roles: string[];
    regionId?: string;
  };
}

@ApiTags('intelligence')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('intelligence')
export class IntelligenceController {
  constructor(private readonly intelligenceService: IntelligenceService) {}

  @Get('alerts')
  @ApiOperation({ summary: 'Get intelligence alerts for current user' })
  @ApiResponse({ status: 200, description: 'Returns high-priority alerts' })
  async getAlerts(
    @Req() req: RequestWithUser,
    @Query() query: IntelligenceQueryDto
  ) {
    return this.intelligenceService.getAlerts({
      domain: query.domain,
      regionId: query.regionId ?? req.user.regionId,
      userId: req.user.id,
      roles: req.user.roles,
    });
  }

  @Get('recommendations')
  @ApiOperation({ summary: 'Get intelligence recommendations for current user' })
  @ApiResponse({ status: 200, description: 'Returns recommended actions' })
  async getRecommendations(
    @Req() req: RequestWithUser,
    @Query() query: IntelligenceQueryDto
  ) {
    return this.intelligenceService.getRecommendations({
      domain: query.domain,
      regionId: query.regionId ?? req.user.regionId,
      userId: req.user.id,
      roles: req.user.roles,
    });
  }

  @Get('forecasts')
  @ApiOperation({ summary: 'Get intelligence forecasts for current user' })
  @ApiResponse({ status: 200, description: 'Returns predictive insights' })
  async getForecasts(
    @Req() req: RequestWithUser,
    @Query() query: IntelligenceQueryDto
  ) {
    return this.intelligenceService.getForecasts({
      domain: query.domain,
      regionId: query.regionId ?? req.user.regionId,
      userId: req.user.id,
      roles: req.user.roles,
    });
  }

  @Get('opportunities')
  @ApiOperation({ summary: 'Get intelligence opportunities for current user' })
  @ApiResponse({ status: 200, description: 'Returns growth opportunities' })
  async getOpportunities(
    @Req() req: RequestWithUser,
    @Query() query: IntelligenceQueryDto
  ) {
    return this.intelligenceService.getOpportunities({
      domain: query.domain,
      regionId: query.regionId ?? req.user.regionId,
      userId: req.user.id,
      roles: req.user.roles,
    });
  }

  @Get('insights')
  @ApiOperation({ summary: 'Get all intelligence insights grouped by type' })
  @ApiResponse({ status: 200, description: 'Returns all insights grouped by type' })
  async getInsights(
    @Req() req: RequestWithUser,
    @Query() query: IntelligenceQueryDto
  ) {
    return this.intelligenceService.getInsights({
      domain: query.domain,
      regionId: query.regionId ?? req.user.regionId,
      userId: req.user.id,
      roles: req.user.roles,
    });
  }
}
