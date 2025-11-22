#!/usr/bin/env node
/**
 * 🔥 CODEX DOMINION MCP CHAT AUTO-START SYSTEM 🔥
 * Flame eternal, radiance supreme - complete integration launcher
 * 
 * This script ensures MCP servers automatically start when chat messages are sent.
 * Silence eternal, covenant whole, blessed across ages and stars.
 */

import { spawn, exec } from 'child_process';
import fs from 'fs/promises';
import path from 'path';
import chalk from 'chalk';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class MCPChatAutoStartSystem {
  constructor() {
    this.processes = new Map();
    this.isShuttingDown = false;
    this.startupComplete = false;
  }

  async initialize() {
    console.log(chalk.red('🔥 INITIATING CODEX DOMINION MCP CHAT AUTO-START SYSTEM 🔥'));
    console.log(chalk.yellow('⚡ Flame eternal, radiance supreme ⚡'));
    console.log('');

    try {
      // Verify environment
      await this.verifyEnvironment();
      
      // Install VS Code extension integration
      await this.setupVSCodeIntegration();
      
      // Start MCP Auto-Startup System
      await this.startAutoStartupSystem();
      
      // Initialize Chat Message Hooks
      await this.initializeChatHooks();
      
      // Setup monitoring and health checks
      await this.setupMonitoring();
      
      // Register shutdown handlers
      this.setupGracefulShutdown();
      
      console.log('');
      console.log(chalk.green('✅ MCP CHAT AUTO-START SYSTEM FULLY OPERATIONAL'));
      console.log(chalk.yellow('🌟 Covenant whole - chat messages will automatically start MCP servers'));
      console.log(chalk.cyan('📡 Monitoring all VS Code chat activity...'));
      console.log('');
      
      this.startupComplete = true;
      
      // Keep the system running
      this.keepAlive();
      
    } catch (error) {
      console.error(chalk.red('💥 System initialization failed:'), error);
      process.exit(1);
    }
  }

  async verifyEnvironment() {
    console.log(chalk.blue('🔍 Verifying environment...'));
    
    // Check if we're in the right directory
    const requiredFiles = [
      'mcp-auto-startup.js',
      'mcp-vscode-integration.js',
      'chat-message-hooks.js',
      'mcp-server-secure.js'
    ];
    
    for (const file of requiredFiles) {
      try {
        await fs.access(file);
        console.log(chalk.green(`  ✓ ${file} found`));
      } catch (error) {
        throw new Error(`Required file not found: ${file}`);
      }
    }
    
    // Check Node.js version
    const nodeVersion = process.version;
    console.log(chalk.green(`  ✓ Node.js version: ${nodeVersion}`));
    
    // Check for VS Code
    try {
      await this.checkVSCode();
      console.log(chalk.green('  ✓ VS Code detected'));
    } catch (error) {
      console.log(chalk.yellow('  ⚠ VS Code not detected (system will still work)'));
    }
    
    console.log(chalk.green('✅ Environment verification complete'));
  }

  async checkVSCode() {
    return new Promise((resolve, reject) => {
      exec('code --version', (error, stdout) => {
        if (error) {
          reject(error);
        } else {
          resolve(stdout.trim());
        }
      });
    });
  }

  async setupVSCodeIntegration() {
    console.log(chalk.blue('🧩 Setting up VS Code integration...'));
    
    try {
      // Create .vscode directory if it doesn't exist
      await fs.mkdir('.vscode', { recursive: true });
      
      // Verify VS Code settings
      const settingsPath = '.vscode/settings.json';
      try {
        await fs.access(settingsPath);
        console.log(chalk.green('  ✓ VS Code settings found'));
      } catch (error) {
        console.log(chalk.yellow('  ⚠ VS Code settings not found - integration may be limited'));
      }
      
      // Create extension manifest symlink for development
      const manifestPath = '.vscode/extension-manifest.json';
      try {
        await fs.copyFile('extension-manifest.json', manifestPath);
        console.log(chalk.green('  ✓ Extension manifest configured'));
      } catch (error) {
        console.log(chalk.yellow('  ⚠ Could not configure extension manifest'));
      }
      
      console.log(chalk.green('✅ VS Code integration setup complete'));
      
    } catch (error) {
      console.log(chalk.yellow('⚠ VS Code integration setup failed:', error.message));
    }
  }

  async startAutoStartupSystem() {
    console.log(chalk.blue('🚀 Starting MCP Auto-Startup System...'));
    
    return new Promise((resolve, reject) => {
      const autoStartup = spawn('node', ['mcp-auto-startup.js'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: process.cwd(),
        env: {
          ...process.env,
          CODEX_MODE: 'CHAT_RESPONSIVE',
          FLAME_ETERNAL: 'true'
        }
      });

      autoStartup.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.log(chalk.cyan(`[AUTO-STARTUP] ${output}`));
          
          if (output.includes('initialized')) {
            resolve();
          }
        }
      });

      autoStartup.stderr.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.error(chalk.red(`[AUTO-STARTUP-ERROR] ${output}`));
        }
      });

      autoStartup.on('close', (code) => {
        console.log(chalk.yellow(`[AUTO-STARTUP] Process exited with code ${code}`));
        
        if (!this.isShuttingDown && this.startupComplete) {
          console.log(chalk.blue('🔄 Restarting Auto-Startup System...'));
          setTimeout(() => this.startAutoStartupSystem(), 5000);
        }
      });

      this.processes.set('autoStartup', autoStartup);
      
      // Timeout after 30 seconds
      setTimeout(() => {
        if (autoStartup.exitCode === null) {
          console.log(chalk.green('✅ Auto-Startup System appears to be running'));
          resolve();
        }
      }, 30000);
    });
  }

  async initializeChatHooks() {
    console.log(chalk.blue('🎯 Initializing Chat Message Hooks...'));
    
    try {
      // For direct Node.js execution (when VS Code is not available)
      const chatHooks = spawn('node', ['chat-message-hooks.js'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: process.cwd()
      });

      chatHooks.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.log(chalk.magenta(`[CHAT-HOOKS] ${output}`));
        }
      });

      chatHooks.stderr.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.error(chalk.red(`[CHAT-HOOKS-ERROR] ${output}`));
        }
      });

      chatHooks.on('close', (code) => {
        console.log(chalk.yellow(`[CHAT-HOOKS] Process exited with code ${code}`));
        
        if (!this.isShuttingDown && this.startupComplete) {
          console.log(chalk.blue('🔄 Restarting Chat Hooks System...'));
          setTimeout(() => this.initializeChatHooks(), 5000);
        }
      });

      this.processes.set('chatHooks', chatHooks);
      
      console.log(chalk.green('✅ Chat Message Hooks initialized'));
      
    } catch (error) {
      console.log(chalk.yellow('⚠ Chat Hooks initialization failed:', error.message));
    }
  }

  async setupMonitoring() {
    console.log(chalk.blue('📊 Setting up system monitoring...'));
    
    // Monitor system health every 30 seconds
    this.healthCheckInterval = setInterval(async () => {
      await this.performHealthCheck();
    }, 30000);
    
    // Monitor chat activity logs
    this.monitorChatLogs();
    
      // Create status endpoint
      await this.createStatusEndpoint();    console.log(chalk.green('✅ System monitoring active'));
  }

  async performHealthCheck() {
    try {
      const status = {
        timestamp: new Date().toISOString(),
        processes: {},
        system: {
          uptime: process.uptime(),
          memory: process.memoryUsage()
        }
      };
      
      // Check each process
      for (const [name, process] of this.processes) {
        status.processes[name] = {
          running: process.exitCode === null,
          pid: process.pid
        };
      }
      
      // Write status to file for external monitoring
      await fs.writeFile('.mcp-system-status.json', JSON.stringify(status, null, 2));
      
    } catch (error) {
      console.error(chalk.red('❌ Health check failed:'), error.message);
    }
  }

  monitorChatLogs() {
    // Watch for chat activity logs
    const logPath = 'chat-activity.log';
    
    try {
      import('fs').then(fsModule => {
        const watcher = fsModule.default.watch(logPath, (eventType) => {
          if (eventType === 'change') {
            console.log(chalk.cyan('💬 Chat activity detected in logs'));
          }
        });
        
        // Handle watcher errors gracefully
        watcher.on('error', (error) => {
          console.log(chalk.yellow('⚠ Chat log monitoring error:', error.message));
        });
      }).catch(() => {
        // File doesn't exist yet, that's ok
      });
    } catch (error) {
      // Log file doesn't exist yet, that's ok
    }
  }

  async createStatusEndpoint() {
    try {
      const express = await import('express');
      const app = express.default();
      const port = 4955;

      app.get('/status', async (req, res) => {
        try {
          const statusFile = '.mcp-system-status.json';
          const status = JSON.parse(await fs.readFile(statusFile, 'utf-8'));
          res.json({
            success: true,
            ...status,
            chatAutoStart: {
              active: this.startupComplete,
              processes: Array.from(this.processes.keys())
            }
          });
        } catch (error) {
          res.status(500).json({
            success: false,
            error: error.message
          });
        }
      });

      app.get('/trigger-chat', (req, res) => {
        console.log(chalk.yellow('🎯 Manual chat activity trigger received'));
        // Simulate chat activity
        this.simulateChatActivity();
        res.json({ success: true, message: 'Chat activity triggered' });
      });

      app.listen(port, () => {
        console.log(chalk.green(`📡 Status endpoint available at http://localhost:${port}/status`));
      });

    } catch (error) {
      console.log(chalk.yellow('⚠ Could not create status endpoint:', error.message));
    }
  }

  simulateChatActivity() {
    // Write a test entry to chat activity log to trigger MCP startup
    const logEntry = {
      timestamp: new Date().toISOString(),
      source: 'manual_trigger',
      details: 'Manual chat activity simulation',
      serverStatus: 'triggered'
    };
    
    fs.appendFile('chat-activity.log', JSON.stringify(logEntry) + '\n')
      .catch(error => console.log('Could not write to chat log:', error.message));
  }

  keepAlive() {
    // Keep the main process alive
    const keepAliveInterval = setInterval(() => {
      if (this.isShuttingDown) {
        clearInterval(keepAliveInterval);
      }
    }, 60000);
    
    // Print periodic status updates
    setInterval(() => {
      if (!this.isShuttingDown) {
        const activeProcesses = Array.from(this.processes.keys()).length;
        console.log(chalk.dim(`🔥 Codex Dominion MCP System: ${activeProcesses} processes active, flame eternal`));
      }
    }, 300000); // Every 5 minutes
  }

  setupGracefulShutdown() {
    const shutdown = async (signal) => {
      console.log('');
      console.log(chalk.yellow(`🛑 Received ${signal}, shutting down gracefully...`));
      this.isShuttingDown = true;
      
      // Clear intervals
      if (this.healthCheckInterval) {
        clearInterval(this.healthCheckInterval);
      }
      
      // Stop all processes
      for (const [name, process] of this.processes) {
        console.log(chalk.blue(`🛑 Stopping ${name}...`));
        process.kill('SIGTERM');
        
        // Wait for graceful shutdown
        await new Promise(resolve => {
          const timeout = setTimeout(() => {
            process.kill('SIGKILL');
            resolve();
          }, 5000);
          
          process.on('close', () => {
            clearTimeout(timeout);
            resolve();
          });
        });
      }
      
      console.log(chalk.green('✅ MCP Chat Auto-Start System shutdown complete'));
      console.log(chalk.yellow('🌟 Flame eternal rests, radiance supreme endures'));
      process.exit(0);
    };

    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));
    
    if (process.platform === 'win32') {
      process.on('SIGHUP', () => shutdown('SIGHUP'));
    }
  }
}

// Auto-start if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const system = new MCPChatAutoStartSystem();
  system.initialize();
}

export default MCPChatAutoStartSystem;