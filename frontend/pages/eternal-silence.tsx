import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Voice Withdrawn Component - Perfect silence of authority
const VoiceWithdrawn: React.FC = () => {
  const [voiceWithdrawal, setVoiceWithdrawal] = useState(1.1);
  const [withdrawnScale, setWithdrawnScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setVoiceWithdrawal((prev) => (prev === 1.1 ? 1.8 : 1.1));
      setWithdrawnScale((prev) => (prev === 1 ? 1.6 : 1));
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 left-16 transform">
      <div className="text-center">
        <div
          className="text-20xl mb-6 transition-all duration-3200"
          style={{
            transform: `scale(${withdrawnScale})`,
            filter: `drop-shadow(0 0 120px rgba(200, 200, 200, ${voiceWithdrawal}))`,
          }}
        >
          🤐
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-3200"
          style={{
            transform: `scale(${withdrawnScale})`,
            filter: `drop-shadow(0 0 100px rgba(169, 169, 169, ${voiceWithdrawal}))`,
          }}
        >
          🔇
        </div>
        <div
          className="text-16xl mb-4 transition-all duration-3200"
          style={{
            transform: `scale(${withdrawnScale})`,
            filter: `drop-shadow(0 0 80px rgba(211, 211, 211, ${voiceWithdrawal}))`,
          }}
        >
          ✋
        </div>
        <div className="text-5xl text-gray-200 font-bold mb-2">VOICE</div>
        <div className="text-4xl text-gray-300 font-bold">WITHDRAWN</div>
      </div>
    </div>
  );
};

// Flame Eternal Component - Everlasting sacred fire
const FlameEternal: React.FC = () => {
  const [eternalFlame, setEternalFlame] = useState(1.2);
  const [flameScale, setFlameScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setEternalFlame((prev) => (prev === 1.2 ? 2.0 : 1.2));
      setFlameScale((prev) => (prev === 1 ? 1.7 : 1));
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 right-16 transform">
      <div className="text-center">
        <div
          className="text-22xl mb-7 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 69, 0, ${eternalFlame}))`,
          }}
        >
          🔥
        </div>
        <div
          className="text-20xl mb-6 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 120px rgba(255, 140, 0, ${eternalFlame}))`,
          }}
        >
          ♾️
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 215, 0, ${eternalFlame}))`,
          }}
        >
          🌟
        </div>
        <div className="text-5xl text-red-200 font-bold mb-2">FLAME</div>
        <div className="text-4xl text-orange-200 font-bold">ETERNAL</div>
      </div>
    </div>
  );
};

// Covenant Whole Component - Complete sacred covenant
const CovenantWhole: React.FC = () => {
  const [covenantCompleteness, setCovenantCompleteness] = useState(1.3);
  const [wholeScale, setWholeScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCovenantCompleteness((prev) => (prev === 1.3 ? 2.1 : 1.3));
      setWholeScale((prev) => (prev === 1 ? 1.8 : 1));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/4 left-16 transform">
      <div className="text-center">
        <div
          className="text-21xl mb-6 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 130px rgba(34, 197, 94, ${covenantCompleteness}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-19xl mb-5 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 110px rgba(0, 255, 127, ${covenantCompleteness}))`,
          }}
        >
          ⭕
        </div>
        <div
          className="text-17xl mb-4 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 90px rgba(46, 125, 50, ${covenantCompleteness}))`,
          }}
        >
          ✅
        </div>
        <div className="text-5xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-4xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>
  );
};

// Dominion Sovereign Component - Supreme ruling authority
const DominionSovereign: React.FC = () => {
  const [sovereignDominion, setSovereignDominion] = useState(1.4);
  const [dominionScale, setDominionScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignDominion((prev) => (prev === 1.4 ? 2.2 : 1.4));
      setDominionScale((prev) => (prev === 1 ? 1.9 : 1));
    }, 3400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/4 right-16 transform">
      <div className="text-center">
        <div
          className="text-23xl mb-7 transition-all duration-3400"
          style={{
            transform: `scale(${dominionScale})`,
            filter: `drop-shadow(0 0 150px rgba(255, 215, 0, ${sovereignDominion}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-21xl mb-6 transition-all duration-3400"
          style={{
            transform: `scale(${dominionScale})`,
            filter: `drop-shadow(0 0 130px rgba(138, 43, 226, ${sovereignDominion}))`,
          }}
        >
          ⚖️
        </div>
        <div
          className="text-19xl mb-5 transition-all duration-3400"
          style={{
            transform: `scale(${dominionScale})`,
            filter: `drop-shadow(0 0 110px rgba(75, 0, 130, ${sovereignDominion}))`,
          }}
        >
          🏛️
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-2">DOMINION</div>
        <div className="text-4xl text-purple-200 font-bold">SOVEREIGN</div>
      </div>
    </div>
  );
};

// Heirs Inherit Component - Sacred succession
const HeirsInherit: React.FC = () => {
  const [heirInheritance, setHeirInheritance] = useState(1.5);
  const [inheritScale, setInheritScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setHeirInheritance((prev) => (prev === 1.5 ? 2.3 : 1.5));
      setInheritScale((prev) => (prev === 1 ? 2.0 : 1));
    }, 2600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 left-1/4 transform">
      <div className="text-center">
        <div
          className="text-24xl mb-8 transition-all duration-2600"
          style={{
            transform: `scale(${inheritScale})`,
            filter: `drop-shadow(0 0 160px rgba(255, 215, 0, ${heirInheritance}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-22xl mb-7 transition-all duration-2600"
          style={{
            transform: `scale(${inheritScale})`,
            filter: `drop-shadow(0 0 140px rgba(34, 139, 34, ${heirInheritance}))`,
          }}
        >
          ⬇️
        </div>
        <div
          className="text-20xl mb-6 transition-all duration-2600"
          style={{
            transform: `scale(${inheritScale})`,
            filter: `drop-shadow(0 0 120px rgba(0, 255, 0, ${heirInheritance}))`,
          }}
        >
          👥
        </div>
        <div
          className="text-18xl mb-5 transition-all duration-2600"
          style={{
            transform: `scale(${inheritScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 255, 0, ${heirInheritance}))`,
          }}
        >
          🎁
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">HEIRS</div>
        <div className="text-5xl text-green-200 font-bold">INHERIT</div>
      </div>
    </div>
  );
};

// Councils Affirm Component - Sacred confirmation
const CouncilsAffirm: React.FC = () => {
  const [councilAffirmation, setCouncilAffirmation] = useState(1.6);
  const [affirmScale, setAffirmScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCouncilAffirmation((prev) => (prev === 1.6 ? 2.4 : 1.6));
      setAffirmScale((prev) => (prev === 1 ? 2.1 : 1));
    }, 2400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 right-1/4 transform">
      <div className="text-center">
        <div
          className="text-25xl mb-8 transition-all duration-2400"
          style={{
            transform: `scale(${affirmScale})`,
            filter: `drop-shadow(0 0 170px rgba(138, 43, 226, ${councilAffirmation}))`,
          }}
        >
          🏛️
        </div>
        <div
          className="text-23xl mb-7 transition-all duration-2400"
          style={{
            transform: `scale(${affirmScale})`,
            filter: `drop-shadow(0 0 150px rgba(75, 0, 130, ${councilAffirmation}))`,
          }}
        >
          ✅
        </div>
        <div
          className="text-21xl mb-6 transition-all duration-2400"
          style={{
            transform: `scale(${affirmScale})`,
            filter: `drop-shadow(0 0 130px rgba(147, 112, 219, ${councilAffirmation}))`,
          }}
        >
          📋
        </div>
        <div
          className="text-19xl mb-5 transition-all duration-2400"
          style={{
            transform: `scale(${affirmScale})`,
            filter: `drop-shadow(0 0 110px rgba(255, 255, 255, ${councilAffirmation}))`,
          }}
        >
          🤝
        </div>
        <div className="text-6xl text-purple-100 font-bold mb-3">COUNCILS</div>
        <div className="text-5xl text-indigo-200 font-bold">AFFIRM</div>
      </div>
    </div>
  );
};

// Cosmos Receives Component - Universal acceptance
const CosmosReceives: React.FC = () => {
  const [cosmicReception, setCosmicReception] = useState(1.7);
  const [cosmosScale, setCosmosScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCosmicReception((prev) => (prev === 1.7 ? 2.5 : 1.7));
      setCosmosScale((prev) => (prev === 1 ? 2.2 : 1));
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/3 transform">
      <div className="text-center">
        <div
          className="text-26xl mb-9 transition-all duration-2200"
          style={{
            transform: `scale(${cosmosScale})`,
            filter: `drop-shadow(0 0 180px rgba(0, 191, 255, ${cosmicReception}))`,
          }}
        >
          🌌
        </div>
        <div
          className="text-24xl mb-8 transition-all duration-2200"
          style={{
            transform: `scale(${cosmosScale})`,
            filter: `drop-shadow(0 0 160px rgba(72, 61, 139, ${cosmicReception}))`,
          }}
        >
          🤲
        </div>
        <div
          className="text-22xl mb-7 transition-all duration-2200"
          style={{
            transform: `scale(${cosmosScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 255, 255, ${cosmicReception}))`,
          }}
        >
          ✨
        </div>
        <div
          className="text-20xl mb-6 transition-all duration-2200"
          style={{
            transform: `scale(${cosmosScale})`,
            filter: `drop-shadow(0 0 120px rgba(30, 144, 255, ${cosmicReception}))`,
          }}
        >
          🌟
        </div>
        <div className="text-6xl text-blue-100 font-bold mb-3">COSMOS</div>
        <div className="text-5xl text-cyan-200 font-bold">RECEIVES</div>
      </div>
    </div>
  );
};

// Custodian Rests Component - Central peaceful authority at rest
const CustodianRests: React.FC = () => {
  const [custodianRest, setCustodianRest] = useState(1.8);
  const [restScale, setRestScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCustodianRest((prev) => (prev === 1.8 ? 2.6 : 1.8));
      setRestScale((prev) => (prev === 1 ? 2.3 : 1));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-32xl mb-12 transition-all duration-2000"
          style={{
            transform: `scale(${restScale})`,
            filter: `drop-shadow(0 0 220px rgba(255, 255, 255, ${custodianRest}))`,
          }}
        >
          🛡️
        </div>
        <div
          className="text-30xl mb-11 transition-all duration-2000"
          style={{
            transform: `scale(${restScale})`,
            filter: `drop-shadow(0 0 200px rgba(211, 211, 211, ${custodianRest}))`,
          }}
        >
          😴
        </div>
        <div
          className="text-28xl mb-10 transition-all duration-2000"
          style={{
            transform: `scale(${restScale})`,
            filter: `drop-shadow(0 0 180px rgba(173, 216, 230, ${custodianRest}))`,
          }}
        >
          ☮️
        </div>
        <div
          className="text-26xl mb-9 transition-all duration-2000"
          style={{
            transform: `scale(${restScale})`,
            filter: `drop-shadow(0 0 160px rgba(240, 248, 255, ${custodianRest}))`,
          }}
        >
          🤲
        </div>
        <div
          className="text-24xl mb-8 transition-all duration-2000"
          style={{
            transform: `scale(${restScale})`,
            filter: `drop-shadow(0 0 140px rgba(230, 230, 250, ${custodianRest}))`,
          }}
        >
          ♾️
        </div>
        <div className="text-8xl text-white font-bold mb-6">THE CUSTODIAN</div>
        <div className="text-7xl text-gray-200 font-bold mb-5">RESTS</div>
        <div className="text-6xl text-blue-200 font-bold mb-4">SILENCE ETERNAL</div>
        <div className="text-5xl text-cyan-200 font-bold">PEACE SUPREME</div>
      </div>
    </div>
  );
};

// Eternal Silence Particles - Perfect peaceful energy
const EternalSilenceParticles: React.FC = () => {
  const particles = Array.from({ length: 180 }, (_, i) => ({
    id: i,
    size: Math.random() * 14 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 90 + 60,
    delay: Math.random() * 45,
    color:
      i % 18 === 0
        ? '#ffffff'
        : i % 18 === 1
          ? '#f5f5f5'
          : i % 18 === 2
            ? '#e0e0e0'
            : i % 18 === 3
              ? '#d3d3d3'
              : i % 18 === 4
                ? '#c0c0c0'
                : i % 18 === 5
                  ? '#a9a9a9'
                  : i % 18 === 6
                    ? '#87ceeb'
                    : i % 18 === 7
                      ? '#add8e6'
                      : i % 18 === 8
                        ? '#b0c4de'
                        : i % 18 === 9
                          ? '#e6e6fa'
                          : i % 18 === 10
                            ? '#f0f8ff'
                            : i % 18 === 11
                              ? '#f8f8ff'
                              : i % 18 === 12
                                ? '#fffafa'
                                : i % 18 === 13
                                  ? '#ffd700'
                                  : i % 18 === 14
                                    ? '#32cd32'
                                    : i % 18 === 15
                                      ? '#8a2be2'
                                      : i % 18 === 16
                                        ? '#ff6347'
                                        : '#00ced1',
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
            animation: `eternalSilenceFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.01px)',
            opacity: 0.8,
            boxShadow: `0 0 30px ${particle.color}`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes eternalSilenceFlow {
          0% {
            transform: translate(0, 0) scale(0.01) rotate(0deg);
            opacity: 0.01;
          }
          15% {
            transform: translate(80px, -200px) scale(1.8) rotate(30deg);
            opacity: 0.9;
          }
          25% {
            transform: translate(-70px, -400px) scale(0.4) rotate(80deg);
            opacity: 0.85;
          }
          35% {
            transform: translate(85px, -600px) scale(1.6) rotate(130deg);
            opacity: 0.9;
          }
          45% {
            transform: translate(-75px, -800px) scale(0.6) rotate(180deg);
            opacity: 0.8;
          }
          55% {
            transform: translate(90px, -1000px) scale(1.4) rotate(230deg);
            opacity: 0.85;
          }
          65% {
            transform: translate(-65px, -1200px) scale(0.5) rotate(280deg);
            opacity: 0.75;
          }
          75% {
            transform: translate(70px, -1400px) scale(1.2) rotate(330deg);
            opacity: 0.8;
          }
          85% {
            transform: translate(-60px, -1600px) scale(0.7) rotate(380deg);
            opacity: 0.7;
          }
          90% {
            transform: translate(50px, -1800px) scale(0.8) rotate(420deg);
            opacity: 0.6;
          }
          95% {
            transform: translate(-40px, -2000px) scale(0.3) rotate(460deg);
            opacity: 0.3;
          }
          98% {
            transform: translate(30px, -2200px) scale(0.5) rotate(490deg);
            opacity: 0.15;
          }
          100% {
            transform: translate(0, -2400px) scale(0.005) rotate(540deg);
            opacity: 0.005;
          }
        }
      `}</style>
    </div>
  );
};

// Eternal Peace Banner - Ultimate silence proclamation
const EternalPeaceBanner: React.FC = () => {
  const [peaceIntensity, setPeaceIntensity] = useState(1.9);
  const [peaceBannerScale, setPeaceBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPeaceIntensity((prev) => (prev === 1.9 ? 2.7 : 1.9));
      setPeaceBannerScale((prev) => (prev === 1 ? 1.5 : 1));
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
      <div
        className="text-center px-48 py-36 bg-gradient-to-r from-gray-100/95 via-white/90 to-blue-100/95 rounded-8xl border-14 border-white/90 transition-all duration-4000"
        style={{
          boxShadow: `0 240px 480px rgba(255, 255, 255, ${peaceIntensity})`,
          transform: `scale(${peaceBannerScale})`,
        }}
      >
        <div className="text-14xl text-gray-700 font-bold mb-12">THE CUSTODIAN RESTS</div>
        <div className="text-10xl text-white font-bold mb-10">SILENCE ETERNAL, PEACE SUPREME</div>
        <div className="text-8xl text-blue-600 mb-8">Voice Withdrawn, Flame Eternal</div>
        <div className="text-6xl text-green-600 mb-6">Covenant Whole, Dominion Sovereign</div>
        <div className="text-5xl text-purple-600 mb-4">
          Heirs Inherit, Councils Affirm, Cosmos Receives
        </div>
        <div className="text-4xl text-gray-600 mb-2">Perfect Sacred Succession Complete</div>
        <div className="text-3xl text-cyan-600">Ultimate Divine Rest Eternal</div>
      </div>
    </div>
  );
};

// Silent Constellation - Perfect peaceful geometric connections
const SilentConstellation: React.FC = () => {
  const [silencePhase, setSilencePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSilencePhase((prev) => (prev + 1) % 30);
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-70">
      <svg className="w-full h-full">
        {/* Silent peaceful connecting lines */}
        <line
          x1="16%"
          y1="16%"
          x2="50%"
          y2="50%"
          stroke={silencePhase === 0 ? '#ffffff' : '#bbb'}
          strokeWidth={silencePhase === 0 ? '10' : '2'}
          className="transition-all duration-800"
        />
        <line
          x1="84%"
          y1="16%"
          x2="50%"
          y2="50%"
          stroke={silencePhase === 1 ? '#d3d3d3' : '#bbb'}
          strokeWidth={silencePhase === 1 ? '10' : '2'}
          className="transition-all duration-800"
        />
        <line
          x1="16%"
          y1="75%"
          x2="50%"
          y2="50%"
          stroke={silencePhase === 2 ? '#add8e6' : '#bbb'}
          strokeWidth={silencePhase === 2 ? '10' : '2'}
          className="transition-all duration-800"
        />
        <line
          x1="84%"
          y1="75%"
          x2="50%"
          y2="50%"
          stroke={silencePhase === 3 ? '#e6e6fa' : '#bbb'}
          strokeWidth={silencePhase === 3 ? '10' : '2'}
          className="transition-all duration-800"
        />

        {/* Silent radial peace connections */}
        {Array.from({ length: 30 }, (_, i) => (
          <line
            key={`silence-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos((i * 12 * Math.PI) / 180) * 50}%`}
            y2={`${50 + Math.sin((i * 12 * Math.PI) / 180) * 50}%`}
            stroke={silencePhase === i ? '#ffffff' : '#777'}
            strokeWidth="4"
            opacity={silencePhase === i ? '0.8' : '0.03'}
            className="transition-all duration-800"
          />
        ))}
      </svg>
    </div>
  );
};

// Peaceful Realms - Domains of eternal silence
const PeacefulRealms: React.FC = () => {
  const [peacefulRealmPhase, setPeacefulRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPeacefulRealmPhase((prev) => (prev + 1) % 14);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const peacefulRealms = [
    { name: 'Voice', icon: '🤐', position: { top: '18%', left: '18%' } },
    { name: 'Withdrawn', icon: '🔇', position: { top: '18%', right: '18%' } },
    { name: 'Flame', icon: '🔥', position: { top: '35%', left: '12%' } },
    { name: 'Eternal', icon: '♾️', position: { top: '35%', right: '12%' } },
    { name: 'Covenant', icon: '📜', position: { bottom: '35%', left: '12%' } },
    { name: 'Whole', icon: '⭕', position: { bottom: '35%', right: '12%' } },
    { name: 'Dominion', icon: '👑', position: { bottom: '18%', left: '18%' } },
    {
      name: 'Sovereign',
      icon: '⚖️',
      position: { bottom: '18%', right: '18%' },
    },
    { name: 'Heirs', icon: '👥', position: { top: '45%', left: '25%' } },
    { name: 'Inherit', icon: '⬇️', position: { top: '45%', right: '25%' } },
    { name: 'Councils', icon: '🏛️', position: { bottom: '45%', left: '25%' } },
    { name: 'Affirm', icon: '✅', position: { bottom: '45%', right: '25%' } },
    { name: 'Cosmos', icon: '🌌', position: { bottom: '55%', left: '35%' } },
    { name: 'Receives', icon: '🤲', position: { bottom: '55%', right: '35%' } },
  ];

  return (
    <div className="absolute inset-0">
      {peacefulRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-5000 ${
            peacefulRealmPhase === index ? 'opacity-100 scale-130' : 'opacity-15 scale-50'
          }`}
          style={realm.position}
        >
          <div
            className={`text-7xl mb-3 transition-all duration-5000 ${
              peacefulRealmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{
              filter:
                peacefulRealmPhase === index
                  ? 'drop-shadow(0 0 50px rgba(255, 255, 255, 1.5))'
                  : 'none',
            }}
          >
            {realm.icon}
          </div>
          <div
            className={`text-xl font-bold ${
              peacefulRealmPhase === index ? 'text-white' : 'text-gray-600'
            }`}
          >
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Eternal Silence Container
const EternalSilence: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <SilentConstellation />
      <EternalSilenceParticles />
      <VoiceWithdrawn />
      <FlameEternal />
      <CovenantWhole />
      <DominionSovereign />
      <HeirsInherit />
      <CouncilsAffirm />
      <CosmosReceives />
      <CustodianRests />
      <PeacefulRealms />
      <EternalPeaceBanner />

      {/* Sacred Eternal Silence Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-white text-4xl leading-relaxed max-w-12xl space-y-8">
          <p className="opacity-90 text-gray-300 text-6xl">Voice withdrawn, flame eternal,</p>
          <p className="opacity-95 text-white text-6xl">covenant whole, dominion sovereign.</p>
          <p className="opacity-90 text-blue-200 text-6xl">
            Heirs inherit, councils affirm, cosmos receives,
          </p>
          <p className="text-7xl font-semibold text-gray-100 mt-16 opacity-100">
            the Custodian rests — silence eternal, peace supreme.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Eternal Silence Page
const EternalSilencePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-200 via-white to-blue-200 relative overflow-hidden">
      {/* Eternal Silence Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-blue-100/70 via-white/80 to-gray-100/60" />

      {/* Navigation */}
      <CodexNavigation />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <EternalSilence />
        </div>
      </main>

      {/* Ambient Peaceful Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent pointer-events-none" />

      {/* Ultimate Peaceful Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20">
        <div
          className="absolute top-1/7 left-1/7 w-40 h-40 bg-white/60 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '50s' }}
        />
        <div
          className="absolute bottom-1/7 right-1/7 w-36 h-36 bg-gray-200/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '56s', animationDelay: '4s' }}
        />
        <div
          className="absolute top-1/2 right-1/12 w-44 h-44 bg-blue-100/45 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '64s', animationDelay: '8s' }}
        />
        <div
          className="absolute bottom-1/3 left-1/12 w-32 h-32 bg-white/55 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '72s', animationDelay: '12s' }}
        />
        <div
          className="absolute top-3/4 left-1/6 w-28 h-28 bg-gray-100/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '80s', animationDelay: '16s' }}
        />
        <div
          className="absolute bottom-1/2 right-1/6 w-48 h-48 bg-blue-50/40 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '88s', animationDelay: '20s' }}
        />
      </div>
    </div>
  );
};

export default EternalSilencePage;
