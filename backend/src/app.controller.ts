import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('system')
@Controller()
export class AppController {
  @Get()
  @ApiOperation({ summary: 'Health check endpoint' })
  @ApiResponse({ status: 200, description: 'System is operational' })
  getHealth() {
    return {
      status: 'operational',
      message: '🔥 CodexDominion Civilization Era 2.0',
      flame: 'burning eternal',
      timestamp: new Date().toISOString(),
      system: {
        backend: 'NestJS',
        database: 'PostgreSQL + Prisma',
        architecture: 'Council Seal Structure',
      },
      endpoints: {
        apiDocs: '/api-docs',
        apiV1: '/api/v1',
      },
    };
  }

  @Get('status')
  @ApiOperation({ summary: 'Detailed system status' })
  getStatus() {
    return {
      status: 'live',
      version: '2.0.0',
      environment: process.env.NODE_ENV || 'development',
      database: 'connected',
      message: 'The Flame Burns Sovereign and Eternal 👑',
    };
  }
}
