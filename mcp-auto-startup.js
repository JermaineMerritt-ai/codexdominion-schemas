/**
 * MCP Auto-Startup System
 * Automatically starts MCP servers when needed and monitors chat activity
 */

const { spawn, exec } = require('child_process');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
const EventEmitter = require('events');

class MCPAutoStartup extends EventEmitter {
  constructor() {
    super();
    this.mcpServerProcess = null;
    this.monitorProcess = null;
    this.isStarting = false;
    this.serverUrl = 'http://localhost:4953';
    this.chatMonitorActive = false;
    this.lastActivityTime = Date.now();
    this.autoShutdownDelay = 300000; // 5 minutes of inactivity
    this.healthCheckInterval = null;
    this.activityCheckInterval = null;
  }

  async initialize() {
    console.log('🚀 Initializing MCP Auto-Startup System');

    try {
      // Check if dependencies are installed
      await this.checkDependencies();

      // Setup chat activity monitoring
      await this.setupChatMonitoring();

      // Setup automatic shutdown on inactivity
      this.setupInactivityShutdown();

      // Setup graceful shutdown
      this.setupGracefulShutdown();

      console.log('✅ MCP Auto-Startup System initialized');

      // Start server immediately if not running
      await this.ensureServerRunning();
    } catch (error) {
      console.error('❌ Failed to initialize MCP Auto-Startup:', error);
      throw error;
    }
  }

  async checkDependencies() {
    console.log('🔍 Checking dependencies...');

    const packagePath = path.join(__dirname, 'package.json');

    try {
      const packageData = JSON.parse(await fs.readFile(packagePath, 'utf-8'));
      const requiredDeps = ['@modelcontextprotocol/sdk', 'express', 'cors', 'ws', 'axios'];

      const missingDeps = requiredDeps.filter(
        (dep) => !packageData.dependencies?.[dep] && !packageData.devDependencies?.[dep]
      );

      if (missingDeps.length > 0) {
        console.log('📦 Installing missing dependencies:', missingDeps.join(', '));
        await this.installDependencies(missingDeps);
      }

      console.log('✅ All dependencies satisfied');
    } catch (error) {
      console.warn('⚠️ Could not verify dependencies:', error.message);
    }
  }

  async installDependencies(deps) {
    return new Promise((resolve, reject) => {
      const npm = spawn('npm', ['install', ...deps], {
        stdio: 'inherit',
        cwd: __dirname,
      });

      npm.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`npm install failed with code ${code}`));
        }
      });
    });
  }

  async setupChatMonitoring() {
    console.log('💬 Setting up chat activity monitoring');

    // Monitor VS Code chat activity by watching for specific patterns
    this.startChatActivityDetection();

    // Setup HTTP endpoint for external chat systems to notify us
    this.setupChatWebhook();
  }

  startChatActivityDetection() {
    // Watch for chat-related file changes or processes
    const chatIndicators = ['chat.log', 'messages.log', 'conversation.json'];

    // Monitor file system for chat activity
    this.monitorChatFiles(chatIndicators);

    // Monitor process list for chat applications
    this.monitorChatProcesses();
  }

  async monitorChatFiles(files) {
    for (const file of files) {
      const filePath = path.join(__dirname, file);

      try {
        // Watch for file changes
        const watcher = require('fs').watch(filePath, (eventType) => {
          if (eventType === 'change') {
            this.onChatActivity('file_change', filePath);
          }
        });

        console.log(`👁️ Monitoring chat file: ${file}`);
      } catch (error) {
        // File doesn't exist, that's ok
      }
    }
  }

  monitorChatProcesses() {
    setInterval(async () => {
      try {
        // Check for chat-related processes
        const chatProcesses = [
          'code.exe', // VS Code
          'cursor.exe', // Cursor AI
          'copilot', // GitHub Copilot
          'chatgpt', // ChatGPT Desktop
          'claude', // Claude Desktop
        ];

        for (const processName of chatProcesses) {
          const isRunning = await this.isProcessRunning(processName);
          if (isRunning) {
            this.onChatActivity('process_detected', processName);
            break;
          }
        }
      } catch (error) {
        // Ignore process monitoring errors
      }
    }, 10000); // Check every 10 seconds
  }

  async isProcessRunning(processName) {
    return new Promise((resolve) => {
      exec(`tasklist /FI "IMAGENAME eq ${processName}" | find /I "${processName}"`, (error) => {
        resolve(!error);
      });
    });
  }

  setupChatWebhook() {
    // Create a simple HTTP endpoint for external systems to notify us of chat activity
    const express = require('express');
    const app = express();
    const webhookPort = 4954;

    app.use(express.json());

    app.post('/chat-activity', (req, res) => {
      this.onChatActivity('webhook', req.body);
      res.json({ success: true, message: 'Chat activity recorded' });
    });

    app.get('/mcp-status', async (req, res) => {
      const status = await this.getServerStatus();
      res.json(status);
    });

    try {
      app.listen(webhookPort, () => {
        console.log(`🪝 Chat webhook listening on port ${webhookPort}`);
      });
    } catch (error) {
      console.warn('⚠️ Could not start chat webhook:', error.message);
    }
  }

  async onChatActivity(source, details) {
    console.log(`💬 Chat activity detected from ${source}:`, details);

    this.lastActivityTime = Date.now();
    this.emit('chatActivity', {
      source,
      details,
      timestamp: this.lastActivityTime,
    });

    // Enhanced response based on activity type
    const activityPriority = this.getActivityPriority(source);

    if (activityPriority === 'high') {
      console.log('🔥 High priority chat activity - immediate MCP startup');
      await this.ensureServerRunning(true); // Force immediate start
    } else if (activityPriority === 'medium') {
      console.log('⚡ Medium priority chat activity - quick MCP startup');
      await this.ensureServerRunning();
    } else {
      console.log('📊 Low priority activity - deferred MCP check');
      // Defer startup for low priority activities
      setTimeout(() => this.ensureServerRunning(), 2000);
    }

    // Log activity for debugging
    await this.logChatActivity(source, details);
  }

  getActivityPriority(source) {
    // High priority - immediate chat interactions
    const highPriorityPatterns = [
      'copilot_command',
      'vscode_chat_api',
      'copilot_chat_activated',
      'enhanced_command',
      'chat_pattern_detected',
    ];

    // Medium priority - potential chat activity
    const mediumPriorityPatterns = [
      'completion_requested',
      'chat_file_changed',
      'copilot_activated',
      'command',
    ];

    if (highPriorityPatterns.some((pattern) => source.includes(pattern))) {
      return 'high';
    } else if (mediumPriorityPatterns.some((pattern) => source.includes(pattern))) {
      return 'medium';
    } else {
      return 'low';
    }
  }

  async logChatActivity(source, details) {
    try {
      const logEntry = {
        timestamp: new Date().toISOString(),
        source: source,
        details: details,
        serverStatus: this.mcpServerProcess ? 'running' : 'stopped',
      };

      const logPath = path.join(__dirname, 'chat-activity.log');
      await fs.appendFile(logPath, JSON.stringify(logEntry) + '\n');
    } catch (error) {
      // Ignore logging errors
    }
  }

  async ensureServerRunning(forceImmediate = false) {
    if (this.isStarting && !forceImmediate) {
      console.log('⏳ Server startup already in progress...');
      return;
    }

    const isRunning = await this.isServerHealthy();

    if (!isRunning) {
      const startupReason = forceImmediate ? 'immediate chat activity' : 'chat activity';
      console.log(`🚀 Starting MCP server due to ${startupReason}...`);

      if (forceImmediate) {
        // Kill any existing startup process and start fresh
        if (this.mcpServerProcess) {
          this.mcpServerProcess.kill('SIGKILL');
          this.mcpServerProcess = null;
        }
        this.isStarting = false;
      }

      await this.startServer(forceImmediate);
    } else {
      console.log('✅ MCP server already running and healthy');

      // If forced immediate and server is running, ensure it's responsive
      if (forceImmediate) {
        await this.ensureServerResponsive();
      }
    }
  }

  async ensureServerResponsive() {
    try {
      // Send a ping to ensure server is responsive to chat requests
      const response = await axios.post(
        `${this.serverUrl}/ping`,
        {
          source: 'chat_activity',
          timestamp: Date.now(),
        },
        { timeout: 2000 }
      );

      if (response.data.status !== 'pong') {
        console.warn('⚠️ Server not responsive, restarting...');
        await this.restartServer();
      }
    } catch (error) {
      console.warn('⚠️ Server responsiveness check failed, restarting...');
      await this.restartServer();
    }
  }

  async isServerHealthy() {
    try {
      const response = await axios.get(`${this.serverUrl}/health`, {
        timeout: 3000,
      });
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }

  async startServer(immediate = false) {
    if (this.isStarting || this.mcpServerProcess) {
      return;
    }

    this.isStarting = true;

    try {
      const startupMode = immediate ? 'immediate' : 'normal';
      console.log(`🔄 Starting MCP Server (${startupMode} mode)...`);

      // Enhanced environment for chat-responsive mode
      const serverEnv = {
        ...process.env,
        CODEX_MODE: 'CHAT_RESPONSIVE',
        FLAME_ETERNAL: 'true',
        AUTO_START: 'true',
        STARTUP_MODE: startupMode,
        CHAT_PRIORITY: immediate ? 'high' : 'normal',
      };

      // Start the secure MCP server with chat-responsive configuration
      this.mcpServerProcess = spawn('node', ['mcp-server-secure.js'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: __dirname,
        detached: false,
        env: serverEnv,
      });

      // Enhanced logging for chat activity
      this.mcpServerProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.log(`[MCP-SERVER] ${output}`);

          // Detect chat-ready status
          if (output.includes('CHAT_READY') || output.includes('listening')) {
            console.log('🎯 MCP Server is chat-ready!');
          }
        }
      });

      this.mcpServerProcess.stderr.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
          console.error(`[MCP-ERROR] ${output}`);
        }
      });

      this.mcpServerProcess.on('close', (code) => {
        console.log(`[MCP-SERVER] Process exited with code ${code}`);
        this.mcpServerProcess = null;

        // Auto-restart if not intentional shutdown
        if (code !== 0 && !this.isShuttingDown) {
          const delay = immediate ? 2000 : 5000; // Faster restart for immediate mode
          console.log(`🔄 Auto-restarting MCP server after crash in ${delay}ms...`);
          setTimeout(() => this.startServer(immediate), delay);
        }
      });

      // Wait for server to be ready with different timeouts based on mode
      const timeout = immediate ? 15000 : 30000; // Shorter timeout for immediate mode
      await this.waitForServer(timeout);

      console.log(`✅ MCP Server started successfully in ${startupMode} mode`);

      // Start health monitoring
      this.startHealthMonitoring();

      // Notify VS Code integration that server is ready
      this.notifyServerReady();
    } catch (error) {
      console.error('❌ Failed to start MCP server:', error);
      this.mcpServerProcess = null;
      throw error;
    } finally {
      this.isStarting = false;
    }
  }

  async notifyServerReady() {
    try {
      // Notify VS Code extension that MCP server is ready for chat
      const notificationPayload = {
        status: 'ready',
        timestamp: new Date().toISOString(),
        pid: this.mcpServerProcess?.pid,
        mode: 'chat_responsive',
      };

      // Try to notify via file system (fallback method)
      const statusFile = path.join(__dirname, '.mcp-status');
      await fs.writeFile(statusFile, JSON.stringify(notificationPayload));

      console.log('📢 Notified VS Code that MCP server is ready');
    } catch (error) {
      console.log('⚠️ Could not notify VS Code of server readiness:', error.message);
    }
  }

  async waitForServer(maxWaitTime = 30000) {
    const startTime = Date.now();

    while (Date.now() - startTime < maxWaitTime) {
      try {
        const response = await axios.get(`${this.serverUrl}/health`, {
          timeout: 2000,
        });
        if (response.data.status === 'healthy') {
          return true;
        }
      } catch (error) {
        // Server not ready yet, wait a bit more
      }

      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    throw new Error('MCP Server failed to start within timeout period');
  }

  startHealthMonitoring() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    this.healthCheckInterval = setInterval(async () => {
      const isHealthy = await this.isServerHealthy();

      if (!isHealthy && this.mcpServerProcess) {
        console.warn('⚠️ MCP Server health check failed, restarting...');
        this.restartServer();
      }
    }, 15000); // Check every 15 seconds
  }

  setupInactivityShutdown() {
    if (this.activityCheckInterval) {
      clearInterval(this.activityCheckInterval);
    }

    this.activityCheckInterval = setInterval(() => {
      const timeSinceActivity = Date.now() - this.lastActivityTime;

      if (timeSinceActivity > this.autoShutdownDelay && this.mcpServerProcess) {
        console.log('😴 No chat activity detected, shutting down MCP server to save resources...');
        this.stopServer();
      }
    }, 60000); // Check every minute
  }

  async restartServer() {
    console.log('🔄 Restarting MCP server...');
    await this.stopServer();
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Wait 2 seconds
    await this.startServer();
  }

  async stopServer() {
    if (this.mcpServerProcess) {
      console.log('🛑 Stopping MCP server...');

      this.mcpServerProcess.kill('SIGTERM');

      // Wait for graceful shutdown
      await new Promise((resolve) => {
        const timeout = setTimeout(() => {
          if (this.mcpServerProcess) {
            this.mcpServerProcess.kill('SIGKILL');
          }
          resolve();
        }, 5000);

        this.mcpServerProcess.on('close', () => {
          clearTimeout(timeout);
          resolve();
        });
      });

      this.mcpServerProcess = null;
      console.log('✅ MCP server stopped');
    }

    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
  }

  async getServerStatus() {
    const isHealthy = await this.isServerHealthy();

    return {
      running: !!this.mcpServerProcess,
      healthy: isHealthy,
      pid: this.mcpServerProcess?.pid,
      lastActivity: new Date(this.lastActivityTime).toISOString(),
      timeSinceActivity: Date.now() - this.lastActivityTime,
      autoShutdownIn: Math.max(0, this.autoShutdownDelay - (Date.now() - this.lastActivityTime)),
    };
  }

  setupGracefulShutdown() {
    const shutdown = async (signal) => {
      console.log(`\n🛑 Received ${signal}, shutting down gracefully...`);
      this.isShuttingDown = true;

      // Clear intervals
      if (this.healthCheckInterval) {
        clearInterval(this.healthCheckInterval);
      }
      if (this.activityCheckInterval) {
        clearInterval(this.activityCheckInterval);
      }

      // Stop MCP server
      await this.stopServer();

      console.log('✅ Auto-startup system shutdown complete');
      process.exit(0);
    };

    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));

    // Handle Windows-specific shutdown
    if (process.platform === 'win32') {
      process.on('SIGHUP', () => shutdown('SIGHUP'));
    }
  }

  // Method to manually trigger chat activity (for testing)
  triggerChatActivity(source = 'manual') {
    this.onChatActivity(source, 'Manual trigger');
  }

  // Method to get comprehensive system status
  async getSystemStatus() {
    const serverStatus = await this.getServerStatus();

    return {
      autoStartup: {
        active: true,
        lastActivity: new Date(this.lastActivityTime).toISOString(),
        monitoring: {
          chat: true,
          health: !!this.healthCheckInterval,
          inactivity: !!this.activityCheckInterval,
        },
      },
      mcpServer: serverStatus,
      system: {
        platform: process.platform,
        nodeVersion: process.version,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
      },
    };
  }
}

// Auto-start if run directly
if (require.main === module) {
  const autoStartup = new MCPAutoStartup();

  autoStartup.initialize().catch((error) => {
    console.error('💥 Auto-startup system failed:', error);
    process.exit(1);
  });

  // Handle manual triggers via command line
  if (process.argv.includes('--trigger-chat')) {
    autoStartup.triggerChatActivity('command-line');
  }

  if (process.argv.includes('--status')) {
    autoStartup.getSystemStatus().then((status) => {
      console.log('\n📊 System Status:');
      console.log(JSON.stringify(status, null, 2));
    });
  }
}

module.exports = MCPAutoStartup;
