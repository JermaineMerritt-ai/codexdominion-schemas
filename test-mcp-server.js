#!/usr/bin/env node

/**
 * MCP Server Test Suite
 * Comprehensive testing for all MCP server endpoints and functionality
 */

const axios = require('axios');

class MCPServerTester {
  constructor(baseUrl = 'http://localhost:4953', apiKey = null) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
    this.results = [];
  }

  async runAllTests() {
    console.log('🧪 Starting MCP Server Test Suite');
    console.log('=' * 50);

    await this.testHealth();
    await this.testCapabilities();
    await this.testAuthentication();
    
    if (this.apiKey) {
      await this.testProtectedEndpoints();
      await this.testToolExecution();
    }

    this.printResults();
  }

  async testHealth() {
    console.log('\\n🏥 Testing Health Endpoint...');
    try {
      const response = await axios.get(`${this.baseUrl}/health`);
      this.addResult('Health Check', true, response.data);
      console.log('✅ Health endpoint working');
    } catch (error) {
      this.addResult('Health Check', false, error.message);
      console.log('❌ Health endpoint failed');
    }
  }

  async testCapabilities() {
    console.log('\\n🛠️ Testing Capabilities Endpoint...');
    try {
      const response = await axios.get(`${this.baseUrl}/capabilities`);
      this.addResult('Capabilities', true, response.data);
      console.log('✅ Capabilities endpoint working');
      console.log(`   Available tools: ${response.data.tools?.join(', ')}`);
    } catch (error) {
      this.addResult('Capabilities', false, error.message);
      console.log('❌ Capabilities endpoint failed');
    }
  }

  async testAuthentication() {
    console.log('\\n🔐 Testing Authentication...');
    try {
      const response = await axios.post(`${this.baseUrl}/auth`);
      this.apiKey = response.data.apiKey;
      this.addResult('Authentication', true, { hasApiKey: !!this.apiKey });
      console.log('✅ Authentication working');
      console.log(`   Generated API Key: ${this.apiKey?.substring(0, 16)}...`);
    } catch (error) {
      this.addResult('Authentication', false, error.message);
      console.log('❌ Authentication failed');
    }
  }

  async testProtectedEndpoints() {
    console.log('\\n🔒 Testing Protected Endpoints...');

    // Test without API key (should fail)
    try {
      await axios.get(`${this.baseUrl}/secure/info`);
      this.addResult('Security Enforcement', false, 'Accessed without API key');
      console.log('❌ Security bypass detected!');
    } catch (error) {
      if (error.response?.status === 401) {
        this.addResult('Security Enforcement', true, 'Properly rejected unauthorized access');
        console.log('✅ Security properly enforced');
      } else {
        this.addResult('Security Enforcement', false, error.message);
        console.log('⚠️ Unexpected security error');
      }
    }

    // Test with API key (should succeed)
    try {
      const response = await axios.get(`${this.baseUrl}/secure/info`, {
        headers: { 'X-API-Key': this.apiKey }
      });
      this.addResult('Authenticated Access', true, response.data);
      console.log('✅ Authenticated access working');
    } catch (error) {
      this.addResult('Authenticated Access', false, error.message);
      console.log('❌ Authenticated access failed');
    }
  }

  async testToolExecution() {
    console.log('\\n🔧 Testing Tool Execution...');

    const tools = [
      { name: 'system_status', args: {} },
      { name: 'workspace_info', args: {} },
      { name: 'list_directory', args: { dirPath: '.' } },
      { name: 'read_file', args: { filePath: 'package.json' } }
    ];

    for (const tool of tools) {
      try {
        const response = await axios.post(
          `${this.baseUrl}/execute/${tool.name}`,
          tool.args,
          { headers: { 'X-API-Key': this.apiKey } }
        );
        
        this.addResult(`Tool: ${tool.name}`, true, {
          success: response.data.success,
          hasResult: !!response.data.result
        });
        console.log(`✅ ${tool.name} executed successfully`);
      } catch (error) {
        this.addResult(`Tool: ${tool.name}`, false, error.response?.data || error.message);
        console.log(`❌ ${tool.name} execution failed`);
      }
    }
  }

  addResult(testName, passed, data) {
    this.results.push({
      test: testName,
      passed,
      data,
      timestamp: new Date().toISOString()
    });
  }

  printResults() {
    console.log('\\n' + '=' * 50);
    console.log('📊 TEST RESULTS SUMMARY');
    console.log('=' * 50);

    const passed = this.results.filter(r => r.passed).length;
    const total = this.results.length;
    
    console.log(`Total Tests: ${total}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${total - passed}`);
    console.log(`Success Rate: ${((passed / total) * 100).toFixed(1)}%`);

    console.log('\\nDetailed Results:');
    this.results.forEach((result, index) => {
      const status = result.passed ? '✅' : '❌';
      console.log(`${index + 1}. ${status} ${result.test}`);
    });

    if (passed === total) {
      console.log('\\n🎉 ALL TESTS PASSED - MCP SERVER FULLY OPERATIONAL');
    } else {
      console.log('\\n⚠️ SOME TESTS FAILED - REVIEW REQUIRED');
    }
  }
}

// Run tests if executed directly
if (require.main === module) {
  const tester = new MCPServerTester();
  
  tester.runAllTests().catch((error) => {
    console.error('💥 Test suite failed:', error);
    process.exit(1);
  });
}

module.exports = MCPServerTester;