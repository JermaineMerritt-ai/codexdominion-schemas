import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class RegionEntity {
  @ApiProperty()
  id: string;

  @ApiProperty()
  name: string;

  @ApiPropertyOptional()
  country?: string | null;

  @ApiPropertyOptional()
  timezone?: string | null;

  @ApiPropertyOptional()
  directorId?: string | null;

  @ApiPropertyOptional()
  director?: {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
  } | null;

  @ApiPropertyOptional()
  schoolCount?: number;

  @ApiPropertyOptional()
  circleCount?: number;

  @ApiPropertyOptional()
  outreachCount?: number;
}
