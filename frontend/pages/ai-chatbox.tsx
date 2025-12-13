import React, { useState, useRef, useEffect } from 'react';
import Head from 'next/head';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  aiModel: string;
  timestamp: Date;
  attachments?: string[];
}

interface AIAssistant {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  capabilities: string[];
  status: 'online' | 'busy' | 'offline';
}

export default function AIChatbox() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I am Jermaine Super Action AI. How can I assist you today? I can help with coding, strategy, automation, content creation, and more.',
      aiModel: 'Jermaine Super Action AI',
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedAI, setSelectedAI] = useState('jermaine');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const aiAssistants: AIAssistant[] = [
    {
      id: 'jermaine',
      name: 'Jermaine Super Action AI',
      icon: '⚡',
      color: 'from-yellow-600 to-orange-600',
      description: 'Command Execution & System Orchestration',
      capabilities: ['Coding', 'Automation', 'Strategy', 'Deployment'],
      status: 'online',
    },
    {
      id: 'claude',
      name: 'Claude Sonnet',
      icon: '🧠',
      color: 'from-purple-600 to-pink-600',
      description: 'Strategic Intelligence & Deep Analysis',
      capabilities: ['Research', 'Writing', 'Analysis', 'Planning'],
      status: 'online',
    },
    {
      id: 'copilot',
      name: 'GitHub Copilot',
      icon: '💻',
      color: 'from-blue-600 to-cyan-600',
      description: 'Code Generation & Development',
      capabilities: ['Code Gen', 'Debugging', 'Refactoring', 'Documentation'],
      status: 'online',
    },
    {
      id: 'gpt4',
      name: 'GPT-4 Turbo',
      icon: '🔍',
      color: 'from-green-600 to-teal-600',
      description: 'General Intelligence & Problem Solving',
      capabilities: ['Q&A', 'Summarization', 'Translation', 'Creative'],
      status: 'online',
    },
    {
      id: 'gemini',
      name: 'Gemini Vision',
      icon: '👁️',
      color: 'from-red-600 to-pink-600',
      description: 'Visual Intelligence & Multi-modal',
      capabilities: ['Image Analysis', 'OCR', 'Vision', 'Multi-modal'],
      status: 'online',
    },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      aiModel: 'User',
      timestamp: new Date(),
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `I understand you want to: "${inputMessage}". Let me help you with that. This would connect to the actual ${aiAssistants.find(ai => ai.id === selectedAI)?.name} API to process your request.`,
        aiModel: aiAssistants.find(ai => ai.id === selectedAI)?.name || 'AI',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileUpload = () => {
    fileInputRef.current?.click();
  };

  const quickPrompts = [
    '💡 Generate code for...',
    '📊 Analyze this data...',
    '🎨 Create content about...',
    '🔧 Debug my code...',
    '📝 Write documentation for...',
    '🚀 Deploy to Azure...',
  ];

  return (
    <>
      <Head>
        <title>AI Chatbox | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
        <div className="flex h-screen">
          {/* AI Assistants Sidebar */}
          <div className="w-80 bg-gray-800/50 backdrop-blur-lg border-r border-gray-700 p-4 overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">🤖 AI Assistants</h2>

            <div className="space-y-3">
              {aiAssistants.map((ai) => (
                <div
                  key={ai.id}
                  onClick={() => setSelectedAI(ai.id)}
                  className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                    selectedAI === ai.id
                      ? `bg-gradient-to-r ${ai.color} border-white`
                      : 'bg-gray-900/50 border-gray-700 hover:border-gray-600'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-3xl">{ai.icon}</span>
                      <div>
                        <div className="font-bold">{ai.name}</div>
                        <div className="text-xs text-gray-400">{ai.description}</div>
                      </div>
                    </div>
                    <div className={`w-2 h-2 rounded-full ${
                      ai.status === 'online' ? 'bg-green-500' :
                      ai.status === 'busy' ? 'bg-yellow-500' :
                      'bg-gray-500'
                    }`} />
                  </div>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {ai.capabilities.map((cap) => (
                      <span
                        key={cap}
                        className="text-xs px-2 py-1 bg-white/10 rounded"
                      >
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* System Status */}
            <div className="mt-6 p-4 bg-gray-900/50 rounded-xl border border-gray-700">
              <h3 className="font-bold mb-3">⚙️ System Status</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">48 Engines</span>
                  <span className="text-green-400">● Active</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">API Gateway</span>
                  <span className="text-green-400">● Healthy</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Response Time</span>
                  <span className="text-blue-400">124ms</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="mt-6 p-4 bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-xl border border-purple-500/30">
              <h3 className="font-bold mb-3">⚡ Quick Actions</h3>
              <div className="space-y-2">
                <button className="w-full py-2 px-3 bg-purple-600 rounded-lg text-sm font-semibold hover:bg-purple-700">
                  📂 Upload Document
                </button>
                <button className="w-full py-2 px-3 bg-blue-600 rounded-lg text-sm font-semibold hover:bg-blue-700">
                  🎙️ Voice Input
                </button>
                <button className="w-full py-2 px-3 bg-green-600 rounded-lg text-sm font-semibold hover:bg-green-700">
                  📸 Image Analysis
                </button>
              </div>
            </div>
          </div>

          {/* Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Header */}
            <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl">
                    {aiAssistants.find(ai => ai.id === selectedAI)?.icon}
                  </span>
                  <div>
                    <h1 className="text-xl font-bold">
                      {aiAssistants.find(ai => ai.id === selectedAI)?.name}
                    </h1>
                    <p className="text-sm text-gray-400">
                      {aiAssistants.find(ai => ai.id === selectedAI)?.description}
                    </p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                    🗑️ Clear Chat
                  </button>
                  <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                    💾 Export
                  </button>
                </div>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-2xl ${
                      message.role === 'user'
                        ? 'bg-gradient-to-r from-blue-600 to-cyan-600'
                        : 'bg-gray-800/50 backdrop-blur-lg border border-gray-700'
                    } rounded-xl p-4`}
                  >
                    <div className="flex items-start space-x-2">
                      {message.role === 'assistant' && (
                        <span className="text-2xl">
                          {aiAssistants.find(ai => ai.name === message.aiModel)?.icon || '🤖'}
                        </span>
                      )}
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-sm">{message.aiModel}</span>
                          <span className="text-xs text-gray-400">
                            {message.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="whitespace-pre-wrap">{message.content}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl">
                        {aiAssistants.find(ai => ai.id === selectedAI)?.icon}
                      </span>
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Prompts */}
            <div className="px-6 py-2 border-t border-gray-700 bg-gray-800/30">
              <div className="flex space-x-2 overflow-x-auto">
                {quickPrompts.map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => setInputMessage(prompt)}
                    className="px-3 py-2 bg-gray-700/50 rounded-lg text-sm whitespace-nowrap hover:bg-gray-700"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {/* Input Area */}
            <div className="bg-gray-800/50 backdrop-blur-lg border-t border-gray-700 p-4">
              <div className="flex items-end space-x-2">
                <input
                  type="file"
                  ref={fileInputRef}
                  className="hidden"
                  multiple
                  accept="image/*,.pdf,.doc,.docx,.txt"
                />
                <button
                  onClick={handleFileUpload}
                  className="px-4 py-3 bg-gray-700 rounded-lg hover:bg-gray-600"
                  title="Upload files"
                >
                  📎
                </button>
                <button
                  className="px-4 py-3 bg-gray-700 rounded-lg hover:bg-gray-600"
                  title="Voice input"
                >
                  🎙️
                </button>
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask anything... (Shift+Enter for new line)"
                  className="flex-1 px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none resize-none"
                  rows={1}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-semibold hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Send ➤
                </button>
              </div>
              <div className="mt-2 text-xs text-gray-500 flex justify-between">
                <span>Powered by Claude Sonnet 4.5 + GPT-4 + Custom Models</span>
                <span>Press Enter to send, Shift+Enter for new line</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
