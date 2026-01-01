import { ApiProperty } from '@nestjs/swagger';

export class CulturalStoryEntity {
  @ApiProperty({
    description: 'Story UUID',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  id: string;

  @ApiProperty({
    description: 'Story title',
    example: 'From Island to Orbit',
  })
  title: string;

  @ApiProperty({
    description: 'Story content (markdown or JSON)',
    example: '# The Journey Begins\n\nOnce there was a people scattered across islands...',
  })
  content: string;

  @ApiProperty({
    description: 'Season ID (if seasonal)',
    required: false,
  })
  seasonId?: string;

  @ApiProperty({
    description: 'Week number (1-4)',
    required: false,
  })
  week?: number;

  @ApiProperty({
    description: 'Region ID (for localized stories)',
    required: false,
  })
  regionId?: string;

  @ApiProperty({
    description: 'Creation timestamp',
  })
  createdAt: Date;

  @ApiProperty({
    description: 'Associated season object',
    required: false,
  })
  season?: {
    id: string;
    name: string;
  };

  @ApiProperty({
    description: 'Associated region object',
    required: false,
  })
  region?: {
    id: string;
    name: string;
  };
}
