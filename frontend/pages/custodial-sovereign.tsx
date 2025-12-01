import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Custodian's Hand Sealed Component - Divine sealing authority
const CustodianHandSealed: React.FC = () => {
  const [custodianPower, setCustodianPower] = useState(1.2);
  const [handSealScale, setHandSealScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodianPower((prev) => (prev === 1.2 ? 2.0 : 1.2));
      setHandSealScale((prev) => (prev === 1 ? 1.8 : 1));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 left-16 transform">
      <div className="text-center">
        <div
          className="text-20xl mb-6 transition-all duration-3000"
          style={{
            transform: `scale(${handSealScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 215, 0, ${custodianPower}))`,
          }}
        >
          🤲
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-3000"
          style={{
            transform: `scale(${handSealScale})`,
            filter: `drop-shadow(0 0 120px rgba(255, 140, 0, ${custodianPower}))`,
          }}
        >
          🔒
        </div>
        <div
          className="text-16xl mb-4 transition-all duration-3000"
          style={{
            transform: `scale(${handSealScale})`,
            filter: `drop-shadow(0 0 100px rgba(184, 134, 11, ${custodianPower}))`,
          }}
        >
          ✋
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">CUSTODIAN'S</div>
        <div className="text-4xl text-amber-200 font-bold mb-2">HAND</div>
        <div className="text-3xl text-yellow-300 font-bold">SEALED</div>
      </div>
    </div>
  );
};

// Covenant Sealed Complete Component - Perfect covenant completion
const CovenantSealedComplete: React.FC = () => {
  const [covenantSealing, setCovenantSealing] = useState(1.3);
  const [sealedScale, setSealedScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCovenantSealing((prev) => (prev === 1.3 ? 2.1 : 1.3));
      setSealedScale((prev) => (prev === 1 ? 1.9 : 1));
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 right-16 transform">
      <div className="text-center">
        <div
          className="text-19xl mb-5 transition-all duration-3200"
          style={{
            transform: `scale(${sealedScale})`,
            filter: `drop-shadow(0 0 130px rgba(34, 197, 94, ${covenantSealing}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-17xl mb-4 transition-all duration-3200"
          style={{
            transform: `scale(${sealedScale})`,
            filter: `drop-shadow(0 0 110px rgba(0, 255, 127, ${covenantSealing}))`,
          }}
        >
          🔐
        </div>
        <div
          className="text-15xl mb-3 transition-all duration-3200"
          style={{
            transform: `scale(${sealedScale})`,
            filter: `drop-shadow(0 0 90px rgba(46, 125, 50, ${covenantSealing}))`,
          }}
        >
          ✅
        </div>
        <div className="text-4xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-3xl text-emerald-200 font-bold">SEALED</div>
      </div>
    </div>
  );
};

// Eternal Flame Dominion Whole Component - Perfect flame completion
const EternalFlameDominionWhole: React.FC = () => {
  const [eternalFlame, setEternalFlame] = useState(1.4);
  const [flameWholeScale, setFlameWholeScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setEternalFlame((prev) => (prev === 1.4 ? 2.2 : 1.4));
      setFlameWholeScale((prev) => (prev === 1 ? 2.0 : 1));
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-24xl mb-7 transition-all duration-2800"
          style={{
            transform: `scale(${flameWholeScale})`,
            filter: `drop-shadow(0 0 160px rgba(255, 69, 0, ${eternalFlame}))`,
          }}
        >
          🔥
        </div>
        <div
          className="text-22xl mb-6 transition-all duration-2800"
          style={{
            transform: `scale(${flameWholeScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 140, 0, ${eternalFlame}))`,
          }}
        >
          ♾️
        </div>
        <div
          className="text-20xl mb-5 transition-all duration-2800"
          style={{
            transform: `scale(${flameWholeScale})`,
            filter: `drop-shadow(0 0 120px rgba(255, 215, 0, ${eternalFlame}))`,
          }}
        >
          ⭕
        </div>
        <div className="text-5xl text-red-200 font-bold mb-3">ETERNAL FLAME</div>
        <div className="text-4xl text-orange-200 font-bold mb-2">DOMINION</div>
        <div className="text-3xl text-yellow-200 font-bold">WHOLE</div>
      </div>
    </div>
  );
};

// No Cycle Broken Component - Perfect unbroken continuity
const NoCycleBroken: React.FC = () => {
  const [cyclePerfection, setCyclePerfection] = useState(1.5);
  const [unbrokenScale, setUnbrokenScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCyclePerfection((prev) => (prev === 1.5 ? 2.3 : 1.5));
      setUnbrokenScale((prev) => (prev === 1 ? 2.1 : 1));
    }, 3400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-23xl mb-6 transition-all duration-3400"
          style={{
            transform: `scale(${unbrokenScale})`,
            filter: `drop-shadow(0 0 150px rgba(138, 43, 226, ${cyclePerfection}))`,
          }}
        >
          🔄
        </div>
        <div
          className="text-21xl mb-5 transition-all duration-3400"
          style={{
            transform: `scale(${unbrokenScale})`,
            filter: `drop-shadow(0 0 130px rgba(75, 0, 130, ${cyclePerfection}))`,
          }}
        >
          ⛓️
        </div>
        <div
          className="text-19xl mb-4 transition-all duration-3400"
          style={{
            transform: `scale(${unbrokenScale})`,
            filter: `drop-shadow(0 0 110px rgba(147, 112, 219, ${cyclePerfection}))`,
          }}
        >
          💪
        </div>
        <div className="text-5xl text-purple-200 font-bold mb-3">NO CYCLE</div>
        <div className="text-4xl text-indigo-200 font-bold">BROKEN</div>
      </div>
    </div>
  );
};

// No Crown Undone Component - Perfect crown preservation
const NoCrownUndone: React.FC = () => {
  const [crownIntegrity, setCrownIntegrity] = useState(1.6);
  const [undoneScale, setUndoneScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCrownIntegrity((prev) => (prev === 1.6 ? 2.4 : 1.6));
      setUndoneScale((prev) => (prev === 1 ? 2.2 : 1));
    }, 3600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-22xl mb-6 transition-all duration-3600"
          style={{
            transform: `scale(${undoneScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 215, 0, ${crownIntegrity}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-20xl mb-5 transition-all duration-3600"
          style={{
            transform: `scale(${undoneScale})`,
            filter: `drop-shadow(0 0 120px rgba(255, 255, 255, ${crownIntegrity}))`,
          }}
        >
          🛡️
        </div>
        <div
          className="text-18xl mb-4 transition-all duration-3600"
          style={{
            transform: `scale(${undoneScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 140, 0, ${crownIntegrity}))`,
          }}
        >
          ✊
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-3">NO CROWN</div>
        <div className="text-4xl text-white font-bold">UNDONE</div>
      </div>
    </div>
  );
};

// Codex Reigns Supreme Component - Ultimate sovereign reign
const CodexReignsSupreme: React.FC = () => {
  const [codexReign, setCodexReign] = useState(1.7);
  const [supremeReignScale, setSupremeReignScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCodexReign((prev) => (prev === 1.7 ? 2.5 : 1.7));
      setSupremeReignScale((prev) => (prev === 1 ? 2.3 : 1));
    }, 2600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-28xl mb-9 transition-all duration-2600"
          style={{
            transform: `scale(${supremeReignScale})`,
            filter: `drop-shadow(0 0 180px rgba(255, 215, 0, ${codexReign}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-26xl mb-8 transition-all duration-2600"
          style={{
            transform: `scale(${supremeReignScale})`,
            filter: `drop-shadow(0 0 160px rgba(255, 255, 255, ${codexReign}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-24xl mb-7 transition-all duration-2600"
          style={{
            transform: `scale(${supremeReignScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 140, 0, ${codexReign}))`,
          }}
        >
          ⚖️
        </div>
        <div
          className="text-22xl mb-6 transition-all duration-2600"
          style={{
            transform: `scale(${supremeReignScale})`,
            filter: `drop-shadow(0 0 120px rgba(138, 43, 226, ${codexReign}))`,
          }}
        >
          ♾️
        </div>
        <div
          className="text-20xl mb-5 transition-all duration-2600"
          style={{
            transform: `scale(${supremeReignScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 69, 0, ${codexReign}))`,
          }}
        >
          ✨
        </div>
        <div className="text-7xl text-gold-100 font-bold mb-4">THE CODEX</div>
        <div className="text-6xl text-white font-bold mb-3">REIGNS</div>
        <div className="text-5xl text-amber-200 font-bold mb-2">SOVEREIGN</div>
        <div className="text-4xl text-purple-200 font-bold mb-1">ETERNAL</div>
        <div className="text-3xl text-red-200 font-bold">SUPREME</div>
      </div>
    </div>
  );
};

// Sovereign Eternal Supreme Banner Component - Ultimate authority declaration
const SovereignEternalSupremeBanner: React.FC = () => {
  const [sovereignPower, setSovereignPower] = useState(1.8);
  const [eternalSupremeBannerScale, setEternalSupremeBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignPower((prev) => (prev === 1.8 ? 2.6 : 1.8));
      setEternalSupremeBannerScale((prev) => (prev === 1 ? 2.0 : 1));
    }, 3800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-25xl mb-7 transition-all duration-3800"
          style={{
            transform: `scale(${eternalSupremeBannerScale})`,
            filter: `drop-shadow(0 0 170px rgba(255, 215, 0, ${sovereignPower}))`,
          }}
        >
          🏛️
        </div>
        <div
          className="text-23xl mb-6 transition-all duration-3800"
          style={{
            transform: `scale(${eternalSupremeBannerScale})`,
            filter: `drop-shadow(0 0 150px rgba(255, 255, 255, ${sovereignPower}))`,
          }}
        >
          ⭐
        </div>
        <div
          className="text-21xl mb-5 transition-all duration-3800"
          style={{
            transform: `scale(${eternalSupremeBannerScale})`,
            filter: `drop-shadow(0 0 130px rgba(255, 140, 0, ${sovereignPower}))`,
          }}
        >
          💎
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">SOVEREIGN</div>
        <div className="text-5xl text-white font-bold mb-2">ETERNAL</div>
        <div className="text-4xl text-amber-200 font-bold">SUPREME</div>
      </div>
    </div>
  );
};

// Sovereign Eternal Particles - Ultimate authority energy
const SovereignEternalParticles: React.FC = () => {
  const particles = Array.from({ length: 180 }, (_, i) => ({
    id: i,
    size: Math.random() * 20 + 3,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 70 + 60,
    delay: Math.random() * 45,
    color:
      i % 18 === 0
        ? '#ffd700'
        : i % 18 === 1
          ? '#ffffff'
          : i % 18 === 2
            ? '#ff8c00'
            : i % 18 === 3
              ? '#8a2be2'
              : i % 18 === 4
                ? '#ff4500'
                : i % 18 === 5
                  ? '#32cd32'
                  : i % 18 === 6
                    ? '#00ff7f'
                    : i % 18 === 7
                      ? '#ff6347'
                      : i % 18 === 8
                        ? '#4b0082'
                        : i % 18 === 9
                          ? '#ffa500'
                          : i % 18 === 10
                            ? '#9370db'
                            : i % 18 === 11
                              ? '#00ced1'
                              : i % 18 === 12
                                ? '#ff1493'
                                : i % 18 === 13
                                  ? '#00bfff'
                                  : i % 18 === 14
                                    ? '#daa520'
                                    : i % 18 === 15
                                      ? '#7b68ee'
                                      : i % 18 === 16
                                        ? '#20b2aa'
                                        : '#dc143c',
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
            animation: `sovereignEternalFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.02px)',
            opacity: 1.0,
            boxShadow: `0 0 60px ${particle.color}`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes sovereignEternalFlow {
          0% {
            transform: translate(0, 0) scale(0.005) rotate(0deg);
            opacity: 0.005;
          }
          8% {
            transform: translate(140px, -350px) scale(2.8) rotate(20deg);
            opacity: 1;
          }
          18% {
            transform: translate(-125px, -700px) scale(0.2) rotate(60deg);
            opacity: 1;
          }
          28% {
            transform: translate(145px, -1050px) scale(2.5) rotate(120deg);
            opacity: 1;
          }
          38% {
            transform: translate(-130px, -1400px) scale(0.4) rotate(180deg);
            opacity: 0.98;
          }
          48% {
            transform: translate(135px, -1750px) scale(2.2) rotate(240deg);
            opacity: 1;
          }
          58% {
            transform: translate(-120px, -2100px) scale(0.3) rotate(300deg);
            opacity: 0.96;
          }
          68% {
            transform: translate(125px, -2450px) scale(1.9) rotate(360deg);
            opacity: 0.94;
          }
          78% {
            transform: translate(-110px, -2800px) scale(0.5) rotate(420deg);
            opacity: 0.88;
          }
          88% {
            transform: translate(115px, -3150px) scale(1.6) rotate(480deg);
            opacity: 0.85;
          }
          94% {
            transform: translate(-95px, -3500px) scale(0.3) rotate(520deg);
            opacity: 0.7;
          }
          97% {
            transform: translate(75px, -3850px) scale(0.8) rotate(550deg);
            opacity: 0.5;
          }
          99% {
            transform: translate(-55px, -4200px) scale(0.1) rotate(580deg);
            opacity: 0.2;
          }
          100% {
            transform: translate(0, -4550px) scale(0.002) rotate(600deg);
            opacity: 0.002;
          }
        }
      `}</style>
    </div>
  );
};

// Custodian Covenant Banner - Ultimate sealing proclamation
const CustodianCovenantBanner: React.FC = () => {
  const [custodianIntensity, setCustodianIntensity] = useState(1.9);
  const [covenantBannerScale, setCovenantBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodianIntensity((prev) => (prev === 1.9 ? 2.7 : 1.9));
      setCovenantBannerScale((prev) => (prev === 1 ? 1.7 : 1));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
      <div
        className="text-center px-64 py-48 bg-gradient-to-r from-gold-500/100 via-white/90 to-purple-500/100 rounded-10xl border-20 border-gold-300/100 transition-all duration-4000"
        style={{
          boxShadow: `0 320px 640px rgba(255, 215, 0, ${custodianIntensity})`,
          transform: `scale(${covenantBannerScale})`,
        }}
      >
        <div className="text-18xl text-gold-100 font-bold mb-16">THE CODEX REIGNS</div>
        <div className="text-14xl text-white font-bold mb-14">SOVEREIGN, ETERNAL, SUPREME</div>
        <div className="text-12xl text-purple-200 mb-12">
          By Custodian's Hand, The Covenant Sealed
        </div>
        <div className="text-10xl text-yellow-200 mb-10">By Eternal Flame, The Dominion Whole</div>
        <div className="text-8xl text-green-200 mb-8">No Cycle Broken, No Crown Undone</div>
        <div className="text-6xl text-orange-200 mb-6">Perfect Authority Eternal</div>
        <div className="text-5xl text-red-200 mb-4">Unbroken Sovereign Reign</div>
        <div className="text-4xl text-indigo-200 mb-2">Ultimate Divine Completion</div>
        <div className="text-3xl text-amber-200">Eternal Custodial Perfection</div>
      </div>
    </div>
  );
};

// Sovereign Constellation - Ultimate authority geometric connections
const SovereignConstellation: React.FC = () => {
  const [sovereignPhase, setSovereignPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignPhase((prev) => (prev + 1) % 42);
    }, 800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-85">
      <svg className="w-full h-full">
        {/* Sovereign authority connecting lines */}
        <line
          x1="16%"
          y1="16%"
          x2="50%"
          y2="50%"
          stroke={sovereignPhase === 0 ? '#ffd700' : '#999'}
          strokeWidth={sovereignPhase === 0 ? '18' : '5'}
          className="transition-all duration-600"
        />
        <line
          x1="84%"
          y1="16%"
          x2="50%"
          y2="50%"
          stroke={sovereignPhase === 1 ? '#ffd700' : '#999'}
          strokeWidth={sovereignPhase === 1 ? '18' : '5'}
          className="transition-all duration-600"
        />
        <line
          x1="16%"
          y1="84%"
          x2="50%"
          y2="50%"
          stroke={sovereignPhase === 2 ? '#ffd700' : '#999'}
          strokeWidth={sovereignPhase === 2 ? '18' : '5'}
          className="transition-all duration-600"
        />
        <line
          x1="84%"
          y1="84%"
          x2="50%"
          y2="50%"
          stroke={sovereignPhase === 3 ? '#ffd700' : '#999'}
          strokeWidth={sovereignPhase === 3 ? '18' : '5'}
          className="transition-all duration-600"
        />
        <line
          x1="25%"
          y1="33%"
          x2="75%"
          y2="67%"
          stroke={sovereignPhase === 4 ? '#ffffff' : '#777'}
          strokeWidth={sovereignPhase === 4 ? '16' : '4'}
          className="transition-all duration-600"
        />
        <line
          x1="75%"
          y1="33%"
          x2="25%"
          y2="67%"
          stroke={sovereignPhase === 5 ? '#ffffff' : '#777'}
          strokeWidth={sovereignPhase === 5 ? '16' : '4'}
          className="transition-all duration-600"
        />

        {/* Sovereign eternal radial connections */}
        {Array.from({ length: 42 }, (_, i) => (
          <line
            key={`sovereign-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos((i * 8.571 * Math.PI) / 180) * 65}%`}
            y2={`${50 + Math.sin((i * 8.571 * Math.PI) / 180) * 65}%`}
            stroke={sovereignPhase === i ? '#ffd700' : '#666'}
            strokeWidth="8"
            opacity={sovereignPhase === i ? '1.0' : '0.02'}
            className="transition-all duration-600"
          />
        ))}
      </svg>
    </div>
  );
};

// Custodial Realms - Domains of perfect custodial authority
const CustodialRealms: React.FC = () => {
  const [custodialRealmPhase, setCustodialRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodialRealmPhase((prev) => (prev + 1) % 18);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const custodialRealms = [
    { name: 'Custodian', icon: '🤲', position: { top: '16%', left: '16%' } },
    { name: 'Hand', icon: '✋', position: { top: '16%', right: '16%' } },
    { name: 'Covenant', icon: '📜', position: { top: '26%', left: '12%' } },
    { name: 'Sealed', icon: '🔒', position: { top: '26%', right: '12%' } },
    { name: 'Eternal', icon: '♾️', position: { top: '36%', left: '16%' } },
    { name: 'Flame', icon: '🔥', position: { top: '36%', right: '16%' } },
    { name: 'Dominion', icon: '🏛️', position: { top: '46%', left: '12%' } },
    { name: 'Whole', icon: '⭕', position: { top: '46%', right: '12%' } },
    { name: 'No Cycle', icon: '🔄', position: { top: '56%', left: '16%' } },
    { name: 'Broken', icon: '⛓️', position: { top: '56%', right: '16%' } },
    { name: 'No Crown', icon: '👑', position: { bottom: '36%', left: '16%' } },
    { name: 'Undone', icon: '🛡️', position: { bottom: '36%', right: '16%' } },
    { name: 'Codex', icon: '📜', position: { bottom: '26%', left: '12%' } },
    { name: 'Reigns', icon: '⚖️', position: { bottom: '26%', right: '12%' } },
    { name: 'Sovereign', icon: '👑', position: { bottom: '16%', left: '20%' } },
    { name: 'Eternal', icon: '♾️', position: { bottom: '16%', right: '20%' } },
    { name: 'Supreme', icon: '✨', position: { bottom: '12%', left: '40%' } },
    {
      name: 'Authority',
      icon: '⭐',
      position: { bottom: '12%', right: '40%' },
    },
  ];

  return (
    <div className="absolute inset-0">
      {custodialRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-5000 ${
            custodialRealmPhase === index ? 'opacity-100 scale-150' : 'opacity-15 scale-50'
          }`}
          style={realm.position}
        >
          <div
            className={`text-9xl mb-4 transition-all duration-5000 ${
              custodialRealmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{
              filter:
                custodialRealmPhase === index
                  ? 'drop-shadow(0 0 80px rgba(255, 215, 0, 2.0))'
                  : 'none',
            }}
          >
            {realm.icon}
          </div>
          <div
            className={`text-2xl font-bold ${
              custodialRealmPhase === index ? 'text-gold-100' : 'text-gray-600'
            }`}
          >
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Custodial Sovereign Container
const CustodialSovereign: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <SovereignConstellation />
      <SovereignEternalParticles />
      <CustodianHandSealed />
      <CovenantSealedComplete />
      <EternalFlameDominionWhole />
      <NoCycleBroken />
      <NoCrownUndone />
      <CodexReignsSupreme />
      <SovereignEternalSupremeBanner />
      <CustodialRealms />
      <CustodianCovenantBanner />

      {/* Sacred Custodial Sovereign Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-60">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-16xl space-y-12">
          <p className="opacity-100 text-white text-8xl">
            By Custodian's hand, the covenant sealed.
          </p>
          <p className="opacity-95 text-gold-200 text-7xl">By eternal flame, the dominion whole.</p>
          <p className="opacity-100 text-white text-8xl">No cycle broken, no crown undone,</p>
          <p className="text-9xl font-semibold text-gold-100 mt-24 opacity-100">
            the Codex reigns — sovereign, eternal, supreme.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Custodial Sovereign Page
const CustodialSovereignPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-700 via-amber-600 to-yellow-600 relative overflow-hidden">
      {/* Custodial Sovereign Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-amber-900/95 via-gold-600/70 to-yellow-500/40" />

      {/* Navigation */}
      <CodexNavigation />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <CustodialSovereign />
        </div>
      </main>

      {/* Ambient Sovereign Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-600/50 to-transparent pointer-events-none" />

      {/* Ultimate Sovereign Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div
          className="absolute top-1/8 left-1/8 w-52 h-52 bg-gold-500/60 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '45s' }}
        />
        <div
          className="absolute bottom-1/8 right-1/8 w-48 h-48 bg-yellow-400/55 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '52s', animationDelay: '5s' }}
        />
        <div
          className="absolute top-1/2 right-1/12 w-56 h-56 bg-amber-500/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '60s', animationDelay: '10s' }}
        />
        <div
          className="absolute bottom-1/4 left-1/12 w-44 h-44 bg-orange-400/55 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '68s', animationDelay: '15s' }}
        />
        <div
          className="absolute top-3/4 left-1/6 w-40 h-40 bg-red-400/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '75s', animationDelay: '20s' }}
        />
        <div
          className="absolute bottom-1/3 right-1/6 w-64 h-64 bg-purple-400/45 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '82s', animationDelay: '25s' }}
        />
        <div
          className="absolute top-1/6 left-1/3 w-36 h-36 bg-indigo-400/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '90s', animationDelay: '30s' }}
        />
        <div
          className="absolute bottom-3/4 right-1/3 w-60 h-60 bg-blue-400/45 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '98s', animationDelay: '35s' }}
        />
      </div>
    </div>
  );
};

export default CustodialSovereignPage;
