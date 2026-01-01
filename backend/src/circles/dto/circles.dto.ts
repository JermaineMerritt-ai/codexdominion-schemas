import { IsString, IsOptional, IsInt, IsEnum, IsDateString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { Transform } from 'class-transformer';

export class CreateCircleDto {
  @ApiProperty({ example: 'Youth Identity Circle' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'b0ed9281-d896-4de6-81b9-59119de05820' })
  @IsString()
  @Transform(({ value, obj }) => value || obj.captain_id)
  captainId: string;

  @ApiProperty({ required: false })
  @IsOptional()
  @IsString()
  @Transform(({ value, obj }) => value || obj.region_id)
  regionId?: string;
}

export class CreateSessionDto {
  @ApiProperty({ example: '2025-02-10T18:00:00Z' })
  @IsDateString()
  @Transform(({ value, obj }) => value || obj.scheduled_at)
  scheduledAt: string;

  @ApiProperty({ example: 'Identity Story Circle', required: false })
  @IsOptional()
  @IsString()
  topic?: string;

  @ApiProperty({ example: 'IDENTITY', enum: ['IDENTITY', 'MASTERY', 'CREATION', 'LEADERSHIP'], required: false })
  @IsOptional()
  @IsEnum(['IDENTITY', 'MASTERY', 'CREATION', 'LEADERSHIP'])
  season?: string;

  @ApiProperty({ example: 2, required: false })
  @IsOptional()
  @IsInt()
  @Transform(({ value, obj }) => value || obj.week_number)
  weekNumber?: number;
}

export class RecordAttendanceDto {
  @ApiProperty({ example: 'b0ed9281-d896-4de6-81b9-59119de05820' })
  @IsString()
  @Transform(({ value, obj }) => value || obj.user_id)
  userId: string;

  @ApiProperty({ example: 'PRESENT', enum: ['PRESENT', 'ABSENT', 'EXCUSED'] })
  @IsEnum(['PRESENT', 'ABSENT', 'EXCUSED'])
  status: string;
}

export class AddMemberDto {
  @ApiProperty({ example: 'b0ed9281-d896-4de6-81b9-59119de05820' })
  @IsString()
  @Transform(({ value, obj }) => value || obj.user_id)
  userId: string;
}
