import { Controller, Get, Query } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiQuery } from '@nestjs/swagger';
import { SeasonsService } from './seasons.service';

@ApiTags('seasons')
@Controller('seasons')
export class SeasonsController {
  constructor(private seasonsService: SeasonsService) {}

  @Get()
  @ApiOperation({ summary: 'List all seasons with date ranges' })
  async findAll() {
    return this.seasonsService.findAll();
  }

  @Get('current')
  @ApiOperation({ summary: 'Get active season based on server date' })
  async getCurrent() {
    return this.seasonsService.getCurrent();
  }
}
