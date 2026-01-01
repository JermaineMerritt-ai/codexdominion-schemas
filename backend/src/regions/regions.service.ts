import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateRegionDto, UpdateRegionDto } from './dto/region.dto';

@Injectable()
export class RegionsService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    const regions = await this.prisma.region.findMany({
      include: {
        director: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        _count: {
          select: {
            schools: true,
            circles: true,
            outreach: true,
          },
        },
      },
    });

    return regions.map((region) => ({
      id: region.id,
      name: region.name,
      country: region.country,
      timezone: region.timezone,
      directorId: region.directorId,
      director: region.director,
      schoolCount: region._count.schools,
      circleCount: region._count.circles,
      outreachCount: region._count.outreach,
    }));
  }

  async findOne(id: string) {
    const region = await this.prisma.region.findUnique({
      where: { id },
      include: {
        director: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        _count: {
          select: {
            schools: true,
            circles: true,
            outreach: true,
          },
        },
      },
    });

    if (!region) {
      throw new NotFoundException(`Region with ID ${id} not found`);
    }

    return {
      id: region.id,
      name: region.name,
      country: region.country,
      timezone: region.timezone,
      directorId: region.directorId,
      director: region.director,
      schoolCount: region._count.schools,
      circleCount: region._count.circles,
      outreachCount: region._count.outreach,
    };
  }

  async create(dto: CreateRegionDto) {
    // Verify director exists if provided
    if (dto.directorId) {
      const director = await this.prisma.user.findUnique({
        where: { id: dto.directorId },
      });
      if (!director) {
        throw new NotFoundException(`Director with ID ${dto.directorId} not found`);
      }
    }

    return this.prisma.region.create({
      data: {
        name: dto.name,
        country: dto.country,
        timezone: dto.timezone,
        directorId: dto.directorId,
      },
      include: {
        director: {
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

  async update(id: string, dto: UpdateRegionDto) {
    // Verify region exists
    await this.findOne(id);

    // Verify director exists if provided
    if (dto.directorId) {
      const director = await this.prisma.user.findUnique({
        where: { id: dto.directorId },
      });
      if (!director) {
        throw new NotFoundException(`Director with ID ${dto.directorId} not found`);
      }
    }

    return this.prisma.region.update({
      where: { id },
      data: dto,
      include: {
        director: {
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

  async remove(id: string) {
    // Verify region exists
    await this.findOne(id);

    await this.prisma.region.delete({
      where: { id },
    });

    return { message: `Region ${id} deleted successfully` };
  }
}
