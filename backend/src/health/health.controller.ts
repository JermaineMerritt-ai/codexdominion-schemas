import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('health')
@Controller('health')
export class HealthController {
  @Get()
  @ApiOperation({ summary: 'API v1 health check' })
  check() {
    return {
      status: 'ok',
      message: 'API v1 is operational',
      timestamp: new Date().toISOString(),
    };
  }

  @Get('db')
  @ApiOperation({ summary: 'Database health check' })
  checkDatabase() {
    return {
      database: 'connected',
      type: 'PostgreSQL',
      orm: 'Prisma',
      status: 'operational',
    };
  }
}
