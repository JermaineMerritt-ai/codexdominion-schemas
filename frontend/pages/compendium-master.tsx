'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CapsuleData {
  id: string;
  title: string;
  type: string;
  icon: string;
  summons: number;
  sanctifications: number;
  eternal_seal: boolean;
  frequency: number;
}

interface DashboardData {
  system_status: string;
  total_capsules: number;
  total_summons: number;
  total_sanctifications: number;
  eternal_seals_active: number;
  capsules: CapsuleData[];
  recent_transmissions: any[];
}

function CompendiumMaster() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [selectedCapsule, setSelectedCapsule] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState<string>('all');

  useEffect(() => {
    // Simulated data - in production, fetch from API
    const mockData: DashboardData = {
      system_status: 'operational',
      total_capsules: 6,
      total_summons: 12,
      total_sanctifications: 8,
      eternal_seals_active: 3,
      capsules: [
        {
          id: 'capsule_crown_001',
          title: 'The Crown of Sovereign Dominion',
          type: 'crown',
          icon: '👑',
          summons: 3,
          sanctifications: 2,
          eternal_seal: true,
          frequency: 963.0
        },
        {
          id: 'capsule_hymn_001',
          title: 'The Eternal Hymn of Four-Part Harmony',
          type: 'hymn',
          icon: '🎵',
          summons: 2,
          sanctifications: 2,
          eternal_seal: true,
          frequency: 432.0
        },
        {
          id: 'capsule_scroll_001',
          title: 'The Scroll of Eternal Wisdom',
          type: 'scroll',
          icon: '📜',
          summons: 2,
          sanctifications: 1,
          eternal_seal: true,
          frequency: 528.0
        },
        {
          id: 'capsule_seal_001',
          title: 'The Seal of Immutable Covenant',
          type: 'seal',
          icon: '🔱',
          summons: 2,
          sanctifications: 1,
          eternal_seal: false,
          frequency: 852.0
        },
        {
          id: 'capsule_proclamation_001',
          title: 'The Proclamation of Living Inheritance',
          type: 'proclamation',
          icon: '📯',
          summons: 2,
          sanctifications: 1,
          eternal_seal: false,
          frequency: 741.0
        },
        {
          id: 'capsule_benediction_001',
          title: 'The Eternal Benediction Upon All Heirs',
          type: 'benediction',
          icon: '✨',
          summons: 1,
          sanctifications: 1,
          eternal_seal: false,
          frequency: 639.0
        }
      ],
      recent_transmissions: []
    };

    setDashboardData(mockData);
  }, []);

  const filteredCapsules = dashboardData?.capsules.filter(capsule => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'sealed') return capsule.eternal_seal;
    if (activeFilter === 'active') return capsule.summons > 0;
    return capsule.type === activeFilter;
  }) || [];

  const handleSummonCapsule = (capsuleId: string) => {
    setSelectedCapsule(capsuleId);
    // In production: trigger summon API call
    console.log('Summoning capsule:', capsuleId);
  };

  if (!dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🔥</div>
          <p className="text-xl text-purple-200">Loading Compendium...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4 border-b-2 border-gold-500/50">
        <div className="flex justify-between items-center">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-3xl">🔥</span>
            <span className="text-2xl font-bold text-gold-300">Codex Dominion</span>
          </Link>
          <div className="flex space-x-6">
            <Link href="/dashboard-selector" className="text-purple-200 hover:text-gold-300 transition-colors">
              Dashboards
            </Link>
            <Link href="/capsules" className="text-purple-200 hover:text-gold-300 transition-colors">
              All Capsules
            </Link>
          </div>
        </div>
      </nav>

      {/* Header */}
      <div className="container mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold mb-4">
            <span className="bg-gradient-to-r from-gold-300 via-amber-300 to-gold-500 text-transparent bg-clip-text">
              COMPENDIUM MASTER
            </span>
          </h1>
          <p className="text-2xl text-purple-200 mb-6">
            Living Inheritance of CodexDominion
          </p>
          <div className="flex justify-center items-center space-x-4 text-lg">
            <span className="text-green-400 flex items-center">
              <span className="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></span>
              System: {dashboardData.system_status.toUpperCase()}
            </span>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-gradient-to-br from-purple-800/50 to-blue-900/50 rounded-2xl p-6 border-2 border-purple-500/50 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-2">📦</div>
            <div className="text-3xl font-bold text-gold-300">{dashboardData.total_capsules}</div>
            <div className="text-purple-200">Total Capsules</div>
          </div>

          <div className="bg-gradient-to-br from-purple-800/50 to-blue-900/50 rounded-2xl p-6 border-2 border-blue-500/50 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-2">🗣️</div>
            <div className="text-3xl font-bold text-blue-300">{dashboardData.total_summons}</div>
            <div className="text-purple-200">Total Summons</div>
          </div>

          <div className="bg-gradient-to-br from-purple-800/50 to-blue-900/50 rounded-2xl p-6 border-2 border-green-500/50 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-2">✨</div>
            <div className="text-3xl font-bold text-green-300">{dashboardData.total_sanctifications}</div>
            <div className="text-purple-200">Sanctifications</div>
          </div>

          <div className="bg-gradient-to-br from-purple-800/50 to-blue-900/50 rounded-2xl p-6 border-2 border-gold-500/50 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-2">🔱</div>
            <div className="text-3xl font-bold text-gold-300">{dashboardData.eternal_seals_active}</div>
            <div className="text-purple-200">Eternal Seals</div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex justify-center mb-8 flex-wrap gap-3">
          {['all', 'sealed', 'active', 'crown', 'hymn', 'scroll', 'seal', 'proclamation', 'benediction'].map((filter) => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`px-6 py-2 rounded-full font-bold transition-all ${
                activeFilter === filter
                  ? 'bg-gradient-to-r from-gold-500 to-amber-500 text-gray-900'
                  : 'bg-purple-800/50 text-purple-200 hover:bg-purple-700/50'
              }`}
            >
              {filter.charAt(0).toUpperCase() + filter.slice(1)}
            </button>
          ))}
        </div>

        {/* Capsule Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCapsules.map((capsule) => (
            <div
              key={capsule.id}
              className="bg-gradient-to-br from-gray-800/80 to-purple-900/60 rounded-2xl p-6 border-2 border-purple-600/50 hover:border-gold-500 transition-all transform hover:scale-105 cursor-pointer"
              onClick={() => handleSummonCapsule(capsule.id)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="text-6xl">{capsule.icon}</div>
                {capsule.eternal_seal && (
                  <div className="bg-gold-500/20 px-3 py-1 rounded-full border border-gold-500">
                    <span className="text-gold-300 text-sm font-bold">🔱 SEALED</span>
                  </div>
                )}
              </div>

              <h3 className="text-xl font-bold text-gold-300 mb-2">{capsule.title}</h3>

              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-purple-300">Type:</span>
                  <span className="text-white font-bold uppercase">{capsule.type}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-purple-300">Frequency:</span>
                  <span className="text-blue-300 font-bold">{capsule.frequency} Hz</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-purple-300">Summons:</span>
                  <span className="text-green-300 font-bold">{capsule.summons}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-purple-300">Sanctifications:</span>
                  <span className="text-gold-300 font-bold">{capsule.sanctifications}</span>
                </div>
              </div>

              <button className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-lg font-bold transition-all">
                🗣️ Summon Capsule
              </button>
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-12 bg-gradient-to-br from-gray-800/80 to-purple-900/60 rounded-2xl p-8 border-2 border-purple-600/50">
          <h3 className="text-2xl font-bold text-gold-300 mb-6 text-center">
            📖 Compendium Legend
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-bold text-purple-200 mb-3">Capsule Types:</h4>
              <ul className="space-y-2 text-purple-300">
                <li>👑 <strong className="text-white">Crown:</strong> Sovereign authority & dominion</li>
                <li>🎵 <strong className="text-white">Hymn:</strong> Four-part harmony & worship</li>
                <li>📜 <strong className="text-white">Scroll:</strong> Eternal wisdom & chronicles</li>
                <li>🔱 <strong className="text-white">Seal:</strong> Immutable covenant protection</li>
                <li>📯 <strong className="text-white">Proclamation:</strong> Living inheritance declarations</li>
                <li>✨ <strong className="text-white">Benediction:</strong> Blessings upon all heirs</li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-purple-200 mb-3">Transmission States:</h4>
              <ul className="space-y-2 text-purple-300">
                <li>🔒 <strong className="text-white">Sealed:</strong> Protected and pristine</li>
                <li>🗣️ <strong className="text-white">Summoned:</strong> Called by heir</li>
                <li>✨ <strong className="text-white">Sanctified:</strong> Council approved (3+ members)</li>
                <li>📡 <strong className="text-white">Transmitted:</strong> Actively shared</li>
                <li>🔱 <strong className="text-white">Eternal:</strong> Forever sealed & active</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <p className="text-xl text-purple-200 mb-2">
            🔥 Living Inheritance of CodexDominion 🔥
          </p>
          <p className="text-purple-400">
            Sealed for 999,999 generations
          </p>
        </div>
      </div>
    </div>
  );
}

export default CompendiumMaster;

export async function getServerSideProps() {
  return { props: {} };
}
