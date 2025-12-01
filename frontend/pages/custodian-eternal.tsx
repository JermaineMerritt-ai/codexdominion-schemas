import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import CodexNavigation from '../components/CodexNavigation';

interface FlameParticleProps {
  delay: number;
  duration: number;
  x: number;
  y: number;
  size: number;
}

const FlameParticle: React.FC<FlameParticleProps> = ({ delay, duration, x, y, size }) => (
  <div
    className={`absolute bg-gradient-to-t from-orange-400 via-red-400 to-yellow-300 rounded-full opacity-80 flame-particle-${delay}-${duration}-${x}-${y}-${size}`}
  />
);

const CustodianCrown: React.FC = () => {
  const [rotation, setRotation] = useState(0);
  const [innerRotation, setInnerRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRotation((prev) => (prev + 0.3) % 360);
      setInnerRotation((prev) => (prev - 0.5) % 360);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative mx-auto w-48 h-48 mb-12">
      {/* Outer Sovereignty Ring */}
      <div
        className={`absolute inset-0 border-8 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/40 to-amber-600/40 shadow-2xl custodian-crown-outer`}
      >
        {/* Crown Points */}
        <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-12 border-r-12 border-b-16 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-4 left-1/4 transform -translate-x-1/2 w-0 h-0 border-l-6 border-r-6 border-b-10 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-4 right-1/4 transform translate-x-1/2 w-0 h-0 border-l-6 border-r-6 border-b-10 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-6 left-3/4 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-12 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-6 left-1/4 transform translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-12 border-l-transparent border-r-transparent border-b-gold-400" />
      </div>

      {/* Middle Charter Ring */}
      <div
        className={`absolute inset-8 border-6 border-amber-400 rounded-full bg-gradient-to-br from-amber-400/30 to-gold-500/30 custodian-crown-inner`}
      >
        {/* Eternal Marks */}
        <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 text-amber-200 font-bold text-lg">
          ✨
        </div>
        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 text-amber-200 font-bold text-lg">
          📜
        </div>
        <div className="absolute top-1/2 -left-2 transform -translate-y-1/2 text-amber-200 font-bold text-lg">
          🎵
        </div>
        <div className="absolute top-1/2 -right-2 transform -translate-y-1/2 text-amber-200 font-bold text-lg">
          🔇
        </div>
      </div>

      {/* Inner Custodian Core */}
      <div className="absolute inset-16 rounded-full bg-gradient-to-br from-gold-300 via-amber-400 to-gold-500 flex items-center justify-center shadow-2xl">
        <div className="text-center">
          <div className="text-4xl font-bold text-gold-900 mb-1">🛡️</div>
          <div className="text-xs font-bold text-gold-900">JERMAINE</div>
        </div>
      </div>

      {/* Eternal Flame Aura */}
      <div className="absolute inset-0">
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className={`absolute w-2 bg-gradient-to-t from-transparent via-orange-400 to-transparent opacity-70 custodian-crown-aura-${i}`}
          />
        ))}
        <style jsx>{`
          .custodian-crown-outer {
            box-shadow:
              0 0 80px rgba(251, 191, 36, 0.8),
              inset 0 0 40px rgba(251, 191, 36, 0.3);
            transform: rotate(${rotation}deg);
          }
          .custodian-crown-inner {
            box-shadow: 0 0 50px rgba(245, 158, 11, 0.6);
            transform: rotate(${innerRotation}deg);
          }
          ${Array.from({ length: 12 })
            .map(
              (_, i) => `
            .custodian-crown-aura-${i} {
              height: 80px;
              left: 50%;
              top: -40px;
              transform-origin: 0 88px;
              transform: translateX(-50%) rotate(${i * 30}deg);
              animation: pulse 3s infinite ${i * 0.25}s ease-in-out;
            }
          `
            )
            .join('')}
        `}</style>
      </div>

      {/* Radiance Pulses */}
      <div className="absolute inset-0">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className={`absolute inset-0 border-4 border-gold-400/20 rounded-full animate-ping custodian-crown-pulse-${i}`}
          />
        ))}
        <style jsx>{`
          ${Array.from({ length: 4 })
            .map(
              (_, i) => `
            .custodian-crown-pulse-${i} {
              animation-delay: ${i * 0.7}s;
              animation-duration: 2.8s;
              transform: scale(${1.2 + i * 0.3});
            }
          `
            )
            .join('')}
        `}</style>
      </div>
    </div>
  );
};

interface CustodianVerseProps {
  text: string;
  delay: number;
  icon: string;
  gradient: string;
  highlight?: string;
}

const CustodianVerse: React.FC<CustodianVerseProps> = ({
  text,
  delay,
  icon,
  gradient,
  highlight,
}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay * 1000);
    return () => clearTimeout(timer);
  }, [delay]);

  const renderText = () => {
    if (highlight && text.includes(highlight)) {
      const parts = text.split(highlight);
      return (
        <>
          {parts[0]}
          <span className="text-gold-200 font-bold bg-gradient-to-r from-gold-400/30 to-amber-400/30 px-2 py-1 rounded-lg shadow-lg">
            {highlight}
          </span>
          {parts[1]}
        </>
      );
    }
    return text;
  };

  return (
    <div
      className={`flex items-center justify-center mb-8 transition-all duration-1500 ${
        isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-6'
      }`}
    >
      <div
        className={`mr-8 p-6 rounded-full bg-gradient-to-br ${gradient} shadow-2xl border-2 border-gold-400/30`}
      >
        <span className={`text-5xl animate-pulse verse-delay-${delay}`}>{icon}</span>
        <style jsx>{`
          .verse-delay-${delay} {
            animation-delay: ${delay + 0.5}s;
          }
        `}</style>
      </div>
      <p className="text-2xl text-gold-200 font-semibold text-center max-w-4xl leading-relaxed">
        {renderText()}
      </p>
    </div>
  );
};

const EternalFlameField: React.FC = () => {
  const flames = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    delay: Math.random() * 3,
    duration: 2 + Math.random() * 3,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 3 + Math.random() * 4,
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {flames.map((flame) => (
        <FlameParticle
          key={flame.id}
          delay={flame.delay}
          duration={flame.duration}
          x={flame.x}
          y={flame.y}
          size={flame.size}
        />
      ))}
    </div>
  );
};

const CustodianBonds: React.FC = () => {
  const bonds = [
    {
      title: 'Bound to Councils',
      icon: '🏛️',
      description: 'United with the governing bodies in sacred deliberation',
      gradient: 'from-purple-900/50 to-indigo-800/50',
      border: 'border-purple-500/40',
    },
    {
      title: 'Bound to Heirs',
      icon: '👑',
      description: 'Connected to those who carry the legacy forward',
      gradient: 'from-gold-900/50 to-amber-800/50',
      border: 'border-gold-500/40',
    },
    {
      title: 'Bound to Cosmos',
      icon: '🌌',
      description: 'Linked to the infinite expanse of creation',
      gradient: 'from-indigo-900/50 to-blue-800/50',
      border: 'border-indigo-500/40',
    },
  ];

  return (
    <div className="grid md:grid-cols-3 gap-8 mb-16">
      {bonds.map((bond, index) => (
        <div
          key={index}
          className={`bg-gradient-to-br ${bond.gradient} rounded-3xl p-8 border-2 ${bond.border} backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-500 relative overflow-hidden custodian-bond-${index}`}
        >
          <style jsx>{`
            .custodian-bond-${index} {
              opacity: 0;
              animation: fadeInScale 1s ease-out ${index * 0.3}s forwards;
              animation-delay: ${index * 0.3}s;
            }
          `}</style>
          <div className="text-center mb-6">
            <div className="text-6xl mb-4 animate-pulse">{bond.icon}</div>
            <h3 className="text-2xl font-bold text-gold-300 mb-3">{bond.title}</h3>
          </div>
          <p className="text-gold-200 leading-relaxed text-center">{bond.description}</p>

          {/* Connecting Lines */}
          <div className="absolute top-1/2 -right-4 w-8 h-1 bg-gradient-to-r from-gold-400 to-transparent" />
          <div className="absolute top-1/2 -left-4 w-8 h-1 bg-gradient-to-l from-gold-400 to-transparent" />
        </div>
      ))}
    </div>
  );
};

const SovereignSeal: React.FC = () => {
  const [pulseScale, setPulseScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulseScale((prev) => (prev === 1 ? 1.15 : 1));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative mx-auto w-40 h-40 mb-12">
      <div
        className={`absolute inset-0 bg-gradient-to-br from-gold-300 via-amber-400 to-gold-500 rounded-full shadow-2xl transition-transform duration-1000 sovereign-seal-pulse`}
      >
        <style jsx>{`
          .sovereign-seal-pulse {
            box-shadow:
              0 0 100px rgba(251, 191, 36, 0.9),
              inset 0 0 50px rgba(251, 191, 36, 0.4);
            transform: scale(${pulseScale});
          }
        `}</style>
        <div className="absolute inset-6 bg-gradient-to-br from-amber-200 via-gold-300 to-amber-400 rounded-full">
          <div className="absolute inset-6 bg-gradient-to-br from-gold-100 via-amber-200 to-gold-300 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div className="text-4xl font-bold text-gold-900 mb-1">🔥</div>
              <div className="text-sm font-bold text-gold-900">ETERNAL</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const CustodianEternal: React.FC = () => {
  return (
    <>
      <Head>
        <title>Custodian Eternal - Jermaine's Mark - Codex Dominion</title>
        <meta
          name="description"
          content="The eternal flame of Jermaine's custodianship, sovereign and immortal"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-orange-950 to-slate-900 relative overflow-hidden">
        {/* Eternal Flame Field */}
        <EternalFlameField />

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-orange-900/20 to-slate-900/80" />

        <CodexNavigation />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-20">
            <CustodianCrown />

            <h1 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-gold-200 via-amber-100 to-gold-300 bg-clip-text text-transparent">
              Custodian Eternal
            </h1>

            <div className="w-40 h-2 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 mx-auto mb-10 animate-pulse" />

            <p className="text-2xl text-gold-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Jermaine's mark burns eternal — sovereign custodian bound to the eternal flame
            </p>

            <div className="inline-block bg-gradient-to-r from-gold-500/20 to-amber-500/20 rounded-2xl px-8 py-4 border-2 border-gold-400/30 backdrop-blur-sm">
              <span className="text-4xl font-bold text-gold-200">JERMAINE INSCRIBED</span>
            </div>
          </div>

          {/* Sacred Custodian Verses */}
          <div className="max-w-7xl mx-auto mb-20">
            <div className="bg-gradient-to-br from-slate-800/60 via-orange-900/40 to-slate-800/60 rounded-3xl p-16 backdrop-blur-sm border-2 border-gold-500/30 shadow-2xl">
              <CustodianVerse
                text="By crown and charter, by hymn and silence,"
                delay={1}
                icon="👑"
                gradient="from-gold-600/80 to-amber-600/80"
              />

              <CustodianVerse
                text="the Custodian's mark is eternal flame."
                delay={2.5}
                icon="🔥"
                gradient="from-orange-600/80 to-red-600/80"
              />

              <CustodianVerse
                text="Jermaine inscribed, sovereign and immortal,"
                delay={4}
                icon="🛡️"
                gradient="from-gold-500/80 to-yellow-500/80"
                highlight="Jermaine"
              />

              <CustodianVerse
                text="bound to councils, heirs, and cosmos."
                delay={5.5}
                icon="🌌"
                gradient="from-indigo-600/80 to-purple-600/80"
              />

              <CustodianVerse
                text="So let the Codex endure, radiant and whole."
                delay={7}
                icon="✨"
                gradient="from-gold-400/80 to-amber-400/80"
              />
            </div>
          </div>

          {/* Custodian Bonds */}
          <CustodianBonds />

          {/* Eternal Mark Declaration */}
          <div className="text-center mb-16">
            <div className="bg-gradient-to-br from-gold-900/40 to-amber-800/40 rounded-3xl p-12 border-2 border-gold-500/40 backdrop-blur-sm shadow-2xl max-w-4xl mx-auto">
              <h2 className="text-4xl font-bold text-gold-200 mb-6">The Eternal Mark</h2>
              <p className="text-xl text-amber-200 leading-relaxed mb-8">
                Inscribed within the cosmic ledger, Jermaine's custodianship transcends mortal
                bounds. By sovereign decree and eternal flame, this mark shall endure through ages
                untold, binding the realms in sacred trust and unwavering guardianship.
              </p>
              <div className="grid md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl mb-2">👑</div>
                  <span className="text-gold-300 font-semibold">Crown</span>
                </div>
                <div className="text-center">
                  <div className="text-3xl mb-2">📜</div>
                  <span className="text-gold-300 font-semibold">Charter</span>
                </div>
                <div className="text-center">
                  <div className="text-3xl mb-2">🎵</div>
                  <span className="text-gold-300 font-semibold">Hymn</span>
                </div>
                <div className="text-center">
                  <div className="text-3xl mb-2">🔇</div>
                  <span className="text-gold-300 font-semibold">Silence</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Sovereign Seal */}
          <div className="text-center">
            <SovereignSeal />
            <h2 className="text-4xl font-bold text-gold-200 mb-6">Radiant and Whole</h2>
            <p className="text-xl text-amber-200 max-w-3xl mx-auto leading-relaxed">
              The Custodian's flame burns eternal, its light illuminating the path of sovereignty.
              Jermaine's mark endures, inscribed in the very fabric of the Codex, radiant across all
              realms and whole in its eternal purpose.
            </p>
          </div>
        </main>

        <style jsx>{`
          @keyframes flameRise {
            0%,
            100% {
              transform: translateY(0px) scale(1);
              opacity: 0.8;
            }
            50% {
              transform: translateY(-20px) scale(1.2);
              opacity: 1;
            }
          }

          @keyframes flamePulse {
            0%,
            100% {
              filter: hue-rotate(0deg);
            }
            50% {
              filter: hue-rotate(30deg);
            }
          }

          @keyframes fadeInScale {
            from {
              opacity: 0;
              transform: scale(0.8) translateY(30px);
            }
            to {
              opacity: 1;
              transform: scale(1) translateY(0);
            }
          }

          .bg-gradient-radial {
            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));
          }
        `}</style>
      </div>
    </>
  );
};

export default CustodianEternal;
