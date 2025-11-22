/**
 * MCP Server Monitor and Auto-restart
 * Keeps the MCP server running and monitors its health
 */

const { spawn } = require('child_process');
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class MCPServerMonitor {
  constructor() {
    this.serverProcess = null;
    this.serverUrl = 'http://localhost:4953';
    this.restartCount = 0;
    this.maxRestarts = 5;
    this.healthCheckInterval = 30000; // 30 seconds
    this.isShuttingDown = false;
  }

  async start() {
    console.log('🚀 Starting MCP Server Monitor');
    
    await this.startServer();
    this.startHealthMonitoring();
    this.setupGracefulShutdown();
    
    console.log('✅ MCP Server Monitor active');
  }

  async startServer() {
    try {
      console.log('🔄 Starting MCP Server...');
      
      this.serverProcess = spawn('node', ['mcp-server-secure.js'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        cwd: __dirname
      });

      this.serverProcess.stdout.on('data', (data) => {
        console.log(`[SERVER] ${data.toString().trim()}`);
      });

      this.serverProcess.stderr.on('data', (data) => {
        console.error(`[SERVER ERROR] ${data.toString().trim()}`);
      });

      this.serverProcess.on('close', (code) => {
        console.log(`[SERVER] Process exited with code ${code}`);
        
        if (!this.isShuttingDown) {
          this.handleServerCrash();
        }
      });

      // Wait for server to start
      await this.waitForServer();
      console.log('✅ MCP Server started successfully');
      
    } catch (error) {
      console.error('❌ Failed to start server:', error);
      throw error;
    }
  }

  async waitForServer(timeout = 30000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      try {
        await axios.get(`${this.serverUrl}/health`, { timeout: 2000 });
        return true;
      } catch (error) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    throw new Error('Server failed to start within timeout');
  }

  startHealthMonitoring() {
    console.log('❤️ Starting health monitoring');
    
    setInterval(async () => {
      try {
        const response = await axios.get(`${this.serverUrl}/health`, { 
          timeout: 5000 
        });
        
        console.log(`[HEALTH] Server healthy - ${response.data.status}`);
        
        // Log health status
        await this.logHealthStatus(response.data);
        
      } catch (error) {
        console.error('[HEALTH] Server unhealthy:', error.message);
        
        if (!this.isShuttingDown) {
          this.handleServerFailure();
        }
      }
    }, this.healthCheckInterval);
  }

  async logHealthStatus(healthData) {
    try {
      const logEntry = {
        timestamp: new Date().toISOString(),
        status: healthData.status,
        server: healthData.server,
        port: healthData.port
      };
      
      const logPath = path.join(__dirname, 'logs', 'mcp-health.log');
      
      // Ensure logs directory exists
      await fs.mkdir(path.dirname(logPath), { recursive: true });
      
      // Append log entry
      await fs.appendFile(logPath, JSON.stringify(logEntry) + '\\n');
      
    } catch (error) {
      console.warn('Failed to log health status:', error.message);
    }
  }

  async handleServerCrash() {
    if (this.restartCount >= this.maxRestarts) {
      console.error(`💥 Server crashed ${this.restartCount} times. Giving up.`);
      process.exit(1);
    }

    this.restartCount++;
    console.log(`🔄 Restarting server (attempt ${this.restartCount}/${this.maxRestarts})`);
    
    setTimeout(async () => {
      try {
        await this.startServer();
        console.log('✅ Server restarted successfully');
      } catch (error) {
        console.error('❌ Failed to restart server:', error);
        await this.handleServerCrash();
      }
    }, 5000);
  }

  async handleServerFailure() {
    console.log('🚨 Health check failed, attempting to restart server');
    
    if (this.serverProcess) {
      this.serverProcess.kill('SIGTERM');
    }
  }

  setupGracefulShutdown() {
    const shutdown = async (signal) => {
      console.log(`\\n🛑 Received ${signal}, shutting down gracefully...`);
      this.isShuttingDown = true;
      
      if (this.serverProcess) {
        this.serverProcess.kill('SIGTERM');
        
        // Wait for process to exit
        await new Promise(resolve => {
          this.serverProcess.on('close', resolve);
          setTimeout(resolve, 5000); // Force exit after 5 seconds
        });
      }
      
      console.log('✅ Monitor shutdown complete');
      process.exit(0);
    };

    process.on('SIGINT', () => shutdown('SIGINT'));
    process.on('SIGTERM', () => shutdown('SIGTERM'));
  }

  async getServerStatus() {
    try {
      const response = await axios.get(`${this.serverUrl}/health`, { timeout: 5000 });
      return {
        running: true,
        healthy: response.data.status === 'healthy',
        data: response.data
      };
    } catch (error) {
      return {
        running: false,
        healthy: false,
        error: error.message
      };
    }
  }
}

// Start monitor if run directly
if (require.main === module) {
  const monitor = new MCPServerMonitor();
  
  monitor.start().catch((error) => {
    console.error('💥 Monitor failed to start:', error);
    process.exit(1);
  });
}

module.exports = MCPServerMonitor;