import { ApiProperty } from '@nestjs/swagger';

export class ChallengeSubmission {
  @ApiProperty({
    description: 'Unique identifier',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  id: string;

  @ApiProperty({
    description: 'Challenge ID',
    example: '123e4567-e89b-12d3-a456-426614174001',
  })
  challengeId: string;

  @ApiProperty({
    description: 'Creator user ID',
    example: '123e4567-e89b-12d3-a456-426614174002',
  })
  creatorId: string;

  @ApiProperty({
    description: 'Artifact ID',
    example: '123e4567-e89b-12d3-a456-426614174003',
  })
  artifactId: string;

  @ApiProperty({
    description: 'Submission timestamp',
    example: '2025-01-20T14:30:00Z',
  })
  submittedAt: Date;

  @ApiProperty({
    description: 'Challenge details',
  })
  challenge?: {
    id: string;
    title: string;
  };

  @ApiProperty({
    description: 'Creator details',
  })
  creator?: {
    id: string;
    name: string;
    email: string;
  };

  @ApiProperty({
    description: 'Artifact details',
  })
  artifact?: {
    id: string;
    title: string;
    artifactType: string;
  };
}
