import { IsString, IsEnum, IsOptional, IsUUID, MaxLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export enum ArtifactType {
  AUTOMATION = 'AUTOMATION',
  DESIGN = 'DESIGN',
  WRITING = 'WRITING',
  VIDEO = 'VIDEO',
  APP = 'APP',
  OTHER = 'OTHER',
}

export enum ArtifactStatus {
  DRAFT = 'DRAFT',
  SUBMITTED = 'SUBMITTED',
  PUBLISHED = 'PUBLISHED',
  ARCHIVED = 'ARCHIVED',
}

export class CreateArtifactDto {
  @ApiProperty({
    description: 'Title of the artifact',
    example: 'Budget Tracker Automation',
  })
  @IsString()
  @MaxLength(200)
  title: string;

  @ApiPropertyOptional({
    description: 'Description of what the artifact does',
    example: 'Automates monthly budget calculations and sends alerts',
  })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiProperty({
    description: 'Type of artifact',
    enum: ArtifactType,
    example: ArtifactType.AUTOMATION,
  })
  @IsEnum(ArtifactType)
  artifactType: ArtifactType;

  @ApiPropertyOptional({
    description: 'URL to the artifact file, repository, or media',
    example: 'https://github.com/user/budget-tracker',
  })
  @IsOptional()
  @IsString()
  fileUrl?: string;

  @ApiPropertyOptional({
    description: 'Mission ID if this artifact is linked to a mission',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  @IsOptional()
  @IsUUID()
  missionId?: string;

  @ApiPropertyOptional({
    description: 'Status of the artifact (defaults to PUBLISHED)',
    enum: ArtifactStatus,
    example: ArtifactStatus.PUBLISHED,
  })
  @IsOptional()
  @IsEnum(ArtifactStatus)
  status?: ArtifactStatus;
}
