import { Injectable, NotFoundException, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateOutreachDto, UpdateOutreachDto, OutreachQueryDto } from './dto/outreach.dto';

@Injectable()
export class OutreachService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: OutreachQueryDto) {
    const where: any = {};

    if (query.regionId) {
      where.regionId = query.regionId;
    }
    if (query.schoolId) {
      where.schoolId = query.schoolId;
    }
    if (query.ambassadorId) {
      where.ambassadorId = query.ambassadorId;
    }
    if (query.type) {
      where.type = query.type;
    }

    return this.prisma.ambassadorOutreach.findMany({
      where,
      include: {
        ambassador: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        school: {
          select: {
            id: true,
            name: true,
          },
        },
      },
      orderBy: { date: 'desc' },
    });
  }

  async findOne(id: string) {
    const outreach = await this.prisma.ambassadorOutreach.findUnique({
      where: { id },
      include: {
        ambassador: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        school: {
          select: {
            id: true,
            name: true,
          },
        },
      },
    });

    if (!outreach) {
      throw new NotFoundException(`Outreach record with ID ${id} not found`);
    }

    return outreach;
  }

  async create(dto: CreateOutreachDto, ambassadorId: string) {
    // Verify region exists
    const region = await this.prisma.region.findUnique({
      where: { id: dto.regionId },
    });
    if (!region) {
      throw new NotFoundException(`Region with ID ${dto.regionId} not found`);
    }

    // Verify school exists if provided
    if (dto.schoolId) {
      const school = await this.prisma.school.findUnique({
        where: { id: dto.schoolId },
      });
      if (!school) {
        throw new NotFoundException(`School with ID ${dto.schoolId} not found`);
      }
    }

    return this.prisma.ambassadorOutreach.create({
      data: {
        ambassadorId,
        regionId: dto.regionId,
        schoolId: dto.schoolId,
        type: dto.type,
        notes: dto.notes,
        date: new Date(dto.date),
      },
      include: {
        ambassador: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        school: {
          select: {
            id: true,
            name: true,
          },
        },
      },
    });
  }

  async update(id: string, dto: UpdateOutreachDto, userId: string) {
    // Verify outreach exists
    const outreach = await this.findOne(id);

    // Only the ambassador who created it can update
    if (outreach.ambassadorId !== userId) {
      throw new ForbiddenException('You can only update your own outreach records');
    }

    // Verify school exists if schoolId is being updated
    if (dto.schoolId) {
      const school = await this.prisma.school.findUnique({
        where: { id: dto.schoolId },
      });
      if (!school) {
        throw new NotFoundException(`School with ID ${dto.schoolId} not found`);
      }
    }

    const updateData: any = { ...dto };
    if (dto.date) {
      updateData.date = new Date(dto.date);
    }

    return this.prisma.ambassadorOutreach.update({
      where: { id },
      data: updateData,
      include: {
        ambassador: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        school: {
          select: {
            id: true,
            name: true,
          },
        },
      },
    });
  }

  async remove(id: string, userId: string) {
    // Verify outreach exists
    const outreach = await this.findOne(id);

    // Only the ambassador who created it can delete
    if (outreach.ambassadorId !== userId) {
      throw new ForbiddenException('You can only delete your own outreach records');
    }

    await this.prisma.ambassadorOutreach.delete({
      where: { id },
    });

    return { message: `Outreach record ${id} deleted successfully` };
  }
}
