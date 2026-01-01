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
  Request,
} from '@nestjs/common';
import {
  ApiTags,
  ApiBearerAuth,
  ApiOperation,
  ApiResponse,
  ApiQuery,
} from '@nestjs/swagger';
import { OutreachService } from './outreach.service';
import { CreateOutreachDto, UpdateOutreachDto, OutreachQueryDto } from './dto/outreach.dto';
import { OutreachEntity } from './entities/outreach.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName, OutreachType } from '@prisma/client';

@ApiTags('outreach')
@Controller('outreach')
export class OutreachController {
  constructor(private readonly outreachService: OutreachService) {}

  @Get()
  @ApiOperation({ summary: 'Get all outreach records with optional filters' })
  @ApiQuery({ name: 'regionId', required: false, description: 'Filter by region ID' })
  @ApiQuery({ name: 'schoolId', required: false, description: 'Filter by school ID' })
  @ApiQuery({ name: 'ambassadorId', required: false, description: 'Filter by ambassador ID' })
  @ApiQuery({ name: 'type', required: false, enum: OutreachType, description: 'Filter by outreach type' })
  @ApiResponse({
    status: 200,
    description: 'List of outreach records with ambassador, region, and school info',
    type: [OutreachEntity],
  })
  async findAll(@Query() query: OutreachQueryDto): Promise<OutreachEntity[]> {
    return this.outreachService.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get outreach record by ID' })
  @ApiResponse({
    status: 200,
    description: 'Outreach record details',
    type: OutreachEntity,
  })
  @ApiResponse({ status: 404, description: 'Outreach record not found' })
  async findOne(@Param('id') id: string): Promise<OutreachEntity> {
    return this.outreachService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.AMBASSADOR, RoleName.REGIONAL_DIRECTOR, RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Log new outreach activity (AMBASSADOR / REGIONAL_DIRECTOR / ADMIN)' })
  @ApiResponse({
    status: 201,
    description: 'Outreach record created successfully',
    type: OutreachEntity,
  })
  @ApiResponse({ status: 404, description: 'Region or School not found' })
  async create(@Body() dto: CreateOutreachDto, @Request() req: any) {
    const ambassadorId = req.user.userId;
    return this.outreachService.create(dto, ambassadorId);
  }

  @Patch(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.AMBASSADOR, RoleName.REGIONAL_DIRECTOR, RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update outreach record (own records only)' })
  @ApiResponse({
    status: 200,
    description: 'Outreach record updated successfully',
    type: OutreachEntity,
  })
  @ApiResponse({ status: 403, description: 'Cannot update others outreach records' })
  @ApiResponse({ status: 404, description: 'Outreach record or School not found' })
  async update(@Param('id') id: string, @Body() dto: UpdateOutreachDto, @Request() req: any) {
    const userId = req.user.userId;
    return this.outreachService.update(id, dto, userId);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.AMBASSADOR, RoleName.REGIONAL_DIRECTOR, RoleName.ADMIN)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete outreach record (own records only)' })
  @ApiResponse({ status: 200, description: 'Outreach record deleted successfully' })
  @ApiResponse({ status: 403, description: 'Cannot delete others outreach records' })
  @ApiResponse({ status: 404, description: 'Outreach record not found' })
  async remove(@Param('id') id: string, @Request() req: any) {
    const userId = req.user.userId;
    return this.outreachService.remove(id, userId);
  }
}
