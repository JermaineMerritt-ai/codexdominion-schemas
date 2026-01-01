import { ApiProperty } from '@nestjs/swagger';
import { IsString, IsEnum, IsOptional } from 'class-validator';
import { RitualType } from '@prisma/client';

export class CreateRitualDto {
  @ApiProperty({
    description: 'Ritual name',
    example: 'Circle Opening Invocation',
  })
  @IsString()
  name: string;

  @ApiProperty({
    description: 'Ritual description and instructions',
    example: 'Begin each Circle session by lighting the flame (symbolic or real) and reciting: "We gather as one Circle, carrying the flame of our ancestors, building the future for our youth."',
  })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiProperty({
    description: 'Type of ritual',
    enum: RitualType,
    example: 'OPENING',
  })
  @IsEnum(RitualType)
  type: RitualType;
}
