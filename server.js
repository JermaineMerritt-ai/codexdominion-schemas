#!/usr/bin/env node

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';

// ES Module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
  })
);

// CORS configuration
app.use(
  cors({
    origin:
      process.env.NODE_ENV === 'production'
        ? ['https://codex-dominion.dev']
        : ['http://localhost:3001', 'http://localhost:3000'],
    credentials: true,
  })
);

// Logging
app.use(morgan('combined'));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Static files
app.use('/static', express.static(path.join(__dirname, 'public')));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    timestamp: new Date().toISOString(),
    version: '2.0.0',
    empire: 'codex-dominion',
    flame_status: 'eternal',
    sovereignty_level: 'supreme',
  });
});

// API Routes
app.get('/api/empire/status', (req, res) => {
  res.json({
    empire_name: 'Codex Dominion',
    status: 'fully_operational',
    components: {
      frontend: 'active',
      backend: 'active',
      dashboard: 'active',
      council: 'active',
      flame: 'eternal',
      sovereignty: 'supreme',
    },
    last_updated: new Date().toISOString(),
    version: '2.0.0',
  });
});

// Empire management endpoints
app.get('/api/empire/flame', (req, res) => {
  res.json({
    flame_status: 'eternal',
    ignited: '2024-01-01T00:00:00.000Z',
    intensity: 'maximum',
    color: 'cosmic_azure',
    power_level: 'infinite',
  });
});

app.get('/api/empire/sovereignty', (req, res) => {
  res.json({
    sovereignty_level: 'supreme',
    digital_independence: true,
    council_status: 'active',
    sacred_seals: 'authenticated',
    proclamations: 'archived',
    dominion_scope: 'cosmic',
  });
});

// Dashboard proxy endpoint
app.get('/api/dashboard/launch', (req, res) => {
  res.json({
    dashboard_url: 'http://localhost:8050',
    council_url: 'http://localhost:8051',
    status: 'ready_to_launch',
    commands: {
      dashboard: 'npm run dashboard',
      council: 'npm run council',
    },
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(chalk.red('Server Error:'), err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong!',
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'The requested resource was not found on this empire.',
  });
});

// Start server
app.listen(PORT, () => {
  console.log(chalk.bold.magenta('🏰 CODEX DOMINION EMPIRE SERVER 🏰'));
  console.log(chalk.bold.green(`🔥 Server ignited on port ${PORT}`));
  console.log(chalk.bold.blue(`👑 Empire Status: FULLY OPERATIONAL`));
  console.log(chalk.bold.yellow(`🌟 Environment: ${process.env.NODE_ENV || 'development'}`));
  console.log(chalk.bold.cyan(`📡 Health Check: http://localhost:${PORT}/health`));
  console.log(chalk.bold.magenta(`⚡ Empire API: http://localhost:${PORT}/api/empire/status`));
  console.log(chalk.bold.green('\n✨ Digital sovereignty achieved ✨'));
});

// Root route
app.get('/', (req, res) => {
  res.send('Welcome to Codex Dominion Empire Server!');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log(chalk.yellow('\n🛑 Received SIGTERM, shutting down gracefully...'));
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log(chalk.yellow('\n🛑 Received SIGINT, shutting down gracefully...'));
  process.exit(0);
});

export default app;
