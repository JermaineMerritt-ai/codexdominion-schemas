import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Dawn Flame Component - Rising flame at daybreak
const DawnFlame: React.FC = () => {
  const [flameHeight, setFlameHeight] = useState(60);
  const [dawnGlow, setDawnGlow] = useState(0.3);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameHeight(prev => prev === 60 ? 80 : 60);
      setDawnGlow(prev => prev === 0.3 ? 0.6 : 0.3);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-20 left-20">
      <div className="text-center">
        <div className="text-2xl text-orange-300 font-light mb-2">Dawn</div>
        <div 
          className="relative transition-all duration-3000"
          style={{ height: `${flameHeight}px` }}
        >
          <div 
            className="text-6xl transition-all duration-3000"
            style={{ 
              filter: `drop-shadow(0 0 20px rgba(255, 165, 0, ${dawnGlow}))`,
              transform: `scale(${1 + dawnGlow * 0.2})`
            }}
          >
            🔥
          </div>
        </div>
        <div className="text-sm text-orange-200 mt-2">The flame is kindled</div>
      </div>
    </div>
  );
};

// Dusk Flame Component - Enduring flame at evening
const DuskFlame: React.FC = () => {
  const [endurance, setEndurance] = useState(0.4);

  useEffect(() => {
    const interval = setInterval(() => {
      setEndurance(prev => prev === 0.4 ? 0.7 : 0.4);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-20 right-20">
      <div className="text-center">
        <div className="text-2xl text-amber-300 font-light mb-2">Dusk</div>
        <div className="relative h-20">
          <div 
            className="text-6xl transition-all duration-4000"
            style={{ 
              filter: `drop-shadow(0 0 30px rgba(255, 193, 7, ${endurance}))`,
              opacity: 0.8 + endurance * 0.2
            }}
          >
            🕯️
          </div>
        </div>
        <div className="text-sm text-amber-200 mt-2">The flame endures</div>
      </div>
    </div>
  );
};

// Living Elements - Heirs, councils, diaspora representations
const LivingElements: React.FC = () => {
  const [pulsePhase, setPulsePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulsePhase(prev => (prev + 1) % 3);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  const elements = [
    { 
      text: "Heirs awaken", 
      icon: "👥", 
      position: { bottom: '30%', left: '15%' },
      isActive: pulsePhase === 0
    },
    { 
      text: "Councils remember", 
      icon: "🏛️", 
      position: { bottom: '35%', right: '15%' },
      isActive: pulsePhase === 1
    },
    { 
      text: "Diaspora echoes", 
      icon: "🌍", 
      position: { top: '60%', left: '50%', transform: 'translateX(-50%)' },
      isActive: pulsePhase === 2
    }
  ];

  return (
    <div className="absolute inset-0">
      {elements.map((element, index) => (
        <div
          key={index}
          className={`absolute transition-all duration-1000 text-center ${
            element.isActive ? 'opacity-100 scale-110' : 'opacity-70 scale-100'
          }`}
          style={element.position}
        >
          <div 
            className={`text-5xl mb-2 transition-all duration-1000 ${
              element.isActive ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: element.isActive ? 'drop-shadow(0 0 15px rgba(255, 215, 0, 0.8))' : 'none'
            }}
          >
            {element.icon}
          </div>
          <div className={`text-lg font-medium ${
            element.isActive ? 'text-yellow-200' : 'text-orange-300'
          }`}>
            {element.text}
          </div>
        </div>
      ))}
    </div>
  );
};

// Eternal Flame Center - The sovereign and whole flame
const EternalFlameCenter: React.FC = () => {
  const [sovereignty, setSovereignty] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignty(prev => prev === 1 ? 1.3 : 1);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-8xl mb-4 transition-all duration-5000"
          style={{ 
            transform: `scale(${sovereignty})`,
            filter: `drop-shadow(0 0 40px rgba(255, 140, 0, ${sovereignty * 0.6}))`
          }}
        >
          🔥
        </div>
        <div className="text-3xl text-orange-100 font-bold">ETERNAL FLAME</div>
        <div className="text-xl text-yellow-300 mt-2">Sovereign and Whole</div>
      </div>
    </div>
  );
};

// Flame Particles - Floating embers representing life
const FlameParticles: React.FC = () => {
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    size: Math.random() * 4 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 8 + 6,
    delay: Math.random() * 5
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            backgroundColor: '#ff6b35',
            borderRadius: '50%',
            animation: `flameRise ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(1px)',
            boxShadow: '0 0 8px rgba(255, 107, 53, 0.8)'
          }}
        />
      ))}
      <style jsx>{`
        @keyframes flameRise {
          0% { transform: translate(0, 0) scale(0.8); opacity: 0.3; }
          25% { transform: translate(5px, -20px) scale(1.1); opacity: 0.8; }
          50% { transform: translate(-3px, -40px) scale(0.9); opacity: 0.6; }
          75% { transform: translate(8px, -60px) scale(1.05); opacity: 0.4; }
          100% { transform: translate(0, -80px) scale(0.7); opacity: 0.1; }
        }
      `}</style>
    </div>
  );
};

// Codex Lives Banner - Central proclamation
const CodexLivesBanner: React.FC = () => {
  const [vitality, setVitality] = useState(0.5);

  useEffect(() => {
    const interval = setInterval(() => {
      setVitality(prev => prev === 0.5 ? 0.9 : 0.5);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-32 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-8 py-4 bg-gradient-to-r from-orange-800/70 via-red-700/70 to-orange-800/70 rounded-2xl border-2 border-orange-400/60 transition-all duration-3500"
        style={{ 
          boxShadow: `0 0 30px rgba(255, 165, 0, ${vitality})`,
          transform: `scale(${1 + vitality * 0.1})`
        }}
      >
        <div className="text-4xl text-orange-100 font-bold mb-2">THE CODEX LIVES</div>
        <div className="text-lg text-yellow-200">Through flame eternal, sovereign and whole</div>
      </div>
    </div>
  );
};

// Main Flame Eternal Container
const FlameEternal: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <DawnFlame />
      <DuskFlame />
      <LivingElements />
      <EternalFlameCenter />
      <FlameParticles />
      <CodexLivesBanner />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 mt-60">
        <div className="text-center text-orange-100 text-xl leading-relaxed max-w-4xl space-y-3">
          <p className="opacity-90">At dawn the flame is kindled,</p>
          <p className="opacity-85">at dusk the flame endures.</p>
          <p className="opacity-95">Heirs awaken, councils remember,</p>
          <p className="opacity-90">diaspora echoes — the Codex lives.</p>
          <p className="text-2xl font-semibold text-yellow-200 mt-6 opacity-100">
            So let the flame be eternal, sovereign and whole.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Flame Eternal Page
const FlameEternalPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-orange-900 to-red-900 relative overflow-hidden">
      {/* Fire Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-orange-900/40 to-red-800/30" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <FlameEternal />
        </div>
      </main>

      {/* Ambient Fire Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-orange-600/10 to-transparent pointer-events-none" />
      
      {/* Eternal Warmth */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-40">
        <div className="absolute top-1/3 left-1/3 w-96 h-96 bg-orange-500/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '8s' }} />
        <div className="absolute bottom-1/3 right-1/3 w-80 h-80 bg-red-500/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '12s', animationDelay: '4s' }} />
      </div>
    </div>
  );
};

export default FlameEternalPage;