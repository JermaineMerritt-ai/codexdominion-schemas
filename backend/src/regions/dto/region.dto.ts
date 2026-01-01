import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsOptional, IsUUID } from 'class-validator';

export class CreateRegionDto {
  @ApiProperty({ example: 'Barbados', description: 'Region name' })
  @IsNotEmpty()
  @IsString()
  name: string;

  @ApiPropertyOptional({ example: 'Barbados', description: 'Country name' })
  @IsOptional()
  @IsString()
  country?: string;

  @ApiPropertyOptional({ example: 'America/Barbados', description: 'Timezone' })
  @IsOptional()
  @IsString()
  timezone?: string;

  @ApiPropertyOptional({ example: 'uuid', description: 'Regional Director user ID' })
  @IsOptional()
  @IsUUID()
  directorId?: string;
}

export class UpdateRegionDto {
  @ApiPropertyOptional({ example: 'Caribbean Region', description: 'Region name' })
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ example: 'Barbados', description: 'Country name' })
  @IsOptional()
  @IsString()
  country?: string;

  @ApiPropertyOptional({ example: 'America/Barbados', description: 'Timezone' })
  @IsOptional()
  @IsString()
  timezone?: string;

  @ApiPropertyOptional({ example: 'uuid', description: 'Regional Director user ID' })
  @IsOptional()
  @IsUUID()
  directorId?: string;
}
