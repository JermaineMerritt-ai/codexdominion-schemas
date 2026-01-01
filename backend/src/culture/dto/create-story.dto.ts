import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsOptional, IsInt, Min, Max, IsJSON } from 'class-validator';

export class CreateStoryDto {
  @ApiProperty({
    description: 'Story title',
    example: 'From Island to Orbit: The Journey Begins',
  })
  @IsString()
  title: string;

  @ApiProperty({
    description: 'Story content (markdown or JSON)',
    example: '# From Island to Orbit\n\nEvery great civilization begins with a story...',
  })
  @IsString()
  content: string;

  @ApiProperty({
    description: 'Season ID (optional, for seasonal stories)',
    required: false,
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  @IsOptional()
  @IsString()
  seasonId?: string;

  @ApiProperty({
    description: 'Week number within season (1-4)',
    required: false,
    example: 2,
  })
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(4)
  week?: number;

  @ApiProperty({
    description: 'Region ID for localized stories (optional)',
    required: false,
    example: '123e4567-e89b-12d3-a456-426614174001',
  })
  @IsOptional()
  @IsString()
  regionId?: string;
}
