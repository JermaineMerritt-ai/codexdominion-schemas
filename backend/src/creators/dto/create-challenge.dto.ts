import { IsString, IsOptional, IsUUID, IsDateString, MaxLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateChallengeDto {
  @ApiProperty({
    description: 'Title of the creator challenge',
    example: 'Build Your First Automation',
  })
  @IsString()
  @MaxLength(200)
  title: string;

  @ApiProperty({
    description: 'Detailed description of the challenge',
    example: 'Create an automation that solves a real problem in your community',
  })
  @IsString()
  description: string;

  @ApiPropertyOptional({
    description: 'Season ID this challenge belongs to',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  @IsOptional()
  @IsUUID()
  seasonId?: string;

  @ApiPropertyOptional({
    description: 'Deadline for challenge submissions (ISO 8601 format)',
    example: '2025-01-31T23:59:59Z',
  })
  @IsOptional()
  @IsDateString()
  deadline?: string;
}
