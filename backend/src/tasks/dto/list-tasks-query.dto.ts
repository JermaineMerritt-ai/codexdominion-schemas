import { IsEnum, IsString, IsOptional, IsISO8601 } from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';
import { TaskStatus } from './update-task.dto';
import { TaskType } from './create-task.dto';

export class ListTasksQueryDto {
  @ApiPropertyOptional({ enum: TaskStatus })
  @IsEnum(TaskStatus)
  @IsOptional()
  status?: TaskStatus;

  @ApiPropertyOptional({ enum: TaskType })
  @IsEnum(TaskType)
  @IsOptional()
  type?: TaskType;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  ownerId?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  ownerType?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  subjectRefType?: string;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  subjectRefId?: string;

  @ApiPropertyOptional({ description: 'Tasks due before this date' })
  @IsISO8601()
  @IsOptional()
  before?: string;

  @ApiPropertyOptional({ description: 'Tasks due after this date' })
  @IsISO8601()
  @IsOptional()
  after?: string;
}
