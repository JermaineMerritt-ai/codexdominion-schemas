import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsOptional, IsUUID, IsEnum, IsDateString } from 'class-validator';
import { OutreachType } from '@prisma/client';

export class CreateOutreachDto {
  @ApiProperty({ example: 'uuid', description: 'Region ID' })
  @IsNotEmpty()
  @IsUUID()
  regionId: string;

  @ApiPropertyOptional({ example: 'uuid', description: 'School ID (optional)' })
  @IsOptional()
  @IsUUID()
  schoolId?: string;

  @ApiProperty({ enum: OutreachType, example: 'VISIT', description: 'Type of outreach activity' })
  @IsNotEmpty()
  @IsEnum(OutreachType)
  type: OutreachType;

  @ApiPropertyOptional({ example: 'Met with 15 students, discussed mission system', description: 'Outreach notes' })
  @IsOptional()
  @IsString()
  notes?: string;

  @ApiProperty({ example: '2025-01-15', description: 'Date of outreach (YYYY-MM-DD)' })
  @IsNotEmpty()
  @IsDateString()
  date: string;
}

export class UpdateOutreachDto {
  @ApiPropertyOptional({ enum: OutreachType, example: 'MEETING', description: 'Type of outreach activity' })
  @IsOptional()
  @IsEnum(OutreachType)
  type?: OutreachType;

  @ApiPropertyOptional({ example: 'Follow-up meeting scheduled', description: 'Outreach notes' })
  @IsOptional()
  @IsString()
  notes?: string;

  @ApiPropertyOptional({ example: '2025-01-16', description: 'Date of outreach' })
  @IsOptional()
  @IsDateString()
  date?: string;

  @ApiPropertyOptional({ example: 'uuid', description: 'School ID' })
  @IsOptional()
  @IsUUID()
  schoolId?: string;
}

export class OutreachQueryDto {
  @ApiPropertyOptional({ description: 'Filter by region ID' })
  @IsOptional()
  @IsUUID()
  regionId?: string;

  @ApiPropertyOptional({ description: 'Filter by school ID' })
  @IsOptional()
  @IsUUID()
  schoolId?: string;

  @ApiPropertyOptional({ description: 'Filter by ambassador ID' })
  @IsOptional()
  @IsUUID()
  ambassadorId?: string;

  @ApiPropertyOptional({ enum: OutreachType, description: 'Filter by outreach type' })
  @IsOptional()
  @IsEnum(OutreachType)
  type?: OutreachType;
}
