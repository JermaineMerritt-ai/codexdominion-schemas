import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiQuery } from '@nestjs/swagger';
import { MissionsService } from './missions.service';

@ApiTags('missions')
@Controller('missions')
export class MissionsController {
  constructor(private missionsService: MissionsService) {}

  @Get()
  @ApiOperation({ summary: 'List missions with optional filters' })
  @ApiQuery({ name: 'season_id', required: false, description: 'Filter by season UUID' })
  @ApiQuery({ name: 'month', required: false, description: 'Filter by month (1-12)' })
  async findAll(@Query('season_id') seasonId?: string, @Query('month') month?: string) {
    return this.missionsService.findAll(seasonId, month ? parseInt(month) : undefined);
  }

  @Get('current')
  @ApiOperation({ summary: 'Get mission for current week/season' })
  async getCurrent() {
    return this.missionsService.getCurrent();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get mission by ID' })
  async findOne(@Param('id') id: string) {
    return this.missionsService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create new mission (ADMIN/COUNCIL only)' })
  async create(@Body() data: any) {
    return this.missionsService.create(data);
  }

  @Post(':id/assign')
  @ApiOperation({ summary: 'Assign mission to user or circle' })
  async assign(@Param('id') id: string, @Body() data: any) {
    return this.missionsService.assignMission(id, data);
  }

  @Post(':id/submit')
  @ApiOperation({ summary: 'Submit mission work' })
  async submit(@Param('id') id: string, @Body() data: any) {
    return this.missionsService.submitMission(id, data);
  }
}
