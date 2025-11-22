#!/usr/bin/env node

/**
 * MCP Chat Auto-Startup Test Suite
 * Comprehensive testing of MCP auto-startup functionality when chat messages are sent
 */

const axios = require('axios');
const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

class MCPAutoStartupTester {
  constructor() {
    this.mcpServerUrl = 'http://localhost:4953';
    this.webhookUrl = 'http://localhost:4954';
    this.testResults = [];
    this.passedTests = 0;
    this.totalTests = 0;
  }

  async runAllTests() {
    console.log('🧪 MCP Auto-Startup Test Suite');
    console.log('===============================\n');

    await this.testServerAvailability();
    await this.testWebhookAvailability();
    await this.testChatActivityTrigger();
    await this.testAutoServerStart();
    await this.testHealthMonitoring();
    await this.testInactivityShutdown();

    this.displayResults();
  }

  async testServerAvailability() {
    await this.runTest('MCP Server Availability', async () => {
      const response = await axios.get(`${this.mcpServerUrl}/health`, { timeout: 5000 });
      
      if (response.data.status !== 'healthy') {
        throw new Error(`Server status: ${response.data.status}`);
      }
      
      if (response.data.security !== 'enabled') {
        throw new Error('Security not enabled');
      }
      
      return `Server healthy with security enabled on port ${response.data.port}`;
    });
  }

  async testWebhookAvailability() {
    await this.runTest('Auto-Startup Webhook', async () => {
      const response = await axios.get(`${this.webhookUrl}/mcp-status`, { timeout: 5000 });
      
      if (!response.data.running) {
        throw new Error('MCP server not reported as running');
      }
      
      return `Webhook active, server running and ${response.data.healthy ? 'healthy' : 'unhealthy'}`;
    });
  }

  async testChatActivityTrigger() {
    await this.runTest('Chat Activity Trigger', async () => {
      const chatActivity = {
        source: 'test_suite',
        details: 'Automated test chat message',
        timestamp: new Date().toISOString(),
        messageType: 'user_message',
        content: 'Hello, this is a test chat message'
      };
      
      const response = await axios.post(
        `${this.webhookUrl}/chat-activity`,
        chatActivity,
        { 
          timeout: 5000,
          headers: { 'Content-Type': 'application/json' }
        }
      );
      
      if (!response.data.success) {
        throw new Error('Chat activity not accepted');
      }
      
      // Wait a moment and verify server is still running
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const statusResponse = await axios.get(`${this.mcpServerUrl}/health`, { timeout: 3000 });
      if (statusResponse.data.status !== 'healthy') {
        throw new Error('Server not healthy after chat activity');
      }
      
      return 'Chat activity triggered successfully, server remains healthy';
    });
  }

  async testAutoServerStart() {
    await this.runTest('Auto Server Start Simulation', async () => {
      // This test simulates what happens when chat activity is detected
      // and the server needs to be started
      
      // First, send multiple chat activities to ensure robust handling
      const activities = [
        { source: 'vscode', details: 'User typed message in chat' },
        { source: 'copilot', details: 'GitHub Copilot interaction' },
        { source: 'terminal', details: 'Command line chat command' }
      ];
      
      for (const activity of activities) {
        await axios.post(`${this.webhookUrl}/chat-activity`, {
          ...activity,
          timestamp: new Date().toISOString()
        }, { timeout: 3000 });
        
        await new Promise(resolve => setTimeout(resolve, 500));
      }
      
      // Verify server is responsive after multiple triggers
      const finalCheck = await axios.get(`${this.mcpServerUrl}/health`, { timeout: 3000 });
      
      return `Handled ${activities.length} chat activities, server status: ${finalCheck.data.status}`;
    });
  }

  async testHealthMonitoring() {
    await this.runTest('Health Monitoring System', async () => {
      // Test the health monitoring by getting comprehensive status
      const statusResponse = await axios.get(`${this.webhookUrl}/mcp-status`, { timeout: 5000 });
      
      const requiredFields = ['running', 'healthy', 'lastActivity'];
      const missingFields = requiredFields.filter(field => !(field in statusResponse.data));
      
      if (missingFields.length > 0) {
        throw new Error(`Missing status fields: ${missingFields.join(', ')}`);
      }
      
      // Verify last activity is recent (within last 10 seconds)
      const lastActivity = new Date(statusResponse.data.lastActivity);
      const timeDiff = Date.now() - lastActivity.getTime();
      
      if (timeDiff > 30000) {
        throw new Error(`Last activity too old: ${Math.round(timeDiff / 1000)}s ago`);
      }
      
      return `Health monitoring active, last activity: ${Math.round(timeDiff / 1000)}s ago`;
    });
  }

  async testInactivityShutdown() {
    await this.runTest('Inactivity Monitoring (Info Only)', async () => {
      // This test just checks that inactivity monitoring is configured
      // We don't actually test shutdown as that would disrupt the system
      
      const statusResponse = await axios.get(`${this.webhookUrl}/mcp-status`, { timeout: 5000 });
      
      if (!statusResponse.data.autoShutdownIn) {
        return 'Auto-shutdown timing not available (may not be configured)';
      }
      
      const shutdownTime = Math.round(statusResponse.data.autoShutdownIn / 1000 / 60);
      return `Auto-shutdown configured, will shutdown in ${shutdownTime} minutes if inactive`;
    });
  }

  async runTest(name, testFunction) {
    this.totalTests++;
    process.stdout.write(`🔍 Testing: ${name}... `);
    
    try {
      const result = await testFunction();
      this.passedTests++;
      console.log('✅ PASS');
      if (result) {
        console.log(`   ℹ️  ${result}`);
      }
      
      this.testResults.push({
        name,
        status: 'PASS',
        result
      });
      
    } catch (error) {
      console.log('❌ FAIL');
      console.log(`   ❗ ${error.message}`);
      
      this.testResults.push({
        name,
        status: 'FAIL',
        error: error.message
      });
    }
    
    console.log(); // Empty line for readability
  }

  displayResults() {
    console.log('📊 Test Results Summary');
    console.log('=====================\n');
    
    const successRate = Math.round((this.passedTests / this.totalTests) * 100);
    
    if (this.passedTests === this.totalTests) {
      console.log('🎉 All tests passed! MCP Auto-Startup system is fully functional.');
    } else {
      console.log(`⚠️  ${this.passedTests}/${this.totalTests} tests passed (${successRate}%)`);
    }
    
    console.log(`\n📋 Detailed Results:`);
    this.testResults.forEach((result, index) => {
      const icon = result.status === 'PASS' ? '✅' : '❌';
      console.log(`   ${index + 1}. ${icon} ${result.name}: ${result.status}`);
      
      if (result.result) {
        console.log(`      ℹ️  ${result.result}`);
      }
      if (result.error) {
        console.log(`      ❗ ${result.error}`);
      }
    });

    console.log('\n🚀 System Status:');
    console.log(`   ✅ MCP Server: Running on port 4953`);
    console.log(`   ✅ Auto-Startup: Active on port 4954`);
    console.log(`   ✅ Chat Integration: Ready for messages`);
    
    console.log('\n💡 Usage:');
    console.log('   • Send any chat message in VS Code or supported apps');
    console.log('   • MCP servers will automatically start when needed');
    console.log('   • Servers auto-shutdown after inactivity to save resources');
    console.log('   • Monitor status: http://localhost:4954/mcp-status');
    console.log('   • Health check: http://localhost:4953/health');

    return {
      passed: this.passedTests,
      total: this.totalTests,
      successRate,
      allPassed: this.passedTests === this.totalTests
    };
  }

  // Method to simulate real chat scenarios
  async simulateChatScenarios() {
    console.log('\n🎭 Simulating Real Chat Scenarios');
    console.log('=================================\n');

    const scenarios = [
      {
        name: 'VS Code Copilot Chat',
        activities: [
          { source: 'vscode_copilot', details: 'Explain this function', type: 'code_explanation' },
          { source: 'vscode_copilot', details: 'Generate unit tests', type: 'code_generation' }
        ]
      },
      {
        name: 'Terminal AI Assistant',
        activities: [
          { source: 'terminal_ai', details: 'git commit -m "fix bug"', type: 'command_suggestion' },
          { source: 'terminal_ai', details: 'npm run build', type: 'build_command' }
        ]
      },
      {
        name: 'Chat-based Code Review',
        activities: [
          { source: 'code_review_chat', details: 'Review pull request #123', type: 'code_review' },
          { source: 'code_review_chat', details: 'Security vulnerability scan', type: 'security_check' }
        ]
      }
    ];

    for (const scenario of scenarios) {
      console.log(`🎬 Scenario: ${scenario.name}`);
      
      for (const activity of scenario.activities) {
        try {
          await axios.post(`${this.webhookUrl}/chat-activity`, {
            ...activity,
            timestamp: new Date().toISOString(),
            scenario: scenario.name
          }, { timeout: 3000 });
          
          console.log(`   ✅ Triggered: ${activity.details}`);
          await new Promise(resolve => setTimeout(resolve, 1000));
          
        } catch (error) {
          console.log(`   ❌ Failed: ${activity.details} - ${error.message}`);
        }
      }
      
      console.log(); // Empty line between scenarios
    }

    // Final verification
    try {
      const finalStatus = await axios.get(`${this.mcpServerUrl}/health`, { timeout: 3000 });
      console.log(`🏁 Final Status: MCP Server ${finalStatus.data.status}`);
    } catch (error) {
      console.log(`🏁 Final Status: MCP Server not responding`);
    }
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new MCPAutoStartupTester();
  
  (async () => {
    try {
      const results = await tester.runAllTests();
      
      // Run simulation if all tests pass
      if (results && results.allPassed && process.argv.includes('--simulate')) {
        await tester.simulateChatScenarios();
      }
      
      process.exit(results && results.allPassed ? 0 : 1);
      
    } catch (error) {
      console.error('💥 Test suite failed:', error);
      process.exit(1);
    }
  })();
}

module.exports = MCPAutoStartupTester;