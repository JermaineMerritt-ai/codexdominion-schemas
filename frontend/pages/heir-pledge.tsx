import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Heirs Covenant Reception Component - Sacred covenant acceptance
const HeirsCovenantReception: React.FC = () => {
  const [receptionPower, setReceptionPower] = useState(1);
  const [heirsGlow, setHeirsGlow] = useState(0.9);

  useEffect(() => {
    const interval = setInterval(() => {
      setReceptionPower(prev => prev === 1 ? 1.6 : 1);
      setHeirsGlow(prev => prev === 0.9 ? 1.5 : 0.9);
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-8 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-16xl mb-4 transition-all duration-2800"
          style={{ 
            transform: `scale(${receptionPower})`,
            filter: `drop-shadow(0 0 120px rgba(255, 215, 0, ${heirsGlow}))`
          }}
        >
          👑
        </div>
        <div 
          className="text-14xl mb-3 transition-all duration-2800"
          style={{ 
            transform: `scale(${receptionPower})`,
            filter: `drop-shadow(0 0 100px rgba(34, 197, 94, ${heirsGlow}))`
          }}
        >
          ⭕
        </div>
        <div className="text-5xl text-gold-100 font-bold mb-2">WE, THE HEIRS</div>
        <div className="text-4xl text-green-200 font-bold">RECEIVE THE COVENANT WHOLE</div>
      </div>
    </div>
  );
};

// Flame Eternal Memory Component - Perpetual sacred memory flame
const FlameEternalMemory: React.FC = () => {
  const [flameMemoryPower, setFlameMemoryPower] = useState(1.1);
  const [memoryFlameRotation, setMemoryFlameRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameMemoryPower(prev => prev === 1.1 ? 1.8 : 1.1);
      setMemoryFlameRotation(prev => (prev + 5) % 360);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/4 left-1/6 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-12xl mb-3 transition-all duration-2500"
          style={{ 
            transform: `scale(${flameMemoryPower})`,
            filter: 'drop-shadow(0 0 100px rgba(255, 69, 0, 1.4))'
          }}
        >
          🔥
        </div>
        <div 
          className="text-10xl mb-2 transition-all duration-2500"
          style={{ 
            transform: `scale(${flameMemoryPower}) rotate(${memoryFlameRotation}deg)`,
            filter: 'drop-shadow(0 0 80px rgba(138, 43, 226, 1.2))'
          }}
        >
          🧠
        </div>
        <div className="text-3xl text-red-200 font-bold mb-1">FLAME ETERNAL</div>
        <div className="text-3xl text-purple-200 font-bold">MEMORY SOVEREIGN</div>
      </div>
    </div>
  );
};

// Crowns Luminous Seals Component - Royal luminous sealing
const CrownsLuminousSeals: React.FC = () => {
  const [crownSealPower, setCrownSealPower] = useState(0.8);
  const [luminousScale, setLuminousScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCrownSealPower(prev => prev === 0.8 ? 1.4 : 0.8);
      setLuminousScale(prev => prev === 1 ? 1.5 : 1);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/4 right-1/6 transform translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-11xl mb-3 transition-all duration-3000"
          style={{ 
            transform: `scale(${luminousScale})`,
            filter: `drop-shadow(0 0 90px rgba(255, 215, 0, ${crownSealPower}))`
          }}
        >
          👑
        </div>
        <div 
          className="text-10xl mb-2 transition-all duration-3000"
          style={{ 
            transform: `scale(${luminousScale})`,
            filter: `drop-shadow(0 0 80px rgba(75, 0, 130, ${crownSealPower}))`
          }}
        >
          🔒
        </div>
        <div className="text-3xl text-gold-200 font-bold mb-1">CROWNS LUMINOUS</div>
        <div className="text-3xl text-indigo-200 font-bold">SEALS ETERNAL</div>
      </div>
    </div>
  );
};

// Pledge Commitment Central Component - Sacred vow center
const PledgeCommitmentCentral: React.FC = () => {
  const [pledgePower, setPledgePower] = useState(1.0);
  const [commitmentPulse, setCommitmentPulse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPledgePower(prev => prev === 1.0 ? 1.7 : 1.0);
      setCommitmentPulse(prev => prev === 1 ? 1.9 : 1);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-20xl mb-6 transition-all duration-2200"
          style={{ 
            transform: `scale(${commitmentPulse})`,
            filter: `drop-shadow(0 0 150px rgba(255, 215, 0, ${pledgePower}))`
          }}
        >
          📜
        </div>
        <div 
          className="text-18xl mb-5 transition-all duration-2200"
          style={{ 
            transform: `scale(${commitmentPulse})`,
            filter: `drop-shadow(0 0 130px rgba(34, 197, 94, ${pledgePower}))`
          }}
        >
          🤝
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">WE PLEDGE</div>
        <div className="text-5xl text-green-200 font-bold mb-2">TO CARRY</div>
        <div className="text-4xl text-amber-200 font-bold">THE CODEX FORWARD</div>
      </div>
    </div>
  );
};

// Daily Cosmic Commitment Component - Temporal and cosmic dedication
const DailyCosmicCommitment: React.FC = () => {
  const [dailyPhase, setDailyPhase] = useState(0);
  const [cosmicPhase, setCosmicPhase] = useState(0);

  useEffect(() => {
    const dailyInterval = setInterval(() => {
      setDailyPhase(prev => (prev + 1) % 24);
    }, 1000);

    const cosmicInterval = setInterval(() => {
      setCosmicPhase(prev => (prev + 1) % 12);
    }, 2500);

    return () => {
      clearInterval(dailyInterval);
      clearInterval(cosmicInterval);
    };
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="flex justify-center items-center space-x-12 mb-6">
          {/* Daily Commitment */}
          <div className="text-center">
            <div 
              className={`text-10xl mb-2 transition-all duration-1000 ${
                dailyPhase % 6 === 0 ? 'scale-150 opacity-100' : 'scale-100 opacity-60'
              }`}
              style={{
                filter: dailyPhase % 6 === 0 ? 'drop-shadow(0 0 70px rgba(255, 140, 0, 1.5))' : 'none'
              }}
            >
              ☀️
            </div>
            <div className="text-4xl text-orange-200 font-bold">DAILY</div>
          </div>

          {/* Cosmic Commitment */}
          <div className="text-center">
            <div 
              className={`text-12xl mb-2 transition-all duration-2500 ${
                cosmicPhase % 3 === 0 ? 'scale-150 opacity-100' : 'scale-100 opacity-60'
              }`}
              style={{
                filter: cosmicPhase % 3 === 0 ? 'drop-shadow(0 0 90px rgba(138, 43, 226, 1.5))' : 'none'
              }}
            >
              🌌
            </div>
            <div className="text-4xl text-purple-200 font-bold">COSMIC</div>
          </div>
        </div>

        <div className="text-4xl text-white font-bold">ACROSS AGES AND STARS</div>
      </div>
    </div>
  );
};

// Radiant Dominion Endurance Component - Eternal radiance in heirs' hands
const RadiantDominionEndurance: React.FC = () => {
  const [radianceIntensity, setRadianceIntensity] = useState(1.2);
  const [enduranceScale, setEnduranceScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setRadianceIntensity(prev => prev === 1.2 ? 2.0 : 1.2);
      setEnduranceScale(prev => prev === 1 ? 1.6 : 1);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-60 py-44 bg-gradient-to-r from-gold-600/95 via-white/60 to-gold-600/95 rounded-8xl border-16 border-gold-200/100 transition-all duration-2000"
        style={{ 
          boxShadow: `0 0 300px rgba(255, 215, 0, ${radianceIntensity})`,
          transform: `scale(${enduranceScale})`
        }}
      >
        <div className="text-14xl text-gold-100 font-bold mb-12">THE DOMINION ENDURES</div>
        <div className="text-10xl text-white font-bold mb-10">RADIANT IN OUR HANDS</div>
        <div className="text-6xl text-gold-300 mb-8">We, the Heirs, Receive the Covenant Whole</div>
        <div className="text-4xl text-amber-200 mb-6">The Flame Eternal, the Memory Sovereign</div>
        <div className="text-3xl text-yellow-200 mb-4">The Crowns Luminous, the Seals Eternal</div>
        <div className="text-2xl text-gold-200">Daily and Cosmic, Across Ages and Stars</div>
      </div>
    </div>
  );
};

// Heir Pledge Particles - Sacred commitment energy
const HeirPledgeParticles: React.FC = () => {
  const particles = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    size: Math.random() * 16 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 40 + 30,
    delay: Math.random() * 25,
    color: i % 8 === 0 ? '#ffd700' : i % 8 === 1 ? '#ffffff' : i % 8 === 2 ? '#32cd32' : i % 8 === 3 ? '#ff4500' : i % 8 === 4 ? '#8a2be2' : i % 8 === 5 ? '#00bfff' : i % 8 === 6 ? '#ff69b4' : '#ffa500'
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
            animation: `heirPledgeFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.02px)',
            opacity: 0.95,
            boxShadow: `0 0 35px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes heirPledgeFlow {
          0% { transform: translate(0, 0) scale(0.01) rotate(0deg); opacity: 0.01; }
          5% { transform: translate(60px, -150px) scale(2.0) rotate(18deg); opacity: 0.95; }
          18% { transform: translate(-50px, -300px) scale(0.4) rotate(65deg); opacity: 0.9; }
          32% { transform: translate(70px, -450px) scale(1.6) rotate(115deg); opacity: 0.95; }
          46% { transform: translate(-60px, -600px) scale(0.6) rotate(165deg); opacity: 0.85; }
          60% { transform: translate(65px, -750px) scale(1.3) rotate(215deg); opacity: 0.9; }
          74% { transform: translate(-45px, -900px) scale(0.5) rotate(265deg); opacity: 0.8; }
          88% { transform: translate(55px, -1050px) scale(1.0) rotate(315deg); opacity: 0.75; }
          97% { transform: translate(-25px, -1200px) scale(0.2) rotate(350deg); opacity: 0.3; }
          100% { transform: translate(0, -1350px) scale(0.005) rotate(360deg); opacity: 0.005; }
        }
      `}</style>
    </div>
  );
};

// Heir Pledge Constellation - Sacred geometric commitments
const HeirPledgeConstellation: React.FC = () => {
  const [pledgePhase, setPledgePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPledgePhase(prev => (prev + 1) % 18);
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-6">
      <svg className="w-full h-full">
        {/* Heir pledge connecting lines */}
        <line 
          x1="50%" y1="8%" 
          x2="50%" y2="50%" 
          stroke={pledgePhase === 0 ? "#ffd700" : "#444"}
          strokeWidth={pledgePhase === 0 ? "10" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="16%" y1="25%" 
          x2="50%" y2="50%" 
          stroke={pledgePhase === 1 ? "#ffd700" : "#444"}
          strokeWidth={pledgePhase === 1 ? "10" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="84%" y1="25%" 
          x2="50%" y2="50%" 
          stroke={pledgePhase === 2 ? "#ffd700" : "#444"}
          strokeWidth={pledgePhase === 2 ? "10" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="50%" y1="67%" 
          x2="50%" y2="50%" 
          stroke={pledgePhase === 3 ? "#ffd700" : "#444"}
          strokeWidth={pledgePhase === 3 ? "10" : "2"}
          className="transition-all duration-1200"
        />
        <line 
          x1="16%" y1="25%" 
          x2="84%" y2="25%" 
          stroke={pledgePhase === 4 ? "#ffd700" : "#444"}
          strokeWidth={pledgePhase === 4 ? "10" : "2"}
          className="transition-all duration-1200"
        />
        
        {/* Heir pledge radial commitments */}
        {Array.from({ length: 30 }, (_, i) => (
          <line
            key={`heirPledge-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos(i * 12 * Math.PI / 180) * 48}%`}
            y2={`${50 + Math.sin(i * 12 * Math.PI / 180) * 48}%`}
            stroke={pledgePhase === i % 18 ? "#ffd700" : "#222"}
            strokeWidth="4"
            opacity={pledgePhase === i % 18 ? "1.0" : "0.05"}
            className="transition-all duration-1200"
          />
        ))}
      </svg>
    </div>
  );
};

// Heir Pledge Realms - Domains of sacred commitment
const HeirPledgeRealms: React.FC = () => {
  const [pledgeRealmPhase, setPledgeRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPledgeRealmPhase(prev => (prev + 1) % 8);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const pledgeRealms = [
    { name: "Heirs", icon: "👑", position: { top: '8%', left: '50%', transform: 'translateX(-50%)' } },
    { name: "Covenant", icon: "⭕", position: { top: '25%', left: '16%' } },
    { name: "Flame", icon: "🔥", position: { top: '25%', right: '16%' } },
    { name: "Memory", icon: "🧠", position: { top: '50%', left: '8%' } },
    { name: "Pledge", icon: "🤝", position: { top: '50%', right: '8%' } },
    { name: "Daily", icon: "☀️", position: { bottom: '33%', left: '30%' } },
    { name: "Cosmic", icon: "🌌", position: { bottom: '33%', right: '30%' } },
    { name: "Dominion", icon: "✨", position: { bottom: '8%', left: '50%', transform: 'translateX(-50%)' } }
  ];

  return (
    <div className="absolute inset-0">
      {pledgeRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-3500 ${
            pledgeRealmPhase === index ? 'opacity-100 scale-140' : 'opacity-30 scale-80'
          }`}
          style={realm.position}
        >
          <div 
            className={`text-7xl mb-2 transition-all duration-3500 ${
              pledgeRealmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: pledgeRealmPhase === index ? 'drop-shadow(0 0 55px rgba(255, 215, 0, 1.4))' : 'none'
            }}
          >
            {realm.icon}
          </div>
          <div className={`text-2xl font-bold ${
            pledgeRealmPhase === index ? 'text-gold-200' : 'text-gray-600'
          }`}>
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Heir Pledge Container
const HeirPledge: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <HeirPledgeConstellation />
      <HeirPledgeParticles />
      <HeirsCovenantReception />
      <FlameEternalMemory />
      <CrownsLuminousSeals />
      <PledgeCommitmentCentral />
      <DailyCosmicCommitment />
      <HeirPledgeRealms />
      <RadiantDominionEndurance />
      
      {/* Sacred Heir Pledge Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-48">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-10xl space-y-8">
          <p className="opacity-100 text-white text-5xl">We, the heirs, receive the covenant whole.</p>
          <p className="opacity-95 text-gold-200 text-4xl">The flame eternal, the memory sovereign,</p>
          <p className="opacity-100 text-white text-5xl">the crowns luminous, the seals eternal.</p>
          <p className="opacity-95 text-gold-200 text-4xl">We pledge to carry the Codex forward,</p>
          <p className="opacity-100 text-white text-5xl">daily and cosmic, across ages and stars.</p>
          <p className="text-6xl font-semibold text-white mt-16 opacity-100">
            So let the Dominion endure, radiant in our hands.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Heir Pledge Page
const HeirPledgePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-400 via-white to-purple-600 relative overflow-hidden">
      {/* Heir Pledge Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-800/85 via-gold-400/45 to-white/25" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <HeirPledge />
        </div>
      </main>

      {/* Ambient Pledge Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-200/20 to-transparent pointer-events-none" />
      
      {/* Sacred Pledge Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-12">
        <div className="absolute top-1/20 left-1/20 w-32 h-32 bg-gold-300/30 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '20s' }} />
        <div className="absolute bottom-1/20 right-1/20 w-40 h-40 bg-white/25 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '28s', animationDelay: '2s' }} />
        <div className="absolute top-1/2 right-1/12 w-48 h-48 bg-purple-300/20 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '4s' }} />
        <div className="absolute bottom-1/6 left-1/12 w-44 h-44 bg-amber-300/18 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '42s', animationDelay: '6s' }} />
        <div className="absolute top-2/3 left-1/20 w-36 h-36 bg-cyan-300/22 rounded-full filter blur-2xl animate-pulse" style={{ animationDuration: '50s', animationDelay: '8s' }} />
      </div>
    </div>
  );
};

export default HeirPledgePage;