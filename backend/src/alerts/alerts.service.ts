import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateAlertDto } from './dto/create-alert.dto';
import { Prisma } from '@prisma/client';

@Injectable()
export class AlertsService {
  constructor(private prisma: PrismaService) {}

  async create(createAlertDto: CreateAlertDto) {
    return this.prisma.alert.create({
      data: {
        domain: createAlertDto.domain,
        rule: createAlertDto.rule,
        message: createAlertDto.message,
        severity: createAlertDto.severity,
        metadata: createAlertDto.metadata || Prisma.JsonNull,
      },
    });
  }

  async findAll(filters?: {
    domain?: string;
    severity?: string;
    acknowledged?: boolean;
    limit?: number;
  }) {
    const where: Prisma.AlertWhereInput = {};

    if (filters?.domain) {
      where.domain = filters.domain as any;
    }
    if (filters?.severity) {
      where.severity = filters.severity as any;
    }
    if (filters?.acknowledged !== undefined) {
      where.acknowledged = filters.acknowledged;
    }

    return this.prisma.alert.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      take: filters?.limit || 50,
      include: {
        acknowledger: {
          select: {
            id: true,
            email: true,
            firstName: true,
            lastName: true,
          },
        },
      },
    });
  }

  async findOne(id: string) {
    return this.prisma.alert.findUnique({
      where: { id },
      include: {
        acknowledger: {
          select: {
            id: true,
            email: true,
            firstName: true,
            lastName: true,
          },
        },
      },
    });
  }

  async acknowledge(id: string, userId: string) {
    return this.prisma.alert.update({
      where: { id },
      data: {
        acknowledged: true,
        acknowledgedAt: new Date(),
        acknowledgedBy: userId,
      },
      include: {
        acknowledger: {
          select: {
            id: true,
            email: true,
            firstName: true,
            lastName: true,
          },
        },
      },
    });
  }

  async getStats() {
    const [total, unacknowledged, bySeverity, byDomain] = await Promise.all([
      this.prisma.alert.count(),
      this.prisma.alert.count({ where: { acknowledged: false } }),
      this.prisma.alert.groupBy({
        by: ['severity'],
        _count: true,
      }),
      this.prisma.alert.groupBy({
        by: ['domain'],
        _count: true,
      }),
    ]);

    return {
      total,
      unacknowledged,
      bySeverity: bySeverity.reduce((acc, item) => {
        acc[item.severity] = item._count;
        return acc;
      }, {} as Record<string, number>),
      byDomain: byDomain.reduce((acc, item) => {
        acc[item.domain] = item._count;
        return acc;
      }, {} as Record<string, number>),
    };
  }
}
