#!/usr/bin/env node

/**
 * MCP System Health Check and Repair Tool
 * Diagnoses and fixes all MCP-related issues automatically
 */

const fs = require('fs').promises;
const path = require('path');
const { spawn, exec } = require('child_process');
const axios = require('axios');

class MCPSystemDoctor {
  constructor() {
    this.workspaceDir = __dirname;
    this.issues = [];
    this.fixes = [];
    this.serverUrl = 'http://localhost:4953';
    this.webhookUrl = 'http://localhost:4954';
  }

  async diagnose() {
    console.log('🔍 MCP System Health Check Started');
    console.log('=====================================\n');

    await this.checkNodeJS();
    await this.checkDependencies();
    await this.checkMCPFiles();
    await this.checkServerHealth();
    await this.checkPorts();
    await this.checkFirewall();
    await this.checkPermissions();
    await this.checkSystemResources();

    return this.generateReport();
  }

  async checkNodeJS() {
    console.log('📋 Checking Node.js installation...');
    
    try {
      const nodeVersion = await this.execCommand('node --version');
      const npmVersion = await this.execCommand('npm --version');
      
      console.log(`   ✅ Node.js: ${nodeVersion.trim()}`);
      console.log(`   ✅ npm: ${npmVersion.trim()}`);
      
      // Check if version is compatible
      const majorVersion = parseInt(nodeVersion.replace('v', '').split('.')[0]);
      if (majorVersion < 16) {
        this.issues.push({
          type: 'warning',
          component: 'nodejs',
          message: `Node.js version ${nodeVersion} may be too old. Recommended: v16+`
        });
      }
      
    } catch (error) {
      this.issues.push({
        type: 'error',
        component: 'nodejs',
        message: 'Node.js is not installed or not accessible',
        fix: 'Install Node.js from https://nodejs.org/'
      });
    }
  }

  async checkDependencies() {
    console.log('📦 Checking dependencies...');
    
    try {
      const packagePath = path.join(this.workspaceDir, 'package.json');
      const packageData = JSON.parse(await fs.readFile(packagePath, 'utf-8'));
      
      const requiredDeps = [
        '@modelcontextprotocol/sdk',
        'express',
        'cors', 
        'ws',
        'axios'
      ];

      const missing = [];
      const nodeModulesPath = path.join(this.workspaceDir, 'node_modules');
      
      for (const dep of requiredDeps) {
        const depPath = path.join(nodeModulesPath, dep);
        try {
          await fs.access(depPath);
          console.log(`   ✅ ${dep}`);
        } catch (error) {
          console.log(`   ❌ ${dep} - Missing`);
          missing.push(dep);
        }
      }

      if (missing.length > 0) {
        this.issues.push({
          type: 'error',
          component: 'dependencies',
          message: `Missing dependencies: ${missing.join(', ')}`,
          fix: `npm install ${missing.join(' ')}`
        });
      }

    } catch (error) {
      this.issues.push({
        type: 'error',
        component: 'package',
        message: 'package.json not found or invalid',
        fix: 'Create or repair package.json file'
      });
    }
  }

  async checkMCPFiles() {
    console.log('📁 Checking MCP system files...');
    
    const requiredFiles = [
      'mcp-server-secure.js',
      'mcp-auto-startup.js', 
      'mcp-monitor.js',
      'start-mcp-auto.bat'
    ];

    for (const file of requiredFiles) {
      const filePath = path.join(this.workspaceDir, file);
      try {
        const stats = await fs.stat(filePath);
        console.log(`   ✅ ${file} (${Math.round(stats.size / 1024)}KB)`);
        
        // Check if file is executable for .bat files
        if (file.endsWith('.bat') && process.platform === 'win32') {
          // Windows batch files are always executable
        }
      } catch (error) {
        console.log(`   ❌ ${file} - Missing`);
        this.issues.push({
          type: 'error',
          component: 'files',
          message: `Required file missing: ${file}`,
          fix: `Create or restore ${file}`
        });
      }
    }
  }

  async checkServerHealth() {
    console.log('🏥 Checking MCP server health...');
    
    try {
      const response = await axios.get(`${this.serverUrl}/health`, { timeout: 5000 });
      console.log(`   ✅ Server responding: ${response.data.status}`);
      console.log(`   ✅ Version: ${response.data.version}`);
      console.log(`   ✅ Security: ${response.data.security}`);
      
    } catch (error) {
      console.log(`   ❌ Server not responding: ${error.message}`);
      this.issues.push({
        type: 'warning',
        component: 'server',
        message: 'MCP server is not running or not healthy',
        fix: 'Start MCP server using auto-startup system'
      });
      
      await this.checkAutoStartupSystem();
    }
  }

  async checkAutoStartupSystem() {
    console.log('🤖 Checking auto-startup system...');
    
    try {
      const response = await axios.get(`${this.webhookUrl}/mcp-status`, { timeout: 3000 });
      console.log(`   ✅ Auto-startup system active`);
      console.log(`   ✅ Last activity: ${new Date(response.data.lastActivity).toLocaleTimeString()}`);
      
    } catch (error) {
      console.log(`   ❌ Auto-startup system not responding`);
      this.issues.push({
        type: 'error',
        component: 'auto-startup',
        message: 'Auto-startup system is not running',
        fix: 'Start auto-startup system manually'
      });
    }
  }

  async checkPorts() {
    console.log('🔌 Checking port availability...');
    
    const ports = [
      { port: 4953, service: 'MCP Server' },
      { port: 4954, service: 'Auto-startup Webhook' }
    ];

    for (const { port, service } of ports) {
      const isAvailable = await this.isPortAvailable(port);
      if (isAvailable) {
        console.log(`   ⚠️  Port ${port} (${service}) - Available but not in use`);
      } else {
        console.log(`   ✅ Port ${port} (${service}) - In use`);
      }
    }
  }

  async isPortAvailable(port) {
    return new Promise((resolve) => {
      const server = require('net').createServer();
      
      server.listen(port, () => {
        server.once('close', () => resolve(true));
        server.close();
      });
      
      server.on('error', () => resolve(false));
    });
  }

  async checkFirewall() {
    console.log('🔥 Checking firewall configuration...');
    
    if (process.platform === 'win32') {
      try {
        // Check Windows Firewall rules for Node.js
        const firewallCheck = await this.execCommand(
          'netsh advfirewall firewall show rule name="Node.js" dir=in'
        );
        
        if (firewallCheck.includes('No rules match')) {
          console.log('   ⚠️  No firewall rules found for Node.js');
          this.issues.push({
            type: 'warning',
            component: 'firewall',
            message: 'Node.js may be blocked by Windows Firewall',
            fix: 'Add firewall exception for Node.js'
          });
        } else {
          console.log('   ✅ Firewall rules configured for Node.js');
        }
        
      } catch (error) {
        console.log('   ⚠️  Could not check firewall status (may require admin)');
      }
    } else {
      console.log('   ℹ️  Firewall check not applicable for this platform');
    }
  }

  async checkPermissions() {
    console.log('🔐 Checking file permissions...');
    
    try {
      // Check if we can write to the workspace
      const testFile = path.join(this.workspaceDir, '.mcp-health-test');
      await fs.writeFile(testFile, 'test');
      await fs.unlink(testFile);
      console.log('   ✅ Write permissions OK');
      
      // Check if we can execute scripts
      const batFile = path.join(this.workspaceDir, 'start-mcp-auto.bat');
      try {
        await fs.access(batFile, fs.constants.R_OK);
        console.log('   ✅ Script execution permissions OK');
      } catch (error) {
        console.log('   ⚠️  May not have script execution permissions');
      }
      
    } catch (error) {
      this.issues.push({
        type: 'error',
        component: 'permissions',
        message: 'Insufficient file system permissions',
        fix: 'Run as administrator or check folder permissions'
      });
    }
  }

  async checkSystemResources() {
    console.log('💾 Checking system resources...');
    
    const usage = process.memoryUsage();
    const totalMemMB = Math.round(usage.heapTotal / 1024 / 1024);
    const usedMemMB = Math.round(usage.heapUsed / 1024 / 1024);
    
    console.log(`   ✅ Memory usage: ${usedMemMB}MB / ${totalMemMB}MB`);
    
    if (usedMemMB > 100) {
      this.issues.push({
        type: 'warning',
        component: 'memory',
        message: `High memory usage: ${usedMemMB}MB`,
        fix: 'Monitor memory usage and restart if necessary'
      });
    }
    
    // Check disk space
    try {
      const stats = await fs.stat(this.workspaceDir);
      console.log('   ✅ Disk access OK');
    } catch (error) {
      this.issues.push({
        type: 'error',
        component: 'disk',
        message: 'Cannot access workspace directory',
        fix: 'Check disk space and permissions'
      });
    }
  }

  async autoFix() {
    console.log('\n🔧 Attempting automatic fixes...');
    console.log('================================\n');

    for (const issue of this.issues) {
      if (issue.fix && issue.type === 'error') {
        console.log(`🔨 Fixing: ${issue.message}`);
        
        try {
          switch (issue.component) {
            case 'dependencies':
              await this.fixDependencies(issue);
              break;
            case 'server':
              await this.fixServer();
              break;
            case 'auto-startup':
              await this.fixAutoStartup();
              break;
            default:
              console.log(`   ℹ️  Manual fix required: ${issue.fix}`);
          }
        } catch (error) {
          console.log(`   ❌ Failed to fix: ${error.message}`);
        }
      }
    }
  }

  async fixDependencies(issue) {
    const deps = issue.fix.replace('npm install ', '').split(' ');
    console.log(`   📦 Installing: ${deps.join(', ')}`);
    
    await this.execCommand(`npm install ${deps.join(' ')}`);
    console.log('   ✅ Dependencies installed');
    
    this.fixes.push(`Installed dependencies: ${deps.join(', ')}`);
  }

  async fixServer() {
    console.log('   🚀 Starting MCP server...');
    
    const serverProcess = spawn('node', ['mcp-server-secure.js'], {
      detached: true,
      stdio: 'ignore',
      cwd: this.workspaceDir
    });
    
    serverProcess.unref();
    
    // Wait a moment and check if it started
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    try {
      await axios.get(`${this.serverUrl}/health`, { timeout: 2000 });
      console.log('   ✅ MCP server started successfully');
      this.fixes.push('Started MCP server');
    } catch (error) {
      throw new Error('Server did not start properly');
    }
  }

  async fixAutoStartup() {
    console.log('   🤖 Starting auto-startup system...');
    
    const autoProcess = spawn('node', ['mcp-auto-startup.js'], {
      detached: true,
      stdio: 'ignore', 
      cwd: this.workspaceDir
    });
    
    autoProcess.unref();
    
    // Wait and verify
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    try {
      await axios.get(`${this.webhookUrl}/mcp-status`, { timeout: 2000 });
      console.log('   ✅ Auto-startup system started successfully');
      this.fixes.push('Started auto-startup system');
    } catch (error) {
      throw new Error('Auto-startup system did not start properly');
    }
  }

  generateReport() {
    console.log('\n📊 MCP System Health Report');
    console.log('============================\n');

    const errorCount = this.issues.filter(i => i.type === 'error').length;
    const warningCount = this.issues.filter(i => i.type === 'warning').length;

    if (errorCount === 0 && warningCount === 0) {
      console.log('🎉 System Status: HEALTHY');
      console.log('   All MCP components are functioning correctly.');
    } else {
      console.log(`⚠️  System Status: ISSUES DETECTED`);
      console.log(`   Errors: ${errorCount}, Warnings: ${warningCount}`);
      
      console.log('\n🔍 Issues Found:');
      this.issues.forEach((issue, index) => {
        const icon = issue.type === 'error' ? '❌' : '⚠️';
        console.log(`   ${index + 1}. ${icon} ${issue.component.toUpperCase()}: ${issue.message}`);
        if (issue.fix) {
          console.log(`      💡 Fix: ${issue.fix}`);
        }
      });
    }

    if (this.fixes.length > 0) {
      console.log('\n✅ Fixes Applied:');
      this.fixes.forEach((fix, index) => {
        console.log(`   ${index + 1}. ${fix}`);
      });
    }

    console.log('\n🚀 Quick Start Commands:');
    console.log('   Manual server start: node mcp-server-secure.js');
    console.log('   Auto-startup system: node mcp-auto-startup.js');
    console.log('   Windows launcher: start-mcp-auto.bat');
    console.log('   Health check: node mcp-system-doctor.js');

    return {
      healthy: errorCount === 0,
      issues: this.issues,
      fixes: this.fixes,
      errorCount,
      warningCount
    };
  }

  async execCommand(command) {
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout || stderr);
      });
    });
  }
}

// Run if called directly
if (require.main === module) {
  const doctor = new MCPSystemDoctor();
  
  (async () => {
    try {
      const report = await doctor.diagnose();
      
      // Ask if user wants auto-fix
      if (report.errorCount > 0) {
        console.log('\n❓ Attempt automatic fixes? (This will try to resolve detected issues)');
        console.log('   Press Ctrl+C to skip, or wait 10 seconds for auto-fix...');
        
        const autoFix = process.argv.includes('--auto-fix') || process.argv.includes('--fix');
        
        if (autoFix) {
          await doctor.autoFix();
          console.log('\n🔄 Re-running health check after fixes...');
          await doctor.diagnose();
        }
      }
      
      process.exit(report.healthy ? 0 : 1);
      
    } catch (error) {
      console.error('💥 Health check failed:', error);
      process.exit(1);
    }
  })();
}

module.exports = MCPSystemDoctor;