import { ApiProperty } from '@nestjs/swagger';

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

export class AlertEntity {
  @ApiProperty({ example: 'uuid' })
  id: string;

  @ApiProperty({ enum: AlertDomain })
  domain: AlertDomain;

  @ApiProperty({ example: 'C2' })
  rule: string;

  @ApiProperty({ example: 'Circle Alpha attendance dropped 22% over 2 weeks.' })
  message: string;

  @ApiProperty({ enum: AlertSeverity })
  severity: AlertSeverity;

  @ApiProperty({ required: false })
  metadata?: Record<string, any>;

  @ApiProperty({ example: false })
  acknowledged: boolean;

  @ApiProperty({ required: false })
  acknowledgedAt?: Date;

  @ApiProperty({ required: false })
  acknowledgedBy?: string;

  @ApiProperty()
  createdAt: Date;
}
