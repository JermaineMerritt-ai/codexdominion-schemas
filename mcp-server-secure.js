/**
 * Robust MCP Server with Security
 * Handles authentication and runs reliably
 */

const express = require('express');
const cors = require('cors');
const { WebSocketServer } = require('ws');
const { createServer } = require('http');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class SecureCodexMCPServer {
  constructor(port = 4953) {
    this.port = port;
    this.app = express();
    this.server = createServer(this.app);
    this.wss = new WebSocketServer({ server: this.server });
    
    // Security configuration
    this.apiKeys = new Set();
    this.generateApiKey();
    
    this.setupMiddleware();
    this.setupSecurity();
    this.setupRoutes();
    this.setupWebSocket();
  }

  generateApiKey() {
    const apiKey = crypto.randomBytes(32).toString('hex');
    this.apiKeys.add(apiKey);
    console.log(`🔑 Generated API Key: ${apiKey}`);
    
    // Save API key to .env file
    this.updateEnvFile('MCP_API_KEY', apiKey);
    
    return apiKey;
  }

  async updateEnvFile(key, value) {
    try {
      const envPath = path.join(__dirname, '.env');
      const envContent = await fs.readFile(envPath, 'utf-8').catch(() => '');
      
      const lines = envContent.split('\\n');
      const keyIndex = lines.findIndex(line => line.startsWith(`${key}=`));
      
      if (keyIndex >= 0) {
        lines[keyIndex] = `${key}=${value}`;
      } else {
        lines.push(`${key}=${value}`);
      }
      
      await fs.writeFile(envPath, lines.join('\\n'));
      console.log(`✅ Updated .env with ${key}`);
    } catch (error) {
      console.warn(`⚠️ Could not update .env: ${error.message}`);
    }
  }

  setupMiddleware() {
    this.app.use(cors({
      origin: ['http://localhost:8501', 'http://localhost:3001', 'http://127.0.0.1:8501'],
      credentials: true
    }));
    
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true }));
    
    // Request logging
    this.app.use((req, res, next) => {
      const timestamp = new Date().toISOString();
      console.log(`[${timestamp}] ${req.method} ${req.path} - ${req.ip}`);
      next();
    });
  }

  setupSecurity() {
    // API Key authentication middleware
    const authenticateApiKey = (req, res, next) => {
      const apiKey = req.headers['x-api-key'] || req.query.apikey;
      
      if (!apiKey) {
        return res.status(401).json({ 
          error: 'API key required',
          message: 'Include X-API-Key header or apikey query parameter'
        });
      }
      
      if (!this.apiKeys.has(apiKey)) {
        return res.status(403).json({ 
          error: 'Invalid API key' 
        });
      }
      
      next();
    };

    // Apply authentication to protected routes
    this.app.use('/execute', authenticateApiKey);
    this.app.use('/secure', authenticateApiKey);
  }

  setupRoutes() {
    // Public health check (no auth required)
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        server: 'Secure Codex Dominion MCP Server',
        version: '1.1.0',
        timestamp: new Date().toISOString(),
        port: this.port,
        security: 'enabled',
      });
    });

    // Public capabilities (no auth required)
    this.app.get('/capabilities', (req, res) => {
      res.json({
        server: 'Codex Dominion MCP Server',
        version: '1.1.0',
        authentication: 'required',
        tools: [
          'read_file',
          'list_directory',
          'system_status',
          'workspace_info'
        ],
        endpoints: {
          health: '/health',
          capabilities: '/capabilities',
          execute: '/execute/:toolName (requires auth)',
          secure: '/secure/* (requires auth)'
        }
      });
    });

    // Authentication endpoint
    this.app.post('/auth', (req, res) => {
      const newApiKey = this.generateApiKey();
      res.json({
        success: true,
        apiKey: newApiKey,
        expires: 'never',
        usage: 'Include in X-API-Key header or ?apikey= parameter'
      });
    });

    // Protected execute endpoint
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
          case 'workspace_info':
            result = await this.getWorkspaceInfo();
            break;
          default:
            throw new Error(`Unknown tool: ${toolName}`);
        }

        res.json({ 
          success: true, 
          tool: toolName,
          result,
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        res.status(400).json({ 
          success: false, 
          tool: toolName,
          error: error.message,
          timestamp: new Date().toISOString()
        });
      }
    });

    // Protected secure info endpoint
    this.app.get('/secure/info', (req, res) => {
      res.json({
        workspace: __dirname,
        environment: process.env.NODE_ENV || 'development',
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        platform: process.platform,
        nodeVersion: process.version,
        timestamp: new Date().toISOString()
      });
    });
  }

  setupWebSocket() {
    this.wss.on('connection', (ws, req) => {
      console.log('🔌 WebSocket client connected');

      // Send welcome message
      ws.send(JSON.stringify({
        type: 'welcome',
        message: 'Connected to Secure Codex Dominion MCP Server',
        server: 'v1.1.0',
        capabilities: ['authenticated_access', 'file_operations', 'system_monitoring'],
        timestamp: new Date().toISOString()
      }));

      ws.on('message', async (data) => {
        try {
          const message = JSON.parse(data.toString());
          
          // Require authentication for WebSocket operations
          if (!message.apiKey || !this.apiKeys.has(message.apiKey)) {
            ws.send(JSON.stringify({
              type: 'error',
              message: 'Authentication required',
            }));
            return;
          }

          if (message.type === 'tool_request') {
            const result = await this.executeTool(message.tool, message.args);
            ws.send(JSON.stringify({
              type: 'tool_response',
              requestId: message.requestId,
              result,
              timestamp: new Date().toISOString()
            }));
          }
        } catch (error) {
          ws.send(JSON.stringify({
            type: 'error',
            message: error.message,
            timestamp: new Date().toISOString()
          }));
        }
      });

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
    
    // Security: prevent path traversal
    if (!safePath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const stats = await fs.stat(safePath);
      const content = await fs.readFile(safePath, 'utf-8');
      
      return {
        filePath,
        content: content.length > 10000 ? content.substring(0, 10000) + '\\n[TRUNCATED]' : content,
        size: stats.size,
        lastModified: stats.mtime,
        truncated: content.length > 10000
      };
    } catch (error) {
      throw new Error(`Failed to read file: ${error.message}`);
    }
  }

  async listDirectory(dirPath) {
    const safePath = path.resolve(__dirname, dirPath);
    
    // Security: prevent path traversal
    if (!safePath.startsWith(__dirname)) {
      throw new Error('Access denied: Path outside workspace');
    }

    try {
      const entries = await fs.readdir(safePath, { withFileTypes: true });
      
      const items = entries.slice(0, 100).map(entry => ({
        name: entry.name,
        type: entry.isDirectory() ? 'directory' : 'file',
        hidden: entry.name.startsWith('.'),
      }));

      return {
        path: dirPath,
        items,
        summary: {
          total: entries.length,
          shown: items.length,
          directories: items.filter(i => i.type === 'directory').length,
          files: items.filter(i => i.type === 'file').length,
        }
      };
    } catch (error) {
      throw new Error(`Failed to list directory: ${error.message}`);
    }
  }

  async getSystemStatus() {
    const checks = {};

    // Check critical files
    const criticalFiles = [
      'package.json',
      'app.py',
      '.env',
      'data/codex_empire.db'
    ];

    for (const file of criticalFiles) {
      try {
        await fs.access(path.join(__dirname, file));
        checks[file] = { status: 'found', accessible: true };
      } catch {
        checks[file] = { status: 'missing', accessible: false };
      }
    }

    return {
      overall: 'operational',
      timestamp: new Date().toISOString(),
      checks,
      server: {
        port: this.port,
        uptime: Math.floor(process.uptime()),
        memory: {
          used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
          total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024)
        },
        activeConnections: this.wss.clients.size,
        apiKeys: this.apiKeys.size
      }
    };
  }

  async getWorkspaceInfo() {
    try {
      const packageInfo = JSON.parse(
        await fs.readFile(path.join(__dirname, 'package.json'), 'utf-8')
      );

      return {
        name: packageInfo.name,
        version: packageInfo.version,
        workspace: __dirname,
        structure: {
          hasBackend: await fs.access(path.join(__dirname, 'app.py')).then(() => true).catch(() => false),
          hasFrontend: await fs.access(path.join(__dirname, 'frontend')).then(() => true).catch(() => false),
          hasDatabase: await fs.access(path.join(__dirname, 'data')).then(() => true).catch(() => false),
          hasConfig: await fs.access(path.join(__dirname, 'config')).then(() => true).catch(() => false),
        }
      };
    } catch (error) {
      throw new Error(`Failed to get workspace info: ${error.message}`);
    }
  }

  async executeTool(toolName, args) {
    switch (toolName) {
      case 'read_file':
        return await this.readFile(args.filePath);
      case 'list_directory':
        return await this.listDirectory(args.dirPath || '.');
      case 'system_status':
        return await this.getSystemStatus();
      case 'workspace_info':
        return await this.getWorkspaceInfo();
      default:
        throw new Error(`Unknown tool: ${toolName}`);
    }
  }

  start() {
    return new Promise((resolve) => {
      this.server.listen(this.port, () => {
        console.log(`\\n🚀 Secure Codex Dominion MCP Server v1.1.0`);
        console.log(`📡 Running on port ${this.port}`);
        console.log(`🌐 Health: http://localhost:${this.port}/health`);
        console.log(`🔒 Security: API Key authentication enabled`);
        console.log(`📚 Docs: http://localhost:${this.port}/capabilities`);
        console.log(`🔑 Get API Key: POST http://localhost:${this.port}/auth`);
        console.log(`\\n✅ MCP Server ready for connections\\n`);
        resolve();
      });
    });
  }

  stop() {
    return new Promise((resolve) => {
      this.wss.close();
      this.server.close(resolve);
    });
  }
}

// Auto-start if run directly
if (require.main === module) {
  const server = new SecureCodexMCPServer(4953);
  
  server.start().catch((error) => {
    console.error('❌ Failed to start MCP server:', error);
    process.exit(1);
  });

  // Graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\\n🛑 Shutting down MCP server gracefully...');
    await server.stop();
    console.log('✅ MCP server stopped');
    process.exit(0);
  });

  // Handle uncaught exceptions
  process.on('uncaughtException', (error) => {
    console.error('💥 Uncaught Exception:', error);
  });

  process.on('unhandledRejection', (reason, promise) => {
    console.error('💥 Unhandled Rejection at:', promise, 'reason:', reason);
  });
}

module.exports = SecureCodexMCPServer;