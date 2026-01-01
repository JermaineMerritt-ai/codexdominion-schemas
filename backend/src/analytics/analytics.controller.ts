import { Controller, Get, UseGuards, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { AnalyticsService } from './analytics.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName } from '@prisma/client';

@ApiTags('analytics')
@Controller('analytics')
export class AnalyticsController {
  constructor(private analyticsService: AnalyticsService) {}

  @Get('dashboard')
  @ApiOperation({ 
    summary: 'Get simplified dashboard metrics',
    description: 'Streamlined key metrics for dashboard widgets and quick stats'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Dashboard metrics returned successfully',
    schema: {
      example: {
        active_youth: 320,
        active_circles: 18,
        missions_completed_this_week: 112,
        regions_active: 4
      }
    }
  })
  async getDashboard() {
    return this.analyticsService.getDashboard();
  }

  @Get('overview')
  @ApiOperation({ 
    summary: 'Get system overview metrics',
    description: 'High-level KPIs for Empire Dashboard: users, circles, missions, events, creators, regions, and current season'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Overview metrics returned successfully',
    schema: {
      example: {
        users: { total: 125, youth: 100, captains: 10, ambassadors: 5, regionalDirectors: 3 },
        circles: { total: 15, active: 12, avgSize: 8 },
        missions: { total: 24, active: 6, completed: 180 },
        events: { total: 8, upcoming: 3 },
        creators: { artifacts: 45, activeChallenges: 4 },
        expansion: { regions: 5, schools: 12 },
        season: { current: 'Mastery Season', phase: 'MASTERY', startDate: '2025-01-01', endDate: '2025-03-31' }
      }
    }
  })
  async getOverview() {
    return this.analyticsService.getOverview();
  }

  @Get('circles')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR, RoleName.YOUTH_CAPTAIN)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get detailed circle health metrics',
    description: 'Circle-by-circle breakdown: members, sessions, attendance, health status. Filter by region_id for regional dashboards.'
  })
  @ApiQuery({ name: 'region_id', required: false, type: String, description: 'Filter circles by region UUID' })
  @ApiResponse({ 
    status: 200, 
    description: 'Circle metrics returned successfully' 
  })
  async getCircleMetrics(@Query('region_id') regionId?: string) {
    return this.analyticsService.getCircleMetrics(regionId);
  }

  @Get('missions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get mission completion and engagement metrics',
    description: 'Mission-by-mission breakdown: assignments, submissions, completion rates. Filter by region_id for regional dashboards.'
  })
  @ApiQuery({ name: 'region_id', required: false, type: String, description: 'Filter missions by region UUID' })
  @ApiResponse({ 
    status: 200, 
    description: 'Mission metrics returned successfully' 
  })
  async getMissionMetrics(@Query('region_id') regionId?: string) {
    return this.analyticsService.getMissionMetrics(regionId);
  }

  @Get('regions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get regional expansion and activity metrics',
    description: 'Region-by-region breakdown: circles, schools, members, events, outreach, activity level'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Regional metrics returned successfully' 
  })
  async getRegionMetrics() {
    return this.analyticsService.getRegionMetrics();
  }

  @Get('creators')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get creator output and challenge metrics',
    description: 'Creator economy metrics: artifacts by type, challenge submissions, top creators'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Creator metrics returned successfully' 
  })
  async getCreatorMetrics() {
    return this.analyticsService.getCreatorMetrics();
  }

  @Get('youth')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR, RoleName.YOUTH_CAPTAIN)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get youth engagement and progression metrics',
    description: 'Youth metrics: total youth, circle participation, mission completion, Rise Path distribution'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Youth metrics returned successfully' 
  })
  async getYouthMetrics() {
    return this.analyticsService.getYouthMetrics();
  }

  @Get('events')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR, RoleName.AMBASSADOR)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Get event attendance and engagement metrics',
    description: 'Event-by-event breakdown: registrations, attendance, attendance rates, ceremony scripts'
  })
  @ApiResponse({ 
    status: 200, 
    description: 'Event metrics returned successfully' 
  })
  async getEventMetrics() {
    return this.analyticsService.getEventMetrics();
  }
}
