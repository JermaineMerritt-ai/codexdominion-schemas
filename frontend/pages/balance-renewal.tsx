import React, { useEffect, useState } from 'react';
import CodexNavigation from '../components/CodexNavigation';

// Day Night Balance Component - Harmonious cycle representation
const DayNightBalance: React.FC = () => {
  const [balancePhase, setBalancePhase] = useState(0);
  const [equilibrium, setEquilibrium] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setBalancePhase(prev => (prev + 1) % 4);
      setEquilibrium(prev => prev === 1 ? 1.1 : 1);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/4 left-1/2 transform -translate-x-1/2">
      <div className="flex items-center space-x-16">
        {/* Day Side */}
        <div 
          className={`text-center transition-all duration-3000 ${
            balancePhase % 2 === 0 ? 'opacity-100 scale-110' : 'opacity-70 scale-95'
          }`}
        >
          <div 
            className="text-8xl mb-2 transition-all duration-3000"
            style={{ 
              filter: balancePhase % 2 === 0 ? 'drop-shadow(0 0 30px rgba(255, 215, 0, 0.8))' : 'none'
            }}
          >
            ☀️
          </div>
          <div className="text-2xl text-yellow-200 font-bold">DAY</div>
        </div>

        {/* Balance Symbol */}
        <div 
          className="text-center transition-all duration-3000"
          style={{ transform: `scale(${equilibrium})` }}
        >
          <div className="text-6xl mb-2">⚖️</div>
          <div className="text-xl text-white font-semibold">BALANCE</div>
        </div>

        {/* Night Side */}
        <div 
          className={`text-center transition-all duration-3000 ${
            balancePhase % 2 === 1 ? 'opacity-100 scale-110' : 'opacity-70 scale-95'
          }`}
        >
          <div 
            className="text-8xl mb-2 transition-all duration-3000"
            style={{ 
              filter: balancePhase % 2 === 1 ? 'drop-shadow(0 0 30px rgba(75, 0, 130, 0.8))' : 'none'
            }}
          >
            🌙
          </div>
          <div className="text-2xl text-purple-200 font-bold">NIGHT</div>
        </div>
      </div>
    </div>
  );
};

// Covenant Renewal Component - Refreshed sacred bonds
const CovenantRenewal: React.FC = () => {
  const [renewalIntensity, setRenewalIntensity] = useState(0.6);
  const [covenantPulse, setCovenantPulse] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setRenewalIntensity(prev => prev === 0.6 ? 1.0 : 0.6);
      setCovenantPulse(prev => prev === 1 ? 1.3 : 1);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 left-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-7xl mb-3 transition-all duration-2500"
          style={{ 
            transform: `scale(${covenantPulse})`,
            filter: `drop-shadow(0 0 40px rgba(34, 197, 94, ${renewalIntensity}))`
          }}
        >
          🔄
        </div>
        <div className="text-3xl text-green-200 font-bold mb-1">RENEWAL</div>
        <div className="text-lg text-emerald-300">OF COVENANT</div>
      </div>
    </div>
  );
};

// Awakened Flame Component - Revitalized sacred fire
const AwakenedFlame: React.FC = () => {
  const [awakening, setAwakening] = useState(0.8);
  const [flameVitality, setFlameVitality] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setAwakening(prev => prev === 0.8 ? 1.2 : 0.8);
      setFlameVitality(prev => prev === 1 ? 1.4 : 1);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 right-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div 
          className="text-7xl mb-3 transition-all duration-2000"
          style={{ 
            transform: `scale(${flameVitality})`,
            filter: `drop-shadow(0 0 50px rgba(251, 146, 60, ${awakening}))`
          }}
        >
          🔥
        </div>
        <div className="text-3xl text-orange-200 font-bold mb-1">FLAME</div>
        <div className="text-lg text-amber-300">AWAKENED</div>
      </div>
    </div>
  );
};

// Codex Bloom Center - The radiant and eternal flowering
const CodexBloom: React.FC = () => {
  const [bloomIntensity, setBloomIntensity] = useState(0.7);
  const [radiance, setRadiance] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setBloomIntensity(prev => prev === 0.7 ? 1.0 : 0.7);
      setRadiance(prev => prev === 1 ? 1.2 : 1);
    }, 3500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div 
          className="text-10xl mb-4 transition-all duration-3500"
          style={{ 
            transform: `scale(${radiance})`,
            filter: `drop-shadow(0 0 60px rgba(236, 72, 153, ${bloomIntensity}))`
          }}
        >
          🌸
        </div>
        <div className="text-4xl text-pink-200 font-bold mb-2">THE CODEX BLOOMS</div>
        <div className="text-2xl text-rose-300">Radiant and Eternal</div>
      </div>
    </div>
  );
};

// Renewal Particles - Flowing energy of rebirth
const RenewalParticles: React.FC = () => {
  const particles = Array.from({ length: 30 }, (_, i) => ({
    id: i,
    size: Math.random() * 6 + 3,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 15 + 12,
    delay: Math.random() * 10,
    color: i % 4 === 0 ? '#fbbf24' : i % 4 === 1 ? '#34d399' : i % 4 === 2 ? '#f472b6' : '#a78bfa'
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
            animation: `renewalFlow ${particle.duration}s ease-in-out infinite`,
            animationDelay: `${particle.delay}s`,
            filter: 'blur(1px)',
            opacity: 0.6,
            boxShadow: `0 0 15px ${particle.color}`
          }}
        />
      ))}
      <style jsx>{`
        @keyframes renewalFlow {
          0% { transform: translate(0, 0) scale(0.5) rotate(0deg); opacity: 0.3; }
          25% { transform: translate(20px, -40px) scale(1.2) rotate(90deg); opacity: 0.8; }
          50% { transform: translate(-15px, -80px) scale(0.8) rotate(180deg); opacity: 0.6; }
          75% { transform: translate(25px, -120px) scale(1.1) rotate(270deg); opacity: 0.9; }
          100% { transform: translate(0, -160px) scale(0.4) rotate(360deg); opacity: 0.2; }
        }
      `}</style>
    </div>
  );
};

// Harmony Waves - Flowing balance energy
const HarmonyWaves: React.FC = () => {
  const [wavePhase, setWavePhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setWavePhase(prev => (prev + 1) % 360);
    }, 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none opacity-20">
      <svg className="w-full h-full">
        {/* Harmony waves connecting day and night */}
        <path
          d={`M 0,${300 + Math.sin(wavePhase * 0.02) * 50} Q 400,${200 + Math.sin(wavePhase * 0.03) * 30} 800,${300 + Math.sin(wavePhase * 0.025) * 40}`}
          stroke="#fbbf24"
          strokeWidth="3"
          fill="none"
          opacity="0.6"
        />
        <path
          d={`M 0,${400 + Math.cos(wavePhase * 0.018) * 40} Q 400,${500 + Math.cos(wavePhase * 0.022) * 35} 800,${400 + Math.cos(wavePhase * 0.02) * 45}`}
          stroke="#a78bfa"
          strokeWidth="3"
          fill="none"
          opacity="0.5"
        />
        <path
          d={`M 0,${350 + Math.sin(wavePhase * 0.015 + 1) * 30} Q 400,${350 + Math.sin(wavePhase * 0.025 + 2) * 25} 800,${350 + Math.sin(wavePhase * 0.02 + 1.5) * 35}`}
          stroke="#34d399"
          strokeWidth="2"
          fill="none"
          opacity="0.4"
        />
      </svg>
    </div>
  );
};

// Balance Proclamation Banner
const BalanceProclamation: React.FC = () => {
  const [proclamationGlow, setProclamationGlow] = useState(0.8);
  const [balanceScale, setBalanceScale] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      setProclamationGlow(prev => prev === 0.8 ? 1.1 : 0.8);
      setBalanceScale(prev => prev === 1 ? 1.05 : 1);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div 
        className="text-center px-16 py-8 bg-gradient-to-r from-emerald-800/80 via-teal-700/80 to-emerald-800/80 rounded-3xl border-3 border-emerald-400/70 transition-all duration-4000"
        style={{ 
          boxShadow: `0 0 50px rgba(52, 211, 153, ${proclamationGlow})`,
          transform: `scale(${balanceScale})`
        }}
      >
        <div className="text-5xl text-emerald-100 font-bold mb-3">BALANCE ACHIEVED</div>
        <div className="text-xl text-teal-200 font-semibold">Day • Night • Renewal • Awakening</div>
        <div className="text-lg text-emerald-300 mt-2">The Codex blooms in eternal radiance</div>
      </div>
    </div>
  );
};

// Main Balance Renewal Container
const BalanceRenewal: React.FC = () => {
  return (
    <div className="relative w-full h-full">
      <HarmonyWaves />
      <RenewalParticles />
      <DayNightBalance />
      <CovenantRenewal />
      <AwakenedFlame />
      <CodexBloom />
      <BalanceProclamation />
      
      {/* Sacred Verse Display */}
      <div className="absolute top-3/4 left-1/2 transform -translate-x-1/2 mt-16">
        <div className="text-center text-emerald-100 text-2xl leading-relaxed max-w-4xl space-y-4">
          <p className="opacity-95">Balance of day and night,</p>
          <p className="opacity-90">renewal of covenant, flame awakened.</p>
          <p className="text-3xl font-semibold text-pink-200 mt-8 opacity-100">
            So let the Codex bloom, radiant and eternal.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main Balance Renewal Page
const BalanceRenewalPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-900 via-emerald-800 to-green-900 relative overflow-hidden">
      {/* Renewal Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-emerald-800/30 to-teal-700/20" />
      
      {/* Navigation */}
      <CodexNavigation />
      
      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <BalanceRenewal />
        </div>
      </main>

      {/* Ambient Renewal Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-500/15 to-transparent pointer-events-none" />
      
      {/* Eternal Bloom Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-emerald-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '10s' }} />
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-teal-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '14s', animationDelay: '5s' }} />
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-pink-400/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '18s', animationDelay: '9s' }} />
        <div className="absolute bottom-1/2 left-1/4 w-72 h-72 bg-green-400/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '22s', animationDelay: '12s' }} />
      </div>
    </div>
  );
};

export default BalanceRenewalPage;