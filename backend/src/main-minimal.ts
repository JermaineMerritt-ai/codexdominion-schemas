import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix('api/v1');
  app.enableCors();

  const config = new DocumentBuilder()
    .setTitle('CodexDominion Civilization API')
    .setDescription('Core API for CodexDominion 2.0')
    .setVersion('1.0.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api-docs', app, document);

  const port = 4000;
  
  // Get Express instance and listen with proper event handling
  await app.init();
  const httpAdapter = app.getHttpAdapter();
  const httpServer = httpAdapter.getHttpServer();
  
  httpServer.listen(port, '0.0.0.0', () => {
    console.log('🔥 Backend successfully listening on port 4000');
    console.log('📚 Swagger docs: http://localhost:4000/api-docs');
  });
  
  // Keep process alive
  process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    httpServer.close(() => {
      console.log('HTTP server closed');
    });
  });
}

bootstrap().catch(err => {
  console.error('Failed to start application:', err);
  process.exit(1);
});
