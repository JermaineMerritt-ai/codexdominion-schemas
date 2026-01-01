import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { ArtifactType, ArtifactStatus } from '../dto/create-artifact.dto';

export class Artifact {
  @ApiProperty({
    description: 'Unique identifier',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  id: string;

  @ApiProperty({
    description: 'Creator user ID',
    example: '123e4567-e89b-12d3-a456-426614174001',
  })
  creatorId: string;

  @ApiProperty({
    description: 'Artifact title',
    example: 'Budget Tracker Automation',
  })
  title: string;

  @ApiPropertyOptional({
    description: 'Artifact description',
    example: 'Automates monthly budget calculations',
  })
  description?: string;

  @ApiProperty({
    description: 'Type of artifact',
    enum: ArtifactType,
    example: ArtifactType.AUTOMATION,
  })
  artifactType: ArtifactType;

  @ApiPropertyOptional({
    description: 'URL to artifact file or repository',
    example: 'https://github.com/user/budget-tracker',
  })
  fileUrl?: string;

  @ApiPropertyOptional({
    description: 'Mission ID if linked to a mission',
    example: '123e4567-e89b-12d3-a456-426614174002',
  })
  missionId?: string;

  @ApiProperty({
    description: 'Artifact status',
    enum: ArtifactStatus,
    example: ArtifactStatus.PUBLISHED,
  })
  status: ArtifactStatus;

  @ApiProperty({
    description: 'Creation timestamp',
    example: '2025-01-15T10:30:00Z',
  })
  createdAt: Date;

  @ApiPropertyOptional({
    description: 'Creator user details',
  })
  creator?: {
    id: string;
    name: string;
    email: string;
  };

  @ApiPropertyOptional({
    description: 'Mission details if linked',
  })
  mission?: {
    id: string;
    title: string;
  };
}
