import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsString, IsEnum, IsUUID, IsDateString, IsOptional } from 'class-validator';
import { EventType } from '@prisma/client';

export class CreateEventDto {
  @ApiProperty({ example: 'Dawn Ceremony - Season of Mastery' })
  @IsString()
  title: string;

  @ApiPropertyOptional({ example: 'A sacred gathering to honor the youth rising in mastery and leadership.' })
  @IsString()
  @IsOptional()
  description?: string;

  @ApiProperty({ enum: EventType, example: 'SEASON_CEREMONY' })
  @IsEnum(EventType)
  eventType: EventType;

  @ApiPropertyOptional({ example: 'barbados-region-001' })
  @IsUUID()
  @IsOptional()
  regionId?: string;

  @ApiProperty({ example: '2025-03-15T18:00:00.000Z' })
  @IsDateString()
  scheduledAt: string;
}
