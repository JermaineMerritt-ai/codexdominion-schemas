#!/usr/bin/env node

/**
 * HTTP-based MCP Server for Codex Dominion
 * Alternative MCP server implementation using HTTP/WebSocket for better connectivity
 */

import express from 'express';
import cors from 'cors';
import { WebSocketServer } from 'ws';
import { createServer } from 'http';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class CodexDominionHTTPMCPServer {
  constructor(port = 4953) {
    this.port = port;
    this.app = express();
    this.server = createServer(this.app);
    this.wss = new WebSocketServer({ server: this.server });

    this.setupMiddleware();
    this.setupRoutes();
    this.setupWebSocket();
  }

  setupMiddleware() {
    this.app.use(cors());
    this.app.use(express.json());

    // Request logging
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        server: 'Codex Dominion MCP Server',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
      });
    });

    // MCP tools endpoint
    this.app.get('/tools', (req, res) => {
      res.json({
        tools: [
          {
            name: 'read_codex_file',
            description: 'Read files from the Codex Dominion workspace',
            inputSchema: {
              type: 'object',
              properties: {
                filePath: { type: 'string', description: 'Path to file' },
              },
              required: ['filePath'],
            },
          },
          {
            name: 'list_directory',
            description: 'List directory contents',
            inputSchema: {
              type: 'object',
              properties: {
                dirPath: {
                  type: 'string',
                  description: 'Directory path',
                  default: '.',
                },
              },
            },
          },
          {
            name: 'system_status',
            description: 'Get system status information',
            inputSchema: { type: 'object', properties: {} },
          },
        ],
      });
    });

    // Tool execution endpoint
    this.app.post('/execute/:toolName', async (req, res) => {
      const { toolName } = req.params;
      const args = req.body;

      try {
        let result;

        switch (toolName) {
          case 'read_codex_file':
            result = await this.readFile(args.filePath);
            break;
          case 'list_directory':
            result = await this.listDirectory(args.dirPath || '.');
            break;
          case 'system_status':
            result = await this.getSystemStatus();
            break;
          default:
            throw new Error(`Unknown tool: ${toolName}`);
        }

        res.json({ success: true, result });
      } catch (error) {
        res.status(400).json({
          success: false,
          error: error.message,
        });
      }
    });

    // Stream endpoint for real-time updates
    this.app.get('/stream', (req, res) => {
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');

      const sendEvent = (data) => {
        res.write(`data: ${JSON.stringify(data)}\\n\\n`);
      };

      // Send initial status
      sendEvent({
        type: 'status',
        message: 'Connected to Codex Dominion MCP Server',
        timestamp: new Date().toISOString(),
      });

      // Keep connection alive
      const heartbeat = setInterval(() => {
        sendEvent({
          type: 'heartbeat',
          timestamp: new Date().toISOString(),
        });
      }, 30000);

      req.on('close', () => {
        clearInterval(heartbeat);
      });
    });
  }

  setupWebSocket() {
    this.wss.on('connection', (ws) => {
      console.log('WebSocket client connected');

      ws.send(
        JSON.stringify({
          type: 'welcome',
          message: 'Connected to Codex Dominion MCP Server',
          capabilities: ['file_access', 'system_monitoring', 'real_time_updates'],
        })
      );

      ws.on('message', async (data) => {
        try {
          const message = JSON.parse(data.toString());

          if (message.type === 'tool_request') {
            const result = await this.executeTool(message.tool, message.args);
            ws.send(
              JSON.stringify({
                type: 'tool_response',
                requestId: message.requestId,
                result,
              })
            );
          }
        } catch (error) {
          ws.send(
            JSON.stringify({
              type: 'error',
              message: error.message,
            })
          );
        }
      });

      ws.on('close', () => {
        console.log('WebSocket client disconnected');
      });
    });
  }

  async readFile(filePath) {
    const fullPath = path.resolve(__dirname, filePath);

    // Security check
    if (!fullPath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const content = await fs.readFile(fullPath, 'utf-8');
      return {
        filePath,
        content,
        size: content.length,
        lastModified: (await fs.stat(fullPath)).mtime,
      };
    } catch (error) {
      throw new Error(`Failed to read file: ${error.message}`);
    }
  }

  async listDirectory(dirPath) {
    const fullPath = path.resolve(__dirname, dirPath);

    // Security check
    if (!fullPath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const entries = await fs.readdir(fullPath, { withFileTypes: true });

      return {
        path: dirPath,
        entries: entries.map((entry) => ({
          name: entry.name,
          type: entry.isDirectory() ? 'directory' : 'file',
          hidden: entry.name.startsWith('.'),
        })),
        summary: {
          total: entries.length,
          files: entries.filter((e) => e.isFile()).length,
          directories: entries.filter((e) => e.isDirectory()).length,
        },
      };
    } catch (error) {
      throw new Error(`Failed to list directory: ${error.message}`);
    }
  }

  async getSystemStatus() {
    const checks = {};

    // Check database
    try {
      await fs.access(path.join(__dirname, 'data', 'codex_empire.db'));
      checks.database = { status: 'healthy', message: 'Database accessible' };
    } catch {
      checks.database = { status: 'warning', message: 'Database not found' };
    }

    // Check frontend
    try {
      await fs.access(path.join(__dirname, 'frontend', 'package.json'));
      checks.frontend = { status: 'healthy', message: 'Frontend configured' };
    } catch {
      checks.frontend = { status: 'error', message: 'Frontend missing' };
    }

    // Check backend
    try {
      await fs.access(path.join(__dirname, 'app.py'));
      checks.backend = { status: 'healthy', message: 'Backend available' };
    } catch {
      checks.backend = { status: 'error', message: 'Backend missing' };
    }

    const overallStatus = Object.values(checks).every((c) => c.status === 'healthy')
      ? 'healthy'
      : Object.values(checks).some((c) => c.status === 'error')
        ? 'degraded'
        : 'warning';

    return {
      overall: overallStatus,
      timestamp: new Date().toISOString(),
      checks,
      server: {
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        platform: process.platform,
        nodeVersion: process.version,
      },
    };
  }

  async executeTool(toolName, args) {
    switch (toolName) {
      case 'read_codex_file':
        return await this.readFile(args.filePath);
      case 'list_directory':
        return await this.listDirectory(args.dirPath || '.');
      case 'system_status':
        return await this.getSystemStatus();
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  start() {
    return new Promise((resolve) => {
      this.server.listen(this.port, () => {
        console.log(`✅ Codex Dominion MCP Server running on port ${this.port}`);
        console.log(`🌐 HTTP API: http://localhost:${this.port}`);
        console.log(`🔌 WebSocket: ws://localhost:${this.port}`);
        console.log(`❤️  Health check: http://localhost:${this.port}/health`);
        resolve();
      });
    });
  }

  stop() {
    return new Promise((resolve) => {
      this.server.close(resolve);
    });
  }
}

// Start server if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new CodexDominionHTTPMCPServer(4953);

  server.start().catch((error) => {
    console.error('❌ Failed to start MCP server:', error);
    process.exit(1);
  });

  // Graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\\n🛑 Shutting down MCP server...');
    await server.stop();
    process.exit(0);
  });
}

export default CodexDominionHTTPMCPServer;
