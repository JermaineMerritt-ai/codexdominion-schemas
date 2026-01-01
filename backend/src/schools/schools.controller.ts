import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
} from '@nestjs/common';
import {
  ApiTags,
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiQuery,
} from '@nestjs/swagger';
import { SchoolsService } from './schools.service';
import { CreateSchoolDto, UpdateSchoolDto, SchoolQueryDto } from './dto/school.dto';
import { SchoolEntity } from './entities/school.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName } from '@prisma/client';

@ApiTags('schools')
@Controller('schools')
export class SchoolsController {
  constructor(private readonly schoolsService: SchoolsService) {}

  @Get()
  @ApiOperation({ summary: 'Get all schools with optional filters' })
  @ApiQuery({ name: 'regionId', required: false, description: 'Filter by region ID' })
  @ApiResponse({
    status: 200,
    description: 'List of schools with region info and counts',
    type: [SchoolEntity],
  })
  async findAll(@Query() query: SchoolQueryDto): Promise<SchoolEntity[]> {
    return this.schoolsService.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get school by ID with details' })
  @ApiResponse({
    status: 200,
    description: 'School details with region and counts',
    type: SchoolEntity,
  })
  @ApiResponse({ status: 404, description: 'School not found' })
  async findOne(@Param('id') id: string): Promise<SchoolEntity> {
    return this.schoolsService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.AMBASSADOR)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create new school (ADMIN / AMBASSADOR)' })
  @ApiResponse({
    status: 201,
    description: 'School created successfully',
    type: SchoolEntity,
  })
  @ApiResponse({ status: 404, description: 'Region not found' })
  async create(@Body() dto: CreateSchoolDto) {
    return this.schoolsService.create(dto);
  }

  @Patch(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.AMBASSADOR, RoleName.REGIONAL_DIRECTOR)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update school (ADMIN / AMBASSADOR / REGIONAL_DIRECTOR)' })
  @ApiResponse({
    status: 200,
    description: 'School updated successfully',
    type: SchoolEntity,
  })
  @ApiResponse({ status: 404, description: 'School or Region not found' })
  async update(@Param('id') id: string, @Body() dto: UpdateSchoolDto) {
    return this.schoolsService.update(id, dto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete school (ADMIN only)' })
  @ApiResponse({ status: 200, description: 'School deleted successfully' })
  @ApiResponse({ status: 404, description: 'School not found' })
  async remove(@Param('id') id: string) {
    return this.schoolsService.remove(id);
  }
}
