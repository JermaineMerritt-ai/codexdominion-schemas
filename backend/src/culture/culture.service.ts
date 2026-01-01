import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateStoryDto } from './dto/create-story.dto';
import { CreateRitualDto } from './dto/create-ritual.dto';
import { SeasonName } from '@prisma/client';

@Injectable()
export class CultureService {
  constructor(private prisma: PrismaService) {}

  // ======================================================
  // 🔥 STORY LOGIC — MYTHIC & INTELLIGENT
  // ======================================================

  /**
   * Get current cultural story for a user.
   * Logic:
   * 1. Determine current season + week
   * 2. If user has region_id, try regional story first
   * 3. Fallback to global story (region_id = null)
   * 4. If no exact match, return most recent story
   */
  async getCurrentStory(userId?: string) {
    // Get current season and week
    const { seasonId, week } = await this.getCurrentSeasonAndWeek();

    // Get user's region if authenticated
    let regionId: string | null = null;
    if (userId) {
      const profile = await this.prisma.profile.findUnique({
        where: { userId },
        select: { regionId: true },
      });
      regionId = profile?.regionId || null;
    }

    // Strategy 1: Try exact match (season + week + region)
    if (seasonId && regionId) {
      const regionalStory = await this.prisma.culturalStory.findFirst({
        where: {
          seasonId,
          week,
          regionId,
        },
        include: {
          season: { select: { id: true, name: true } },
          region: { select: { id: true, name: true } },
        },
      });
      if (regionalStory) return regionalStory;
    }

    // Strategy 2: Try global story (season + week, no region)
    if (seasonId) {
      const globalStory = await this.prisma.culturalStory.findFirst({
        where: {
          seasonId,
          week,
          regionId: null,
        },
        include: {
          season: { select: { id: true, name: true } },
        },
      });
      if (globalStory) return globalStory;
    }

    // Strategy 3: Most recent story (fallback)
    const fallbackStory = await this.prisma.culturalStory.findFirst({
      orderBy: { createdAt: 'desc' },
      include: {
        season: { select: { id: true, name: true } },
        region: { select: { id: true, name: true } },
      },
    });

    if (!fallbackStory) {
      return {
        message: 'No cultural story available at this time',
        flame: '🔥',
        instruction:
          'Create your first story via POST /culture/stories to ignite the cultural heartbeat',
      };
    }

    return fallbackStory;
  }

  /**
   * List all stories, optionally filtered by season
   */
  async getStories(seasonId?: string) {
    const where = seasonId ? { seasonId } : {};

    return this.prisma.culturalStory.findMany({
      where,
      include: {
        season: { select: { id: true, name: true } },
        region: { select: { id: true, name: true } },
      },
      orderBy: [{ createdAt: 'desc' }],
    });
  }

  /**
   * Create a new cultural story
   */
  async createStory(dto: CreateStoryDto) {
    // Validate season exists if provided
    if (dto.seasonId) {
      const season = await this.prisma.season.findUnique({
        where: { id: dto.seasonId },
      });
      if (!season) {
        throw new NotFoundException(
          `Season with ID ${dto.seasonId} not found`,
        );
      }
    }

    // Validate region exists if provided
    if (dto.regionId) {
      const region = await this.prisma.region.findUnique({
        where: { id: dto.regionId },
      });
      if (!region) {
        throw new NotFoundException(
          `Region with ID ${dto.regionId} not found`,
        );
      }
    }

    return this.prisma.culturalStory.create({
      data: {
        title: dto.title,
        content: dto.content,
        seasonId: dto.seasonId,
        week: dto.week,
        regionId: dto.regionId,
      },
      include: {
        season: { select: { id: true, name: true } },
        region: { select: { id: true, name: true } },
      },
    });
  }

  // ======================================================
  // 🔱 RITUAL LOGIC — CEREMONIAL STRUCTURE
  // ======================================================

  /**
   * Get all rituals, optionally filtered by type
   */
  async getRituals(type?: string) {
    const where = type ? { type: type as any } : {};

    return this.prisma.ritual.findMany({
      where,
      orderBy: { name: 'asc' },
    });
  }

  /**
   * Create a new ritual
   */
  async createRitual(dto: CreateRitualDto) {
    return this.prisma.ritual.create({
      data: {
        name: dto.name,
        description: dto.description,
        type: dto.type,
      },
    });
  }

  // ======================================================
  // 📅 HELPER: DETERMINE CURRENT SEASON & WEEK
  // ======================================================

  /**
   * Determine current season and week based on date.
   * Uses same logic as Mission Engine for consistency.
   */
  private async getCurrentSeasonAndWeek(): Promise<{
    seasonId: string | null;
    week: number;
  }> {
    const now = new Date();
    const currentMonth = now.getMonth() + 1; // 1-12
    const dayOfMonth = now.getDate();

    // Calculate week of month (1-4)
    const week = Math.ceil(dayOfMonth / 7);

    // Map month to season (3-month cycles)
    let seasonName: SeasonName;
    if (currentMonth >= 1 && currentMonth <= 3) {
      seasonName = SeasonName.IDENTITY;
    } else if (currentMonth >= 4 && currentMonth <= 6) {
      seasonName = SeasonName.MASTERY;
    } else if (currentMonth >= 7 && currentMonth <= 9) {
      seasonName = SeasonName.CREATION;
    } else {
      seasonName = SeasonName.LEADERSHIP;
    }

    // Get season ID
    const season = await this.prisma.season.findUnique({
      where: { name: seasonName },
      select: { id: true },
    });

    return {
      seasonId: season?.id || null,
      week,
    };
  }
}
