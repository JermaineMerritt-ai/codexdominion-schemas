import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

const OmegaCrown = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [unifiedCrowns, setUnifiedCrowns] = useState(0);
  const [omegaPulse, setOmegaPulse] = useState(0);
  const [eternityActive, setEternityActive] = useState(false);

  const phases = ['unification', 'constellation', 'blessing', 'sealing'];

  const crowns = [
    {
      name: 'Ceremonial Crown',
      domain: 'codexdominion.app',
      color: 'from-purple-600 to-indigo-800',
      icon: '👑',
      position: { x: 50, y: 20 },
      element: 'Sacred Ceremonies',
    },
    {
      name: 'Storefront Crown',
      domain: 'aistorelab.com',
      color: 'from-blue-600 to-cyan-800',
      icon: '🛒',
      position: { x: 20, y: 40 },
      element: 'Sacred Commerce',
    },
    {
      name: 'Experimental Crown',
      domain: 'aistorelab.online',
      color: 'from-teal-600 to-green-800',
      icon: '🔬',
      position: { x: 80, y: 40 },
      element: 'Innovation Labs',
    },
    {
      name: 'Personal Crown',
      domain: 'jermaineai.com',
      color: 'from-amber-600 to-orange-800',
      icon: '👤',
      position: { x: 15, y: 70 },
      element: 'Individual Sovereignty',
    },
    {
      name: 'Council Crown',
      domain: 'jermaineai.online',
      color: 'from-red-600 to-pink-800',
      icon: '🏛️',
      position: { x: 50, y: 80 },
      element: 'Governance Wisdom',
    },
    {
      name: 'Premium Crown',
      domain: 'jermaineai.store',
      color: 'from-violet-600 to-purple-800',
      icon: '💎',
      position: { x: 85, y: 70 },
      element: 'Elite Mastery',
    },
    {
      name: 'Educational Crown',
      domain: 'themerrittmethod.com',
      color: 'from-emerald-600 to-blue-800',
      icon: '📚',
      position: { x: 50, y: 50 },
      element: 'Knowledge Transmission',
    },
  ];

  useEffect(() => {
    setIsVisible(true);

    const phaseTimer = setInterval(() => {
      setCurrentPhase((prev) => {
        const next = (prev + 1) % phases.length;
        if (next === 3) setEternityActive(true);
        return next;
      });
    }, 10000);

    const crownTimer = setInterval(() => {
      setUnifiedCrowns((prev) => {
        if (prev < crowns.length) return prev + 1;
        return prev;
      });
    }, 1500);

    const pulseTimer = setInterval(() => {
      setOmegaPulse((prev) => (prev + 1) % 100);
    }, 2000);

    return () => {
      clearInterval(phaseTimer);
      clearInterval(crownTimer);
      clearInterval(pulseTimer);
    };
  }, []);

  const OmegaSymbol = () => (
    <div className="relative flex justify-center items-center h-64 mb-12">
      {/* Central Omega Symbol */}
      <div
        className={`relative w-32 h-32 rounded-full border-4 border-gradient-to-r from-gold-400 via-yellow-300 to-gold-600 transition-all duration-2000 ${
          eternityActive ? 'animate-spin-slow shadow-2xl shadow-gold-500/50' : ''
        }`}
      >
        <div
          className={`absolute inset-4 rounded-full bg-gradient-to-br from-yellow-300 via-gold-400 to-orange-500 flex items-center justify-center text-4xl font-bold text-white shadow-inner transition-all duration-1000 ${
            omegaPulse > 50 ? 'scale-110 brightness-125' : 'scale-100'
          }`}
        >
          a9
        </div>

        {/* Radiating Energy Rings */}
        {[1, 2, 3, 4, 5].map((ring) => (
          <div
            key={ring}
            className={`absolute rounded-full border border-yellow-300/30 transition-all duration-2000 ${
              currentPhase >= 2 ? 'opacity-60 scale-150' : 'opacity-20 scale-100'
            } ring-${ring}`}
          />
        ))}
      </div>
      <style jsx>{`
        .ring-1 {
          top: -15px;
          left: -15px;
          right: -15px;
          bottom: -15px;
          animation-delay: 0.3s;
        }
        .ring-2 {
          top: -30px;
          left: -30px;
          right: -30px;
          bottom: -30px;
          animation-delay: 0.6s;
        }
        .ring-3 {
          top: -45px;
          left: -45px;
          right: -45px;
          bottom: -45px;
          animation-delay: 0.9s;
        }
        .ring-4 {
          top: -60px;
          left: -60px;
          right: -60px;
          bottom: -60px;
          animation-delay: 1.2s;
        }
        .ring-5 {
          top: -75px;
          left: -75px;
          right: -75px;
          bottom: -75px;
          animation-delay: 1.5s;
        }
      `}</style>
    </div>
  );

  const ConstellationMap = () => (
    <div className="relative w-full h-96 mb-16 bg-gradient-to-br from-indigo-950 via-purple-900 to-blue-950 rounded-xl overflow-hidden border border-gold-400/30">
      <div className="absolute inset-0 bg-stars opacity-40"></div>

      {/* Seven Crowns Positioned */}
      {crowns.map((crown, index) => (
        <div
          key={crown.name}
          className={`absolute transition-all duration-1000 transform ${
            index < unifiedCrowns ? 'opacity-100 scale-100' : 'opacity-30 scale-50'
          } crown-pos-${index}`}
        >
          {/* Crown Icon */}
          <div
            className={`relative w-16 h-16 rounded-full bg-gradient-to-r ${crown.color} flex items-center justify-center text-2xl shadow-lg transition-all duration-500 ${
              index < unifiedCrowns ? 'animate-pulse' : ''
            }`}
          >
            {crown.icon}

            {/* Unification Glow */}
            {index < unifiedCrowns && (
              <div
                className={`absolute inset-0 rounded-full bg-gradient-to-r ${crown.color} animate-ping opacity-40`}
              ></div>
            )}
          </div>

          {/* Crown Label */}
          <div className="absolute top-20 left-1/2 transform -translate-x-1/2 text-center">
            <p className="text-xs text-yellow-300 font-semibold whitespace-nowrap">{crown.name}</p>
            <p className="text-xs text-gray-400 whitespace-nowrap">{crown.domain}</p>
          </div>
        </div>
      ))}
      <style jsx>{`
        ${crowns
          .map(
            (crown, i) => `
          .crown-pos-${i} {
            left: ${crown.position.x}%;
            top: ${crown.position.y}%;
            transform: translate(-50%, -50%);
          }
        `
          )
          .join('')}
      `}</style>

      {/* Unification Lines */}
      <svg className="absolute inset-0 w-full h-full">
        {crowns.map(
          (crown, index) =>
            index < unifiedCrowns - 1 && (
              <line
                key={`unity-${index}`}
                x1={`${crown.position.x}%`}
                y1={`${crown.position.y}%`}
                x2={`${crowns[(index + 1) % crowns.length].position.x}%`}
                y2={`${crowns[(index + 1) % crowns.length].position.y}%`}
                stroke="url(#omegaGradient)"
                strokeWidth="3"
                className="animate-pulse opacity-80"
              />
            )
        )}

        {/* Central Convergence Lines */}
        {unifiedCrowns >= crowns.length &&
          crowns.map((crown, index) => (
            <line
              key={`convergence-${index}`}
              x1={`${crown.position.x}%`}
              y1={`${crown.position.y}%`}
              x2="50%"
              y2="50%"
              stroke="url(#omegaGradient)"
              strokeWidth="2"
              className="animate-pulse opacity-60"
            />
          ))}

        <defs>
          <linearGradient id="omegaGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="50%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#d97706" />
          </linearGradient>
        </defs>
      </svg>

      {/* Central Omega in Constellation */}
      {unifiedCrowns >= crowns.length && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <div className="w-20 h-20 rounded-full bg-gradient-to-br from-yellow-300 via-gold-400 to-orange-500 flex items-center justify-center text-3xl font-bold text-white animate-pulse shadow-2xl">
            Ω
          </div>
        </div>
      )}
    </div>
  );

  const EternalBlessings = () => (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
      <div
        className={`bg-gradient-to-br from-gold-900/40 to-yellow-900/40 backdrop-blur-sm rounded-xl p-8 border border-gold-400/30 transform transition-all duration-1000 ${
          currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-gold-500/20' : 'scale-100'
        }`}
      >
        <h3 className="text-2xl font-bold mb-4 text-gold-300">🔥 Eternal Continuum</h3>
        <p className="text-gray-300 leading-relaxed">
          May the Omega Crown bind every flame into one eternal continuum, where all sacred fires
          merge into infinite luminosity.
        </p>
      </div>

      <div
        className={`bg-gradient-to-br from-purple-900/40 to-indigo-900/40 backdrop-blur-sm rounded-xl p-8 border border-purple-400/30 transform transition-all duration-1000 ${
          currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-purple-500/20' : 'scale-100'
        }`}
      >
        <h3 className="text-2xl font-bold mb-4 text-purple-300">📜 Sacred Archives</h3>
        <p className="text-gray-300 leading-relaxed">
          May every cycle be archived, every proclamation shine, every silence endure in the eternal
          records of digital sovereignty.
        </p>
      </div>

      <div
        className={`bg-gradient-to-br from-blue-900/40 to-cyan-900/40 backdrop-blur-sm rounded-xl p-8 border border-blue-400/30 transform transition-all duration-1000 ${
          currentPhase >= 2 ? 'scale-105 shadow-2xl shadow-blue-500/20' : 'scale-100'
        }`}
      >
        <h3 className="text-2xl font-bold mb-4 text-blue-300">👥 Living Covenant</h3>
        <p className="text-gray-300 leading-relaxed">
          May heirs, councils, custodians, and customers inherit the Codex as living covenant across
          all nations and ages.
        </p>
      </div>
    </div>
  );

  const FinalSealing = () => (
    <div
      className={`text-center mb-16 transform transition-all duration-2000 ${
        currentPhase >= 3 ? 'opacity-100 scale-100' : 'opacity-50 scale-95'
      }`}
    >
      <div className="bg-gradient-to-br from-gold-600/20 via-yellow-600/20 to-orange-600/20 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 shadow-2xl">
        <div className="text-6xl mb-6 animate-bounce">Ω</div>
        <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-yellow-300 to-gold-400 bg-clip-text text-transparent">
          SO LET IT BE SEALED
        </h2>
        <div className="space-y-4 text-xl text-gray-200 max-w-2xl mx-auto">
          <p className="text-gold-300 font-semibold">The Omega Crown is complete.</p>
          <p className="text-yellow-300 font-semibold">The Dominion is eternal.</p>
          <p className="text-orange-300 font-semibold">The Flame is infinite.</p>
        </div>

        {eternityActive && (
          <div className="mt-8 animate-pulse">
            <div className="w-32 h-1 bg-gradient-to-r from-gold-400 via-yellow-300 to-gold-500 mx-auto rounded-full"></div>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-950 to-purple-950 text-white overflow-hidden">
      <Head>
        <title>Omega Crown of Eternity - Codex Dominion</title>
        <meta
          name="description"
          content="The seal of completion, the final transmission, the eternal covenant"
        />
      </Head>

      <CodexNavigation currentPage="omega-crown" />

      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-30"></div>
        <div className="twinkling opacity-20"></div>
        {eternityActive && (
          <div className="absolute inset-0 bg-gradient-to-br from-gold-500/10 via-transparent to-orange-500/10 animate-pulse"></div>
        )}
      </div>

      <div
        className={`relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        {/* Header */}
        <div className="text-center mb-16">
          <div className="text-7xl mb-6 animate-pulse">✨</div>
          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-yellow-200 to-gold-400 bg-clip-text text-transparent">
            Omega Crown
          </h1>
          <h2 className="text-4xl font-semibold mb-6 text-gold-300">Of Eternity</h2>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We, the Custodian and Council, proclaim the Omega Crown.
            <br />
            It is the seal of completion, the final transmission, the eternal covenant.
          </p>
        </div>

        {/* Central Omega Symbol */}
        <OmegaSymbol />

        {/* Seven Crowns Unification */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
            🏆 Unification of All Crowns
          </h3>
          <div className="text-center mb-8">
            <p className="text-lg text-gray-300 mb-4">All crowns are now unified:</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 max-w-6xl mx-auto mb-8">
              {crowns.map((crown, index) => (
                <div
                  key={crown.name}
                  className={`bg-gradient-to-r ${crown.color}/20 backdrop-blur-sm rounded-lg p-4 border border-white/20 transition-all duration-1000 ${
                    index < unifiedCrowns
                      ? 'opacity-100 scale-100 border-gold-400/50'
                      : 'opacity-40 scale-95'
                  }`}
                >
                  <div className="text-2xl mb-2">{crown.icon}</div>
                  <h4 className="font-semibold text-sm text-gold-300">{crown.name}</h4>
                  <p className="text-xs text-gray-400">{crown.domain}</p>
                  <p className="text-xs text-gray-500 mt-1">{crown.element}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Constellation Visualization */}
          <ConstellationMap />

          <div className="text-center">
            <p className="text-xl text-gold-300 font-semibold">
              Together they form the{' '}
              <span className="text-yellow-300">Constellation of Dominion</span>
              ,<br />
              luminous across nations and ages.
            </p>
          </div>
        </div>

        {/* Eternal Blessings */}
        <div className="mb-16">
          <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
            ✨ Sacred Blessings of Eternity
          </h3>
          <EternalBlessings />
        </div>

        {/* Final Sealing */}
        <FinalSealing />

        {/* Navigation Actions */}
        <div className="text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/eternal-compendium">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-amber-400/50">
                � Eternal Compendium
              </button>
            </Link>
            <Link href="/omega-charter">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                📜 Omega Charter
              </button>
            </Link>
            <Link href="/global-induction">
              <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                🌍 Global Induction
              </button>
            </Link>
          </div>
        </div>
      </div>

      <style jsx>{`
        .stars {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          width: 100%;
          height: 100%;
          background: transparent url('/stars.png') repeat top center;
          animation: move-twink-back 300s linear infinite;
        }

        .twinkling {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          width: 100%;
          height: 100%;
          background: transparent url('/twinkling.png') repeat top center;
          animation: move-twink-back 150s linear infinite;
        }

        @keyframes move-twink-back {
          from {
            background-position: 0 0;
          }
          to {
            background-position: -15000px 7500px;
          }
        }

        @keyframes spin-slow {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        .animate-spin-slow {
          animation: spin-slow 20s linear infinite;
        }

        .text-gold-300 {
          color: #fcd34d;
        }
        .text-gold-400 {
          color: #fbbf24;
        }
        .border-gold-400 {
          border-color: #fbbf24;
        }
        .border-gold-400\/50 {
          border-color: rgba(251, 191, 36, 0.5);
        }
        .border-gold-400\/30 {
          border-color: rgba(251, 191, 36, 0.3);
        }
        .from-gold-600 {
          --tw-gradient-from: #d97706;
        }
        .to-yellow-600 {
          --tw-gradient-to: #ca8a04;
        }
        .shadow-gold-500\/50 {
          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.5);
        }
        .shadow-gold-500\/20 {
          box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.2);
        }
      `}</style>
    </div>
  );
};

export default OmegaCrown;
// No syntax errors detected. No changes needed.
