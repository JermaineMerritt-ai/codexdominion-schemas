import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Body,
  Param,
  UseGuards,
} from '@nestjs/common';
import {
  ApiTags,
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
} from '@nestjs/swagger';
import { RegionsService } from './regions.service';
import { CreateRegionDto, UpdateRegionDto } from './dto/region.dto';
import { RegionEntity } from './entities/region.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName } from '@prisma/client';

@ApiTags('regions')
@Controller('regions')
export class RegionsController {
  constructor(private readonly regionsService: RegionsService) {}

  @Get()
  @ApiOperation({ summary: 'Get all regions with counts' })
  @ApiResponse({
    status: 200,
    description: 'List of regions with director info and counts',
    type: [RegionEntity],
  })
  async findAll(): Promise<RegionEntity[]> {
    return this.regionsService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get region by ID with details' })
  @ApiResponse({
    status: 200,
    description: 'Region details with director and counts',
    type: RegionEntity,
  })
  @ApiResponse({ status: 404, description: 'Region not found' })
  async findOne(@Param('id') id: string): Promise<RegionEntity> {
    return this.regionsService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create new region (ADMIN only)' })
  @ApiResponse({
    status: 201,
    description: 'Region created successfully',
    type: RegionEntity,
  })
  @ApiResponse({ status: 404, description: 'Director not found' })
  async create(@Body() dto: CreateRegionDto) {
    return this.regionsService.create(dto);
  }

  @Patch(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.REGIONAL_DIRECTOR)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update region (ADMIN / REGIONAL_DIRECTOR)' })
  @ApiResponse({
    status: 200,
    description: 'Region updated successfully',
    type: RegionEntity,
  })
  @ApiResponse({ status: 404, description: 'Region or Director not found' })
  async update(@Param('id') id: string, @Body() dto: UpdateRegionDto) {
    return this.regionsService.update(id, dto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete region (ADMIN only)' })
  @ApiResponse({ status: 200, description: 'Region deleted successfully' })
  @ApiResponse({ status: 404, description: 'Region not found' })
  async remove(@Param('id') id: string) {
    return this.regionsService.remove(id);
  }
}
