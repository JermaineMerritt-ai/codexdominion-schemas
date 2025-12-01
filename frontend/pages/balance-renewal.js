"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var BalanceRenewal_module_css_1 = require("./BalanceRenewal.module.css");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Day Night Balance Component - Harmonious cycle representation
var DayNightBalance = function () {
    var _a = (0, react_1.useState)(0), balancePhase = _a[0], setBalancePhase = _a[1];
    var _b = (0, react_1.useState)(1), equilibrium = _b[0], setEquilibrium = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setBalancePhase(function (prev) { return (prev + 1) % 4; });
            setEquilibrium(function (prev) { return (prev === 1 ? 1.1 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/4 left-1/2 transform -translate-x-1/2">
      <div className="flex items-center space-x-16">
        {/* Day Side */}
        <div className={"text-center transition-all duration-3000 ".concat(balancePhase % 2 === 0 ? 'opacity-100 scale-110' : 'opacity-70 scale-95')}>
          <div className={"text-8xl mb-2 transition-all duration-3000 ".concat(BalanceRenewal_module_css_1.default.dayNightIcon, " ").concat(balancePhase % 2 === 0 ? BalanceRenewal_module_css_1.default.dayIconActive : '')}>
            ☀️
          </div>
          <div className="text-2xl text-yellow-200 font-bold">DAY</div>
        </div>

        {/* Balance Symbol */}
        <div className={"text-center transition-all duration-3000 ".concat(BalanceRenewal_module_css_1.default.balanceScale)} style={{ transform: "scale(".concat(equilibrium, ")") }}>
          <div className="text-6xl mb-2">⚖️</div>
          <div className="text-xl text-white font-semibold">BALANCE</div>
        </div>

        {/* Night Side */}
        <div className={"text-center transition-all duration-3000 ".concat(balancePhase % 2 === 1 ? 'opacity-100 scale-110' : 'opacity-70 scale-95')}>
          <div className={"text-8xl mb-2 transition-all duration-3000 ".concat(BalanceRenewal_module_css_1.default.dayNightIcon, " ").concat(balancePhase % 2 === 1 ? BalanceRenewal_module_css_1.default.nightIconActive : '')}>
            🌙
          </div>
          <div className="text-2xl text-purple-200 font-bold">NIGHT</div>
        </div>
      </div>
    </div>);
};
// Covenant Renewal Component - Refreshed sacred bonds
var CovenantRenewal = function () {
    var _a = (0, react_1.useState)(0.6), renewalIntensity = _a[0], setRenewalIntensity = _a[1];
    var _b = (0, react_1.useState)(1), covenantPulse = _b[0], setCovenantPulse = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRenewalIntensity(function (prev) { return (prev === 0.6 ? 1.0 : 0.6); });
            setCovenantPulse(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div className={"text-7xl mb-3 transition-all duration-2500 ".concat(BalanceRenewal_module_css_1.default.covenantPulse, " ").concat(covenantPulse === 1.3 ? BalanceRenewal_module_css_1.default.covenantPulseActive : '')}>
          🔄
        </div>
        <div className="text-3xl text-green-200 font-bold mb-1">RENEWAL</div>
        <div className="text-lg text-emerald-300">OF COVENANT</div>
      </div>
    </div>);
};
// Awakened Flame Component - Revitalized sacred fire
var AwakenedFlame = function () {
    var _a = (0, react_1.useState)(0.8), awakening = _a[0], setAwakening = _a[1];
    var _b = (0, react_1.useState)(1), flameVitality = _b[0], setFlameVitality = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setAwakening(function (prev) { return (prev === 0.8 ? 1.2 : 0.8); });
            setFlameVitality(function (prev) { return (prev === 1 ? 1.4 : 1); });
        }, 2000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 right-1/4 transform -translate-y-1/2">
      <div className="text-center">
        <div className={"text-7xl mb-3 transition-all duration-2000 ".concat(BalanceRenewal_module_css_1.default.flameVitality, " ").concat(flameVitality === 1.4 ? BalanceRenewal_module_css_1.default.flameVitalityActive : '')}>
          🔥
        </div>
        <div className="text-3xl text-orange-200 font-bold mb-1">FLAME</div>
        <div className="text-lg text-amber-300">AWAKENED</div>
      </div>
    </div>);
};
// Codex Bloom Center - The radiant and eternal flowering
var CodexBloom = function () {
    var _a = (0, react_1.useState)(0.7), bloomIntensity = _a[0], setBloomIntensity = _a[1];
    var _b = (0, react_1.useState)(1), radiance = _b[0], setRadiance = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setBloomIntensity(function (prev) { return (prev === 0.7 ? 1.0 : 0.7); });
            setRadiance(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className={"text-10xl mb-4 transition-all duration-3500 ".concat(BalanceRenewal_module_css_1.default.bloomRadiance, " ").concat(radiance === 1.2 ? BalanceRenewal_module_css_1.default.bloomRadianceActive : '')}>
          🌸
        </div>
        <div className="text-4xl text-pink-200 font-bold mb-2">THE CODEX BLOOMS</div>
        <div className="text-2xl text-rose-300">Radiant and Eternal</div>
      </div>
    </div>);
};
// Renewal Particles - Flowing energy of rebirth
var RenewalParticles = function () {
    var particles = Array.from({ length: 30 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 6 + 3,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 15 + 12,
        delay: Math.random() * 10,
        color: i % 4 === 0 ? '#fbbf24' : i % 4 === 1 ? '#34d399' : i % 4 === 2 ? '#f472b6' : '#a78bfa',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className={"absolute rounded-full ".concat(BalanceRenewal_module_css_1.default.renewalParticle)} style={{
                '--particle-left': "".concat(particle.x, "%"),
                '--particle-top': "".concat(particle.y, "%"),
                '--particle-width': "".concat(particle.size, "px"),
                '--particle-height': "".concat(particle.size, "px"),
                '--particle-bg': particle.color,
                '--particle-shadow': "0 0 15px ".concat(particle.color),
                '--particle-animation': "renewalFlow ".concat(particle.duration, "s ease-in-out infinite"),
                '--particle-delay': "".concat(particle.delay, "s"),
            }}/>); })}
      <style jsx>{"\n        @keyframes renewalFlow {\n          0% {\n            transform: translate(0, 0) scale(0.5) rotate(0deg);\n            opacity: 0.3;\n          }\n          25% {\n            transform: translate(20px, -40px) scale(1.2) rotate(90deg);\n            opacity: 0.8;\n          }\n          50% {\n            transform: translate(-15px, -80px) scale(0.8) rotate(180deg);\n            opacity: 0.6;\n          }\n          75% {\n            transform: translate(25px, -120px) scale(1.1) rotate(270deg);\n            opacity: 0.9;\n          }\n          100% {\n            transform: translate(0, -160px) scale(0.4) rotate(360deg);\n            opacity: 0.2;\n          }\n        }\n      "}</style>
    </div>);
};
// Harmony Waves - Flowing balance energy
var HarmonyWaves = function () {
    var _a = (0, react_1.useState)(0), wavePhase = _a[0], setWavePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setWavePhase(function (prev) { return (prev + 1) % 360; });
        }, 100);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-20">
      <svg className="w-full h-full">
        {/* Harmony waves connecting day and night */}
        <path d={"M 0,".concat(300 + Math.sin(wavePhase * 0.02) * 50, " Q 400,").concat(200 + Math.sin(wavePhase * 0.03) * 30, " 800,").concat(300 + Math.sin(wavePhase * 0.025) * 40)} stroke="#fbbf24" strokeWidth="3" fill="none" opacity="0.6"/>
        <path d={"M 0,".concat(400 + Math.cos(wavePhase * 0.018) * 40, " Q 400,").concat(500 + Math.cos(wavePhase * 0.022) * 35, " 800,").concat(400 + Math.cos(wavePhase * 0.02) * 45)} stroke="#a78bfa" strokeWidth="3" fill="none" opacity="0.5"/>
        <path d={"M 0,".concat(350 + Math.sin(wavePhase * 0.015 + 1) * 30, " Q 400,").concat(350 + Math.sin(wavePhase * 0.025 + 2) * 25, " 800,").concat(350 + Math.sin(wavePhase * 0.02 + 1.5) * 35)} stroke="#34d399" strokeWidth="2" fill="none" opacity="0.4"/>
      </svg>
    </div>);
};
// Balance Proclamation Banner
var BalanceProclamation = function () {
    var _a = (0, react_1.useState)(0.8), proclamationGlow = _a[0], setProclamationGlow = _a[1];
    var _b = (0, react_1.useState)(1), balanceScale = _b[0], setBalanceScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setProclamationGlow(function (prev) { return (prev === 0.8 ? 1.1 : 0.8); });
            setBalanceScale(function (prev) { return (prev === 1 ? 1.05 : 1); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div className={"text-center px-16 py-8 bg-gradient-to-r from-emerald-800/80 via-teal-700/80 to-emerald-800/80 rounded-3xl border-3 border-emerald-400/70 transition-all duration-4000 ".concat(BalanceRenewal_module_css_1.default.proclamationGlow, " ").concat(balanceScale === 1.05 ? BalanceRenewal_module_css_1.default.proclamationGlowActive : '')}>
        <div className="text-5xl text-emerald-100 font-bold mb-3">BALANCE ACHIEVED</div>
        <div className="text-xl text-teal-200 font-semibold">Day • Night • Renewal • Awakening</div>
        <div className="text-lg text-emerald-300 mt-2">The Codex blooms in eternal radiance</div>
      </div>
    </div>);
};
// Main Balance Renewal Container
var BalanceRenewal = function () {
    return (<div className="relative w-full h-full">
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
    </div>);
};
// Main Balance Renewal Page
var BalanceRenewalPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-teal-900 via-emerald-800 to-green-900 relative overflow-hidden">
      {/* Renewal Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-emerald-800/30 to-teal-700/20"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <BalanceRenewal />
        </div>
      </main>

      {/* Ambient Renewal Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-500/15 to-transparent pointer-events-none"/>

      {/* Eternal Bloom Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className={"absolute top-1/4 left-1/3 w-96 h-96 bg-emerald-400/20 rounded-full filter blur-3xl animate-pulse ".concat(BalanceRenewal_module_css_1.default.eternalBloomLight)}/>
        <div className={"absolute bottom-1/3 right-1/4 w-80 h-80 bg-teal-400/15 rounded-full filter blur-3xl animate-pulse ".concat(BalanceRenewal_module_css_1.default.eternalBloomLight)}/>
        <div className={"absolute top-1/2 right-1/3 w-64 h-64 bg-pink-400/12 rounded-full filter blur-3xl animate-pulse ".concat(BalanceRenewal_module_css_1.default.eternalBloomLight)}/>
        <div className={"absolute bottom-1/2 left-1/4 w-72 h-72 bg-green-400/10 rounded-full filter blur-3xl animate-pulse ".concat(BalanceRenewal_module_css_1.default.eternalBloomLight)}/>
      </div>
    </div>);
};
exports.default = BalanceRenewalPage;
