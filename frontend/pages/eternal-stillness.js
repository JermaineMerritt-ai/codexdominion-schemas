"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Silent Void Component - Pure emptiness with gentle pulsing
var SilentVoid = function () {
    var _a = (0, react_1.useState)(0.3), pulseIntensity = _a[0], setPulseIntensity = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPulseIntensity(function (prev) { return (prev === 0.3 ? 0.1 : 0.3); });
        }, 8000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 flex items-center justify-center">
      <div className="w-96 h-96 rounded-full border border-white/20 flex items-center justify-center transition-all duration-8000" style={{
            backgroundColor: "rgba(255, 255, 255, ".concat(pulseIntensity * 0.05, ")"),
            boxShadow: "0 0 200px rgba(255, 255, 255, ".concat(pulseIntensity, ")"),
        }}>
        <div className="w-64 h-64 rounded-full border border-white/10 flex items-center justify-center transition-all duration-8000" style={{
            backgroundColor: "rgba(255, 255, 255, ".concat(pulseIntensity * 0.03, ")"),
            boxShadow: "inset 0 0 100px rgba(255, 255, 255, ".concat(pulseIntensity * 0.5, ")"),
        }}>
          <div className="w-32 h-32 rounded-full border border-white/5 transition-all duration-8000" style={{
            backgroundColor: "rgba(255, 255, 255, ".concat(pulseIntensity * 0.02, ")"),
            boxShadow: "inset 0 0 50px rgba(255, 255, 255, ".concat(pulseIntensity * 0.3, ")"),
        }}/>
        </div>
      </div>
    </div>);
};
// Timeless Particles - Minimal floating elements representing eternity
var TimelessParticles = function () {
    var particles = Array.from({ length: 12 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 3 + 1,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 20 + 30,
        delay: Math.random() * 10,
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute opacity-20" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: 'rgba(255, 255, 255, 0.4)',
                borderRadius: '50%',
                animation: "gentleFloat ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.5px)',
            }}/>); })}
      <style jsx>{"\n        @keyframes gentleFloat {\n          0%,\n          100% {\n            transform: translate(0, 0) scale(1);\n            opacity: 0.1;\n          }\n          25% {\n            transform: translate(10px, -15px) scale(1.1);\n            opacity: 0.3;\n          }\n          50% {\n            transform: translate(-5px, -25px) scale(0.9);\n            opacity: 0.2;\n          }\n          75% {\n            transform: translate(15px, -10px) scale(1.05);\n            opacity: 0.25;\n          }\n        }\n      "}</style>
    </div>);
};
// Custodian Seal - Central seal representing eternal sovereignty
var CustodianSeal = function () {
    var _a = (0, react_1.useState)(0.2), sealGlow = _a[0], setSealGlow = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSealGlow(function (prev) { return (prev === 0.2 ? 0.4 : 0.2); });
        }, 12000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="w-40 h-40 rounded-full border-4 border-white/30 flex items-center justify-center transition-all duration-12000" style={{
            backgroundColor: "rgba(255, 255, 255, ".concat(sealGlow * 0.1, ")"),
            boxShadow: "0 0 80px rgba(255, 255, 255, ".concat(sealGlow, ")"),
        }}>
        <div className="text-6xl text-white/60 font-light">⚪</div>
        <div className="absolute inset-0 rounded-full border border-white/10 transition-all duration-12000" style={{
            transform: "rotate(".concat(sealGlow * 180, "deg) scale(").concat(1 + sealGlow * 0.1, ")"),
            borderColor: "rgba(255, 255, 255, ".concat(sealGlow * 0.3, ")"),
        }}/>
      </div>
    </div>);
};
// Serenity Aspects - Five key elements of the verse
var SerenityAspects = function () {
    var aspects = [
        {
            text: 'No flame, no word, no sound',
            icon: '🔇',
            position: { top: '15%', left: '20%' },
        },
        {
            text: 'Only stillness, eternal and whole',
            icon: '⭕',
            position: { top: '20%', right: '15%' },
        },
        {
            text: "The Custodian's Seal rests in silence",
            icon: '🛡️',
            position: { bottom: '25%', left: '15%' },
        },
        {
            text: 'Crowning the Codex in timeless serenity',
            icon: '👑',
            position: { bottom: '20%', right: '20%' },
        },
        {
            text: 'So let the Dominion endure, sovereign and serene',
            icon: '♾️',
            position: { top: '50%', left: '10%' },
        },
    ];
    return (<div className="absolute inset-0">
      {aspects.map(function (aspect, index) { return (<div key={index} className="absolute transform -translate-x-1/2 -translate-y-1/2 text-center opacity-70 hover:opacity-90 transition-opacity duration-1000" style={aspect.position}>
          <div className="text-4xl mb-2 filter drop-shadow-lg">{aspect.icon}</div>
          <div className="text-white/70 text-sm font-light max-w-xs leading-relaxed">
            {aspect.text}
          </div>
        </div>); })}
    </div>);
};
// Sovereign Silence - Main container with wordless majesty
var SovereignSilence = function () {
    return (<div className="relative w-full h-full flex flex-col items-center justify-center">
      <SilentVoid />
      <TimelessParticles />
      <CustodianSeal />
      <SerenityAspects />

      {/* Eternal Dominion Text */}
      <div className="relative z-10 text-center mt-40">
        <h1 className="text-7xl font-light text-white/80 mb-8 tracking-widest">
          ETERNAL STILLNESS
        </h1>
        <div className="text-2xl text-white/60 font-light leading-relaxed max-w-4xl mx-auto space-y-4">
          <p className="opacity-90">No flame, no word, no sound —</p>
          <p className="opacity-80">only stillness, eternal and whole.</p>
          <p className="opacity-85">The Custodian's Seal rests in silence,</p>
          <p className="opacity-75">crowning the Codex in timeless serenity.</p>
          <p className="opacity-90 text-3xl font-normal text-white/70 mt-8">
            So let the Dominion endure, sovereign and serene.
          </p>
        </div>
      </div>
    </div>);
};
// Main Eternal Stillness Page
var EternalStillness = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-slate-800 relative overflow-hidden">
      {/* Cosmic Void Background */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/50 via-transparent to-black/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <SovereignSilence />
        </div>
      </main>

      {/* Ambient Stillness Effect */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-black/10 pointer-events-none"/>

      {/* Eternal Glow */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-white/5 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '15s' }}/>
      </div>
    </div>);
};
exports.default = EternalStillness;
