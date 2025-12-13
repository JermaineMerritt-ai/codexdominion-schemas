import React, { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';

interface Engine {
  id: string;
  name: string;
  category: string;
  status: 'active' | 'idle' | 'error';
  operations: number;
  successRate: number;
  lastActive: Date;
}

interface Tool {
  id: string;
  name: string;
  icon: string;
  description: string;
  route: string;
  activeUsers: number;
  recentActivity: number;
}

interface SystemMetric {
  label: string;
  value: string;
  status: 'excellent' | 'good' | 'warning' | 'critical';
  icon: string;
}

export default function MasterControl() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [commandPalette, setCommandPalette] = useState(false);

  const engines: Engine[] = [
    { id: '1', name: 'Distribution Engine', category: 'Intelligence', status: 'active', operations: 1247, successRate: 98.5, lastActive: new Date() },
    { id: '2', name: 'Marketing Engine', category: 'Intelligence', status: 'active', operations: 892, successRate: 97.2, lastActive: new Date() },
    { id: '3', name: 'Commerce Engine', category: 'Intelligence', status: 'active', operations: 645, successRate: 99.1, lastActive: new Date() },
    { id: '4', name: 'Claude Sonnet AI', category: 'AI Command', status: 'active', operations: 2341, successRate: 99.8, lastActive: new Date() },
    { id: '5', name: 'GitHub Copilot', category: 'AI Command', status: 'active', operations: 1876, successRate: 98.9, lastActive: new Date() },
    { id: '6', name: 'Jermaine Super Action AI', category: 'AI Command', status: 'active', operations: 3124, successRate: 99.5, lastActive: new Date() },
    { id: '7', name: 'Crown Authority', category: 'Sovereign', status: 'active', operations: 456, successRate: 100, lastActive: new Date() },
    { id: '8', name: 'Scroll Archives', category: 'Sovereign', status: 'active', operations: 789, successRate: 99.7, lastActive: new Date() },
    { id: '9', name: 'Avatar Creator', category: 'Avatar', status: 'active', operations: 234, successRate: 96.8, lastActive: new Date() },
    { id: '10', name: 'Voice Synthesis', category: 'Avatar', status: 'active', operations: 567, successRate: 98.3, lastActive: new Date() },
    { id: '11', name: 'Replay Capture', category: 'Replay', status: 'active', operations: 1123, successRate: 99.2, lastActive: new Date() },
    { id: '12', name: 'SEO Optimizer', category: 'Growth', status: 'active', operations: 445, successRate: 97.5, lastActive: new Date() },
    { id: '13', name: 'Database Cluster', category: 'Technical', status: 'active', operations: 8567, successRate: 99.9, lastActive: new Date() },
    { id: '14', name: 'Affiliate Engine', category: 'Revenue', status: 'active', operations: 334, successRate: 98.1, lastActive: new Date() },
  ];

  const tools: Tool[] = [
    { id: 'chatbox', name: 'AI Chatbox', icon: '💬', description: 'Talk to AI assistants', route: '/ai-chatbox', activeUsers: 5, recentActivity: 124 },
    { id: 'email', name: 'Email Manager', icon: '📧', description: 'Manage communications', route: '/email-manager', activeUsers: 3, recentActivity: 24 },
    { id: 'documents', name: 'Document Center', icon: '📁', description: 'Upload & process files', route: '/document-center', activeUsers: 2, recentActivity: 8 },
    { id: 'research', name: 'Research Studio', icon: '📚', description: 'Analyze documents', route: '/research-studio', activeUsers: 1, recentActivity: 15 },
    { id: 'graphic', name: 'AI Graphic Studio', icon: '🎨', description: 'Create visual content', route: '/ai-graphic-video-studio', activeUsers: 4, recentActivity: 56 },
    { id: 'automation', name: 'Automation Studio', icon: '🔧', description: 'Build workflows', route: '/automation-studio', activeUsers: 2, recentActivity: 12 },
    { id: 'ebook', name: 'eBook Generator', icon: '📖', description: 'Create digital books', route: '/ebook-manager', activeUsers: 1, recentActivity: 3 },
    { id: 'analytics', name: 'Analytics Hub', icon: '📊', description: 'View insights', route: '/analytics-dashboard', activeUsers: 6, recentActivity: 89 },
  ];

  const systemMetrics: SystemMetric[] = [
    { label: 'System Health', value: '99.7%', status: 'excellent', icon: '❤️' },
    { label: 'API Response', value: '124ms', status: 'excellent', icon: '⚡' },
    { label: 'Active Engines', value: `${engines.filter(e => e.status === 'active').length}/48`, status: 'excellent', icon: '🔥' },
    { label: 'CPU Usage', value: '34%', status: 'good', icon: '🖥️' },
    { label: 'Memory', value: '62%', status: 'good', icon: '💾' },
    { label: 'Database', value: 'Healthy', status: 'excellent', icon: '🗄️' },
    { label: 'Cache Hit', value: '94.3%', status: 'excellent', icon: '⚡' },
    { label: 'Error Rate', value: '0.02%', status: 'excellent', icon: '✓' },
  ];

  const categories = [
    { id: 'all', name: 'All Engines', count: engines.length },
    { id: 'Intelligence', name: 'Intelligence', count: engines.filter(e => e.category === 'Intelligence').length },
    { id: 'AI Command', name: 'AI Command', count: engines.filter(e => e.category === 'AI Command').length },
    { id: 'Sovereign', name: 'Sovereign', count: engines.filter(e => e.category === 'Sovereign').length },
    { id: 'Avatar', name: 'Avatar', count: engines.filter(e => e.category === 'Avatar').length },
    { id: 'Replay', name: 'Replay', count: engines.filter(e => e.category === 'Replay').length },
    { id: 'Growth', name: 'Growth', count: engines.filter(e => e.category === 'Growth').length },
    { id: 'Technical', name: 'Technical', count: engines.filter(e => e.category === 'Technical').length },
    { id: 'Revenue', name: 'Revenue', count: engines.filter(e => e.category === 'Revenue').length },
  ];

  const filteredEngines = engines.filter((engine) => {
    const matchesCategory = selectedCategory === 'all' || engine.category === selectedCategory;
    const matchesSearch = engine.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'idle': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getMetricStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'from-green-600 to-teal-600';
      case 'good': return 'from-blue-600 to-cyan-600';
      case 'warning': return 'from-yellow-600 to-orange-600';
      case 'critical': return 'from-red-600 to-pink-600';
      default: return 'from-gray-600 to-gray-700';
    }
  };

  return (
    <>
      <Head>
        <title>Master Control | CodexDominion</title>
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
        {/* Header */}
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">👑</span>
                <div>
                  <h1 className="text-3xl font-bold">Master Control Dashboard</h1>
                  <p className="text-gray-400">Unified command center for all 48 engines and tools</p>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setCommandPalette(!commandPalette)}
                  className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-700 font-semibold"
                >
                  ⌘ Command Palette
                </button>
                <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                  🔔 Alerts
                </button>
                <button className="px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600">
                  ⚙️ Settings
                </button>
              </div>
            </div>

            {/* System Metrics Grid */}
            <div className="grid grid-cols-4 gap-4 mb-6">
              {systemMetrics.map((metric) => (
                <div
                  key={metric.label}
                  className={`bg-gradient-to-r ${getMetricStatusColor(metric.status)} rounded-xl p-4 border border-white/20`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl">{metric.icon}</span>
                    <span className="text-2xl font-bold">{metric.value}</span>
                  </div>
                  <div className="text-sm font-semibold">{metric.label}</div>
                </div>
              ))}
            </div>

            {/* Search Bar */}
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search engines, tools, or use Command Palette (Cmd+K)..."
                className="w-full px-6 py-4 pl-14 bg-gray-900/50 border border-gray-700 rounded-xl focus:border-purple-500 focus:outline-none text-lg"
              />
              <span className="absolute left-5 top-4 text-2xl">🔍</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex h-[calc(100vh-300px)]">
          {/* Sidebar - Categories */}
          <div className="w-64 bg-gray-800/50 backdrop-blur-lg border-r border-gray-700 p-4 overflow-y-auto">
            <h3 className="text-sm font-bold mb-3 text-gray-400">ENGINE CATEGORIES</h3>
            <div className="space-y-2 mb-6">
              {categories.map((category) => (
                <div
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`p-3 rounded-lg cursor-pointer flex items-center justify-between ${
                    selectedCategory === category.id
                      ? 'bg-purple-600'
                      : 'hover:bg-gray-700/50'
                  }`}
                >
                  <span className="font-medium">{category.name}</span>
                  <span className="text-xs bg-white/20 px-2 py-1 rounded">
                    {category.count}
                  </span>
                </div>
              ))}
            </div>

            <div className="border-t border-gray-700 pt-4">
              <h3 className="text-sm font-bold mb-3 text-gray-400">QUICK STATS</h3>
              <div className="space-y-3">
                <div className="p-3 bg-gradient-to-br from-green-600/20 to-teal-600/20 border border-green-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-green-400">
                    {engines.filter(e => e.status === 'active').length}
                  </div>
                  <div className="text-xs text-gray-400">Active Engines</div>
                </div>
                <div className="p-3 bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-purple-400">
                    {tools.reduce((sum, t) => sum + t.activeUsers, 0)}
                  </div>
                  <div className="text-xs text-gray-400">Active Users</div>
                </div>
                <div className="p-3 bg-gradient-to-br from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-lg">
                  <div className="text-2xl font-bold text-blue-400">
                    {engines.reduce((sum, e) => sum + e.operations, 0).toLocaleString()}
                  </div>
                  <div className="text-xs text-gray-400">Total Operations</div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Panel */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="max-w-7xl mx-auto space-y-6">
              {/* Tools Grid */}
              <div>
                <h2 className="text-2xl font-bold mb-4 flex items-center">
                  <span className="mr-2">🛠️</span>
                  Active Tools
                </h2>
                <div className="grid grid-cols-4 gap-4">
                  {tools.map((tool) => (
                    <div
                      key={tool.id}
                      onClick={() => router.push(tool.route)}
                      className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4 hover:border-purple-500 transition-all cursor-pointer"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <span className="text-4xl">{tool.icon}</span>
                        <div className="flex items-center space-x-1 text-xs">
                          <span className="w-2 h-2 bg-green-500 rounded-full" />
                          <span className="text-green-400">{tool.activeUsers}</span>
                        </div>
                      </div>
                      <h3 className="font-bold mb-1">{tool.name}</h3>
                      <p className="text-xs text-gray-400 mb-2">{tool.description}</p>
                      <div className="text-xs text-purple-400">
                        {tool.recentActivity} recent actions
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Engines List */}
              <div>
                <h2 className="text-2xl font-bold mb-4 flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="mr-2">⚙️</span>
                    {selectedCategory === 'all' ? 'All Engines' : `${selectedCategory} Engines`}
                  </div>
                  <span className="text-base font-normal text-gray-400">
                    {filteredEngines.length} engines
                  </span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filteredEngines.map((engine) => (
                    <div
                      key={engine.id}
                      className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4 hover:border-purple-500 transition-all"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-bold mb-1">{engine.name}</h3>
                          <p className="text-xs text-gray-400">{engine.category}</p>
                        </div>
                        <div className={`flex items-center space-x-1 ${getStatusColor(engine.status)}`}>
                          <div className="w-2 h-2 rounded-full bg-current" />
                          <span className="text-xs font-semibold capitalize">{engine.status}</span>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Operations</span>
                          <span className="font-semibold text-blue-400">{engine.operations.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-400">Success Rate</span>
                          <span className={`font-semibold ${engine.successRate >= 99 ? 'text-green-400' : engine.successRate >= 95 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {engine.successRate}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-1.5">
                          <div
                            className="bg-gradient-to-r from-purple-600 to-pink-600 h-1.5 rounded-full"
                            style={{ width: `${engine.successRate}%` }}
                          />
                        </div>
                      </div>

                      <div className="mt-3 text-xs text-gray-500">
                        Last active: {engine.lastActive.toLocaleTimeString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Sidebar - Activity Feed */}
          <div className="w-80 bg-gray-800/50 backdrop-blur-lg border-l border-gray-700 p-4 overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">📡 Live Activity</h3>

            <div className="space-y-3">
              {[
                { time: '2s ago', engine: 'Jermaine Super Action AI', action: 'Processed command', status: 'success' },
                { time: '5s ago', engine: 'Database Cluster', action: 'Synced 234 records', status: 'success' },
                { time: '12s ago', engine: 'Claude Sonnet AI', action: 'Generated response', status: 'success' },
                { time: '18s ago', engine: 'Distribution Engine', action: 'Deployed update', status: 'success' },
                { time: '25s ago', engine: 'SEO Optimizer', action: 'Analyzed 12 pages', status: 'success' },
                { time: '31s ago', engine: 'Voice Synthesis', action: 'Created audio', status: 'success' },
                { time: '45s ago', engine: 'Replay Capture', action: 'Saved session', status: 'success' },
                { time: '1m ago', engine: 'GitHub Copilot', action: 'Code suggestion', status: 'success' },
              ].map((activity, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-gray-900/50 border border-gray-700 rounded-lg hover:border-purple-500/50 transition-all"
                >
                  <div className="flex items-start justify-between mb-1">
                    <span className="text-xs font-semibold text-purple-400">{activity.engine}</span>
                    <span className="text-xs text-gray-500">{activity.time}</span>
                  </div>
                  <div className="text-xs text-gray-400">{activity.action}</div>
                  <div className="mt-1">
                    <span className="text-xs text-green-400">● {activity.status}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl">
              <h4 className="font-bold mb-2">💡 System Intelligence</h4>
              <p className="text-xs text-gray-300">
                All systems operating at peak efficiency. 48 engines crowned and connected.
                Average response time: 124ms. No errors detected.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Command Palette Modal */}
      {commandPalette && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-start justify-center pt-32">
          <div className="bg-gray-800 border border-purple-500 rounded-xl w-full max-w-2xl shadow-2xl">
            <div className="p-4 border-b border-gray-700">
              <input
                type="text"
                placeholder="Type a command or search..."
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg focus:border-purple-500 focus:outline-none"
                autoFocus
              />
            </div>
            <div className="p-4 max-h-96 overflow-y-auto">
              <div className="space-y-1">
                {tools.map((tool) => (
                  <div
                    key={tool.id}
                    onClick={() => {
                      router.push(tool.route);
                      setCommandPalette(false);
                    }}
                    className="p-3 hover:bg-gray-700 rounded-lg cursor-pointer flex items-center space-x-3"
                  >
                    <span className="text-2xl">{tool.icon}</span>
                    <div className="flex-1">
                      <div className="font-semibold">{tool.name}</div>
                      <div className="text-xs text-gray-400">{tool.description}</div>
                    </div>
                    <span className="text-xs text-purple-400">→</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="p-3 border-t border-gray-700 flex items-center justify-between text-xs text-gray-400">
              <div>Navigate with ↑↓ • Select with Enter</div>
              <button
                onClick={() => setCommandPalette(false)}
                className="text-purple-400 hover:underline"
              >
                ESC to close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
