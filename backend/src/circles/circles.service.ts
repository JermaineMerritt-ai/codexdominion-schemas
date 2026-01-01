import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class CirclesService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.circle.findMany({
      include: {
        captain: {
          select: { id: true, firstName: true, lastName: true, email: true },
        },
        members: {
          include: {
            user: {
              select: { id: true, firstName: true, lastName: true, email: true },
            },
          },
        },
        _count: {
          select: { members: true, sessions: true },
        },
      },
    });
  }

  async findOne(id: string) {
    return this.prisma.circle.findUnique({
      where: { id },
      include: {
        captain: {
          select: { id: true, firstName: true, lastName: true, email: true },
        },
        members: {
          include: {
            user: {
              select: { id: true, firstName: true, lastName: true, email: true },
            },
          },
        },
        sessions: {
          include: {
            attendance: {
              include: {
                user: {
                  select: { id: true, firstName: true, lastName: true },
                },
              },
            },
          },
          orderBy: { scheduledAt: 'desc' },
        },
      },
    });
  }

  async create(data: any) {
    return this.prisma.circle.create({
      data: {
        name: data.name,
        captainId: data.captainId,
        regionId: data.regionId,
      },
      include: {
        captain: {
          select: { id: true, firstName: true, lastName: true, email: true },
        },
      },
    });
  }

  async update(id: string, data: any) {
    return this.prisma.circle.update({
      where: { id },
      data: {
        name: data.name,
        captainId: data.captainId,
        regionId: data.regionId,
      },
    });
  }

  async addMember(circleId: string, userId: string) {
    return this.prisma.circleMember.create({
      data: {
        circleId,
        userId,
      },
      include: {
        user: {
          select: { id: true, firstName: true, lastName: true, email: true },
        },
      },
    });
  }

  async removeMember(circleId: string, userId: string) {
    return this.prisma.circleMember.delete({
      where: {
        circleId_userId: { circleId, userId },
      },
    });
  }

  async getSessions(circleId: string) {
    return this.prisma.circleSession.findMany({
      where: { circleId },
      include: {
        attendance: {
          include: {
            user: {
              select: { id: true, firstName: true, lastName: true },
            },
          },
        },
      },
      orderBy: { scheduledAt: 'desc' },
    });
  }

  async createSession(circleId: string, data: any) {
    // Support both camelCase and snake_case
    const scheduledAt = data.scheduledAt || data.scheduled_at;
    const weekNumber = data.weekNumber || data.week_number;
    
    return this.prisma.circleSession.create({
      data: {
        circleId,
        scheduledAt: new Date(scheduledAt),
        topic: data.topic,
        season: data.season,
        weekNumber: weekNumber ? parseInt(weekNumber) : undefined,
      },
      include: {
        circle: {
          select: { id: true, name: true },
        },
      },
    });
  }

  async recordAttendance(sessionId: string, userId: string, status: string) {
    return this.prisma.circleAttendance.upsert({
      where: {
        sessionId_userId: { sessionId, userId },
      },
      update: {
        status: status.toUpperCase() as any,
      },
      create: {
        sessionId,
        userId,
        status: status.toUpperCase() as any,
      },
      include: {
        user: {
          select: { id: true, firstName: true, lastName: true },
        },
      },
    });
  }

  async recordBatchAttendance(sessionId: string, records: any[]) {
    const results = await Promise.all(
      records.map(record => {
        const userId = record.user_id || record.userId;
        const status = record.status;
        return this.recordAttendance(sessionId, userId, status);
      })
    );
    
    return {
      sessionId,
      recordsProcessed: results.length,
      attendance: results,
    };
  }
}
