import { Injectable, BadRequestException, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { promises as fs } from 'fs';
import { join } from 'path';

export enum UploadType {
  AVATAR = 'avatar',
  ARTIFACT = 'artifact',
  MISSION_SUBMISSION = 'mission_submission',
  CULTURAL_STORY = 'cultural_story',
  EVENT_MATERIAL = 'event_material',
  DOCUMENT = 'document',
}

export interface UploadMetadata {
  userId: string;
  type: UploadType;
  entityId?: string; // ID of related entity (mission, artifact, etc.)
  originalName: string;
  mimeType: string;
  size: number;
  path: string;
}

@Injectable()
export class UploadsService {
  constructor(private prisma: PrismaService) {}

  private readonly UPLOAD_DIR = './uploads';
  private readonly MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

  private readonly ALLOWED_MIME_TYPES = {
    [UploadType.AVATAR]: ['image/jpeg', 'image/png', 'image/webp', 'image/gif'],
    [UploadType.ARTIFACT]: [
      'image/jpeg',
      'image/png',
      'image/webp',
      'image/gif',
      'video/mp4',
      'video/webm',
      'application/pdf',
      'application/zip',
    ],
    [UploadType.MISSION_SUBMISSION]: [
      'image/jpeg',
      'image/png',
      'image/webp',
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ],
    [UploadType.CULTURAL_STORY]: ['image/jpeg', 'image/png', 'image/webp'],
    [UploadType.EVENT_MATERIAL]: [
      'image/jpeg',
      'image/png',
      'image/webp',
      'application/pdf',
      'video/mp4',
    ],
    [UploadType.DOCUMENT]: [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ],
  };

  /**
   * Validate file type and size
   */
  validateFile(file: Express.Multer.File, type: UploadType): void {
    // Check file size
    if (file.size > this.MAX_FILE_SIZE) {
      throw new BadRequestException(
        `File size exceeds maximum allowed size of ${this.MAX_FILE_SIZE / 1024 / 1024}MB`,
      );
    }

    // Check MIME type
    const allowedTypes = this.ALLOWED_MIME_TYPES[type];
    if (!allowedTypes.includes(file.mimetype)) {
      throw new BadRequestException(
        `File type ${file.mimetype} is not allowed for ${type}. Allowed types: ${allowedTypes.join(', ')}`,
      );
    }
  }

  /**
   * Save upload metadata (can be extended to save to database)
   */
  async saveUploadMetadata(metadata: UploadMetadata): Promise<any> {
    // For now, just return the metadata
    // In production, save to database with Prisma
    return {
      id: `upload_${Date.now()}`,
      ...metadata,
      url: `/uploads/${metadata.path}`,
      uploadedAt: new Date(),
    };
  }

  /**
   * Get upload by ID (placeholder for database query)
   */
  async getUpload(id: string): Promise<any> {
    // In production, query from database
    throw new NotFoundException('Upload not found');
  }

  /**
   * Delete file from disk
   */
  async deleteFile(filePath: string): Promise<void> {
    try {
      const fullPath = join(this.UPLOAD_DIR, filePath);
      await fs.unlink(fullPath);
    } catch (error) {
      console.error(`Failed to delete file ${filePath}:`, error);
      throw new BadRequestException('Failed to delete file');
    }
  }

  /**
   * Get file statistics
   */
  async getUploadStats(userId?: string): Promise<any> {
    // In production, query from database
    return {
      totalUploads: 0,
      totalSize: 0,
      byType: {},
    };
  }

  /**
   * Update user avatar
   */
  async updateUserAvatar(userId: string, file: Express.Multer.File): Promise<any> {
    this.validateFile(file, UploadType.AVATAR);

    const metadata: UploadMetadata = {
      userId,
      type: UploadType.AVATAR,
      originalName: file.originalname,
      mimeType: file.mimetype,
      size: file.size,
      path: file.filename,
    };

    const upload = await this.saveUploadMetadata(metadata);

    // Update user profile with new avatar URL
    await this.prisma.profile.update({
      where: { userId },
      data: {
        avatarUrl: upload.url,
      },
    });

    return upload;
  }

  /**
   * Upload creator artifact
   */
  async uploadArtifact(
    userId: string,
    artifactId: string,
    file: Express.Multer.File,
  ): Promise<any> {
    this.validateFile(file, UploadType.ARTIFACT);

    const metadata: UploadMetadata = {
      userId,
      type: UploadType.ARTIFACT,
      entityId: artifactId,
      originalName: file.originalname,
      mimeType: file.mimetype,
      size: file.size,
      path: file.filename,
    };

    const upload = await this.saveUploadMetadata(metadata);

    // Update artifact with file URL
    await this.prisma.artifact.update({
      where: { id: artifactId },
      data: {
        fileUrl: upload.url,
      },
    });

    return upload;
  }

  /**
   * Upload mission submission file
   */
  async uploadMissionSubmission(
    userId: string,
    missionId: string,
    file: Express.Multer.File,
  ): Promise<any> {
    this.validateFile(file, UploadType.MISSION_SUBMISSION);

    const metadata: UploadMetadata = {
      userId,
      type: UploadType.MISSION_SUBMISSION,
      entityId: missionId,
      originalName: file.originalname,
      mimeType: file.mimetype,
      size: file.size,
      path: file.filename,
    };

    return await this.saveUploadMetadata(metadata);
  }

  /**
   * Upload cultural story image
   * NOTE: CulturalStory model currently doesn't have imageUrl field
   * This method saves metadata only - add imageUrl to schema if needed
   */
  async uploadCulturalStory(
    userId: string,
    storyId: string,
    file: Express.Multer.File,
  ): Promise<any> {
    this.validateFile(file, UploadType.CULTURAL_STORY);

    const metadata: UploadMetadata = {
      userId,
      type: UploadType.CULTURAL_STORY,
      entityId: storyId,
      originalName: file.originalname,
      mimeType: file.mimetype,
      size: file.size,
      path: file.filename,
    };

    const upload = await this.saveUploadMetadata(metadata);

    // TODO: Add imageUrl field to CulturalStory model in schema.prisma
    // Then uncomment this code:
    // await this.prisma.culturalStory.update({
    //   where: { id: storyId },
    //   data: {
    //     imageUrl: upload.url,
    //   },
    // });

    return upload;
  }
}
