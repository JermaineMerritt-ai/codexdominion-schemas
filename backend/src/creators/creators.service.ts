import { Injectable, NotFoundException, ForbiddenException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateArtifactDto, ArtifactStatus } from './dto/create-artifact.dto';
import { CreateChallengeDto } from './dto/create-challenge.dto';
import { CreateSubmissionDto } from './dto/create-submission.dto';

@Injectable()
export class CreatorsService {
  constructor(private prisma: PrismaService) {}

  // ========================================
  // ARTIFACTS
  // ========================================

  /**
   * Create a new artifact
   */
  async createArtifact(userId: string, dto: CreateArtifactDto) {
    // Validate mission exists if provided
    if (dto.missionId) {
      const mission = await this.prisma.mission.findUnique({
        where: { id: dto.missionId },
      });
      if (!mission) {
        throw new NotFoundException(`Mission with ID ${dto.missionId} not found`);
      }
    }

    return this.prisma.artifact.create({
      data: {
        creatorId: userId,
        title: dto.title,
        description: dto.description,
        artifactType: dto.artifactType,
        fileUrl: dto.fileUrl,
        missionId: dto.missionId,
        status: dto.status || ArtifactStatus.PUBLISHED,
      },
      include: {
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        mission: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });
  }

  /**
   * Get all artifacts with optional filters
   */
  async getArtifacts(filters?: {
    creatorId?: string;
    artifactType?: string;
    missionId?: string;
    status?: string;
  }) {
    const where: any = {};

    if (filters?.creatorId) {
      where.creatorId = filters.creatorId;
    }
    if (filters?.artifactType) {
      where.artifactType = filters.artifactType;
    }
    if (filters?.missionId) {
      where.missionId = filters.missionId;
    }
    if (filters?.status) {
      where.status = filters.status;
    }

    return this.prisma.artifact.findMany({
      where,
      include: {
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        mission: {
          select: {
            id: true,
            title: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  }

  /**
   * Get a single artifact by ID
   */
  async getArtifactById(artifactId: string) {
    const artifact = await this.prisma.artifact.findUnique({
      where: { id: artifactId },
      include: {
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        mission: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });

    if (!artifact) {
      throw new NotFoundException(`Artifact with ID ${artifactId} not found`);
    }

    return artifact;
  }

  /**
   * Update an artifact (creator can only update their own)
   */
  async updateArtifact(userId: string, artifactId: string, dto: Partial<CreateArtifactDto>) {
    const artifact = await this.prisma.artifact.findUnique({
      where: { id: artifactId },
    });

    if (!artifact) {
      throw new NotFoundException(`Artifact with ID ${artifactId} not found`);
    }

    if (artifact.creatorId !== userId) {
      throw new ForbiddenException('You can only update your own artifacts');
    }

    return this.prisma.artifact.update({
      where: { id: artifactId },
      data: dto,
      include: {
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        mission: {
          select: {
            id: true,
            title: true,
          },
        },
      },
    });
  }

  /**
   * Delete an artifact (creator can only delete their own)
   */
  async deleteArtifact(userId: string, artifactId: string) {
    const artifact = await this.prisma.artifact.findUnique({
      where: { id: artifactId },
    });

    if (!artifact) {
      throw new NotFoundException(`Artifact with ID ${artifactId} not found`);
    }

    if (artifact.creatorId !== userId) {
      throw new ForbiddenException('You can only delete your own artifacts');
    }

    await this.prisma.artifact.delete({
      where: { id: artifactId },
    });

    return { message: 'Artifact deleted successfully' };
  }

  // ========================================
  // CREATOR CHALLENGES
  // ========================================

  /**
   * Create a new creator challenge (admin/council only)
   */
  async createChallenge(userId: string, dto: CreateChallengeDto) {
    // Validate season exists if provided
    if (dto.seasonId) {
      const season = await this.prisma.season.findUnique({
        where: { id: dto.seasonId },
      });
      if (!season) {
        throw new NotFoundException(`Season with ID ${dto.seasonId} not found`);
      }
    }

    return this.prisma.creatorChallenge.create({
      data: {
        title: dto.title,
        description: dto.description,
        seasonId: dto.seasonId,
        deadline: dto.deadline ? new Date(dto.deadline) : null,
        createdBy: userId,
      },
      include: {
        season: {
          select: {
            id: true,
            name: true,
          },
        },
      },
    });
  }

  /**
   * Get all challenges with optional filters
   */
  async getChallenges(filters?: {
    seasonId?: string;
    active?: boolean;
  }) {
    const where: any = {};

    if (filters?.seasonId) {
      where.seasonId = filters.seasonId;
    }

    // If active filter is true, only show challenges with future deadlines
    if (filters?.active === true) {
      where.deadline = {
        gte: new Date(),
      };
    }

    const challenges = await this.prisma.creatorChallenge.findMany({
      where,
      include: {
        season: {
          select: {
            id: true,
            name: true,
          },
        },
        _count: {
          select: {
            submissions: true,
          },
        },
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    // Map _count to submissionCount
    return challenges.map((challenge) => ({
      ...challenge,
      submissionCount: challenge._count.submissions,
      _count: undefined,
    }));
  }

  /**
   * Get a single challenge by ID
   */
  async getChallengeById(challengeId: string) {
    const challenge = await this.prisma.creatorChallenge.findUnique({
      where: { id: challengeId },
      include: {
        season: {
          select: {
            id: true,
            name: true,
          },
        },
        submissions: {
          include: {
            artifact: true,
            creator: {
              select: {
                id: true,
                firstName: true,
                lastName: true,
                email: true,
              },
            },
          },
        },
      },
    });

    if (!challenge) {
      throw new NotFoundException(`Challenge with ID ${challengeId} not found`);
    }

    return challenge;
  }

  // ========================================
  // CHALLENGE SUBMISSIONS
  // ========================================

  /**
   * Submit an artifact to a challenge
   */
  async createSubmission(userId: string, dto: CreateSubmissionDto) {
    // Validate challenge exists
    const challenge = await this.prisma.creatorChallenge.findUnique({
      where: { id: dto.challengeId },
    });
    if (!challenge) {
      throw new NotFoundException(`Challenge with ID ${dto.challengeId} not found`);
    }

    // Check if deadline has passed
    if (challenge.deadline && new Date() > challenge.deadline) {
      throw new BadRequestException('Challenge deadline has passed');
    }

    // Validate artifact exists and belongs to user
    const artifact = await this.prisma.artifact.findUnique({
      where: { id: dto.artifactId },
    });
    if (!artifact) {
      throw new NotFoundException(`Artifact with ID ${dto.artifactId} not found`);
    }
    if (artifact.creatorId !== userId) {
      throw new ForbiddenException('You can only submit your own artifacts');
    }

    // Check if already submitted
    const existingSubmission = await this.prisma.challengeSubmission.findFirst({
      where: {
        challengeId: dto.challengeId,
        creatorId: userId,
        artifactId: dto.artifactId,
      },
    });
    if (existingSubmission) {
      throw new BadRequestException('This artifact is already submitted to this challenge');
    }

    return this.prisma.challengeSubmission.create({
      data: {
        challengeId: dto.challengeId,
        creatorId: userId,
        artifactId: dto.artifactId,
      },
      include: {
        challenge: {
          select: {
            id: true,
            title: true,
          },
        },
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        artifact: {
          select: {
            id: true,
            title: true,
            artifactType: true,
          },
        },
      },
    });
  }

  /**
   * Get submissions with optional filters
   */
  async getSubmissions(filters?: {
    challengeId?: string;
    creatorId?: string;
  }) {
    const where: any = {};

    if (filters?.challengeId) {
      where.challengeId = filters.challengeId;
    }
    if (filters?.creatorId) {
      where.creatorId = filters.creatorId;
    }

    return this.prisma.challengeSubmission.findMany({
      where,
      include: {
        challenge: {
          select: {
            id: true,
            title: true,
          },
        },
        creator: {
          select: {
            id: true,
            firstName: true,
            lastName: true,
            email: true,
          },
        },
        artifact: {
          select: {
            id: true,
            title: true,
            artifactType: true,
            fileUrl: true,
          },
        },
      },
      orderBy: {
        submittedAt: 'desc',
      },
    });
  }
}
