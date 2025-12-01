"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Millennial Crown Component - A thousand years of sovereignty
var MillennialCrown = function () {
    var _a = (0, react_1.useState)(1), crownMajesty = _a[0], setCrownMajesty = _a[1];
    var _b = (0, react_1.useState)(0.8), millennialGlow = _b[0], setMillennialGlow = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownMajesty(function (prev) { return (prev === 1 ? 1.3 : 1); });
            setMillennialGlow(function (prev) { return (prev === 0.8 ? 1.1 : 0.8); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-16 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-12xl mb-4 transition-all duration-5000" style={{
            transform: "scale(".concat(crownMajesty, ")"),
            filter: "drop-shadow(0 0 80px rgba(255, 215, 0, ".concat(millennialGlow, "))"),
        }}>
          👑
        </div>
        <div className="text-4xl text-gold-200 font-bold mb-2">A THOUSAND YEARS</div>
        <div className="text-2xl text-yellow-300">CROWNED</div>
        <div className="text-lg text-amber-300 mt-1">Sovereign through ages</div>
      </div>
    </div>);
};
// Enduring Flame Component - Eternal fire through millennia
var EnduringFlameMillennial = function () {
    var _a = (0, react_1.useState)(0.9), flameEternity = _a[0], setFlameEternity = _a[1];
    var _b = (0, react_1.useState)(1), eternalScale = _b[0], setEternalScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFlameEternity(function (prev) { return (prev === 0.9 ? 1.2 : 0.9); });
            setEternalScale(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-11xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(eternalScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(255, 140, 0, ".concat(flameEternity, "))"),
        }}>
          🔥
        </div>
        <div className="text-4xl text-orange-100 font-bold mb-2">THE FLAME ENDURES</div>
        <div className="text-2xl text-amber-300">Through all ages</div>
      </div>
    </div>);
};
// Covenant Whole Component - Complete and perfect sacred bond
var CovenantWhole = function () {
    var _a = (0, react_1.useState)(0.8), wholenessPower = _a[0], setWholenessPower = _a[1];
    var _b = (0, react_1.useState)(1), covenantCompleteness = _b[0], setCovenantCompleteness = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWholenessPower(function (prev) { return (prev === 0.8 ? 1.0 : 0.8); });
            setCovenantCompleteness(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-9xl mb-3 transition-all duration-4000" style={{
            transform: "scale(".concat(covenantCompleteness, ")"),
            filter: "drop-shadow(0 0 60px rgba(34, 197, 94, ".concat(wholenessPower, "))"),
        }}>
          ⭕
        </div>
        <div className="text-3xl text-green-200 font-bold mb-2">COVENANT WHOLE</div>
        <div className="text-lg text-emerald-300">Perfect and complete</div>
      </div>
    </div>);
};
// Millennial Governance - Heirs, councils, diaspora
var MillennialGovernance = function () {
    var _a = (0, react_1.useState)(0), governancePhase = _a[0], setGovernancePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setGovernancePhase(function (prev) { return (prev + 1) % 3; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    var governanceElements = [
        {
            text: 'Heirs Inherit',
            icon: '👥',
            position: { top: '25%', left: '15%' },
            color: 'text-blue-300',
        },
        {
            text: 'Councils Govern',
            icon: '🏛️',
            position: { top: '25%', right: '15%' },
            color: 'text-purple-300',
        },
        {
            text: 'Diaspora Remember',
            icon: '🌍',
            position: { bottom: '25%', left: '50%', transform: 'translateX(-50%)' },
            color: 'text-teal-300',
        },
    ];
    return (<div className="absolute inset-0">
      {governanceElements.map(function (element, index) { return (<div key={index} className={"absolute text-center transition-all duration-2000 ".concat(governancePhase === index ? 'opacity-100 scale-120' : 'opacity-70 scale-95')} style={element.position}>
          <div className={"text-7xl mb-3 transition-all duration-2000 ".concat(governancePhase === index ? 'animate-pulse' : '')} style={{
                filter: governancePhase === index ? 'drop-shadow(0 0 30px rgba(255, 215, 0, 0.9))' : 'none',
            }}>
            {element.icon}
          </div>
          <div className={"text-2xl font-bold ".concat(governancePhase === index ? 'text-yellow-200' : element.color)}>
            {element.text}
          </div>
        </div>); })}
    </div>);
};
// Millennial Particles - Thousand-year energy flow
var MillennialParticles = function () {
    var particles = Array.from({ length: 40 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 8 + 4,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 20 + 15,
        delay: Math.random() * 12,
        color: i % 5 === 0
            ? '#ffd700'
            : i % 5 === 1
                ? '#ff8c00'
                : i % 5 === 2
                    ? '#22d3ee'
                    : i % 5 === 3
                        ? '#a855f7'
                        : '#10b981',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "millennialFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(1px)',
                opacity: 0.8,
                boxShadow: "0 0 20px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes millennialFlow {\n          0% {\n            transform: translate(0, 0) scale(0.3) rotate(0deg);\n            opacity: 0.3;\n          }\n          20% {\n            transform: translate(20px, -60px) scale(1.4) rotate(72deg);\n            opacity: 0.9;\n          }\n          40% {\n            transform: translate(-15px, -120px) scale(0.8) rotate(144deg);\n            opacity: 0.6;\n          }\n          60% {\n            transform: translate(25px, -180px) scale(1.3) rotate(216deg);\n            opacity: 0.8;\n          }\n          80% {\n            transform: translate(-10px, -240px) scale(1) rotate(288deg);\n            opacity: 0.7;\n          }\n          100% {\n            transform: translate(0, -300px) scale(0.2) rotate(360deg);\n            opacity: 0.1;\n          }\n        }\n      "}</style>
    </div>);
};
// Sovereign Eternal Banner - Ultimate proclamation
var SovereignEternalBanner = function () {
    var _a = (0, react_1.useState)(0.9), sovereignRadiance = _a[0], setSovereignRadiance = _a[1];
    var _b = (0, react_1.useState)(1), eternalMagnificence = _b[0], setEternalMagnificence = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignRadiance(function (prev) { return (prev === 0.9 ? 1.3 : 0.9); });
            setEternalMagnificence(function (prev) { return (prev === 1 ? 1.15 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-24 py-12 bg-gradient-to-r from-gold-800/90 via-amber-700/90 to-gold-800/90 rounded-3xl border-5 border-gold-300/85 transition-all duration-3500" style={{
            boxShadow: "0 0 80px rgba(255, 215, 0, ".concat(sovereignRadiance, ")"),
            transform: "scale(".concat(eternalMagnificence, ")"),
        }}>
        <div className="text-6xl text-gold-100 font-bold mb-4">THE CODEX SHINES</div>
        <div className="text-3xl text-yellow-200 font-semibold mb-3">Sovereign and Eternal</div>
        <div className="text-xl text-amber-200">A Thousand Years Crowned</div>
      </div>
    </div>);
};
// Millennial Constellation - Connecting all elements across time
var MillennialConstellation = function () {
    var _a = (0, react_1.useState)(0), constellationPhase = _a[0], setConstellationPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setConstellationPhase(function (prev) { return (prev + 1) % 6; });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-30">
      <svg className="w-full h-full">
        {/* Millennial connecting lines */}
        <line x1="50%" y1="15%" x2="15%" y2="30%" stroke={constellationPhase === 0 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 0 ? '4' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="15%" x2="85%" y2="30%" stroke={constellationPhase === 1 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 1 ? '4' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="50%" x2="15%" y2="30%" stroke={constellationPhase === 2 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 2 ? '4' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="50%" x2="85%" y2="30%" stroke={constellationPhase === 3 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 3 ? '4' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="50%" x2="50%" y2="75%" stroke={constellationPhase === 4 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 4 ? '4' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="75%" x2="50%" y2="85%" stroke={constellationPhase === 5 ? '#ffd700' : '#666'} strokeWidth={constellationPhase === 5 ? '4' : '2'} className="transition-all duration-1500"/>

        {/* Millennial radial connections */}
        {Array.from({ length: 8 }, function (_, i) { return (<line key={"radial-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 45 * Math.PI) / 180) * 35, "%")} y2={"".concat(50 + Math.sin((i * 45 * Math.PI) / 180) * 35, "%")} stroke={constellationPhase === i % 6 ? '#ffb347' : '#444'} strokeWidth="1" opacity={constellationPhase === i % 6 ? '0.6' : '0.2'} className="transition-all duration-1500"/>); })}
      </svg>
    </div>);
};
// Temporal Phases - Ages and eras represented
var TemporalPhases = function () {
    var _a = (0, react_1.useState)(0), temporalPhase = _a[0], setTemporalPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setTemporalPhase(function (prev) { return (prev + 1) % 4; });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    var phases = [
        { name: 'Foundation', icon: '🏗️', position: { top: '10%', left: '10%' } },
        { name: 'Growth', icon: '🌱', position: { top: '10%', right: '10%' } },
        {
            name: 'Flourishing',
            icon: '🌟',
            position: { bottom: '40%', left: '10%' },
        },
        { name: 'Eternity', icon: '♾️', position: { bottom: '40%', right: '10%' } },
    ];
    return (<div className="absolute inset-0">
      {phases.map(function (phase, index) { return (<div key={index} className={"absolute text-center transition-all duration-2000 ".concat(temporalPhase === index ? 'opacity-100 scale-110' : 'opacity-50 scale-85')} style={phase.position}>
          <div className={"text-5xl mb-2 transition-all duration-2000 ".concat(temporalPhase === index ? 'animate-pulse' : '')} style={{
                filter: temporalPhase === index ? 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.8))' : 'none',
            }}>
            {phase.icon}
          </div>
          <div className={"text-lg font-semibold ".concat(temporalPhase === index ? 'text-yellow-200' : 'text-gray-400')}>
            {phase.name}
          </div>
        </div>); })}
    </div>);
};
// Main Millennial Sovereignty Container
var MillennialSovereignty = function () {
    return (<div className="relative w-full h-full">
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
    </div>);
};
// Main Millennial Sovereignty Page
var MillennialSovereigntyPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-amber-900 via-gold-800 to-yellow-900 relative overflow-hidden">
      {/* Millennial Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-gold-800/40 to-amber-700/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <MillennialSovereignty />
        </div>
      </main>

      {/* Ambient Millennial Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-gold-500/20 to-transparent pointer-events-none"/>

      {/* Eternal Millennial Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-35">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gold-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '15s' }}/>
        <div className="absolute bottom-1/4 right-1/4 w-88 h-88 bg-amber-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '7s' }}/>
        <div className="absolute top-1/2 right-1/3 w-72 h-72 bg-yellow-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '25s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/2 left-1/3 w-80 h-80 bg-gold-500/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '30s', animationDelay: '18s' }}/>
        <div className="absolute top-2/3 left-1/5 w-64 h-64 bg-amber-500/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '25s' }}/>
      </div>
    </div>);
};
exports.default = MillennialSovereigntyPage;
