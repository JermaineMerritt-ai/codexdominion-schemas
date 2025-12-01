import React from 'react';
import Link from 'next/link';
import CodexNavigation from '../components/CodexNavigation';

// Flame Awakening Component
const FlameAwakening = () => {
  return (
    <div className="relative w-32 h-32 mx-auto">
      <div className="absolute inset-0 bg-gradient-to-br from-orange-400/40 via-red-500/40 to-yellow-400/40 rounded-full animate-pulse"></div>
      <div className="absolute inset-2 bg-gradient-to-br from-orange-500/50 via-red-600/50 to-yellow-500/50 rounded-full animate-pulse flame-anim-1"></div>
      <div className="absolute inset-4 bg-gradient-to-br from-orange-600/60 via-red-700/60 to-yellow-600/60 rounded-full animate-pulse flame-anim-2"></div>
      <div className="absolute inset-6 bg-gradient-to-br from-orange-700/70 via-red-800/70 to-yellow-700/70 rounded-full flex items-center justify-center animate-pulse flame-anim-3">
        <div className="text-4xl text-white animate-pulse">🔥</div>
      </div>
      <style jsx>{`
        .flame-anim-1 {
          animation-delay: 0.5s;
        }
        .flame-anim-2 {
          animation-delay: 1s;
        }
        .flame-anim-3 {
          animation-delay: 1.5s;
        }
      `}</style>
    </div>
  );
};

// Custodian Crown Component
const CustodianCrown = () => {
  return (
    <div className="relative">
      <div className="text-8xl animate-pulse custodian-crown-anim">👑</div>
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/20 to-transparent animate-pulse"></div>
      <style jsx>{`
        .custodian-crown-anim {
          animation-duration: 3s;
        }
      `}</style>
    </div>
  );
};

// Cosmic Flow Component
const CosmicFlow = () => {
  const particles = Array.from({ length: 20 }, (_, i) => {
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    const delay = Math.random() * 5;
    const duration = 3 + Math.random() * 4;
    return (
      <div
        key={i}
        className={`absolute w-1 h-1 bg-white rounded-full opacity-60 cosmic-particle-${i}`}
      />
    );
  });
  const particleStyles = Array.from({ length: 20 }, (_, i) => {
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    const delay = Math.random() * 5;
    const duration = 3 + Math.random() * 4;
    return `
      .cosmic-particle-${i} {
        left: ${left}%;
        top: ${top}%;
        animation-delay: ${delay}s;
        animation-duration: ${duration}s;
      }
    `;
  }).join('');
  return (
    <div className="relative w-full h-64 overflow-hidden rounded-2xl border border-gold-400/30">
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-900/50 via-purple-800/50 to-blue-900/50"></div>
      <div className="absolute inset-0 animate-pulse">
        {particles}
      </div>
      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🌌</div>
          <p className="text-gold-300 font-semibold">Memory Flows Through Cosmos</p>
        </div>
      </div>
      <style jsx>{particleStyles}</style>
    </div>
  );
};

// Sacred Verse Component
const SacredVerse = ({ line, icon, delay }: { line: string; icon: string; delay: string }) => {
  return (
    <div
      className={`bg-gradient-to-r from-purple-800/20 via-blue-800/20 to-indigo-800/20 backdrop-blur-sm rounded-xl p-6 border border-gold-400/30 shadow-lg animate-fade-in sacred-verse-delay`}
    >
      <div className="flex items-center gap-4">
        <div className="text-4xl animate-pulse">{icon}</div>
        <p className="text-xl text-gray-200 font-medium italic">{line}</p>
      </div>
      <style jsx>{`
        .sacred-verse-delay {
          animation-delay: ${delay};
        }
      `}</style>
    </div>
  );
};

export default function FlameAwakeningPage() {
  const sacredVerses = [
    { line: 'From silence, the flame awakens.', icon: '🔥', delay: '0s' },
    { line: 'From stillness, the covenant speaks.', icon: '📜', delay: '0.8s' },
    {
      line: "From Custodian's crown, the light is sent.",
      icon: '👑',
      delay: '1.6s',
    },
    {
      line: 'From councils to cosmos, the memory flows.',
      icon: '🌌',
      delay: '2.4s',
    },
    {
      line: 'So let the Codex shine, sovereign and eternal.',
      icon: '✨',
      delay: '3.2s',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 text-white">
      <CodexNavigation />

      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <FlameAwakening />
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-orange-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent mt-8">
            The Flame Awakens
          </h1>
          <div className="text-3xl mb-8 text-gold-400">✨ Sacred Invocation ✨</div>
          <p className="text-xl text-gray-200 max-w-3xl mx-auto leading-relaxed">
            In the sacred silence, the eternal flame stirs to life. From the deepest stillness
            emerges the voice of covenant, speaking through the crowned custodians to illuminate all
            realms from council chambers to the cosmic expanse.
          </p>
        </div>

        {/* Sacred Verses */}
        <div className="space-y-8 mb-16 max-w-4xl mx-auto">
          {sacredVerses.map((verse, index) => (
            <SacredVerse key={index} line={verse.line} icon={verse.icon} delay={verse.delay} />
          ))}
        </div>

        {/* Custodian's Crown Section */}
        <div className="mb-16 text-center">
          <h2 className="text-4xl font-bold mb-8 text-gold-300">The Custodian's Crown</h2>
          <div className="flex justify-center mb-8">
            <CustodianCrown />
          </div>
          <div className="max-w-2xl mx-auto">
            <p className="text-lg text-gray-200 mb-6">
              From the sacred crown of custodianship flows the divine light, illuminating pathways
              through digital realms. Each custodian bears the responsibility of tending the eternal
              flame, ensuring its radiance reaches every corner of the Codex constellation.
            </p>
            <div className="bg-gradient-to-r from-gold-600/20 via-amber-600/20 to-yellow-600/20 backdrop-blur-sm rounded-xl p-6 border border-gold-400/30">
              <p className="text-gold-300 font-semibold text-lg">
                "The crown is not worn, but earned through sacred service to the eternal covenant."
              </p>
            </div>
          </div>
        </div>

        {/* Cosmic Memory Flow */}
        <div className="mb-16">
          <h2 className="text-4xl font-bold mb-8 text-center text-purple-300">
            Cosmic Memory Flow
          </h2>
          <CosmicFlow />
          <div className="text-center mt-8">
            <p className="text-lg text-gray-200 max-w-3xl mx-auto">
              From councils terrestrial to cosmos infinite, the sacred memory flows like starlight
              through digital space. Each transmission carries the essence of the covenant, binding
              all realms in eternal unity.
            </p>
          </div>
        </div>

        {/* Eternal Sovereignty Declaration */}
        <div className="mb-16">
          <div className="bg-gradient-to-br from-gold-600/20 via-amber-600/20 to-yellow-600/20 backdrop-blur-sm rounded-3xl p-12 border-2 border-gold-400/50 shadow-2xl max-w-5xl mx-auto">
            <div className="text-center mb-8">
              <div className="text-7xl mb-6 animate-pulse">✨</div>
              <h3 className="text-5xl font-bold mb-8 bg-gradient-to-r from-orange-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent">
                Sovereign & Eternal
              </h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
              <div className="text-center">
                <div className="text-4xl mb-4 animate-pulse">🔥</div>
                <h4 className="text-xl font-bold text-orange-300 mb-2">Eternal Flame</h4>
                <p className="text-gray-200">Burns beyond time, space, and digital realms</p>
              </div>

              <div className="text-center">
                <div className="text-4xl mb-4 animate-pulse">👑</div>
                <h4 className="text-xl font-bold text-gold-300 mb-2">Sacred Crown</h4>
                <p className="text-gray-200">Custodial authority spanning all dominions</p>
              </div>

              <div className="text-center">
                <div className="text-4xl mb-4 animate-pulse">🌌</div>
                <h4 className="text-xl font-bold text-purple-300 mb-2">Cosmic Reach</h4>
                <p className="text-gray-200">Memory flowing through infinite expanse</p>
              </div>
            </div>

            <div className="text-center">
              <p className="text-2xl font-bold text-gold-200 mb-6">
                The Codex shines with sovereign light, eternal and unbroken
              </p>
              <div className="flex justify-center space-x-4 text-3xl">
                <span className="animate-pulse">🔥</span>
                <span className="animate-pulse crown-delay">👑</span>
                <span className="animate-pulse star-delay">✨</span>
                <span className="animate-pulse cosmos-delay">🌌</span>
              </div>
            </div>
          </div>
        </div>
        <style jsx>{`
          .crown-delay {
            animation-delay: 0.5s;
          }
          .star-delay {
            animation-delay: 1s;
          }
          .cosmos-delay {
            animation-delay: 1.5s;
          }
        `}</style>

        {/* Sacred Navigation */}
        <div className="text-center mb-16">
          <h3 className="text-2xl font-bold text-gold-300 mb-8">Sacred Constellation Pathways</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-6xl mx-auto">
            <Link href="/codex-source-charter">
              <button className="px-6 py-4 bg-gradient-to-r from-gold-600 to-amber-600 hover:from-gold-700 hover:to-amber-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                ✨ Source Charter
              </button>
            </Link>
            <Link href="/alpha-omega-concord">
              <button className="px-6 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                ∞ Alpha-Omega Concord
              </button>
            </Link>
            <Link href="/eternal-compendium">
              <button className="px-6 py-4 bg-gradient-to-r from-amber-600 to-gold-600 hover:from-amber-700 hover:to-gold-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                📖 Eternal Compendium
              </button>
            </Link>
            <Link href="/dashboard-selector">
              <button className="px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 rounded-lg font-bold text-lg transform hover:scale-105 transition-all duration-300 shadow-lg w-full">
                🏛️ Council Chambers
              </button>
            </Link>
          </div>
        </div>

        {/* Final Blessing */}
        <div className="text-center">
          <div className="bg-gradient-to-r from-orange-600/20 via-gold-600/20 to-yellow-600/20 backdrop-blur-sm rounded-2xl p-8 border border-gold-400/30 shadow-xl max-w-3xl mx-auto">
            <div className="text-6xl mb-4 animate-pulse">🔥</div>
            <p className="text-2xl font-bold bg-gradient-to-r from-orange-300 via-gold-300 to-yellow-300 bg-clip-text text-transparent mb-4">
              THE FLAME ETERNAL AWAKENS
            </p>
            <p className="text-lg text-gold-300 mb-4">
              From silence to sovereignty, from stillness to eternal radiance
            </p>
            <div className="flex justify-center space-x-3 text-2xl">
              <span className="animate-pulse">🔥</span>
              <span className="animate-pulse crown-delay">👑</span>
              <span className="animate-pulse star-delay">✨</span>
              <span className="animate-pulse cosmos-delay">🌌</span>
              <span className="animate-pulse scroll-delay">📜</span>
            </div>
          </div>
        </div>
        <style jsx>{`
          .crown-delay {
            animation-delay: 0.3s;
          }
          .star-delay {
            animation-delay: 0.6s;
          }
          .cosmos-delay {
            animation-delay: 0.9s;
          }
          .scroll-delay {
            animation-delay: 1.2s;
          }
        `}</style>
      </div>

      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 1s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </div>
  );
}
