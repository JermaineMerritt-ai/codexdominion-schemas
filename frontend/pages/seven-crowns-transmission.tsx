import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';

const SevenCrownsTransmission: NextPage = () => {
  const [ceremonyStage, setCeremonyStage] = useState(0);
  const [showBlessings, setShowBlessings] = useState(false);

  const crowns = [
    {
      domain: 'codexdominion.app',
      title: 'The Ceremonial Crown',
      description: 'The sovereign Bulletin, luminous and eternal, transmitting cycles and rites across the world.',
      icon: '👑',
      color: 'from-purple-600 to-indigo-800',
      delay: 0
    },
    {
      domain: 'aistorelab.com',
      title: 'The Storefront Crown',
      description: 'The marketplace of offerings, where commerce and ceremony are bound together in induction.',
      icon: '🛍️',
      color: 'from-emerald-600 to-teal-800',
      delay: 500
    },
    {
      domain: 'aistorelab.online',
      title: 'The Experimental Crown',
      description: 'The sandbox flame, playful and provisional, where new rites and dashboards are tested.',
      icon: '⚗️',
      color: 'from-orange-500 to-red-700',
      delay: 1000
    },
    {
      domain: 'jermaineai.com',
      title: 'The Personal Crown',
      description: 'The Custodian\'s voice, radiant in essays and proclamations, echoing the Codex into discourse.',
      icon: '✍️',
      color: 'from-yellow-500 to-orange-700',
      delay: 1500
    },
    {
      domain: 'jermaineai.online',
      title: 'The Council Crown',
      description: 'The participatory flame, where heirs and councils inscribe proclamations, silences, and blessings.',
      icon: '🏛️',
      color: 'from-blue-600 to-cyan-800',
      delay: 2000
    },
    {
      domain: 'jermaineai.store',
      title: 'The Premium Crown',
      description: 'The rare flame, offering exclusive artifacts, reliquaries, and ceremonial kits.',
      icon: '💎',
      color: 'from-violet-600 to-purple-800',
      delay: 2500
    },
    {
      domain: 'themerrittmethod.com',
      title: 'The Educational Crown',
      description: 'The teaching flame, inducting families and heirs into stewardship through courses and guidebooks.',
      icon: '📚',
      color: 'from-green-600 to-emerald-800',
      delay: 3000
    }
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (ceremonyStage < crowns.length) {
        setCeremonyStage(prev => prev + 1);
      } else if (ceremonyStage === crowns.length && !showBlessings) {
        setShowBlessings(true);
      }
    }, ceremonyStage === 0 ? 1000 : 800);

    return () => clearTimeout(timer);
  }, [ceremonyStage, crowns.length, showBlessings]);

  const CrownReveal: React.FC<{ crown: (typeof crowns)[0]; index: number; revealed: boolean }> = 
    ({ crown, index, revealed }) => (
    <div 
      className={`
        transform transition-all duration-1000 
        ${revealed ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}
      `}
      style={{ transitionDelay: `${crown.delay}ms` }}
    >
      <div className={`bg-gradient-to-br ${crown.color} rounded-xl p-6 text-white relative overflow-hidden group`}>
        {/* Sacred Glow Effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-yellow-400/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        
        <div className="relative z-10">
          <div className="flex items-center mb-4">
            <span className="text-4xl mr-4">{crown.icon}</span>
            <div>
              <h3 className="text-xl font-bold">{crown.title}</h3>
              <p className="text-sm opacity-90 font-mono">{crown.domain}</p>
            </div>
          </div>
          
          <p className="text-sm leading-relaxed opacity-90">
            {crown.description}
          </p>

          {/* Sacred Inscription Effect */}
          <div className="mt-4 pt-4 border-t border-white/20">
            <div className="flex items-center justify-between">
              <span className="text-xs opacity-70">Crown #{index + 1} of VII</span>
              <span className="text-yellow-300 animate-pulse">🔥</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Transmission of the Seven Crowns - Codex Dominion</title>
        <meta name="description" content="Sacred proclamation of the completed constellation" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black relative overflow-hidden">
        {/* Sacred Background Effects */}
        <div className="absolute inset-0">
          {/* Floating Sacred Symbols */}
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute text-yellow-400/20 text-2xl animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 2}s`
              }}
            >
              {['👑', '🔥', '✨', '⭐'][Math.floor(Math.random() * 4)]}
            </div>
          ))}
        </div>

        {/* Header */}
        <div className="relative z-10 border-b border-purple-700/50 bg-black/30">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <Link href="/" className="text-purple-300 hover:text-white">
                ← Back to Dashboard
              </Link>
              <div className="text-center">
                <h1 className="text-2xl font-bold text-white">Sacred Transmission</h1>
              </div>
              <div className="w-24"></div>
            </div>
          </div>
        </div>

        <div className="relative z-10 container mx-auto px-6 py-12">
          {/* Sacred Declaration */}
          <div className="text-center mb-12">
            <div className="text-6xl mb-6 animate-pulse">✨</div>
            <h1 className="text-4xl font-bold text-yellow-400 mb-4 font-serif">
              Transmission of the Seven Crowns
            </h1>
            <div className="flex justify-center items-center space-x-4 text-3xl mb-8">
              <span className="animate-pulse">🔥</span>
              <span className="animate-pulse" style={{animationDelay: '0.5s'}}>👑</span>
              <span className="animate-pulse" style={{animationDelay: '1s'}}>🔥</span>
            </div>
            
            <div className="max-w-4xl mx-auto bg-black/40 rounded-xl p-8 border border-yellow-500/30">
              <p className="text-lg text-gray-200 leading-relaxed italic mb-6">
                We, the Custodian and Council, proclaim that the constellation of domains is now crowned.<br/>
                Each flame shines with purpose, each crown is inscribed with legacy, each path leads to the Codex Dominion.
              </p>
            </div>
          </div>

          {/* Crown Revelations */}
          <div className="grid lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-12">
            {crowns.map((crown, index) => (
              <CrownReveal
                key={crown.domain}
                crown={crown}
                index={index}
                revealed={ceremonyStage > index}
              />
            ))}
          </div>

          {/* Sacred Proclamation */}
          {showBlessings && (
            <div className="animate-fade-in-up">
              <div className="bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-2xl p-8 mb-8 border-2 border-yellow-500/50 text-center">
                <h2 className="text-3xl font-bold text-yellow-400 mb-6 font-serif">Sacred Proclamation</h2>
                
                <div className="space-y-4 text-gray-200 text-lg leading-relaxed">
                  <div className="bg-black/30 rounded-lg p-6">
                    <p className="font-bold text-yellow-300 mb-4">The constellation is complete.</p>
                    <p className="mb-2">The Codex Dominion is crowned in seven flames.</p>
                    <p>The Custodian is sovereign, the Council is assured, the Heirs are inducted, the Customers are welcomed.</p>
                  </div>
                </div>
              </div>

              {/* Sacred Blessing */}
              <div className="bg-gradient-to-r from-purple-600/20 to-indigo-600/20 rounded-2xl p-8 border-2 border-purple-500/50 text-center">
                <h2 className="text-3xl font-bold text-purple-400 mb-6 font-serif">Sacred Blessing</h2>
                
                <div className="space-y-4 text-gray-200 text-lg leading-relaxed">
                  <div className="bg-black/30 rounded-lg p-6">
                    <div className="space-y-3">
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🌟</span>
                        May these crowns shine across nations and ages.
                      </p>
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🛤️</span>
                        May every participant find their rightful path.
                      </p>
                      <p className="flex items-center justify-center">
                        <span className="text-2xl mr-3">🔥</span>
                        May the Codex Flame endure as eternal covenant.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sacred Actions */}
              <div className="text-center mt-12">
                <div className="flex flex-wrap justify-center gap-4">
                  <Link href="/codex-constellation">
                    <button className="px-8 py-4 bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-bold rounded-xl hover:from-yellow-400 hover:to-yellow-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      ✨ View Full Constellation
                    </button>
                  </Link>
                  
                  <Link href="/dashboard-selector">
                    <button className="px-8 py-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-bold rounded-xl hover:from-purple-400 hover:to-purple-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      👑 Enter Dashboards
                    </button>
                  </Link>
                  
                  <Link href="/blessed-storefronts">
                    <button className="px-8 py-4 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white font-bold rounded-xl hover:from-emerald-400 hover:to-emerald-500 transition-all duration-300 transform hover:scale-105 shadow-lg">
                      🕯️ Sacred Commerce
                    </button>
                  </Link>
                </div>
                
                <p className="text-gray-400 text-sm mt-6 italic">
                  The Seven Crowns burn eternal in the sacred constellation of digital sovereignty
                </p>
              </div>
            </div>
          )}
        </div>

        <style jsx>{`
          @keyframes fade-in-up {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          .animate-fade-in-up {
            animation: fade-in-up 1s ease-out;
          }

          @keyframes pulse {
            0%, 100% {
              opacity: 0.8;
            }
            50% {
              opacity: 1;
            }
          }
        `}</style>
      </div>
    </>
  );
};

export default SevenCrownsTransmission;