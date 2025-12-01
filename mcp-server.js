#!/usr/bin/env node

/**
 * Codex Dominion MCP Server
 * Model Context Protocol server implementation for the Codex Dominion system
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class CodexDominionMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'codex-dominion-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'read_codex_file',
            description: 'Read files from the Codex Dominion workspace',
            inputSchema: {
              type: 'object',
              properties: {
                filePath: {
                  type: 'string',
                  description: 'Path to the file to read (relative to workspace root)',
                },
              },
              required: ['filePath'],
            },
          },
          {
            name: 'list_codex_directory',
            description: 'List contents of a directory in the Codex Dominion workspace',
            inputSchema: {
              type: 'object',
              properties: {
                dirPath: {
                  type: 'string',
                  description: 'Path to the directory to list (relative to workspace root)',
                  default: '.',
                },
              },
            },
          },
          {
            name: 'check_codex_status',
            description: 'Check the operational status of Codex Dominion systems',
            inputSchema: {
              type: 'object',
              properties: {
                component: {
                  type: 'string',
                  enum: ['database', 'frontend', 'backend', 'all'],
                  description: 'Component to check status for',
                  default: 'all',
                },
              },
            },
          },
          {
            name: 'get_system_info',
            description: 'Get comprehensive system information',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
        ],
      };
    });

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'read_codex_file':
            return await this.readCodexFile(args.filePath);

          case 'list_codex_directory':
            return await this.listCodexDirectory(args.dirPath || '.');

          case 'check_codex_status':
            return await this.checkCodexStatus(args.component || 'all');

          case 'get_system_info':
            return await this.getSystemInfo();

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error executing ${name}: ${error.message}`,
            },
          ],
        };
      }
    });
  }

  async readCodexFile(filePath) {
    try {
      const fullPath = path.resolve(__dirname, filePath);

      // Security check: ensure path is within workspace
      if (!fullPath.startsWith(__dirname)) {
        throw new Error('Access denied: Path outside workspace');
      }

      const content = await fs.readFile(fullPath, 'utf-8');

      return {
        content: [
          {
            type: 'text',
            text: `File: ${filePath}\n\n${content}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Failed to read file ${filePath}: ${error.message}`);
    }
  }

  async listCodexDirectory(dirPath) {
    try {
      const fullPath = path.resolve(__dirname, dirPath);

      // Security check: ensure path is within workspace
      if (!fullPath.startsWith(__dirname)) {
        throw new Error('Access denied: Path outside workspace');
      }

      const entries = await fs.readdir(fullPath, { withFileTypes: true });

      const items = entries.map((entry) => ({
        name: entry.name,
        type: entry.isDirectory() ? 'directory' : 'file',
        isHidden: entry.name.startsWith('.'),
      }));

      const summary = {
        path: dirPath,
        totalItems: items.length,
        directories: items.filter((item) => item.type === 'directory').length,
        files: items.filter((item) => item.type === 'file').length,
      };

      return {
        content: [
          {
            type: 'text',
            text: `Directory: ${dirPath}\n\nSummary:\n- Total items: ${summary.totalItems}\n- Directories: ${summary.directories}\n- Files: ${summary.files}\n\nContents:\n${items.map((item) => `${item.type === 'directory' ? '📁' : '📄'} ${item.name}`).join('\n')}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Failed to list directory ${dirPath}: ${error.message}`);
    }
  }

  async checkCodexStatus(component) {
    const status = {
      timestamp: new Date().toISOString(),
      overall: 'operational',
      components: {},
    };

    try {
      // Check database
      if (component === 'all' || component === 'database') {
        try {
          await fs.access(path.join(__dirname, 'data', 'codex_empire.db'));
          status.components.database = {
            status: 'operational',
            message: 'Database file accessible',
          };
        } catch {
          status.components.database = {
            status: 'warning',
            message: 'Database file not found',
          };
        }
      }

      // Check frontend
      if (component === 'all' || component === 'frontend') {
        try {
          await fs.access(path.join(__dirname, 'frontend', 'package.json'));
          status.components.frontend = {
            status: 'operational',
            message: 'Frontend configuration found',
          };
        } catch {
          status.components.frontend = {
            status: 'error',
            message: 'Frontend not configured',
          };
        }
      }

      // Check backend
      if (component === 'all' || component === 'backend') {
        try {
          await fs.access(path.join(__dirname, 'app.py'));
          status.components.backend = {
            status: 'operational',
            message: 'Backend application found',
          };
        } catch {
          status.components.backend = {
            status: 'error',
            message: 'Backend application not found',
          };
        }
      }

      // Determine overall status
      const componentStatuses = Object.values(status.components).map((c) => c.status);
      if (componentStatuses.includes('error')) {
        status.overall = 'degraded';
      } else if (componentStatuses.includes('warning')) {
        status.overall = 'warning';
      }

      return {
        content: [
          {
            type: 'text',
            text: `Codex Dominion System Status\n\nOverall: ${status.overall.toUpperCase()}\nTimestamp: ${status.timestamp}\n\nComponents:\n${Object.entries(
              status.components
            )
              .map(([name, info]) => `- ${name}: ${info.status.toUpperCase()} - ${info.message}`)
              .join('\n')}`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Status check failed: ${error.message}`);
    }
  }

  async getSystemInfo() {
    const info = {
      server: {
        name: 'Codex Dominion MCP Server',
        version: '1.0.0',
        protocol: 'Model Context Protocol',
      },
      workspace: {
        root: __dirname,
        platform: process.platform,
        nodeVersion: process.version,
      },
      capabilities: {
        fileAccess: true,
        statusMonitoring: true,
        securityRestricted: true,
      },
      timestamp: new Date().toISOString(),
    };

    return {
      content: [
        {
          type: 'text',
          text: `Codex Dominion MCP Server Information\n\n${JSON.stringify(info, null, 2)}`,
        },
      ],
    };
  }

  setupErrorHandling() {
    this.server.onerror = (error) => {
      console.error('[MCP Server Error]:', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Codex Dominion MCP Server started successfully');
  }
}

// Start the server
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new CodexDominionMCPServer();
  server.start().catch((error) => {
    console.error('Failed to start MCP server:', error);
    process.exit(1);
  });
}

export default CodexDominionMCPServer;
