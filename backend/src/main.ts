import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { NestExpressApplication } from '@nestjs/platform-express';
import { AppModule } from './app.module';
import { join } from 'path';

async function bootstrap() {
  // Create with explicit Express type
  const app = await NestFactory.create<NestExpressApplication>(AppModule);

  // Serve static files from uploads directory
  app.useStaticAssets(join(__dirname, '..', 'uploads'), {
    prefix: '/uploads/',
  });

  // Global prefix (excludes only root and status for direct access)
  app.setGlobalPrefix('api/v1', {
    exclude: ['/', 'status'],
  });

  // Validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: false, // Allow snake_case fields
      transform: true,
      transformOptions: {
        enableImplicitConversion: true,
      },
    }),
  );

  // CORS
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  });

  // Swagger documentation
  const config = new DocumentBuilder()
    .setTitle('CodexDominion Civilization API')
    .setDescription('Core API for CodexDominion 2.0 — youth, creators, circles, missions, culture, and analytics.')
    .setVersion('1.0.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api-docs', app, document);

  const port = parseInt(process.env.PORT || '4000', 10);
  const host = '0.0.0.0';
  
  console.log(`[DEBUG] Attempting to bind to ${host}:${port}...`);
  
  // Initialize app but DON'T use app.listen - use raw Express
  await app.init();
  
  // Get raw Express instance
  const expressApp = app.getHttpAdapter().getInstance();
  const http = require('http');
  const server = http.createServer(expressApp);
  
  // Explicit listen with error handling
  await new Promise<void>((resolve, reject) => {
    server.listen(port, host, () => {
      const address = server.address();
      console.log(`✅ BOUND TO: ${JSON.stringify(address)}`);
      console.log(`🔥 CodexDominion backend running on http://localhost:${port}`);
      console.log(`📚 API docs available at http://localhost:${port}/api-docs`);
      resolve();
    });
    
    server.on('error', (err: any) => {
      console.error(`❌ FATAL ERROR:`, err);
      reject(err);
    });
  });
}

bootstrap().catch(err => {
  console.error('Bootstrap failed:', err);
  process.exit(1);
});
