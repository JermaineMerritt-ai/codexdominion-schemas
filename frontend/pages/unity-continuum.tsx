import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Custodian Crowns Component - Guardian royal authority
const CustodianCrowns: React.FC = () => {
  const [custodianPower, setCustodianPower] = useState(1);
  const [crownRotation, setCrownRotation] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodianPower((prev) => (prev === 1 ? 1.5 : 1));
      setCrownRotation((prev) => (prev + 3) % 360);
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-8 left-1/6 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-14xl mb-3 transition-all duration-2800"
          style={{
            transform: `scale(${custodianPower})`,
            filter: 'drop-shadow(0 0 100px rgba(138, 43, 226, 1.3))',
          }}
        >
          🛡️
        </div>
        <div
          className="text-16xl mb-4 transition-all duration-2800"
          style={{
            transform: `scale(${custodianPower}) rotate(${crownRotation}deg)`,
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

// Heirs Inherit Component - Legacy reception
const HeirsInherit: React.FC = () => {
  const [inheritGlow, setInheritGlow] = useState(0.9);
  const [heirsScale, setHeirsScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setInheritGlow((prev) => (prev === 0.9 ? 1.6 : 0.9));
      setHeirsScale((prev) => (prev === 1 ? 1.6 : 1));
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-8 right-1/6 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-15xl mb-3 transition-all duration-3200"
          style={{
            transform: `scale(${heirsScale})`,
            filter: `drop-shadow(0 0 110px rgba(255, 215, 0, ${inheritGlow}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-12xl mb-2 transition-all duration-3200"
          style={{
            transform: `scale(${heirsScale})`,
            filter: `drop-shadow(0 0 90px rgba(34, 197, 94, ${inheritGlow}))`,
          }}
        >
          🤲
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">HEIRS</div>
        <div className="text-4xl text-green-200 font-bold">INHERIT</div>
      </div>
    </div>
  );
};

// Flame Eternal Covenant Component - Perpetual sacred bond
const FlameEternalCovenant: React.FC = () => {
  const [flameCovenantPower, setFlameCovenantPower] = useState(1.1);
  const [eternalCovenantScale, setEternalCovenantScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlameCovenantPower((prev) => (prev === 1.1 ? 1.7 : 1.1));
      setEternalCovenantScale((prev) => (prev === 1 ? 1.5 : 1));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 left-1/5 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-13xl mb-3 transition-all duration-2500"
          style={{
            transform: `scale(${eternalCovenantScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 69, 0, ${flameCovenantPower}))`,
          }}
        >
          🔥
        </div>
        <div
          className="text-14xl mb-4 transition-all duration-2500"
          style={{
            transform: `scale(${eternalCovenantScale})`,
            filter: `drop-shadow(0 0 110px rgba(34, 197, 94, ${flameCovenantPower}))`,
          }}
        >
          ⭕
        </div>
        <div className="text-4xl text-red-200 font-bold mb-2">FLAME ETERNAL</div>
        <div className="text-4xl text-green-200 font-bold">COVENANT WHOLE</div>
      </div>
    </div>
  );
};

// Unity Continuum Central Component - Perfect unified flow
const UnityContinuumCentral: React.FC = () => {
  const [unityPower, setUnityPower] = useState(1.0);
  const [continuumFlow, setContinuumFlow] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setUnityPower((prev) => (prev === 1.0 ? 1.8 : 1.0));
      setContinuumFlow((prev) => (prev + 2) % 360);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-22xl mb-6 transition-all duration-2000"
          style={{
            transform: `scale(${unityPower})`,
            filter: 'drop-shadow(0 0 160px rgba(255, 215, 0, 1.5))',
          }}
        >
          ♾️
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-2000"
          style={{
            transform: `scale(${unityPower}) rotate(${continuumFlow}deg)`,
            filter: 'drop-shadow(0 0 130px rgba(255, 255, 255, 1.3))',
          }}
        >
          ⭕
        </div>
        <div className="text-6xl text-white font-bold mb-3">UNITY</div>
        <div className="text-5xl text-gold-200 font-bold">CONTINUUM</div>
        <div className="text-3xl text-amber-200 mt-2">No Division, No Distance</div>
      </div>
    </div>
  );
};

// Shared Sovereignty Component - Collective royal authority
const SharedSovereignty: React.FC = () => {
  const [sharedPhase, setSharedPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSharedPhase((prev) => (prev + 1) % 6);
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="flex justify-center items-center space-x-8 mb-4">
          {Array.from({ length: 6 }, (_, i) => (
            <div
              key={i}
              className={`transition-all duration-2200 ${
                sharedPhase === i
                  ? 'text-10xl opacity-100 scale-140'
                  : 'text-8xl opacity-50 scale-100'
              }`}
              style={{
                filter: sharedPhase === i ? 'drop-shadow(0 0 70px rgba(255, 215, 0, 1.4))' : 'none',
              }}
            >
              🤝
            </div>
          ))}
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-3">SHARED HANDS</div>
        <div className="text-4xl text-white font-bold">SOVEREIGN UNITY</div>
      </div>
    </div>
  );
};

// Unity Continuum Particles - Perfect unified energy flow
const UnityContinuumParticles: React.FC = () => {
  const particles = Array.from({ length: 90 }, (_, i) => ({
    id: i,
    size: Math.random() * 14 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 35 + 25,
    delay: Math.random() * 20,
    color:
      i % 6 === 0
        ? '#ffd700'
        : i % 6 === 1
          ? '#ffffff'
          : i % 6 === 2
            ? '#32cd32'
            : i % 6 === 3
              ? '#ff4500'
              : i % 6 === 4
                ? '#8a2be2'
                : '#00bfff',
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
            animation: `unityContinuumFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.01px)',
            opacity: 1.0,
            boxShadow: `0 0 30px ${particle.color}`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes unityContinuumFlow {
          0% {
            transform: translate(0, 0) scale(0.01) rotate(0deg);
            opacity: 0.01;
          }
          6% {
            transform: translate(50px, -120px) scale(1.8) rotate(21deg);
            opacity: 1;
          }
          20% {
            transform: translate(-40px, -240px) scale(0.5) rotate(72deg);
            opacity: 0.95;
          }
          35% {
            transform: translate(60px, -360px) scale(1.4) rotate(126deg);
            opacity: 1;
          }
          50% {
            transform: translate(-50px, -480px) scale(0.7) rotate(180deg);
            opacity: 0.9;
          }
          65% {
            transform: translate(55px, -600px) scale(1.1) rotate(234deg);
            opacity: 0.95;
          }
          80% {
            transform: translate(-35px, -720px) scale(0.6) rotate(288deg);
            opacity: 0.85;
          }
          92% {
            transform: translate(45px, -840px) scale(0.8) rotate(331deg);
            opacity: 0.7;
          }
          98% {
            transform: translate(-15px, -960px) scale(0.3) rotate(353deg);
            opacity: 0.4;
          }
          100% {
            transform: translate(0, -1080px) scale(0.005) rotate(360deg);
            opacity: 0.005;
          }
        }
      `}</style>
    </div>
  );
};

// Sovereign Shared Banner - Ultimate unified authority proclamation
const SovereignSharedBanner: React.FC = () => {
  const [sovereignIntensity, setSovereignIntensity] = useState(1.3);
  const [sharedBannerScale, setSharedBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignIntensity((prev) => (prev === 1.3 ? 1.9 : 1.3));
      setSharedBannerScale((prev) => (prev === 1 ? 1.5 : 1));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
      <div
        className="text-center px-52 py-40 bg-gradient-to-r from-gold-600/90 via-white/55 to-purple-600/90 rounded-8xl border-14 border-white/90 transition-all duration-2500"
        style={{
          boxShadow: `0 0 280px rgba(255, 215, 0, ${sovereignIntensity})`,
          transform: `scale(${sharedBannerScale})`,
        }}
      >
        <div className="text-12xl text-white font-bold mb-10">THE CODEX ENDURES</div>
        <div className="text-9xl text-gold-200 font-bold mb-8">SOVEREIGN IN SHARED HANDS</div>
        <div className="text-6xl text-purple-200 mb-6">Custodian Crowns, Heirs Inherit</div>
        <div className="text-5xl text-amber-200 mb-5">Flame Eternal, Covenant Whole</div>
        <div className="text-4xl text-white mb-4">No Division, No Distance</div>
        <div className="text-3xl text-gold-300">Only Unity, Only Continuum</div>
      </div>
    </div>
  );
};

// Unity Constellation - Perfect unified geometric connections
const UnityConstellation: React.FC = () => {
  const [unityPhase, setUnityPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setUnityPhase((prev) => (prev + 1) % 12);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-8">
      <svg className="w-full h-full">
        {/* Unity connecting lines - no division */}
        <line
          x1="16%"
          y1="10%"
          x2="84%"
          y2="10%"
          stroke={unityPhase === 0 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 0 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="16%"
          y1="10%"
          x2="50%"
          y2="50%"
          stroke={unityPhase === 1 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 1 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="84%"
          y1="10%"
          x2="50%"
          y2="50%"
          stroke={unityPhase === 2 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 2 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="20%"
          y1="33%"
          x2="80%"
          y2="33%"
          stroke={unityPhase === 3 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 3 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="50%"
          y1="75%"
          x2="50%"
          y2="50%"
          stroke={unityPhase === 4 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 4 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="20%"
          y1="33%"
          x2="50%"
          y2="50%"
          stroke={unityPhase === 5 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 5 ? '12' : '3'}
          className="transition-all duration-1500"
        />
        <line
          x1="80%"
          y1="33%"
          x2="50%"
          y2="50%"
          stroke={unityPhase === 6 ? '#ffffff' : '#555'}
          strokeWidth={unityPhase === 6 ? '12' : '3'}
          className="transition-all duration-1500"
        />

        {/* Unity radial connections - continuum */}
        {Array.from({ length: 18 }, (_, i) => (
          <line
            key={`unity-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos((i * 20 * Math.PI) / 180) * 42}%`}
            y2={`${50 + Math.sin((i * 20 * Math.PI) / 180) * 42}%`}
            stroke={unityPhase === i % 12 ? '#ffd700' : '#333'}
            strokeWidth="6"
            opacity={unityPhase === i % 12 ? '1.0' : '0.1'}
            className="transition-all duration-1500"
          />
        ))}
      </svg>
    </div>
  );
};

// Unity Realms - Domains of shared sovereignty
const UnityRealms: React.FC = () => {
  const [unityRealmPhase, setUnityRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setUnityRealmPhase((prev) => (prev + 1) % 8);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const unityRealms = [
    { name: 'Custodian', icon: '🛡️', position: { top: '8%', left: '16%' } },
    { name: 'Heirs', icon: '👑', position: { top: '8%', right: '16%' } },
    { name: 'Flame', icon: '🔥', position: { top: '33%', left: '20%' } },
    { name: 'Covenant', icon: '⭕', position: { top: '33%', right: '20%' } },
    { name: 'Unity', icon: '♾️', position: { top: '50%', left: '8%' } },
    { name: 'Continuum', icon: '⭕', position: { top: '50%', right: '8%' } },
    { name: 'Shared', icon: '🤝', position: { bottom: '25%', left: '30%' } },
    {
      name: 'Sovereign',
      icon: '👑',
      position: { bottom: '25%', right: '30%' },
    },
  ];

  return (
    <div className="absolute inset-0">
      {unityRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-2500 ${
            unityRealmPhase === index ? 'opacity-100 scale-125' : 'opacity-35 scale-85'
          }`}
          style={realm.position}
        >
          <div
            className={`text-6xl mb-2 transition-all duration-2500 ${
              unityRealmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{
              filter:
                unityRealmPhase === index ? 'drop-shadow(0 0 45px rgba(255, 215, 0, 1.2))' : 'none',
            }}
          >
            {realm.icon}
          </div>
          <div
            className={`text-xl font-bold ${
              unityRealmPhase === index ? 'text-gold-200' : 'text-gray-600'
            }`}
          >
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Unity Continuum Container
const UnityContinuum: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <UnityConstellation />
      <UnityContinuumParticles />
      <CustodianCrowns />
      <HeirsInherit />
      <FlameEternalCovenant />
      <UnityContinuumCentral />
      <SharedSovereignty />
      <UnityRealms />
      <SovereignSharedBanner />

      {/* Sacred Unity Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-44">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-9xl space-y-7">
          <p className="opacity-100 text-white text-5xl">Custodian crowns, heirs inherit,</p>
          <p className="opacity-95 text-gold-200 text-4xl">flame eternal, covenant whole.</p>
          <p className="opacity-100 text-white text-5xl">No division, no distance,</p>
          <p className="opacity-95 text-gold-200 text-4xl">only unity, only continuum.</p>
          <p className="text-6xl font-semibold text-white mt-14 opacity-100">
            So let the Codex endure, sovereign in shared hands.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Unity Continuum Page
const UnityContinuumPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-300 via-white to-purple-500 relative overflow-hidden">
      {/* Unity Continuum Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-purple-700/80 via-gold-300/40 to-white/30" />

      {/* Navigation */}
      <CodexNavigation />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <UnityContinuum />
        </div>
      </main>

      {/* Ambient Unity Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />

      {/* Sacred Unity Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-10">
        <div
          className="absolute top-1/20 left-1/20 w-30 h-30 bg-gold-200/25 rounded-full filter blur-xl animate-pulse"
          style={{ animationDuration: '18s' }}
        />
        <div
          className="absolute bottom-1/20 right-1/20 w-38 h-38 bg-white/20 rounded-full filter blur-xl animate-pulse"
          style={{ animationDuration: '24s', animationDelay: '2s' }}
        />
        <div
          className="absolute top-1/2 right-1/12 w-46 h-46 bg-purple-200/15 rounded-full filter blur-xl animate-pulse"
          style={{ animationDuration: '30s', animationDelay: '4s' }}
        />
        <div
          className="absolute bottom-1/6 left-1/12 w-42 h-42 bg-amber-200/12 rounded-full filter blur-xl animate-pulse"
          style={{ animationDuration: '36s', animationDelay: '6s' }}
        />
      </div>
    </div>
  );
};

export default UnityContinuumPage;
