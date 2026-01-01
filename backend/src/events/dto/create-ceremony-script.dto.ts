import { ApiProperty } from '@nestjs/swagger';
import { IsObject, IsNotEmpty } from 'class-validator';

export class CreateCeremonyScriptDto {
  @ApiProperty({
    description: 'Ceremony script sections',
    example: {
      rituals: ['Opening flame lighting', 'Circle formation', 'Unity pledge'],
      readings: ['Diaspora story: The Journey Home', 'Cultural reading'],
      affirmations: [
        'I rise with my identity',
        'I honor my community',
        'I carry the flame'
      ],
      transitions: ['Dawn transition music', 'Circle closing ritual']
    }
  })
  @IsObject()
  @IsNotEmpty()
  sections: {
    rituals?: string[];
    readings?: string[];
    affirmations?: string[];
    transitions?: string[];
    [key: string]: any;
  };
}
