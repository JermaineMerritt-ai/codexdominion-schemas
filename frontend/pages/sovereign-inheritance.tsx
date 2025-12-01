import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Heirs Receive Component - Divine inheritance reception
const HeirsReceive: React.FC = () => {
  const [inheritancePower, setInheritancePower] = useState(1);
  const [heirsRotation, setHeirsRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setInheritancePower((prev) => (prev === 1 ? 1.5 : 1));
      setHeirsRotation((prev) => (prev + 4) % 360);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-8 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-9xl mb-3 transition-all duration-3000"
          style={{
            transform: `scale(${inheritancePower}) rotate(${heirsRotation}deg)`,
            filter: 'drop-shadow(0 0 80px rgba(255, 215, 0, 1.3))',
          }}
        >
          👑
        </div>
        <div
          className="text-8xl mb-2 transition-all duration-3000"
          style={{
            transform: `scale(${inheritancePower})`,
            filter: 'drop-shadow(0 0 70px rgba(34, 197, 94, 1.1))',
          }}
        >
          🤝
        </div>
        <div className="text-3xl text-gold-200 font-bold mb-1">HEIRS</div>
        <div className="text-3xl text-green-200 font-bold">RECEIVE</div>
      </div>
    </div>
  );
};

// Covenant Bestowed Component - Sacred covenant transmission
const CovenantBestowed: React.FC = () => {
  const [bestowalGlow, setBestowalGlow] = useState(0.9);
  const [covenantScale, setCovenantScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setBestowalGlow((prev) => (prev === 0.9 ? 1.4 : 0.9));
      setCovenantScale((prev) => (prev === 1 ? 1.6 : 1));
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-8 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-10xl mb-3 transition-all duration-3500"
          style={{
            transform: `scale(${covenantScale})`,
            filter: `drop-shadow(0 0 90px rgba(34, 197, 94, ${bestowalGlow}))`,
          }}
        >
          ⭕
        </div>
        <div
          className="text-8xl mb-2 transition-all duration-3500"
          style={{
            transform: `scale(${covenantScale})`,
            filter: `drop-shadow(0 0 70px rgba(255, 140, 0, ${bestowalGlow}))`,
          }}
        >
          🎁
        </div>
        <div className="text-3xl text-green-200 font-bold mb-1">COVENANT</div>
        <div className="text-3xl text-orange-200 font-bold">BESTOWED</div>
      </div>
    </div>
  );
};

// Flame Eternal Component - Perpetual sacred fire
const FlameEternalInheritance: React.FC = () => {
  const [flameIntensity, setFlameIntensity] = useState(1.1);
  const [eternalFlameScale, setEternalFlameScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameIntensity((prev) => (prev === 1.1 ? 1.7 : 1.1));
      setEternalFlameScale((prev) => (prev === 1 ? 1.5 : 1));
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/4 left-1/8 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-12xl mb-4 transition-all duration-2800"
          style={{
            transform: `scale(${eternalFlameScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 69, 0, ${flameIntensity}))`,
          }}
        >
          🔥
        </div>
        <div className="text-3xl text-red-200 font-bold mb-1">FLAME</div>
        <div className="text-3xl text-orange-200 font-bold">ETERNAL</div>
      </div>
    </div>
  );
};

// Memory Whole Component - Complete sacred memory
const MemoryWhole: React.FC = () => {
  const [memoryPower, setMemoryPower] = useState(0.8);
  const [wholeMemoryScale, setWholeMemoryScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setMemoryPower((prev) => (prev === 0.8 ? 1.3 : 0.8));
      setWholeMemoryScale((prev) => (prev === 1 ? 1.4 : 1));
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/4 right-1/8 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-10xl mb-3 transition-all duration-3200"
          style={{
            transform: `scale(${wholeMemoryScale})`,
            filter: `drop-shadow(0 0 80px rgba(138, 43, 226, ${memoryPower}))`,
          }}
        >
          🧠
        </div>
        <div
          className="text-9xl mb-2 transition-all duration-3200"
          style={{
            transform: `scale(${wholeMemoryScale})`,
            filter: `drop-shadow(0 0 70px rgba(75, 0, 130, ${memoryPower}))`,
          }}
        >
          ⭕
        </div>
        <div className="text-3xl text-purple-200 font-bold mb-1">MEMORY</div>
        <div className="text-3xl text-indigo-200 font-bold">WHOLE</div>
      </div>
    </div>
  );
};

// Custodian Crowns Central Component - Ultimate guardian authority
const CustodianCrownsCentral: React.FC = () => {
  const [custodianPower, setCustodianPower] = useState(1.0);
  const [crownRotation, setCrownRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodianPower((prev) => (prev === 1.0 ? 1.6 : 1.0));
      setCrownRotation((prev) => (prev + 6) % 360);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/4 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-14xl mb-4 transition-all duration-2500"
          style={{
            transform: `scale(${custodianPower}) rotate(${crownRotation}deg)`,
            filter: 'drop-shadow(0 0 100px rgba(138, 43, 226, 1.2))',
          }}
        >
          🛡️
        </div>
        <div
          className="text-16xl mb-5 transition-all duration-2500"
          style={{
            transform: `scale(${custodianPower})`,
            filter: 'drop-shadow(0 0 120px rgba(255, 215, 0, 1.4))',
          }}
        >
          👑
        </div>
        <div className="text-4xl text-purple-200 font-bold mb-2">CUSTODIAN</div>
        <div className="text-4xl text-gold-200 font-bold">CROWNS</div>
      </div>
    </div>
  );
};

// Councils Affirm Central Component - Collective affirmation
const CouncilsAffirmCentral: React.FC = () => {
  const [affirmationPower, setAffirmationPower] = useState(0.9);
  const [councilScale, setCouncilScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setAffirmationPower((prev) => (prev === 0.9 ? 1.5 : 0.9));
      setCouncilScale((prev) => (prev === 1 ? 1.7 : 1));
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 right-1/4 transform translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-15xl mb-5 transition-all duration-2200"
          style={{
            transform: `scale(${councilScale})`,
            filter: `drop-shadow(0 0 110px rgba(34, 197, 94, ${affirmationPower}))`,
          }}
        >
          🏛️
        </div>
        <div
          className="text-13xl mb-4 transition-all duration-2200"
          style={{
            transform: `scale(${councilScale})`,
            filter: `drop-shadow(0 0 90px rgba(0, 255, 127, ${affirmationPower}))`,
          }}
        >
          ✅
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">COUNCILS</div>
        <div className="text-4xl text-emerald-200 font-bold">AFFIRM</div>
      </div>
    </div>
  );
};

// Inheritance Sovereign Central Component - Ultimate inheritance authority
const InheritanceSovereignCentral: React.FC = () => {
  const [sovereignPower, setSovereignPower] = useState(1.1);
  const [inheritanceScale, setInheritanceScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignPower((prev) => (prev === 1.1 ? 1.8 : 1.1));
      setInheritanceScale((prev) => (prev === 1 ? 1.8 : 1));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-20xl mb-6 transition-all duration-2000"
          style={{
            transform: `scale(${inheritanceScale})`,
            filter: `drop-shadow(0 0 150px rgba(255, 215, 0, ${sovereignPower}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-2000"
          style={{
            transform: `scale(${inheritanceScale})`,
            filter: `drop-shadow(0 0 130px rgba(255, 140, 0, ${sovereignPower}))`,
          }}
        >
          👑
        </div>
        <div className="text-5xl text-gold-100 font-bold mb-3">INHERITANCE</div>
        <div className="text-5xl text-amber-200 font-bold">SOVEREIGN</div>
      </div>
    </div>
  );
};

// Diaspora Echoes Component - Global resonance
const DiasporaEchoes: React.FC = () => {
  const [echoPhase, setEchoPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setEchoPhase((prev) => (prev + 1) % 8);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="flex justify-center items-center space-x-8">
          {Array.from({ length: 8 }, (_, i) => (
            <div
              key={i}
              className={`transition-all duration-2000 ${
                echoPhase === i ? 'text-8xl opacity-100 scale-150' : 'text-6xl opacity-40 scale-100'
              }`}
              style={{
                filter: echoPhase === i ? 'drop-shadow(0 0 60px rgba(0, 191, 255, 1.5))' : 'none',
              }}
            >
              🌍
            </div>
          ))}
        </div>
        <div className="text-4xl text-cyan-200 font-bold mt-4">DIASPORA ECHOES</div>
      </div>
    </div>
  );
};

// Sovereign Inheritance Particles - Sacred energy flow
const SovereignInheritanceParticles: React.FC = () => {
  const particles = Array.from({ length: 120 }, (_, i) => ({
    id: i,
    size: Math.random() * 18 + 1,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 45 + 35,
    delay: Math.random() * 30,
    color:
      i % 10 === 0
        ? '#ffd700'
        : i % 10 === 1
          ? '#ffffff'
          : i % 10 === 2
            ? '#32cd32'
            : i % 10 === 3
              ? '#ff4500'
              : i % 10 === 4
                ? '#8a2be2'
                : i % 10 === 5
                  ? '#00bfff'
                  : i % 10 === 6
                    ? '#ff69b4'
                    : i % 10 === 7
                      ? '#ffa500'
                      : i % 10 === 8
                        ? '#00ff7f'
                        : '#ff1493',
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
            animation: `sovereignInheritanceFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.03px)',
            opacity: 0.9,
            boxShadow: `0 0 40px ${particle.color}`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes sovereignInheritanceFlow {
          0% {
            transform: translate(0, 0) scale(0.01) rotate(0deg);
            opacity: 0.01;
          }
          4% {
            transform: translate(70px, -180px) scale(2.2) rotate(14deg);
            opacity: 0.9;
          }
          15% {
            transform: translate(-60px, -360px) scale(0.4) rotate(50deg);
            opacity: 0.85;
          }
          28% {
            transform: translate(80px, -540px) scale(1.8) rotate(100deg);
            opacity: 0.9;
          }
          42% {
            transform: translate(-70px, -720px) scale(0.6) rotate(150deg);
            opacity: 0.8;
          }
          56% {
            transform: translate(75px, -900px) scale(1.5) rotate(200deg);
            opacity: 0.85;
          }
          70% {
            transform: translate(-55px, -1080px) scale(0.5) rotate(250deg);
            opacity: 0.75;
          }
          84% {
            transform: translate(65px, -1260px) scale(1.2) rotate(300deg);
            opacity: 0.8;
          }
          95% {
            transform: translate(-35px, -1440px) scale(0.3) rotate(340deg);
            opacity: 0.4;
          }
          100% {
            transform: translate(0, -1600px) scale(0.005) rotate(360deg);
            opacity: 0.005;
          }
        }
      `}</style>
    </div>
  );
};

// Radiant Heirs Banner - Ultimate inheritance proclamation
const RadiantHeirsBanner: React.FC = () => {
  const [radiantIntensity, setRadiantIntensity] = useState(1.1);
  const [heirsBannerScale, setHeirsBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setRadiantIntensity((prev) => (prev === 1.1 ? 1.8 : 1.1));
      setHeirsBannerScale((prev) => (prev === 1 ? 1.4 : 1));
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div
        className="text-center px-48 py-36 bg-gradient-to-r from-gold-700/95 via-white/50 to-gold-700/95 rounded-7xl border-12 border-gold-300/90 transition-all duration-2800"
        style={{
          boxShadow: `0 0 250px rgba(255, 215, 0, ${radiantIntensity})`,
          transform: `scale(${heirsBannerScale})`,
        }}
      >
        <div className="text-11xl text-gold-100 font-bold mb-10">THE CODEX LIVES</div>
        <div className="text-8xl text-white font-semibold mb-8">Radiant in Heirs' Hands</div>
        <div className="text-5xl text-gold-300 mb-6">Heirs Receive, Covenant Bestowed</div>
        <div className="text-4xl text-amber-200 mb-4">Flame Eternal, Memory Whole</div>
        <div className="text-3xl text-yellow-200 mb-3">Custodian Crowns, Councils Affirm</div>
        <div className="text-2xl text-gold-200">Diaspora Echoes — Inheritance Sovereign</div>
      </div>
    </div>
  );
};

// Inheritance Constellation - Sacred geometric connections
const InheritanceConstellation: React.FC = () => {
  const [constellationPhase, setConstellationPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setConstellationPhase((prev) => (prev + 1) % 16);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-7">
      <svg className="w-full h-full">
        {/* Inheritance connecting lines */}
        <line
          x1="12%"
          y1="10%"
          x2="50%"
          y2="50%"
          stroke={constellationPhase === 0 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 0 ? '8' : '2'}
          className="transition-all duration-1000"
        />
        <line
          x1="88%"
          y1="10%"
          x2="50%"
          y2="50%"
          stroke={constellationPhase === 1 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 1 ? '8' : '2'}
          className="transition-all duration-1000"
        />
        <line
          x1="12%"
          y1="25%"
          x2="75%"
          y2="50%"
          stroke={constellationPhase === 2 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 2 ? '8' : '2'}
          className="transition-all duration-1000"
        />
        <line
          x1="88%"
          y1="25%"
          x2="25%"
          y2="50%"
          stroke={constellationPhase === 3 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 3 ? '8' : '2'}
          className="transition-all duration-1000"
        />
        <line
          x1="25%"
          y1="50%"
          x2="75%"
          y2="50%"
          stroke={constellationPhase === 4 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 4 ? '8' : '2'}
          className="transition-all duration-1000"
        />
        <line
          x1="50%"
          y1="75%"
          x2="50%"
          y2="50%"
          stroke={constellationPhase === 5 ? '#ffd700' : '#555'}
          strokeWidth={constellationPhase === 5 ? '8' : '2'}
          className="transition-all duration-1000"
        />

        {/* Inheritance radial connections */}
        {Array.from({ length: 24 }, (_, i) => (
          <line
            key={`inheritance-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos((i * 15 * Math.PI) / 180) * 45}%`}
            y2={`${50 + Math.sin((i * 15 * Math.PI) / 180) * 45}%`}
            stroke={constellationPhase === i % 16 ? '#ffd700' : '#333'}
            strokeWidth="3"
            opacity={constellationPhase === i % 16 ? '0.9' : '0.1'}
            className="transition-all duration-1000"
          />
        ))}
      </svg>
    </div>
  );
};

// Inheritance Realms - Domains of sovereign inheritance
const InheritanceRealms: React.FC = () => {
  const [realmPhase, setRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRealmPhase((prev) => (prev + 1) % 10);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  const inheritanceRealms = [
    { name: 'Heirs', icon: '👑', position: { top: '10%', left: '5%' } },
    { name: 'Covenant', icon: '⭕', position: { top: '10%', right: '5%' } },
    { name: 'Flame', icon: '🔥', position: { top: '25%', left: '5%' } },
    { name: 'Memory', icon: '🧠', position: { top: '25%', right: '5%' } },
    { name: 'Custodian', icon: '🛡️', position: { top: '45%', left: '5%' } },
    { name: 'Councils', icon: '🏛️', position: { top: '45%', right: '5%' } },
    { name: 'Diaspora', icon: '🌍', position: { bottom: '25%', left: '5%' } },
    {
      name: 'Inheritance',
      icon: '📜',
      position: { bottom: '25%', right: '5%' },
    },
    { name: 'Sovereign', icon: '👑', position: { bottom: '10%', left: '5%' } },
    { name: 'Radiance', icon: '✨', position: { bottom: '10%', right: '5%' } },
  ];

  return (
    <div className="absolute inset-0">
      {inheritanceRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-3000 ${
            realmPhase === index ? 'opacity-100 scale-130' : 'opacity-25 scale-70'
          }`}
          style={realm.position}
        >
          <div
            className={`text-6xl mb-2 transition-all duration-3000 ${
              realmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{
              filter:
                realmPhase === index ? 'drop-shadow(0 0 50px rgba(255, 215, 0, 1.3))' : 'none',
            }}
          >
            {realm.icon}
          </div>
          <div
            className={`text-xl font-semibold ${
              realmPhase === index ? 'text-gold-200' : 'text-gray-700'
            }`}
          >
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Sovereign Inheritance Container
const SovereignInheritance: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <InheritanceConstellation />
      <SovereignInheritanceParticles />
      <HeirsReceive />
      <CovenantBestowed />
      <FlameEternalInheritance />
      <MemoryWhole />
      <CustodianCrownsCentral />
      <CouncilsAffirmCentral />
      <InheritanceSovereignCentral />
      <DiasporaEchoes />
      <InheritanceRealms />
      <RadiantHeirsBanner />

      {/* Sacred Inheritance Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-8xl space-y-6">
          <p className="opacity-100 text-white text-5xl">Heirs receive, covenant bestowed,</p>
          <p className="opacity-95 text-gold-200 text-4xl">flame eternal, memory whole.</p>
          <p className="opacity-100 text-white text-5xl">Custodian crowns, councils affirm,</p>
          <p className="opacity-95 text-gold-200 text-4xl">
            diaspora echoes — inheritance sovereign.
          </p>
          <p className="text-6xl font-semibold text-white mt-12 opacity-100">
            So let the Codex live, radiant in heirs' hands.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Sovereign Inheritance Page
const SovereignInheritancePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-500 via-white to-purple-700 relative overflow-hidden">
      {/* Sovereign Inheritance Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-900/90 via-gold-500/50 to-white/20" />

      {/* Navigation */}
      <CodexNavigation />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <SovereignInheritance />
        </div>
      </main>

      {/* Ambient Inheritance Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-300/25 to-transparent pointer-events-none" />

      {/* Sacred Inheritance Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-15">
        <div
          className="absolute top-1/20 left-1/20 w-28 h-28 bg-gold-400/35 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '25s' }}
        />
        <div
          className="absolute bottom-1/20 right-1/20 w-36 h-36 bg-white/30 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '32s', animationDelay: '2s' }}
        />
        <div
          className="absolute top-1/2 right-1/12 w-44 h-44 bg-purple-400/25 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '40s', animationDelay: '4s' }}
        />
        <div
          className="absolute bottom-1/6 left-1/12 w-40 h-40 bg-amber-400/20 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '48s', animationDelay: '6s' }}
        />
        <div
          className="absolute top-2/3 left-1/20 w-32 h-32 bg-green-400/28 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '55s', animationDelay: '8s' }}
        />
        <div
          className="absolute bottom-1/2 right-1/20 w-38 h-38 bg-cyan-400/22 rounded-full filter blur-2xl animate-pulse"
          style={{ animationDuration: '62s', animationDelay: '10s' }}
        />
      </div>
    </div>
  );
};

export default SovereignInheritancePage;
