import React, { useState } from 'react';
import Head from 'next/head';

interface Capsule {
  id: number;
  name: string;
  avatar: string;
  industry: string;
  tier: 1 | 2 | 3;
  status: 'active' | 'launching' | 'planning' | 'idle';
  customers: number;
  problemsSolved: number;
  revenue: number;
  successRate: number;
  uptime: number;
  satisfaction: number;
}

export default function CapsuleDashboard() {
  const [selectedTier, setSelectedTier] = useState<'all' | 1 | 2 | 3>('all');
  const [selectedCapsule, setSelectedCapsule] = useState<Capsule | null>(null);

  const capsules: Capsule[] = [
    // TIER 1: FOUNDATION INDUSTRIES
    { id: 1, name: 'BuildMaster AI', avatar: '🏗️', industry: 'Construction', tier: 1, status: 'active', customers: 234, problemsSolved: 4520, revenue: 521000, successRate: 96.9, uptime: 99.8, satisfaction: 4.6 },
    { id: 2, name: 'FactoryMind AI', avatar: '🏭', industry: 'Manufacturing', tier: 1, status: 'active', customers: 189, problemsSolved: 5890, revenue: 612000, successRate: 97.8, uptime: 99.9, satisfaction: 4.8 },
    { id: 3, name: 'RouteGenius AI', avatar: '🚚', industry: 'Logistics', tier: 1, status: 'active', customers: 276, problemsSolved: 6234, revenue: 548000, successRate: 97.1, uptime: 99.7, satisfaction: 4.7 },
    { id: 4, name: 'ShopSense AI', avatar: '🛒', industry: 'Retail', tier: 1, status: 'active', customers: 198, problemsSolved: 3421, revenue: 425000, successRate: 95.8, uptime: 99.6, satisfaction: 4.5 },
    { id: 5, name: 'MedFlow AI', avatar: '🏥', industry: 'Healthcare', tier: 1, status: 'active', customers: 342, problemsSolved: 7854, revenue: 685000, successRate: 98.2, uptime: 99.9, satisfaction: 4.9 },
    { id: 6, name: 'FarmWise AI', avatar: '🌾', industry: 'Agriculture', tier: 1, status: 'active', customers: 167, problemsSolved: 2987, revenue: 398000, successRate: 94.5, uptime: 99.5, satisfaction: 4.4 },
    { id: 7, name: 'PowerGrid AI', avatar: '⚡', industry: 'Energy', tier: 1, status: 'active', customers: 156, problemsSolved: 4231, revenue: 489000, successRate: 96.5, uptime: 99.8, satisfaction: 4.7 },
    { id: 8, name: 'PropertyPro AI', avatar: '🏘️', industry: 'Real Estate', tier: 1, status: 'active', customers: 223, problemsSolved: 3876, revenue: 467000, successRate: 95.2, uptime: 99.4, satisfaction: 4.5 },
    { id: 9, name: 'HotelHub AI', avatar: '🏨', industry: 'Hospitality', tier: 1, status: 'launching', customers: 145, problemsSolved: 2654, revenue: 356000, successRate: 93.8, uptime: 99.3, satisfaction: 4.3 },
    { id: 10, name: 'MenuMaster AI', avatar: '🍽️', industry: 'Food Service', tier: 1, status: 'active', customers: 201, problemsSolved: 3542, revenue: 412000, successRate: 94.9, uptime: 99.5, satisfaction: 4.4 },

    // TIER 2: PROFESSIONAL SERVICES
    { id: 11, name: 'LawLogic AI', avatar: '⚖️', industry: 'Legal', tier: 2, status: 'active', customers: 89, problemsSolved: 1876, revenue: 289000, successRate: 97.3, uptime: 99.7, satisfaction: 4.8 },
    { id: 12, name: 'LedgerAI', avatar: '📊', industry: 'Accounting', tier: 2, status: 'active', customers: 134, problemsSolved: 2987, revenue: 345000, successRate: 96.8, uptime: 99.6, satisfaction: 4.7 },
    { id: 13, name: 'RiskGuard AI', avatar: '🛡️', industry: 'Insurance', tier: 2, status: 'active', customers: 98, problemsSolved: 2154, revenue: 312000, successRate: 96.2, uptime: 99.5, satisfaction: 4.6 },
    { id: 14, name: 'EduFlow AI', avatar: '📚', industry: 'Education', tier: 2, status: 'launching', customers: 76, problemsSolved: 1654, revenue: 234000, successRate: 94.5, uptime: 99.4, satisfaction: 4.5 },
    { id: 15, name: 'CampaignIQ AI', avatar: '📢', industry: 'Marketing', tier: 2, status: 'active', customers: 112, problemsSolved: 2345, revenue: 278000, successRate: 95.7, uptime: 99.6, satisfaction: 4.6 },
    { id: 16, name: 'TalentFlow AI', avatar: '👥', industry: 'HR', tier: 2, status: 'active', customers: 87, problemsSolved: 1987, revenue: 245000, successRate: 95.2, uptime: 99.5, satisfaction: 4.5 },
    { id: 17, name: 'StrategyPro AI', avatar: '💼', industry: 'Consulting', tier: 2, status: 'launching', customers: 54, problemsSolved: 987, revenue: 198000, successRate: 96.5, uptime: 99.3, satisfaction: 4.7 },
    { id: 18, name: 'DesignGenius AI', avatar: '📐', industry: 'Architecture', tier: 2, status: 'planning', customers: 42, problemsSolved: 876, revenue: 167000, successRate: 94.8, uptime: 99.2, satisfaction: 4.4 },
    { id: 19, name: 'CalcMaster AI', avatar: '⚙️', industry: 'Engineering', tier: 2, status: 'planning', customers: 38, problemsSolved: 765, revenue: 154000, successRate: 95.3, uptime: 99.4, satisfaction: 4.5 },
    { id: 20, name: 'ContentKing AI', avatar: '🎬', industry: 'Media', tier: 2, status: 'planning', customers: 67, problemsSolved: 1234, revenue: 189000, successRate: 93.7, uptime: 99.1, satisfaction: 4.3 },

    // TIER 3: SPECIALIZED INDUSTRIES
    { id: 21, name: 'AutoTech AI', avatar: '🚗', industry: 'Automotive', tier: 3, status: 'planning', customers: 29, problemsSolved: 543, revenue: 123000, successRate: 94.2, uptime: 99.0, satisfaction: 4.4 },
    { id: 22, name: 'SkyOps AI', avatar: '✈️', industry: 'Aviation', tier: 3, status: 'planning', customers: 18, problemsSolved: 456, revenue: 289000, successRate: 96.8, uptime: 99.5, satisfaction: 4.8 },
    { id: 23, name: 'SeaRoute AI', avatar: '⚓', industry: 'Maritime', tier: 3, status: 'planning', customers: 15, problemsSolved: 387, revenue: 234000, successRate: 95.5, uptime: 99.3, satisfaction: 4.6 },
    { id: 24, name: 'NetFlow AI', avatar: '📡', industry: 'Telecom', tier: 3, status: 'planning', customers: 34, problemsSolved: 876, revenue: 298000, successRate: 95.9, uptime: 99.7, satisfaction: 4.7 },
    { id: 25, name: 'PharmaFlow AI', avatar: '💊', industry: 'Pharmaceutical', tier: 3, status: 'planning', customers: 22, problemsSolved: 654, revenue: 267000, successRate: 97.1, uptime: 99.6, satisfaction: 4.8 },
    { id: 26, name: 'ChemSafe AI', avatar: '🧪', industry: 'Chemical', tier: 3, status: 'planning', customers: 12, problemsSolved: 432, revenue: 198000, successRate: 96.3, uptime: 99.4, satisfaction: 4.7 },
    { id: 27, name: 'EarthCore AI', avatar: '⛏️', industry: 'Mining', tier: 3, status: 'planning', customers: 9, problemsSolved: 321, revenue: 245000, successRate: 95.7, uptime: 99.2, satisfaction: 4.6 },
    { id: 28, name: 'RecycleFlow AI', avatar: '♻️', industry: 'Waste Management', tier: 3, status: 'planning', customers: 31, problemsSolved: 765, revenue: 156000, successRate: 94.4, uptime: 99.3, satisfaction: 4.5 },
    { id: 29, name: 'GuardNet AI', avatar: '🔒', industry: 'Security', tier: 3, status: 'planning', customers: 27, problemsSolved: 687, revenue: 178000, successRate: 95.1, uptime: 99.5, satisfaction: 4.6 },
    { id: 30, name: 'EcoWatch AI', avatar: '🌍', industry: 'Environmental', tier: 3, status: 'planning', customers: 19, problemsSolved: 543, revenue: 189000, successRate: 96.2, uptime: 99.4, satisfaction: 4.7 },
  ];

  const filteredCapsules = selectedTier === 'all'
    ? capsules
    : capsules.filter(c => c.tier === selectedTier);

  const totalStats = {
    customers: capsules.reduce((sum, c) => sum + c.customers, 0),
    problemsSolved: capsules.reduce((sum, c) => sum + c.problemsSolved, 0),
    revenue: capsules.reduce((sum, c) => sum + c.revenue, 0),
    avgSuccessRate: (capsules.reduce((sum, c) => sum + c.successRate, 0) / capsules.length),
    avgUptime: (capsules.reduce((sum, c) => sum + c.uptime, 0) / capsules.length),
    avgSatisfaction: (capsules.reduce((sum, c) => sum + c.satisfaction, 0) / capsules.length),
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'launching': return 'text-blue-400';
      case 'planning': return 'text-yellow-400';
      case 'idle': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusBg = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-600';
      case 'launching': return 'bg-blue-600';
      case 'planning': return 'bg-yellow-600';
      case 'idle': return 'bg-gray-600';
      default: return 'bg-gray-600';
    }
  };

  return (
    <>
      <Head>
        <title>BIIE Capsule Dashboard | CodexDominion</title>
        <meta name="description" content="30 Industry Intelligence Capsules" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 text-white">
        {/* Header */}
        <div className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700 p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <span className="text-4xl">🌌</span>
                <div>
                  <h1 className="text-3xl font-bold">BIIE Capsule Dashboard</h1>
                  <p className="text-gray-400">Boring Industry Intelligence Engine - 30 Capsule Constellation</p>
                </div>
              </div>
            </div>

            {/* Total Stats */}
            <div className="grid grid-cols-6 gap-4">
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">30</div>
                <div className="text-sm">Total Capsules</div>
              </div>
              <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{totalStats.customers.toLocaleString()}</div>
                <div className="text-sm">Total Customers</div>
              </div>
              <div className="bg-gradient-to-r from-green-600 to-teal-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{totalStats.problemsSolved.toLocaleString()}</div>
                <div className="text-sm">Problems Solved</div>
              </div>
              <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">${(totalStats.revenue / 1000000).toFixed(1)}M</div>
                <div className="text-sm">Monthly Revenue</div>
              </div>
              <div className="bg-gradient-to-r from-red-600 to-pink-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{totalStats.avgSuccessRate.toFixed(1)}%</div>
                <div className="text-sm">Avg Success Rate</div>
              </div>
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-4 border border-white/20">
                <div className="text-2xl font-bold">{totalStats.avgUptime.toFixed(1)}%</div>
                <div className="text-sm">Avg Uptime</div>
              </div>
            </div>
          </div>
        </div>

        {/* Tier Filter */}
        <div className="bg-gray-800/30 backdrop-blur-lg border-b border-gray-700">
          <div className="max-w-7xl mx-auto flex space-x-2 px-6 py-3">
            {[
              { id: 'all' as const, label: 'All Capsules (30)', count: 30 },
              { id: 1 as const, label: 'Tier 1: Foundation (10)', count: 10 },
              { id: 2 as const, label: 'Tier 2: Professional (10)', count: 10 },
              { id: 3 as const, label: 'Tier 3: Specialized (10)', count: 10 },
            ].map((tier) => (
              <button
                key={tier.id}
                onClick={() => setSelectedTier(tier.id)}
                className={`px-6 py-2 font-semibold rounded-lg transition-colors ${
                  selectedTier === tier.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-400 hover:text-white'
                }`}
              >
                {tier.label}
              </button>
            ))}
          </div>
        </div>

        {/* Capsules Grid */}
        <div className="max-w-7xl mx-auto p-6">
          <div className="grid grid-cols-3 gap-4">
            {filteredCapsules.map((capsule) => (
              <div
                key={capsule.id}
                onClick={() => setSelectedCapsule(capsule)}
                className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-xl p-4 hover:border-blue-500 transition-all cursor-pointer"
              >
                {/* Header */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-4xl">{capsule.avatar}</span>
                    <div>
                      <h3 className="font-bold text-lg">{capsule.name}</h3>
                      <p className="text-xs text-gray-400">Capsule {capsule.id.toString().padStart(2, '0')}</p>
                    </div>
                  </div>
                  <div className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBg(capsule.status)}`}>
                    {capsule.status.toUpperCase()}
                  </div>
                </div>

                {/* Industry */}
                <div className="mb-3">
                  <div className="text-sm text-gray-400">Industry</div>
                  <div className="font-semibold">{capsule.industry}</div>
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-2 gap-2 mb-3">
                  <div className="bg-gray-900/50 rounded p-2">
                    <div className="text-xs text-gray-400">Customers</div>
                    <div className="text-lg font-bold">{capsule.customers}</div>
                  </div>
                  <div className="bg-gray-900/50 rounded p-2">
                    <div className="text-xs text-gray-400">Solved</div>
                    <div className="text-lg font-bold">{capsule.problemsSolved.toLocaleString()}</div>
                  </div>
                  <div className="bg-gray-900/50 rounded p-2">
                    <div className="text-xs text-gray-400">Revenue</div>
                    <div className="text-lg font-bold">${(capsule.revenue / 1000).toFixed(0)}K</div>
                  </div>
                  <div className="bg-gray-900/50 rounded p-2">
                    <div className="text-xs text-gray-400">Success</div>
                    <div className="text-lg font-bold">{capsule.successRate.toFixed(1)}%</div>
                  </div>
                </div>

                {/* Footer Stats */}
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-1">
                    <span className="text-green-400">●</span>
                    <span className="text-gray-400">{capsule.uptime.toFixed(1)}% uptime</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span className="text-yellow-400">⭐</span>
                    <span className="text-gray-400">{capsule.satisfaction.toFixed(1)}/5.0</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Capsule Detail Modal */}
        {selectedCapsule && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50" onClick={() => setSelectedCapsule(null)}>
            <div className="bg-gray-800 rounded-xl border border-gray-700 max-w-2xl w-full p-6" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-4">
                  <span className="text-6xl">{selectedCapsule.avatar}</span>
                  <div>
                    <h2 className="text-3xl font-bold">{selectedCapsule.name}</h2>
                    <p className="text-gray-400">{selectedCapsule.industry} Intelligence</p>
                  </div>
                </div>
                <button onClick={() => setSelectedCapsule(null)} className="text-gray-400 hover:text-white text-2xl">×</button>
              </div>

              <div className="space-y-4">
                {/* Status */}
                <div>
                  <div className="text-sm text-gray-400 mb-1">Status</div>
                  <div className={`inline-block px-4 py-2 rounded-lg ${getStatusBg(selectedCapsule.status)} font-semibold`}>
                    {selectedCapsule.status.toUpperCase()}
                  </div>
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-3xl font-bold text-blue-400">{selectedCapsule.customers}</div>
                    <div className="text-sm text-gray-400">Customers Served</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-3xl font-bold text-green-400">{selectedCapsule.problemsSolved.toLocaleString()}</div>
                    <div className="text-sm text-gray-400">Problems Solved</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-3xl font-bold text-yellow-400">${(selectedCapsule.revenue / 1000).toFixed(0)}K</div>
                    <div className="text-sm text-gray-400">Monthly Revenue</div>
                  </div>
                </div>

                {/* Performance */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-purple-400">{selectedCapsule.successRate.toFixed(1)}%</div>
                    <div className="text-sm text-gray-400">Success Rate</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-green-400">{selectedCapsule.uptime.toFixed(1)}%</div>
                    <div className="text-sm text-gray-400">Uptime</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <div className="text-2xl font-bold text-yellow-400">{selectedCapsule.satisfaction.toFixed(1)}/5.0</div>
                    <div className="text-sm text-gray-400">Satisfaction</div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-3 pt-4">
                  <button className="flex-1 py-3 bg-blue-600 rounded-lg hover:bg-blue-700 font-semibold">
                    📊 View Analytics
                  </button>
                  <button className="flex-1 py-3 bg-green-600 rounded-lg hover:bg-green-700 font-semibold">
                    💬 Chat with Avatar
                  </button>
                  <button className="flex-1 py-3 bg-purple-600 rounded-lg hover:bg-purple-700 font-semibold">
                    ⚙️ Configure
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
