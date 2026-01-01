import { Controller, Get, Post, Patch, Delete, Body, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { CirclesService } from './circles.service';
import { CreateCircleDto, CreateSessionDto, RecordAttendanceDto, AddMemberDto } from './dto/circles.dto';
import { CircleCaptainGuard } from './guards/circle-captain.guard';

@ApiTags('circles')
@Controller('circles')
export class CirclesController {
  constructor(private circlesService: CirclesService) {}

  @Get()
  @ApiOperation({ summary: 'List all circles' })
  async findAll() {
    return this.circlesService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get circle by ID' })
  async findOne(@Param('id') id: string) {
    return this.circlesService.findOne(id);
  }

  @Post()
  @ApiOperation({ summary: 'Create new circle (ADMIN/AMBASSADOR)' })
  async create(@Body() dto: CreateCircleDto) {
    return this.circlesService.create(dto);
  }

  @Patch(':id')
  @UseGuards(CircleCaptainGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update circle (captain only)' })
  async update(@Param('id') id: string, @Body() dto: CreateCircleDto) {
    return this.circlesService.update(id, dto);
  }

  @Post(':id/members')
  @ApiOperation({ summary: 'Add member to circle' })
  async addMember(@Param('id') id: string, @Body() dto: AddMemberDto) {
    return this.circlesService.addMember(id, dto.userId);
  }

  @Delete(':id/members/:userId')
  @UseGuards(CircleCaptainGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Remove member from circle (captain only)' })
  async removeMember(@Param('id') id: string, @Param('userId') userId: string) {
    return this.circlesService.removeMember(id, userId);
  }

  @Get(':id/sessions')
  @ApiOperation({ summary: 'List circle sessions' })
  async getSessions(@Param('id') id: string) {
    return this.circlesService.getSessions(id);
  }

  @Post(':id/sessions')
  @UseGuards(CircleCaptainGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create circle session (captain only)' })
  async createSession(@Param('id') id: string, @Body() dto: any) {
    return this.circlesService.createSession(id, dto);
  }

  @Post(':id/sessions/:sessionId/attendance')
  @UseGuards(CircleCaptainGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Record attendance for session (captain only)' })
  async recordAttendance(
    @Param('id') id: string,
    @Param('sessionId') sessionId: string,
    @Body() dto: any,
  ) {
    // Support both single record and batch records
    if (dto.records && Array.isArray(dto.records)) {
      // Batch mode
      return this.circlesService.recordBatchAttendance(sessionId, dto.records);
    } else {
      // Single record mode
      const userId = dto.userId || dto.user_id;
      const status = dto.status;
      
      if (!userId || !status) {
        throw new Error('userId and status are required');
      }
      
      return this.circlesService.recordAttendance(sessionId, userId, status);
    }
  }
}
