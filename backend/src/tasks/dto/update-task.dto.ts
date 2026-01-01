import { IsEnum, IsString, IsOptional, IsISO8601 } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export enum TaskStatus {
  PENDING = 'PENDING',
  SCHEDULED = 'SCHEDULED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
}

export enum ActorType {
  SYSTEM = 'SYSTEM',
  AI = 'AI',
  HUMAN = 'HUMAN',
}

export class UpdateTaskDto {
  @ApiProperty({ enum: TaskStatus })
  @IsEnum(TaskStatus)
  newStatus: TaskStatus;

  @ApiPropertyOptional()
  @IsISO8601()
  @IsOptional()
  scheduledAt?: string;

  @ApiProperty({ enum: ActorType })
  @IsEnum(ActorType)
  actorType: ActorType;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  actorId?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  error?: string;
}
