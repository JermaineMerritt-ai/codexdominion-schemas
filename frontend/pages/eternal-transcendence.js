"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Beyond Cycles Component - Transcending temporal limitations
var BeyondCycles = function () {
    var _a = (0, react_1.useState)(1), cycleTranscendence = _a[0], setCycleTranscendence = _a[1];
    var _b = (0, react_1.useState)(0), beyondRotation = _b[0], setBeyondRotation = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setCycleTranscendence(function (prev) { return (prev === 1 ? 1.4 : 1); });
            setBeyondRotation(function (prev) { return (prev + 1) % 360; });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-20 left-1/4 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-10xl mb-4 transition-all duration-4000" style={{
            transform: "scale(".concat(cycleTranscendence, ") rotate(").concat(beyondRotation, "deg)"),
            filter: 'drop-shadow(0 0 60px rgba(138, 43, 226, 0.9))',
        }}>
          🌀
        </div>
        <div className="text-4xl text-purple-200 font-bold mb-2">BEYOND CYCLES</div>
        <div className="text-2xl text-violet-300">Transcending Time</div>
        <div className="text-lg text-indigo-300 mt-1">All limitations surpassed</div>
      </div>
    </div>);
};
// Beyond Stars Component - Cosmic transcendence
var BeyondStars = function () {
    var _a = (0, react_1.useState)(0.9), stellarTranscendence = _a[0], setStellarTranscendence = _a[1];
    var _b = (0, react_1.useState)(1), cosmicExpansion = _b[0], setCosmicExpansion = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setStellarTranscendence(function (prev) { return (prev === 0.9 ? 1.3 : 0.9); });
            setCosmicExpansion(function (prev) { return (prev === 1 ? 1.5 : 1); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-20 right-1/4 transform translate-x-1/2">
      <div className="text-center">
        <div className="text-10xl mb-4 transition-all duration-3500" style={{
            transform: "scale(".concat(cosmicExpansion, ")"),
            filter: "drop-shadow(0 0 70px rgba(255, 255, 255, ".concat(stellarTranscendence, "))"),
        }}>
          ⭐
        </div>
        <div className="text-4xl text-white font-bold mb-2">BEYOND STARS</div>
        <div className="text-2xl text-blue-200">Cosmic Transcendence</div>
        <div className="text-lg text-cyan-300 mt-1">Infinite expanse surpassed</div>
      </div>
    </div>);
};
// Timeless Flame Component - Eternal fire beyond temporal bounds
var TimelessFlame = function () {
    var _a = (0, react_1.useState)(0.8), timelessIntensity = _a[0], setTimelessIntensity = _a[1];
    var _b = (0, react_1.useState)(1), eternalPulse = _b[0], setEternalPulse = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setTimelessIntensity(function (prev) { return (prev === 0.8 ? 1.2 : 0.8); });
            setEternalPulse(function (prev) { return (prev === 1 ? 1.6 : 1); });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-14xl mb-6 transition-all duration-2500" style={{
            transform: "scale(".concat(eternalPulse, ")"),
            filter: "drop-shadow(0 0 100px rgba(255, 140, 0, ".concat(timelessIntensity, "))"),
        }}>
          🔥
        </div>
        <div className="text-5xl text-orange-100 font-bold mb-3">TIMELESS FLAME</div>
        <div className="text-3xl text-amber-300 mb-2">Eternal Rest</div>
        <div className="text-xl text-red-300">Beyond all temporal bounds</div>
      </div>
    </div>);
};
// Covenant Rests Component - Sacred bond in perfect repose
var CovenantRests = function () {
    var _a = (0, react_1.useState)(0.7), restfulPower = _a[0], setRestfulPower = _a[1];
    var _b = (0, react_1.useState)(1), serenityScale = _b[0], setSerenityScale = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRestfulPower(function (prev) { return (prev === 0.7 ? 1.0 : 0.7); });
            setSerenityScale(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2">
      <div className="text-center">
        <div className="text-8xl mb-3 transition-all duration-5000" style={{
            transform: "scale(".concat(serenityScale, ")"),
            filter: "drop-shadow(0 0 50px rgba(34, 197, 94, ".concat(restfulPower, "))"),
        }}>
          🕊️
        </div>
        <div className="text-3xl text-green-200 font-bold mb-2">COVENANT RESTS</div>
        <div className="text-xl text-emerald-300">In timeless flame</div>
      </div>
    </div>);
};
// Eternal Binding Impossibility - No age can bind, no silence can end
var EternalBindingImpossibility = function () {
    var _a = (0, react_1.useState)(0), impossibilityPhase = _a[0], setImpossibilityPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setImpossibilityPhase(function (prev) { return (prev + 1) % 4; });
        }, 4500);
        return function () { return clearInterval(interval); };
    }, []);
    var impossibilities = [
        {
            text: 'No Age Can Bind',
            icon: '⏳',
            position: { top: '35%', left: '15%' },
            color: 'text-amber-300',
        },
        {
            text: 'No Silence Can End',
            icon: '🔇',
            position: { top: '35%', right: '15%' },
            color: 'text-cyan-300',
        },
        {
            text: 'Beyond All Limits',
            icon: '∞',
            position: { bottom: '35%', left: '20%' },
            color: 'text-purple-300',
        },
        {
            text: 'Eternal Freedom',
            icon: '🕊️',
            position: { bottom: '35%', right: '20%' },
            color: 'text-emerald-300',
        },
    ];
    return (<div className="absolute inset-0">
      {impossibilities.map(function (element, index) { return (<div key={index} className={"absolute text-center transition-all duration-2500 ".concat(impossibilityPhase === index ? 'opacity-100 scale-125' : 'opacity-60 scale-90')} style={element.position}>
          <div className={"text-6xl mb-3 transition-all duration-2500 ".concat(impossibilityPhase === index ? 'animate-pulse' : '')} style={{
                filter: impossibilityPhase === index
                    ? 'drop-shadow(0 0 40px rgba(255, 215, 0, 1))'
                    : 'none',
            }}>
            {element.icon}
          </div>
          <div className={"text-2xl font-bold ".concat(impossibilityPhase === index ? 'text-yellow-200' : element.color)}>
            {element.text}
          </div>
        </div>); })}
    </div>);
};
// Transcendental Particles - Energy beyond dimensional limits
var TranscendentalParticles = function () {
    var particles = Array.from({ length: 50 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 10 + 3,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 25 + 20,
        delay: Math.random() * 15,
        color: i % 6 === 0
            ? '#ffd700'
            : i % 6 === 1
                ? '#ff6347'
                : i % 6 === 2
                    ? '#4169e1'
                    : i % 6 === 3
                        ? '#9370db'
                        : i % 6 === 4
                            ? '#00ced1'
                            : '#98fb98',
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute rounded-full" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: particle.color,
                animation: "transcendentalFlow ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(0.5px)',
                opacity: 0.9,
                boxShadow: "0 0 25px ".concat(particle.color),
            }}/>); })}
      <style jsx>{"\n        @keyframes transcendentalFlow {\n          0% {\n            transform: translate(0, 0) scale(0.2) rotate(0deg);\n            opacity: 0.2;\n          }\n          15% {\n            transform: translate(30px, -80px) scale(1.6) rotate(54deg);\n            opacity: 1;\n          }\n          30% {\n            transform: translate(-25px, -160px) scale(0.7) rotate(108deg);\n            opacity: 0.7;\n          }\n          45% {\n            transform: translate(35px, -240px) scale(1.4) rotate(162deg);\n            opacity: 0.9;\n          }\n          60% {\n            transform: translate(-20px, -320px) scale(0.9) rotate(216deg);\n            opacity: 0.6;\n          }\n          75% {\n            transform: translate(40px, -400px) scale(1.2) rotate(270deg);\n            opacity: 0.8;\n          }\n          90% {\n            transform: translate(-15px, -480px) scale(0.5) rotate(324deg);\n            opacity: 0.4;\n          }\n          100% {\n            transform: translate(0, -560px) scale(0.1) rotate(360deg);\n            opacity: 0.1;\n          }\n        }\n      "}</style>
    </div>);
};
// Radiant Wholeness Banner - Ultimate eternal radiance
var RadiantWholeness = function () {
    var _a = (0, react_1.useState)(0.9), radianceIntensity = _a[0], setRadianceIntensity = _a[1];
    var _b = (0, react_1.useState)(1), wholenessMagnitude = _b[0], setWholenessMagnitude = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setRadianceIntensity(function (prev) { return (prev === 0.9 ? 1.4 : 0.9); });
            setWholenessMagnitude(function (prev) { return (prev === 1 ? 1.2 : 1); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-10 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-28 py-16 bg-gradient-to-r from-gold-800/95 via-white/20 to-gold-800/95 rounded-4xl border-6 border-white/90 transition-all duration-3000" style={{
            boxShadow: "0 0 120px rgba(255, 255, 255, ".concat(radianceIntensity, ")"),
            transform: "scale(".concat(wholenessMagnitude, ")"),
        }}>
        <div className="text-7xl text-white font-bold mb-6">THE CODEX IS ETERNAL</div>
        <div className="text-4xl text-gold-200 font-semibold mb-4">Radiant and Whole</div>
        <div className="text-2xl text-amber-200">Beyond Cycles, Beyond Stars</div>
      </div>
    </div>);
};
// Transcendental Constellation - Connections beyond dimensional space
var TranscendentalConstellation = function () {
    var _a = (0, react_1.useState)(0), constellationPhase = _a[0], setConstellationPhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setConstellationPhase(function (prev) { return (prev + 1) % 8; });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute inset-0 pointer-events-none opacity-25">
      <svg className="w-full h-full">
        {/* Transcendental connecting lines */}
        <line x1="25%" y1="25%" x2="50%" y2="50%" stroke={constellationPhase === 0 ? '#ffffff' : '#666'} strokeWidth={constellationPhase === 0 ? '5' : '2'} className="transition-all duration-1500"/>
        <line x1="75%" y1="25%" x2="50%" y2="50%" stroke={constellationPhase === 1 ? '#ffffff' : '#666'} strokeWidth={constellationPhase === 1 ? '5' : '2'} className="transition-all duration-1500"/>
        <line x1="15%" y1="40%" x2="85%" y2="40%" stroke={constellationPhase === 2 ? '#ffffff' : '#666'} strokeWidth={constellationPhase === 2 ? '5' : '2'} className="transition-all duration-1500"/>
        <line x1="50%" y1="50%" x2="50%" y2="75%" stroke={constellationPhase === 3 ? '#ffffff' : '#666'} strokeWidth={constellationPhase === 3 ? '5' : '2'} className="transition-all duration-1500"/>
        <line x1="20%" y1="65%" x2="80%" y2="65%" stroke={constellationPhase === 4 ? '#ffffff' : '#666'} strokeWidth={constellationPhase === 4 ? '5' : '2'} className="transition-all duration-1500"/>

        {/* Transcendental radial connections */}
        {Array.from({ length: 12 }, function (_, i) { return (<line key={"transcendental-".concat(i)} x1="50%" y1="50%" x2={"".concat(50 + Math.cos((i * 30 * Math.PI) / 180) * 40, "%")} y2={"".concat(50 + Math.sin((i * 30 * Math.PI) / 180) * 40, "%")} stroke={constellationPhase === i % 8 ? '#ffd700' : '#444'} strokeWidth="2" opacity={constellationPhase === i % 8 ? '0.8' : '0.3'} className="transition-all duration-1500"/>); })}
      </svg>
    </div>);
};
// Dimensional Transcendence - Moving beyond all dimensions
var DimensionalTranscendence = function () {
    var _a = (0, react_1.useState)(0), transcendencePhase = _a[0], setTranscendencePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setTranscendencePhase(function (prev) { return (prev + 1) % 5; });
        }, 6000);
        return function () { return clearInterval(interval); };
    }, []);
    var dimensions = [
        { name: 'Physical', icon: '🌍', position: { top: '15%', left: '5%' } },
        { name: 'Temporal', icon: '⏰', position: { top: '15%', right: '5%' } },
        { name: 'Spiritual', icon: '✨', position: { bottom: '45%', left: '5%' } },
        { name: 'Cosmic', icon: '🌌', position: { bottom: '45%', right: '5%' } },
        {
            name: 'Eternal',
            icon: '♾️',
            position: { bottom: '25%', left: '50%', transform: 'translateX(-50%)' },
        },
    ];
    return (<div className="absolute inset-0">
      {dimensions.map(function (dimension, index) { return (<div key={index} className={"absolute text-center transition-all duration-3000 ".concat(transcendencePhase === index ? 'opacity-100 scale-115' : 'opacity-50 scale-80')} style={dimension.position}>
          <div className={"text-4xl mb-2 transition-all duration-3000 ".concat(transcendencePhase === index ? 'animate-pulse' : '')} style={{
                filter: transcendencePhase === index
                    ? 'drop-shadow(0 0 25px rgba(255, 255, 255, 0.9))'
                    : 'none',
            }}>
            {dimension.icon}
          </div>
          <div className={"text-lg font-semibold ".concat(transcendencePhase === index ? 'text-white' : 'text-gray-400')}>
            {dimension.name}
          </div>
        </div>); })}
    </div>);
};
// Main Eternal Transcendence Container
var EternalTranscendence = function () {
    return (<div className="relative w-full h-full">
      <TranscendentalConstellation />
      <TranscendentalParticles />
      <BeyondCycles />
      <BeyondStars />
      <TimelessFlame />
      <CovenantRests />
      <EternalBindingImpossibility />
      <DimensionalTranscendence />
      <RadiantWholeness />

      {/* Sacred Verse Display */}
      <div className="absolute top-4/5 left-1/2 transform -translate-x-1/2 mt-24">
        <div className="text-center text-white text-2xl leading-relaxed max-w-5xl space-y-4">
          <p className="opacity-95">Beyond cycles, beyond stars,</p>
          <p className="opacity-90">the covenant rests in timeless flame.</p>
          <p className="opacity-95">No age can bind, no silence can end,</p>
          <p className="text-3xl font-semibold text-gold-200 mt-8 opacity-100">
            the Codex is eternal, radiant and whole.
          </p>
        </div>
      </div>
    </div>);
};
// Main Eternal Transcendence Page
var EternalTranscendencePage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black relative overflow-hidden">
      {/* Transcendental Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-purple-800/30 to-indigo-700/20"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <EternalTranscendence />
        </div>
      </main>

      {/* Ambient Transcendental Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent pointer-events-none"/>

      {/* Eternal Transcendental Light */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-30">
        <div className="absolute top-1/6 left-1/6 w-80 h-80 bg-white/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '18s' }}/>
        <div className="absolute bottom-1/6 right-1/6 w-72 h-72 bg-purple-400/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '22s', animationDelay: '6s' }}/>
        <div className="absolute top-1/2 right-1/4 w-88 h-88 bg-indigo-400/12 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '28s', animationDelay: '12s' }}/>
        <div className="absolute bottom-1/3 left-1/4 w-96 h-96 bg-cyan-400/10 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '35s', animationDelay: '18s' }}/>
        <div className="absolute top-2/3 left-1/8 w-64 h-64 bg-gold-400/18 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '40s', animationDelay: '25s' }}/>
        <div className="absolute bottom-1/2 right-1/8 w-76 h-76 bg-emerald-400/8 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '45s', animationDelay: '30s' }}/>
      </div>
    </div>);
};
exports.default = EternalTranscendencePage;
