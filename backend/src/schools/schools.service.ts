import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSchoolDto, UpdateSchoolDto, SchoolQueryDto } from './dto/school.dto';

@Injectable()
export class SchoolsService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: SchoolQueryDto) {
    const where: any = {};

    if (query.regionId) {
      where.regionId = query.regionId;
    }

    const schools = await this.prisma.school.findMany({
      where,
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        _count: {
          select: {
            profiles: true,
            ambassadorOutreach: true,
          },
        },
      },
      orderBy: { name: 'asc' },
    });

    return schools.map((school) => ({
      id: school.id,
      regionId: school.regionId,
      name: school.name,
      address: school.address,
      contactPerson: school.contactPerson,
      region: school.region,
      profileCount: school._count.profiles,
      outreachCount: school._count.ambassadorOutreach,
    }));
  }

  async findOne(id: string) {
    const school = await this.prisma.school.findUnique({
      where: { id },
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
        _count: {
          select: {
            profiles: true,
            ambassadorOutreach: true,
          },
        },
      },
    });

    if (!school) {
      throw new NotFoundException(`School with ID ${id} not found`);
    }

    return {
      id: school.id,
      regionId: school.regionId,
      name: school.name,
      address: school.address,
      contactPerson: school.contactPerson,
      region: school.region,
      profileCount: school._count.profiles,
      outreachCount: school._count.ambassadorOutreach,
    };
  }

  async create(dto: CreateSchoolDto) {
    // Verify region exists
    const region = await this.prisma.region.findUnique({
      where: { id: dto.regionId },
    });
    if (!region) {
      throw new NotFoundException(`Region with ID ${dto.regionId} not found`);
    }

    return this.prisma.school.create({
      data: {
        regionId: dto.regionId,
        name: dto.name,
        address: dto.address,
        contactPerson: dto.contactPerson,
      },
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
      },
    });
  }

  async update(id: string, dto: UpdateSchoolDto) {
    // Verify school exists
    await this.findOne(id);

    // Verify region exists if regionId is being updated
    if (dto.regionId) {
      const region = await this.prisma.region.findUnique({
        where: { id: dto.regionId },
      });
      if (!region) {
        throw new NotFoundException(`Region with ID ${dto.regionId} not found`);
      }
    }

    return this.prisma.school.update({
      where: { id },
      data: dto,
      include: {
        region: {
          select: {
            id: true,
            name: true,
            country: true,
          },
        },
      },
    });
  }

  async remove(id: string) {
    // Verify school exists
    await this.findOne(id);

    await this.prisma.school.delete({
      where: { id },
    });

    return { message: `School ${id} deleted successfully` };
  }
}
