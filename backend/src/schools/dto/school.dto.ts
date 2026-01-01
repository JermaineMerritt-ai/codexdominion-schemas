import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsOptional, IsUUID } from 'class-validator';

export class CreateSchoolDto {
  @ApiProperty({ example: 'uuid', description: 'Region ID where school is located' })
  @IsNotEmpty()
  @IsUUID()
  regionId: string;

  @ApiProperty({ example: 'Harrison College', description: 'School name' })
  @IsNotEmpty()
  @IsString()
  name: string;

  @ApiPropertyOptional({ example: '123 Main St, Bridgetown', description: 'School address' })
  @IsOptional()
  @IsString()
  address?: string;

  @ApiPropertyOptional({ example: 'Principal John Smith', description: 'Contact person' })
  @IsOptional()
  @IsString()
  contactPerson?: string;
}

export class UpdateSchoolDto {
  @ApiPropertyOptional({ example: 'Harrison College', description: 'School name' })
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ example: '123 Main St, Bridgetown', description: 'School address' })
  @IsOptional()
  @IsString()
  address?: string;

  @ApiPropertyOptional({ example: 'Principal John Smith', description: 'Contact person' })
  @IsOptional()
  @IsString()
  contactPerson?: string;

  @ApiPropertyOptional({ example: 'uuid', description: 'Region ID' })
  @IsOptional()
  @IsUUID()
  regionId?: string;
}

export class SchoolQueryDto {
  @ApiPropertyOptional({ description: 'Filter by region ID' })
  @IsOptional()
  @IsUUID()
  regionId?: string;
}
