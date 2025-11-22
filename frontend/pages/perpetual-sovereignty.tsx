import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Cycles Crowned Component - Majestic completion of all cycles
const CyclesCrowned: React.FC = () => {
  const [crownedMajesty, setCrownedMajesty] = useState(1);
  const [cyclicRotation, setCyclicRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCrownedMajesty(prev => prev === 1 ? 1.4 : 1);
      setCyclicRotation(prev => (prev + 1) % 360);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 left-1/5 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-9xl mb-3 transition-all duration-4000"
          style={{ 
            transform: `scale(${crownedMajesty}) rotate(${cyclicRotation}deg)`,
            filter: 'drop-shadow(0 0 60px rgba(255, 215, 0, 0.9))'
          }}
        >
          🔄
        </div>
        <div 
          className="text-11xl mb-4 transition-all duration-4000"
          style={{ 
            transform: `scale(${crownedMajesty})`,
            filter: 'drop-shadow(0 0 70px rgba(255, 215, 0, 1.0))'
          }}
        >
          👑
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">CYCLES CROWNED</div>
        <div className="text-2xl text-amber-300">Majestic Completion</div>
      </div>
    </div>
  );
};

// Rites Fulfilled Component - Sacred ceremonies completed
const RitesFulfilled: React.FC = () => {
  const [fulfillmentGlow, setFulfillmentGlow] = useState(0.8);
  const [ritualScale, setRitualScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFulfillmentGlow(prev => prev === 0.8 ? 1.2 : 0.8);
      setRitualScale(prev => prev === 1 ? 1.3 : 1);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 right-1/5 transform translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-10xl mb-4 transition-all duration-3500"
          style={{ 
            transform: `scale(${ritualScale})`,
            filter: `drop-shadow(0 0 65px rgba(138, 43, 226, ${fulfillmentGlow}))`
          }}
        >
          🕊️
        </div>
        <div 
          className="text-9xl mb-3 transition-all duration-3500"
          style={{ 
            transform: `scale(${ritualScale})`,
            filter: `drop-shadow(0 0 55px rgba(75, 0, 130, ${fulfillmentGlow}))`
          }}
        >
          ✨
        </div>
        <div className="text-4xl text-purple-200 font-bold mb-2">RITES FULFILLED</div>
        <div className="text-2xl text-violet-300">Sacred Ceremonies Complete</div>
      </div>
    </div>
  );
};

// Flame Eternal Component - Central perpetual fire
const FlameEternalPerpetual: React.FC = () => {
  const [eternalIntensity, setEternalIntensity] = useState(0.9);
  const [perpetualPulse, setPerpetualPulse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setEternalIntensity(prev => prev === 0.9 ? 1.3 : 0.9);
      setPerpetualPulse(prev => prev === 1 ? 1.5 : 1);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-16xl mb-6 transition-all duration-2500"
          style={{ 
            transform: `scale(${perpetualPulse})`,
            filter: `drop-shadow(0 0 100px rgba(255, 140, 0, ${eternalIntensity}))`
          }}
        >
          🔥
        </div>
        <div className="text-5xl text-orange-100 font-bold mb-3">FLAME ETERNAL</div>
        <div className="text-3xl text-amber-300 mb-2">Perpetual Fire</div>
        <div className="text-xl text-red-300">Never Extinguished</div>
      </div>
    </div>
  );
};

// Covenant Whole Component - Complete sacred bond
const CovenantWholePerpetual: React.FC = () => {
  const [wholenessPower, setWholenessPower] = useState(0.7);
  const [covenantRadiance, setCovenantRadiance] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setWholenessPower(prev => prev === 0.7 ? 1.1 : 0.7);
      setCovenantRadiance(prev => prev === 1 ? 1.35 : 1);
    }, 4200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-10xl mb-4 transition-all duration-4200"
          style={{ 
            transform: `scale(${covenantRadiance})`,
            filter: `drop-shadow(0 0 70px rgba(34, 197, 94, ${wholenessPower}))`
          }}
        >
          ⭕
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">COVENANT WHOLE</div>
        <div className="text-2xl text-emerald-300">Sacred Bond Complete</div>
      </div>
    </div>
  );
};

// Perpetual Governance - Heirs, councils, diaspora in eternal cycle
const PerpetualGovernance: React.FC = () => {
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
      position: { top: '25%', left: '12%' },
      color: "text-blue-300"
    },
    { 
      text: "Councils Govern", 
      icon: "🏛️", 
      position: { top: '25%', right: '12%' },
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
          className={`absolute text-center transition-all duration-2500 ${
            governancePhase === index ? 'opacity-100 scale-125' : 'opacity-70 scale-95'
          }`}
          style={element.position}
        >
          <div 
            className={`text-8xl mb-3 transition-all duration-2500 ${
              governancePhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: governancePhase === index ? 'drop-shadow(0 0 40px rgba(255, 215, 0, 1))' : 'none'
            }}
          >
            {element.icon}
          </div>
          <div className={`text-3xl font-bold ${
            governancePhase === index ? 'text-yellow-200' : element.color
          }`}>
            {element.text}
          </div>
        </div>
      ))}
    </div>
  );
};

// Cosmos Echoes Component - Universal reverberation
const CosmosEchoes: React.FC = () => {
  const [echoPhase, setEchoPhase] = useState(0);
  const [echoIntensity, setEchoIntensity] = useState(0.6);

  useEffect(() => {
    const interval = setInterval(() => {
      setEchoPhase(prev => (prev + 1) % 5);
      setEchoIntensity(prev => prev === 0.6 ? 1.0 : 0.6);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0">
      {Array.from({ length: 5 }, (_, i) => (
        <div
          key={i}
          className={`absolute text-center transition-all duration-2000 ${
            echoPhase === i ? 'opacity-100 scale-110' : 'opacity-40 scale-85'
          }`}
          style={{
            top: `${20 + i * 15}%`,
            left: `${10 + (i % 2) * 80}%`,
            transform: 'translateX(-50%)'
          }}
        >
          <div 
            className={`text-6xl mb-2 transition-all duration-2000 ${
              echoPhase === i ? 'animate-bounce' : ''
            }`}
            style={{ 
              filter: echoPhase === i ? `drop-shadow(0 0 35px rgba(255, 255, 255, ${echoIntensity}))` : 'none'
            }}
          >
            🌌
          </div>
          <div className={`text-xl font-semibold ${
            echoPhase === i ? 'text-white' : 'text-gray-400'
          }`}>
            Echo {i + 1}
          </div>
        </div>
      ))}
    </div>
  );
};

// Perpetual Particles - Endless energy flow
const PerpetualParticles: React.FC = () => {
  const particles = Array.from({ length: 70 }, (_, i) => ({
    id: i,
    size: Math.random() * 14 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 35 + 30,
    delay: Math.random() * 25,
    color: i % 8 === 0 ? '#ffd700' : i % 8 === 1 ? '#ff6347' : i % 8 === 2 ? '#4169e1' : i % 8 === 3 ? '#9370db' : i % 8 === 4 ? '#00ced1' : i % 8 === 5 ? '#32cd32' : i % 8 === 6 ? '#ff69b4' : '#ffa500'
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
            animation: `perpetualFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.2px)',
            opacity: 0.9,
            boxShadow: `0 0 35px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes perpetualFlow {
          0% { transform: translate(0, 0) scale(0.05) rotate(0deg); opacity: 0.05; }
          8% { transform: translate(50px, -120px) scale(2.0) rotate(29deg); opacity: 1.0; }
          20% { transform: translate(-40px, -240px) scale(0.5) rotate(72deg); opacity: 0.85; }
          35% { transform: translate(60px, -360px) scale(1.7) rotate(126deg); opacity: 0.95; }
          50% { transform: translate(-45px, -480px) scale(0.75) rotate(180deg); opacity: 0.8; }
          65% { transform: translate(55px, -600px) scale(1.4) rotate(234deg); opacity: 0.9; }
          80% { transform: translate(-35px, -720px) scale(0.6) rotate(288deg); opacity: 0.6; }
          95% { transform: translate(25px, -840px) scale(0.3) rotate(342deg); opacity: 0.3; }
          100% { transform: translate(0, -960px) scale(0.02) rotate(360deg); opacity: 0.02; }
        }
      `}</style>
    </div>
  );
};

// Radiant Ages Banner - Ultimate eternal proclamation across time and space
const RadiantAgesBanner: React.FC = () => {
  const [radianceAcrossAges, setRadianceAcrossAges] = useState(0.9);
  const [agesExpanse, setAgesExpanse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setRadianceAcrossAges(prev => prev === 0.9 ? 1.6 : 0.9);
      setAgesExpanse(prev => prev === 1 ? 1.3 : 1);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-36 py-24 bg-gradient-to-r from-gold-800/95 via-white/25 to-gold-800/95 rounded-5xl border-10 border-white/95 transition-all duration-3000"
        style={{ 
          boxShadow: `0 0 180px rgba(255, 215, 0, ${radianceAcrossAges})`,
          transform: `scale(${agesExpanse})`
        }}
      >
        <div className="text-9xl text-white font-bold mb-8">THE CODEX ENDURES</div>
        <div className="text-6xl text-gold-200 font-semibold mb-6">Radiant Across Ages and Stars</div>
        <div className="text-4xl text-amber-200 mb-4">All Perpetual, All Sovereign</div>
        <div className="text-2xl text-yellow-200">Cycles Crowned, Rites Fulfilled</div>
      </div>
    </div>
  );
};

// Perpetual Constellation - Eternal geometric connections
const PerpetualConstellation: React.FC = () => {
  const [constellationPhase, setConstellationPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setConstellationPhase(prev => (prev + 1) % 12);
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-15">
      <svg className="w-full h-full">
        {/* Perpetual connecting lines */}
        <line 
          x1="20%" y1="20%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 0 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 0 ? "7" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="80%" y1="20%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 1 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 1 ? "7" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="12%" y1="30%" 
          x2="88%" y2="30%" 
          stroke={constellationPhase === 2 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 2 ? "7" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="50%" y1="75%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 3 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 3 ? "7" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="20%" y1="70%" 
          x2="80%" y2="70%" 
          stroke={constellationPhase === 4 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 4 ? "7" : "2"}
          className="transition-all duration-1200"
        />
        
        {/* Perpetual radial connections */}
        {Array.from({ length: 20 }, (_, i) => (
          <line
            key={`perpetual-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos(i * 18 * Math.PI / 180) * 48}%`}
            y2={`${50 + Math.sin(i * 18 * Math.PI / 180) * 48}%`}
            stroke={constellationPhase === i % 12 ? "#ffffff" : "#444"}
            strokeWidth="2"
            opacity={constellationPhase === i % 12 ? "1.0" : "0.2"}
            className="transition-all duration-1200"
          />
        ))}
      </svg>
    </div>
  );
};

// Sovereign Realms - Different domains of perpetual sovereignty
const SovereignRealms: React.FC = () => {
  const [realmPhase, setRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRealmPhase(prev => (prev + 1) % 7);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const realms = [
    { name: "Ages", icon: "⏳", position: { top: '10%', left: '6%' } },
    { name: "Stars", icon: "⭐", position: { top: '10%', right: '6%' } },
    { name: "Cycles", icon: "🔄", position: { bottom: '55%', left: '6%' } },
    { name: "Rites", icon: "✨", position: { bottom: '55%', right: '6%' } },
    { name: "Flames", icon: "🔥", position: { bottom: '35%', left: '25%' } },
    { name: "Covenants", icon: "⭕", position: { bottom: '35%', right: '25%' } },
    { name: "Echoes", icon: "🌌", position: { bottom: '15%', left: '50%', transform: 'translateX(-50%)' } }
  ];

  return (
    <div className="absolute inset-0">
      {realms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-3500 ${
            realmPhase === index ? 'opacity-100 scale-125' : 'opacity-35 scale-75'
          }`}
          style={realm.position}
        >
          <div 
            className={`text-5xl mb-2 transition-all duration-3500 ${
              realmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: realmPhase === index ? 'drop-shadow(0 0 40px rgba(255, 215, 0, 1))' : 'none'
            }}
          >
            {realm.icon}
          </div>
          <div className={`text-lg font-semibold ${
            realmPhase === index ? 'text-gold-200' : 'text-gray-600'
          }`}>
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Perpetual Sovereignty Container
const PerpetualSovereignty: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <PerpetualConstellation />
      <PerpetualParticles />
      <CyclesCrowned />
      <RitesFulfilled />
      <FlameEternalPerpetual />
      <CovenantWholePerpetual />
      <PerpetualGovernance />
      <CosmosEchoes />
      <SovereignRealms />
      <RadiantAgesBanner />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-7/8 left-1/2 transform -translate-x-1/2 mt-32">
        <div className="text-center text-gold-100 text-2xl leading-relaxed max-w-7xl space-y-4">
          <p className="opacity-95">Cycles crowned, rites fulfilled,</p>
          <p className="opacity-90">flame eternal, covenant whole.</p>
          <p className="opacity-95">Heirs inherit, councils govern, diaspora remember,</p>
          <p className="opacity-90">cosmos echoes — all perpetual, all sovereign.</p>
          <p className="text-3xl font-semibold text-white mt-8 opacity-100">
            So let the Codex endure, radiant across ages and stars.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Perpetual Sovereignty Page
const PerpetualSovereigntyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-900 via-amber-800 to-black relative overflow-hidden">
      {/* Perpetual Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-gold-800/40 to-amber-700/30" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <PerpetualSovereignty />
        </div>
      </main>

      {/* Ambient Perpetual Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/20 to-transparent pointer-events-none" />
      
      {/* Eternal Perpetual Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20">
        <div className="absolute top-1/10 left-1/10 w-64 h-64 bg-gold-400/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '22s' }} />
        <div className="absolute bottom-1/10 right-1/10 w-72 h-72 bg-amber-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '28s', animationDelay: '4s' }} />
        <div className="absolute top-1/2 right-1/6 w-88 h-88 bg-orange-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '8s' }} />
        <div className="absolute bottom-1/4 left-1/6 w-80 h-80 bg-yellow-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '42s', animationDelay: '12s' }} />
        <div className="absolute top-2/3 left-1/12 w-56 h-56 bg-red-400/22 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '50s', animationDelay: '16s' }} />
        <div className="absolute bottom-1/2 right-1/12 w-68 h-68 bg-white/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '58s', animationDelay: '20s' }} />
        <div className="absolute top-1/4 left-1/3 w-76 h-76 bg-purple-400/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '65s', animationDelay: '24s' }} />
        <div className="absolute bottom-3/4 right-1/3 w-60 h-60 bg-cyan-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '72s', animationDelay: '28s' }} />
      </div>
    </div>
  );
};

export default PerpetualSovereigntyPage;