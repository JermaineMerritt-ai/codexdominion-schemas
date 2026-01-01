import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateTaskDto, UpdateTaskDto, ListTasksQueryDto } from './dto';
import { Task } from '@prisma/client';

@Injectable()
export class TasksService {
  constructor(private readonly prisma: PrismaService) {}

  async createTask(dto: CreateTaskDto): Promise<Task> {
    // TODO: guardrails: dedupe, etc.
    const task = await this.prisma.task.create({
      data: {
        type: dto.type,
        status: 'PENDING',
        priority: dto.priority,
        mode: dto.mode,
        ownerType: dto.ownerType,
        ownerId: dto.ownerId,
        subjectRefType: dto.subjectRefType,
        subjectRefId: dto.subjectRefId,
        dueAt: dto.dueAt ? new Date(dto.dueAt) : null,
        source: dto.source,
        payload: dto.payload,
      },
    });

    await this.prisma.taskEvent.create({
      data: {
        taskId: task.id,
        eventType: 'TASK_CREATED',
        actorType: 'SYSTEM',
        actorId: 'TASK_ENGINE',
        metadata: {},
      },
    });

    return task;
  }

  async updateTaskStatus(id: string, dto: UpdateTaskDto): Promise<Task> {
    const existing = await this.prisma.task.findUnique({ where: { id } });
    if (!existing) {
      throw new NotFoundException('Task not found');
    }

    // TODO: enforce valid transitions here

    const updated = await this.prisma.task.update({
      where: { id },
      data: {
        status: dto.newStatus,
        scheduledAt: dto.scheduledAt ? new Date(dto.scheduledAt) : existing.scheduledAt,
        completedAt: dto.newStatus === 'COMPLETED' ? new Date() : existing.completedAt,
        failedAt: dto.newStatus === 'FAILED' ? new Date() : existing.failedAt,
        lastError: dto.error ?? existing.lastError,
      },
    });

    await this.prisma.taskEvent.create({
      data: {
        taskId: id,
        eventType: 'TASK_STATUS_CHANGED',
        oldStatus: existing.status,
        newStatus: dto.newStatus,
        actorType: dto.actorType,
        actorId: dto.actorId,
        metadata: dto.error ? { error: dto.error } : {},
      },
    });

    return updated;
  }

  async listTasks(query: ListTasksQueryDto): Promise<Task[]> {
    return this.prisma.task.findMany({
      where: {
        status: query.status,
        type: query.type,
        ownerId: query.ownerId,
        ownerType: query.ownerType,
        subjectRefType: query.subjectRefType,
        subjectRefId: query.subjectRefId,
        // you can add date filters here
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async getTask(id: string): Promise<Task> {
    const task = await this.prisma.task.findUnique({ where: { id } });
    if (!task) throw new NotFoundException('Task not found');
    return task;
  }
}
