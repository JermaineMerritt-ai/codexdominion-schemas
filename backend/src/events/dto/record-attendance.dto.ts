import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsUUID, IsEnum, IsOptional, IsDateString, IsArray, ValidateNested } from 'class-validator';
import { EventAttendanceStatus } from '@prisma/client';
import { Type } from 'class-transformer';

/**
 * Single attendance record - supports both snake_case and camelCase
 */
export class RecordAttendanceDto {
  @ApiProperty({ example: '123e4567-e89b-12d3-a456-426614174000', description: 'User ID (supports user_id or userId)' })
  @IsUUID()
  userId?: string;

  user_id?: string; // snake_case alternative

  @ApiProperty({ enum: EventAttendanceStatus, example: 'PRESENT' })
  @IsEnum(EventAttendanceStatus)
  status: EventAttendanceStatus;

  @ApiPropertyOptional({ example: '2025-03-15T18:30:00.000Z' })
  @IsDateString()
  @IsOptional()
  checkedInAt?: string;

  checked_in_at?: string; // snake_case alternative
}

/**
 * Batch attendance records - supports user's preferred format
 */
export class BatchAttendanceDto {
  @ApiProperty({ type: [RecordAttendanceDto] })
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => RecordAttendanceDto)
  records: RecordAttendanceDto[];
}
