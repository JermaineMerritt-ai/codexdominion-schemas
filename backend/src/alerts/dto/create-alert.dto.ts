import { ApiProperty } from '@nestjs/swagger';
import { IsEnum, IsNotEmpty, IsString, IsOptional, IsObject } from 'class-validator';

export enum AlertDomain {
  CIRCLES = 'CIRCLES',
  MISSIONS = 'MISSIONS',
  YOUTH = 'YOUTH',
  CREATORS = 'CREATORS',
  REGIONS = 'REGIONS',
  SYSTEM = 'SYSTEM',
}

export enum AlertSeverity {
  CRITICAL = 'CRITICAL',
  HIGH = 'HIGH',
  MEDIUM = 'MEDIUM',
  LOW = 'LOW',
}

export class CreateAlertDto {
  @ApiProperty({ enum: AlertDomain, example: 'CIRCLES' })
  @IsEnum(AlertDomain)
  domain: AlertDomain;

  @ApiProperty({ example: 'C2', description: 'Rule identifier' })
  @IsString()
  @IsNotEmpty()
  rule: string;

  @ApiProperty({ example: 'Circle Alpha attendance dropped 22% over 2 weeks.' })
  @IsString()
  @IsNotEmpty()
  message: string;

  @ApiProperty({ enum: AlertSeverity, example: 'HIGH' })
  @IsEnum(AlertSeverity)
  severity: AlertSeverity;

  @ApiProperty({ required: false, example: { circleId: 'uuid', dropPercentage: 22 } })
  @IsOptional()
  @IsObject()
  metadata?: Record<string, any>;
}
