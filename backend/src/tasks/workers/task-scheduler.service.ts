import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { TasksService } from '../tasks.service';
import { TaskStatus, ActorType } from '../dto';

/**
 * TASK SCHEDULER SERVICE
 * Stage 2 of 3-stage pipeline: Polls for PENDING tasks and schedules them
 * Runs every 5 minutes via cron
 */
@Injectable()
export class TaskSchedulerService {
  private readonly logger = new Logger(TaskSchedulerService.name);

  constructor(private tasksService: TasksService) {}

  @Cron(CronExpression.EVERY_5_MINUTES)
  async scheduleReadyTasks() {
    this.logger.log('Running task scheduler...');

    try {
      // Find tasks that are PENDING and ready to be scheduled
      const pendingTasks = await this.tasksService.findAll({
        status: TaskStatus.PENDING,
      });

      const now = new Date();
      const tasksToSchedule = pendingTasks.filter((task) => {
        // Schedule if: no due date OR due date has passed
        return !task.dueAt || new Date(task.dueAt) <= now;
      });

      this.logger.log(`Found ${tasksToSchedule.length} tasks ready for scheduling`);

      for (const task of tasksToSchedule) {
        try {
          await this.tasksService.update(task.id, {
            newStatus: TaskStatus.SCHEDULED,
            scheduledAt: now.toISOString(),
            actorType: ActorType.SYSTEM,
            actorId: 'TASK_SCHEDULER',
          });

          this.logger.log(`Scheduled task ${task.id} (${task.type})`);
        } catch (error) {
          this.logger.error(`Failed to schedule task ${task.id}:`, error.message);
        }
      }
    } catch (error) {
      this.logger.error('Scheduler error:', error);
    }
  }
}
