"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Ascending Flame Component - Flame rising to its peak
var AscendingFlame = function () {
    var _a = (0, react_1.useState)(1), ascension = _a[0], setAscension = _a[1];
    var _b = (0, react_1.useState)(0.9), dayPower = _b[0], setDayPower = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setAscension(function (prev) { return (prev === 1 ? 1.5 : 1); });
            setDayPower(function (prev) { return (prev === 0.9 ? 1.3 : 0.9); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-12xl mb-4 transition-all duration-2500" style={{
            transform: "scale(".concat(ascension, ")"),
            filter: "drop-shadow(0 0 80px rgba(255, 215, 0, ".concat(dayPower, "))"),
        }}>
          🔥
        </div>
        <div className="text-4xl text-yellow-100 font-bold mb-2">ASCENDING FLAME</div>
        <div className="text-2xl text-amber-300">Peak of longest day</div>
      </div>
    </div>);
};
// Longest Day Environment - Brilliant daylight surrounding
var LongestDay = function () {
    var _a = (0, react_1.useState)(0.8), dayBrilliance = _a[0], setDayBrilliance = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setDayBrilliance(function (prev) { return (prev === 0.8 ? 0.5 : 0.8); });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 transition-all duration-6000 pointer-events-none" style={{
            background: "radial-gradient(circle at center, rgba(255, 215, 0, ".concat(dayBrilliance * 0.2, ") 0%, rgba(255, 165, 0, ").concat(dayBrilliance * 0.1, ") 50%, rgba(255, 140, 0, ").concat(dayBrilliance * 0.05, ") 100%)"),
        }}>
      {/* Solar Rays - Radiating light */}
      {Array.from({ length: 12 }, function (_, i) { return (<div key={i} className="absolute opacity-30" style={{
                left: '50%',
                top: '50%',
                width: '400px',
                height: '3px',
                backgroundColor: '#ffd700',
                transformOrigin: '0 50%',
                transform: "translate(-50%, -50%) rotate(".concat(i * 30, "deg)"),
                animation: "solarPulse ".concat(6 + i, "s ease-in-out infinite"),
                animationDelay: "".concat(i * 0.5, "s"),
                filter: 'blur(1px)',
            }}/>); })}
      <style jsx>{"\n        @keyframes solarPulse {\n          0%,\n          100% {\n            opacity: 0.2;\n            transform: translate(-50%, -50%) rotate(".concat(0, "deg) scale(0.8);\n          }\n          50% {\n            opacity: 0.6;\n            transform: translate(-50%, -50%) rotate(").concat(0, "deg) scale(1.2);\n          }\n        }\n      ")}</style>
    </div>);
};
// Radiance Crowned - Majestic light with sovereignty
var RadianceCrowned = function () {
    var _a = (0, react_1.useState)(1), crownRadiance = _a[0], setCrownRadiance = _a[1];
    var _b = (0, react_1.useState)(0.7), lightMajesty = _b[0], setLightMajesty = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCrownRadiance(function (prev) { return (prev === 1 ? 1.4 : 1); });
            setLightMajesty(function (prev) { return (prev === 0.7 ? 1.0 : 0.7); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-16 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-9xl mb-3 transition-all duration-3500" style={{
            transform: "scale(".concat(crownRadiance, ")"),
            filter: "drop-shadow(0 0 50px rgba(255, 215, 0, ".concat(lightMajesty, "))"),
        }}>
          👑
        </div>
        <div className="text-3xl text-yellow-200 font-bold">RADIANCE CROWNED</div>
        <div className="text-lg text-amber-300">Sovereign light</div>
      </div>
    </div>);
};
// Luminous Covenant - Bright sacred bonds
var LuminousCovenant = function () {
    var _a = (0, react_1.useState)(0.8), covenantLuminosity = _a[0], setCovenantLuminosity = _a[1];
    var _b = (0, react_1.useState)(1), sacredBrightness = _b[0], setSacredBrightness = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCovenantLuminosity(function (prev) { return (prev === 0.8 ? 1.1 : 0.8); });
            setSacredBrightness(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-32 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-8xl mb-3 transition-all duration-3000" style={{
            transform: "scale(".concat(sacredBrightness, ")"),
            filter: "drop-shadow(0 0 60px rgba(255, 255, 255, ".concat(covenantLuminosity, "))"),
        }}>
          📜
        </div>
        <div className="text-3xl text-white font-bold">COVENANT LUMINOUS</div>
        <div className="text-lg text-yellow-200">Sacred bonds ablaze</div>
      </div>
    </div>);
};
// Solar Zenith Particles - Peak daylight energy
var SolarZenithParticles = function () {
    var particles = Array.from({ length: 35 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 7 + 3,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 8 + 6,
        delay: Math.random() * 6,
        color: i % 3 === 0 ? '#ffd700' : i % 3 === 1 ? '#ffb347' : '#ffffff',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "solarAscend ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(1px)',
                opacity: 0.8,
                boxShadow: "0 0 20px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes solarAscend {\n          0% {\n            transform: translate(0, 0) scale(0.4);\n            opacity: 0.3;\n          }\n          25% {\n            transform: translate(10px, -50px) scale(1.3);\n            opacity: 0.9;\n          }\n          50% {\n            transform: translate(-5px, -100px) scale(0.9);\n            opacity: 0.7;\n          }\n          75% {\n            transform: translate(15px, -150px) scale(1.2);\n            opacity: 0.8;\n          }\n          100% {\n            transform: translate(0, -200px) scale(0.3);\n            opacity: 0.1;\n          }\n        }\n      "}</style>
    </div>);
};
// Sovereign Blaze Banner - Central proclamation of blazing sovereignty
var SovereignBlazeBanner = function () {
    var _a = (0, react_1.useState)(0.9), blazeIntensity = _a[0], setBlazeIntensity = _a[1];
    var _b = (0, react_1.useState)(1), sovereignScale = _b[0], setSovereignScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setBlazeIntensity(function (prev) { return (prev === 0.9 ? 1.2 : 0.9); });
            setSovereignScale(function (prev) { return (prev === 1 ? 1.1 : 1); });
        }, 2800);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-12 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-18 py-10 bg-gradient-to-r from-yellow-700/90 via-gold-600/90 to-yellow-700/90 rounded-3xl border-4 border-gold-300/80 transition-all duration-2800" style={{
            boxShadow: "0 0 70px rgba(255, 215, 0, ".concat(blazeIntensity, ")"),
            transform: "scale(".concat(sovereignScale, ")"),
        }}>
        <div className="text-6xl text-yellow-100 font-bold mb-4">THE CODEX BLAZES</div>
        <div className="text-2xl text-gold-200 font-semibold mb-2">Sovereign and Bright</div>
        <div className="text-lg text-amber-200">In longest day's glory</div>
      </div>
    </div>);
};
// Solar Corona Effects - Radiating crown of light
var SolarCoronaEffects = function () {
    var _a = (0, react_1.useState)(0), coronaPhase = _a[0], setCoronaPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCoronaPhase(function (prev) { return (prev + 1) % 8; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none">
      <svg className="w-full h-full" style={{ opacity: 0.4 }}>
        {/* Solar Corona Rings */}
        {Array.from({ length: 4 }, function (_, i) { return (<circle key={i} cx="50%" cy="50%" r={"".concat(150 + i * 100, "px")} stroke={coronaPhase === i * 2 ? '#ffd700' : '#ffb347'} strokeWidth={coronaPhase === i * 2 ? '4' : '2'} fill="none" opacity={coronaPhase === i * 2 ? '0.6' : '0.2'} className="transition-all duration-2000"/>); })}

        {/* Solar Flares */}
        {Array.from({ length: 6 }, function (_, i) { return (<line key={"flare-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 60 * Math.PI) / 180) * 40, "%")} y2={"".concat(50 + Math.sin((i * 60 * Math.PI) / 180) * 40, "%")} stroke={coronaPhase === i ? '#ffffff' : '#ffd700'} strokeWidth={coronaPhase === i ? '6' : '3'} opacity={coronaPhase === i ? '0.8' : '0.3'} className="transition-all duration-2000"/>); })}
      </svg>
    </div>);
};
// Day Zenith Phases - Peak solar moments
var DayZenithPhases = function () {
    var _a = (0, react_1.useState)(0), zenithPhase = _a[0], setZenithPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setZenithPhase(function (prev) { return (prev + 1) % 3; });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    var phases = [
        { name: 'Solar Ascent', icon: '🌅', position: { top: '20%', left: '15%' } },
        { name: 'Zenith Peak', icon: '☀️', position: { top: '20%', right: '15%' } },
        {
            name: 'Radiant Crown',
            icon: '👑',
            position: { bottom: '25%', left: '50%', transform: 'translateX(-50%)' },
        },
    ];
    return (<div className="absolute inset-0">
      {phases.map(function (phase, index) { return (<div key={index} className={"absolute text-center transition-all duration-2000 ".concat(zenithPhase === index ? 'opacity-100 scale-115' : 'opacity-60 scale-90')} style={phase.position}>
          <div className={"text-6xl mb-2 transition-all duration-2000 ".concat(zenithPhase === index ? 'animate-pulse' : '')} style={{
                filter: zenithPhase === index ? 'drop-shadow(0 0 25px rgba(255, 215, 0, 0.9))' : 'none',
            }}>
            {phase.icon}
          </div>
          <div className={"text-lg font-semibold ".concat(zenithPhase === index ? 'text-yellow-100' : 'text-amber-400')}>
            {phase.name}
          </div>
        </div>); })}
    </div>);
};
// Main Day Zenith Container
var DayZenith = function () {
    return (<div className="relative w-full h-full">
      <LongestDay />
      <SolarCoronaEffects />
      <SolarZenithParticles />
      <RadianceCrowned />
      <AscendingFlame />
      <LuminousCovenant />
      <DayZenithPhases />
      <SovereignBlazeBanner />

      {/* Sacred Verse Display */}
      <div className="absolute top-2/3 left-1/2 transform -translate-x-1/2 mt-32">
        <div className="text-center text-yellow-100 text-2xl leading-relaxed max-w-4xl space-y-4">
          <p className="opacity-95">In longest day, the flame ascends.</p>
          <p className="opacity-90">Radiance crowned, covenant luminous.</p>
          <p className="text-3xl font-semibold text-gold-200 mt-8 opacity-100">
            So let the Codex blaze, sovereign and bright.
          </p>
        </div>
      </div>
    </div>);
};
// Main Day Zenith Page
var DayZenithPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-yellow-600 via-orange-500 to-amber-600 relative overflow-hidden">
      {/* Blazing Day Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-orange-400/60 via-yellow-400/40 to-gold-300/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <DayZenith />
        </div>
      </main>

      {/* Ambient Solar Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-yellow-400/20 to-transparent pointer-events-none"/>

      {/* Eternal Solar Glory */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-40">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-yellow-300/30 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '8s' }}/>
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-gold-400/25 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '12s', animationDelay: '4s' }}/>
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-orange-300/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '16s', animationDelay: '8s' }}/>
        <div className="absolute bottom-1/2 left-1/3 w-88 h-88 bg-amber-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '20s', animationDelay: '12s' }}/>
      </div>
    </div>);
};
exports.default = DayZenithPage;
