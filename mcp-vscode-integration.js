/**
 * MCP Chat Integration for VS Code
 * Integrates with VS Code to automatically detect chat messages and start MCP servers
 */

const vscode = require('vscode');
const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');

class MCPChatIntegration {
  constructor() {
    this.mcpAutoStartupUrl = 'http://localhost:4954';
    this.mcpServerUrl = 'http://localhost:4953';
    this.isActive = false;
    this.statusBarItem = null;
    this.autoStartupProcess = null;
  }

  activate(context) {
    console.log('🚀 Activating MCP Chat Integration');

    // Create status bar item
    this.createStatusBarItem();

    // Register commands
    this.registerCommands(context);

    // Start monitoring
    this.startChatMonitoring(context);

    // Start auto-startup system
    this.startAutoStartupSystem();

    this.isActive = true;
    console.log('✅ MCP Chat Integration activated');
  }

  createStatusBarItem() {
    this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);

    this.statusBarItem.text = '$(pulse) MCP Auto';
    this.statusBarItem.tooltip = 'MCP Auto-Startup System - Click for status';
    this.statusBarItem.command = 'mcpChatIntegration.showStatus';
    this.statusBarItem.show();
  }

  registerCommands(context) {
    // Show MCP status command
    const showStatusCommand = vscode.commands.registerCommand(
      'mcpChatIntegration.showStatus',
      async () => {
        const status = await this.getMCPStatus();
        this.showStatusMessage(status);
      }
    );

    // Start MCP server command
    const startServerCommand = vscode.commands.registerCommand(
      'mcpChatIntegration.startServer',
      async () => {
        await this.triggerMCPStart();
        vscode.window.showInformationMessage('MCP Server startup triggered');
      }
    );

    // Stop MCP server command
    const stopServerCommand = vscode.commands.registerCommand(
      'mcpChatIntegration.stopServer',
      async () => {
        await this.stopMCPServer();
        vscode.window.showInformationMessage('MCP Server stopped');
      }
    );

    // Toggle auto-startup command
    const toggleAutoCommand = vscode.commands.registerCommand(
      'mcpChatIntegration.toggleAuto',
      async () => {
        await this.toggleAutoStartup();
      }
    );

    context.subscriptions.push(
      showStatusCommand,
      startServerCommand,
      stopServerCommand,
      toggleAutoCommand,
      this.statusBarItem
    );
  }

  startChatMonitoring(context) {
    console.log('🔍 Starting enhanced chat monitoring system...');

    // Monitor when user sends chat messages in VS Code

    // Listen for text document changes (potential chat activity)
    const textChangeDisposable = vscode.workspace.onDidChangeTextDocument((event) => {
      if (this.isChatRelatedDocument(event.document)) {
        this.onChatActivity('text_change', event.document.fileName);
      }

      // Detect chat patterns in text changes
      if (this.detectChatPatterns(event)) {
        this.onChatActivity('chat_pattern_detected', event.document.fileName);
      }
    });

    // Listen for active editor changes
    const editorChangeDisposable = vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor && this.isChatRelatedDocument(editor.document)) {
        this.onChatActivity('editor_change', editor.document.fileName);
      }
    });

    // Listen for terminal creation (potential chat commands)
    const terminalDisposable = vscode.window.onDidOpenTerminal((terminal) => {
      this.onChatActivity('terminal_opened', terminal.name);
    });

    // Enhanced command monitoring for GitHub Copilot and AI assistants
    const enhancedCommandMonitoring = this.setupEnhancedCommandMonitoring(context);

    // Monitor VS Code chat APIs directly
    const chatApiMonitoring = this.setupChatApiMonitoring(context);

    // Monitor GitHub Copilot specific events
    const copilotMonitoring = this.setupCopilotMonitoring(context);

    // Monitor file system for chat logs and conversation files
    const fileSystemMonitoring = this.setupFileSystemMonitoring(context);

    context.subscriptions.push(
      textChangeDisposable,
      editorChangeDisposable,
      terminalDisposable,
      ...enhancedCommandMonitoring,
      ...chatApiMonitoring,
      ...copilotMonitoring,
      ...fileSystemMonitoring
    );

    // Setup periodic chat detection with enhanced patterns
    this.setupPeriodicChatDetection();
  }

  isChatRelatedDocument(document) {
    const chatKeywords = [
      'chat',
      'conversation',
      'copilot',
      'assistant',
      'ai',
      'gpt',
      'claude',
      'message',
    ];

    const filename = path.basename(document.fileName).toLowerCase();
    const content = document.getText().toLowerCase();

    return chatKeywords.some(
      (keyword) =>
        filename.includes(keyword) ||
        content.includes(keyword + ':') ||
        content.includes('@' + keyword)
    );
  }

  isChatRelatedCommand(command) {
    const chatCommands = [
      'github.copilot',
      'chatgpt',
      'claude',
      'ai.chat',
      'assistant',
      'copilot.chat',
      'workbench.action.chat',
      'copilot.interactiveEditor',
      'copilot.generate',
      'copilot.explain',
      'copilot.fix',
      'copilot.refactor',
      'vscode.executeCompletionItemProvider',
      'vscode.executeHoverProvider',
    ];

    return chatCommands.some((cmd) => command.includes(cmd));
  }

  detectChatPatterns(event) {
    // Detect common chat patterns in text changes
    const changes = event.contentChanges;

    for (const change of changes) {
      const text = change.text.toLowerCase();

      // Look for chat-like patterns
      const chatPatterns = [
        /^(user|human|me):\s*/, // "User: " or "Me: "
        /^(assistant|ai|copilot|bot):\s*/, // "Assistant: " or "AI: "
        /^>\s*.+/, // "> quoted text"
        /@\w+/, // @mentions
        /^\$\s*[\w\s]+\?$/, // Questions starting with $
        /how do i|can you|please help|explain/i, // Help requests
        /generate|create|make|build|write/i, // Generation requests
        /fix|debug|error|problem|issue/i, // Fix requests
      ];

      if (chatPatterns.some((pattern) => pattern.test(text))) {
        return true;
      }

      // Detect if typing in a chat-like context
      if (text.length > 10 && this.isChatRelatedDocument(event.document)) {
        return true;
      }
    }

    return false;
  }

  setupEnhancedCommandMonitoring(context) {
    const disposables = [];

    // Monitor all command executions for AI/Chat related activity
    const originalExecuteCommand = vscode.commands.executeCommand;

    // Intercept command execution to detect chat activity
    vscode.commands.executeCommand = async (command, ...args) => {
      // Check if this is a chat-related command
      if (this.isChatRelatedCommand(command)) {
        console.log(`🎯 Chat command detected: ${command}`);
        this.onChatActivity('enhanced_command', command);
      }

      // Execute the original command
      return originalExecuteCommand.call(vscode.commands, command, ...args);
    };

    // Specific GitHub Copilot command monitoring
    const copilotCommands = [
      'github.copilot.generate',
      'github.copilot.interactiveEditor.explain',
      'github.copilot.interactiveEditor.fix',
      'github.copilot.chat.open',
      'github.copilot.chat.newChat',
    ];

    copilotCommands.forEach((command) => {
      const disposable = vscode.commands.registerCommand(command, (...args) => {
        console.log(`🤖 Copilot command intercepted: ${command}`);
        this.onChatActivity('copilot_command', command);
        // Don't prevent the original command from running
        return vscode.commands.executeCommand(`original.${command}`, ...args);
      });
      disposables.push(disposable);
    });

    return disposables;
  }

  setupChatApiMonitoring(context) {
    const disposables = [];

    try {
      // Monitor VS Code's chat API if available
      if (vscode.chat) {
        console.log('📡 Setting up VS Code Chat API monitoring');

        // Register a chat participant that monitors all chat activity
        const participant = vscode.chat.createChatParticipant(
          'codex-dominion-monitor',
          (request, chatContext, stream, token) => {
            console.log('💬 Chat API activity detected:', request.prompt);
            this.onChatActivity('vscode_chat_api', request.prompt.substring(0, 100));

            // Don't actually respond, just monitor
            return;
          }
        );

        disposables.push(participant);
      }

      // Monitor language model API usage
      if (vscode.lm) {
        console.log('🧠 Setting up Language Model API monitoring');
        // This would monitor language model requests
        // Implementation depends on VS Code API availability
      }
    } catch (error) {
      console.log('⚠️ Chat API monitoring not available:', error.message);
    }

    return disposables;
  }

  setupCopilotMonitoring(context) {
    const disposables = [];

    try {
      // Monitor GitHub Copilot extension if available
      const copilotExtension = vscode.extensions.getExtension('GitHub.copilot');

      if (copilotExtension) {
        console.log('🤖 GitHub Copilot extension found, setting up monitoring');

        // Monitor when Copilot is activated
        if (!copilotExtension.isActive) {
          copilotExtension.activate().then(() => {
            console.log('🚀 GitHub Copilot activated');
            this.onChatActivity('copilot_activated', 'GitHub Copilot extension activated');
          });
        }

        // Monitor Copilot Chat extension
        const copilotChatExtension = vscode.extensions.getExtension('GitHub.copilot-chat');
        if (copilotChatExtension && !copilotChatExtension.isActive) {
          copilotChatExtension.activate().then(() => {
            console.log('💬 GitHub Copilot Chat activated');
            this.onChatActivity(
              'copilot_chat_activated',
              'GitHub Copilot Chat extension activated'
            );
          });
        }
      }

      // Monitor for Copilot completion requests
      const completionMonitor = vscode.languages.registerCompletionItemProvider(
        { pattern: '**' },
        {
          provideCompletionItems: (document, position, token, context) => {
            // This fires when completions are requested, which could indicate AI usage
            if (context.triggerKind === vscode.CompletionTriggerKind.Invoke) {
              this.onChatActivity('completion_requested', document.fileName);
            }
            return undefined; // Don't provide actual completions
          },
        }
      );

      disposables.push(completionMonitor);
    } catch (error) {
      console.log('⚠️ Copilot monitoring setup failed:', error.message);
    }

    return disposables;
  }

  setupFileSystemMonitoring(context) {
    const disposables = [];

    try {
      // Monitor file system for chat-related files
      const chatFilePatterns = [
        '**/*.chat',
        '**/*.conversation',
        '**/chat.log',
        '**/messages.json',
        '**/.copilot/**',
        '**/copilot-chat/**',
      ];

      chatFilePatterns.forEach((pattern) => {
        const watcher = vscode.workspace.createFileSystemWatcher(pattern);

        watcher.onDidCreate((uri) => {
          console.log(`📁 Chat file created: ${uri.fsPath}`);
          this.onChatActivity('chat_file_created', uri.fsPath);
        });

        watcher.onDidChange((uri) => {
          console.log(`📝 Chat file changed: ${uri.fsPath}`);
          this.onChatActivity('chat_file_changed', uri.fsPath);
        });

        disposables.push(watcher);
      });

      // Monitor workspace state changes that might indicate chat usage
      const configWatcher = vscode.workspace.onDidChangeConfiguration((event) => {
        if (
          event.affectsConfiguration('github.copilot') ||
          event.affectsConfiguration('chat') ||
          event.affectsConfiguration('ai')
        ) {
          this.onChatActivity('config_change', 'Chat-related configuration changed');
        }
      });

      disposables.push(configWatcher);
    } catch (error) {
      console.log('⚠️ File system monitoring setup failed:', error.message);
    }

    return disposables;
  }

  setupPeriodicChatDetection() {
    // Check for chat-related extensions and activity every 30 seconds
    setInterval(async () => {
      try {
        // Check if chat extensions are active
        const extensions = vscode.extensions.all;
        const chatExtensions = extensions.filter(
          (ext) =>
            ext.id.includes('copilot') ||
            ext.id.includes('chat') ||
            ext.id.includes('ai') ||
            ext.id.includes('assistant')
        );

        if (chatExtensions.some((ext) => ext.isActive)) {
          this.onChatActivity('extension_active', chatExtensions.map((e) => e.id).join(', '));
        }

        // Check for open chat-related files
        const openEditors = vscode.window.visibleTextEditors;
        const chatEditors = openEditors.filter((editor) =>
          this.isChatRelatedDocument(editor.document)
        );

        if (chatEditors.length > 0) {
          this.onChatActivity('chat_files_open', chatEditors.length);
        }
      } catch (error) {
        console.log('Chat detection error:', error.message);
      }
    }, 30000);
  }

  async onChatActivity(source, details) {
    console.log(`💬 VS Code chat activity detected: ${source} - ${details}`);

    // Update status bar
    this.statusBarItem.text = '$(pulse) MCP Active';
    this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');

    // Notify auto-startup system
    await this.triggerMCPStart(source, details);

    // Reset status bar after a few seconds
    setTimeout(() => {
      this.statusBarItem.text = '$(pulse) MCP Auto';
      this.statusBarItem.backgroundColor = undefined;
    }, 5000);
  }

  async startAutoStartupSystem() {
    try {
      console.log('🚀 Starting MCP Auto-Startup System...');

      const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
      if (!workspacePath) {
        console.warn('No workspace folder found for MCP startup');
        return;
      }

      this.autoStartupProcess = spawn('node', ['mcp-auto-startup.js'], {
        cwd: workspacePath,
        stdio: 'pipe',
        detached: false,
      });

      this.autoStartupProcess.stdout.on('data', (data) => {
        console.log(`[MCP-AUTO] ${data.toString().trim()}`);
      });

      this.autoStartupProcess.stderr.on('data', (data) => {
        console.error(`[MCP-AUTO-ERROR] ${data.toString().trim()}`);
      });

      this.autoStartupProcess.on('close', (code) => {
        console.log(`[MCP-AUTO] Process exited with code ${code}`);
        this.autoStartupProcess = null;

        // Update status bar to show system is offline
        this.statusBarItem.text = '$(circle-slash) MCP Offline';
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
      });

      // Wait a moment for startup
      await new Promise((resolve) => setTimeout(resolve, 3000));

      console.log('✅ MCP Auto-Startup System started');
    } catch (error) {
      console.error('❌ Failed to start MCP Auto-Startup System:', error);
      vscode.window.showErrorMessage(`MCP Auto-Startup failed: ${error.message}`);
    }
  }

  async triggerMCPStart(source = 'vscode', details = 'chat activity') {
    try {
      // Send chat activity notification to auto-startup system
      await axios.post(
        `${this.mcpAutoStartupUrl}/chat-activity`,
        {
          source: `vscode_${source}`,
          details: details,
          timestamp: new Date().toISOString(),
          workspace: vscode.workspace.name || 'unknown',
        },
        { timeout: 5000 }
      );
    } catch (error) {
      console.log('Could not notify auto-startup system:', error.message);

      // Fallback: try to start server directly
      try {
        await this.startMCPServerDirect();
      } catch (directError) {
        console.error('Failed to start MCP server directly:', directError.message);
      }
    }
  }

  async startMCPServerDirect() {
    const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
    if (!workspacePath) return;

    return new Promise((resolve, reject) => {
      const serverProcess = spawn('node', ['mcp-server-secure.js'], {
        cwd: workspacePath,
        detached: true,
        stdio: 'ignore',
      });

      serverProcess.unref();

      // Give it a moment to start
      setTimeout(() => resolve(), 3000);
    });
  }

  async getMCPStatus() {
    try {
      // Try to get status from auto-startup system first
      const autoResponse = await axios.get(`${this.mcpAutoStartupUrl}/mcp-status`, {
        timeout: 3000,
      });

      return {
        autoStartup: true,
        ...autoResponse.data,
      };
    } catch (autoError) {
      // Fallback: check MCP server directly
      try {
        const serverResponse = await axios.get(`${this.mcpServerUrl}/health`, {
          timeout: 3000,
        });

        return {
          autoStartup: false,
          running: true,
          healthy: serverResponse.data.status === 'healthy',
          server: serverResponse.data,
        };
      } catch (serverError) {
        return {
          autoStartup: false,
          running: false,
          healthy: false,
          error: 'MCP systems not available',
        };
      }
    }
  }

  async showStatusMessage(status) {
    let message = 'MCP System Status:\n\n';

    if (status.autoStartup) {
      message += '✅ Auto-Startup System: Active\n';
    } else {
      message += '⚠️ Auto-Startup System: Offline\n';
    }

    if (status.running) {
      message += '✅ MCP Server: Running\n';
    } else {
      message += '❌ MCP Server: Stopped\n';
    }

    if (status.healthy) {
      message += '✅ Health Status: Healthy\n';
    } else {
      message += '⚠️ Health Status: Unhealthy\n';
    }

    if (status.lastActivity) {
      message += `🕒 Last Activity: ${new Date(status.lastActivity).toLocaleTimeString()}\n`;
    }

    const action = await vscode.window.showInformationMessage(
      message,
      'Start Server',
      'Stop Server',
      'Refresh Status'
    );

    switch (action) {
      case 'Start Server':
        await this.triggerMCPStart();
        vscode.window.showInformationMessage('MCP Server startup triggered');
        break;
      case 'Stop Server':
        await this.stopMCPServer();
        vscode.window.showInformationMessage('MCP Server stopped');
        break;
      case 'Refresh Status':
        const newStatus = await this.getMCPStatus();
        await this.showStatusMessage(newStatus);
        break;
    }
  }

  async stopMCPServer() {
    try {
      // Try to stop via auto-startup system
      await axios.post(`${this.mcpAutoStartupUrl}/stop-server`, {}, { timeout: 5000 });
    } catch (error) {
      console.log('Could not stop via auto-startup system:', error.message);
    }
  }

  async toggleAutoStartup() {
    if (this.autoStartupProcess) {
      // Stop auto-startup system
      this.autoStartupProcess.kill();
      this.autoStartupProcess = null;
      vscode.window.showInformationMessage('MCP Auto-Startup disabled');
    } else {
      // Start auto-startup system
      await this.startAutoStartupSystem();
      vscode.window.showInformationMessage('MCP Auto-Startup enabled');
    }
  }

  deactivate() {
    console.log('🛑 Deactivating MCP Chat Integration');

    if (this.statusBarItem) {
      this.statusBarItem.dispose();
    }

    if (this.autoStartupProcess) {
      this.autoStartupProcess.kill();
    }

    this.isActive = false;
    console.log('✅ MCP Chat Integration deactivated');
  }
}

// VS Code extension exports
function activate(context) {
  const integration = new MCPChatIntegration();
  integration.activate(context);

  // Store reference for deactivation
  context.globalState.update('mcpIntegration', integration);
}

function deactivate() {
  const integration = context?.globalState?.get('mcpIntegration');
  if (integration) {
    integration.deactivate();
  }
}

module.exports = {
  activate,
  deactivate,
  MCPChatIntegration,
};
