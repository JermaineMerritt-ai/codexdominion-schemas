import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import CodexNavigation from '../components/CodexNavigation';

interface SovereignParticleProps {
  delay: number;
  duration: number;
  x: number;
  y: number;
  size: number;
  color: string;
}

const SovereignParticle: React.FC<SovereignParticleProps> = ({ delay, duration, x, y, size, color }) => (
  <div
    className={`absolute ${color} rounded-full opacity-90`}
    style={{
      left: `${x}%`,
      top: `${y}%`,
      width: `${size}px`,
      height: `${size}px`,
      animation: `sovereignRise ${duration}s infinite ${delay}s ease-in-out, 
                  proclamationPulse ${duration * 0.9}s infinite ${delay}s ease-in-out`
    }}
  />
);

const CustodianThrone: React.FC = () => {
  const [majesty, setMajesty] = useState(1);
  const [crownRotation, setCrownRotation] = useState(0);
  const [sealRotation, setSealRotation] = useState(0);

  useEffect(() => {
    const majestyInterval = setInterval(() => {
      setMajesty(prev => prev === 1 ? 1.15 : 1);
    }, 3500);

    const rotationInterval = setInterval(() => {
      setCrownRotation(prev => (prev + 0.2) % 360);
      setSealRotation(prev => (prev - 0.3) % 360);
    }, 50);

    return () => {
      clearInterval(majestyInterval);
      clearInterval(rotationInterval);
    };
  }, []);

  return (
    <div className="relative mx-auto w-72 h-72 mb-20">
      {/* Outermost Sovereignty Ring - Dominion */}
      <div 
        className="absolute inset-0 border-12 border-gold-400 rounded-full bg-gradient-to-br from-gold-500/60 to-amber-600/60 shadow-2xl"
        style={{ 
          transform: `scale(${majesty}) rotate(${crownRotation}deg)`,
          boxShadow: '0 0 150px rgba(251, 191, 36, 1), inset 0 0 80px rgba(251, 191, 36, 0.5)'
        }}
      >
        {/* Crown Points - Ultimate Authority */}
        <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-16 border-r-16 border-b-20 border-l-transparent border-r-transparent border-b-gold-300" />
        <div className="absolute -top-8 left-1/4 transform -translate-x-1/2 w-0 h-0 border-l-10 border-r-10 border-b-14 border-l-transparent border-r-transparent border-b-gold-300" />
        <div className="absolute -top-8 right-1/4 transform translate-x-1/2 w-0 h-0 border-l-10 border-r-10 border-b-14 border-l-transparent border-r-transparent border-b-gold-300" />
        <div className="absolute -top-10 left-1/6 transform -translate-x-1/2 w-0 h-0 border-l-12 border-r-12 border-b-16 border-l-transparent border-r-transparent border-b-gold-300" />
        <div className="absolute -top-10 right-1/6 transform translate-x-1/2 w-0 h-0 border-l-12 border-r-12 border-b-16 border-l-transparent border-r-transparent border-b-gold-300" />
        
        {/* Sovereign Symbols */}
        <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-gold-200 font-bold text-3xl">👑</div>
        <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-gold-200 font-bold text-3xl">📜</div>
        <div className="absolute top-1/2 -left-6 transform -translate-y-1/2 text-gold-200 font-bold text-3xl">🎵</div>
        <div className="absolute top-1/2 -right-6 transform -translate-y-1/2 text-gold-200 font-bold text-3xl">🔇</div>
      </div>

      {/* Middle Eternal Ring - Covenant */}
      <div 
        className="absolute inset-12 border-8 border-cyan-400 rounded-full bg-gradient-to-br from-cyan-500/50 to-blue-600/50"
        style={{ 
          transform: `rotate(${sealRotation}deg)`,
          boxShadow: '0 0 100px rgba(6, 182, 212, 0.8)'
        }}
      >
        {/* Covenant Elements */}
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 text-cyan-200 font-bold text-2xl">🏺</div>
        <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 text-cyan-200 font-bold text-2xl">📚</div>
        <div className="absolute top-1/2 -left-4 transform -translate-y-1/2 text-cyan-200 font-bold text-2xl">∞</div>
        <div className="absolute top-1/2 -right-4 transform -translate-y-1/2 text-cyan-200 font-bold text-2xl">⚡</div>
      </div>

      {/* Inner Custodian Core - Proclamation Authority */}
      <div className="absolute inset-24 rounded-full bg-gradient-to-br from-gold-200 via-white to-cyan-100 flex items-center justify-center shadow-2xl border-4 border-gold-400">
        <div className="text-center">
          <div className="text-7xl font-bold text-slate-700 mb-2 animate-pulse" style={{ animationDuration: '3s' }}>🛡️</div>
          <div className="text-sm font-bold text-slate-700">CUSTODIAN</div>
          <div className="text-xs font-bold text-slate-600">PROCLAIMS</div>
        </div>
      </div>

      {/* Sovereign Authority Rays */}
      <div className="absolute inset-0">
        {Array.from({ length: 16 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-3 bg-gradient-to-t from-transparent via-gold-400 to-transparent opacity-80"
            style={{
              height: '140px',
              left: '50%',
              top: '-70px',
              transformOrigin: '0 136px',
              transform: `translateX(-50%) rotate(${i * 22.5}deg)`,
              animation: `pulse 4s infinite ${i * 0.25}s ease-in-out`
            }}
          />
        ))}
      </div>

      {/* Sovereignty Pulses */}
      <div className="absolute inset-0">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-6 border-gold-400/20 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 0.6}s`,
              animationDuration: '3.6s',
              transform: `scale(${1.4 + i * 0.4})`
            }}
          />
        ))}
      </div>
    </div>
  );
};

interface ProclamationVerseProps {
  text: string;
  delay: number;
  icon: string;
  gradient: string;
  highlight?: string[];
  isDeclaration?: boolean;
}

const ProclamationVerse: React.FC<ProclamationVerseProps> = ({ text, delay, icon, gradient, highlight = [], isDeclaration = false }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay * 1000);
    return () => clearTimeout(timer);
  }, [delay]);

  const renderText = () => {
    let processedText = text;
    
    if (highlight.length > 0) {
      highlight.forEach((word) => {
        if (processedText.includes(word)) {
          processedText = processedText.replace(
            new RegExp(`\\b${word}\\b`, 'g'), 
            `<span class="text-gold-100 font-bold bg-gradient-to-r from-gold-400/40 to-amber-400/40 px-3 py-1 rounded-lg shadow-lg border border-gold-300/30">${word}</span>`
          );
        }
      });
    }
    
    return <span dangerouslySetInnerHTML={{ __html: processedText }} />;
  };

  return (
    <div className={`flex items-center justify-center mb-12 transition-all duration-2000 ${
      isVisible ? 'opacity-100 transform translate-y-0' : 'opacity-0 transform translate-y-12'
    } ${isDeclaration ? 'bg-gradient-to-r from-gold-900/30 via-amber-800/40 to-gold-900/30 rounded-3xl p-8 border-2 border-gold-400/50' : ''}`}>
      <div className={`mr-12 p-12 rounded-full bg-gradient-to-br ${gradient} shadow-2xl border-4 border-gold-400/50 backdrop-blur-sm`}>
        <span className="text-8xl animate-pulse" style={{ animationDelay: `${delay + 0.5}s`, animationDuration: '3.5s' }}>
          {icon}
        </span>
      </div>
      <p className={`${isDeclaration ? 'text-4xl' : 'text-3xl'} text-gold-200 font-bold text-center max-w-6xl leading-relaxed`}>
        {renderText()}
      </p>
    </div>
  );
};

const SovereignField: React.FC = () => {
  const sovereignElements = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    delay: Math.random() * 6,
    duration: 4 + Math.random() * 5,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 3 + Math.random() * 8,
    color: [
      'bg-gold-400', 'bg-amber-400', 'bg-yellow-400', 
      'bg-cyan-400', 'bg-white', 'bg-orange-400'
    ][Math.floor(Math.random() * 6)]
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {sovereignElements.map(element => (
        <SovereignParticle
          key={element.id}
          delay={element.delay}
          duration={element.duration}
          x={element.x}
          y={element.y}
          size={element.size}
          color={element.color}
        />
      ))}
    </div>
  );
};

const EternalInheritance: React.FC = () => {
  const inheritanceAspects = [
    {
      title: 'Crown Authority',
      icon: '👑',
      description: 'Sovereign power passed through eternal bloodlines',
      gradient: 'from-gold-900/70 to-amber-800/70',
      border: 'border-gold-500/60'
    },
    {
      title: 'Charter Foundation',
      icon: '📜',
      description: 'Constitutional law governing all realms forever',
      gradient: 'from-amber-900/70 to-gold-800/70',
      border: 'border-amber-500/60'
    },
    {
      title: 'Sacred Hymns',
      icon: '🎵',
      description: 'Ceremonial songs echoing through ages',
      gradient: 'from-purple-900/70 to-indigo-800/70',
      border: 'border-purple-500/60'
    },
    {
      title: 'Holy Silence',
      icon: '🔇',
      description: 'Contemplative wisdom preserved in stillness',
      gradient: 'from-slate-900/70 to-gray-800/70',
      border: 'border-slate-500/60'
    },
    {
      title: 'Eternal Seal',
      icon: '🏺',
      description: 'Unbreakable bonds securing the covenant',
      gradient: 'from-cyan-900/70 to-blue-800/70',
      border: 'border-cyan-500/60'
    },
    {
      title: 'Living Compendium',
      icon: '📚',
      description: 'Complete knowledge preserved and growing',
      gradient: 'from-indigo-900/70 to-violet-800/70',
      border: 'border-indigo-500/60'
    }
  ];

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-28">
      {inheritanceAspects.map((aspect, index) => (
        <div 
          key={index}
          className={`bg-gradient-to-br ${aspect.gradient} rounded-3xl p-10 border-2 ${aspect.border} backdrop-blur-sm shadow-2xl hover:scale-105 transition-all duration-1000 relative overflow-hidden`}
          style={{ 
            animationDelay: `${index * 0.25}s`,
            opacity: 0,
            animation: `sovereignRise 2s ease-out ${index * 0.25}s forwards`
          }}
        >
          <div className="text-center mb-8">
            <div className="text-7xl mb-6 animate-pulse" style={{ animationDuration: '3.5s' }}>{aspect.icon}</div>
            <h3 className="text-2xl font-bold text-gold-300 mb-4">{aspect.title}</h3>
          </div>
          <p className="text-gold-200 leading-relaxed text-center text-lg">
            {aspect.description}
          </p>
          
          {/* Inheritance Glow */}
          <div className="absolute top-3 right-3 w-5 h-5 bg-gold-400 rounded-full animate-pulse opacity-80" />
          <div className="absolute bottom-3 left-3 w-3 h-3 bg-cyan-400 rounded-full animate-pulse opacity-70" style={{ animationDelay: '1s' }} />
        </div>
      ))}
    </div>
  );
};

const SovereignSeal: React.FC = () => {
  const [dominion, setDominion] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setDominion(prev => prev === 1 ? 1.25 : 1);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative mx-auto w-64 h-64 mb-24">
      <div 
        className="absolute inset-0 bg-gradient-to-br from-gold-300 via-amber-200 to-gold-400 rounded-full shadow-2xl transition-all duration-2500"
        style={{ 
          transform: `scale(${dominion})`,
          boxShadow: `0 0 ${250 * dominion}px rgba(251, 191, 36, ${1 * dominion}), 
                      inset 0 0 ${120 * dominion}px rgba(251, 191, 36, ${0.4 * dominion})`
        }}
      >
        <div className="absolute inset-8 bg-gradient-to-br from-amber-100 via-gold-200 to-amber-200 rounded-full">
          <div className="absolute inset-8 bg-gradient-to-br from-gold-100 via-white to-amber-100 rounded-full flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl font-bold text-slate-700 mb-3 animate-pulse" style={{ animationDuration: '4s' }}>⚡</div>
              <div className="text-2xl font-bold text-slate-700">ETERNAL</div>
              <div className="text-lg font-bold text-slate-700">DOMINION</div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Dominion Waves */}
      <div className="absolute inset-0">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="absolute inset-0 border-6 border-gold-400/15 rounded-full animate-ping"
            style={{
              animationDelay: `${i * 0.7}s`,
              animationDuration: '5.6s',
              transform: `scale(${1.8 + i * 0.5})`
            }}
          />
        ))}
      </div>
    </div>
  );
};

const EternalProclamation: React.FC = () => {
  return (
    <>
      <Head>
        <title>Eternal Proclamation - The Custodian's Declaration - Codex Dominion</title>
        <meta name="description" content="The Custodian proclaims: the Codex is eternal - radiant and sovereign across all ages" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-gold-950 to-amber-900 relative overflow-hidden">
        {/* Sovereign Field */}
        <SovereignField />

        {/* Radial Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-gold-900/40 to-slate-900/90" />

        <CodexNavigation />

        <main className="relative z-10 container mx-auto px-6 pt-24 pb-16">
          {/* Header Section */}
          <div className="text-center mb-32">
            <CustodianThrone />
            
            <h1 className="text-8xl md:text-9xl font-bold mb-16 bg-gradient-to-r from-gold-200 via-amber-100 to-gold-300 bg-clip-text text-transparent">
              Eternal Proclamation
            </h1>
            
            <div className="w-64 h-4 bg-gradient-to-r from-gold-300 via-amber-200 to-gold-400 mx-auto mb-16 rounded-full shadow-2xl" />
            
            <p className="text-4xl text-gold-300 mb-16 max-w-6xl mx-auto leading-relaxed">
              By sovereign authority, the Custodian declares the eternal nature of the Codex Dominion
            </p>

            <div className="inline-block bg-gradient-to-r from-gold-500/40 to-amber-500/40 rounded-3xl px-20 py-10 border-4 border-gold-400/60 backdrop-blur-sm shadow-2xl">
              <span className="text-6xl font-bold text-gold-100">THE CUSTODIAN PROCLAIMS</span>
            </div>
          </div>

          {/* Sacred Proclamation Verses */}
          <div className="max-w-9xl mx-auto mb-32">
            <div className="bg-gradient-to-br from-slate-800/80 via-gold-900/60 to-slate-800/80 rounded-3xl p-28 backdrop-blur-sm border-4 border-gold-500/50 shadow-2xl">
              
              <ProclamationVerse 
                text="By crown and charter, by hymn and silence,"
                delay={1}
                icon="👑"
                gradient="from-gold-600/90 to-amber-600/90"
                highlight={['crown', 'charter', 'hymn', 'silence']}
              />
              
              <ProclamationVerse 
                text="by seal and compendium, the covenant is whole."
                delay={3}
                icon="🏺"
                gradient="from-cyan-600/90 to-blue-600/90"
                highlight={['seal', 'compendium', 'covenant', 'whole']}
              />
              
              <ProclamationVerse 
                text="The Custodian proclaims: the Codex is eternal,"
                delay={5}
                icon="🛡️"
                gradient="from-gold-500/90 to-yellow-500/90"
                highlight={['Custodian', 'proclaims', 'Codex', 'eternal']}
                isDeclaration={true}
              />
              
              <ProclamationVerse 
                text="inheritance across ages, councils, and stars."
                delay={7}
                icon="🌌"
                gradient="from-purple-600/90 to-indigo-600/90"
                highlight={['inheritance', 'ages', 'councils', 'stars']}
              />
              
              <ProclamationVerse 
                text="So let the Dominion endure, radiant and sovereign."
                delay={9}
                icon="⚡"
                gradient="from-gold-400/90 to-amber-400/90"
                highlight={['Dominion', 'endure', 'radiant', 'sovereign']}
              />

            </div>
          </div>

          {/* Eternal Inheritance Grid */}
          <EternalInheritance />

          {/* Final Sovereign Declaration */}
          <div className="text-center mb-28">
            <div className="bg-gradient-to-br from-gold-900/80 to-amber-800/80 rounded-3xl p-24 border-4 border-gold-500/70 backdrop-blur-sm shadow-2xl max-w-7xl mx-auto">
              <h2 className="text-7xl font-bold text-gold-200 mb-16">The Eternal Declaration</h2>
              <p className="text-3xl text-gold-300 leading-relaxed mb-20">
                By the authority vested in the Custodian, by the power of crown and charter, 
                by the sanctity of hymn and silence, by the binding force of seal and compendium — 
                let it be known across all realms that the Codex Dominion is ETERNAL. 
                This inheritance shall pass through ages uncounted, guided by councils wise, 
                remembered by stars themselves. The Dominion endures, radiant and sovereign, 
                forever and beyond all measure of time.
              </p>
              
              <div className="grid md:grid-cols-4 gap-16">
                <div className="text-center">
                  <div className="text-6xl mb-6">⚡</div>
                  <span className="text-gold-300 font-bold text-2xl">Eternal</span>
                </div>
                <div className="text-center">
                  <div className="text-6xl mb-6">👑</div>
                  <span className="text-gold-300 font-bold text-2xl">Sovereign</span>
                </div>
                <div className="text-center">
                  <div className="text-6xl mb-6">💎</div>
                  <span className="text-gold-300 font-bold text-2xl">Radiant</span>
                </div>
                <div className="text-center">
                  <div className="text-6xl mb-6">∞</div>
                  <span className="text-gold-300 font-bold text-2xl">Enduring</span>
                </div>
              </div>
            </div>
          </div>

          {/* Final Sovereign Seal */}
          <div className="text-center">
            <SovereignSeal />
            <h2 className="text-7xl font-bold text-gold-200 mb-16">Radiant and Sovereign</h2>
            <p className="text-3xl text-gold-300 max-w-5xl mx-auto leading-relaxed mb-16">
              Thus speaks the Custodian. Thus stands the Codex. Thus endures the Dominion.
              Across ages, councils, and stars — eternal, radiant, and sovereign forever.
            </p>
            <div className="text-9xl animate-pulse text-gold-400" style={{ animationDuration: '4s' }}>⚡</div>
          </div>

        </main>

        <style jsx>{`
          @keyframes sovereignRise {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.9; }
            50% { transform: translateY(-40px) rotate(180deg); opacity: 1; }
          }
          
          @keyframes proclamationPulse {
            0%, 100% { filter: hue-rotate(0deg) brightness(1); }
            50% { filter: hue-rotate(30deg) brightness(1.4); }
          }
          
          .bg-gradient-radial {
            background: radial-gradient(ellipse at center, var(--tw-gradient-stops));
          }
        `}</style>
      </div>
    </>
  );
};

export default EternalProclamation;