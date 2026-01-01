import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreatorChallenge {
  @ApiProperty({
    description: 'Unique identifier',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  id: string;

  @ApiProperty({
    description: 'Challenge title',
    example: 'Build Your First Automation',
  })
  title: string;

  @ApiProperty({
    description: 'Challenge description',
    example: 'Create an automation that solves a real problem',
  })
  description: string;

  @ApiPropertyOptional({
    description: 'Season ID if linked to a season',
    example: '123e4567-e89b-12d3-a456-426614174001',
  })
  seasonId?: string;

  @ApiPropertyOptional({
    description: 'Challenge deadline',
    example: '2025-01-31T23:59:59Z',
  })
  deadline?: Date;

  @ApiProperty({
    description: 'Creator user ID (admin/council)',
    example: '123e4567-e89b-12d3-a456-426614174002',
  })
  createdBy: string;

  @ApiProperty({
    description: 'Creation timestamp',
    example: '2025-01-01T00:00:00Z',
  })
  createdAt: Date;

  @ApiPropertyOptional({
    description: 'Season details if linked',
  })
  season?: {
    id: string;
    name: string;
  };

  @ApiPropertyOptional({
    description: 'Number of submissions',
    example: 15,
  })
  submissionCount?: number;
}
