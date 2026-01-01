import { IsEnum, IsString, IsOptional, IsISO8601, IsObject, IsNotEmpty } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export enum TaskType {
  INVOICE_FOLLOW_UP = 'INVOICE_FOLLOW_UP',
  LEAD_FOLLOW_UP = 'LEAD_FOLLOW_UP',
}

export enum TaskMode {
  SUGGESTION = 'SUGGESTION',
  ASSISTED = 'ASSISTED',
  AUTONOMOUS = 'AUTONOMOUS',
}

export enum TaskPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

export enum OwnerType {
  AI = 'AI',
  HUMAN = 'HUMAN',
}

export enum SubjectRefType {
  INVOICE = 'INVOICE',
  LEAD = 'LEAD',
}

export class CreateTaskDto {
  @ApiProperty({ enum: TaskType })
  @IsEnum(TaskType)
  @IsNotEmpty()
  type: TaskType;

  @ApiProperty({ enum: TaskMode })
  @IsEnum(TaskMode)
  @IsNotEmpty()
  mode: TaskMode;

  @ApiProperty({ enum: TaskPriority })
  @IsEnum(TaskPriority)
  @IsNotEmpty()
  priority: TaskPriority;

  @ApiProperty({ enum: OwnerType })
  @IsEnum(OwnerType)
  @IsNotEmpty()
  ownerType: OwnerType;

  @ApiPropertyOptional()
  @IsString()
  @IsOptional()
  ownerId?: string;

  @ApiProperty({ enum: SubjectRefType })
  @IsEnum(SubjectRefType)
  @IsNotEmpty()
  subjectRefType: SubjectRefType;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  subjectRefId: string;

  @ApiPropertyOptional()
  @IsISO8601()
  @IsOptional()
  dueAt?: string;

  @ApiProperty()
  @IsString()
  @IsNotEmpty()
  source: string;

  @ApiProperty({
    description: 'Complete context for task execution (customer details, invoice details, etc.)',
    example: {
      customer_name: 'ACME Corp',
      customer_email: 'billing@acme.com',
      invoice_number: 'INV-123',
      invoice_amount: 1200,
      currency: 'USD',
      due_date: '2025-12-20',
      days_overdue: 10,
    },
  })
  @IsObject()
  @IsNotEmpty()
  payload: Record<string, any>;
}
