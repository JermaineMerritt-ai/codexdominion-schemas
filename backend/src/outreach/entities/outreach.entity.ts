import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { OutreachType } from '@prisma/client';

export class OutreachEntity {
  @ApiProperty()
  id: string;

  @ApiProperty()
  ambassadorId: string;

  @ApiProperty()
  regionId: string;

  @ApiPropertyOptional()
  schoolId?: string | null;

  @ApiProperty({ enum: OutreachType })
  type: OutreachType;

  @ApiPropertyOptional()
  notes?: string | null;

  @ApiProperty()
  date: Date;

  @ApiPropertyOptional()
  ambassador?: {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
  } | null;

  @ApiPropertyOptional()
  region?: {
    id: string;
    name: string;
    country?: string | null;
  } | null;

  @ApiPropertyOptional()
  school?: {
    id: string;
    name: string;
  } | null;
}
