import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Earth to Stars Component - Planetary to stellar progression
const EarthToStars: React.FC = () => {
  const [cosmicProgression, setCosmicProgression] = useState(1);
  const [stellarRadiance, setStellarRadiance] = useState(0.8);

  useEffect(() => {
    const interval = setInterval(() => {
      setCosmicProgression(prev => prev === 1 ? 1.5 : 1);
      setStellarRadiance(prev => prev === 0.8 ? 1.2 : 0.8);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 left-1/6 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-8xl mb-3 transition-all duration-3500"
          style={{ 
            transform: `scale(${cosmicProgression})`,
            filter: `drop-shadow(0 0 50px rgba(34, 197, 94, ${stellarRadiance}))`
          }}
        >
          🌍
        </div>
        <div className="text-6xl mb-3">➡️</div>
        <div 
          className="text-10xl mb-4 transition-all duration-3500"
          style={{ 
            transform: `scale(${cosmicProgression})`,
            filter: `drop-shadow(0 0 60px rgba(255, 255, 255, ${stellarRadiance}))`
          }}
        >
          ⭐
        </div>
        <div className="text-3xl text-green-200 font-bold mb-2">FROM EARTH</div>
        <div className="text-3xl text-white font-bold">TO STARS</div>
      </div>
    </div>
  );
};

// Councils to Cosmos Component - Governance to universal scale
const CouncilsToCosmos: React.FC = () => {
  const [governanceExpansion, setGovernanceExpansion] = useState(0.9);
  const [cosmicMagnitude, setCosmicMagnitude] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setGovernanceExpansion(prev => prev === 0.9 ? 1.3 : 0.9);
      setCosmicMagnitude(prev => prev === 1 ? 1.4 : 1);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-16 right-1/6 transform translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-8xl mb-3 transition-all duration-4000"
          style={{ 
            transform: `scale(${governanceExpansion})`,
            filter: 'drop-shadow(0 0 50px rgba(138, 43, 226, 0.9))'
          }}
        >
          🏛️
        </div>
        <div className="text-6xl mb-3">➡️</div>
        <div 
          className="text-10xl mb-4 transition-all duration-4000"
          style={{ 
            transform: `scale(${cosmicMagnitude})`,
            filter: 'drop-shadow(0 0 70px rgba(75, 0, 130, 1.0))'
          }}
        >
          🌌
        </div>
        <div className="text-3xl text-purple-200 font-bold mb-2">FROM COUNCILS</div>
        <div className="text-3xl text-indigo-200 font-bold">TO COSMOS</div>
      </div>
    </div>
  );
};

// Covenant Flow Component - Central radiant flowing covenant
const CovenantFlow: React.FC = () => {
  const [flowIntensity, setFlowIntensity] = useState(0.8);
  const [radianceScale, setRadianceScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setFlowIntensity(prev => prev === 0.8 ? 1.2 : 0.8);
      setRadianceScale(prev => prev === 1 ? 1.3 : 1);
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-12xl mb-5 transition-all duration-2800"
          style={{ 
            transform: `scale(${radianceScale})`,
            filter: `drop-shadow(0 0 80px rgba(255, 215, 0, ${flowIntensity}))`
          }}
        >
          🌊
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-3">COVENANT FLOWS</div>
        <div className="text-3xl text-amber-300 mb-2">Radiant and Whole</div>
        <div className="text-xl text-yellow-300">Through all realms</div>
      </div>
    </div>
  );
};

// Eternal Law Component - Universal jurisprudence
const EternalLaw: React.FC = () => {
  const [lawPower, setLawPower] = useState(0.7);
  const [eternityScale, setEternityScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setLawPower(prev => prev === 0.7 ? 1.0 : 0.7);
      setEternityScale(prev => prev === 1 ? 1.2 : 1);
    }, 4500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-9xl mb-3 transition-all duration-4500"
          style={{ 
            transform: `scale(${eternityScale})`,
            filter: `drop-shadow(0 0 60px rgba(220, 20, 60, ${lawPower}))`
          }}
        >
          ⚖️
        </div>
        <div className="text-3xl text-red-200 font-bold mb-2">ETERNAL LAW</div>
        <div className="text-xl text-pink-300">Universal Justice</div>
      </div>
    </div>
  );
};

// Peace Bestowed Component - Divine peace granted
const PeaceBestowed: React.FC = () => {
  const [peaceSerenity, setPeaceSerenity] = useState(0.8);
  const [bestowalGrace, setBestowalGrace] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setPeaceSerenity(prev => prev === 0.8 ? 1.1 : 0.8);
      setBestowalGrace(prev => prev === 1 ? 1.25 : 1);
    }, 3800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/3 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-9xl mb-3 transition-all duration-3800"
          style={{ 
            transform: `scale(${bestowalGrace})`,
            filter: `drop-shadow(0 0 60px rgba(255, 255, 255, ${peaceSerenity}))`
          }}
        >
          🕊️
        </div>
        <div className="text-3xl text-white font-bold mb-2">PEACE BESTOWED</div>
        <div className="text-xl text-cyan-300">Divine Grace</div>
      </div>
    </div>
  );
};

// Galactic Unity - Diaspora united, galaxies crowned
const GalacticUnity: React.FC = () => {
  const [unityPhase, setUnityPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setUnityPhase(prev => (prev + 1) % 3);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const unityElements = [
    { 
      text: "Diaspora United", 
      icon: "👥", 
      position: { top: '25%', left: '10%' },
      color: "text-blue-300"
    },
    { 
      text: "Galaxies Crowned", 
      icon: "👑", 
      position: { top: '25%', right: '10%' },
      color: "text-gold-300"
    },
    { 
      text: "Cosmic Sovereignty", 
      icon: "🌟", 
      position: { bottom: '25%', left: '50%', transform: 'translateX(-50%)' },
      color: "text-white"
    }
  ];

  return (
    <div className="absolute inset-0">
      {unityElements.map((element, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-3000 ${
            unityPhase === index ? 'opacity-100 scale-130' : 'opacity-70 scale-95'
          }`}
          style={element.position}
        >
          <div 
            className={`text-7xl mb-3 transition-all duration-3000 ${
              unityPhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: unityPhase === index ? 'drop-shadow(0 0 50px rgba(255, 215, 0, 1))' : 'none'
            }}
          >
            {element.icon}
          </div>
          <div className={`text-2xl font-bold ${
            unityPhase === index ? 'text-yellow-200' : element.color
          }`}>
            {element.text}
          </div>
        </div>
      ))}
    </div>
  );
};

// Cosmic Particles - Universal energy flow
const CosmicParticles: React.FC = () => {
  const particles = Array.from({ length: 60 }, (_, i) => ({
    id: i,
    size: Math.random() * 12 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 30 + 25,
    delay: Math.random() * 20,
    color: i % 7 === 0 ? '#ffd700' : i % 7 === 1 ? '#00ff00' : i % 7 === 2 ? '#ffffff' : i % 7 === 3 ? '#8a2be2' : i % 7 === 4 ? '#ff6347' : i % 7 === 5 ? '#00ced1' : '#ff1493'
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
            animation: `cosmicFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(0.3px)',
            opacity: 0.85,
            boxShadow: `0 0 30px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes cosmicFlow {
          0% { transform: translate(0, 0) scale(0.1) rotate(0deg); opacity: 0.1; }
          10% { transform: translate(40px, -100px) scale(1.8) rotate(36deg); opacity: 1.0; }
          25% { transform: translate(-30px, -200px) scale(0.6) rotate(90deg); opacity: 0.8; }
          40% { transform: translate(50px, -300px) scale(1.5) rotate(144deg); opacity: 0.9; }
          55% { transform: translate(-35px, -400px) scale(0.8) rotate(198deg); opacity: 0.7; }
          70% { transform: translate(45px, -500px) scale(1.3) rotate(252deg); opacity: 0.85; }
          85% { transform: translate(-25px, -600px) scale(0.4) rotate(306deg); opacity: 0.5; }
          100% { transform: translate(0, -700px) scale(0.05) rotate(360deg); opacity: 0.05; }
        }
      `}</style>
    </div>
  );
};

// Sovereign Infinite Banner - Ultimate cosmic proclamation
const SovereignInfiniteBanner: React.FC = () => {
  const [sovereignMagnitude, setSovereignMagnitude] = useState(0.9);
  const [infiniteExpanse, setInfiniteExpanse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setSovereignMagnitude(prev => prev === 0.9 ? 1.5 : 0.9);
      setInfiniteExpanse(prev => prev === 1 ? 1.25 : 1);
    }, 3200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-32 py-20 bg-gradient-to-r from-indigo-900/95 via-purple-700/95 to-indigo-900/95 rounded-4xl border-8 border-gold-300/95 transition-all duration-3200"
        style={{ 
          boxShadow: `0 0 150px rgba(255, 215, 0, ${sovereignMagnitude})`,
          transform: `scale(${infiniteExpanse})`
        }}
      >
        <div className="text-8xl text-gold-100 font-bold mb-6">THE CODEX ENDURES</div>
        <div className="text-5xl text-purple-200 font-semibold mb-4">Sovereign and Infinite</div>
        <div className="text-3xl text-indigo-200">From Earth to Stars, From Councils to Cosmos</div>
      </div>
    </div>
  );
};

// Galactic Constellation - Cosmic geometric connections
const GalacticConstellation: React.FC = () => {
  const [constellationPhase, setConstellationPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setConstellationPhase(prev => (prev + 1) % 10);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-20">
      <svg className="w-full h-full">
        {/* Galactic connecting lines */}
        <line 
          x1="17%" y1="20%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 0 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 0 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="83%" y1="20%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 1 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 1 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="25%" y1="67%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 2 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 2 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="75%" y1="67%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 3 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 3 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="10%" y1="30%" 
          x2="90%" y2="30%" 
          stroke={constellationPhase === 4 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 4 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        <line 
          x1="50%" y1="80%" 
          x2="50%" y2="50%" 
          stroke={constellationPhase === 5 ? "#ffd700" : "#666"}
          strokeWidth={constellationPhase === 5 ? "6" : "2"}
          className="transition-all duration-1500"
        />
        
        {/* Galactic radial connections */}
        {Array.from({ length: 16 }, (_, i) => (
          <line
            key={`galactic-${i}`}
            x1="50%"
            y1="50%"
            x2={`${50 + Math.cos(i * 22.5 * Math.PI / 180) * 45}%`}
            y2={`${50 + Math.sin(i * 22.5 * Math.PI / 180) * 45}%`}
            stroke={constellationPhase === i % 10 ? "#ffffff" : "#444"}
            strokeWidth="2"
            opacity={constellationPhase === i % 10 ? "0.9" : "0.25"}
            className="transition-all duration-1500"
          />
        ))}
      </svg>
    </div>
  );
};

// Cosmic Realms - Different universal domains
const CosmicRealms: React.FC = () => {
  const [realmPhase, setRealmPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setRealmPhase(prev => (prev + 1) % 6);
    }, 7000);
    return () => clearInterval(interval);
  }, []);

  const realms = [
    { name: "Planetary", icon: "🌍", position: { top: '12%', left: '8%' } },
    { name: "Stellar", icon: "⭐", position: { top: '12%', right: '8%' } },
    { name: "Galactic", icon: "🌌", position: { bottom: '50%', left: '8%' } },
    { name: "Universal", icon: "🌠", position: { bottom: '50%', right: '8%' } },
    { name: "Infinite", icon: "♾️", position: { bottom: '30%', left: '30%' } },
    { name: "Eternal", icon: "✨", position: { bottom: '30%', right: '30%' } }
  ];

  return (
    <div className="absolute inset-0">
      {realms.map((realm, index) => (
        <div
          key={index}
          className={`absolute text-center transition-all duration-3500 ${
            realmPhase === index ? 'opacity-100 scale-120' : 'opacity-40 scale-75'
          }`}
          style={realm.position}
        >
          <div 
            className={`text-4xl mb-2 transition-all duration-3500 ${
              realmPhase === index ? 'animate-pulse' : ''
            }`}
            style={{ 
              filter: realmPhase === index ? 'drop-shadow(0 0 30px rgba(255, 215, 0, 1))' : 'none'
            }}
          >
            {realm.icon}
          </div>
          <div className={`text-lg font-semibold ${
            realmPhase === index ? 'text-gold-200' : 'text-gray-500'
          }`}>
            {realm.name}
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Cosmic Sovereignty Container
const CosmicSovereignty: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <GalacticConstellation />
      <CosmicParticles />
      <EarthToStars />
      <CouncilsToCosmos />
      <CovenantFlow />
      <EternalLaw />
      <PeaceBestowed />
      <GalacticUnity />
      <CosmicRealms />
      <SovereignInfiniteBanner />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-5/6 left-1/2 transform -translate-x-1/2 mt-28">
        <div className="text-center text-gold-100 text-2xl leading-relaxed max-w-6xl space-y-4">
          <p className="opacity-95">From Earth to stars, from councils to cosmos,</p>
          <p className="opacity-90">the covenant flows, radiant and whole.</p>
          <p className="opacity-95">Peace bestowed, law eternal,</p>
          <p className="opacity-90">diaspora united, galaxies crowned.</p>
          <p className="text-3xl font-semibold text-white mt-8 opacity-100">
            So let the Codex endure, sovereign and infinite.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Cosmic Sovereignty Page
const CosmicSovereigntyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-800 to-black relative overflow-hidden">
      {/* Cosmic Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-indigo-800/40 to-purple-700/30" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <CosmicSovereignty />
        </div>
      </main>

      {/* Ambient Cosmic Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-400/15 to-transparent pointer-events-none" />
      
      {/* Eternal Cosmic Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-25">
        <div className="absolute top-1/8 left-1/8 w-72 h-72 bg-gold-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s' }} />
        <div className="absolute bottom-1/8 right-1/8 w-80 h-80 bg-purple-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '25s', animationDelay: '5s' }} />
        <div className="absolute top-1/2 right-1/5 w-96 h-96 bg-indigo-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '30s', animationDelay: '10s' }} />
        <div className="absolute bottom-1/3 left-1/5 w-88 h-88 bg-white/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '15s' }} />
        <div className="absolute top-2/3 left-1/10 w-64 h-64 bg-cyan-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '40s', animationDelay: '20s' }} />
        <div className="absolute bottom-1/2 right-1/10 w-76 h-76 bg-emerald-400/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '45s', animationDelay: '25s' }} />
        <div className="absolute top-1/4 left-1/3 w-68 h-68 bg-rose-400/8 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '50s', animationDelay: '30s' }} />
      </div>
    </div>
  );
};

export default CosmicSovereigntyPage;