import { ApiProperty } from '@nestjs/swagger';
import { RitualType } from '@prisma/client';

export class RitualEntity {
  @ApiProperty({
    description: 'Ritual UUID',
    example: '123e4567-e89b-12d3-a456-426614174000',
  })
  id: string;

  @ApiProperty({
    description: 'Ritual name',
    example: 'Circle Opening Invocation',
  })
  name: string;

  @ApiProperty({
    description: 'Ritual description and instructions',
    required: false,
  })
  description?: string;

  @ApiProperty({
    description: 'Type of ritual',
    enum: RitualType,
    example: 'OPENING',
  })
  type: RitualType;
}
