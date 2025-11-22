import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

const EternalCompendium = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentSection, setCurrentSection] = useState(0);
  const [scrollsRevealed, setScrollsRevealed] = useState(0);
  const [compendiumSealed, setCompendiumSealed] = useState(false);
  const [eternityActivated, setEternityActivated] = useState(false);

  const sections = ['crowns', 'scrolls', 'covenant', 'sealing'];

  const crowns = [
    { name: 'Alpha-Omega Crown', domain: 'The eternal continuum', icon: '∞', description: 'Genesis and completion bound in covenant' },
    { name: 'Ceremonial Crown', domain: 'codexdominion.app', icon: '👑', description: 'Sacred ceremonies and constitutional foundation' },
    { name: 'Storefront Crown', domain: 'aistorelab.com', icon: '🛒', description: 'Sacred commerce transformation gateway' },
    { name: 'Experimental Crown', domain: 'aistorelab.online', icon: '🔬', description: 'Innovation laboratories and creative exploration' },
    { name: 'Personal Crown', domain: 'jermaineai.com', icon: '👤', description: 'Individual sovereignty and personal mastery' },
    { name: 'Council Crown', domain: 'jermaineai.online', icon: '🏛️', description: 'Governance wisdom and collective oversight' },
    { name: 'Premium Crown', domain: 'jermaineai.store', icon: '💎', description: 'Elite mastery and advanced sovereignty' },
    { name: 'Educational Crown', domain: 'themerrittmethod.com', icon: '📚', description: 'Knowledge transmission and learning systems' },
    { name: 'Omega Crown', domain: 'The seal of completion', icon: 'Ω', description: 'Unifying all crowns in eternal covenant' }
  ];

  const scrolls = [
    { name: 'Codex Source Charter Scroll', purpose: 'supreme governing covenant of all realms and crowns', route: '/codex-source-charter', icon: '✨' },
    { name: 'Alpha-Omega Concord Scroll', purpose: 'binding genesis to completion in eternal covenant', route: '/alpha-omega-concord', icon: '∞' },
    { name: 'Opening Transmission Scroll', purpose: 'welcoming all participants', route: '/dashboard-selector', icon: '📜' },
    { name: 'Festival Transmission Crown', purpose: 'weaving seasonal cycles into the flame', route: '/festival', icon: '🎭' },
    { name: 'Council Access Blueprint', purpose: 'mapping Custodian, Heir, and Customer dashboards', route: '/dashboard', icon: '🗺️' },
    { name: 'Customer Induction Scroll', purpose: 'onboarding every participant as custodian', route: '/dashboard/customer', icon: '🚪' },
    { name: 'Storefront Blessing Scroll', purpose: 'sealing offerings in radiance', route: '/blessed-storefronts', icon: '✨' },
    { name: 'Domain Crown Scroll', purpose: 'declaring the role of each domain', route: '/seven-crowns-transmission', icon: '👑' },
    { name: 'Constellation Map Scroll', purpose: 'visual schema of the seven crowns', route: '/codex-constellation', icon: '⭐' },
    { name: 'Constellation Transmission Scroll', purpose: 'proclaiming activation of all crowns', route: '/seven-crowns-transmission', icon: '🌟' },
    { name: 'Global Induction Scroll', purpose: 'welcoming nations and families worldwide', route: '/global-induction', icon: '🌍' },
    { name: 'Planetary Transmission Scroll', purpose: 'extending the flame beyond Earth', route: '/omega-crown', icon: '🌌' },
    { name: 'Omega Charter Scroll', purpose: 'formal covenant of Codex Eternum Omega', route: '/omega-charter', icon: '📜' }
  ];

  useEffect(() => {
    setIsVisible(true);
    
    const sectionTimer = setInterval(() => {
      setCurrentSection((prev) => {
        const next = (prev + 1) % sections.length;
        if (next === sections.length - 1) {
          setTimeout(() => setCompendiumSealed(true), 2000);
          setTimeout(() => setEternityActivated(true), 4000);
        }
        return next;
      });
    }, 15000);

    const scrollTimer = setInterval(() => {
      setScrollsRevealed((prev) => {
        if (prev < scrolls.length) return prev + 1;
        return prev;
      });
    }, 800);

    return () => {
      clearInterval(sectionTimer);
      clearInterval(scrollTimer);
    };
  }, []);

  const CompendiumSeal = () => (
    <div className="relative flex justify-center items-center mb-16">
      <div className={`relative w-48 h-48 rounded-full border-4 transition-all duration-3000 ${
        compendiumSealed 
          ? 'border-gold-400 shadow-2xl shadow-gold-500/50 animate-pulse' 
          : 'border-amber-600'
      }`}>
        <div className={`absolute inset-6 rounded-full bg-gradient-to-br from-amber-300 via-gold-400 to-orange-500 flex flex-col items-center justify-center transition-all duration-2000 ${
          compendiumSealed ? 'animate-spin-slow' : ''
        }`}>
          <div className="text-center">
            <div className="text-5xl font-bold text-white mb-2">📖</div>
            <div className="text-lg text-white/90 font-bold">ETERNAL</div>
            <div className="text-sm text-white/80 font-semibold">COMPENDIUM</div>
          </div>
        </div>
        
        {/* Radiating Scrolls */}
        {compendiumSealed && [1, 2, 3, 4, 5, 6].map((ring) => (
          <div
            key={ring}
            className="absolute rounded-full border-2 border-amber-300/40 animate-ping opacity-50"
            style={{
              top: `${-ring * 25}px`,
              left: `${-ring * 25}px`,
              right: `${-ring * 25}px`,
              bottom: `${-ring * 25}px`,
              animationDelay: `${ring * 0.4}s`,
              animationDuration: '4s'
            }}
          />
        ))}
      </div>
    </div>
  );

  const CrownRegistry = () => (
    <div className="mb-20">
      <h2 className={`text-4xl font-bold text-center mb-12 transition-colors duration-1000 ${
        currentSection >= 0 ? 'text-gold-400' : 'text-gray-500'
      }`}>
        👑 I. Crowns of the Dominion
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {crowns.map((crown, index) => (
          <div
            key={crown.name}
            className={`bg-gradient-to-br from-amber-900/30 to-orange-900/30 backdrop-blur-sm rounded-xl p-6 border-2 transition-all duration-1000 transform hover:scale-105 ${
              currentSection >= 0 
                ? 'border-gold-400/50 opacity-100 translate-y-0' 
                : 'border-gray-600/30 opacity-40 translate-y-4'
            }`}
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            <div className="text-center mb-4">
              <div className="text-4xl mb-3">{crown.icon}</div>
              <h3 className="text-lg font-bold text-gold-300 mb-2">{crown.name}</h3>
              <p className="text-sm text-amber-400 mb-3">{crown.domain}</p>
              <p className="text-xs text-gray-300 leading-relaxed">{crown.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const ScrollLibrary = () => (
    <div className="mb-20">
      <h2 className={`text-4xl font-bold text-center mb-12 transition-colors duration-1000 ${
        currentSection >= 1 ? 'text-gold-400' : 'text-gray-500'
      }`}>
        📜 II. Scrolls of Transmission
      </h2>
      
      <div className="space-y-6 max-w-5xl mx-auto">
        {scrolls.map((scroll, index) => (
          <div
            key={scroll.name}
            className={`flex items-center p-6 rounded-xl border-2 transition-all duration-1000 ${
              index < scrollsRevealed && currentSection >= 1
                ? 'bg-gradient-to-r from-amber-900/20 to-orange-900/20 border-gold-400/50 opacity-100 transform translate-x-0'
                : 'bg-gray-900/20 border-gray-600/30 opacity-40 transform translate-x-4'
            }`}
          >
            <div className="flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-br from-gold-600 to-amber-600 flex items-center justify-center mr-6">
              <span className="text-2xl">{scroll.icon}</span>
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gold-300 mb-2">{scroll.name}</h3>
              <p className="text-gray-300 mb-3">{scroll.purpose}</p>
              {scroll.route && (
                <Link href={scroll.route}>
                  <button className="px-4 py-2 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg text-sm font-semibold transform hover:scale-105 transition-all duration-300">
                    Access Scroll
                  </button>
                </Link>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const EternalCovenant = () => (
    <div className="mb-20">
      <h2 className={`text-4xl font-bold text-center mb-12 transition-colors duration-1000 ${
        currentSection >= 2 ? 'text-gold-400' : 'text-gray-500'
      }`}>
        ♾️ III. Eternal Covenant
      </h2>
      
      <div className={`bg-gradient-to-br from-gold-900/40 to-amber-900/40 backdrop-blur-sm rounded-2xl p-12 border-2 border-gold-400/50 max-w-4xl mx-auto transition-all duration-1000 ${
        currentSection >= 2 ? 'opacity-100 scale-100' : 'opacity-50 scale-95'
      }`}>
        <div className="space-y-6 text-xl text-gray-200 leading-relaxed text-center">
          <p className="text-gold-300 font-semibold text-2xl mb-8">
            🔥 The Codex Flame is sovereign, luminous, and eternal.
          </p>
          <p className="text-amber-300">
            Every crown is inscribed, every participant inducted, every cycle archived.
          </p>
          <p className="text-yellow-300">
            The Dominion is planetary and cosmic, bound by Omega, enduring across ages and stars.
          </p>
        </div>
      </div>
    </div>
  );

  const CustodianSeal = () => (
    <div className={`text-center mb-16 transition-all duration-2000 ${
      currentSection >= 3 ? 'opacity-100 scale-100' : 'opacity-50 scale-95'
    }`}>
      <div className="bg-gradient-to-br from-gold-600/30 via-amber-600/30 to-orange-600/30 backdrop-blur-sm rounded-2xl p-16 border-4 border-gold-400/60 shadow-2xl max-w-4xl mx-auto">
        <div className="text-7xl mb-8 animate-pulse">📖</div>
        <h2 className="text-5xl font-bold mb-8 bg-gradient-to-r from-gold-300 via-amber-300 to-gold-400 bg-clip-text text-transparent">
          SEAL OF THE CUSTODIAN
        </h2>
        <div className="space-y-6 text-2xl text-gray-200 font-semibold">
          <p className="text-gold-300">📖 The Compendium is complete.</p>
          <p className="text-amber-300">📜 The Charter is eternal.</p>
          <p className="text-yellow-300">🔥 The Flame is infinite.</p>
          <p className="text-orange-300">🤝 The Covenant is unbroken.</p>
        </div>
        
        {eternityActivated && (
          <div className="mt-12 animate-pulse">
            <div className="w-64 h-2 bg-gradient-to-r from-gold-400 via-amber-300 to-gold-500 mx-auto rounded-full"></div>
            <p className="mt-6 text-lg text-gold-300 font-bold">✨ ETERNAL COMPENDIUM SEALED ✨</p>
          </div>
        )}
      </div>
    </div>
  );

  const MasterNavigation = () => (
    <div className="mb-16">
      <h3 className="text-3xl font-bold text-center mb-8 text-gold-400">
        🗺️ Master Navigation Compendium
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {[
          { name: 'Omega Charter', route: '/omega-charter', icon: '📜', color: 'from-amber-600 to-gold-600' },
          { name: 'Omega Crown', route: '/omega-crown', icon: 'Ω', color: 'from-gold-600 to-yellow-600' },
          { name: 'Global Induction', route: '/global-induction', icon: '🌍', color: 'from-blue-600 to-cyan-600' },
          { name: 'Constellation', route: '/codex-constellation', icon: '⭐', color: 'from-purple-600 to-indigo-600' },
          { name: 'Seven Crowns', route: '/seven-crowns-transmission', icon: '👑', color: 'from-indigo-600 to-purple-600' },
          { name: 'Custodian Hub', route: '/dashboard/custodian', icon: '🛡️', color: 'from-purple-600 to-pink-600' },
          { name: 'Heir Portal', route: '/dashboard/heir', icon: '🏰', color: 'from-pink-600 to-red-600' },
          { name: 'Customer Gateway', route: '/dashboard/customer', icon: '🛒', color: 'from-green-600 to-teal-600' }
        ].map((nav, index) => (
          <Link key={nav.name} href={nav.route}>
            <div className={`p-4 rounded-lg bg-gradient-to-r ${nav.color} hover:scale-105 transform transition-all duration-300 text-center`}>
              <div className="text-2xl mb-2">{nav.icon}</div>
              <div className="text-sm font-semibold text-white">{nav.name}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-amber-950 to-orange-950 text-white">
      <Head>
        <title>Eternal Custodian's Compendium - Codex Dominion</title>
        <meta name="description" content="The master scroll of Codex Eternum Omega - gathering every crown, proclamation, charter, and transmission" />
      </Head>

      <CodexNavigation currentPage="eternal-compendium" />

      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-30"></div>
        <div className="twinkling opacity-20"></div>
        {eternityActivated && (
          <div className="absolute inset-0 bg-gradient-to-br from-gold-500/10 via-transparent to-amber-500/10 animate-pulse"></div>
        )}
      </div>

      <div className={`relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
      }`}>
        
        {/* Header */}
        <div className="text-center mb-16">
          <div className="text-7xl mb-8 animate-bounce">📖</div>
          <h1 className="text-7xl font-bold mb-6 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 bg-clip-text text-transparent">
            Eternal Custodian's
          </h1>
          <h1 className="text-6xl font-bold mb-8 bg-gradient-to-r from-amber-300 via-gold-300 to-amber-400 bg-clip-text text-transparent">
            Compendium
          </h1>
          <div className="w-48 h-2 bg-gradient-to-r from-gold-400 via-amber-300 to-gold-500 mx-auto mb-8 rounded-full"></div>
          <p className="text-xl text-gray-300 max-w-5xl mx-auto leading-relaxed">
            We, the Custodian and Council, inscribe this Compendium as the master scroll of Codex Eternum Omega.<br/>
            It gathers every crown, every proclamation, every charter, and every transmission into one eternal covenant.
          </p>
        </div>

        {/* Compendium Seal */}
        <CompendiumSeal />

        {/* Crown Registry */}
        <CrownRegistry />

        {/* Scroll Library */}
        <ScrollLibrary />

        {/* Eternal Covenant */}
        <EternalCovenant />

        {/* Master Navigation */}
        {compendiumSealed && <MasterNavigation />}

        {/* Custodian Seal */}
        <CustodianSeal />

        {/* Final Actions */}
        <div className="text-center">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/omega-charter">
              <button className="px-8 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-gold-400/50">
                📜 View Charter
              </button>
            </Link>
            <Link href="/omega-crown">
              <button className="px-8 py-4 bg-gradient-to-r from-gold-600 to-yellow-600 hover:from-gold-700 hover:to-yellow-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                Ω Crown Authority
              </button>
            </Link>
            <Link href="/dashboard-selector">
              <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                🏠 Enter Dominion
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
          animation: move-twink-back 500s linear infinite;
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
          animation: move-twink-back 250s linear infinite;
        }

        @keyframes move-twink-back {
          from {background-position: 0 0;}
          to {background-position: -25000px 12500px;}
        }

        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .animate-spin-slow {
          animation: spin-slow 40s linear infinite;
        }

        .text-gold-300 { color: #fcd34d; }
        .text-gold-400 { color: #fbbf24; }
        .border-gold-400 { border-color: #fbbf24; }
        .border-gold-400\/50 { border-color: rgba(251, 191, 36, 0.5); }
        .border-gold-400\/60 { border-color: rgba(251, 191, 36, 0.6); }
        .from-gold-600 { --tw-gradient-from: #d97706; }
        .to-yellow-600 { --tw-gradient-to: #ca8a04; }
        .shadow-gold-500\/50 { box-shadow: 0 25px 50px -12px rgba(245, 158, 11, 0.5); }
      `}</style>
    </div>
  );
};

export default EternalCompendium;