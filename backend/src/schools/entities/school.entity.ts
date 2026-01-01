import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class SchoolEntity {
  @ApiProperty()
  id: string;

  @ApiProperty()
  regionId: string;

  @ApiProperty()
  name: string;

  @ApiPropertyOptional()
  address?: string | null;

  @ApiPropertyOptional()
  contactPerson?: string | null;

  @ApiPropertyOptional()
  region?: {
    id: string;
    name: string;
    country?: string | null;
  } | null;

  @ApiPropertyOptional()
  profileCount?: number;

  @ApiPropertyOptional()
  outreachCount?: number;
}
