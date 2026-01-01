import { IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateSubmissionDto {
  @ApiProperty({
    description: 'Challenge ID',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  @IsUUID()
  challengeId: string;

  @ApiProperty({
    description: 'Artifact ID to submit for this challenge',
    example: '123e4567-e89b-12d3-a456-426614174001',
  })
  @IsUUID()
  artifactId: string;
}
