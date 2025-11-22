/**
 * 🔥 CODEX DOMINION CHAT MESSAGE HOOKS 🔥
 * Flame eternal, radiance supreme - advanced chat detection system
 * Detects chat messages and triggers MCP server startup automatically
 */

const vscode = require('vscode');
const { MCPChatIntegration } = require('./mcp-vscode-integration');
const MCPAutoStartup = require('./mcp-auto-startup');

class ChatMessageHooks {
  constructor() {
    this.mcpIntegration = null;
    this.autoStartup = null;
    this.isActive = false;
    this.hooks = [];
    this.chatPatterns = [
      // GitHub Copilot patterns
      /\/\*\s*@(copilot|github)\s*/i,
      /@copilot\s+/i,
      /\/\/\s*copilot:/i,
      
      // Chat conversation patterns
      /^(user|human|me):\s*/i,
      /^(assistant|ai|bot|copilot):\s*/i,
      /^>\s*.+/,
      
      // Question patterns
      /^(how|what|why|when|where|can|could|should|would)\s+/i,
      /\?\s*$/,
      
      // Request patterns
      /^(please|help|explain|show|generate|create|make|build|write|fix|debug)/i,
      
      // AI interaction patterns
      /@\w+\s+(help|explain|generate|create|fix|debug)/i,
      /^\/\w+/,  // Slash commands
      
      // Code comment questions
      /\/\/\s*(how|what|why|can|should|TODO|FIXME|NOTE)/i,
      /\/\*\s*(how|what|why|can|should|TODO|FIXME|NOTE)/i
    ];
  }

  async initialize() {
    console.log('🎯 Initializing Chat Message Hooks System');
    
    try {
      // Initialize MCP components
      this.autoStartup = new MCPAutoStartup();
      await this.autoStartup.initialize();
      
      this.mcpIntegration = new MCPChatIntegration();
      
      // Setup various hook types
      this.setupTextHooks();
      this.setupCommandHooks();
      this.setupExtensionHooks();
      this.setupKeyboardHooks();
      this.setupContextHooks();
      
      this.isActive = true;
      console.log('✅ Chat Message Hooks System initialized');
      
    } catch (error) {
      console.error('❌ Failed to initialize Chat Message Hooks:', error);
      throw error;
    }
  }

  setupTextHooks() {
    console.log('📝 Setting up text-based chat detection hooks');
    
    // Hook into text document changes with advanced pattern matching
    const textChangeHook = vscode.workspace.onDidChangeTextDocument((event) => {
      this.analyzeTextChange(event);
    });
    
    // Hook into active text editor changes
    const editorChangeHook = vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) {
        this.analyzeEditorContext(editor);
      }
    });
    
    // Hook into text selection changes (user selecting text for AI interaction)
    const selectionChangeHook = vscode.window.onDidChangeTextEditorSelection((event) => {
      this.analyzeSelection(event);
    });
    
    this.hooks.push(textChangeHook, editorChangeHook, selectionChangeHook);
  }

  setupCommandHooks() {
    console.log('⚡ Setting up command-based chat detection hooks');
    
    // Hook into all command executions
    const commandHook = this.interceptCommands();
    
    // Specific AI/Chat command hooks
    const aiCommands = [
      'github.copilot.generate',
      'github.copilot.interactiveEditor.explain',
      'github.copilot.interactiveEditor.fix',
      'github.copilot.chat.open',
      'workbench.action.chat.open',
      'workbench.action.chat.openInSidebar',
      'editor.action.inlineSuggest.trigger',
      'editor.action.triggerSuggest'
    ];
    
    aiCommands.forEach(command => {
      try {
        const hook = vscode.commands.registerCommand(`hooks.${command}`, (...args) => {
          console.log(`🎯 AI command hook triggered: ${command}`);
          this.onChatMessage('command_hook', command);
          
          // Execute original command
          return vscode.commands.executeCommand(command, ...args);
        });
        this.hooks.push(hook);
      } catch (error) {
        console.log(`⚠️ Could not hook command ${command}:`, error.message);
      }
    });
  }

  setupExtensionHooks() {
    console.log('🧩 Setting up extension-based chat detection hooks');
    
    // Monitor GitHub Copilot extension
    this.monitorCopilotExtension();
    
    // Monitor other AI extensions
    this.monitorAIExtensions();
    
    // Hook into extension activation events
    const extensionHook = vscode.extensions.onDidChange(() => {
      this.checkForNewAIExtensions();
    });
    
    this.hooks.push(extensionHook);
  }

  setupKeyboardHooks() {
    console.log('⌨️ Setting up keyboard-based chat detection hooks');
    
    // Monitor for common AI interaction key combinations
    const keySequences = [
      'ctrl+k ctrl+i',  // Copilot inline chat
      'ctrl+shift+i',   // Quick AI action
      'ctrl+/',          // Comment toggle (often used with AI)
      'f1'               // Command palette (for AI commands)
    ];
    
    // Note: VS Code doesn't allow direct keyboard hooks for security
    // Instead, we monitor command palette usage and related actions
    
    const commandPaletteHook = vscode.commands.registerCommand('hooks.commandPalette', () => {
      this.onChatMessage('keyboard_hook', 'Command palette opened');
      return vscode.commands.executeCommand('workbench.action.showCommands');
    });
    
    this.hooks.push(commandPaletteHook);
  }

  setupContextHooks() {
    console.log('🔍 Setting up context-based chat detection hooks');
    
    // Monitor workspace context changes
    const contextHook = vscode.workspace.onDidChangeConfiguration((event) => {
      if (event.affectsConfiguration('github.copilot') ||
          event.affectsConfiguration('chat') ||
          event.affectsConfiguration('ai')) {
        this.onChatMessage('context_change', 'AI configuration changed');
      }
    });
    
    // Monitor file opening patterns that suggest AI usage
    const fileOpenHook = vscode.workspace.onDidOpenTextDocument((document) => {
      if (this.isChatContextFile(document)) {
        this.onChatMessage('file_context', document.fileName);
      }
    });
    
    this.hooks.push(contextHook, fileOpenHook);
  }

  async analyzeTextChange(event) {
    const changes = event.contentChanges;
    
    for (const change of changes) {
      // Check if the text matches chat patterns
      if (this.matchesChatPattern(change.text)) {
        console.log('💬 Chat pattern detected in text change');
        this.onChatMessage('text_pattern', change.text.substring(0, 100));
      }
      
      // Check for AI-specific markers
      if (this.containsAIMarkers(change.text)) {
        console.log('🤖 AI marker detected in text');
        this.onChatMessage('ai_marker', change.text.substring(0, 50));
      }
      
      // Check typing patterns that suggest chat interaction
      if (this.suggestsChatInteraction(change, event.document)) {
        console.log('💭 Chat interaction pattern detected');
        this.onChatMessage('interaction_pattern', 'Chat-like typing detected');
      }
    }
  }

  analyzeEditorContext(editor) {
    const document = editor.document;
    
    // Check if this is a chat-related file
    if (this.isChatContextFile(document)) {
      this.onChatMessage('chat_file', document.fileName);
    }
    
    // Check if the file contains chat-like content
    const text = document.getText();
    if (this.containsChatContent(text)) {
      this.onChatMessage('chat_content', 'Chat content detected in file');
    }
  }

  analyzeSelection(event) {
    const selection = event.textEditor.selection;
    
    // If user selects significant amount of code, they might be preparing for AI interaction
    if (!selection.isEmpty && selection.end.line - selection.start.line > 2) {
      const selectedText = event.textEditor.document.getText(selection);
      
      if (selectedText.length > 50) {
        console.log('📋 Significant text selection detected (potential AI interaction)');
        this.onChatMessage('text_selection', `Selected ${selectedText.length} characters`);
      }
    }
  }

  interceptCommands() {
    // Create a wrapper around command execution to detect AI-related commands
    const originalExecuteCommand = vscode.commands.executeCommand;
    
    vscode.commands.executeCommand = async (command, ...args) => {
      // Check if this is an AI/Chat related command
      if (this.isAIRelatedCommand(command)) {
        console.log(`🎯 AI-related command detected: ${command}`);
        this.onChatMessage('ai_command', command);
      }
      
      // Execute original command
      return originalExecuteCommand.call(vscode.commands, command, ...args);
    };
  }

  matchesChatPattern(text) {
    return this.chatPatterns.some(pattern => pattern.test(text));
  }

  containsAIMarkers(text) {
    const aiMarkers = [
      '@copilot',
      '@github',
      '@ai',
      '@assistant',
      '#copilot',
      '//copilot:',
      '/*copilot:',
      'TODO: ask',
      'FIXME: help',
      'NOTE: explain'
    ];
    
    const lowerText = text.toLowerCase();
    return aiMarkers.some(marker => lowerText.includes(marker.toLowerCase()));
  }

  suggestsChatInteraction(change, document) {
    // Rapid typing followed by pause suggests question formulation
    const text = change.text;
    const isQuestion = text.includes('?') || text.match(/^(how|what|why|when|where|can|could|should|would)/i);
    const isAtEndOfLine = change.range.end.character === document.lineAt(change.range.end.line).text.length;
    
    return isQuestion && isAtEndOfLine && text.length > 10;
  }

  isChatContextFile(document) {
    const fileName = document.fileName.toLowerCase();
    const chatFilePatterns = [
      'chat',
      'conversation',
      'copilot',
      'ai',
      'assistant',
      'prompt',
      'query'
    ];
    
    return chatFilePatterns.some(pattern => fileName.includes(pattern)) ||
           document.languageId === 'chat' ||
           document.uri.scheme === 'copilot';
  }

  containsChatContent(text) {
    const chatIndicators = [
      /^(user|human|me):/mi,
      /^(assistant|ai|bot):/mi,
      /@copilot/gi,
      /\/\/\s*copilot:/gi,
      /\/\*\s*@github/gi
    ];
    
    return chatIndicators.some(indicator => indicator.test(text));
  }

  isAIRelatedCommand(command) {
    const aiCommandPatterns = [
      'github.copilot',
      'copilot',
      'chat',
      'ai',
      'assistant',
      'suggest',
      'complete',
      'generate',
      'explain',
      'fix',
      'refactor'
    ];
    
    return aiCommandPatterns.some(pattern => command.toLowerCase().includes(pattern));
  }

  monitorCopilotExtension() {
    const copilotExtension = vscode.extensions.getExtension('GitHub.copilot');
    const copilotChatExtension = vscode.extensions.getExtension('GitHub.copilot-chat');
    
    [copilotExtension, copilotChatExtension].forEach(ext => {
      if (ext) {
        if (!ext.isActive) {
          ext.activate().then(() => {
            console.log(`🤖 ${ext.id} activated - triggering MCP startup`);
            this.onChatMessage('extension_activated', ext.id);
          });
        }
      }
    });
  }

  monitorAIExtensions() {
    const aiExtensionPatterns = [
      'chatgpt',
      'claude',
      'openai',
      'anthropic',
      'ai',
      'assistant',
      'copilot'
    ];
    
    vscode.extensions.all.forEach(ext => {
      if (aiExtensionPatterns.some(pattern => ext.id.toLowerCase().includes(pattern))) {
        if (ext.isActive) {
          console.log(`🧠 AI extension detected: ${ext.id}`);
          this.onChatMessage('ai_extension_active', ext.id);
        }
      }
    });
  }

  checkForNewAIExtensions() {
    // Check for newly installed or activated AI extensions
    this.monitorAIExtensions();
  }

  async onChatMessage(source, details) {
    console.log(`🔥 CHAT MESSAGE DETECTED: ${source} - ${details}`);
    
    try {
      // Trigger MCP auto-startup with high priority
      if (this.autoStartup) {
        await this.autoStartup.onChatActivity(`hook_${source}`, details);
      }
      
      // Notify VS Code integration
      if (this.mcpIntegration) {
        await this.mcpIntegration.onChatActivity(`hook_${source}`, details);
      }
      
      // Log the chat message detection
      console.log(`✨ MCP servers triggered by chat hook: ${source}`);
      
    } catch (error) {
      console.error('❌ Error handling chat message:', error);
    }
  }

  dispose() {
    console.log('🛑 Disposing Chat Message Hooks');
    
    this.hooks.forEach(hook => {
      if (hook && typeof hook.dispose === 'function') {
        hook.dispose();
      }
    });
    
    this.hooks = [];
    this.isActive = false;
    
    if (this.autoStartup) {
      this.autoStartup.setupGracefulShutdown();
    }
  }
}

// Auto-initialization for direct execution
if (require.main === module) {
  const hooks = new ChatMessageHooks();
  hooks.initialize().catch(error => {
    console.error('💥 Chat Message Hooks failed to initialize:', error);
    process.exit(1);
  });
}

module.exports = ChatMessageHooks;