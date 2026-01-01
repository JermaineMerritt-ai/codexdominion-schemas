import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
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
import { CreatorsService } from './creators.service';
import { CreateArtifactDto } from './dto/create-artifact.dto';
import { CreateChallengeDto } from './dto/create-challenge.dto';
import { CreateSubmissionDto } from './dto/create-submission.dto';
import { Artifact } from './entities/artifact.entity';
import { CreatorChallenge } from './entities/creator-challenge.entity';
import { ChallengeSubmission } from './entities/challenge-submission.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { RoleName } from '@prisma/client';

@ApiTags('creators')
@Controller('creators')
export class CreatorsController {
  constructor(private readonly creatorsService: CreatorsService) {}

  // ========================================
  // ARTIFACTS
  // ========================================

  @Post('artifacts')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a new artifact' })
  @ApiResponse({
    status: 201,
    description: 'Artifact created successfully',
    type: Artifact,
  })
  async createArtifact(@Req() req: any, @Body() dto: CreateArtifactDto) {
    return this.creatorsService.createArtifact(req.user.userId, dto);
  }

  @Get('artifacts')
  @ApiOperation({ summary: 'Get all artifacts with optional filters' })
  @ApiQuery({ name: 'creator_id', required: false })
  @ApiQuery({ name: 'artifact_type', required: false })
  @ApiQuery({ name: 'mission_id', required: false })
  @ApiQuery({ name: 'status', required: false })
  @ApiResponse({
    status: 200,
    description: 'List of artifacts',
    type: [Artifact],
  })
  async getArtifacts(
    @Query('creator_id') creatorId?: string,
    @Query('artifact_type') artifactType?: string,
    @Query('mission_id') missionId?: string,
    @Query('status') status?: string,
  ) {
    return this.creatorsService.getArtifacts({
      creatorId,
      artifactType,
      missionId,
      status,
    });
  }

  @Get('artifacts/:id')
  @ApiOperation({ summary: 'Get a single artifact by ID' })
  @ApiResponse({
    status: 200,
    description: 'Artifact details',
    type: Artifact,
  })
  async getArtifactById(@Param('id') id: string) {
    return this.creatorsService.getArtifactById(id);
  }

  @Put('artifacts/:id')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Update an artifact (creator only)' })
  @ApiResponse({
    status: 200,
    description: 'Artifact updated successfully',
    type: Artifact,
  })
  async updateArtifact(
    @Req() req: any,
    @Param('id') id: string,
    @Body() dto: Partial<CreateArtifactDto>,
  ) {
    return this.creatorsService.updateArtifact(req.user.userId, id, dto);
  }

  @Delete('artifacts/:id')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Delete an artifact (creator only)' })
  @ApiResponse({
    status: 200,
    description: 'Artifact deleted successfully',
  })
  async deleteArtifact(@Req() req: any, @Param('id') id: string) {
    return this.creatorsService.deleteArtifact(req.user.userId, id);
  }

  // ========================================
  // CREATOR CHALLENGES
  // ========================================

  @Post('challenges')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a new creator challenge (Admin/Council only)' })
  @ApiResponse({
    status: 201,
    description: 'Challenge created successfully',
    type: CreatorChallenge,
  })
  async createChallenge(@Req() req: any, @Body() dto: CreateChallengeDto) {
    return this.creatorsService.createChallenge(req.user.userId, dto);
  }

  @Get('challenges')
  @ApiOperation({ summary: 'Get all challenges with optional filters' })
  @ApiQuery({ name: 'season_id', required: false })
  @ApiQuery({ name: 'active', required: false, type: Boolean })
  @ApiResponse({
    status: 200,
    description: 'List of challenges',
    type: [CreatorChallenge],
  })
  async getChallenges(
    @Query('season_id') seasonId?: string,
    @Query('active') active?: string,
  ) {
    return this.creatorsService.getChallenges({
      seasonId,
      active: active === 'true',
    });
  }

  @Get('challenges/:id')
  @ApiOperation({ summary: 'Get a single challenge by ID' })
  @ApiResponse({
    status: 200,
    description: 'Challenge details with submissions',
    type: CreatorChallenge,
  })
  async getChallengeById(@Param('id') id: string) {
    return this.creatorsService.getChallengeById(id);
  }

  @Get('challenges/:id/submissions')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(RoleName.ADMIN, RoleName.COUNCIL)
  @ApiBearerAuth()
  @ApiOperation({
    summary: 'Get submissions for a challenge (Admin/Council only)',
  })
  @ApiResponse({
    status: 200,
    description: 'List of submissions with artifact + creator info',
    type: [ChallengeSubmission],
  })
  async getChallengeSubmissions(@Param('id') challengeId: string) {
    return this.creatorsService.getSubmissions({ challengeId });
  }

  // ========================================
  // CHALLENGE SUBMISSIONS
  // ========================================

  @Post('submissions')
  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Submit an artifact to a challenge' })
  @ApiResponse({
    status: 201,
    description: 'Submission created successfully',
    type: ChallengeSubmission,
  })
  async createSubmission(@Req() req: any, @Body() dto: CreateSubmissionDto) {
    return this.creatorsService.createSubmission(req.user.userId, dto);
  }

  @Get('submissions')
  @ApiOperation({ summary: 'Get all submissions with optional filters' })
  @ApiQuery({ name: 'challenge_id', required: false })
  @ApiQuery({ name: 'creator_id', required: false })
  @ApiResponse({
    status: 200,
    description: 'List of submissions',
    type: [ChallengeSubmission],
  })
  async getSubmissions(
    @Query('challenge_id') challengeId?: string,
    @Query('creator_id') creatorId?: string,
  ) {
    return this.creatorsService.getSubmissions({
      challengeId,
      creatorId,
    });
  }
}
