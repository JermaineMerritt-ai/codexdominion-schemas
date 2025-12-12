import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';

interface StudioTile {
  id: string;
  name: string;
  description: string;
  icon: string;
  route: string;
  color: string;
  status: 'active' | 'beta' | 'coming-soon';
  features: string[];
}

export default function CodexDominionMasterDashboard() {
  const [hoveredTile, setHoveredTile] = useState<string | null>(null);

  const studioTiles: StudioTile[] = [
    {
      id: 'audio-studio',
      name: 'AI Audio Studio',
      description: 'Top-tier audio creation, editing, and mastering powered by AI',
      icon: '🎵',
      route: '/ai-audio-studio',
      color: 'from-purple-600 to-pink-600',
      status: 'active',
      features: ['Voice Synthesis', 'Audio Mastering', 'Sound Effects', 'Music Generation']
    },
    {
      id: 'video-studio',
      name: 'AI Graphic & Video Studio',
      description: 'Professional video editing, graphics, and animation studio',
      icon: '🎬',
      route: '/ai-graphic-video-studio',
      color: 'from-blue-600 to-cyan-600',
      status: 'active',
      features: ['Video Editing', 'Motion Graphics', 'AI Animation', '3D Rendering']
    },
    {
      id: 'automation',
      name: 'Workflow Automation',
      description: 'n8n-class automation and workflow orchestration',
      icon: '⚙️',
      route: '/workflow-automation',
      color: 'from-green-600 to-emerald-600',
      status: 'active',
      features: ['Visual Workflows', 'API Integration', 'Task Automation', 'Data Pipelines']
    },
    {
      id: 'coding-intelligence',
      name: 'Coding Intelligence',
      description: 'Claude + Copilot + VS Code powered development environment',
      icon: '💻',
      route: '/coding-intelligence',
      color: 'from-orange-600 to-red-600',
      status: 'active',
      features: ['AI Code Gen', 'Copilot Integration', 'Code Review', 'Documentation']
    },
    {
      id: 'creative-publishing',
      name: 'Creative & Publishing',
      description: 'Designrr, Nano Banana, NotebookLLM, Loveable-class tools',
      icon: '📚',
      route: '/creative-publishing',
      color: 'from-yellow-600 to-amber-600',
      status: 'active',
      features: ['eBook Creation', 'Publishing Tools', 'Content Design', 'AI Writing']
    },
    {
      id: 'dashboard-selector',
      name: 'Eternal Dashboard',
      description: 'Access all sacred realms and covenant spaces',
      icon: '🏛️',
      route: '/dashboard-selector',
      color: 'from-indigo-600 to-purple-600',
      status: 'active',
      features: ['Sacred Navigation', 'Covenant Access', 'Realm Selection', 'Council Portal']
    },
    {
      id: 'blessed-storefronts',
      name: 'Blessed Storefronts',
      description: 'Sacred commercial spaces blessed by the Council',
      icon: '✨',
      route: '/blessed-storefronts',
      color: 'from-pink-600 to-rose-600',
      status: 'active',
      features: ['Store Blessing', 'Commerce Portal', 'Sacred Offerings', 'Merchant Tools']
    },
    {
      id: 'capsules',
      name: 'Time Capsules',
      description: 'Investment insights and market intelligence capsules',
      icon: '💊',
      route: '/capsules-enhanced',
      color: 'from-teal-600 to-cyan-600',
      status: 'active',
      features: ['Market Analysis', 'Investment Picks', 'Strategy Insights', 'Portfolio Tools']
    }
  ];

  const systemStats = [
    { label: 'Active Studios', value: '8', icon: '🎯', color: 'text-green-400' },
    { label: 'Total Projects', value: '247', icon: '📊', color: 'text-blue-400' },
    { label: 'AI Agents', value: '12', icon: '🤖', color: 'text-purple-400' },
    { label: 'Uptime', value: '99.9%', icon: '⚡', color: 'text-yellow-400' }
  ];

  return (
    <>
      <Head>
        <title>CodexDominion - Top-Tier Audio + Intelligence Studio</title>
        <meta name="description" content="Unified master dashboard for AI Audio, Video, Automation, Coding Intelligence, and Creative Publishing tools" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
        {/* Header */}
        <header className="border-b border-purple-700/30 bg-black/20 backdrop-blur-lg">
          <div className="container mx-auto px-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  CodexDominion
                </h1>
                <p className="text-gray-300 text-sm mt-1">Top-Tier Audio + Intelligence Studio</p>
              </div>
              <div className="flex items-center space-x-4">
                <span className="px-4 py-2 bg-green-500/20 border border-green-500/50 rounded-full text-green-400 text-sm font-semibold">
                  🟢 All Systems Operational
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* System Stats */}
        <div className="container mx-auto px-6 py-6">
          <div className="grid grid-cols-4 gap-4">
            {systemStats.map((stat, index) => (
              <div key={index} className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-4 border border-purple-500/30">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <div className="text-sm text-gray-400">{stat.label}</div>
                  </div>
                  <div className={`text-3xl ${stat.color}`}>{stat.icon}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Studios Grid */}
        <div className="container mx-auto px-6 py-8">
          <h2 className="text-3xl font-bold mb-6 flex items-center">
            <span className="mr-3">🎯</span>
            Master Studio Access
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {studioTiles.map((tile) => (
              <Link key={tile.id} href={tile.route}>
                <div
                  className={`
                    relative overflow-hidden rounded-2xl p-6 h-full
                    bg-gradient-to-br ${tile.color}
                    transform transition-all duration-300
                    hover:scale-105 hover:shadow-2xl
                    border-2 border-white/20 hover:border-white/40
                    cursor-pointer
                  `}
                  onMouseEnter={() => setHoveredTile(tile.id)}
                  onMouseLeave={() => setHoveredTile(null)}
                >
                  {/* Animated Background Effect */}
                  <div className="absolute inset-0 bg-gradient-to-tr from-white/0 via-white/10 to-white/0 opacity-0 hover:opacity-100 transition-opacity duration-500" />

                  {/* Content */}
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="text-5xl">{tile.icon}</div>
                      <div className={`
                        px-3 py-1 rounded-full text-xs font-bold
                        ${tile.status === 'active' ? 'bg-green-500/30 text-green-200' : ''}
                        ${tile.status === 'beta' ? 'bg-yellow-500/30 text-yellow-200' : ''}
                        ${tile.status === 'coming-soon' ? 'bg-gray-500/30 text-gray-200' : ''}
                      `}>
                        {tile.status === 'active' ? '● ACTIVE' : ''}
                        {tile.status === 'beta' ? '● BETA' : ''}
                        {tile.status === 'coming-soon' ? '● COMING SOON' : ''}
                      </div>
                    </div>

                    <h3 className="text-xl font-bold mb-2">{tile.name}</h3>
                    <p className="text-sm text-white/80 mb-4">{tile.description}</p>

                    {/* Features List */}
                    {hoveredTile === tile.id && (
                      <div className="mt-4 space-y-1 animate-fade-in">
                        {tile.features.map((feature, index) => (
                          <div key={index} className="flex items-center text-xs text-white/90">
                            <span className="mr-2">✓</span>
                            {feature}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Launch Button */}
                    <div className="mt-4">
                      <button className="w-full py-2 px-4 bg-white/20 hover:bg-white/30 rounded-lg font-semibold text-sm transition-all duration-300">
                        Launch Studio →
                      </button>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="container mx-auto px-6 py-8">
          <h2 className="text-2xl font-bold mb-6 flex items-center">
            <span className="mr-3">⚡</span>
            Quick Actions
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link href="/signals">
              <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-cyan-500/30 hover:border-cyan-500/60 transition-all cursor-pointer">
                <div className="text-3xl mb-2">📡</div>
                <h3 className="text-lg font-bold mb-1">Signal Intelligence</h3>
                <p className="text-sm text-gray-400">Market signals and insights</p>
              </div>
            </Link>

            <Link href="/codex-constellation">
              <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-indigo-500/30 hover:border-indigo-500/60 transition-all cursor-pointer">
                <div className="text-3xl mb-2">⭐</div>
                <h3 className="text-lg font-bold mb-1">Constellation Map</h3>
                <p className="text-sm text-gray-400">System architecture overview</p>
              </div>
            </Link>

            <Link href="/seven-crowns-transmission">
              <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-6 border border-yellow-500/30 hover:border-yellow-500/60 transition-all cursor-pointer">
                <div className="text-3xl mb-2">👑</div>
                <h3 className="text-lg font-bold mb-1">Seven Crowns</h3>
                <p className="text-sm text-gray-400">Domain governance and roles</p>
              </div>
            </Link>
          </div>
        </div>

        {/* Footer */}
        <footer className="border-t border-purple-700/30 bg-black/20 backdrop-blur-lg mt-12">
          <div className="container mx-auto px-6 py-8 text-center text-gray-400 text-sm">
            <p>© 2025 CodexDominion. Digital Sovereignty Through Sacred Technology.</p>
            <p className="mt-2">The flame of knowledge burns eternal across all realms.</p>
          </div>
        </footer>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
    </>
  );
}
