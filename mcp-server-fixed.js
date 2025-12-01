/**
 * Simple MCP Server for Codex Dominion
 * Fixed version using CommonJS for compatibility
 */

const express = require('express');
const cors = require('cors');
const { WebSocketServer } = require('ws');
const { createServer } = require('http');
const fs = require('fs').promises;
const path = require('path');

class CodexDominionMCPServer {
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
        port: this.port,
      });
    });

    // MCP capabilities
    this.app.get('/capabilities', (req, res) => {
      res.json({
        tools: [
          {
            name: 'read_file',
            description: 'Read files from workspace',
          },
          {
            name: 'list_directory',
            description: 'List directory contents',
          },
          {
            name: 'system_status',
            description: 'Get system status',
          },
        ],
      });
    });

    // Test endpoint
    this.app.get('/test', (req, res) => {
      res.json({
        message: 'MCP Server is working correctly',
        timestamp: new Date().toISOString(),
        workspace: __dirname,
      });
    });

    // Execute tool
    this.app.post('/execute/:toolName', async (req, res) => {
      const { toolName } = req.params;
      const args = req.body;

      try {
        let result;

        switch (toolName) {
          case 'read_file':
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
  }

  setupWebSocket() {
    this.wss.on('connection', (ws) => {
      console.log('✅ WebSocket client connected');

      ws.send(
        JSON.stringify({
          type: 'welcome',
          message: 'Connected to Codex Dominion MCP Server',
          capabilities: ['file_access', 'system_monitoring'],
        })
      );

      ws.on('close', () => {
        console.log('❌ WebSocket client disconnected');
      });
    });
  }

  async readFile(filePath) {
    if (!filePath) {
      throw new Error('File path is required');
    }

    const safePath = path.resolve(__dirname, filePath);

    // Security check
    if (!safePath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const content = await fs.readFile(safePath, 'utf-8');
      return {
        filePath,
        content: content.substring(0, 5000), // Limit content size
        size: content.length,
      };
    } catch (error) {
      throw new Error(`Failed to read file: ${error.message}`);
    }
  }

  async listDirectory(dirPath) {
    const safePath = path.resolve(__dirname, dirPath);

    // Security check
    if (!safePath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const entries = await fs.readdir(safePath, { withFileTypes: true });

      return {
        path: dirPath,
        entries: entries.slice(0, 50).map((entry) => ({
          // Limit entries
          name: entry.name,
          type: entry.isDirectory() ? 'directory' : 'file',
        })),
        total: entries.length,
      };
    } catch (error) {
      throw new Error(`Failed to list directory: ${error.message}`);
    }
  }

  async getSystemStatus() {
    const checks = {};

    // Basic file system checks
    try {
      await fs.access(path.join(__dirname, 'package.json'));
      checks.workspace = { status: 'healthy', message: 'Workspace accessible' };
    } catch {
      checks.workspace = { status: 'error', message: 'Workspace issues' };
    }

    return {
      overall: 'healthy',
      timestamp: new Date().toISOString(),
      checks,
      server: {
        port: this.port,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
      },
    };
  }

  start() {
    return new Promise((resolve) => {
      this.server.listen(this.port, () => {
        console.log(`✅ Codex Dominion MCP Server running on port ${this.port}`);
        console.log(`🌐 Health check: http://localhost:${this.port}/health`);
        console.log(`🔧 Test endpoint: http://localhost:${this.port}/test`);
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
if (require.main === module) {
  const server = new CodexDominionMCPServer(4953);

  server.start().catch((error) => {
    console.error('❌ Failed to start MCP server:', error);
    process.exit(1);
  });

  // Graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\n🛑 Shutting down MCP server...');
    await server.stop();
    process.exit(0);
  });
}

module.exports = CodexDominionMCPServer;
