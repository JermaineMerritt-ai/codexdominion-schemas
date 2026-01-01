import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Patch,
  Query,
  UseGuards,
  Request,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { AlertsService } from './alerts.service';
import { CreateAlertDto } from './dto/create-alert.dto';
import { AlertEntity } from './entities/alert.entity';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';

@ApiTags('alerts')
@Controller('alerts')
export class AlertsController {
  constructor(private readonly alertsService: AlertsService) {}

  @Post()
  // Temporarily disabled auth for testing
  // @UseGuards(JwtAuthGuard, RolesGuard)
  // @Roles('ADMIN', 'COUNCIL', 'REGIONAL_DIRECTOR', 'YOUTH_CAPTAIN')
  // @ApiBearerAuth()
  @ApiOperation({ summary: 'Create a new alert' })
  @ApiResponse({ status: 201, type: AlertEntity })
  create(@Body() createAlertDto: CreateAlertDto) {
    return this.alertsService.create(createAlertDto);
  }

  @Get()
  // Temporarily disabled auth for testing
  // @UseGuards(JwtAuthGuard)
  // @ApiBearerAuth()
  @ApiOperation({ summary: 'Get all alerts with optional filters' })
  @ApiResponse({ status: 200, type: [AlertEntity] })
  findAll(
    @Query('domain') domain?: string,
    @Query('severity') severity?: string,
    @Query('acknowledged') acknowledged?: string,
    @Query('limit') limit?: string,
  ) {
    return this.alertsService.findAll({
      domain,
      severity,
      acknowledged: acknowledged ? acknowledged === 'true' : undefined,
      limit: limit ? parseInt(limit, 10) : undefined,
    });
  }

  @Get('stats')
  // Temporarily disabled auth for testing
  // @UseGuards(JwtAuthGuard)
  // @ApiBearerAuth()
  @ApiOperation({ summary: 'Get alert statistics' })
  @ApiResponse({ status: 200 })
  getStats() {
    return this.alertsService.getStats();
  }

  @Get(':id')
  // Temporarily disabled auth for testing
  // @UseGuards(JwtAuthGuard)
  // @ApiBearerAuth()
  @ApiOperation({ summary: 'Get a specific alert by ID' })
  @ApiResponse({ status: 200, type: AlertEntity })
  findOne(@Param('id') id: string) {
    return this.alertsService.findOne(id);
  }

  @Patch(':id/acknowledge')
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('ADMIN', 'COUNCIL', 'REGIONAL_DIRECTOR', 'YOUTH_CAPTAIN')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Acknowledge an alert' })
  @ApiResponse({ status: 200, type: AlertEntity })
  acknowledge(@Param('id') id: string, @Request() req: any) {
    return this.alertsService.acknowledge(id, req.user.userId);
  }
}
