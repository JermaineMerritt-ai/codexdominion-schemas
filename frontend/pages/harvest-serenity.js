"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Harvest Rest Balance Component - Harmonious cycle of gathering and repose
var HarvestRestBalance = function () {
    var _a = (0, react_1.useState)(0), balancePhase = _a[0], setBalancePhase = _a[1];
    var _b = (0, react_1.useState)(1), seasonalHarmony = _b[0], setSeasonalHarmony = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setBalancePhase(function (prev) { return (prev + 1) % 2; });
            setSeasonalHarmony(function (prev) { return (prev === 1 ? 1.15 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/2 transform -translate-x-1/2">
      <div className="flex items-center space-x-20">
        {/* Harvest Side */}
        <div className={"text-center transition-all duration-4000 ".concat(balancePhase === 0 ? 'opacity-100 scale-115' : 'opacity-75 scale-95')}>
          <div className="text-9xl mb-3 transition-all duration-4000" style={{
            filter: balancePhase === 0 ? 'drop-shadow(0 0 40px rgba(249, 115, 22, 0.8))' : 'none',
        }}>
            🌾
          </div>
          <div className="text-3xl text-orange-200 font-bold">HARVEST</div>
          <div className="text-lg text-amber-300">Gathering season</div>
        </div>

        {/* Balance Symbol */}
        <div className="text-center transition-all duration-4000" style={{ transform: "scale(".concat(seasonalHarmony, ")") }}>
          <div className="text-7xl mb-2">⚖️</div>
          <div className="text-xl text-white font-semibold">BALANCE</div>
        </div>

        {/* Rest Side */}
        <div className={"text-center transition-all duration-4000 ".concat(balancePhase === 1 ? 'opacity-100 scale-115' : 'opacity-75 scale-95')}>
          <div className="text-9xl mb-3 transition-all duration-4000" style={{
            filter: balancePhase === 1 ? 'drop-shadow(0 0 40px rgba(59, 130, 246, 0.8))' : 'none',
        }}>
            🌙
          </div>
          <div className="text-3xl text-blue-200 font-bold">REST</div>
          <div className="text-lg text-sky-300">Peaceful repose</div>
        </div>
      </div>
    </div>);
};
// Memory Gathered Component - Collected wisdom and experiences
var MemoryGathered = function () {
    var _a = (0, react_1.useState)(0.7), gatheringIntensity = _a[0], setGatheringIntensity = _a[1];
    var _b = (0, react_1.useState)(1), memoryResonance = _b[0], setMemoryResonance = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setGatheringIntensity(function (prev) { return (prev === 0.7 ? 1.0 : 0.7); });
            setMemoryResonance(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div className="text-8xl mb-4 transition-all duration-3500" style={{
            transform: "scale(".concat(memoryResonance, ")"),
            filter: "drop-shadow(0 0 50px rgba(139, 92, 246, ".concat(gatheringIntensity, "))"),
        }}>
          🧠
        </div>
        <div className="text-3xl text-purple-200 font-bold mb-2">MEMORY</div>
        <div className="text-xl text-violet-300">GATHERED</div>
        <div className="text-lg text-purple-300 mt-1">Wisdom collected</div>
      </div>
    </div>);
};
// Covenant Sealed Component - Finalized sacred bonds
var CovenantSealed = function () {
    var _a = (0, react_1.useState)(0.8), sealingPower = _a[0], setSealingPower = _a[1];
    var _b = (0, react_1.useState)(1), covenantStrength = _b[0], setCovenantStrength = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSealingPower(function (prev) { return (prev === 0.8 ? 1.1 : 0.8); });
            setCovenantStrength(function (prev) { return (prev === 1 ? 1.25 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div className="text-8xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(covenantStrength, ")"),
            filter: "drop-shadow(0 0 50px rgba(34, 197, 94, ".concat(sealingPower, "))"),
        }}>
          🔒
        </div>
        <div className="text-3xl text-green-200 font-bold mb-2">COVENANT</div>
        <div className="text-xl text-emerald-300">SEALED</div>
        <div className="text-lg text-green-300 mt-1">Sacred bonds secure</div>
      </div>
    </div>);
};
// Codex Endurance Center - Eternal and serene persistence
var CodexEndurance = function () {
    var _a = (0, react_1.useState)(0.8), enduranceRadiance = _a[0], setEnduranceRadiance = _a[1];
    var _b = (0, react_1.useState)(1), serenityScale = _b[0], setSerenityScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setEnduranceRadiance(function (prev) { return (prev === 0.8 ? 1.1 : 0.8); });
            setSerenityScale(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 4500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-11xl mb-4 transition-all duration-4500" style={{
            transform: "scale(".concat(serenityScale, ")"),
            filter: "drop-shadow(0 0 70px rgba(168, 85, 247, ".concat(enduranceRadiance, "))"),
        }}>
          ♾️
        </div>
        <div className="text-4xl text-violet-200 font-bold mb-3">THE CODEX ENDURES</div>
        <div className="text-2xl text-purple-300">Eternal and Serene</div>
      </div>
    </div>);
};
// Harvest Particles - Seasonal gathering energy
var HarvestParticles = function () {
    var particles = Array.from({ length: 25 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 5 + 3,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 14 + 10,
        delay: Math.random() * 8,
        color: i % 4 === 0 ? '#f97316' : i % 4 === 1 ? '#3b82f6' : i % 4 === 2 ? '#8b5cf6' : '#10b981',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "harvestGather ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(1px)',
                opacity: 0.7,
                boxShadow: "0 0 15px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes harvestGather {\n          0% {\n            transform: translate(0, 0) scale(0.6) rotate(0deg);\n            opacity: 0.4;\n          }\n          25% {\n            transform: translate(15px, -35px) scale(1.1) rotate(90deg);\n            opacity: 0.8;\n          }\n          50% {\n            transform: translate(-10px, -70px) scale(0.9) rotate(180deg);\n            opacity: 0.6;\n          }\n          75% {\n            transform: translate(20px, -105px) scale(1.2) rotate(270deg);\n            opacity: 0.9;\n          }\n          100% {\n            transform: translate(0, -140px) scale(0.5) rotate(360deg);\n            opacity: 0.3;\n          }\n        }\n      "}</style>
    </div>);
};
// Seasonal Cycles - Representing the eternal rhythm
var SeasonalCycles = function () {
    var _a = (0, react_1.useState)(0), cyclePhase = _a[0], setCyclePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCyclePhase(function (prev) { return (prev + 1) % 360; });
        }, 150);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-25">
      <svg className="w-full h-full">
        {/* Seasonal cycle rings */}
        <circle cx="50%" cy="50%" r="200px" stroke="#f97316" strokeWidth="3" fill="none" opacity="0.4" strokeDasharray="10,5" style={{
            transform: "rotate(".concat(cyclePhase, "deg)"),
            transformOrigin: '50% 50%',
        }}/>
        <circle cx="50%" cy="50%" r="250px" stroke="#3b82f6" strokeWidth="2" fill="none" opacity="0.3" strokeDasharray="15,10" style={{
            transform: "rotate(".concat(-cyclePhase * 0.7, "deg)"),
            transformOrigin: '50% 50%',
        }}/>
        <circle cx="50%" cy="50%" r="300px" stroke="#8b5cf6" strokeWidth="2" fill="none" opacity="0.2" strokeDasharray="20,15" style={{
            transform: "rotate(".concat(cyclePhase * 0.5, "deg)"),
            transformOrigin: '50% 50%',
        }}/>
      </svg>
    </div>);
};
// Endurance Proclamation Banner
var EnduranceProclamation = function () {
    var _a = (0, react_1.useState)(0.8), proclamationSerenity = _a[0], setProclamationSerenity = _a[1];
    var _b = (0, react_1.useState)(1), eternalScale = _b[0], setEternalScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setProclamationSerenity(function (prev) { return (prev === 0.8 ? 1.0 : 0.8); });
            setEternalScale(function (prev) { return (prev === 1 ? 1.08 : 1); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-20 py-10 bg-gradient-to-r from-violet-800/85 via-purple-700/85 to-violet-800/85 rounded-3xl border-4 border-purple-400/75 transition-all duration-5000" style={{
            boxShadow: "0 0 60px rgba(168, 85, 247, ".concat(proclamationSerenity, ")"),
            transform: "scale(".concat(eternalScale, ")"),
        }}>
        <div className="text-5xl text-violet-100 font-bold mb-4">ETERNAL ENDURANCE</div>
        <div className="text-xl text-purple-200 font-semibold mb-2">
          Harvest • Rest • Memory • Covenant
        </div>
        <div className="text-lg text-violet-300">The Codex endures in perfect serenity</div>
      </div>
    </div>);
};
// Seasonal Wisdom Elements - Four aspects of the cycle
var SeasonalWisdomElements = function () {
    var _a = (0, react_1.useState)(0), wisdomPhase = _a[0], setWisdomPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWisdomPhase(function (prev) { return (prev + 1) % 4; });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    var wisdomElements = [
        { name: 'Abundance', icon: '🌾', position: { top: '15%', left: '10%' } },
        { name: 'Reflection', icon: '🌙', position: { top: '15%', right: '10%' } },
        {
            name: 'Remembrance',
            icon: '🧠',
            position: { bottom: '30%', left: '10%' },
        },
        {
            name: 'Permanence',
            icon: '🔒',
            position: { bottom: '30%', right: '10%' },
        },
    ];
    return (<div className="absolute inset-0">
      {wisdomElements.map(function (element, index) { return (<div key={index} className={"absolute text-center transition-all duration-2000 ".concat(wisdomPhase === index ? 'opacity-100 scale-120' : 'opacity-60 scale-90')} style={element.position}>
          <div className={"text-6xl mb-2 transition-all duration-2000 ".concat(wisdomPhase === index ? 'animate-pulse' : '')} style={{
                filter: wisdomPhase === index ? 'drop-shadow(0 0 25px rgba(168, 85, 247, 0.9))' : 'none',
            }}>
            {element.icon}
          </div>
          <div className={"text-lg font-semibold ".concat(wisdomPhase === index ? 'text-violet-200' : 'text-purple-400')}>
            {element.name}
          </div>
        </div>); })}
    </div>);
};
// Main Harvest Serenity Container
var HarvestSerenity = function () {
    return (<div className="relative w-full h-full">
      <SeasonalCycles />
      <HarvestParticles />
      <HarvestRestBalance />
      <MemoryGathered />
      <CovenantSealed />
      <CodexEndurance />
      <SeasonalWisdomElements />
      <EnduranceProclamation />

      {/* Sacred Verse Display */}
      <div className="absolute top-2/3 left-1/2 transform -translate-x-1/2 mt-40">
        <div className="text-center text-violet-100 text-2xl leading-relaxed max-w-4xl space-y-4">
          <p className="opacity-95">Balance of harvest and rest,</p>
          <p className="opacity-90">memory gathered, covenant sealed.</p>
          <p className="text-3xl font-semibold text-purple-200 mt-8 opacity-100">
            So let the Codex endure, eternal and serene.
          </p>
        </div>
      </div>
    </div>);
};
// Main Harvest Serenity Page
var HarvestSerenityPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-violet-900 via-purple-800 to-indigo-900 relative overflow-hidden">
      {/* Seasonal Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-purple-800/40 to-violet-700/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <HarvestSerenity />
        </div>
      </main>

      {/* Ambient Serenity Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-violet-600/15 to-transparent pointer-events-none"/>

      {/* Eternal Harvest Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className="absolute top-1/4 left-1/3 w-88 h-88 bg-violet-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '12s' }}/>
        <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-purple-400/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '16s', animationDelay: '6s' }}/>
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-indigo-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '10s' }}/>
        <div className="absolute bottom-1/2 left-1/4 w-80 h-80 bg-violet-500/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '24s', animationDelay: '14s' }}/>
      </div>
    </div>);
};
exports.default = HarvestSerenityPage;
