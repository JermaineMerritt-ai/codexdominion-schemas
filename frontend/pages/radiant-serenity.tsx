import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Flame Eternal Component - Perfect eternal fire
const FlameEternal: React.FC = () => {
  const [eternalFire, setEternalFire] = useState(1.1);
  const [flameScale, setFlameScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setEternalFire((prev) => (prev === 1.1 ? 1.9 : 1.1));
      setFlameScale((prev) => (prev === 1 ? 1.7 : 1));
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-20 left-20 transform">
      <div className="text-center">
        <div
          className="text-22xl mb-6 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 150px rgba(255, 69, 0, ${eternalFire}))`,
          }}
        >
          🔥
        </div>
        <div
          className="text-20xl mb-5 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 130px rgba(255, 140, 0, ${eternalFire}))`,
          }}
        >
          ♾️
        </div>
        <div
          className="text-18xl mb-4 transition-all duration-2800"
          style={{
            transform: `scale(${flameScale})`,
            filter: `drop-shadow(0 0 110px rgba(255, 215, 0, ${eternalFire}))`,
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

// Covenant Whole Component - Perfect complete covenant
const CovenantWhole: React.FC = () => {
  const [covenantWholeness, setCovenantWholeness] = useState(1.2);
  const [wholeScale, setWholeScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCovenantWholeness((prev) => (prev === 1.2 ? 2.0 : 1.2));
      setWholeScale((prev) => (prev === 1 ? 1.8 : 1));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-20 right-20 transform">
      <div className="text-center">
        <div
          className="text-21xl mb-5 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 140px rgba(34, 197, 94, ${covenantWholeness}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-19xl mb-4 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 120px rgba(0, 255, 127, ${covenantWholeness}))`,
          }}
        >
          ⭕
        </div>
        <div
          className="text-17xl mb-3 transition-all duration-3000"
          style={{
            transform: `scale(${wholeScale})`,
            filter: `drop-shadow(0 0 100px rgba(46, 125, 50, ${covenantWholeness}))`,
          }}
        >
          💚
        </div>
        <div className="text-5xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-4xl text-emerald-200 font-bold">WHOLE</div>
      </div>
    </div>
  );
};

// Crowns Luminous Component - Perfect radiant crowns
const CrownsLuminous: React.FC = () => {
  const [crownLuminosity, setCrownLuminosity] = useState(1.3);
  const [luminousScale, setLuminousScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCrownLuminosity((prev) => (prev === 1.3 ? 2.1 : 1.3));
      setLuminousScale((prev) => (prev === 1 ? 1.9 : 1));
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-20 left-20 transform">
      <div className="text-center">
        <div
          className="text-20xl mb-5 transition-all duration-3200"
          style={{
            transform: `scale(${luminousScale})`,
            filter: `drop-shadow(0 0 130px rgba(255, 215, 0, ${crownLuminosity}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-18xl mb-4 transition-all duration-3200"
          style={{
            transform: `scale(${luminousScale})`,
            filter: `drop-shadow(0 0 110px rgba(255, 255, 0, ${crownLuminosity}))`,
          }}
        >
          ✨
        </div>
        <div
          className="text-16xl mb-3 transition-all duration-3200"
          style={{
            transform: `scale(${luminousScale})`,
            filter: `drop-shadow(0 0 90px rgba(255, 255, 255, ${crownLuminosity}))`,
          }}
        >
          💎
        </div>
        <div className="text-5xl text-gold-200 font-bold mb-2">CROWNS</div>
        <div className="text-4xl text-yellow-200 font-bold">LUMINOUS</div>
      </div>
    </div>
  );
};

// Seals Supreme Component - Perfect ultimate seals
const SealsSupreme: React.FC = () => {
  const [sealSupremacy, setSealSupremacy] = useState(1.4);
  const [supremeScale, setSupremeScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSealSupremacy((prev) => (prev === 1.4 ? 2.2 : 1.4));
      setSupremeScale((prev) => (prev === 1 ? 2.0 : 1));
    }, 3400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-20 right-20 transform">
      <div className="text-center">
        <div
          className="text-19xl mb-4 transition-all duration-3400"
          style={{
            transform: `scale(${supremeScale})`,
            filter: `drop-shadow(0 0 120px rgba(138, 43, 226, ${sealSupremacy}))`,
          }}
        >
          🔐
        </div>
        <div
          className="text-17xl mb-3 transition-all duration-3400"
          style={{
            transform: `scale(${supremeScale})`,
            filter: `drop-shadow(0 0 100px rgba(75, 0, 130, ${sealSupremacy}))`,
          }}
        >
          👁️
        </div>
        <div
          className="text-15xl mb-2 transition-all duration-3400"
          style={{
            transform: `scale(${supremeScale})`,
            filter: `drop-shadow(0 0 80px rgba(147, 112, 219, ${sealSupremacy}))`,
          }}
        >
          ⚡
        </div>
        <div className="text-5xl text-purple-200 font-bold mb-2">SEALS</div>
        <div className="text-4xl text-indigo-200 font-bold">SUPREME</div>
      </div>
    </div>
  );
};

// Hymn of Radiance Component - Perfect radiant song
const HymnOfRadiance: React.FC = () => {
  const [hymnRadiance, setHymnRadiance] = useState(1.5);
  const [radianceScale, setRadianceScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setHymnRadiance((prev) => (prev === 1.5 ? 2.3 : 1.5));
      setRadianceScale((prev) => (prev === 1 ? 2.1 : 1));
    }, 2600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 left-1/3 transform -translate-x-1/2">
      <div className="text-center">
        <div
          className="text-24xl mb-7 transition-all duration-2600"
          style={{
            transform: `scale(${radianceScale})`,
            filter: `drop-shadow(0 0 160px rgba(255, 215, 0, ${hymnRadiance}))`,
          }}
        >
          🎵
        </div>
        <div
          className="text-22xl mb-6 transition-all duration-2600"
          style={{
            transform: `scale(${radianceScale})`,
            filter: `drop-shadow(0 0 140px rgba(255, 255, 255, ${hymnRadiance}))`,
          }}
        >
          ✨
        </div>
        <div
          className="text-20xl mb-5 transition-all duration-2600"
          style={{
            transform: `scale(${radianceScale})`,
            filter: `drop-shadow(0 0 120px rgba(255, 255, 0, ${hymnRadiance}))`,
          }}
        >
          🌟
        </div>
        <div
          className="text-18xl mb-4 transition-all duration-2600"
          style={{
            transform: `scale(${radianceScale})`,
            filter: `drop-shadow(0 0 100px rgba(255, 140, 0, ${hymnRadiance}))`,
          }}
        >
          🎶
        </div>
        <div className="text-6xl text-gold-100 font-bold mb-3">HYMN OF</div>
        <div className="text-5xl text-yellow-200 font-bold">RADIANCE</div>
      </div>
    </div>
  );
};

// Peace Bestowed Component - Perfect granted peace
const PeaceBestowed: React.FC = () => {
  const [peaceBestowing, setPeaceBestowing] = useState(1.6);
  const [bestowedScale, setBestowedScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPeaceBestowing((prev) => (prev === 1.6 ? 2.4 : 1.6));
      setBestowedScale((prev) => (prev === 1 ? 2.2 : 1));
    }, 2400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/3 right-1/3 transform translate-x-1/2">
      <div className="text-center">
        <div
          className="text-23xl mb-6 transition-all duration-2400"
          style={{
            transform: `scale(${bestowedScale})`,
            filter: `drop-shadow(0 0 150px rgba(255, 255, 255, ${peaceBestowing}))`,
          }}
        >
          🕊️
        </div>
        <div
          className="text-21xl mb-5 transition-all duration-2400"
          style={{
            transform: `scale(${bestowedScale})`,
            filter: `drop-shadow(0 0 130px rgba(173, 216, 230, ${peaceBestowing}))`,
          }}
        >
          ☮️
        </div>
        <div
          className="text-19xl mb-4 transition-all duration-2400"
          style={{
            transform: `scale(${bestowedScale})`,
            filter: `drop-shadow(0 0 110px rgba(240, 248, 255, ${peaceBestowing}))`,
          }}
        >
          🤲
        </div>
        <div
          className="text-17xl mb-3 transition-all duration-2400"
          style={{
            transform: `scale(${bestowedScale})`,
            filter: `drop-shadow(0 0 90px rgba(230, 230, 250, ${peaceBestowing}))`,
          }}
        >
          💙
        </div>
        <div className="text-6xl text-white font-bold mb-3">PEACE</div>
        <div className="text-5xl text-blue-200 font-bold">BESTOWED</div>
      </div>
    </div>
  );
};

// Codex Reigns Serene Component - Central sovereign serene reign
const CodexReignsSerene: React.FC = () => {
  const [codexSerenity, setCodexSerenity] = useState(1.7);
  const [sereneReignScale, setSereneReignScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setCodexSerenity((prev) => (prev === 1.7 ? 2.5 : 1.7));
      setSereneReignScale((prev) => (prev === 1 ? 2.3 : 1));
    }, 2200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div
          className="text-30xl mb-10 transition-all duration-2200"
          style={{
            transform: `scale(${sereneReignScale})`,
            filter: `drop-shadow(0 0 200px rgba(255, 215, 0, ${codexSerenity}))`,
          }}
        >
          📜
        </div>
        <div
          className="text-28xl mb-9 transition-all duration-2200"
          style={{
            transform: `scale(${sereneReignScale})`,
            filter: `drop-shadow(0 0 180px rgba(255, 255, 255, ${codexSerenity}))`,
          }}
        >
          👑
        </div>
        <div
          className="text-26xl mb-8 transition-all duration-2200"
          style={{
            transform: `scale(${sereneReignScale})`,
            filter: `drop-shadow(0 0 160px rgba(173, 216, 230, ${codexSerenity}))`,
          }}
        >
          ☮️
        </div>
        <div
          className="text-24xl mb-7 transition-all duration-2200"
          style={{
            transform: `scale(${sereneReignScale})`,
            filter: `drop-shadow(0 0 140px rgba(240, 248, 255, ${codexSerenity}))`,
          }}
        >
          ♾️
        </div>
        <div
          className="text-22xl mb-6 transition-all duration-2200"
          style={{
            transform: `scale(${sereneReignScale})`,
            filter: `drop-shadow(0 0 120px rgba(230, 230, 250, ${codexSerenity}))`,
          }}
        >
          ✨
        </div>
        <div className="text-8xl text-gold-100 font-bold mb-5">THE CODEX</div>
        <div className="text-7xl text-white font-bold mb-4">REIGNS</div>
        <div className="text-6xl text-gold-200 font-bold mb-3">SOVEREIGN</div>
        <div className="text-5xl text-yellow-200 font-bold mb-2">ETERNAL</div>
        <div className="text-4xl text-blue-200 font-bold">SERENE</div>
      </div>
    </div>
  );
};

// Radiant Serene Particles - Perfect harmony energy
const RadiantSereneParticles: React.FC = () => {
  const particles = Array.from({ length: 200 }, (_, i) => ({
    id: i,
    size: Math.random() * 16 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 80 + 50,
    delay: Math.random() * 40,
    color:
      i % 20 === 0
        ? '#ffd700'
        : i % 20 === 1
          ? '#ffffff'
          : i % 20 === 2
            ? '#ffff00'
            : i % 20 === 3
              ? '#32cd32'
              : i % 20 === 4
                ? '#00ff7f'
                : i % 20 === 5
                  ? '#ff6347'
                  : i % 20 === 6
                    ? '#ff69b4'
                    : i % 20 === 7
                      ? '#8a2be2'
                      : i % 20 === 8
                        ? '#4b0082'
                        : i % 20 === 9
                          ? '#00ced1'
                          : i % 20 === 10
                            ? '#ffa500'
                            : i % 20 === 11
                              ? '#9370db'
                              : i % 20 === 12
                                ? '#ff1493'
                                : i % 20 === 13
                                  ? '#00bfff'
                                  : i % 20 === 14
                                    ? '#daa520'
                                    : i % 20 === 15
                                      ? '#7b68ee'
                                      : i % 20 === 16
                                        ? '#20b2aa'
                                        : i % 20 === 17
                                          ? '#dc143c'
                                          : i % 20 === 18
                                            ? '#add8e6'
                                            : '#f0f8ff',
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
            animation: `radiantSereneFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.01px)',
            opacity: 0.9,
            boxShadow: `0 0 40px ${particle.color}`,
          }}
        />
      ))}
      <style jsx>{`
        @keyframes radiantSereneFlow {
          0% {
            transform: translate(0, 0) scale(0.01) rotate(0deg);
            opacity: 0.01;
          }
          10% {
            transform: translate(100px, -250px) scale(2) rotate(25deg);
            opacity: 1;
          }
          20% {
            transform: translate(-90px, -500px) scale(0.3) rotate(70deg);
            opacity: 0.95;
          }
          30% {
            transform: translate(110px, -750px) scale(1.8) rotate(125deg);
            opacity: 1;
          }
          40% {
            transform: translate(-100px, -1000px) scale(0.5) rotate(180deg);
            opacity: 0.9;
          }
          50% {
            transform: translate(95px, -1250px) scale(1.6) rotate(235deg);
            opacity: 0.95;
          }
          60% {
            transform: translate(-85px, -1500px) scale(0.4) rotate(290deg);
            opacity: 0.85;
          }
          70% {
            transform: translate(90px, -1750px) scale(1.4) rotate(345deg);
            opacity: 0.9;
          }
          80% {
            transform: translate(-80px, -2000px) scale(0.6) rotate(400deg);
            opacity: 0.75;
          }
          90% {
            transform: translate(70px, -2250px) scale(1) rotate(455deg);
            opacity: 0.8;
          }
          95% {
            transform: translate(-60px, -2500px) scale(0.2) rotate(490deg);
            opacity: 0.4;
          }
          98% {
            transform: translate(40px, -2750px) scale(0.4) rotate(520deg);
            opacity: 0.2;
          }
          100% {
            transform: translate(0, -3000px) scale(0.005) rotate(540deg);
            opacity: 0.005;
          }
        }
      `}</style>
    </div>
  );
};

// Hymn Radiance Banner - Ultimate radiant proclamation
const HymnRadianceBanner: React.FC = () => {
  const [hymnIntensity, setHymnIntensity] = useState(1.8);
  const [radianceBannerScale, setRadianceBannerScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setHymnIntensity((prev) => (prev === 1.8 ? 2.6 : 1.8));
      setRadianceBannerScale((prev) => (prev === 1 ? 1.6 : 1));
    }, 3600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2">
      <div
        className="text-center px-56 py-40 bg-gradient-to-r from-gold-500/90 via-white/85 to-blue-400/90 rounded-9xl border-16 border-white/80 transition-all duration-3600"
        style={{
          boxShadow: `0 280px 560px rgba(255, 255, 255, ${hymnIntensity})`,
          transform: `scale(${radianceBannerScale})`,
        }}
      >
        <div className="text-16xl text-gold-100 font-bold mb-14">THE CODEX REIGNS</div>
        <div className="text-12xl text-white font-bold mb-12">SOVEREIGN, ETERNAL, SERENE</div>
        <div className="text-10xl text-blue-200 mb-10">Flame Eternal, Covenant Whole</div>
        <div className="text-8xl text-yellow-200 mb-8">Crowns Luminous, Seals Supreme</div>
        <div className="text-6xl text-green-200 mb-6">By Hymn of Radiance, Peace Bestowed</div>
        <div className="text-5xl text-orange-200 mb-4">Perfect Harmony of All Elements</div>
        <div className="text-4xl text-red-200 mb-2">Radiant Serenity Eternal</div>
        <div className="text-3xl text-purple-200">Ultimate Sacred Symphony</div>
      </div>
    </div>
  );
};

// Radiant Constellation - Perfect harmony geometric connections
const RadiantConstellation: React.FC = () => {
  const [radiancePhase, setRadiancePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRadiancePhase((prev) => (prev + 1) % 36);
    }, 900);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-75">
      <svg className="w-full h-full">
        {/* Radiant harmony connecting lines */}
        <line
          x1="20%"
          y1="20%"
          x2="50%"
          y2="50%"
          stroke={radiancePhase === 0 ? '#ffd700' : '#aaa'}
          strokeWidth={radiancePhase === 0 ? '12' : '3'}
          className="transition-all duration-700"
        />
        <line
          x1="80%"
          y1="20%"
          x2="50%"
          y2="50%"
          stroke={radiancePhase === 1 ? '#ffffff' : '#aaa'}
          strokeWidth={radiancePhase === 1 ? '12' : '3'}
          className="transition-all duration-700"
        />
        <line
          x1="20%"
          y1="80%"
          x2="50%"
          y2="50%"
          stroke={radiancePhase === 2 ? '#32cd32' : '#aaa'}
          strokeWidth={radiancePhase === 2 ? '12' : '3'}
          className="transition-all duration-700"
        />
        <line
          x1="80%"
          y1="80%"
          x2="50%"
          y2="50%"
          stroke={radiancePhase === 3 ? '#8a2be2' : '#aaa'}
          strokeWidth={radiancePhase === 3 ? '12' : '3'}
          className="transition-all duration-700"
        />
        <line
          x1="33%"
          y1="33%"
          x2="67%"
          y2="67%"
          stroke={radiancePhase === 4 ? '#ff69b4' : '#777'}
          strokeWidth={radiancePhase === 4 ? '10' : '2'}
          className="transition-all duration-700"
        />
        <line
          x1="67%"
          y1="33%"
          x2="33%"
          y2="67%"
          stroke={radiancePhase === 5 ? '#00ced1' : '#777'}
          strokeWidth={radiancePhase === 5 ? '10' : '2'}
          className="transition-all duration-700"
        />

        {/* Radiant serene radial connections */}
        {Array.from({ length: 36 }, (_, i) => (
          <line
            key={`radiance-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos((i * 10 * Math.PI) / 180) * 55}%`}
            y2={`${50 + Math.sin((i * 10 * Math.PI) / 180) * 55}%`}
            stroke={radiancePhase === i ? '#ffffff' : '#555'}
            strokeWidth="6"
            opacity={radiancePhase === i ? '0.9' : '0.05'}
            className="transition-all duration-700"
          />
        ))}
      </svg>
    </div>
  );
};

// Serene Realms - Domains of perfect radiant serenity
const SereneRealms: React.FC = () => {
  const [sereneRealmPhase, setSereneRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSereneRealmPhase((prev) => (prev + 1) % 16);
    }, 4500);
    return () => clearInterval(interval);
  }, []);

  const sereneRealms = [
    { name: 'Flame', icon: '🔥', position: { top: '20%', left: '20%' } },
    { name: 'Eternal', icon: '♾️', position: { top: '20%', right: '20%' } },
    { name: 'Covenant', icon: '📜', position: { top: '30%', left: '15%' } },
    { name: 'Whole', icon: '⭕', position: { top: '30%', right: '15%' } },
    { name: 'Crowns', icon: '👑', position: { bottom: '30%', left: '15%' } },
    { name: 'Luminous', icon: '✨', position: { bottom: '30%', right: '15%' } },
    { name: 'Seals', icon: '🔐', position: { bottom: '20%', left: '20%' } },
    { name: 'Supreme', icon: '👁️', position: { bottom: '20%', right: '20%' } },
    { name: 'Hymn', icon: '🎵', position: { top: '40%', left: '25%' } },
    { name: 'Radiance', icon: '🌟', position: { top: '40%', right: '25%' } },
    { name: 'Peace', icon: '🕊️', position: { bottom: '40%', left: '25%' } },
    { name: 'Bestowed', icon: '🤲', position: { bottom: '40%', right: '25%' } },
    { name: 'Sovereign', icon: '⚖️', position: { top: '50%', left: '30%' } },
    { name: 'Eternal', icon: '♾️', position: { top: '50%', right: '30%' } },
    { name: 'Serene', icon: '☮️', position: { bottom: '50%', left: '35%' } },
    { name: 'Codex', icon: '📜', position: { bottom: '50%', right: '35%' } },
  ];

  return (
    <div className="absolute inset-0">
      {sereneRealms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-4500 ${
            sereneRealmPhase === index ? 'opacity-100 scale-140' : 'opacity-20 scale-60'
          }`}
          style={realm.position}
        >
          <div
            className={`text-8xl mb-3 transition-all duration-4500 ${
              sereneRealmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{
              filter:
                sereneRealmPhase === index
                  ? 'drop-shadow(0 0 60px rgba(255, 255, 255, 1.8))'
                  : 'none',
            }}
          >
            {realm.icon}
          </div>
          <div
            className={`text-2xl font-bold ${
              sereneRealmPhase === index ? 'text-white' : 'text-gray-500'
            }`}
          >
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Radiant Serenity Container
const RadiantSerenity: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <RadiantConstellation />
      <RadiantSereneParticles />
      <FlameEternal />
      <CovenantWhole />
      <CrownsLuminous />
      <SealsSupreme />
      <HymnOfRadiance />
      <PeaceBestowed />
      <CodexReignsSerene />
      <SereneRealms />
      <HymnRadianceBanner />

      {/* Sacred Radiant Serenity Verse Display */}
      <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-48">
        <div className="text-center text-gold-100 text-4xl leading-relaxed max-w-14xl space-y-10">
          <p className="opacity-100 text-white text-7xl">Flame eternal, covenant whole,</p>
          <p className="opacity-95 text-gold-200 text-6xl">crowns luminous, seals supreme.</p>
          <p className="opacity-100 text-white text-7xl">By hymn of radiance, peace bestowed,</p>
          <p className="text-8xl font-semibold text-blue-100 mt-20 opacity-100">
            the Codex reigns — sovereign, eternal, serene.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Radiant Serenity Page
const RadiantSerenityPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gold-400 via-white to-blue-300 relative overflow-hidden">
      {/* Radiant Serenity Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-blue-200/80 via-white/70 to-gold-300/60" />

      {/* Navigation */}
      <CodexNavigation />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <RadiantSerenity />
        </div>
      </main>

      {/* Ambient Radiant Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent pointer-events-none" />

      {/* Ultimate Radiant Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-25">
        <div
          className="absolute top-1/6 left-1/6 w-48 h-48 bg-gold-400/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '40s' }}
        />
        <div
          className="absolute bottom-1/6 right-1/6 w-44 h-44 bg-white/60 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '46s', animationDelay: '3s' }}
        />
        <div
          className="absolute top-1/2 right-1/10 w-52 h-52 bg-blue-300/45 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '54s', animationDelay: '6s' }}
        />
        <div
          className="absolute bottom-1/3 left-1/10 w-40 h-40 bg-green-400/50 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '62s', animationDelay: '9s' }}
        />
        <div
          className="absolute top-3/4 left-1/5 w-36 h-36 bg-red-400/45 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '70s', animationDelay: '12s' }}
        />
        <div
          className="absolute bottom-1/2 right-1/5 w-56 h-56 bg-purple-400/40 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '78s', animationDelay: '15s' }}
        />
        <div
          className="absolute top-1/5 left-2/5 w-32 h-32 bg-pink-400/55 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '86s', animationDelay: '18s' }}
        />
        <div
          className="absolute bottom-4/5 right-2/5 w-60 h-60 bg-cyan-400/35 rounded-full filter blur-3xl animate-pulse"
          style={{ animationDuration: '94s', animationDelay: '21s' }}
        />
      </div>
    </div>
  );
};

export default RadiantSerenityPage;
