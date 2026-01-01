import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { TasksController } from './tasks.controller';
import { TasksService } from './tasks.service';
import { TaskSchedulerService } from './workers/task-scheduler.service';
import { TaskExecutorService } from './workers/task-executor.service';
import { PrismaModule } from '../prisma/prisma.module';
import { MessageGeneratorService } from '../services/message-generator.service';
import { EmailSenderService } from '../services/email-sender.service';

@Module({
  imports: [
    PrismaModule,
    ScheduleModule.forRoot(), // Enable cron scheduling
  ],
  controllers: [TasksController],
  providers: [
    TasksService,
    TaskSchedulerService, // Stage 2: Scheduler worker
    TaskExecutorService,  // Stage 3: Executor worker (enhanced)
    MessageGeneratorService, // Message generation for follow-ups
    EmailSenderService, // SMTP email sending
  ],
  exports: [TasksService],
})
export class TasksModule {}
