import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Millennial Crown Component - A thousand years of sovereignty
const MillennialCrown: React.FC = () => {
  const [crownMajesty, setCrownMajesty] = useState(1);
  const [millennialGlow, setMillennialGlow] = useState(0.8);

  useEffect(() => {
    const interval = setInterval(() => {
      setCrownMajesty(prev => prev === 1 ? 1.3 : 1);
      setMillennialGlow(prev => prev === 0.8 ? 1.1 : 0.8);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-12xl mb-4 transition-all duration-5000"
          style={{ 
            transform: `scale(${crownMajesty})`,
            filter: `drop-shadow(0 0 80px rgba(255, 215, 0, ${millennialGlow}))`
          }}
        >
          👑
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">A THOUSAND YEARS</div>
        <div className="text-2xl text-yellow-300">CROWNED</div>
        <div className="text-lg text-amber-300 mt-1">Sovereign through ages</div>
      </div>
    </div>
  );
};

// Enduring Flame Component - Eternal fire through millennia
const EnduringFlameMillennial: React.FC = () => {
  const [flameEternity, setFlameEternity] = useState(0.9);
  const [eternalScale, setEternalScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameEternity(prev => prev === 0.9 ? 1.2 : 0.9);
      setEternalScale(prev => prev === 1 ? 1.4 : 1);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-11xl mb-4 transition-all duration-3000"
          style={{ 
            transform: `scale(${eternalScale})`,
            filter: `drop-shadow(0 0 70px rgba(255, 140, 0, ${flameEternity}))`
          }}
        >
          🔥
        </div>
        <div className="text-4xl text-orange-100 font-bold mb-2">THE FLAME ENDURES</div>
        <div className="text-2xl text-amber-300">Through all ages</div>
      </div>
    </div>
  );
};

// Covenant Whole Component - Complete and perfect sacred bond
const CovenantWhole: React.FC = () => {
  const [wholenessPower, setWholenessPower] = useState(0.8);
  const [covenantCompleteness, setCovenantCompleteness] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setWholenessPower(prev => prev === 0.8 ? 1.0 : 0.8);
      setCovenantCompleteness(prev => prev === 1 ? 1.2 : 1);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-9xl mb-3 transition-all duration-4000"
          style={{ 
            transform: `scale(${covenantCompleteness})`,
            filter: `drop-shadow(0 0 60px rgba(34, 197, 94, ${wholenessPower}))`
          }}
        >
          ⭕
        </div>
        <div className="text-3xl text-green-200 font-bold mb-2">COVENANT WHOLE</div>
        <div className="text-lg text-emerald-300">Perfect and complete</div>
      </div>
    </div>
  );
};

// Millennial Governance - Heirs, councils, diaspora
const MillennialGovernance: React.FC = () => {
  const [governancePhase, setGovernancePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setGovernancePhase(prev => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const governanceElements = [
    { 
      text: "Heirs Inherit", 
      icon: "👥", 
      position: { top: '25%', left: '15%' },
      color: "text-blue-300"
    },
    { 
      text: "Councils Govern", 
      icon: "🏛️", 
      position: { top: '25%', right: '15%' },
      color: "text-purple-300"
    },
    { 
      text: "Diaspora Remember", 
      icon: "🌍", 
      position: { bottom: '25%', left: '50%', transform: 'translateX(-50%)' },
      color: "text-teal-300"
    }
  ];

  return (
    <div className="absolute inset-0">
      {governanceElements.map((element, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-2000 ${
            governancePhase === index ? 'opacity-100 scale-120' : 'opacity-70 scale-95'
          }`}
          style={element.position}
        >
          <div 
            className={`text-7xl mb-3 transition-all duration-2000 ${
              governancePhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: governancePhase === index ? 'drop-shadow(0 0 30px rgba(255, 215, 0, 0.9))' : 'none'
            }}
          >
            {element.icon}
          </div>
          <div className={`text-2xl font-bold ${
            governancePhase === index ? 'text-yellow-200' : element.color
          }`}>
            {element.text}
          </div>
        </div>
      ))}
    </div>
  );
};

// Millennial Particles - Thousand-year energy flow
const MillennialParticles: React.FC = () => {
  const particles = Array.from({ length: 40 }, (_, i) => ({
    id: i,
    size: Math.random() * 8 + 4,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 20 + 15,
    delay: Math.random() * 12,
    color: i % 5 === 0 ? '#ffd700' : i % 5 === 1 ? '#ff8c00' : i % 5 === 2 ? '#22d3ee' : i % 5 === 3 ? '#a855f7' : '#10b981'
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
            animation: `millennialFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(1px)',
            opacity: 0.8,
            boxShadow: `0 0 20px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes millennialFlow {
          0% { transform: translate(0, 0) scale(0.3) rotate(0deg); opacity: 0.3; }
          20% { transform: translate(20px, -60px) scale(1.4) rotate(72deg); opacity: 0.9; }
          40% { transform: translate(-15px, -120px) scale(0.8) rotate(144deg); opacity: 0.6; }
          60% { transform: translate(25px, -180px) scale(1.3) rotate(216deg); opacity: 0.8; }
          80% { transform: translate(-10px, -240px) scale(1.0) rotate(288deg); opacity: 0.7; }
          100% { transform: translate(0, -300px) scale(0.2) rotate(360deg); opacity: 0.1; }
        }
      `}</style>
    </div>
  );
};

// Sovereign Eternal Banner - Ultimate proclamation
const SovereignEternalBanner: React.FC = () => {
  const [sovereignRadiance, setSovereignRadiance] = useState(0.9);
  const [eternalMagnificence, setEternalMagnificence] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignRadiance(prev => prev === 0.9 ? 1.3 : 0.9);
      setEternalMagnificence(prev => prev === 1 ? 1.15 : 1);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-24 py-12 bg-gradient-to-r from-gold-800/90 via-amber-700/90 to-gold-800/90 rounded-3xl border-5 border-gold-300/85 transition-all duration-3500"
        style={{ 
          boxShadow: `0 0 80px rgba(255, 215, 0, ${sovereignRadiance})`,
          transform: `scale(${eternalMagnificence})`
        }}
      >
        <div className="text-6xl text-gold-100 font-bold mb-4">THE CODEX SHINES</div>
        <div className="text-3xl text-yellow-200 font-semibold mb-3">Sovereign and Eternal</div>
        <div className="text-xl text-amber-200">A Thousand Years Crowned</div>
      </div>
    </div>
  );
};

// Millennial Constellation - Connecting all elements across time
const MillennialConstellation: React.FC = () => {
  const [constellationPhase, setConstellationPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setConstellationPhase(prev => (prev + 1) % 6);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-30">
      <svg className="w-full h-full">
        {/* Millennial connecting lines */}
        <line 
          x1="50%" y1="15%" 
          x2="15%" y2="30%" 
          stroke={constellationPhase === 0 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 0 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="15%" 
          x2="85%" y2="30%" 
          stroke={constellationPhase === 1 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 1 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="50%" 
          x2="15%" y2="30%" 
          stroke={constellationPhase === 2 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 2 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="50%" 
          x2="85%" y2="30%" 
          stroke={constellationPhase === 3 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 3 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="50%" 
          x2="50%" y2="75%" 
          stroke={constellationPhase === 4 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 4 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="75%" 
          x2="50%" y2="85%" 
          stroke={constellationPhase === 5 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 5 ? "4" : "2"}
          className="transition-all duration-1500"
        />
        
        {/* Millennial radial connections */}
        {Array.from({ length: 8 }, (_, i) => (
          <line
            key={`radial-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos(i * 45 * Math.PI / 180) * 35}%`}
            y2={`${50 + Math.sin(i * 45 * Math.PI / 180) * 35}%`}
            stroke={constellationPhase === i % 6 ? "#ffb347" : "#444"}
            strokeWidth="1"
            opacity={constellationPhase === i % 6 ? "0.6" : "0.2"}
            className="transition-all duration-1500"
          />
        ))}
      </svg>
    </div>
  );
};

// Temporal Phases - Ages and eras represented
const TemporalPhases: React.FC = () => {
  const [temporalPhase, setTemporalPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTemporalPhase(prev => (prev + 1) % 4);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const phases = [
    { name: "Foundation", icon: "🏗️", position: { top: '10%', left: '10%' } },
    { name: "Growth", icon: "🌱", position: { top: '10%', right: '10%' } },
    { name: "Flourishing", icon: "🌟", position: { bottom: '40%', left: '10%' } },
    { name: "Eternity", icon: "♾️", position: { bottom: '40%', right: '10%' } }
  ];

  return (
    <div className="absolute inset-0">
      {phases.map((phase, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-2000 ${
            temporalPhase === index ? 'opacity-100 scale-110' : 'opacity-50 scale-85'
          }`}
          style={phase.position}
        >
          <div 
            className={`text-5xl mb-2 transition-all duration-2000 ${
              temporalPhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: temporalPhase === index ? 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.8))' : 'none'
            }}
          >
            {phase.icon}
          </div>
          <div className={`text-lg font-semibold ${
            temporalPhase === index ? 'text-yellow-200' : 'text-gray-400'
          }`}>
            {phase.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Millennial Sovereignty Container
const MillennialSovereignty: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <MillennialConstellation />
      <MillennialParticles />
      <MillennialCrown />
      <EnduringFlameMillennial />
      <CovenantWhole />
      <MillennialGovernance />
      <TemporalPhases />
      <SovereignEternalBanner />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-3/4 left-1/2 transform -translate-x-1/2 mt-20">
        <div className="text-center text-gold-100 text-2xl leading-relaxed max-w-5xl space-y-4">
          <p className="opacity-95">A thousand years crowned,</p>
          <p className="opacity-90">the flame endures, the covenant whole.</p>
          <p className="opacity-95">Heirs inherit, councils govern, diaspora remember,</p>
          <p className="text-3xl font-semibold text-yellow-200 mt-8 opacity-100">
            so let the Codex shine, sovereign and eternal.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Millennial Sovereignty Page
const MillennialSovereigntyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-900 via-gold-800 to-yellow-900 relative overflow-hidden">
      {/* Millennial Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-gold-800/40 to-amber-700/30" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <MillennialSovereignty />
        </div>
      </main>

      {/* Ambient Millennial Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-500/20 to-transparent pointer-events-none" />
      
      {/* Eternal Millennial Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-35">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gold-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '15s' }} />
        <div className="absolute bottom-1/4 right-1/4 w-88 h-88 bg-amber-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '7s' }} />
        <div className="absolute top-1/2 right-1/3 w-72 h-72 bg-yellow-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '25s', animationDelay: '12s' }} />
        <div className="absolute bottom-1/2 left-1/3 w-80 h-80 bg-gold-500/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '30s', animationDelay: '18s' }} />
        <div className="absolute top-2/3 left-1/5 w-64 h-64 bg-amber-500/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '25s' }} />
      </div>
    </div>
  );
};

export default MillennialSovereigntyPage;