import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class SeasonsService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.season.findMany({
      orderBy: { startDate: 'asc' },
      include: {
        _count: {
          select: {
            missions: true,
            culturalStories: true,
            curriculumModules: true,
            creatorChallenges: true,
          },
        },
      },
    });
  }

  async getCurrent() {
    const now = new Date();
    
    // Find season where now is between startDate and endDate
    const currentSeason = await this.prisma.season.findFirst({
      where: {
        AND: [
          { startDate: { lte: now } },
          { endDate: { gte: now } },
        ],
      },
      include: {
        _count: {
          select: {
            missions: true,
            culturalStories: true,
          },
        },
      },
    });

    // If no date-based season, return most recent one
    if (!currentSeason) {
      return this.prisma.season.findFirst({
        orderBy: { startDate: 'desc' },
      });
    }

    return currentSeason;
  }
}
