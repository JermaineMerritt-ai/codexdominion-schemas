import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateEventDto } from './dto/create-event.dto';
import { UpdateEventDto } from './dto/update-event.dto';
import { RecordAttendanceDto } from './dto/record-attendance.dto';
import { CreateCeremonyScriptDto } from './dto/create-ceremony-script.dto';
import { UpdateCeremonyScriptDto } from './dto/update-ceremony-script.dto';
import { EventType, EventAttendanceStatus } from '@prisma/client';

@Injectable()
export class EventsService {
  constructor(private prisma: PrismaService) {}

  /**
   * Create a new event
   */
  async create(createEventDto: CreateEventDto, createdBy: string) {
    return this.prisma.event.create({
      data: {
        ...createEventDto,
        createdBy,
        scheduledAt: new Date(createEventDto.scheduledAt),
      },
      include: {
        region: true,
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
      },
    });
  }

  /**
   * Get all events with optional filters
   */
  async findAll(query: {
    regionId?: string;
    eventType?: EventType;
    upcoming?: boolean;
  }) {
    const where: any = {};

    if (query.regionId) {
      where.regionId = query.regionId;
    }

    if (query.eventType) {
      where.eventType = query.eventType;
    }

    if (query.upcoming) {
      where.scheduledAt = {
        gte: new Date(),
      };
    }

    return this.prisma.event.findMany({
      where,
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        attendance: {
          include: {
            user: {
              select: {
                id: true,
                firstName: true,
                lastName: true,
                email: true,
              },
            },
          },
        },
      },
      orderBy: {
        scheduledAt: 'desc',
      },
    });
  }

  /**
   * Get a single event with full attendance
   */
  async findOne(id: string) {
    const event = await this.prisma.event.findUnique({
      where: { id },
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        attendance: {
          include: {
            user: {
              select: {
                id: true,
                firstName: true,
                lastName: true,
                email: true,
              },
            },
          },
          orderBy: {
            checkedInAt: 'desc',
          },
        },
      },
    });

    if (!event) {
      throw new NotFoundException(`Event with ID ${id} not found`);
    }

    return event;
  }

  /**
   * Update an event
   */
  async update(id: string, updateEventDto: UpdateEventDto) {
    const event = await this.prisma.event.findUnique({ where: { id } });
    if (!event) {
      throw new NotFoundException(`Event with ID ${id} not found`);
    }

    const data: any = { ...updateEventDto };
    if (updateEventDto.scheduledAt) {
      data.scheduledAt = new Date(updateEventDto.scheduledAt);
    }

    return this.prisma.event.update({
      where: { id },
      data,
      include: {
        region: true,
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        attendance: {
          include: {
            user: {
              select: {
                id: true,
                firstName: true,
                lastName: true,
              },
            },
          },
        },
      },
    });
  }

  /**
   * Delete an event
   */
  async remove(id: string) {
    const event = await this.prisma.event.findUnique({ where: { id } });
    if (!event) {
      throw new NotFoundException(`Event with ID ${id} not found`);
    }

    await this.prisma.event.delete({ where: { id } });
    return { message: `Event ${id} deleted successfully` };
  }

  /**
   * Record attendance (supports both single and batch)
   * Supports snake_case (user_id) and camelCase (userId)
   */
  async recordAttendance(
    eventId: string,
    dto: RecordAttendanceDto | RecordAttendanceDto[],
  ) {
    const event = await this.prisma.event.findUnique({ where: { id: eventId } });
    if (!event) {
      throw new NotFoundException(`Event with ID ${eventId} not found`);
    }

    // Normalize format: convert to array if single record
    const records = Array.isArray(dto) ? dto : [dto];

    // Process each record
    const results = await Promise.all(
      records.map(async (record) => {
        // Support both snake_case and camelCase
        const userId = record.userId || record.user_id;
        const checkedInAt = record.checkedInAt || record.checked_in_at;

        if (!userId) {
          throw new Error('userId (or user_id) is required');
        }

        return this.prisma.eventAttendance.upsert({
          where: {
            eventId_userId: {
              eventId,
              userId,
            },
          },
          create: {
            eventId,
            userId,
            status: record.status,
            checkedInAt: checkedInAt ? new Date(checkedInAt) : new Date(),
          },
          update: {
            status: record.status,
            checkedInAt: checkedInAt ? new Date(checkedInAt) : new Date(),
          },
          include: {
            user: {
              select: {
                id: true,
                firstName: true,
                lastName: true,
                email: true,
              },
            },
          },
        });
      }),
    );

    return {
      eventId,
      recordsProcessed: results.length,
      attendance: results,
    };
  }

  /**
   * Get attendance for an event
   */
  async getAttendance(eventId: string) {
    const event = await this.prisma.event.findUnique({ where: { id: eventId } });
    if (!event) {
      throw new NotFoundException(`Event with ID ${eventId} not found`);
    }

    const attendance = await this.prisma.eventAttendance.findMany({
      where: { eventId },
      include: {
        user: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
      },
      orderBy: {
        checkedInAt: 'desc',
      },
    });

    // Count by status
    const summary = {
      total: attendance.length,
      present: attendance.filter((a) => a.status === 'PRESENT').length,
      absent: attendance.filter((a) => a.status === 'ABSENT').length,
      registered: attendance.filter((a) => a.status === 'REGISTERED').length,
    };

    return {
      eventId,
      summary,
      attendance,
    };
  }

  /**
   * Create or update ceremony script for an event
   */
  async createScript(eventId: string, dto: CreateCeremonyScriptDto) {
    // Verify event exists
    const event = await this.prisma.event.findUnique({ where: { id: eventId } });
    if (!event) {
      throw new NotFoundException(`Event with ID ${eventId} not found`);
    }

    // Upsert ceremony script
    return this.prisma.ceremonyScript.upsert({
      where: { eventId },
      create: {
        eventId,
        sections: dto.sections,
      },
      update: {
        sections: dto.sections,
      },
    });
  }

  /**
   * Get ceremony script for an event
   */
  async getScript(eventId: string) {
    const script = await this.prisma.ceremonyScript.findUnique({
      where: { eventId },
      include: {
        event: {
          select: {
            id: true,
            title: true,
            eventType: true,
            scheduledAt: true,
          },
        },
      },
    });

    if (!script) {
      throw new NotFoundException(`Ceremony script not found for event ${eventId}`);
    }

    return script;
  }

  /**
   * Delete ceremony script
   */
  async deleteScript(eventId: string) {
    const script = await this.prisma.ceremonyScript.findUnique({
      where: { eventId },
    });

    if (!script) {
      throw new NotFoundException(`Ceremony script not found for event ${eventId}`);
    }

    await this.prisma.ceremonyScript.delete({
      where: { eventId },
    });

    return { message: 'Ceremony script deleted successfully' };
  }
}
