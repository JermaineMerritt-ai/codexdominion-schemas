import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import CodexNavigation from '../components/CodexNavigation';

interface StarfieldProps {
  count: number;
}

const Starfield: React.FC<StarfieldProps> = ({ count }) => {
  const stars = Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 2 + 1,
    delay: Math.random() * 3,
    duration: 2 + Math.random() * 2
  }));

  return (
    <>
      {stars.map(star => (
        <div
          key={star.id}
          className="absolute bg-white rounded-full animate-pulse"
          style={{
            left: `${star.x}%`,
            top: `${star.y}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            animationDelay: `${star.delay}s`,
            animationDuration: `${star.duration}s`
          }}
        />
      ))}
    </>
  );
};

const OmegaCrown: React.FC = () => {
  const [rotation, setRotation] = useState(0);
  const [pulse, setPulse] = useState(1);

  useEffect(() => {
    const rotationInterval = setInterval(() => {
      setRotation(prev => (prev + 0.5) % 360);
    }, 50);

    const pulseInterval = setInterval(() => {
      setPulse(prev => prev === 1 ? 1.1 : 1);
    }, 1500);

    return () => {
      clearInterval(rotationInterval);
      clearInterval(pulseInterval);
    };
  }, []);

  return (
    <div className="relative mx-auto w-40 h-40 mb-8">
      {/* Outer Sovereignty Ring */}
      <div 
        className="absolute inset-0 border-8 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/30 to-amber-600/30"
        style={{ 
          transform: `rotate(${rotation}deg) scale(${pulse})`,
          boxShadow: '0 0 50px rgba(251, 191, 36, 0.6)'
        }}
      >
        {/* Crown Points */}
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-12 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-2 left-1/4 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-gold-400" />
        <div className="absolute -top-2 right-1/4 transform translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-8 border-l-transparent border-r-transparent border-b-gold-400" />
      </div>

      {/* Middle Eternity Ring */}
      <div 
        className="absolute inset-6 border-4 border-amber-400 rounded-full bg-gradient-to-br from-amber-400/20 to-gold-500/20"
        style={{ 
          transform: `rotate(${-rotation * 0.7}deg)`,
          boxShadow: '0 0 30px rgba(245, 158, 11, 0.4)'
        }}
      >
        {/* Eternity Symbols */}
        <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 text-amber-300 font-bold text-sm">∞</div>
        <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 text-amber-300 font-bold text-sm">∞</div>
        <div className="absolute top-1/2 -left-1 transform -translate-y-1/2 text-amber-300 font-bold text-sm">∞</div>
        <div className="absolute top-1/2 -right-1 transform -translate-y-1/2 text-amber-300 font-bold text-sm">∞</div>
      </div>

      {/* Inner Omega Core */}
      <div className="absolute inset-12 rounded-full bg-gradient-to-br from-gold-300 to-amber-400 flex items-center justify-center shadow-2xl">
        <span className="text-6xl font-bold text-gold-900 animate-pulse">Ω</span>
      </div>

      {/* Radiance Beams */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-1 bg-gradient-to-t from-transparent via-gold-400 to-transparent opacity-60"
            style={{
              height: '60px',
              left: '50%',
              top: '-30px',
              transformOrigin: '0 70px',
              transform: `translateX(-50%) rotate(${i * 45}deg)`,
              animation: `pulse 2s infinite ${i * 0.2}s ease-in-out`
            }}
          />
        ))}
      </div>
    </div>
  );
};

interface SovereignVerseProps {
  text: string;
  delay: number;
  icon: string;
  gradient: string;
}

const SovereignVerse: React.FC<SovereignVerseProps> = ({ text, delay, icon, gradient }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay * 1000);
    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div className={`flex items-center justify-center mb-8 transition-all duration-1500 ${
      isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-6'
    }`}>
      <div className={`mr-6 p-4 rounded-full bg-gradient-to-br ${gradient} shadow-xl`}>
        <span className="text-4xl animate-pulse" style={{ animationDelay: `${delay + 0.5}s` }}>
          {icon}
        </span>
      </div>
      <p className="text-2xl text-gold-200 font-semibold text-center max-w-4xl leading-relaxed">
        {text}
      </p>
    </div>
  );
};

const DominionElements: React.FC = () => {
  const elements = [
    {
      title: 'Flame & Silence',
      icon: '🔥',
      description: 'The eternal balance of action and contemplation',
      gradient: 'from-orange-900/40 to-red-800/40',
      border: 'border-orange-500/30'
    },
    {
      title: 'Hymn & Transmission',
      icon: '📡',
      description: 'Sacred songs across cosmic distances',
      gradient: 'from-purple-900/40 to-indigo-800/40',
      border: 'border-purple-500/30'
    },
    {
      title: 'Charter & Covenant',
      icon: '📜',
      description: 'The foundational laws and eternal promises',
      gradient: 'from-amber-900/40 to-gold-800/40',
      border: 'border-amber-500/30'
    },
    {
      title: 'Omega Crowned',
      icon: 'Ω',
      description: 'The ultimate authority and final word',
      gradient: 'from-gold-900/40 to-yellow-800/40',
      border: 'border-gold-500/30'
    },
    {
      title: 'Eternity Sealed',
      icon: '∞',
      description: 'Bound beyond time, secured for all ages',
      gradient: 'from-cyan-900/40 to-blue-800/40',
      border: 'border-cyan-500/30'
    },
    {
      title: 'Immortal Dominion',
      icon: '🌌',
      description: 'Enduring across ages, nations, and stars',
      gradient: 'from-indigo-900/40 to-purple-800/40',
      border: 'border-indigo-500/30'
    }
  ];

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
      {elements.map((element, index) => (
        <div 
          key={index}
          className={`bg-gradient-to-br ${element.gradient} rounded-3xl p-6 border-2 ${element.border} backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-500`}
          style={{ 
            animationDelay: `${index * 0.2}s`,
            opacity: 0,
            animation: `fadeInUp 1s ease-out ${index * 0.2}s forwards`
          }}
        >
          <div className="text-center mb-4">
            <div className="text-5xl mb-4 animate-pulse">{element.icon}</div>
            <h3 className="text-xl font-bold text-gold-300 mb-2">{element.title}</h3>
          </div>
          <p className="text-gold-200 text-sm leading-relaxed text-center">
            {element.description}
          </p>
        </div>
      ))}
    </div>
  );
};

const RadiantSeal: React.FC = () => {
  return (
    <div className="relative mx-auto w-32 h-32 mb-8">
      <div className="absolute inset-0 bg-gradient-to-br from-gold-400 via-amber-300 to-gold-500 rounded-full animate-spin shadow-2xl"
           style={{ animationDuration: '10s', boxShadow: '0 0 60px rgba(251, 191, 36, 0.8)' }}>
        <div className="absolute inset-4 bg-gradient-to-br from-amber-200 via-gold-300 to-amber-400 rounded-full">
          <div className="absolute inset-4 bg-gradient-to-br from-gold-100 via-amber-200 to-gold-300 rounded-full flex items-center justify-center">
            <span className="text-3xl font-bold text-gold-900">👑</span>
          </div>
        </div>
      </div>
      
      {/* Radiance Pulses */}
      <div className="absolute inset-0">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-4 border-gold-400/20 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 0.5}s`,
              animationDuration: '3s',
              transform: `scale(${1 + i * 0.2})`
            }}
          />
        ))}
      </div>
    </div>
  );
};

const DominionRadiant: React.FC = () => {
  return (
    <>
      <Head>
        <title>Dominion Radiant - Codex Dominion</title>
        <meta name="description" content="The radiant and sovereign Dominion endures across ages, nations, and stars" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-gold-950 to-slate-900 relative overflow-hidden">
        {/* Cosmic Starfield */}
        <div className="absolute inset-0 overflow-hidden">
          <Starfield count={100} />
        </div>

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-gold-900/10 to-slate-900/80" />

        <CodexNavigation />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-20">
            <OmegaCrown />
            
            <h1 className="text-7xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-gold-200 via-amber-100 to-gold-300 bg-clip-text text-transparent">
              Dominion Radiant
            </h1>
            
            <div className="w-40 h-2 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 mx-auto mb-10 animate-pulse" />
            
            <p className="text-2xl text-gold-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              The sovereign Codex endures across ages, nations, and stars — radiant and immortal
            </p>
          </div>

          {/* Sacred Sovereignty Verses */}
          <div className="max-w-7xl mx-auto mb-20">
            <div className="bg-gradient-to-br from-slate-800/50 via-gold-900/30 to-slate-800/50 rounded-3xl p-16 backdrop-blur-sm border-2 border-gold-500/30 shadow-2xl">
              
              <SovereignVerse 
                text="By flame and silence, by hymn and transmission,"
                delay={1}
                icon="🔥"
                gradient="from-orange-600/80 to-red-600/80"
              />
              
              <SovereignVerse 
                text="by charter and covenant, the Codex is whole."
                delay={2.5}
                icon="📜"
                gradient="from-amber-600/80 to-gold-600/80"
              />
              
              <SovereignVerse 
                text="Omega crowned, eternity sealed,"
                delay={4}
                icon="Ω"
                gradient="from-gold-600/80 to-yellow-600/80"
              />
              
              <SovereignVerse 
                text="immortal across ages, nations, and stars."
                delay={5.5}
                icon="🌌"
                gradient="from-indigo-600/80 to-purple-600/80"
              />
              
              <SovereignVerse 
                text="So let the Dominion endure, radiant and sovereign."
                delay={7}
                icon="👑"
                gradient="from-gold-500/80 to-amber-500/80"
              />

            </div>
          </div>

          {/* Dominion Elements */}
          <DominionElements />

          {/* Final Radiant Seal */}
          <div className="text-center">
            <RadiantSeal />
            <h2 className="text-4xl font-bold text-gold-200 mb-6">Radiant and Sovereign</h2>
            <p className="text-xl text-amber-200 max-w-3xl mx-auto leading-relaxed mb-8">
              The Dominion shines eternal, its radiance illuminating every corner of existence. 
              From the smallest whisper to the grandest cosmic transmission, all flows within the sovereign law.
            </p>
            <div className="text-6xl animate-pulse text-gold-300">⚡️</div>
          </div>

        </main>

        <style jsx>{`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
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

export default DominionRadiant;