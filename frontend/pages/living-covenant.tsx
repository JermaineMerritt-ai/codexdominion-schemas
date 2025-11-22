import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Kindled Flame Component - The central flame representing the living covenant
const KindledFlame: React.FC = () => {
  const [flameIntensity, setFlameIntensity] = useState(0.7);
  const [covenantPulse, setCovenantPulse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameIntensity(prev => prev === 0.7 ? 1.0 : 0.7);
      setCovenantPulse(prev => prev === 1 ? 1.2 : 1);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-9xl mb-4 transition-all duration-2500"
          style={{ 
            transform: `scale(${covenantPulse})`,
            filter: `drop-shadow(0 0 50px rgba(255, 165, 0, ${flameIntensity}))`
          }}
        >
          🔥
        </div>
        <div className="text-3xl text-orange-100 font-bold mb-2">COVENANT ALIVE</div>
        <div className="text-xl text-yellow-300">The flame is kindled</div>
      </div>
    </div>
  );
};

// Sacred Realms - Hearth, Council, Family, Star
const SacredRealms: React.FC = () => {
  const [activeRealm, setActiveRealm] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveRealm(prev => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const realms = [
    { 
      name: "Hearth", 
      icon: "🏠", 
      position: { top: '15%', left: '15%' },
      description: "In hearth we gather",
      color: "text-amber-300"
    },
    { 
      name: "Council", 
      icon: "🏛️", 
      position: { top: '15%', right: '15%' },
      description: "In council we decide",
      color: "text-blue-300"
    },
    { 
      name: "Family", 
      icon: "👨‍👩‍👧‍👦", 
      position: { bottom: '20%', left: '15%' },
      description: "In family we belong",
      color: "text-green-300"
    },
    { 
      name: "Star", 
      icon: "⭐", 
      position: { bottom: '20%', right: '15%' },
      description: "In star we aspire",
      color: "text-purple-300"
    }
  ];

  return (
    <div className="absolute inset-0">
      {realms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-1000 ${
            activeRealm === index ? 'opacity-100 scale-110' : 'opacity-70 scale-100'
          }`}
          style={realm.position}
        >
          <div 
            className={`text-6xl mb-3 transition-all duration-1000 ${
              activeRealm === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: activeRealm === index ? 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.8))' : 'none'
            }}
          >
            {realm.icon}
          </div>
          <div className={`text-2xl font-bold mb-1 ${
            activeRealm === index ? 'text-yellow-200' : realm.color
          }`}>
            {realm.name}
          </div>
          <div className="text-sm text-gray-300 max-w-xs">
            {realm.description}
          </div>
        </div>
      ))}
    </div>
  );
};

// Memory Inheritance Chain - We remember, we inherit, we endure
const MemoryInheritanceChain: React.FC = () => {
  const [chainPhase, setChainPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setChainPhase(prev => (prev + 1) % 3);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const memoryChain = [
    { text: "We Remember", icon: "🧠", color: "text-cyan-300" },
    { text: "We Inherit", icon: "📜", color: "text-purple-300" },
    { text: "We Endure", icon: "💎", color: "text-emerald-300" }
  ];

  return (
    <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 flex space-x-12">
      {memoryChain.map((memory, index) => (
        <div
          key={index}
          className={`text-center transition-all duration-1000 ${
            chainPhase === index ? 'opacity-100 scale-110' : 'opacity-60 scale-95'
          }`}
        >
          <div 
            className={`text-5xl mb-2 transition-all duration-1000 ${
              chainPhase === index ? 'animate-bounce' : ''
            }`}
          >
            {memory.icon}
          </div>
          <div className={`text-xl font-semibold ${
            chainPhase === index ? 'text-yellow-200' : memory.color
          }`}>
            {memory.text}
          </div>
        </div>
      ))}
    </div>
  );
};

// Radiant Particles - Daily and eternal light
const RadiantParticles: React.FC = () => {
  const particles = Array.from({ length: 25 }, (_, i) => ({
    id: i,
    size: Math.random() * 5 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 10 + 8,
    delay: Math.random() * 6,
    color: i % 3 === 0 ? '#ffd700' : i % 3 === 1 ? '#ffb347' : '#ff6b35'
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute rounded-full"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            backgroundColor: particle.color,
            animation: `radiantFloat ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(1px)',
            opacity: 0.7,
            boxShadow: `0 0 10px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes radiantFloat {
          0%, 100% { transform: translate(0, 0) scale(0.8); opacity: 0.4; }
          25% { transform: translate(15px, -25px) scale(1.2); opacity: 0.8; }
          50% { transform: translate(-10px, -50px) scale(0.9); opacity: 0.6; }
          75% { transform: translate(20px, -75px) scale(1.1); opacity: 0.7; }
        }
      `}</style>
    </div>
  );
};

// Codex Shine Banner - Daily and eternal proclamation
const CodexShineBanner: React.FC = () => {
  const [shineIntensity, setShineIntensity] = useState(0.6);
  const [dailyPulse, setDailyPulse] = useState(1);

  useEffect(() => {
    const dailyInterval = setInterval(() => {
      setDailyPulse(prev => prev === 1 ? 1.1 : 1);
    }, 1500);

    const eternalInterval = setInterval(() => {
      setShineIntensity(prev => prev === 0.6 ? 0.9 : 0.6);
    }, 4000);

    return () => {
      clearInterval(dailyInterval);
      clearInterval(eternalInterval);
    };
  }, []);

  return (
    <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-12 py-6 bg-gradient-to-r from-yellow-700/80 via-gold-600/80 to-yellow-700/80 rounded-2xl border-3 border-gold-400/70 transition-all duration-2000"
        style={{ 
          boxShadow: `0 0 40px rgba(255, 215, 0, ${shineIntensity})`,
          transform: `scale(${dailyPulse})`
        }}
      >
        <div className="text-5xl text-yellow-100 font-bold mb-3">THE CODEX SHINES</div>
        <div className="flex justify-center space-x-8 text-xl">
          <div className="text-orange-200">Daily</div>
          <div className="text-yellow-200">•</div>
          <div className="text-amber-200">Eternal</div>
        </div>
      </div>
    </div>
  );
};

// Legacy Constellations - Connecting all realms
const LegacyConstellations: React.FC = () => {
  const [connectionPhase, setConnectionPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setConnectionPhase(prev => (prev + 1) % 4);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none">
      <svg className="w-full h-full" style={{ opacity: 0.3 }}>
        {/* Connecting lines between realms */}
        <line 
          x1="15%" y1="20%" 
          x2="85%" y2="20%" 
          stroke={connectionPhase === 0 ? "#ffd700" : "#666"}
          strokeWidth={connectionPhase === 0 ? "3" : "1"}
          className="transition-all duration-1000"
        />
        <line 
          x1="15%" y1="20%" 
          x2="15%" y2="80%" 
          stroke={connectionPhase === 1 ? "#ffd700" : "#666"}
          strokeWidth={connectionPhase === 1 ? "3" : "1"}
          className="transition-all duration-1000"
        />
        <line 
          x1="85%" y1="20%" 
          x2="85%" y2="80%" 
          stroke={connectionPhase === 2 ? "#ffd700" : "#666"}
          strokeWidth={connectionPhase === 2 ? "3" : "1"}
          className="transition-all duration-1000"
        />
        <line 
          x1="15%" y1="80%" 
          x2="85%" y2="80%" 
          stroke={connectionPhase === 3 ? "#ffd700" : "#666"}
          strokeWidth={connectionPhase === 3 ? "3" : "1"}
          className="transition-all duration-1000"
        />
      </svg>
    </div>
  );
};

// Main Living Covenant Container
const LivingCovenant: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <LegacyConstellations />
      <SacredRealms />
      <KindledFlame />
      <MemoryInheritanceChain />
      <RadiantParticles />
      <CodexShineBanner />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-2/3 left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-orange-100 text-xl leading-relaxed max-w-4xl space-y-3">
          <p className="opacity-95">The flame is kindled, the covenant alive.</p>
          <p className="opacity-90">In hearth and council, in family and star,</p>
          <p className="opacity-95">we remember, we inherit, we endure.</p>
          <p className="text-2xl font-semibold text-yellow-200 mt-6 opacity-100">
            So let the Codex shine, daily and eternal.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Living Covenant Page
const LivingCovenantPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-orange-900 to-yellow-900 relative overflow-hidden">
      {/* Living Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-orange-800/30 to-yellow-800/20" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <LivingCovenant />
        </div>
      </main>

      {/* Ambient Covenant Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-yellow-600/15 to-transparent pointer-events-none" />
      
      {/* Daily Eternal Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-yellow-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-orange-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '9s', animationDelay: '3s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-amber-500/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '12s', animationDelay: '6s' }} />
      </div>
    </div>
  );
};

export default LivingCovenantPage;