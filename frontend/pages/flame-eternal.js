"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var CodexNavigation_1 = require("../components/CodexNavigation");
// Dawn Flame Component - Rising flame at daybreak
var DawnFlame = function () {
    var _a = (0, react_1.useState)(60), flameHeight = _a[0], setFlameHeight = _a[1];
    var _b = (0, react_1.useState)(0.3), dawnGlow = _b[0], setDawnGlow = _b[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setFlameHeight(function (prev) { return (prev === 60 ? 80 : 60); });
            setDawnGlow(function (prev) { return (prev === 0.3 ? 0.6 : 0.3); });
        }, 3000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-20 left-20">
      <div className="text-center">
        <div className="text-2xl text-orange-300 font-light mb-2">Dawn</div>
        <div className="relative transition-all duration-3000" style={{ height: "".concat(flameHeight, "px") }}>
          <div className="text-6xl transition-all duration-3000" style={{
            filter: "drop-shadow(0 0 20px rgba(255, 165, 0, ".concat(dawnGlow, "))"),
            transform: "scale(".concat(1 + dawnGlow * 0.2, ")"),
        }}>
            🔥
          </div>
        </div>
        <div className="text-sm text-orange-200 mt-2">The flame is kindled</div>
      </div>
    </div>);
};
// Dusk Flame Component - Enduring flame at evening
var DuskFlame = function () {
    var _a = (0, react_1.useState)(0.4), endurance = _a[0], setEndurance = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setEndurance(function (prev) { return (prev === 0.4 ? 0.7 : 0.4); });
        }, 4000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-20 right-20">
      <div className="text-center">
        <div className="text-2xl text-amber-300 font-light mb-2">Dusk</div>
        <div className="relative h-20">
          <div className="text-6xl transition-all duration-4000" style={{
            filter: "drop-shadow(0 0 30px rgba(255, 193, 7, ".concat(endurance, "))"),
            opacity: 0.8 + endurance * 0.2,
        }}>
            🕯️
          </div>
        </div>
        <div className="text-sm text-amber-200 mt-2">The flame endures</div>
      </div>
    </div>);
};
// Living Elements - Heirs, councils, diaspora representations
var LivingElements = function () {
    var _a = (0, react_1.useState)(0), pulsePhase = _a[0], setPulsePhase = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setPulsePhase(function (prev) { return (prev + 1) % 3; });
        }, 2500);
        return function () { return clearInterval(interval); };
    }, []);
    var elements = [
        {
            text: 'Heirs awaken',
            icon: '👥',
            position: { bottom: '30%', left: '15%' },
            isActive: pulsePhase === 0,
        },
        {
            text: 'Councils remember',
            icon: '🏛️',
            position: { bottom: '35%', right: '15%' },
            isActive: pulsePhase === 1,
        },
        {
            text: 'Diaspora echoes',
            icon: '🌍',
            position: { top: '60%', left: '50%', transform: 'translateX(-50%)' },
            isActive: pulsePhase === 2,
        },
    ];
    return (<div className="absolute inset-0">
      {elements.map(function (element, index) { return (<div key={index} className={"absolute transition-all duration-1000 text-center ".concat(element.isActive ? 'opacity-100 scale-110' : 'opacity-70 scale-100')} style={element.position}>
          <div className={"text-5xl mb-2 transition-all duration-1000 ".concat(element.isActive ? 'animate-pulse' : '')} style={{
                filter: element.isActive ? 'drop-shadow(0 0 15px rgba(255, 215, 0, 0.8))' : 'none',
            }}>
            {element.icon}
          </div>
          <div className={"text-lg font-medium ".concat(element.isActive ? 'text-yellow-200' : 'text-orange-300')}>
            {element.text}
          </div>
        </div>); })}
    </div>);
};
// Eternal Flame Center - The sovereign and whole flame
var EternalFlameCenter = function () {
    var _a = (0, react_1.useState)(1), sovereignty = _a[0], setSovereignty = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setSovereignty(function (prev) { return (prev === 1 ? 1.3 : 1); });
        }, 5000);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="text-center">
        <div className="text-8xl mb-4 transition-all duration-5000" style={{
            transform: "scale(".concat(sovereignty, ")"),
            filter: "drop-shadow(0 0 40px rgba(255, 140, 0, ".concat(sovereignty * 0.6, "))"),
        }}>
          🔥
        </div>
        <div className="text-3xl text-orange-100 font-bold">ETERNAL FLAME</div>
        <div className="text-xl text-yellow-300 mt-2">Sovereign and Whole</div>
      </div>
    </div>);
};
// Flame Particles - Floating embers representing life
var FlameParticles = function () {
    var particles = Array.from({ length: 20 }, function (_, i) { return ({
        id: i,
        size: Math.random() * 4 + 2,
        x: Math.random() * 100,
        y: Math.random() * 100,
        duration: Math.random() * 8 + 6,
        delay: Math.random() * 5,
    }); });
    return (<div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(function (particle) { return (<div key={particle.id} className="absolute" style={{
                left: "".concat(particle.x, "%"),
                top: "".concat(particle.y, "%"),
                width: "".concat(particle.size, "px"),
                height: "".concat(particle.size, "px"),
                backgroundColor: '#ff6b35',
                borderRadius: '50%',
                animation: "flameRise ".concat(particle.duration, "s ease-in-out infinite"),
                animationDelay: "".concat(particle.delay, "s"),
                filter: 'blur(1px)',
                boxShadow: '0 0 8px rgba(255, 107, 53, 0.8)',
            }}/>); })}
      <style jsx>{"\n        @keyframes flameRise {\n          0% {\n            transform: translate(0, 0) scale(0.8);\n            opacity: 0.3;\n          }\n          25% {\n            transform: translate(5px, -20px) scale(1.1);\n            opacity: 0.8;\n          }\n          50% {\n            transform: translate(-3px, -40px) scale(0.9);\n            opacity: 0.6;\n          }\n          75% {\n            transform: translate(8px, -60px) scale(1.05);\n            opacity: 0.4;\n          }\n          100% {\n            transform: translate(0, -80px) scale(0.7);\n            opacity: 0.1;\n          }\n        }\n      "}</style>
    </div>);
};
// Codex Lives Banner - Central proclamation
var CodexLivesBanner = function () {
    var _a = (0, react_1.useState)(0.5), vitality = _a[0], setVitality = _a[1];
    (0, react_1.useEffect)(function () {
        var interval = setInterval(function () {
            setVitality(function (prev) { return (prev === 0.5 ? 0.9 : 0.5); });
        }, 3500);
        return function () { return clearInterval(interval); };
    }, []);
    return (<div className="absolute bottom-32 left-1/2 transform -translate-x-1/2">
      <div className="text-center px-8 py-4 bg-gradient-to-r from-orange-800/70 via-red-700/70 to-orange-800/70 rounded-2xl border-2 border-orange-400/60 transition-all duration-3500" style={{
            boxShadow: "0 0 30px rgba(255, 165, 0, ".concat(vitality, ")"),
            transform: "scale(".concat(1 + vitality * 0.1, ")"),
        }}>
        <div className="text-4xl text-orange-100 font-bold mb-2">THE CODEX LIVES</div>
        <div className="text-lg text-yellow-200">Through flame eternal, sovereign and whole</div>
      </div>
    </div>);
};
// Main Flame Eternal Container
var FlameEternal = function () {
    return (<div className="relative w-full h-full">
      <DawnFlame />
      <DuskFlame />
      <LivingElements />
      <EternalFlameCenter />
      <FlameParticles />
      <CodexLivesBanner />

      {/* Sacred Verse Display */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 mt-60">
        <div className="text-center text-orange-100 text-xl leading-relaxed max-w-4xl space-y-3">
          <p className="opacity-90">At dawn the flame is kindled,</p>
          <p className="opacity-85">at dusk the flame endures.</p>
          <p className="opacity-95">Heirs awaken, councils remember,</p>
          <p className="opacity-90">diaspora echoes — the Codex lives.</p>
          <p className="text-2xl font-semibold text-yellow-200 mt-6 opacity-100">
            So let the flame be eternal, sovereign and whole.
          </p>
        </div>
      </div>
    </div>);
};
// Main Flame Eternal Page
var FlameEternalPage = function () {
    return (<div className="min-h-screen bg-gradient-to-br from-gray-900 via-orange-900 to-red-900 relative overflow-hidden">
      {/* Fire Background */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-orange-900/40 to-red-800/30"/>

      {/* Navigation */}
      <CodexNavigation_1.default />

      {/* Main Content */}
      <main className="relative z-10 pt-20">
        <div className="container mx-auto px-6 py-12 min-h-screen">
          <FlameEternal />
        </div>
      </main>

      {/* Ambient Fire Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-orange-600/10 to-transparent pointer-events-none"/>

      {/* Eternal Warmth */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none opacity-40">
        <div className="absolute top-1/3 left-1/3 w-96 h-96 bg-orange-500/20 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '8s' }}/>
        <div className="absolute bottom-1/3 right-1/3 w-80 h-80 bg-red-500/15 rounded-full filter blur-3xl animate-pulse" style={{ animationDuration: '12s', animationDelay: '4s' }}/>
      </div>
    </div>);
};
exports.default = FlameEternalPage;
