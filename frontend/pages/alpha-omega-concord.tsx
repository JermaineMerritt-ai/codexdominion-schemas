import React from 'react';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

// Alpha Symbol Component
const AlphaSymbol = () => {
  return (
    <div className="text-8xl font-bold text-blue-400 animate-pulse">
      Α
    </div>
  );
};

// Omega Symbol Component
const OmegaSymbol = () => {
  return (
    <div className="text-8xl font-bold text-gold-400 animate-pulse">
      Ω
    </div>
  );
};

// Continuum Bridge Component
const ContinuumBridge = () => {
  return (
    <div className="flex items-center justify-center my-8">
      <div className="flex items-center space-x-4">
        <AlphaSymbol />
        <div className="w-32 opacity-100">
          <div className="h-1 bg-gradient-to-r from-blue-400 via-purple-400 to-gold-400 rounded-full animate-pulse"></div>
          <div className="text-center mt-2 text-sm text-purple-300 font-semibold">
            ETERNAL CONTINUUM
          </div>
        </div>
        <OmegaSymbol />
      </div>
    </div>
  );
};

// Covenant Seal Component
const CovenantSeal = () => {
  return (
    <div className="scale-100 opacity-100 rotate-0 transition-all duration-2000 transform">
      <div className="relative w-32 h-32 mx-auto">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-400/30 via-purple-400/30 to-gold-400/30 rounded-full backdrop-blur-sm border-2 border-purple-400/50"></div>
        <div className="absolute inset-4 bg-gradient-to-br from-blue-500/40 via-purple-500/40 to-gold-500/40 rounded-full backdrop-blur-sm"></div>
        <div className="absolute inset-8 bg-gradient-to-br from-blue-600/50 via-purple-600/50 to-gold-600/50 rounded-full backdrop-blur-sm flex items-center justify-center">
          <div className="text-2xl font-bold text-white animate-pulse">∞</div>
        </div>
      </div>
    </div>
  );
};

// Luminous Crown Visualization
const LuminousCrowns = () => {
  const crowns = [
    { name: 'Primordialis', symbol: '🔥', color: 'text-red-400' },
    { name: 'Custodian', symbol: '👑', color: 'text-purple-400' },
    { name: 'Heir', symbol: '🏛️', color: 'text-blue-400' },
    { name: 'Customer', symbol: '⭐', color: 'text-green-400' },
    { name: 'Constellation', symbol: '🌟', color: 'text-indigo-400' },
    { name: 'Transmission', symbol: '📡', color: 'text-cyan-400' },
    { name: 'Omega', symbol: 'Ω', color: 'text-gold-400' }
  ];

  return (
    <div className="grid grid-cols-7 gap-4 max-w-4xl mx-auto">
      {crowns.map((crown, index) => (
        <div key={crown.name} className="text-center">
          <div className={`text-3xl ${crown.color} animate-pulse`} style={{ animationDelay: `${index * 300}ms` }}>
            {crown.symbol}
          </div>
          <div className="text-xs text-gray-300 mt-1">{crown.name}</div>
        </div>
      ))}
    </div>
  );
};

export default function AlphaOmegaConcord() {

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 text-white">
      <CodexNavigation />
      
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="text-6xl mb-6">✨</div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-300 via-purple-300 to-gold-300 bg-clip-text text-transparent">
            Alpha–Omega Concord
          </h1>
          <h2 className="text-3xl font-bold mb-8 text-purple-300">
            of the Codex Dominion
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            We, the Custodian and Council, inscribe this Concord as eternal covenant.<br/>
            It binds the First Flame of Primordialis to the Final Crown of Omega,<br/>
            so that genesis and completion are one continuum, luminous and unbroken.
          </p>
        </div>

        {/* Continuum Bridge */}
        <div className="mb-16">
          <ContinuumBridge />
        </div>

        {/* Alpha Section */}
        <div className="mb-16 opacity-100 transform translate-y-0 transition-all duration-1000">
          <div className="bg-gradient-to-br from-blue-600/20 via-blue-500/20 to-cyan-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-blue-400/50 shadow-2xl max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4 text-blue-400">Α</div>
              <h3 className="text-4xl font-bold text-blue-300 mb-6">Alpha — Codex Originum Primordialis</h3>
            </div>
            <div className="space-y-4 text-xl text-gray-200">
              <p className="text-blue-300 font-bold">🔥 The First Flame is lit.</p>
              <p className="text-cyan-300 font-bold">⚡ The Originum Crest is forged.</p>
              <p className="text-blue-200 font-bold">🗿 The Custodian Genesis Oathstone is bound.</p>
              <p className="text-indigo-200 font-bold">✨ The ceremonial singularity is initiated, and all realms trace their lineage to this source.</p>
            </div>
          </div>
        </div>

        {/* Omega Section */}
        <div className="mb-16 opacity-100 transform translate-y-0 transition-all duration-1000">
          <div className="bg-gradient-to-br from-gold-600/20 via-yellow-600/20 to-orange-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <div className="text-6xl mb-4 text-gold-400">Ω</div>
              <h3 className="text-4xl font-bold text-gold-300 mb-6">Omega — Codex Eternum Omega</h3>
            </div>
            <div className="space-y-4 text-xl text-gray-200">
              <p className="text-gold-300 font-bold">👑 The Final Crown is sealed.</p>
              <p className="text-yellow-300 font-bold">🌟 The Constellation of Domains shines as seven luminous crowns.</p>
              <p className="text-gold-200 font-bold">📜 The Eternal Charter is proclaimed.</p>
              <p className="text-orange-200 font-bold">🌍 The Dominion is complete, planetary, and cosmic.</p>
            </div>
          </div>
        </div>

        {/* Luminous Crowns Visualization */}
        <div className="mb-16 opacity-100 transform translate-y-0 transition-all duration-1000">
          <div className="text-center mb-8">
            <h3 className="text-3xl font-bold text-purple-300 mb-6">Seven Luminous Crowns</h3>
            <LuminousCrowns />
          </div>
        </div>

        {/* Concord of Alpha and Omega */}
        <div className="mb-16 opacity-100 transform translate-y-0 transition-all duration-1000">
          <div className="bg-gradient-to-br from-purple-600/20 via-indigo-600/20 to-blue-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-purple-400/50 shadow-2xl max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <div className="text-5xl mb-4">∞</div>
              <h3 className="text-4xl font-bold text-purple-300 mb-6">Concord of Alpha and Omega</h3>
            </div>
            <div className="space-y-4 text-xl text-gray-200">
              <p className="text-purple-300 font-bold">⚡ Alpha is the spark, Omega is the seal.</p>
              <p className="text-indigo-300 font-bold">🔄 Together they form the eternal continuum.</p>
              <p className="text-blue-300 font-bold">🌀 Every cycle begins in Primordialis and ends in Omega.</p>
              <p className="text-cyan-300 font-bold">📢 Every proclamation echoes from genesis to completion.</p>
              <p className="text-purple-200 font-bold">🤝 Every participant is bound in covenant across ages and stars.</p>
            </div>
          </div>
        </div>

        {/* Eternal Blessing */}
        <div className="mb-16">
          <div className="bg-gradient-to-br from-gold-600/20 via-purple-600/20 to-blue-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <CovenantSeal />
              <h3 className="text-4xl font-bold mb-8 bg-gradient-to-r from-blue-300 via-purple-300 to-gold-300 bg-clip-text text-transparent mt-6">
                Eternal Blessing
              </h3>
            </div>
            <div className="space-y-4 text-xl text-gray-200 text-center">
              <p className="text-blue-300 font-bold">🔥 May the Alpha Flame never fade.</p>
              <p className="text-gold-300 font-bold">👑 May the Omega Crown never break.</p>
              <p className="text-purple-300 font-bold">✨ May the Codex Dominion endure as eternal covenant,</p>
              <p className="text-indigo-300 font-bold">🌟 luminous across nations, worlds, and cosmos.</p>
            </div>
          </div>
        </div>

        {/* Sacred Navigation */}
          <div className="text-center mb-16">
            <h3 className="text-2xl font-bold text-purple-300 mb-8">Sacred Navigation</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
              <Link href="/eternal-compendium">
                <button className="px-6 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-amber-400/50 w-full">
                  📖 Eternal Compendium
                </button>
              </Link>
              <Link href="/omega-charter">
                <button className="px-6 py-4 bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                  📜 Omega Charter
                </button>
              </Link>
              <Link href="/omega-crown">
                <button className="px-6 py-4 bg-gradient-to-r from-gold-600 to-yellow-600 hover:from-gold-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                  Ω Omega Crown
                </button>
              </Link>
              <Link href="/codex-constellation">
                <button className="px-6 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                  ⭐ View Constellation
                </button>
              </Link>
            </div>
          </div>

        {/* Cosmic Declaration */}
          <div className="text-center">
            <div className="bg-gradient-to-br from-indigo-600/20 via-purple-600/20 to-pink-600/20 backdrop-blur-sm rounded-2xl p-8 border-2 border-purple-400/50 shadow-2xl max-w-2xl mx-auto">
              <div className="text-5xl mb-4 animate-pulse">∞</div>
              <p className="text-2xl font-bold bg-gradient-to-r from-blue-300 via-purple-300 to-gold-300 bg-clip-text text-transparent mb-4">
                CONCORD ETERNALLY SEALED
              </p>
              <p className="text-lg text-purple-300">
                The Alpha-Omega Continuum is complete.<br/>
                Genesis and Completion are One.<br/>
                The Dominion shines eternal.
              </p>
            </div>
          </div>
      </div>
    </div>
  );
}