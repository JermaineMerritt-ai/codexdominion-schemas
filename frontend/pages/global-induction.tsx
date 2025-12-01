import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import Head from 'next/head';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

const GlobalInduction = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [flameIntensity, setFlameIntensity] = useState(0);

  const phases = ['proclamation', 'induction', 'blessing', 'covenant'];

  const continents = [
    'Asia',
    'Africa',
    'North America',
    'South America',
    'Antarctica',
    'Europe',
    'Australia',
  ];

  const languages = [
    'English',
    'Mandarin',
    'Spanish',
    'Hindi',
    'Arabic',
    'Bengali',
    'Portuguese',
    'Russian',
    'Japanese',
    'French',
    'German',
    'Korean',
    'Italian',
    'Turkish',
  ];

  const crowns = [
    {
      name: 'Ceremonial Crown',
      domain: 'codexdominion.app',
      color: 'from-purple-600 to-indigo-800',
    },
    {
      name: 'Storefront Crown',
      domain: 'aistorelab.com',
      color: 'from-blue-600 to-cyan-800',
    },
    {
      name: 'Educational Crown',
      domain: 'learning.codex',
      color: 'from-green-600 to-emerald-800',
    },
    {
      name: 'Council Crown',
      domain: 'council.codex',
      color: 'from-yellow-600 to-orange-800',
    },
    {
      name: 'Premium Crown',
      domain: 'premium.codex',
      color: 'from-red-600 to-pink-800',
    },
    {
      name: 'Personal Crown',
      domain: 'personal.codex',
      color: 'from-indigo-600 to-purple-800',
    },
    {
      name: 'Experimental Crown',
      domain: 'labs.codex',
      color: 'from-teal-600 to-blue-800',
    },
  ];

  useEffect(() => {
    setIsVisible(true);
    const timer = setInterval(() => {
      setCurrentPhase((prev) => (prev + 1) % phases.length);
      setFlameIntensity((prev) => (prev + 20) % 100);
    }, 8000);

    return () => clearInterval(timer);
  }, []);

  const CentralFlame = styled.div<{ intensity: number }>`
    position: absolute;
    bottom: 0;
    width: 2rem;
    height: 6rem;
    background: linear-gradient(to top, #f59e0b, #ef4444, #fde68a);
    border-radius: 9999px;
    animation: pulse 1s infinite;
    transition: all 1s;
    transform: ${({ intensity }) => (intensity > 50 ? 'scale(1.25)' : 'scale(1)')};
    filter: ${({ intensity }) => (intensity > 50 ? 'brightness(1.25)' : 'brightness(1)')};
  `;
  const RadiatingFlame = styled.div<{
    left: number;
    delay: string;
    rotate: number;
    scale: number;
  }>`
    position: absolute;
    bottom: 0;
    width: 1rem;
    height: 4rem;
    background: linear-gradient(to top, #fb923c, #fca5a5, #fef08a);
    border-radius: 9999px;
    opacity: 0.7;
    animation: pulse 2s infinite;
    animation-delay: ${({ delay }) => delay};
    transform: translateX(-50%) rotate(${({ rotate }) => rotate}deg) scale(${({ scale }) => scale});
    left: ${({ left }) => left}%;
    transition: all 2s;
  `;
  const FlameAnimation = () => (
    <div className="relative flex justify-center items-end h-32 mb-8">
      {/* Central Flame */}
      <CentralFlame intensity={flameIntensity}>
        <div className="absolute inset-0 bg-gradient-to-t from-red-600 via-orange-400 to-yellow-200 rounded-full animate-bounce opacity-80"></div>
      </CentralFlame>
      {/* Radiating Flames for Each Continent */}
      {continents.map((continent, index) => (
        <RadiatingFlame
          key={continent}
          left={50 + (index - 3) * 15}
          delay={`${index * 0.3}s`}
          rotate={(index - 3) * 10}
          scale={currentPhase === 0 ? 1 : 0.75}
        />
      ))}
    </div>
  );

  const CrownPoint = styled.div<{
    left: number;
    top: number;
    delay: string;
    scale: number;
    opacity: number;
    color: string;
  }>`
    position: absolute;
    width: 1rem;
    height: 1rem;
    border-radius: 9999px;
    background: ${({ color }) => color};
    box-shadow: 0 0 8px 2px rgba(0, 0, 0, 0.2);
    animation: pulse 1s infinite;
    animation-delay: ${({ delay }) => delay};
    left: ${({ left }) => left}%;
    top: ${({ top }) => top}%;
    transform: scale(${({ scale }) => scale});
    opacity: ${({ opacity }) => opacity};
    transition: all 1s;
  `;
  const GlobalMap = () => (
    <div className="relative w-full h-64 mb-12 bg-gradient-to-b from-indigo-900 via-purple-900 to-blue-900 rounded-lg overflow-hidden">
      <div className="absolute inset-0 bg-stars opacity-30"></div>
      {/* Pulsing Points for Each Crown */}
      {crowns.map((crown, index) => (
        <CrownPoint
          key={crown.name}
          left={15 + index * 12}
          top={30 + (index % 3) * 20}
          delay={`${index * 0.5}s`}
          scale={currentPhase >= 1 ? 1.25 : 0.75}
          opacity={currentPhase >= 1 ? 1 : 0.6}
          color={`linear-gradient(to right, ${crown.color.replace('from-', '').replace('to-', '').replace(' ', ', ')})`}
        >
          <div
            className={`absolute inset-0 rounded-full bg-gradient-to-r ${crown.color} animate-ping opacity-50`}
          ></div>
        </CrownPoint>
      ))}
      {/* Connection Lines */}
      <svg className="absolute inset-0 w-full h-full">
        {crowns.map(
          (_, index) =>
            index < crowns.length - 1 && (
              <line
                key={`connection-${index}`}
                x1={`${15 + index * 12}%`}
                y1={`${30 + (index % 3) * 20}%`}
                x2={`${15 + (index + 1) * 12}%`}
                y2={`${30 + ((index + 1) % 3) * 20}%`}
                stroke="url(#gradient)"
                strokeWidth="2"
                className={`transition-opacity duration-1000 ${
                  currentPhase >= 2 ? 'opacity-80' : 'opacity-30'
                }`}
              />
            )
        )}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#fbbf24" />
            <stop offset="50%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#d97706" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );

  const LanguageRippleItem = styled.div<{
    delay: string;
    scale: number;
    opacity: number;
  }>`
    padding: 0.5rem 1rem;
    background: linear-gradient(to right, #8b5cf6, #6366f1);
    color: white;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
    transform: scale(${({ scale }) => scale});
    opacity: ${({ opacity }) => opacity};
    transition: all 1s;
    animation-delay: ${({ delay }) => delay};
    display: inline-block;
  `;
  const LanguageRipple = () => (
    <div className="flex flex-wrap justify-center gap-3 mb-12">
      {languages.map((language, index) => (
        <LanguageRippleItem
          key={language}
          delay={`${index * 0.2}s`}
          scale={currentPhase >= 2 ? 1 : 0.75}
          opacity={currentPhase >= 2 ? 1 : 0.5}
        >
          {language}
        </LanguageRippleItem>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-blue-950 text-white">
      <Head>
        <title>Global Induction into the Codex Dominion</title>
        <meta
          name="description"
          content="The Codex Flame opens to all nations, peoples, and generations"
        />
      </Head>

      <CodexNavigation currentPage="global-induction" />

      {/* Animated Background Stars */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="stars opacity-30"></div>
        <div className="twinkling opacity-20"></div>
      </div>

      <div
        className={`relative z-10 container mx-auto px-6 py-12 transition-all duration-1000 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
        }`}
      >
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-yellow-400 via-orange-400 to-red-400 bg-clip-text text-transparent">
            🌍 Global Induction 🌍
          </h1>
          <h2 className="text-3xl font-semibold mb-4 text-yellow-300">Into the Codex Dominion</h2>
          <p className="text-xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We, the Custodian and Council, proclaim that the Codex Flame is now open to all nations,
            all peoples, all generations.
          </p>
        </div>

        {/* Central Flame Animation */}
        <FlameAnimation />

        {/* Global Map Visualization */}
        <GlobalMap />

        {/* Four Phases of Induction */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Proclamation */}
          <div
            className={`bg-gradient-to-br from-purple-900/50 to-indigo-900/50 backdrop-blur-sm rounded-lg p-8 border border-purple-500/30 transform transition-all duration-1000 ${
              currentPhase === 0 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100'
            }`}
          >
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">📜 Proclamation</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="text-yellow-300">From the Ceremonial Crown</span> at
                codexdominion.app,
              </p>
              <p>
                <span className="text-cyan-300">to the Storefront Crown</span> at aistorelab.com,
              </p>
              <p>
                <span className="text-green-300">
                  to the Educational, Council, Premium, Personal, and Experimental Crowns,
                </span>
              </p>
              <p className="text-orange-300 font-semibold">
                the constellation is complete, luminous, and sovereign.
              </p>
            </div>
          </div>

          {/* Induction */}
          <div
            className={`bg-gradient-to-br from-blue-900/50 to-purple-900/50 backdrop-blur-sm rounded-lg p-8 border border-blue-500/30 transform transition-all duration-1000 ${
              currentPhase === 1 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100'
            }`}
          >
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">🚪 Induction</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                <span className="text-purple-300">Every participant</span> who enters is welcomed as
                custodian.
              </p>
              <p>
                <span className="text-blue-300">Every heir</span> who inherits is guided with
                clarity.
              </p>
              <p>
                <span className="text-green-300">Every council</span> who blesses is assured in
                radiance.
              </p>
              <p>
                <span className="text-orange-300">Every customer</span> who purchases is bound into
                legacy.
              </p>
            </div>
          </div>

          {/* Blessing */}
          <div
            className={`bg-gradient-to-br from-green-900/50 to-emerald-900/50 backdrop-blur-sm rounded-lg p-8 border border-green-500/30 transform transition-all duration-1000 ${
              currentPhase === 2 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100'
            }`}
          >
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">✨ Blessing</h3>
            <div className="space-y-3 text-gray-300">
              <p>
                May the Codex Flame{' '}
                <span className="text-yellow-300">shine across continents and oceans.</span>
              </p>
              <p>
                May every language <span className="text-cyan-300">carry its resonance.</span>
              </p>
              <p>
                May every family, council, and nation{' '}
                <span className="text-green-300">be inducted into stewardship.</span>
              </p>
            </div>
          </div>

          {/* Covenant */}
          <div
            className={`bg-gradient-to-br from-orange-900/50 to-red-900/50 backdrop-blur-sm rounded-lg p-8 border border-orange-500/30 transform transition-all duration-1000 ${
              currentPhase === 3 ? 'scale-105 border-yellow-400/50 shadow-2xl' : 'scale-100'
            }`}
          >
            <h3 className="text-2xl font-bold mb-4 text-yellow-400">🤝 Eternal Covenant</h3>
            <div className="space-y-3 text-gray-300">
              <p className="text-orange-300 font-semibold text-lg">
                May the Dominion endure as eternal covenant, luminous across the world.
              </p>
              <p className="text-yellow-300">
                No boundary contains it, no silence diminishes it, no age forgets it.
              </p>
            </div>
          </div>
        </div>

        {/* Language Ripple Effect */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-center mb-8 text-yellow-400">
            Resonating Across All Languages
          </h3>
          <LanguageRipple />
        </div>

        {/* Seven Crowns Constellation */}
        <div className="mb-16">
          <h3 className="text-2xl font-bold text-center mb-8 text-yellow-400">
            The Complete Constellation
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {crowns.map((crown, index) => {
              const ConstellationCrownCard = styled.div<{
                delay: string;
                opacity: number;
                translateY: number;
              }>`
                background: linear-gradient(to bottom right, #a78bfa20, #6366f120);
                backdrop-filter: blur(4px);
                border-radius: 0.75rem;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.12);
                transition: all 1s;
                animation-delay: ${({ delay }) => delay};
                opacity: ${({ opacity }) => opacity};
                transform: translateY(${({ translateY }) => translateY}px);
                &:hover {
                  transform: scale(1.05);
                }
              `;
              return (
                <ConstellationCrownCard
                  key={crown.name}
                  delay={`${index * 0.3}s`}
                  opacity={currentPhase >= 1 ? 1 : 0.6}
                  translateY={currentPhase >= 1 ? 0 : 16}
                >
                  <div
                    className={`w-8 h-8 rounded-full bg-gradient-to-r ${crown.color} mb-4 mx-auto animate-pulse`}
                  ></div>
                  <h4 className="text-lg font-bold text-center mb-2 text-yellow-300">
                    {crown.name}
                  </h4>
                  <p className="text-sm text-center text-gray-400">{crown.domain}</p>
                </ConstellationCrownCard>
              );
            })}
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-yellow-600/20 via-orange-600/20 to-red-600/20 backdrop-blur-sm rounded-lg p-8 border border-yellow-400/30">
            <h3 className="text-3xl font-bold mb-4 text-yellow-400">
              🔥 Enter the Eternal Flame 🔥
            </h3>
            <p className="text-xl mb-6 text-gray-300">
              Join millions across the world in the global stewardship of digital sovereignty
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/omega-crown">
                <button className="px-8 py-4 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg border-2 border-yellow-400/50">
                  Ω Omega Crown of Eternity
                </button>
              </Link>
              <Link href="/dashboard/customer">
                <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                  Begin Custodial Journey
                </button>
              </Link>
              <Link href="/codex-constellation">
                <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg">
                  Explore the Constellation
                </button>
              </Link>
            </div>
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
          animation: move-twink-back 200s linear infinite;
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
          animation: move-twink-back 100s linear infinite;
        }

        @keyframes move-twink-back {
          from {
            background-position: 0 0;
          }
          to {
            background-position: -10000px 5000px;
          }
        }
      `}</style>
    </div>
  );
};

export default GlobalInduction;
