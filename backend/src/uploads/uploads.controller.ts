import {
  Controller,
  Post,
  Get,
  Delete,
  Param,
  UseGuards,
  UseInterceptors,
  UploadedFile,
  UploadedFiles,
  Request,
  BadRequestException,
  HttpCode,
  HttpStatus,
} from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
  ApiConsumes,
  ApiBody,
} from '@nestjs/swagger';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { UploadsService, UploadType } from './uploads.service';

@ApiTags('Uploads')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('uploads')
export class UploadsController {
  constructor(private readonly uploadsService: UploadsService) {}

  /**
   * Upload user avatar
   */
  @Post('avatar')
  @ApiOperation({
    summary: 'Upload user avatar',
    description: 'Upload or update user profile avatar. Max size: 50MB. Allowed: JPEG, PNG, WebP, GIF.',
  })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        file: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  @ApiResponse({ status: 201, description: 'Avatar uploaded successfully' })
  @ApiResponse({ status: 400, description: 'Invalid file type or size' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadAvatar(@UploadedFile() file: Express.Multer.File, @Request() req) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user.sub;
    return await this.uploadsService.updateUserAvatar(userId, file);
  }

  /**
   * Upload creator artifact file
   */
  @Post('artifact/:artifactId')
  @ApiOperation({
    summary: 'Upload creator artifact file',
    description:
      'Upload file for creator artifact. Supports images, videos, PDFs, ZIP files. Max size: 50MB.',
  })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        file: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  @ApiResponse({ status: 201, description: 'Artifact file uploaded successfully' })
  @ApiResponse({ status: 400, description: 'Invalid file type or size' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadArtifact(
    @Param('artifactId') artifactId: string,
    @UploadedFile() file: Express.Multer.File,
    @Request() req,
  ) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user.sub;
    return await this.uploadsService.uploadArtifact(userId, artifactId, file);
  }

  /**
   * Upload mission submission file
   */
  @Post('mission/:missionId/submission')
  @ApiOperation({
    summary: 'Upload mission submission file',
    description:
      'Upload file as part of mission submission. Supports images, PDFs, Word documents. Max size: 50MB.',
  })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        file: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  @ApiResponse({ status: 201, description: 'Mission submission file uploaded successfully' })
  @ApiResponse({ status: 400, description: 'Invalid file type or size' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadMissionSubmission(
    @Param('missionId') missionId: string,
    @UploadedFile() file: Express.Multer.File,
    @Request() req,
  ) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user.sub;
    return await this.uploadsService.uploadMissionSubmission(userId, missionId, file);
  }

  /**
   * Upload cultural story image
   */
  @Post('culture/story/:storyId')
  @ApiOperation({
    summary: 'Upload cultural story image',
    description: 'Upload image for cultural story. Supports JPEG, PNG, WebP. Max size: 50MB.',
  })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        file: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  @ApiResponse({ status: 201, description: 'Cultural story image uploaded successfully' })
  @ApiResponse({ status: 400, description: 'Invalid file type or size' })
  @UseInterceptors(FileInterceptor('file'))
  async uploadCulturalStoryImage(
    @Param('storyId') storyId: string,
    @UploadedFile() file: Express.Multer.File,
    @Request() req,
  ) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    const userId = req.user.sub;
    return await this.uploadsService.uploadCulturalStory(userId, storyId, file);
  }

  /**
   * Upload multiple files (batch upload)
   */
  @Post('batch')
  @ApiOperation({
    summary: 'Batch upload multiple files',
    description: 'Upload multiple files at once. Max 10 files per request, 50MB each.',
  })
  @ApiConsumes('multipart/form-data')
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        files: {
          type: 'array',
          items: {
            type: 'string',
            format: 'binary',
          },
        },
      },
    },
  })
  @ApiResponse({ status: 201, description: 'Files uploaded successfully' })
  @ApiResponse({ status: 400, description: 'Invalid files' })
  @UseInterceptors(FilesInterceptor('files', 10))
  async uploadBatch(@UploadedFiles() files: Express.Multer.File[], @Request() req) {
    if (!files || files.length === 0) {
      throw new BadRequestException('No files uploaded');
    }

    const userId = req.user.sub;
    const uploads: any[] = [];

    for (const file of files) {
      const metadata = {
        userId,
        type: UploadType.DOCUMENT,
        originalName: file.originalname,
        mimeType: file.mimetype,
        size: file.size,
        path: file.filename,
      };
      uploads.push(await this.uploadsService.saveUploadMetadata(metadata));
    }

    return {
      count: uploads.length,
      uploads,
    };
  }

  /**
   * Get upload statistics
   */
  @Get('stats')
  @ApiOperation({
    summary: 'Get upload statistics',
    description: 'Get upload statistics for current user (total uploads, size, by type).',
  })
  @ApiResponse({ status: 200, description: 'Statistics retrieved successfully' })
  async getStats(@Request() req) {
    const userId = req.user.sub;
    return await this.uploadsService.getUploadStats(userId);
  }

  /**
   * Delete uploaded file
   */
  @Delete(':filename')
  @ApiOperation({
    summary: 'Delete uploaded file',
    description: 'Delete a previously uploaded file from storage.',
  })
  @ApiResponse({ status: 200, description: 'File deleted successfully' })
  @ApiResponse({ status: 404, description: 'File not found' })
  @HttpCode(HttpStatus.OK)
  async deleteFile(@Param('filename') filename: string) {
    await this.uploadsService.deleteFile(filename);
    return {
      message: 'File deleted successfully',
      filename,
    };
  }
}
