import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class MissionsService {
  constructor(private prisma: PrismaService) {}

  async findAll(seasonId?: string, month?: number) {
    const where: any = {};
    
    if (seasonId) {
      where.seasonId = seasonId;
    }
    
    if (month !== undefined) {
      where.month = month;
    }

    return this.prisma.mission.findMany({
      where,
      include: { 
        season: true,
        createdBy: {
          select: { id: true, firstName: true, lastName: true },
        },
        _count: {
          select: {
            submissions: true,
            assignments: true,
          },
        },
      },
      orderBy: [
        { month: 'asc' },
        { week: 'asc' },
      ],
    });
  }

  async getCurrent() {
    // Determine current date components
    const now = new Date();
    const currentMonth = now.getMonth() + 1; // 1-12
    const dayOfMonth = now.getDate();
    const currentWeek = Math.ceil(dayOfMonth / 7); // Rough week estimation

    // Get current season
    const currentSeason = await this.prisma.season.findFirst({
      where: {
        AND: [
          { startDate: { lte: now } },
          { endDate: { gte: now } },
        ],
      },
    });

    if (!currentSeason) {
      return { message: 'No active season at this time' };
    }

    // Find mission matching current season + month + week
    const mission = await this.prisma.mission.findFirst({
      where: {
        seasonId: currentSeason.id,
        month: currentMonth,
        week: currentWeek,
        type: 'GLOBAL', // Prioritize GLOBAL missions
      },
      include: { 
        season: true,
        _count: {
          select: { submissions: true },
        },
      },
    });

    // Fallback: any mission in current season + month
    if (!mission) {
      const fallback = await this.prisma.mission.findFirst({
        where: {
          seasonId: currentSeason.id,
          month: currentMonth,
        },
        include: { season: true },
      });

      return fallback || { 
        message: 'No mission available for current week',
        currentSeason,
        currentMonth,
        currentWeek,
      };
    }

    return mission;
  }

  async findOne(id: string) {
    return this.prisma.mission.findUnique({
      where: { id },
      include: { 
        season: true,
        createdBy: {
          select: { id: true, firstName: true, lastName: true, email: true },
        },
        assignments: {
          include: {
            user: {
              select: { id: true, firstName: true, lastName: true },
            },
            circle: {
              select: { id: true, name: true },
            },
          },
        },
        submissions: {
          include: {
            user: {
              select: { id: true, firstName: true, lastName: true },
            },
          },
          orderBy: { submittedAt: 'desc' },
          take: 10,
        },
      },
    });
  }

  async create(data: any) {
    const seasonId = data.seasonId || data.season_id;
    const createdById = data.createdById || data.created_by_id;
    
    return this.prisma.mission.create({ 
      data: {
        title: data.title,
        description: data.description,
        seasonId,
        month: data.month,
        week: data.week,
        type: data.type || 'GLOBAL',
        createdById,
      },
      include: { season: true },
    });
  }

  async assignMission(missionId: string, data: any) {
    const userId = data.userId || data.user_id;
    const circleId = data.circleId || data.circle_id;
    
    // Must have either userId or circleId
    if (!userId && !circleId) {
      throw new Error('Either user_id or circle_id is required');
    }
    
    return this.prisma.missionAssignment.create({
      data: {
        missionId,
        userId,
        circleId,
      },
      include: {
        mission: { select: { id: true, title: true, type: true } },
        user: userId ? { select: { id: true, firstName: true, lastName: true } } : undefined,
        circle: circleId ? { select: { id: true, name: true } } : undefined,
      },
    });
  }

  async submitMission(missionId: string, data: any) {
    const userId = data.userId || data.user_id;
    const circleId = data.circleId || data.circle_id;
    
    return this.prisma.missionSubmission.create({
      data: {
        missionId,
        userId,
        circleId,
        content: data.content,
        reflection: data.reflection,
        status: 'SUBMITTED',
      },
      include: {
        mission: { select: { id: true, title: true } },
        user: { select: { id: true, firstName: true, lastName: true } },
      },
    });
  }
}
