import { PartialType } from '@nestjs/swagger';
import { CreateCeremonyScriptDto } from './create-ceremony-script.dto';

export class UpdateCeremonyScriptDto extends PartialType(CreateCeremonyScriptDto) {}
