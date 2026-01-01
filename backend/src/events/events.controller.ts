import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
  UseGuards,
  Request,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { EventsService } from './events.service';
import { CreateEventDto } from './dto/create-event.dto';
import { UpdateEventDto } from './dto/update-event.dto';
import { RecordAttendanceDto, BatchAttendanceDto } from './dto/record-attendance.dto';
import { CreateCeremonyScriptDto } from './dto/create-ceremony-script.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName, EventType } from '@prisma/client';

@ApiTags('events')
@Controller('events')
export class EventsController {
  constructor(private readonly eventsService: EventsService) {}

  /**
   * Create a new event
   * Admin, Council, Regional Directors, and Ambassadors can create events
   */
  @Post()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR, RoleName.AMBASSADOR)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a new event or ceremony' })
  @ApiResponse({ status: 201, description: 'Event created successfully' })
  @ApiResponse({ status: 403, description: 'Forbidden - insufficient permissions' })
  create(
    @Body() createEventDto: CreateEventDto,
    @Request() req: any,
  ) {
    const userId = req.user.userId;
    return this.eventsService.create(createEventDto, userId);
  }

  /**
   * Get all events with optional filters
   */
  @Get()
  @ApiOperation({ summary: 'Get all events with optional filters (public access)' })
  @ApiQuery({ name: 'regionId', required: false, description: 'Filter by region ID' })
  @ApiQuery({ name: 'eventType', required: false, enum: EventType, description: 'Filter by event type' })
  @ApiQuery({ name: 'upcoming', required: false, type: Boolean, description: 'Show only upcoming events' })
  @ApiResponse({ status: 200, description: 'List of events' })
  findAll(
    @Query('regionId') regionId?: string,
    @Query('eventType') eventType?: EventType,
    @Query('upcoming') upcoming?: string,
  ) {
    return this.eventsService.findAll({
      regionId,
      eventType,
      upcoming: upcoming === 'true',
    });
  }

  /**
   * Get a single event with full attendance
   */
  @Get(':id')
  @ApiOperation({ summary: 'Get a single event with attendance (public access)' })
  @ApiResponse({ status: 200, description: 'Event details with attendance' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  findOne(@Param('id') id: string) {
    return this.eventsService.findOne(id);
  }

  /**
   * Update an event
   * Only event creator, admins, or regional directors can update
   */
  @Patch(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR, RoleName.AMBASSADOR)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update an event' })
  @ApiResponse({ status: 200, description: 'Event updated successfully' })
  @ApiResponse({ status: 403, description: 'Forbidden - insufficient permissions' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  update(@Param('id') id: string, @Body() updateEventDto: UpdateEventDto) {
    return this.eventsService.update(id, updateEventDto);
  }

  /**
   * Delete an event (Admin only)
   */
  @Delete(':id')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete an event (Admin/Council only)' })
  @ApiResponse({ status: 200, description: 'Event deleted successfully' })
  @ApiResponse({ status: 403, description: 'Forbidden - admin access required' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  remove(@Param('id') id: string) {
    return this.eventsService.remove(id);
  }

  /**
   * Record attendance for an event
   * Supports both single record and batch (array of records)
   * Supports snake_case (user_id) and camelCase (userId)
   */
  @Post(':id/attendance')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(
    RoleName.ADMIN,
    RoleName.COUNCIL,
    RoleName.REGIONAL_DIRECTOR,
    RoleName.AMBASSADOR,
    RoleName.YOUTH_CAPTAIN,
  )
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Record attendance for an event',
    description: 'Supports single record or batch. Accepts both snake_case (user_id) and camelCase (userId)'
  })
  @ApiResponse({ status: 201, description: 'Attendance recorded successfully' })
  @ApiResponse({ status: 403, description: 'Forbidden - insufficient permissions' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  recordAttendance(
    @Param('id') eventId: string,
    @Body() dto: RecordAttendanceDto | BatchAttendanceDto,
  ) {
    // Check if it's batch format (has "records" array)
    if ('records' in dto) {
      return this.eventsService.recordAttendance(eventId, dto.records);
    }
    // Otherwise treat as single record
    return this.eventsService.recordAttendance(eventId, dto as RecordAttendanceDto);
  }

  /**
   * Get attendance for an event
   */
  @Get(':id/attendance')
  @ApiOperation({ summary: 'Get attendance for an event with summary stats (public access)' })
  @ApiResponse({ status: 200, description: 'Event attendance with summary' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  getAttendance(@Param('id') eventId: string) {
    return this.eventsService.getAttendance(eventId);
  }

  /**
   * Create or update ceremony script for an event
   */
  @Post(':id/script')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL, RoleName.REGIONAL_DIRECTOR)
  @ApiBearerAuth()
  @ApiOperation({ 
    summary: 'Create or update ceremony script',
    description: 'Add structured ceremony script with rituals, readings, affirmations, and transitions'
  })
  @ApiResponse({ status: 201, description: 'Ceremony script created/updated successfully' })
  @ApiResponse({ status: 403, description: 'Forbidden - insufficient permissions' })
  @ApiResponse({ status: 404, description: 'Event not found' })
  createScript(
    @Param('id') eventId: string,
    @Body() dto: CreateCeremonyScriptDto,
  ) {
    return this.eventsService.createScript(eventId, dto);
  }

  /**
   * Get ceremony script for an event
   */
  @Get(':id/script')
  @ApiOperation({ summary: 'Get ceremony script for an event (public access)' })
  @ApiResponse({ status: 200, description: 'Ceremony script retrieved' })
  @ApiResponse({ status: 404, description: 'Ceremony script not found' })
  getScript(@Param('id') eventId: string) {
    return this.eventsService.getScript(eventId);
  }

  /**
   * Delete ceremony script
   */
  @Delete(':id/script')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete ceremony script' })
  @ApiResponse({ status: 200, description: 'Ceremony script deleted successfully' })
  @ApiResponse({ status: 404, description: 'Ceremony script not found' })
  deleteScript(@Param('id') eventId: string) {
    return this.eventsService.deleteScript(eventId);
  }
}
