import {
  Controller,
  Get,
  Post,
  Body,
  Query,
  UseGuards,
  Req,
} from '@nestjs/common';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiQuery,
} from '@nestjs/swagger';
import { CultureService } from './culture.service';
import { CreateStoryDto } from './dto/create-story.dto';
import { CreateRitualDto } from './dto/create-ritual.dto';
import { CulturalStoryEntity } from './entities/cultural-story.entity';
import { RitualEntity } from './entities/ritual.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { RoleName } from '@prisma/client';

@ApiTags('culture')
@Controller('culture')
export class CultureController {
  constructor(private cultureService: CultureService) {}

  // ======================================================
  // 🔥 STORY ENDPOINTS
  // ======================================================

  @Get('story/current')
  @ApiOperation({
    summary: 'Get current cultural story',
    description:
      'Returns the current week\'s cultural story for the authenticated user. Region-aware if user has region_id.',
  })
  @ApiResponse({
    status: 200,
    description: 'Current cultural story retrieved',
    type: CulturalStoryEntity,
  })
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard)
  async getCurrentStory(@Req() req: any) {
    const userId = req.user?.userId;
    return this.cultureService.getCurrentStory(userId);
  }

  @Get('stories')
  @ApiOperation({
    summary: 'List cultural stories',
    description: 'Returns all cultural stories, optionally filtered by season',
  })
  @ApiQuery({
    name: 'season_id',
    required: false,
    description: 'Filter stories by season UUID',
  })
  @ApiResponse({
    status: 200,
    description: 'Cultural stories retrieved',
    type: [CulturalStoryEntity],
  })
  async getStories(@Query('season_id') seasonId?: string) {
    return this.cultureService.getStories(seasonId);
  }

  @Post('stories')
  @ApiOperation({
    summary: 'Create cultural story',
    description:
      'Create a new cultural story (Council/Admin/Educator only). Stories become part of the weekly cultural heartbeat.',
  })
  @ApiResponse({
    status: 201,
    description: 'Story created successfully',
    type: CulturalStoryEntity,
  })
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.COUNCIL, RoleName.ADMIN, RoleName.EDUCATOR)
  async createStory(@Body() dto: CreateStoryDto) {
    return this.cultureService.createStory(dto);
  }

  // ======================================================
  // 🔱 RITUAL ENDPOINTS
  // ======================================================

  @Get('rituals')
  @ApiOperation({
    summary: 'List all rituals',
    description:
      'Returns all rituals (opening, closing, seasonal, unity, ceremony)',
  })
  @ApiQuery({
    name: 'type',
    required: false,
    enum: ['OPENING', 'CLOSING', 'SEASONAL', 'UNITY', 'CEREMONY'],
    description: 'Filter by ritual type',
  })
  @ApiResponse({
    status: 200,
    description: 'Rituals retrieved',
    type: [RitualEntity],
  })
  async getRituals(@Query('type') type?: string) {
    return this.cultureService.getRituals(type);
  }

  @Post('rituals')
  @ApiOperation({
    summary: 'Create ritual',
    description:
      'Create a new ritual or ceremony (Council/Admin only). Rituals define the ceremonial structure of CodexDominion.',
  })
  @ApiResponse({
    status: 201,
    description: 'Ritual created successfully',
    type: RitualEntity,
  })
  @ApiBearerAuth()
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.COUNCIL, RoleName.ADMIN)
  async createRitual(@Body() dto: CreateRitualDto) {
    return this.cultureService.createRitual(dto);
  }
}
