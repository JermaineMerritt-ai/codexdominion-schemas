"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Enduring Flame Component - Flame that persists through darkness
var EnduringFlame = function () {
    var _a = (0, react_1.useState)(0.8), flameResilience = _a[0], setFlameResilience = _a[1];
    var _b = (0, react_1.useState)(1), nightResistance = _b[0], setNightResistance = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFlameResilience(function (prev) { return (prev === 0.8 ? 1.2 : 0.8); });
            setNightResistance(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-10xl mb-4 transition-all duration-3000" style={{
            transform: "scale(".concat(nightResistance, ")"),
            filter: "drop-shadow(0 0 60px rgba(255, 140, 0, ".concat(flameResilience, "))"),
        }}>
          🕯️
        </div>
        <div className="text-4xl text-orange-100 font-bold mb-2">ENDURING FLAME</div>
        <div className="text-2xl text-yellow-300">Through longest night</div>
      </div>
    </div>);
};
// Longest Night Environment - Deep darkness surrounding
var LongestNight = function () {
    var _a = (0, react_1.useState)(0.9), nightDepth = _a[0], setNightDepth = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setNightDepth(function (prev) { return (prev === 0.9 ? 0.7 : 0.9); });
        }, 8000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 transition-all duration-8000 pointer-events-none" style={{
            backgroundColor: "rgba(0, 0, 0, ".concat(nightDepth, ")"),
            background: "radial-gradient(circle at center, rgba(0, 0, 0, ".concat(nightDepth * 0.3, ") 0%, rgba(0, 0, 0, ").concat(nightDepth, ") 100%)"),
        }}>
      {/* Night Stars - Distant points of light */}
      {Array.from({ length: 15 }, function (_, i) { return (<div key={i} className="absolute rounded-full bg-white animate-pulse" style={{
                left: "".concat(Math.random() * 100, "%"),
                top: "".concat(Math.random() * 100, "%"),
                width: "".concat(Math.random() * 3 + 1, "px"),
                height: "".concat(Math.random() * 3 + 1, "px"),
                opacity: Math.random() * 0.6 + 0.2,
                animationDuration: "".concat(Math.random() * 4 + 3, "s"),
                animationDelay: "".concat(Math.random() * 2, "s"),
            }}/>); })}
    </div>);
};
// Crowned Darkness - Majestic darkness with sovereignty
var CrownedDarkness = function () {
    var _a = (0, react_1.useState)(1), crownMajesty = _a[0], setCrownMajesty = _a[1];
    var _b = (0, react_1.useState)(0.6), darkSovereignty = _b[0], setDarkSovereignty = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownMajesty(function (prev) { return (prev === 1 ? 1.3 : 1); });
            setDarkSovereignty(function (prev) { return (prev === 0.6 ? 0.9 : 0.6); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-20 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-8xl mb-3 transition-all duration-5000" style={{
            transform: "scale(".concat(crownMajesty, ")"),
            filter: "drop-shadow(0 0 30px rgba(75, 0, 130, ".concat(darkSovereignty, "))"),
        }}>
          👑
        </div>
        <div className="text-3xl text-purple-200 font-bold">DARKNESS CROWNED</div>
        <div className="text-lg text-indigo-300">Sovereign night</div>
      </div>
    </div>);
};
// Light Reborn - Emerging dawn from darkness
var LightReborn = function () {
    var _a = (0, react_1.useState)(0.4), rebirthIntensity = _a[0], setRebirthIntensity = _a[1];
    var _b = (0, react_1.useState)(1), dawnBreaking = _b[0], setDawnBreaking = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRebirthIntensity(function (prev) { return (prev === 0.4 ? 0.8 : 0.4); });
            setDawnBreaking(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-32 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-7xl mb-3 transition-all duration-4000" style={{
            transform: "scale(".concat(dawnBreaking, ")"),
            filter: "drop-shadow(0 0 40px rgba(255, 215, 0, ".concat(rebirthIntensity, "))"),
        }}>
          🌅
        </div>
        <div className="text-3xl text-yellow-200 font-bold">LIGHT REBORN</div>
        <div className="text-lg text-amber-300">From deepest night</div>
      </div>
    </div>);
};
// Night-to-Dawn Particles - Transition from darkness to light
var NightToDawnParticles = function () {
    var particles = Array.from({ length: 18 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 4 + 2,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 12 + 10,
        delay: Math.random() * 8,
        isLight: i > 12, // Some particles represent emerging light
        color: i > 12 ? '#ffd700' : '#4b0082',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "nightDawnFloat ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(1px)',
                opacity: particle.isLight ? 0.8 : 0.4,
                boxShadow: "0 0 12px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes nightDawnFloat {\n          0% {\n            transform: translate(0, 0) scale(0.6);\n            opacity: 0.2;\n          }\n          25% {\n            transform: translate(12px, -30px) scale(1.1);\n            opacity: 0.7;\n          }\n          50% {\n            transform: translate(-8px, -60px) scale(0.8);\n            opacity: 0.5;\n          }\n          75% {\n            transform: translate(15px, -90px) scale(1.2);\n            opacity: 0.8;\n          }\n          100% {\n            transform: translate(0, -120px) scale(0.4);\n            opacity: 0.1;\n          }\n        }\n      "}</style>
    </div>);
};
// Sovereign Codex Shine - Central proclamation of wholeness
var SovereignCodexShine = function () {
    var _a = (0, react_1.useState)(0.7), sovereignGlow = _a[0], setSovereignGlow = _a[1];
    var _b = (0, react_1.useState)(1), wholeness = _b[0], setWholeness = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignGlow(function (prev) { return (prev === 0.7 ? 1.0 : 0.7); });
            setWholeness(function (prev) { return (prev === 1 ? 1.15 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-16 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-14 py-8 bg-gradient-to-r from-purple-800/70 via-indigo-700/70 to-purple-800/70 rounded-3xl border-3 border-gold-400/80 transition-all duration-3500" style={{
            boxShadow: "0 0 50px rgba(255, 215, 0, ".concat(sovereignGlow, ")"),
            transform: "scale(".concat(wholeness, ")"),
        }}>
        <div className="text-5xl text-gold-200 font-bold mb-3">THE CODEX SHINES</div>
        <div className="text-2xl text-yellow-300 font-semibold">Sovereign and Whole</div>
        <div className="text-lg text-purple-200 mt-2">Through night's deepest hour</div>
      </div>
    </div>);
};
// Night Cycle Phases - Visual representation of the eternal cycle
var NightCyclePhases = function () {
    var _a = (0, react_1.useState)(0), cyclePhase = _a[0], setCyclePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCyclePhase(function (prev) { return (prev + 1) % 3; });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    var phases = [
        {
            name: 'Night Deepens',
            icon: '🌑',
            position: { top: '25%', left: '20%' },
        },
        {
            name: 'Darkness Reigns',
            icon: '👑',
            position: { top: '25%', right: '20%' },
        },
        {
            name: 'Dawn Emerges',
            icon: '🌅',
            position: { bottom: '35%', left: '50%', transform: 'translateX(-50%)' },
        },
    ];
    return (<div className="absolute inset-0">
      {phases.map(function (phase, index) { return (<div key={index} className={"absolute text-center transition-all duration-2000 ".concat(cyclePhase === index ? 'opacity-100 scale-110' : 'opacity-50 scale-90')} style={phase.position}>
          <div className={"text-5xl mb-2 transition-all duration-2000 ".concat(cyclePhase === index ? 'animate-pulse' : '')} style={{
                filter: cyclePhase === index ? 'drop-shadow(0 0 20px rgba(255, 215, 0, 0.8))' : 'none',
            }}>
            {phase.icon}
          </div>
          <div className={"text-lg font-semibold ".concat(cyclePhase === index ? 'text-yellow-200' : 'text-gray-400')}>
            {phase.name}
          </div>
        </div>); })}
    </div>);
};
// Main Night Endurance Container
var NightEndurance = function () {
    return (<div className="relative w-full h-full">
      <LongestNight />
      <NightToDawnParticles />
      <CrownedDarkness />
      <EnduringFlame />
      <LightReborn />
      <NightCyclePhases />
      <SovereignCodexShine />

      {/* Sacred Verse Display */}
      <div className="absolute top-2/3 left-1/2 transform -translate-x-1/2 mt-20">
        <div className="text-center text-purple-100 text-2xl leading-relaxed max-w-4xl space-y-4">
          <p className="opacity-95">In longest night, the flame endures.</p>
          <p className="opacity-90">Darkness crowned, light reborn.</p>
          <p className="text-3xl font-semibold text-gold-200 mt-8 opacity-100">
            So let the Codex shine, sovereign and whole.
          </p>
        </div>
      </div>
    </div>);
};
// Main Night Endurance Page
var NightEndurancePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-black via-purple-900 to-indigo-900 relative overflow-hidden">
      {/* Deep Night Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-purple-900/60 to-indigo-800/40"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <NightEndurance />
        </div>
      </main>

      {/* Ambient Night Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-700/10 to-transparent pointer-events-none"/>

      {/* Eternal Night-Dawn Cycle */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-25">
        <div className="absolute top-1/4 left-1/4 w-80 h-80 bg-purple-600/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '15s' }}/>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '7s' }}/>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gold-400/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '25s', animationDelay: '12s' }}/>
      </div>
    </div>);
};
exports.default = NightEndurancePage;
