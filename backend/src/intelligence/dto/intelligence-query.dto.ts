import { IsOptional, IsString, IsIn } from 'class-validator';

export class IntelligenceQueryDto {
  @IsOptional()
  @IsString()
  @IsIn(['youth', 'circles', 'missions', 'curriculum', 'culture', 'creators', 'expansion'])
  domain?: string;

  @IsOptional()
  @IsString()
  regionId?: string;
}
